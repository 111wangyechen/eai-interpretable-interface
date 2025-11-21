#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InterPreT集成版目标解释器
实现从语言反馈学习符号谓词构建PDDL域的功能
"""

import re
import json
import sys
import os
import time
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .goal_interpreter import GoalInterpreter, LTLFormula
    from .nlp_parser import NLPParser
    from .ltl_generator import LTLGenerator
    from .ltl_validator import LTLValidator
    from .data_loader import ParquetDataLoader
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from goal_interpreter import GoalInterpreter, LTLFormula
    from nlp_parser import NLPParser
    from ltl_generator import LTLGenerator
    from ltl_validator import LTLValidator
    from data_loader import ParquetDataLoader


@dataclass
class FeedbackRecord:
    """反馈记录类"""
    # 兼容测试脚本的参数结构
    goal: Optional[str] = None  # 从测试脚本传入
    user_feedback: Optional[str] = None  # 从测试脚本传入
    corrected_predicate: Optional[str] = None  # 从测试脚本传入
    
    # 原有参数结构
    text: str = ""
    initial_formula: str = ""
    refined_formula: str = ""
    feedback_type: str = "correction"  # "positive", "negative", "correction"
    feedback_content: str = ""
    timestamp: float = 0.0
    confidence: float = 0.9
    
    def __post_init__(self):
        # 初始化兼容性转换
        if self.goal:
            self.text = self.goal
        if self.user_feedback:
            self.feedback_content = self.user_feedback
        if not self.timestamp:
            self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SymbolicPredicate:
    """符号谓词类"""
    name: str
    # 兼容测试脚本的参数名
    arguments: Optional[List[str]] = None  # 从测试脚本传入
    parameters: Optional[List[str]] = None  # 原有参数名
    arity: int = 0
    description: str = ""
    confidence: float = 0.9
    examples: List[str] = None
    
    def __post_init__(self):
        # 初始化兼容性转换
        if self.examples is None:
            self.examples = []
        # 使用arguments或parameters
        if self.arguments:
            self.parameters = self.arguments
        if not self.parameters:
            self.parameters = []
        # 计算arity
        self.arity = len(self.parameters)
    
    def to_pddl(self) -> str:
        """转换为PDDL格式"""
        params_str = " ".join([f"?{p}" for p in self.parameters])
        return f"({self.name} {params_str})"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PDDLDomain:
    """PDDL域类"""
    name: str
    requirements: List[str]
    types: List[str]
    predicates: List[SymbolicPredicate]
    actions: List[Dict[str, Any]]
    
    def to_pddl_string(self) -> str:
        """生成PDDL域文件内容"""
        lines = []
        lines.append(f"(define (domain {self.name})")
        
        # Requirements
        if self.requirements:
            req_str = " ".join(self.requirements)
            lines.append(f"  (:requirements :{req_str})")
        
        # Types
        if self.types:
            types_str = " ".join(self.types)
            lines.append(f"  (:types {types_str})")
        
        # Predicates
        if self.predicates:
            lines.append("  (:predicates")
            for pred in self.predicates:
                lines.append(f"    {pred.to_pddl()}")
            lines.append("  )")
        
        # Actions
        for action in self.actions:
            lines.append(f"  (:action {action['name']}")
            lines.append(f"    :parameters ({action['parameters']})")
            if action.get('precondition'):
                lines.append(f"    :precondition {action['precondition']}")
            if action.get('effect'):
                lines.append(f"    :effect {action['effect']}")
            lines.append("  )")
        
        lines.append(")")
        return "\n".join(lines)


class InterPreTFeedbackLearner:
    """InterPreT反馈学习器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化反馈学习器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 学习参数
        self.learning_rate = self.config.get('learning_rate', 0.001)
        self.max_iterations = self.config.get('max_iterations', 5)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.8)
        
        # 反馈缓冲区
        self.feedback_buffer: List[FeedbackRecord] = []
        self.buffer_size = self.config.get('buffer_size', 1000)
        
        # 谓词学习
        self.predicate_patterns: Dict[str, List[str]] = defaultdict(list)
        self.predicate_confidence: Dict[str, float] = defaultdict(float)
        
        # 统计信息
        self.learning_stats = {
            'total_feedback': 0,
            'positive_feedback': 0,
            'negative_feedback': 0,
            'correction_feedback': 0,
            'predicates_learned': 0
        }
    
    def add_feedback(self, record: FeedbackRecord):
        """添加反馈记录"""
        self.feedback_buffer.append(record)
        
        # 保持缓冲区大小
        if len(self.feedback_buffer) > self.buffer_size:
            self.feedback_buffer.pop(0)
        
        # 更新统计信息
        self.learning_stats['total_feedback'] += 1
        self.learning_stats[f'{record.feedback_type}_feedback'] += 1
        
        # 学习谓词模式
        self._learn_from_feedback(record)
    
    def _learn_from_feedback(self, record: FeedbackRecord):
        """从反馈中学习"""
        if record.feedback_type == "correction":
            # 从纠正反馈中提取谓词模式
            self._extract_predicate_patterns(record)
        elif record.feedback_type == "positive":
            # 强化正确的模式
            self._reinforce_patterns(record)
    
    def _extract_predicate_patterns(self, record: FeedbackRecord):
        """提取谓词模式"""
        # 简单的模式提取：从文本中识别动词-名词组合
        words = record.text.lower().split()
        for i, word in enumerate(words):
            if word in ['pick', 'place', 'move', 'open', 'close', 'clean']:
                if i + 1 < len(words):
                    predicate = f"{word}_{words[i+1]}"
                    self.predicate_patterns[predicate].append(record.text)
                    self.predicate_confidence[predicate] += self.learning_rate
    
    def _reinforce_patterns(self, record: FeedbackRecord):
        """强化正确的模式"""
        # 基于正面反馈增强置信度
        for predicate in self.predicate_patterns:
            if any(word in record.text.lower() for word in predicate.split('_')):
                self.predicate_confidence[predicate] += self.learning_rate * 0.5
    
    def learn_from_feedback(self, feedback: FeedbackRecord) -> Optional[SymbolicPredicate]:
        """从反馈中学习谓词（测试脚本调用的方法）"""
        # 添加反馈记录
        self.add_feedback(feedback)
        
        # 如果有corrected_predicate，创建对应的SymbolicPredicate
        if feedback.corrected_predicate:
            # 简单解析corrected_predicate来创建SymbolicPredicate
            # 格式如: is_red(book)
            match = re.match(r'(\w+)\(([^)]+)\)', feedback.corrected_predicate)
            if match:
                name = match.group(1)
                args = [arg.strip() for arg in match.group(2).split(',')]
                
                # 创建并返回新的谓词
                new_predicate = SymbolicPredicate(
                    name=name,
                    parameters=args,
                    arity=len(args),
                    description=f"{name} predicate",
                    confidence=feedback.confidence,
                    examples=[feedback.text] if feedback.text else []
                )
                
                # 更新统计信息
                self.learning_stats['predicates_learned'] += 1
                
                return new_predicate
        
        # 如果没有明确的corrected_predicate，返回None
        return None
    
    def get_learned_predicates(self) -> List[SymbolicPredicate]:
        """获取学习到的谓词"""
        predicates = []
        for predicate_name, confidence in self.predicate_confidence.items():
            if confidence >= self.confidence_threshold:
                parts = predicate_name.split('_')
                if len(parts) >= 2:
                    pred = SymbolicPredicate(
                        name=predicate_name,
                        parameters=[f"obj_{i}" for i in range(len(parts)-1)],
                        arity=len(parts)-1,
                        description=f"Learned predicate for {predicate_name}",
                        confidence=confidence,
                        examples=self.predicate_patterns[predicate_name][:3]
                    )
                    predicates.append(pred)
        
        return predicates
    
    def refine_formula(self, original_formula: str, feedback: str) -> str:
        """基于反馈优化公式"""
        # 简单的优化策略：基于反馈内容调整操作符
        refined = original_formula
        
        if "always" in feedback.lower():
            if "G " not in refined:
                refined = f"G ({refined})"
        elif "eventually" in feedback.lower():
            if "F " not in refined:
                refined = f"F ({refined})"
        
        return refined


