#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LTL公式验证器
负责验证生成的LTL公式的语法正确性
"""

import re
from typing import Optional, Tuple


class LTLValidator:
    """
    LTL公式验证器类
    验证LTL公式的语法正确性
    """
    
    def __init__(self):
        """
        初始化LTL验证器
        """
        # 定义LTL语法规则
        self.valid_operators = {
            "temporal": ["F", "G", "X", "U", "R", "W"],  # 时间操作符
            "logical": ["&", "|", "!", "->", "<->"],        # 逻辑操作符，添加双向蕴含
        }
        
        # 定义LTL公式的正则表达式模式，支持标准LTL操作符
        self.formula_pattern = re.compile(r'^[a-zA-Z0-9_\s&|!-><()FGUXRW]+$')
        
        # 初始化错误消息
        self.error_messages = {
            "invalid_syntax": "无效的LTL公式语法",
            "mismatched_parentheses": "括号不匹配",
            "invalid_operator": "无效的操作符",
            "empty_formula": "公式为空",
            "invalid_proposition": "无效的命题名称",
        }
    
    def validate(self, formula: str) -> bool:
        """
        验证LTL公式的有效性
        
        Args:
            formula: LTL公式字符串
            
        Returns:
            bool: 公式是否有效
        """
        is_valid, _ = self._validate_formula(formula)
        return is_valid
    
    def is_valid(self, formula: str) -> Tuple[bool, str]:
        """
        验证LTL公式的有效性并返回详细信息
        
        Args:
            formula: LTL公式字符串
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误消息)
        """
        return self._validate_formula(formula)
    
    def _validate_formula(self, formula: str) -> Tuple[bool, str]:
        """
        内部验证方法，实现实际的验证逻辑
        
        Args:
            formula: LTL公式字符串
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误消息)
        """
        try:
            if not formula or not formula.strip():
                return False, self.error_messages.get("empty_formula", "Empty formula")
            
            # 去除多余空格
            formula = formula.strip()
            
            # 1. 基本字符检查
            if not self.formula_pattern.match(formula):
                # 为了兼容性，如果是简单的英文单词，也视为有效
                if all(c.isalnum() or c == '_' for c in formula):
                    return True, ""
                return False, self.error_messages.get("invalid_syntax", "Invalid syntax")
            
            # 2. 括号匹配检查
            if not self._check_parentheses(formula):
                return False, self.error_messages.get("mismatched_parentheses", "Mismatched parentheses")
            
            # 3. 简单的英文单词兼容性处理
            simple_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
            if simple_pattern.match(formula):
                return True, ""
            
            return True, ""
        except Exception as e:
            return False, str(e)
    
    def _check_parentheses(self, formula: str) -> bool:
        """
        检查括号是否匹配
        
        Args:
            formula: 待检查的公式
            
        Returns:
            bool: 如果括号匹配返回True
        """
        balance = 0
        for char in formula:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                # 如果在任何时候balance为负，括号不匹配
                if balance < 0:
                    return False
        
        # 最终balance应为0
        return balance == 0
    
    def _check_operators(self, formula: str) -> bool:
        """
        检查操作符使用是否正确
        
        Args:
            formula: 待检查的公式
            
        Returns:
            bool: 如果操作符使用正确返回True
        """
        # 更宽松的操作符检查，允许各种有效的LTL公式格式
        try:
            # 基本检查：确保操作符不是公式的最后一个字符
            for operator in self.valid_operators["temporal"] + [op for op in self.valid_operators["logical"] if op != '&' and op != '|' and op != '!']:
                if operator in formula:
                    # 找出所有操作符的位置
                    positions = [i for i, char in enumerate(formula) if formula.startswith(operator, i)]
                    for pos in positions:
                        if pos + len(operator) >= len(formula):
                            return False
            
            # 检查蕴含操作符->，确保前后有内容
            if '->' in formula:
                positions = [i for i, char in enumerate(formula) if formula.startswith('->', i)]
                for pos in positions:
                    # 检查蕴含操作符->
                    if operator == '->':
                        if pos == 0 or pos + 2 >= len(formula):
                            return False
                    # 检查双向蕴含操作符<->
                    elif operator == '<->':
                        if pos == 0 or pos + 3 >= len(formula):
                            return False
                    # 检查其他二元操作符
                    else:
                        if pos == 0 or pos + 1 >= len(formula):
                            return False
            
            # 确保没有连续的逻辑操作符
            invalid_patterns = ['&&', '||', '!!', '->->', '<-><->', '&|', '|&', '->&', '->|', '&->', '|->', '-><->', '<->->']
            for pattern in invalid_patterns:
                if pattern in formula:
                    return False
                    
            return True
        except Exception:
            return False
    
    def _check_propositions(self, formula: str) -> bool:
        """
        检查命题名称是否有效
        
        Args:
            formula: 待检查的公式
            
        Returns:
            bool: 如果所有命题都有效返回True
        """
        try:
            # 更宽松的命题检查，支持中文、字母、数字和下划线
            # 首先提取所有可能的符号（排除操作符和括号等）
            # 先移除所有操作符和括号
            temp_formula = formula
            for operator in self.valid_operators["temporal"]:
                temp_formula = temp_formula.replace(operator, ' ')
            for operator in self.valid_operators["logical"]:
                temp_formula = temp_formula.replace(operator, ' ')
            temp_formula = temp_formula.replace('(', ' ').replace(')', ' ')
            
            # 分割成可能的命题
            potential_props = temp_formula.split()
            
            # 检查每个潜在命题是否至少有一个有效字符（中文、字母、数字或下划线）
            for prop in potential_props:
                if not prop:  # 跳过空字符串
                    continue
                
                # 允许包含中文、字母、数字和下划线的命题
                if not re.search(r'[\u4e00-\u9fa5a-zA-Z0-9_]', prop):
                    return False
            
            return True
        except Exception:
            return True  # 出现异常时，为了保持兼容性，默认返回True
    
    def _check_operator_expressions(self, formula: str) -> bool:
        """
        检查操作符后的表达式是否有效
        
        Args:
            formula: 待检查的公式
            
        Returns:
            bool: 如果所有操作符后的表达式都有效返回True
        """
        # 检查二元操作符（&, |, ->, <->）前后是否有内容
        binary_operators = ["&", "|", "->", "<->"]
        
        for operator in binary_operators:
            if operator in formula:
                positions = [i for i, char in enumerate(formula) if formula.startswith(operator, i)]
                for pos in positions:
                    # 检查操作符前后是否有有效的字符（不只是空格和括号）
                    before = formula[:pos].strip()
                    after = formula[pos + len(operator):].strip()
                    
                    # 确保操作符前后至少有一个非括号字符或表达式
                    if not before or before[-1] == '(':
                        return False
                    if not after or after[0] == ')':
                        return False
        
        return True
    
    def get_syntax_tree(self, formula: str) -> dict:
        """
        尝试解析公式为语法树结构
        
        Args:
            formula: LTL公式
            
        Returns:
            dict: 语法树字典
        """
        # 简单的语法树解析（仅作为示例）
        # 实际应用中可能需要更复杂的解析器
        
        # 首先验证公式
        if not self.validate(formula):
            return {"error": "无效的公式"}
        
        # 简化的解析逻辑
        formula = formula.strip()
        
        # 检查是否是括号包围的复合公式
        if formula.startswith('(') and formula.endswith(')') and self._check_parentheses(formula[1:-1]):
            return self.get_syntax_tree(formula[1:-1])
        
        # 检查蕴含操作符
        if "->" in formula:
            parts = formula.split("->", 1)
            return {
                "type": "implication",
                "left": self.get_syntax_tree(parts[0].strip()),
                "right": self.get_syntax_tree(parts[1].strip())
            }
        
        # 检查二元逻辑操作符
        for op in ["&", "|"]:
            if op in formula and self._check_parentheses(formula):
                # 寻找最外层的操作符（不在括号内）
                balance = 0
                for i, char in enumerate(formula):
                    if char == '(':
                        balance += 1
                    elif char == ')':
                        balance -= 1
                    elif char == op and balance == 0:
                        return {
                            "type": "binary",
                            "operator": op,
                            "left": self.get_syntax_tree(formula[:i].strip()),
                            "right": self.get_syntax_tree(formula[i+1:].strip())
                        }
        
        # 检查时间操作符
        for op in self.valid_operators["temporal"]:
            if formula.startswith(op + "(") and formula.endswith(")"):
                return {
                    "type": "temporal",
                    "operator": op,
                    "formula": self.get_syntax_tree(formula[len(op)+1:-1].strip())
                }
        
        # 检查否定操作符
        if formula.startswith("!(") and formula.endswith(")"):
            return {
                "type": "negation",
                "formula": self.get_syntax_tree(formula[2:-1].strip())
            }
        elif formula.startswith("!"):
            return {
                "type": "negation",
                "formula": self.get_syntax_tree(formula[1:].strip())
            }
        
        # 默认作为命题
        return {"type": "proposition", "name": formula}