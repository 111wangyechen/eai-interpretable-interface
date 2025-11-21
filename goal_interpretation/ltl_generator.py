#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LTL公式生成器
负责将解析后的语义结构转换为LTL公式
"""

from typing import Dict, List, Optional, Union


class LTLGenerator:
    """
    LTL公式生成器类
    根据解析后的语义结构生成对应的LTL公式
    """
    
    def __init__(self):
        """
        初始化LTL生成器
        """
        # 初始化时间操作符映射
        self.temporal_operator_mapping = {
            # 时间操作符
            "最终": "F",  # Finally
            "总是": "G",  # Globally
            "直到": "U",  # Until
            "下一个": "X",  # Next
            # 逻辑操作符
            "并且": "&",  # And
            "或者": "|",  # Or
            "非": "!",   # Not
            "蕴含": "-",  # Implies (通常用 -> 表示)
            # 任务类型对应的结构
            "顺序任务": "F(",
            "条件任务": "",
            "并行任务": "&",
        }
        
        # 初始化结构模板
        self.structure_templates = {
            "sequential": self._generate_sequential,
            "conditional": self._generate_conditional,
            "parallel": self._generate_parallel,
            "simple": self._generate_simple,
        }
    
    def generate(self, semantics: Dict) -> str:
        """
        根据语义结构生成LTL公式
        
        Args:
            semantics: 解析后的语义结构
            
        Returns:
            str: 生成的LTL公式
        """
        # 确定任务结构类型
        structure_type = semantics.get("structure", "simple")
        
        # 根据结构类型选择生成方法
        generator = self.structure_templates.get(structure_type, self._generate_simple)
        
        # 生成LTL公式
        ltl_formula = generator(semantics)
        
        # 验证并格式化结果
        return self._format_formula(ltl_formula)
    
    def _generate_simple(self, semantics: Dict) -> str:
        """
        生成简单结构的LTL公式
        
        Args:
            semantics: 解析后的语义结构
            
        Returns:
            str: 生成的LTL公式
        """
        # 获取命题列表
        propositions = semantics.get("propositions", [])
        
        # 如果有命题，使用第一个作为简单公式
        if propositions:
            # 检查是否有时间操作符
            temporal_operators = semantics.get("temporal_operators", [])
            if temporal_operators and temporal_operators[0] in self.temporal_operator_mapping:
                operator = self.temporal_operator_mapping[temporal_operators[0]]
                return f"{operator}({propositions[0]})"
            else:
                return propositions[0]
        
        # 如果没有命题，尝试从动作和对象构建
        actions = semantics.get("actions", [])
        objects = semantics.get("objects", [])
        
        if actions and objects and len(actions) == len(objects):
            # 构建命题（动作_对象）
            prop = f"{actions[0]}_{objects[0]}"
            return prop
        
        return "True"  # 默认公式
    
    def _generate_sequential(self, semantics: Dict) -> str:
        """
        生成顺序结构的LTL公式
        
        Args:
            semantics: 解析后的语义结构
            
        Returns:
            str: 生成的LTL公式
        """
        # 获取命题列表或从动作对象构建命题
        propositions = semantics.get("propositions", [])
        
        # 如果没有现成的命题，尝试构建
        if not propositions:
            actions = semantics.get("actions", [])
            objects = semantics.get("objects", [])
            
            # 构建动作对象对
            for i in range(min(len(actions), len(objects))):
                propositions.append(f"{actions[i]}_{objects[i]}")
        
        # 生成顺序公式 (a -> F(b -> F(c...)))
        if len(propositions) < 2:
            return self._generate_simple(semantics)
        
        formula = propositions[-1]  # 从最后一个开始
        
        # 从后往前构建蕴含链
        for prop in reversed(propositions[:-1]):
            formula = f"({prop} -> F({formula}))"
        
        # 确保第一个命题最终会发生
        return f"F({formula})"
    
    def _generate_conditional(self, semantics: Dict) -> str:
        """
        生成条件结构的LTL公式
        
        Args:
            semantics: 解析后的语义结构
            
        Returns:
            str: 生成的LTL公式
        """
        # 获取条件和结果
        conditions = semantics.get("conditions", [])
        actions = semantics.get("actions", [])
        objects = semantics.get("objects", [])
        
        # 如果有条件
        if conditions:
            condition_str = " ".join(conditions)
            
            # 构建结果命题
            if actions and objects and len(actions) >= 1:
                result = f"{actions[0]}_{objects[0]}"
                return f"(G({condition_str} -> F({result})))"
        
        return self._generate_simple(semantics)
    
    def _generate_parallel(self, semantics: Dict) -> str:
        """
        生成并行结构的LTL公式
        
        Args:
            semantics: 解析后的语义结构
            
        Returns:
            str: 生成的LTL公式
        """
        # 获取命题列表
        propositions = semantics.get("propositions", [])
        
        # 如果没有现成的命题，尝试构建
        if not propositions:
            actions = semantics.get("actions", [])
            objects = semantics.get("objects", [])
            
            # 构建动作对象对
            for i in range(min(len(actions), len(objects))):
                propositions.append(f"{actions[i]}_{objects[i]}")
        
        # 生成并行公式 (F(a) & F(b) & ...)
        if not propositions:
            return "True"
        
        if len(propositions) == 1:
            return f"F({propositions[0]})"
        
        # 所有命题都最终发生
        return " & ".join([f"F({p})" for p in propositions])
    
    def _format_formula(self, formula: str) -> str:
        """
        格式化LTL公式
        
        Args:
            formula: 原始公式
            
        Returns:
            str: 格式化后的公式
        """
        # 确保基本的格式正确性
        formula = formula.strip()
        
        # 替换可能的问题字符
        formula = formula.replace("-", "->")  # 正确表示蕴含
        
        return formula
    
    def generate_from_task(self, task_type: str, details: Dict) -> str:
        """
        根据任务类型和详细信息生成LTL公式
        
        Args:
            task_type: 任务类型
            details: 任务详细信息
            
        Returns:
            str: 生成的LTL公式
        """
        # 根据任务类型选择生成策略
        if "顺序" in task_type:
            semantics = {"structure": "sequential", **details}
            return self.generate(semantics)
        elif "条件" in task_type:
            semantics = {"structure": "conditional", **details}
            return self.generate(semantics)
        elif "并行" in task_type:
            semantics = {"structure": "parallel", **details}
            return self.generate(semantics)
        else:
            semantics = {"structure": "simple", **details}
            return self.generate(semantics)