class PDDLDomainBuilder:
    """PDDL域构建器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化PDDL域构建器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 构建参数
        self.use_llm = self.config.get('use_llm', True)
        self.llm_model = self.config.get('llm_model', 'gpt-3.5-turbo')
        self.temperature = self.config.get('temperature', 0.7)
        self.max_tokens = self.config.get('max_tokens', 1000)
    
    def build_domain(self, ltl_formula: LTLFormula, 
                    learned_predicates: List[SymbolicPredicate]) -> PDDLDomain:
        """
        构建PDDL域
        
        Args:
            ltl_formula: LTL公式
            learned_predicates: 学习到的谓词列表
            
        Returns:
            PDDLDomain: 构建的PDDL域
        """
        domain_name = f"domain_{int(time.time())}"
        
        # 基础要求
        requirements = ["strips", "typing"]
        
        # 基础类型
        types = ["object", "location", "agent"]
        
        # 合并基础谓词和学习到的谓词
        base_predicates = self._get_base_predicates()
        all_predicates = base_predicates + learned_predicates
        
        # 生成动作
        actions = self._generate_actions(all_predicates, ltl_formula)
        
        return PDDLDomain(
            name=domain_name,
            requirements=requirements,
            types=types,
            predicates=all_predicates,
            actions=actions
        )
    
    def _get_base_predicates(self) -> List[SymbolicPredicate]:
        """获取基础谓词"""
        return [
            SymbolicPredicate(
                name="at",
                parameters=["agent", "location"],
                arity=2,
                description="Agent is at location",
                confidence=1.0,
                examples=["agent at kitchen", "robot at living room"]
            ),
            SymbolicPredicate(
                name="holding",
                parameters=["agent", "object"],
                arity=2,
                description="Agent is holding object",
                confidence=1.0,
                examples=["holding cup", "robot holding book"]
            ),
            SymbolicPredicate(
                name="on",
                parameters=["object", "surface"],
                arity=2,
                description="Object is on surface",
                confidence=1.0,
                examples=["book on table", "cup on counter"]
            ),
            SymbolicPredicate(
                name="is_clean",
                parameters=["object"],
                arity=1,
                description="Object is clean",
                confidence=1.0,
                examples=["table is clean", "floor is clean"]
            )
        ]
    
    def _generate_actions(self, predicates: List[SymbolicPredicate], 
                        ltl_formula: LTLFormula) -> List[Dict[str, Any]]:
        """生成动作定义"""
        actions = []
        
        # 基础移动动作
        actions.append({
            'name': 'move',
            'parameters': '?agent - agent ?from - location ?to - location',
            'precondition': '(and (at ?agent ?from))',
            'effect': '(and (not (at ?agent ?from)) (at ?agent ?to))'
        })
        
        # 基础抓取动作
        actions.append({
            'name': 'pick',
            'parameters': '?agent - agent ?object - object ?location - location',
            'precondition': '(and (at ?agent ?location) (on ?object ?location))',
            'effect': '(and (not (on ?object ?location)) (holding ?agent ?object))'
        })
        
        # 基础放置动作
        actions.append({
            'name': 'place',
            'parameters': '?agent - agent ?object - object ?location - location',
            'precondition': '(and (at ?agent ?location) (holding ?agent ?object))',
            'effect': '(and (not (holding ?agent ?object)) (on ?object ?location))'
        })
        
        # 清洁动作（如果有清洁相关谓词）
        clean_predicates = [p for p in predicates if 'clean' in p.name.lower()]
        if clean_predicates:
            actions.append({
                'name': 'clean',
                'parameters': '?agent - agent ?object - object ?location - location',
                'precondition': '(and (at ?agent ?location) (on ?object ?location))',
                'effect': '(is_clean ?object)'
            })
        
        return actions


class InterpretableGoalInterpreter(GoalInterpreter):
    """可解释的目标解释器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化解释器
        
        Args:
            config: 配置参数
        """
        # 调用父类初始化，只传递use_data_loader参数
        super().__init__(use_data_loader=True)
        
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 初始化反馈学习器
        self.feedback_learner = InterPreTFeedbackLearner(config)
        
        # 初始化PDDL域构建器
        self.domain_builder = PDDLDomainBuilder(config)
        
        # 交互式学习配置
        self.enable_interactive_learning = self.config.get('enable_interactive_learning', True)
        self.max_feedback_iterations = self.config.get('max_feedback_iterations', 5)
        
        # 解释统计
        self.interpretation_stats = {
            'total_interpretations': 0,
            'successful_interpretations': 0,
            'feedback_iterations_used': 0,
            'domains_generated': 0
        }
        
        # 学习的谓词
        self.learned_predicates: List[SymbolicPredicate] = []
    
    def interpret_with_feedback(self, text: str, 
                               feedback_history: Optional[List[Dict]] = None) -> Tuple[LTLFormula, PDDLDomain]:
        """
        带反馈的目标解释
        
        Args:
            text: 输入文本
            feedback_history: 反馈历史
            
        Returns:
            Tuple[LTLFormula, PDDLDomain]: LTL公式和PDDL域
        """
        self.interpretation_stats['total_interpretations'] += 1
        
        try:
            # 1. 初始解释
            initial_formula = self.interpret(text)
            current_formula = initial_formula
            
            # 2. 交互式优化
            if self.enable_interactive_learning and feedback_history:
                current_formula = self._interactive_refinement(current_formula, feedback_history)
            
            # 3. 构建PDDL域
            learned_predicates = self.feedback_learner.get_learned_predicates()
            pddl_domain = self.domain_builder.build_domain(current_formula, learned_predicates)
            
            # 4. 更新统计信息
            if current_formula.is_valid():
                self.interpretation_stats['successful_interpretations'] += 1
            self.interpretation_stats['domains_generated'] += 1
            
            return current_formula, pddl_domain
            
        except Exception as e:
            self.logger.error(f"Interpretation with feedback failed: {e}")
            # 返回默认结果
            default_formula = LTLFormula("True", {"error": str(e), "original_text": text})
            default_domain = self.domain_builder.build_domain(default_formula, [])
            return default_formula, default_domain
    
    def _interactive_refinement(self, initial_formula: LTLFormula, 
                              feedback_history: List[Dict]) -> LTLFormula:
        """交互式优化"""
        current_formula = initial_formula
        iterations_used = 0
        
        for feedback in feedback_history[:self.max_feedback_iterations]:
            # 创建反馈记录
            feedback_record = FeedbackRecord(
                text=feedback.get('text', ''),
                initial_formula=current_formula.formula,
                refined_formula=current_formula.formula,
                feedback_type=feedback.get('type', 'positive'),
                feedback_content=feedback.get('content', ''),
                timestamp=time.time(),
                confidence=feedback.get('confidence', 0.5)
            )
            
            # 添加到学习器
            self.feedback_learner.add_feedback(feedback_record)
            
            # 优化公式
            refined_formula_str = self.feedback_learner.refine_formula(
                current_formula.formula, 
                feedback.get('content', '')
            )
            
            # 创建新的公式对象
            refined_formula = LTLFormula(
                refined_formula_str, 
                current_formula.semantics
            )
            
            if refined_formula.is_valid():
                current_formula = refined_formula
            
            iterations_used += 1
        
        self.interpretation_stats['feedback_iterations_used'] += iterations_used
        return current_formula
    
    def add_feedback(self, text: str, formula: LTLFormula, 
                    feedback_type: str, feedback_content: str, 
                    confidence: float = 0.5):
        """添加反馈"""
        feedback_record = FeedbackRecord(
            text=text,
            initial_formula=formula.formula,
            refined_formula=formula.formula,
            feedback_type=feedback_type,
            feedback_content=feedback_content,
            timestamp=time.time(),
            confidence=confidence
        )
        
        self.feedback_learner.add_feedback(feedback_record)
    
    def _update_statistics(self, goal: str, interpretation: Any, success: bool):
        """更新统计信息（测试脚本调用的方法）"""
        # 这个方法会被测试脚本调用
        self.interpretation_stats['total_interpretations'] += 1
        if success:
            self.interpretation_stats['successful_interpretations'] += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取解释器统计信息"""
        # 为了兼容测试，添加total_tasks, successful_tasks, success_rate字段
        total_tasks = self.interpretation_stats['total_interpretations']
        successful_tasks = self.interpretation_stats['successful_interpretations']
        success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0.0
        
        return {
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'success_rate': success_rate,
            'interpretation_stats': self.interpretation_stats,
            'learning_stats': self.feedback_learner.learning_stats,
            'learned_predicates_count': len(self.learned_predicates)
        }
    
    def save_learned_predicates(self, filepath: str):
        """保存学习到的谓词"""
        predicates = self.feedback_learner.get_learned_predicates()
        predicates_data = [pred.to_dict() for pred in predicates]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(predicates_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved {len(predicates)} learned predicates to {filepath}")
    
    def load_learned_predicates(self, filepath: str):
        """加载学习到的谓词"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                predicates_data = json.load(f)
            
            for pred_data in predicates_data:
                predicate = SymbolicPredicate(**pred_data)
                self.feedback_learner.predicate_patterns[predicate.name] = predicate.examples
                self.feedback_learner.predicate_confidence[predicate.name] = predicate.confidence
            
            self.logger.info(f"Loaded {len(predicates_data)} learned predicates from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to load learned predicates: {e}")
    
    def interpret_goal(self, goal_text: str) -> Dict[str, Any]:
        """
        解释目标文本，返回解释结果字典
        
        Args:
            goal_text: 目标文本
            
        Returns:
            Dict[str, Any]: 包含公式和语义的结果字典
        """
        # 使用interpret方法生成LTL公式
        ltl_formula = self.interpret(goal_text)
        
        # 返回格式化结果
        return {
            'formula': ltl_formula.formula,
            'semantics': ltl_formula.semantics,
            'is_valid': ltl_formula.is_valid()
        }
    
    def interpret_from_text(self, text: str) -> LTLFormula:
        """
        从文本解释目标，提供额外的文本处理
        
        Args:
            text: 输入文本
            
        Returns:
            LTLFormula: LTL公式对象
        """
        # 预处理文本
        processed_text = self._preprocess(text)
        
        # 使用现有interpret方法
        return self.interpret(processed_text)
    
    def extract_symbols(self, text: str) -> List[str]:
        """
        从文本中提取符号谓词
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 提取的符号谓词列表
        """
        # 简单的符号提取实现
        symbols = []
        
        # 从文本中提取动词-名词组合作为候选谓词
        words = text.lower().split()
        for i, word in enumerate(words):
            if word in ['pick', 'place', 'move', 'open', 'close', 'clean', 'grab', 'put']:
                if i + 1 < len(words):
                    symbol = f"{word}_{words[i+1]}"
                    symbols.append(symbol)
        
        return symbols
    
    def generate_domain_from_goal(self, goal_text: str) -> PDDLDomain:
        """
        从目标文本直接生成PDDL域
        
        Args:
            goal_text: 目标文本
            
        Returns:
            PDDLDomain: PDDL域对象
        """
        # 解释目标
        ltl_formula = self.interpret(goal_text)
        
        # 获取学习到的谓词
        learned_predicates = self.feedback_learner.get_learned_predicates()
        
        # 构建PDDL域
        return self.domain_builder.build_domain(ltl_formula, learned_predicates)


# 使用示例和测试
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建配置
    config = {
        'interpretable': {
            'enabled': True,
            'max_feedback_iterations': 3,
            'interactive_learning': {
                'enabled': True,
                'feedback_buffer_size': 100
            },
            'pddl_domain': {
                'auto_generate': True,
                'use_llm': False
            }
        }
    }
    
    # 创建解释器
    interpreter = InterpretableGoalInterpreter(config)
    
    # 测试文本
    test_text = "Pick up the cup from the table and place it in the kitchen"
    
    # 模拟反馈历史
    feedback_history = [
        {
            'text': test_text,
            'type': 'positive',
            'content': 'The interpretation is correct',
            'confidence': 0.8
        },
        {
            'text': test_text,
            'type': 'correction',
            'content': 'Add temporal constraint: eventually the cup should be in kitchen',
            'confidence': 0.9
        }
    ]
    
    # 执行解释
    ltl_formula, pddl_domain = interpreter.interpret_with_feedback(test_text, feedback_history)
    
    print("=== LTL Formula ===")
    print(f"Formula: {ltl_formula.formula}")
    print(f"Valid: {ltl_formula.is_valid()}")
    
    print("\n=== PDDL Domain ===")
    print(pddl_domain.to_pddl_string())
    
    print("\n=== Statistics ===")
    stats = interpreter.get_statistics()
    print(json.dumps(stats, indent=2))