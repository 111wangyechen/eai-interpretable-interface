#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版目标解释器
集成增强的NLP解析器和LTL生成器，支持更复杂的目标解释
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
import json
import re
from datetime import datetime

from enhanced_nlp_parser import EnhancedNLPParser
from enhanced_ltl_generator import EnhancedLTLGenerator


class EnhancedGoalInterpreter:
    """
    增强版目标解释器类
    集成增强的NLP解析器和LTL生成器
    """
    
    def __init__(self):
        """
        初始化增强版目标解释器
        """
        self.enhanced_parser = EnhancedNLPParser()
        self.enhanced_generator = EnhancedLTLGenerator()
        self._init_enhanced_rules()
    
    def _init_enhanced_rules(self):
        """
        初始化增强的规则映射
        """
        # 增强的时间操作符映射
        self.enhanced_temporal_operators = {
            # 基本时序
            "最终": "F", "finally": "F", "eventually": "F",
            "总是": "G", "always": "G", "globally": "G", 
            "下一个": "X", "next": "X",
            "直到": "U", "until": "U",
            "释放": "R", "release": "R",
            
            # 组合时序
            "最终总是": "FG", "finally_always": "FG",
            "总是最终": "GF", "always_eventually": "GF",
            "最终下一个": "FX", "finally_next": "FX",
            "总是下一个": "GX", "always_next": "GX",
            
            # 条件时序
            "如果那么": "->", "if_then": "->", "implies": "->",
            "当且仅当": "<->", "iff": "<->", "equivalent": "<->",
            
            # 路径量词
            "存在": "E", "exists": "E", "exists_path": "E",
            "全称": "A", "forall": "A", "forall_path": "A"
        }
        
        # 增强的逻辑操作符映射
        self.enhanced_logical_operators = {
            "并且": "&", "and": "&",
            "或者": "|", "or": "|",
            "非": "!", "not": "!",
            "异或": "^", "xor": "^"
        }
        
        # 增强的关键词模式
        self.enhanced_keyword_patterns = {
            # 复杂任务模式
            "multi_step": [
                r"(first|then|next|after|before|finally|step\s*\d+)",
                r"(先|首先|第一步|然后|接着|第二步|最后|完成|第三步)"
            ],
            "conditional": [
                r"(if.*?then|when.*?then|provided.*?then)",
                r"(如果.*?那么|当.*?时|只要.*?就)"
            ],
            "iterative": [
                r"(repeat|again|multiple|times|keep|continue)",
                r"(重复|再次|多次|一直|继续|保持)"
            ],
            "parallel": [
                r"(and|also|simultaneously|at the same time|both.*?and)",
                r"(并且|同时|也|既.*?又)"
            ],
            "temporal": [
                r"(within|before|after|during|by|immediately|eventually)",
                r"(在.*?之前|在.*?之后|在.*?期间|在.*?之内|立即|最终)"
            ]
        }
    
    def interpret(self, text: str) -> Dict:
        """
        解释自然语言目标（增强版）
        
        Args:
            text: 自然语言目标文本
            
        Returns:
            Dict: 增强的解释结果
        """
        # 使用增强的NLP解析器解析文本
        parse_result = self.enhanced_parser.parse(text)
        
        # 使用增强的LTL生成器生成公式
        ltl_formula = self.enhanced_generator.generate(parse_result)
        
        # 验证生成的公式
        validation_result = self.enhanced_generator.validate_formula(ltl_formula)
        
        # 优化公式
        if validation_result["is_valid"]:
            optimized_formula = self.enhanced_generator.optimize_formula(ltl_formula)
        else:
            optimized_formula = ltl_formula
        
        # 构建增强的结果
        result = {
            "original_text": text,
            "parse_result": parse_result,
            "ltl_formula": ltl_formula,
            "optimized_formula": optimized_formula,
            "validation_result": validation_result,
            # 直接包含关键字段，便于测试脚本访问
            "structure": parse_result.get("structure", "simple"),
            "task_complexity": parse_result.get("task_complexity", "simple"),
            "language": parse_result.get("language", "unknown"),
            "actions": parse_result.get("actions", []),
            "objects": parse_result.get("objects", []),
            "conditions": parse_result.get("conditions", []),
            "constraints": parse_result.get("constraints", []),
            "temporal_info": parse_result.get("temporal_info", []),
            "propositions": parse_result.get("propositions", []),
            "dependencies": parse_result.get("dependencies", []),
            "semantic_roles": parse_result.get("semantic_roles", {}),
            "interpretation_metadata": {
                "timestamp": datetime.now().isoformat(),
                "proposition_count": len(parse_result.get("propositions", [])),
                "condition_count": len(parse_result.get("conditions", [])),
                "constraint_count": len(parse_result.get("constraints", [])),
                "dependency_count": len(parse_result.get("dependencies", []))
            }
        }
        
        return result
    
    def interpret_goal(self, text: str) -> Dict:
        """
        解释自然语言目标（别名方法）
        
        Args:
            text: 自然语言目标文本
            
        Returns:
            Dict: 解释结果
        """
        return self.interpret(text)
    
    def interpret_from_dataset(self, dataset_path: str, limit: Optional[int] = None) -> List[Dict]:
        """
        从数据集批量解释目标（增强版）
        
        Args:
            dataset_path: 数据集文件路径
            limit: 限制处理的数量
            
        Returns:
            List[Dict]: 批量解释结果
        """
        try:
            # 读取数据集
            df = pd.read_parquet(dataset_path)
            
            # 限制数量
            if limit:
                df = df.head(limit)
            
            results = []
            
            for idx, row in df.iterrows():
                try:
                    # 获取自然语言文本
                    nl_text = row.get('nl', '')
                    if not nl_text:
                        nl_text = row.get('natural_language', '')
                    
                    if not nl_text:
                        continue
                    
                    # 解释目标
                    interpretation = self.interpret(nl_text)
                    
                    # 添加数据集信息
                    interpretation["dataset_info"] = {
                        "index": idx,
                        "original_tl": row.get('tl', ''),
                        "dataset_file": dataset_path.split('/')[-1]
                    }
                    
                    results.append(interpretation)
                    
                except Exception as e:
                    print(f"处理第{idx}行时出错: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"读取数据集时出错: {e}")
            return []
    
    def compare_with_dataset(self, dataset_path: str, limit: Optional[int] = None) -> Dict:
        """
        与数据集进行比较分析（增强版）
        
        Args:
            dataset_path: 数据集文件路径
            limit: 限制处理的数量
            
        Returns:
            Dict: 比较分析结果
        """
        interpretations = self.interpret_from_dataset(dataset_path, limit)
        
        if not interpretations:
            return {"error": "无法获取解释结果"}
        
        # 统计信息
        total_count = len(interpretations)
        valid_count = sum(1 for interp in interpretations 
                         if interp["validation_result"]["is_valid"])
        
        complexity_stats = {}
        structure_stats = {}
        language_stats = {}
        
        # 详细分析
        detailed_analysis = []
        
        for interp in interpretations:
            metadata = interp["interpretation_metadata"]
            
            # 复杂度统计
            complexity = metadata["complexity"]
            complexity_stats[complexity] = complexity_stats.get(complexity, 0) + 1
            
            # 结构统计
            structure = metadata["structure"]
            structure_stats[structure] = structure_stats.get(structure, 0) + 1
            
            # 语言统计
            language = metadata["language"]
            language_stats[language] = language_stats.get(language, 0) + 1
            
            # 详细分析
            analysis = {
                "index": interp["dataset_info"]["index"],
                "original_text": interp["original_text"],
                "generated_formula": interp["optimized_formula"],
                "original_tl": interp["dataset_info"]["original_tl"],
                "complexity": complexity,
                "structure": structure,
                "language": language,
                "proposition_count": metadata["proposition_count"],
                "condition_count": metadata["condition_count"],
                "constraint_count": metadata["constraint_count"],
                "is_valid": interp["validation_result"]["is_valid"],
                "warnings": interp["validation_result"]["warnings"],
                "errors": interp["validation_result"]["errors"]
            }
            
            detailed_analysis.append(analysis)
        
        # 生成报告
        comparison_result = {
            "summary": {
                "total_count": total_count,
                "valid_count": valid_count,
                "validity_rate": valid_count / total_count if total_count > 0 else 0,
                "dataset_file": dataset_path.split('/')[-1]
            },
            "statistics": {
                "complexity_distribution": complexity_stats,
                "structure_distribution": structure_stats,
                "language_distribution": language_stats
            },
            "detailed_analysis": detailed_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        return comparison_result
    
    def generate_complex_formula(self, task_type: str, components: List[str], **kwargs) -> str:
        """
        生成复杂类型的LTL公式
        
        Args:
            task_type: 任务类型
            components: 组件列表
            **kwargs: 额外参数
            
        Returns:
            str: 生成的LTL公式
        """
        return self.enhanced_generator.generate_from_template(task_type, components, **kwargs)
    
    def analyze_formula_complexity(self, formula: str) -> Dict:
        """
        分析LTL公式复杂度
        
        Args:
            formula: LTL公式
            
        Returns:
            Dict: 复杂度分析结果
        """
        analysis = {
            "length": len(formula),
            "operator_count": 0,
            "proposition_count": 0,
            "nesting_depth": 0,
            "complexity_score": 0,
            "complexity_level": "simple"
        }
        
        # 统计操作符
        operators = ['&', '|', '^', '->', '<->', 'U', 'R', 'F', 'G', 'X', '!', 'E', 'A']
        for op in operators:
            analysis["operator_count"] += formula.count(op)
        
        # 统计命题
        prop_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        propositions = re.findall(prop_pattern, formula)
        
        # 过滤掉操作符和关键词
        filtered_props = [prop for prop in propositions 
                         if prop not in ['true', 'false'] + operators]
        analysis["proposition_count"] = len(filtered_props)
        
        # 计算嵌套深度
        max_depth = 0
        current_depth = 0
        for char in formula:
            if char == '(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                current_depth -= 1
        analysis["nesting_depth"] = max_depth
        
        # 计算复杂度分数
        score = 0
        score += analysis["operator_count"] * 1
        score += analysis["proposition_count"] * 0.5
        score += analysis["nesting_depth"] * 2
        score += len(formula) * 0.01
        
        analysis["complexity_score"] = score
        
        # 确定复杂度级别
        if score < 10:
            analysis["complexity_level"] = "simple"
        elif score < 30:
            analysis["complexity_level"] = "medium"
        else:
            analysis["complexity_level"] = "complex"
        
        return analysis
    
    def get_supported_operators(self) -> Dict:
        """
        获取支持的操作符列表
        
        Returns:
            Dict: 支持的操作符
        """
        return {
            "temporal_operators": self.enhanced_temporal_operators,
            "logical_operators": self.enhanced_logical_operators,
            "keyword_patterns": self.enhanced_keyword_patterns
        }
    
    def get_supported_templates(self) -> Dict:
        """
        获取支持的模板列表
        
        Returns:
            Dict: 支持的模板
        """
        return self.enhanced_generator.complex_templates
    
    def batch_interpret(self, texts: List[str]) -> List[Dict]:
        """
        批量解释多个文本
        
        Args:
            texts: 文本列表
            
        Returns:
            List[Dict]: 解释结果列表
        """
        results = []
        for text in texts:
            try:
                result = self.interpret(text)
                results.append(result)
            except Exception as e:
                error_result = {
                    "original_text": text,
                    "error": str(e),
                    "ltl_formula": "",
                    "validation_result": {"is_valid": False, "errors": [str(e)]}
                }
                results.append(error_result)
        return results
    
    def export_results(self, results: List[Dict], output_path: str, format: str = "json"):
        """
        导出结果到文件
        
        Args:
            results: 结果列表
            output_path: 输出路径
            format: 输出格式 (json, csv)
        """
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        
        elif format == "csv":
            # 转换为DataFrame
            csv_data = []
            for result in results:
                row = {
                    "original_text": result.get("original_text", ""),
                    "ltl_formula": result.get("ltl_formula", ""),
                    "optimized_formula": result.get("optimized_formula", ""),
                    "is_valid": result.get("validation_result", {}).get("is_valid", False),
                    "complexity": result.get("interpretation_metadata", {}).get("complexity", ""),
                    "structure": result.get("interpretation_metadata", {}).get("structure", ""),
                    "language": result.get("interpretation_metadata", {}).get("language", ""),
                    "proposition_count": result.get("interpretation_metadata", {}).get("proposition_count", 0),
                    "errors": "; ".join(result.get("validation_result", {}).get("errors", [])),
                    "warnings": "; ".join(result.get("validation_result", {}).get("warnings", []))
                }
                csv_data.append(row)
            
            df = pd.DataFrame(csv_data)
            df.to_csv(output_path, index=False, encoding='utf-8')
        
        else:
            raise ValueError(f"不支持的格式: {format}")


def main():
    """
    主函数，用于测试增强版目标解释器
    """
    # 创建增强版目标解释器
    interpreter = EnhancedGoalInterpreter()
    
    # 测试用例
    test_cases = [
        "Go to the kitchen and get a glass of water",
        "If it's raining, then take an umbrella, otherwise wear sunglasses",
        "First turn on the lights, then open the window, finally adjust the temperature",
        "Repeat checking the mail until you find a package",
        "Clean the room and also wash the dishes simultaneously",
        "Eventually always ensure the door is locked",
        "When the alarm rings, immediately get out of bed",
        "Go to the store before it closes and buy groceries"
    ]
    
    print("=== 增强版目标解释器测试 ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case}")
        print("-" * 50)
        
        try:
            result = interpreter.interpret(test_case)
            
            print(f"原始文本: {result['original_text']}")
            print(f"生成的LTL公式: {result['ltl_formula']}")
            print(f"优化后的公式: {result['optimized_formula']}")
            print(f"公式有效性: {result['validation_result']['is_valid']}")
            
            metadata = result['interpretation_metadata']
            print(f"任务复杂度: {metadata['complexity']}")
            print(f"结构类型: {metadata['structure']}")
            print(f"语言: {metadata['language']}")
            print(f"命题数量: {metadata['proposition_count']}")
            print(f"条件数量: {metadata['condition_count']}")
            print(f"约束数量: {metadata['constraint_count']}")
            
            if result['validation_result']['warnings']:
                print(f"警告: {result['validation_result']['warnings']}")
            
            if result['validation_result']['errors']:
                print(f"错误: {result['validation_result']['errors']}")
            
            # 分析公式复杂度
            complexity = interpreter.analyze_formula_complexity(result['optimized_formula'])
            print(f"公式复杂度: {complexity['complexity_level']} (分数: {complexity['complexity_score']:.2f})")
            
        except Exception as e:
            print(f"解释失败: {e}")
        
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()