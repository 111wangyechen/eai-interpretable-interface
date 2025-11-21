#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版LTL公式生成器
支持更完整的LTL公式生成，包括复杂时序逻辑和嵌套结构
"""

from typing import Dict, List, Optional, Union
import re


class EnhancedLTLGenerator:
    """
    增强版LTL公式生成器类
    支持更完整的LTL公式生成
    """
    
    def __init__(self):
        """
        初始化增强版LTL生成器
        """
        self._init_enhanced_operators()
        self._init_complex_templates()
        self._init_nested_patterns()
        self._init_temporal_extensions()
    
    def _init_enhanced_operators(self):
        """
        初始化增强的操作符映射
        """
        # 增强的时间操作符
        self.enhanced_temporal_operators = {
            # 基本时序操作符
            "最终": "F",
            "总是": "G", 
            "下一个": "X",
            "直到": "U",
            "释放": "R",
            
            # 英文对应
            "finally": "F",
            "eventually": "F",
            "always": "G",
            "globally": "G",
            "next": "X",
            "until": "U",
            "release": "R",
            
            # 扩展时序操作符
            "最终总是": "FG",
            "总是最终": "GF",
            "最终下一个": "FX",
            "总是下一个": "GX",
            
            "finally_always": "FG",
            "always_eventually": "GF",
            "finally_next": "FX",
            "always_next": "GX",
            
            # 条件时序
            "如果那么": "->",
            "当且仅当": "<->",
            "蕴含": "->",
            "等价": "<->",
            
            "if_then": "->",
            "iff": "<->",
            "implies": "->",
            "equivalent": "<->"
        }
        
        # 增强的逻辑操作符
        self.enhanced_logical_operators = {
            "并且": "&",
            "或者": "|",
            "非": "!",
            "异或": "^",
            
            "and": "&",
            "or": "|", 
            "not": "!",
            "xor": "^",
            
            # 量化操作符
            "存在": "E",
            "全称": "A",
            "存在路径": "E",
            "所有路径": "A",
            
            "exists": "E",
            "forall": "A",
            "exists_path": "E",
            "forall_path": "A"
        }
    
    def _init_complex_templates(self):
        """
        初始化复杂结构模板
        """
        self.complex_templates = {
            # 多步骤顺序任务
            "multi_step_sequential": {
                "pattern": "({}) -> ({} -> ({} -> ...))",
                "description": "多步骤顺序执行",
                "example": "go_to_kitchen -> (open_fridge -> (take_milk -> close_fridge))"
            },
            
            # 条件分支任务
            "conditional_branch": {
                "pattern": "({} -> {}) & (!{} -> {})",
                "description": "条件分支执行",
                "example": "(is_hungry -> eat_food) & (!is_hungry -> drink_water)"
            },
            
            # 循环任务
            "iterative_task": {
                "pattern": "G(!done -> ({} -> X(!done)))",
                "description": "循环执行直到完成",
                "example": "G(!cleaning_done -> (clean_floor -> X(!cleaning_done)))"
            },
            
            # 并行任务
            "parallel_task": {
                "pattern": "F({}) & F({}) & F({})",
                "description": "并行执行多个任务",
                "example": "F(turn_on_light) & F(open_window) & F(adjust_temperature)"
            },
            
            # 时间约束任务
            "temporal_constraint": {
                "pattern": "F({}) & ({} -> {})",
                "description": "带时间约束的任务",
                "example": "F(reach_destination) & (start_journey -> F(reach_destination))"
            },
            
            # 嵌套条件任务
            "nested_condition": {
                "pattern": "({} & {} -> {}) & (!{} -> {})",
                "description": "嵌套条件执行",
                "example": "(is_raining & have_umbrella -> go_outside) & (!is_raining -> go_outside)"
            },
            
            # 优先级任务
            "priority_task": {
                "pattern": "({} -> F(!{})) & F({})",
                "description": "优先级任务执行",
                "example": "(emergency -> F(!emergency)) & F(handle_emergency)"
            },
            
            # 资源约束任务
            "resource_constraint": {
                "pattern": "(!resource_available -> F(resource_available)) & (resource_available -> F({}))",
                "description": "资源约束下的任务",
                "example": "(!tool_available -> F(tool_available)) & (tool_available -> F(use_tool))"
            }
        }
    
    def _init_nested_patterns(self):
        """
        初始化嵌套模式
        """
        self.nested_patterns = {
            # 嵌套顺序
            "nested_sequential": {
                "structure": "({} -> ({} -> ({} -> {})))",
                "depth": 3,
                "description": "三层嵌套顺序"
            },
            
            # 嵌套条件
            "nested_conditional": {
                "structure": "({} -> ({} -> {})) & (!{} -> {})",
                "depth": 2,
                "description": "二层嵌套条件"
            },
            
            # 混合嵌套
            "mixed_nested": {
                "structure": "({} -> (F({}) & G(!{} -> {})))",
                "depth": 2,
                "description": "条件与时序混合嵌套"
            }
        }
    
    def _init_temporal_extensions(self):
        """
        初始化时序扩展
        """
        self.temporal_extensions = {
            # 时间窗口
            "time_window": {
                "pattern": "F[<=t]({})",
                "description": "在时间t内完成",
                "example": "F[<=10](reach_destination)"
            },
            
            # 持续时间
            "duration": {
                "pattern": "G[duration]({} -> {})",
                "description": "在持续时间内保持状态",
                "example": "G[5](light_on -> light_on)"
            },
            
            # 周期性
            "periodic": {
                "pattern": "G(F({}) -> X(F({})))",
                "description": "周期性执行",
                "example": "G(F(check_mail) -> X(F(check_mail)))"
            },
            
            # 超时处理
            "timeout": {
                "pattern": "F[>t](!{}) -> {}",
                "description": "超时后执行备选方案",
                "example": "F[>30](!task_complete) -> abort_task"
            }
        }
    
    def generate(self, parse_result: Dict) -> str:
        """
        生成增强的LTL公式
        
        Args:
            parse_result: 增强的解析结果
            
        Returns:
            str: 生成的LTL公式
        """
        structure = parse_result.get("structure", "simple")
        task_complexity = parse_result.get("task_complexity", "simple")
        propositions = parse_result.get("propositions", [])
        conditions = parse_result.get("conditions", [])
        temporal_info = parse_result.get("temporal_info", [])
        constraints = parse_result.get("constraints", [])
        dependencies = parse_result.get("dependencies", [])
        
        # 根据结构和复杂度选择生成策略
        if task_complexity == "complex":
            return self._generate_complex_ltl(parse_result)
        elif structure == "conditional":
            return self._generate_conditional_ltl(parse_result)
        elif structure == "temporal_sequential":
            return self._generate_temporal_sequential_ltl(parse_result)
        elif structure == "sequential":
            return self._generate_sequential_ltl(parse_result)
        else:
            return self._generate_simple_ltl(parse_result)
    
    def _generate_complex_ltl(self, parse_result: Dict) -> str:
        """
        生成复杂LTL公式
        """
        propositions = parse_result.get("propositions", [])
        conditions = parse_result.get("conditions", [])
        dependencies = parse_result.get("dependencies", [])
        constraints = parse_result.get("constraints", [])
        
        # 检查具体的复杂模式
        if len(conditions) > 1:
            return self._generate_nested_conditional(parse_result)
        elif len(dependencies) > 0:
            return self._generate_causal_ltl(parse_result)
        elif len(constraints) > 1:
            return self._generate_multi_constraint_ltl(parse_result)
        else:
            return self._generate_complex_sequential(parse_result)
    
    def _generate_nested_conditional(self, parse_result: Dict) -> str:
        """
        生成嵌套条件LTL公式
        """
        conditions = parse_result.get("conditions", [])
        propositions = parse_result.get("propositions", [])
        
        if not conditions:
            return self._generate_sequential_ltl(parse_result)
        
        # 构建嵌套条件
        condition_parts = []
        for i, condition in enumerate(conditions):
            cond_prop = condition.get("condition", "").replace(" ", "_")
            consequence = condition.get("consequence", "").replace(" ", "_")
            
            if consequence and i < len(propositions):
                cond_part = f"({cond_prop} -> {propositions[i]})"
            else:
                cond_part = f"({cond_prop} -> F({propositions[i] if i < len(propositions) else cond_prop}))"
            
            condition_parts.append(cond_part)
        
        # 组合嵌套条件
        if len(condition_parts) == 1:
            return condition_parts[0]
        elif len(condition_parts) == 2:
            return f"({condition_parts[0]} & {condition_parts[1]})"
        else:
            return " & ".join([f"({part})" for part in condition_parts])
    
    def _generate_causal_ltl(self, parse_result: Dict) -> str:
        """
        生成因果LTL公式
        """
        dependencies = parse_result.get("dependencies", [])
        propositions = parse_result.get("propositions", [])
        
        if not dependencies:
            return self._generate_sequential_ltl(parse_result)
        
        causal_parts = []
        for dep in dependencies:
            cause = dep.get("cause", "").replace(" ", "_")
            effect = dep.get("effect", "").replace(" ", "_")
            
            # 查找对应的命题
            cause_prop = self._find_matching_proposition(cause, propositions)
            effect_prop = self._find_matching_proposition(effect, propositions)
            
            if cause_prop and effect_prop:
                causal_part = f"({cause_prop} -> F({effect_prop}))"
                causal_parts.append(causal_part)
        
        if causal_parts:
            return " & ".join(causal_parts)
        else:
            return self._generate_sequential_ltl(parse_result)
    
    def _generate_multi_constraint_ltl(self, parse_result: Dict) -> str:
        """
        生成多约束LTL公式
        """
        constraints = parse_result.get("constraints", [])
        propositions = parse_result.get("propositions", [])
        
        constraint_parts = []
        for constraint in constraints:
            constraint_type = constraint.get("type", "")
            content = constraint.get("content", "").replace(" ", "_")
            
            if constraint_type in ["obligation", "obligation_zh"]:
                # 义务性约束
                matching_prop = self._find_matching_proposition(content, propositions)
                if matching_prop:
                    constraint_parts.append(f"F({matching_prop})")
                else:
                    constraint_parts.append(f"F({content})")
            
            elif constraint_type in ["prohibition", "prohibition_zh", "negation"]:
                # 禁止性约束
                matching_prop = self._find_matching_proposition(content, propositions)
                if matching_prop:
                    constraint_parts.append(f"G(!{matching_prop})")
                else:
                    constraint_parts.append(f"G(!{content})")
            
            elif constraint_type == "temporal_constraint":
                # 时间约束
                operator = constraint.get("operator", "")
                if operator in ["before", "在...之前"]:
                    constraint_parts.append(f"({content} -> F({propositions[0] if propositions else content}))")
                elif operator in ["after", "在...之后"]:
                    constraint_parts.append(f"({propositions[0] if propositions else content} -> F({content}))")
        
        if constraint_parts:
            return " & ".join(constraint_parts)
        else:
            return self._generate_sequential_ltl(parse_result)
    
    def _generate_complex_sequential(self, parse_result: Dict) -> str:
        """
        生成复杂顺序LTL公式
        """
        propositions = parse_result.get("propositions", [])
        
        if len(propositions) <= 1:
            return self._generate_simple_ltl(parse_result)
        
        # 构建复杂顺序链
        if len(propositions) == 2:
            return f"({propositions[0]} -> F({propositions[1]}))"
        elif len(propositions) == 3:
            return f"({propositions[0]} -> F({propositions[1]} -> F({propositions[2]})))"
        else:
            # 对于更多命题，使用嵌套结构
            formula = propositions[0]
            for prop in propositions[1:]:
                formula = f"({formula} -> F({prop}))"
            return formula
    
    def _generate_conditional_ltl(self, parse_result: Dict) -> str:
        """
        生成条件LTL公式
        """
        conditions = parse_result.get("conditions", [])
        propositions = parse_result.get("propositions", [])
        
        if not conditions:
            return self._generate_sequential_ltl(parse_result)
        
        condition = conditions[0]
        condition_text = condition.get("condition", "").replace(" ", "_")
        consequence = condition.get("consequence", "").replace(" ", "_")
        
        # 查找匹配的命题
        cond_prop = self._find_matching_proposition(condition_text, propositions)
        cons_prop = self._find_matching_proposition(consequence, propositions) if consequence else None
        
        if cond_prop and cons_prop:
            return f"({cond_prop} -> {cons_prop})"
        elif cond_prop:
            return f"({cond_prop} -> F({propositions[0] if propositions else cond_prop}))"
        else:
            return self._generate_sequential_ltl(parse_result)
    
    def _generate_temporal_sequential_ltl(self, parse_result: Dict) -> str:
        """
        生成时序顺序LTL公式
        """
        propositions = parse_result.get("propositions", [])
        temporal_info = parse_result.get("temporal_info", [])
        
        # 基础顺序结构
        base_formula = self._generate_sequential_ltl(parse_result)
        
        # 添加时序修饰
        if temporal_info:
            for temp_info in temporal_info:
                temp_type = temp_info.get("type", "")
                if temp_type in ["relative_time", "duration"]:
                    # 添加时序约束
                    if "immediately" in temp_info.get("expression", "") or "立即" in temp_info.get("expression", ""):
                        base_formula = f"X({base_formula})"
                    elif "eventually" in temp_info.get("expression", "") or "最终" in temp_info.get("expression", ""):
                        base_formula = f"F({base_formula})"
                    elif "always" in temp_info.get("expression", "") or "总是" in temp_info.get("expression", ""):
                        base_formula = f"G({base_formula})"
        
        return base_formula
    
    def _generate_sequential_ltl(self, parse_result: Dict) -> str:
        """
        生成顺序LTL公式
        """
        propositions = parse_result.get("propositions", [])
        
        if not propositions:
            return "true"
        
        # 清理和验证命题
        valid_props = []
        for prop in propositions:
            clean_prop = prop.strip()
            if clean_prop and clean_prop != "true" and clean_prop != "false":
                valid_props.append(clean_prop)
        
        if not valid_props:
            return "true"
        
        if len(valid_props) == 1:
            return f"F({valid_props[0]})"
        elif len(valid_props) == 2:
            return f"({valid_props[0]} -> F({valid_props[1]}))"
        else:
            # 构建顺序链：p1 -> F(p2 -> F(p3 -> ...))
            formula = valid_props[0]
            for prop in valid_props[1:]:
                formula = f"({formula} -> F({prop}))"
            return formula
    
    def _generate_simple_ltl(self, parse_result: Dict) -> str:
        """
        生成简单LTL公式
        """
        propositions = parse_result.get("propositions", [])
        
        if not propositions:
            return "true"
        
        # 对于简单任务，使用最直接的形式
        if len(propositions) == 1:
            prop = propositions[0].strip()
            # 确保命题是有效的LTL原子命题
            if prop and prop != "true" and prop != "false":
                return f"F({prop})"
            else:
                return "true"
        elif len(propositions) == 2:
            # 两个命题使用顺序关系
            prop1, prop2 = propositions[0].strip(), propositions[1].strip()
            if prop1 and prop2 and prop1 != "true" and prop2 != "true":
                return f"({prop1} -> F({prop2}))"
            else:
                return f"F({prop1 if prop1 != 'true' else prop2})"
        else:
            # 多个命题使用合取，但每个都用F包裹
            valid_props = []
            for prop in propositions:
                clean_prop = prop.strip()
                if clean_prop and clean_prop != "true" and clean_prop != "false":
                    valid_props.append(clean_prop)
            
            if not valid_props:
                return "true"
            elif len(valid_props) == 1:
                return f"F({valid_props[0]})"
            else:
                # 使用合取形式，确保所有目标都最终达成
                return " & ".join([f"F({prop})" for prop in valid_props])
    
    def _find_matching_proposition(self, text: str, propositions: List[str]) -> Optional[str]:
        """
        查找匹配的命题
        """
        text_lower = text.lower().replace("_", " ")
        
        for prop in propositions:
            prop_lower = prop.lower().replace("_", " ")
            
            # 精确匹配
            if text_lower == prop_lower:
                return prop
            
            # 部分匹配
            if text_lower in prop_lower or prop_lower in text_lower:
                return prop
            
            # 关键词匹配
            text_words = set(text_lower.split())
            prop_words = set(prop_lower.split())
            
            if text_words & prop_words:  # 有共同词汇
                overlap_ratio = len(text_words & prop_words) / len(text_words | prop_words)
                if overlap_ratio > 0.3:  # 重叠度超过30%
                    return prop
        
        return None
    
    def generate_from_template(self, template_name: str, propositions: List[str], **kwargs) -> str:
        """
        根据模板生成LTL公式
        
        Args:
            template_name: 模板名称
            propositions: 命题列表
            **kwargs: 额外参数
            
        Returns:
            str: 生成的LTL公式
        """
        template = self.complex_templates.get(template_name)
        if not template:
            return self._generate_simple_ltl({"propositions": propositions})
        
        pattern = template["pattern"]
        
        # 根据模板类型填充
        if template_name == "multi_step_sequential":
            if len(propositions) >= 3:
                return pattern.format(propositions[0], propositions[1], propositions[2])
            elif len(propositions) == 2:
                return f"({propositions[0]} -> F({propositions[1]}))"
            else:
                return f"F({propositions[0]})" if propositions else "true"
        
        elif template_name == "conditional_branch":
            condition = kwargs.get("condition", propositions[0] if propositions else "true")
            true_branch = kwargs.get("true_branch", propositions[1] if len(propositions) > 1 else "true")
            false_branch = kwargs.get("false_branch", propositions[2] if len(propositions) > 2 else "true")
            return pattern.format(condition, true_branch, condition, false_branch)
        
        elif template_name == "iterative_task":
            task = kwargs.get("task", propositions[0] if propositions else "true")
            done_condition = kwargs.get("done_condition", "done")
            return pattern.format(task, done_condition)
        
        elif template_name == "parallel_task":
            if len(propositions) >= 3:
                return pattern.format(propositions[0], propositions[1], propositions[2])
            elif len(propositions) == 2:
                return f"F({propositions[0]}) & F({propositions[1]})"
            else:
                return f"F({propositions[0]})" if propositions else "true"
        
        elif template_name == "temporal_constraint":
            main_task = kwargs.get("main_task", propositions[0] if propositions else "true")
            trigger = kwargs.get("trigger", propositions[1] if len(propositions) > 1 else "true")
            return pattern.format(main_task, trigger, main_task)
        
        else:
            # 默认使用简单生成
            return self._generate_simple_ltl({"propositions": propositions})
    
    def validate_formula(self, formula: str) -> Dict:
        """
        验证LTL公式
        
        Args:
            formula: LTL公式字符串
            
        Returns:
            Dict: 验证结果
        """
        result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        # 基本语法检查
        if not formula:
            result["is_valid"] = False
            result["errors"].append("公式为空")
            return result
        
        # 检查括号匹配
        stack = []
        for i, char in enumerate(formula):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if not stack:
                    result["is_valid"] = False
                    result["errors"].append(f"位置{i}: 未匹配的右括号")
                else:
                    stack.pop()
        
        if stack:
            result["is_valid"] = False
            result["errors"].append(f"位置{stack[-1]}: 未匹配的左括号")
        
        # 检查操作符使用
        operators = ['&', '|', '^', '->', '<->', 'U', 'R']
        for op in operators:
            if formula.count(op) > 10:  # 操作符过多可能表示公式过于复杂
                result["warnings"].append(f"操作符'{op}'使用过多，公式可能过于复杂")
        
        # 检查命题格式
        prop_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        propositions = re.findall(prop_pattern, formula)
        
        # 检查是否包含非标准命题
        for prop in propositions:
            if prop in ['true', 'false', 'G', 'F', 'X', 'U', 'R', '&', '|', '!', '^']:
                continue
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', prop):
                result["warnings"].append(f"命题'{prop}'格式可能不规范")
        
        # 检查公式复杂度
        if len(formula) > 200:
            result["warnings"].append("公式过长，建议分解为多个子公式")
        
        if formula.count('(') > 10:
            result["warnings"].append("嵌套层次过深，建议简化公式结构")
        
        return result
    
    def optimize_formula(self, formula: str) -> str:
        """
        优化LTL公式
        
        Args:
            formula: 原始LTL公式
            
        Returns:
            str: 优化后的LTL公式
        """
        optimized = formula
        
        # 移除多余的括号
        optimized = re.sub(r'\(\s*([^()&|UFR]+)\s*\)', r'\1', optimized)
        
        # 简化双重否定
        optimized = re.sub(r'!!\s*', '', optimized)
        
        # 合并连续的相同操作符
        optimized = re.sub(r'F\s+F', 'F', optimized)
        optimized = re.sub(r'G\s+G', 'G', optimized)
        optimized = re.sub(r'X\s+X', 'X', optimized)
        
        # 标准化空格
        optimized = re.sub(r'\s+', ' ', optimized)
        optimized = re.sub(r'\s*([()&|!UFR])\s*', r'\1', optimized)
        
        return optimized.strip()