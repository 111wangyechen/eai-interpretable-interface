#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标解释器核心类
负责将自然语言转换为LTL公式，支持parquet数据集处理
"""

import re
import json
import sys
import os
from typing import Dict, List, Optional, Tuple, Union

# 添加当前目录到Python路径以支持相对导入
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .nlp_parser import NLPParser
    from .ltl_generator import LTLGenerator
    from .ltl_validator import LTLValidator
    from .data_loader import ParquetDataLoader
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from nlp_parser import NLPParser
    from ltl_generator import LTLGenerator
    from ltl_validator import LTLValidator
    from data_loader import ParquetDataLoader


class LTLFormula:
    """
    LTL公式类，表示线性时序逻辑公式，包含语义信息
    """
    
    def __init__(self, formula: str, semantics: Optional[Dict] = None):
        """
        初始化LTL公式
        
        Args:
            formula: LTL公式字符串
            semantics: 公式的语义信息，包含原始文本和命题等
        """
        self.formula = formula
        self.semantics = semantics or {}
        self.valid = False
        self._validate()
    
    def _validate(self) -> bool:
        """
        验证LTL公式的有效性
        
        Returns:
            bool: 公式是否有效
        """
        # 简单的有效性检查
        try:
            # 检查括号匹配
            parentheses = []
            for char in self.formula:
                if char == '(':
                    parentheses.append(char)
                elif char == ')':
                    if not parentheses:
                        return False
                    parentheses.pop()
            
            self.valid = len(parentheses) == 0
            return self.valid
        except Exception:
            return False
    
    def __str__(self) -> str:
        """
        返回LTL公式字符串
        """
        return self.formula
    
    def is_valid(self) -> bool:
        """
        检查公式是否有效
        """
        return self.valid


class GoalInterpreter:
    """
    目标解释器类，负责将自然语言转换为LTL公式，支持parquet数据集处理
    """
    
    def __init__(self, use_data_loader: bool = False):
        """
        初始化目标解释器
        
        Args:
            use_data_loader: 是否使用数据加载器处理parquet数据
        """
        # 初始化组件
        self.nlp_parser = NLPParser()
        self.semantic_mapper = None
        self.ltl_generator = LTLGenerator()
        self.ltl_validator = LTLValidator()
        
        # 如果需要使用数据加载器
        self.data_loader = None
        if use_data_loader:
            self.data_loader = ParquetDataLoader()
        
        # 初始化内部映射和规则
        self._init_rules()
    
    def _init_rules(self):
        """
        初始化语义映射规则
        """
        # 时间操作符映射
        self.temporal_operators = {
            "总是": "□",  # 全局/总是
            "最终": "◇",  # 最终/终于
            "直到": "U",  # 直到
            "下一个": "X"  # 下一个
        }
        
        # 逻辑操作符映射
        self.logical_operators = {
            "并且": "∧",  # 合取
            "或者": "∨",  # 析取
            "非": "¬",   # 否定
            "蕴含": "→"  # 蕴含
        }
        
        # 关键词模式
        self.keyword_patterns = {
            "最终": r"(最终|最终要|最终需要|最终必须|终将|最后)",
            "总是": r"(总是|始终|一直|永远)",
            "直到": r"(直到|在.*之前)",
            "条件": r"(如果|当.*时|在.*的情况下)",
            "顺序": r"(然后|接着|之后|下一步)",
            "完成": r"(完成|结束|达成|实现)",
            "避免": r"(避免|不要|禁止|防止)",
            "优先": r"(首先|优先|第一步)",
        }
    
    def interpret(self, text: str) -> LTLFormula:
        """
        解释自然语言文本，生成LTL公式
        
        Args:
            text: 输入的自然语言文本
            
        Returns:
            LTLFormula: 生成的LTL公式对象
        """
        try:
            # 1. 预处理文本
            processed_text = self._preprocess(text)
            
            # 2. 解析语义
            semantics = self._parse_semantics(processed_text)
            
            # 3. 生成LTL公式
            ltl_string = self._generate_ltl(semantics)
            
            # 4. 验证生成的公式（如果验证器可用）
            if self.ltl_validator:
                try:
                    self.ltl_validator.validate(ltl_string)
                except Exception as e:
                    print(f"警告: LTL公式验证失败: {e}")
                    # 验证失败不阻止返回，仍返回生成的公式
            
            # 5. 创建LTL公式对象
            ltl_formula = LTLFormula(ltl_string, semantics)
            
            # 验证公式
            self.validate_ltl(ltl_formula)
            
            return ltl_formula
        except Exception as e:
            # 如果转换失败，返回一个基本的错误公式
            error_semantics = {"error": str(e), "original_text": text}
            error_formula = LTLFormula("True", error_semantics)
            error_formula.valid = False
            return error_formula
    
    def interpret_from_dataset(self, dataset: str = "all", limit: Optional[int] = None) -> List[Dict]:
        """
        从parquet数据集批量解释自然语言到LTL公式
        
        Args:
            dataset: 数据集名称('behavior', 'virtualhome'或'all')
            limit: 处理的最大样本数量
            
        Returns:
            包含原始文本、生成公式和评估结果的列表
        """
        # 确保数据加载器存在并已加载数据
        if not self.data_loader:
            print("初始化数据加载器...")
            self.data_loader = ParquetDataLoader()
        
        # 显式加载数据
        print(f"加载{dataset}数据集...")
        try:
            self.data_loader.load_data(dataset)
        except Exception as e:
            print(f"警告: 数据加载异常: {e}")
        
        # 检查数据是否已加载
        if dataset == 'behavior' and self.data_loader.behavior_data is None:
            print("错误: Behavior数据集未成功加载")
        if dataset == 'virtualhome' and self.data_loader.virtualhome_data is None:
            print("错误: Virtualhome数据集未成功加载")
        if dataset == 'all' and self.data_loader.behavior_data is None and self.data_loader.virtualhome_data is None:
            print("错误: 所有数据集都未成功加载")
            return []
        
        # 获取自然语言和TL目标的配对
        print("获取数据对...")
        pairs = self.data_loader.get_nl_tl_pairs(dataset, limit)
        
        # 如果没有获取到数据对，尝试直接从dataframe中提取
        if not pairs:
            print("警告: 未获取到数据对，尝试直接从dataframe中提取...")
            pairs = self._extract_nl_tl_directly(dataset, limit)
        
        print(f"找到 {len(pairs)} 个数据对")
        
        results = []
        for i, (nl_text, actual_tl) in enumerate(pairs, 1):
            print(f"处理样本 {i}/{len(pairs)}: {nl_text[:50]}...")
            
            try:
                # 生成LTL公式
                ltl_formula = self.interpret(nl_text)
                
                # 验证生成的公式
                is_valid, error_msg = self.ltl_validator.is_valid(ltl_formula.formula) if self.ltl_validator else (ltl_formula.is_valid(), "")
                
                results.append({
                    'natural_language': nl_text,
                    'generated_ltl': ltl_formula.formula,
                    'actual_tl': actual_tl,
                    'is_valid': is_valid,
                    'error_message': error_msg,
                    'semantics': ltl_formula.semantics
                })
                
            except Exception as e:
                results.append({
                    'natural_language': nl_text,
                    'generated_ltl': "Error",
                    'actual_tl': actual_tl,
                    'is_valid': False,
                    'error_message': str(e),
                    'semantics': None
                })
        
        return results
    
    def _extract_nl_tl_directly(self, dataset: str = "all", limit: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        直接从dataframe中提取自然语言和TL目标的配对
        当get_nl_tl_pairs方法失败时使用此备用方法
        
        Args:
            dataset: 数据集名称
            limit: 返回的最大配对数量
            
        Returns:
            (自然语言描述, TL目标)配对列表
        """
        pairs = []
        count = 0
        
        # 尝试直接从dataframe中提取数据
        try:
            if dataset in ['behavior', 'all'] and self.data_loader.behavior_data is not None:
                for _, row in self.data_loader.behavior_data.iterrows():
                    # 检查必要的列是否存在
                    if 'natural_language_description' in row and 'tl_goal' in row:
                        pairs.append((row['natural_language_description'], row['tl_goal']))
                        count += 1
                        if limit and count >= limit:
                            return pairs
            
            if dataset in ['virtualhome', 'all'] and self.data_loader.virtualhome_data is not None:
                for _, row in self.data_loader.virtualhome_data.iterrows():
                    # 检查必要的列是否存在
                    if 'natural_language_description' in row and 'tl_goal' in row:
                        pairs.append((row['natural_language_description'], row['tl_goal']))
                        count += 1
                        if limit and count >= limit:
                            return pairs
        except Exception as e:
            print(f"直接提取数据失败: {e}")
        
        return pairs
    
    def compare_with_dataset(self, output_file: str = "comparison_results.json", dataset: str = "all", limit: int = 20) -> Dict:
        """
        比较生成的LTL公式与数据集中的实际TL目标
        
        Args:
            output_file: 结果输出文件
            dataset: 数据集名称
            limit: 处理的样本数量
            
        Returns:
            包含评估统计信息的字典
        """
        results = self.interpret_from_dataset(dataset, limit)
        
        # 统计信息
        total = len(results)
        valid_count = sum(1 for r in results if r['is_valid'])
        error_count = sum(1 for r in results if r['error_message'])
        
        stats = {
            'total_samples': total,
            'valid_formulas': valid_count,
            'error_count': error_count,
            'valid_rate': valid_count / total if total > 0 else 0
        }
        
        # 保存结果
        output_data = {
            'stats': stats,
            'results': results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"比较结果已保存到 {output_file}")
        print(f"统计信息: 总样本数={total}, 有效公式数={valid_count}, 有效率={stats['valid_rate']:.2f}")
        
        return stats
    
    def _preprocess(self, text: str) -> str:
        """
        预处理自然语言文本
        
        Args:
            text: 原始文本
            
        Returns:
            str: 预处理后的文本
        """
        # 去除多余空格和特殊字符
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # 转换为小写
        text = text.lower()
        
        return text
    
    def _parse_semantics(self, text: str) -> Dict:
        """
        解析自然语言的语义结构
        
        Args:
            text: 预处理后的文本
            
        Returns:
            Dict: 语义结构字典
        """
        # 使用NLP解析器进行详细解析
        if self.nlp_parser:
            semantics = self.nlp_parser.parse(text)
        else:
            # 回退到简单解析
            semantics = {
                "original_text": text,
                "propositions": [],
                "temporal_operators": [],
                "logical_operators": [],
                "structure": "simple",
                "actions": [],
                "objects": [],
                "temporal_info": [],
                "conditions": [],
                "constraints": [],
                "task_type": "简单任务"
            }
            
            # 提取命题（简化处理）
            for keyword, pattern in self.keyword_patterns.items():
                if re.search(pattern, text):
                    semantics["temporal_operators"].append(keyword)
            
            proposition_patterns = [
                r'(\w+)\s+(\w+)',  # 简单动宾结构
            ]
            
            for pattern in proposition_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    proposition = "_".join(match)
                    semantics["propositions"].append(proposition)
        
        return semantics
    
    def _generate_ltl(self, semantics: Dict) -> str:
        """
        根据语义结构生成LTL公式
        
        Args:
            semantics: 解析后的语义结构
            
        Returns:
            str: 生成的LTL公式
        """
        # 使用LTL生成器生成公式
        if self.ltl_generator:
            return self.ltl_generator.generate(semantics)
        
        # 简化的回退方案
        ltl_formula = ""
        
        # 提取关键信息
        propositions = semantics.get("propositions", [])
        temporal_operators = semantics.get("temporal_operators", [])
        structure = semantics.get("structure", "simple")
        
        # 根据结构类型生成不同的公式
        if structure == "sequential" and len(propositions) >= 2:
            # 顺序结构: F(p1 -> F(p2 -> ...))
            ltl_formula = propositions[-1]
            for prop in reversed(propositions[:-1]):
                ltl_formula = f"({prop} -> F({ltl_formula}))"
            ltl_formula = f"F({ltl_formula})"
        
        elif structure == "conditional" and len(propositions) >= 2:
            # 条件结构: G(p1 -> F(p2))
            ltl_formula = f"G({propositions[0]} -> F({propositions[1]}))"
        
        elif len(propositions) > 0:
            # 简单结构，使用第一个命题
            if temporal_operators and temporal_operators[0] in self.temporal_operators:
                operator = self.temporal_operators[temporal_operators[0]]
                ltl_formula = f"{operator}({propositions[0]})"
            else:
                ltl_formula = propositions[0]
        
        else:
            # 默认公式
            ltl_formula = "True"
        
        return ltl_formula
    
    def validate_ltl(self, ltl_formula: LTLFormula) -> bool:
        """
        验证LTL公式的有效性
        
        Args:
            ltl_formula: LTL公式对象
            
        Returns:
            bool: 公式是否有效
        """
        if self.ltl_validator:
            is_valid, error_msg = self.ltl_validator.is_valid(ltl_formula.formula)
            ltl_formula.valid = is_valid
            if not is_valid and 'error' not in ltl_formula.semantics:
                ltl_formula.semantics['error'] = error_msg
            return is_valid
        return ltl_formula.is_valid()
    
    def get_supported_temporal_operators(self) -> Dict[str, str]:
        """
        获取支持的时间操作符
        
        Returns:
            Dict: 自然语言到LTL操作符的映射
        """
        return self.temporal_operators
    
    def get_supported_logical_operators(self) -> Dict[str, str]:
        """
        获取支持的逻辑操作符
        
        Returns:
            Dict: 自然语言到逻辑操作符的映射
        """
        return self.logical_operators