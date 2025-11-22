#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AuDeRe (Action Understanding and Derivation) 模块
提供高级动作理解、推导和优化功能，增强动作序列生成能力
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import json
import re
import logging
from pathlib import Path
import numpy as np
from collections import defaultdict

# 导入action_data中的类
from .action_data import Action, ActionSequence, ActionType, ActionStatus

@dataclass
class ActionPattern:
    """动作模式类"""
    pattern_id: str
    pattern_name: str
    action_template: str
    parameters: List[str]
    condition_templates: List[str] = None
    effect_templates: List[str] = None
    confidence: float = 0.9
    frequency: int = 1
    examples: List[str] = None
    
    def __post_init__(self):
        if self.condition_templates is None:
            self.condition_templates = []
        if self.effect_templates is None:
            self.effect_templates = []
        if self.examples is None:
            self.examples = []

@dataclass
class AudereConfig:
    """AuDeRe模块配置类"""
    enable_pattern_recognition: bool = True
    enable_action_derivation: bool = True
    enable_action_optimization: bool = True
    pattern_confidence_threshold: float = 0.7
    derivation_max_depth: int = 3
    optimization_iterations: int = 2
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_caching: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AudereConfig':
        """从字典创建配置"""
        return cls(**config_dict)

class AuDeRe:
    """动作理解和推导引擎"""
    
    def __init__(self, config: Optional[AudereConfig] = None):
        """
        初始化AuDeRe引擎
        
        Args:
            config: AuDeRe配置
        """
        self.config = config or AudereConfig()
        
        # 设置日志
        if self.config.enable_logging:
            self._setup_logging()
        
        # 动作模式库
        self.action_patterns = []
        self.pattern_index = defaultdict(list)  # 用于快速查找模式
        
        # 初始化内置模式
        self._init_builtin_patterns()
        
        # 缓存
        self._cache = {} if self.config.enable_caching else None
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("AuDeRe")
        self.logger.info("AuDeRe engine initialized")
    
    def _init_builtin_patterns(self):
        """初始化内置动作模式"""
        # 基本动作模式
        basic_patterns = [
            ActionPattern(
                pattern_id="P001",
                pattern_name="pick_up_object",
                action_template="pick_up({object})",
                parameters=["object"],
                condition_templates=["at({agent}, {location})", "at({object}, {location})"],
                effect_templates=["holding({agent}, {object})", "not at({object}, {location})"],
                examples=["pick up the cup", "grab the book", "take the phone"]
            ),
            ActionPattern(
                pattern_id="P002",
                pattern_name="put_down_object",
                action_template="put_down({object}, {location})",
                parameters=["object", "location"],
                condition_templates=["holding({agent}, {object})", "at({agent}, {location})"],
                effect_templates=["not holding({agent}, {object})", "at({object}, {location})"],
                examples=["put down the cup on table", "place the book on shelf"]
            ),
            ActionPattern(
                pattern_id="P003",
                pattern_name="move_to_location",
                action_template="move_to({location})",
                parameters=["location"],
                condition_templates=["at({agent}, {current_location})"],
                effect_templates=["at({agent}, {location})", "not at({agent}, {current_location})"],
                examples=["walk to kitchen", "go to bedroom", "move to living room"]
            ),
            ActionPattern(
                pattern_id="P004",
                pattern_name="open_object",
                action_template="open({object})",
                parameters=["object"],
                condition_templates=["at({agent}, {location})", "at({object}, {location})"],
                effect_templates=["is_open({object})"],
                examples=["open the door", "open the window", "open the box"]
            ),
            ActionPattern(
                pattern_id="P005",
                pattern_name="close_object",
                action_template="close({object})",
                parameters=["object"],
                condition_templates=["at({agent}, {location})", "at({object}, {location})", "is_open({object})"],
                effect_templates=["not is_open({object})"],
                examples=["close the door", "close the window", "close the box"]
            )
        ]
        
        # 添加内置模式
        for pattern in basic_patterns:
            self.add_action_pattern(pattern)
    
    def add_action_pattern(self, pattern: ActionPattern):
        """
        添加动作模式
        
        Args:
            pattern: 动作模式对象
        """
        self.action_patterns.append(pattern)
        
        # 更新模式索引
        for example in pattern.examples:
            # 提取关键词作为索引
            keywords = set(re.findall(r'\b\w+\b', example.lower()))
            for keyword in keywords:
                self.pattern_index[keyword].append(len(self.action_patterns) - 1)
    
    def recognize_action_patterns(self, natural_language_action: str) -> List[Tuple[ActionPattern, float]]:
        """
        从自然语言动作中识别动作模式
        
        Args:
            natural_language_action: 自然语言动作描述
            
        Returns:
            List[Tuple[ActionPattern, float]]: 识别出的模式及其置信度
        """
        # 检查缓存
        if self._cache is not None:
            cache_key = f"pattern_recognition:{natural_language_action}"
            if cache_key in self._cache:
                return self._cache[cache_key]
        
        # 提取关键词
        action_lower = natural_language_action.lower()
        keywords = set(re.findall(r'\b\w+\b', action_lower))
        
        # 查找匹配的模式
        pattern_scores = {}
        
        # 1. 使用关键词匹配
        for keyword in keywords:
            if keyword in self.pattern_index:
                for pattern_idx in self.pattern_index[keyword]:
                    pattern = self.action_patterns[pattern_idx]
                    # 计算匹配分数
                    score = self._calculate_pattern_match_score(pattern, action_lower, keywords)
                    if score >= self.config.pattern_confidence_threshold:
                        if pattern_idx not in pattern_scores or score > pattern_scores[pattern_idx]:
                            pattern_scores[pattern_idx] = score
        
        # 2. 排序并返回结果
        results = sorted(
            [(self.action_patterns[idx], score) for idx, score in pattern_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        # 更新缓存
        if self._cache is not None:
            self._cache[f"pattern_recognition:{natural_language_action}"] = results
        
        return results
    
    def _calculate_pattern_match_score(self, pattern: ActionPattern, action_text: str, keywords: set) -> float:
        """
        计算动作模式与文本的匹配分数
        
        Args:
            pattern: 动作模式
            action_text: 动作文本
            keywords: 关键词集合
            
        Returns:
            float: 匹配分数 (0-1)
        """
        # 示例匹配分数
        example_scores = []
        for example in pattern.examples:
            example_lower = example.lower()
            # 计算词重叠比例
            example_keywords = set(re.findall(r'\b\w+\b', example_lower))
            overlap = keywords.intersection(example_keywords)
            if example_keywords:
                overlap_ratio = len(overlap) / len(example_keywords)
                example_scores.append(overlap_ratio)
        
        # 平均示例分数
        avg_example_score = sum(example_scores) / len(example_scores) if example_scores else 0
        
        # 模式名称匹配
        name_match = 0
        pattern_name_parts = pattern.pattern_name.split('_')
        for part in pattern_name_parts:
            if part in action_text:
                name_match += 0.2
        name_match = min(name_match, 0.5)  # 最高0.5分
        
        # 综合分数
        total_score = (avg_example_score * 0.5) + name_match
        return min(total_score, 1.0)
    
    def derive_new_action(self, base_action: Action, derivation_rules: List[Dict[str, Any]]) -> List[Action]:
        """
        从基础动作推导出新动作
        
        Args:
            base_action: 基础动作
            derivation_rules: 推导规则列表
            
        Returns:
            List[Action]: 推导出的新动作列表
        """
        derived_actions = []
        
        # 应用推导规则
        for rule in derivation_rules:
            if self._should_apply_rule(base_action, rule):
                new_action = self._apply_derivation_rule(base_action, rule)
                if new_action:
                    derived_actions.append(new_action)
        
        return derived_actions
    
    def _should_apply_rule(self, action: Action, rule: Dict[str, Any]) -> bool:
        """
        检查是否应该应用推导规则
        
        Args:
            action: 动作
            rule: 推导规则
            
        Returns:
            bool: 是否应用规则
        """
        # 检查规则条件
        if 'conditions' in rule:
            for condition in rule['conditions']:
                # 检查动作类型条件
                if 'action_type' in condition and action.action_type != condition['action_type']:
                    return False
                
                # 检查动作名称条件
                if 'action_name' in condition:
                    name_pattern = condition['action_name']
                    if not re.search(name_pattern, action.name):
                        return False
                
                # 检查参数条件
                if 'parameters' in condition:
                    for param_name, param_condition in condition['parameters'].items():
                        if param_name not in action.parameters:
                            return False
                        if 'pattern' in param_condition and not re.search(param_condition['pattern'], action.parameters[param_name]):
                            return False
        
        return True
    
    def _apply_derivation_rule(self, action: Action, rule: Dict[str, Any]) -> Optional[Action]:
        """
        应用推导规则生成新动作
        
        Args:
            action: 原始动作
            rule: 推导规则
            
        Returns:
            Optional[Action]: 新动作，失败时返回None
        """
        try:
            # 创建新动作数据
            new_action_data = {
                'name': action.name,
                'action_type': action.action_type,
                'parameters': action.parameters.copy(),
                'preconditions': action.preconditions.copy(),
                'effects': action.effects.copy(),
                'estimated_duration': action.estimated_duration,
                'cost': action.cost,
                'success_rate': action.success_rate
            }
            
            # 应用修改
            if 'modifications' in rule:
                for modification in rule['modifications']:
                    if 'name' in modification:
                        new_action_data['name'] = modification['name'].format(**action.parameters)
                    
                    if 'action_type' in modification:
                        new_action_data['action_type'] = modification['action_type']
                    
                    if 'parameters' in modification:
                        for param_name, param_value in modification['parameters'].items():
                            if isinstance(param_value, str):
                                new_action_data['parameters'][param_name] = param_value.format(**action.parameters)
                            else:
                                new_action_data['parameters'][param_name] = param_value
                    
                    if 'preconditions' in modification:
                        new_action_data['preconditions'].extend(modification['preconditions'])
                    
                    if 'effects' in modification:
                        new_action_data['effects'].extend(modification['effects'])
                    
                    if 'estimated_duration' in modification:
                        new_action_data['estimated_duration'] *= modification['estimated_duration']
                    
                    if 'cost' in modification:
                        new_action_data['cost'] *= modification['cost']
            
            # 创建新动作
            return Action(**new_action_data)
            
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error applying derivation rule: {str(e)}")
            return None
    
    def optimize_action_sequence(self, sequence: ActionSequence, optimization_goals: Dict[str, Any]) -> ActionSequence:
        """
        优化动作序列
        
        Args:
            sequence: 原始动作序列
            optimization_goals: 优化目标
            
        Returns:
            ActionSequence: 优化后的动作序列
        """
        # 检查缓存
        if self._cache is not None:
            cache_key = f"optimize_sequence:{hash(str(sequence.actions))}:{hash(str(optimization_goals))}"
            if cache_key in self._cache:
                return self._cache[cache_key]
        
        optimized_actions = sequence.actions.copy()
        
        # 执行优化迭代
        for _ in range(self.config.optimization_iterations):
            # 1. 消除冗余动作
            optimized_actions = self._remove_redundant_actions(optimized_actions)
            
            # 2. 根据优化目标调整动作顺序
            if optimization_goals.get('minimize_duration', False):
                optimized_actions = self._sort_by_duration(optimized_actions)
            
            if optimization_goals.get('minimize_cost', False):
                optimized_actions = self._sort_by_cost(optimized_actions)
            
            if optimization_goals.get('maximize_success_rate', False):
                optimized_actions = self._prioritize_high_success_rate(optimized_actions)
        
        # 创建优化后的序列
        optimized_sequence = ActionSequence(
            id=f"{sequence.id}_optimized",
            actions=optimized_actions,
            initial_state=sequence.initial_state,
            goal_state=sequence.goal_state
        )
        
        # 更新缓存
        if self._cache is not None:
            cache_key = f"optimize_sequence:{hash(str(sequence.actions))}:{hash(str(optimization_goals))}"
            self._cache[cache_key] = optimized_sequence
        
        return optimized_sequence
    
    def _remove_redundant_actions(self, actions: List[Action]) -> List[Action]:
        """
        移除冗余动作
        
        Args:
            actions: 动作列表
            
        Returns:
            List[Action]: 移除冗余后的动作列表
        """
        if not actions:
            return []
        
        # 简单的冗余检测：相同动作连续执行
        filtered_actions = [actions[0]]
        
        for action in actions[1:]:
            # 检查是否与前一个动作完全相同
            prev_action = filtered_actions[-1]
            if not self._are_actions_identical(action, prev_action):
                filtered_actions.append(action)
        
        return filtered_actions
    
    def _are_actions_identical(self, action1: Action, action2: Action) -> bool:
        """
        检查两个动作是否完全相同
        
        Args:
            action1: 第一个动作
            action2: 第二个动作
            
        Returns:
            bool: 是否相同
        """
        return (
            action1.name == action2.name and
            action1.action_type == action2.action_type and
            action1.parameters == action2.parameters
        )
    
    def _sort_by_duration(self, actions: List[Action]) -> List[Action]:
        """
        按持续时间排序动作
        
        Args:
            actions: 动作列表
            
        Returns:
            List[Action]: 排序后的动作列表
        """
        # 短持续时间的动作优先，处理estimated_duration为None的情况
        return sorted(actions, key=lambda a: a.estimated_duration if a.estimated_duration is not None else float('inf'))
    
    def _sort_by_cost(self, actions: List[Action]) -> List[Action]:
        """
        按成本排序动作
        
        Args:
            actions: 动作列表
            
        Returns:
            List[Action]: 排序后的动作列表
        """
        # 低成本动作优先，使用duration作为替代成本指标
        return sorted(actions, key=lambda a: a.duration)
    
    def _prioritize_high_success_rate(self, actions: List[Action]) -> List[Action]:
        """
        优先安排成功率高的动作
        
        Args:
            actions: 动作列表
            
        Returns:
            List[Action]: 排序后的动作列表
        """
        # 成功率高的动作优先，使用success_probability属性
        return sorted(actions, key=lambda a: a.success_probability, reverse=True)
    
    def interpret_natural_language_goal(self, goal_text: str) -> Dict[str, Any]:
        """
        解释自然语言目标，提取状态信息
        
        Args:
            goal_text: 自然语言目标文本
            
        Returns:
            Dict[str, Any]: 目标状态信息
        """
        # 这里实现简单的目标解析
        interpreted_goal = {}
        
        # 检查缓存
        if self._cache is not None:
            cache_key = f"interpret_goal:{goal_text}"
            if cache_key in self._cache:
                return self._cache[cache_key]
        
        # 简单目标模式匹配
        patterns = [
            (r'(.*) on (.*)', lambda m: {f"on({m.group(1)},{m.group(2)})": True}),
            (r'(.*) in (.*)', lambda m: {f"in({m.group(1)},{m.group(2)})": True}),
            (r'open (.*)', lambda m: {f"is_open({m.group(1)})": True}),
            (r'close (.*)', lambda m: {f"is_open({m.group(1)})": False}),
            (r'(.*) holding (.*)', lambda m: {f"holding({m.group(1)},{m.group(2)})": True}),
            (r'(.*) at (.*)', lambda m: {f"at({m.group(1)},{m.group(2)})": True})
        ]
        
        for pattern, handler in patterns:
            match = re.search(pattern, goal_text.lower())
            if match:
                interpreted_goal.update(handler(match))
        
        # 更新缓存
        if self._cache is not None:
            self._cache[f"interpret_goal:{goal_text}"] = interpreted_goal
        
        return interpreted_goal
    
    def generate_action_suggestions(self, current_state: Dict[str, Any], goal_state: Dict[str, Any], 
                                  available_actions: List[Action], top_n: int = 5) -> List[Tuple[Action, float]]:
        """
        生成动作建议
        
        Args:
            current_state: 当前状态
            goal_state: 目标状态
            available_actions: 可用动作列表
            top_n: 返回前N个建议
            
        Returns:
            List[Tuple[Action, float]]: 动作建议及得分
        """
        # 计算每个动作的建议得分
        action_scores = []
        
        for action in available_actions:
            # 检查动作是否可执行
            if not action.can_execute(current_state):
                continue
            
            # 模拟执行动作
            try:
                next_state = action.execute(current_state.copy())
                
                # 计算与目标状态的接近程度
                proximity_score = self._calculate_state_proximity(next_state, goal_state)
                
                # 考虑动作成功率和成本
                overall_score = proximity_score * action.success_rate / (action.cost + 1.0)  # +1避免除零
                
                action_scores.append((action, overall_score))
                
            except Exception:
                # 动作执行失败，跳过
                continue
        
        # 按得分排序并返回前N个
        action_scores.sort(key=lambda x: x[1], reverse=True)
        return action_scores[:top_n]
    
    def _calculate_state_proximity(self, state: Dict[str, Any], goal_state: Dict[str, Any]) -> float:
        """
        计算状态与目标状态的接近程度
        
        Args:
            state: 当前状态
            goal_state: 目标状态
            
        Returns:
            float: 接近度得分 (0-1)
        """
        if not goal_state:
            return 0.0
        
        # 计算匹配的状态数量
        matched = 0
        total = len(goal_state)
        
        for key, goal_value in goal_state.items():
            if key in state and state[key] == goal_value:
                matched += 1
        
        return matched / total if total > 0 else 0.0
    
    def save_patterns(self, file_path: str):
        """
        保存动作模式到文件
        
        Args:
            file_path: 文件路径
        """
        try:
            patterns_data = [asdict(pattern) for pattern in self.action_patterns]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(patterns_data, f, indent=2, ensure_ascii=False)
            
            if hasattr(self, 'logger'):
                self.logger.info(f"Saved {len(self.action_patterns)} action patterns to {file_path}")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to save action patterns: {str(e)}")
            raise
    
    def load_patterns(self, file_path: str):
        """
        从文件加载动作模式
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                patterns_data = json.load(f)
            
            # 清除现有模式
            self.action_patterns = []
            self.pattern_index = defaultdict(list)
            
            # 加载新模式
            for pattern_data in patterns_data:
                pattern = ActionPattern(**pattern_data)
                self.add_action_pattern(pattern)
            
            if hasattr(self, 'logger'):
                self.logger.info(f"Loaded {len(self.action_patterns)} action patterns from {file_path}")
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to load action patterns: {str(e)}")
            raise
    
    def clear_cache(self):
        """清空缓存"""
        if self._cache is not None:
            self._cache.clear()
            if hasattr(self, 'logger'):
                self.logger.info("AuDeRe cache cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息
        
        Returns:
            Dict[str, Any]: 包含统计信息的字典
        """
        return {
            'pattern_count': len(self.action_patterns),
            'cache_enabled': self.config.enable_caching,
            'cache_size': len(self._cache) if self._cache is not None else 0,
            'config': {
                'enable_pattern_recognition': self.config.enable_pattern_recognition,
                'enable_action_derivation': self.config.enable_action_derivation,
                'enable_action_optimization': self.config.enable_action_optimization
            }
        }

# 创建导出的公共接口
def create_aude_re(config: Optional[Dict[str, Any]] = None) -> AuDeRe:
    """
    创建AuDeRe实例的工厂函数
    
    Args:
        config: 配置字典
        
    Returns:
        AuDeRe: AuDeRe实例
    """
    if config:
        audere_config = AudereConfig.from_dict(config)
        return AuDeRe(audere_config)
    return AuDeRe()