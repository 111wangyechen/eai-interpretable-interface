#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子目标验证和优化模块
负责验证分解结果的正确性和优化子目标序列
与现有的ltl_validator.py对齐
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Dict, List, Optional, Tuple, Set, Union
import re
import logging
from dataclasses import dataclass

from .subgoal_decomposer import Subgoal, DecompositionResult, SubgoalType
from goal_interpretation.ltl_validator import LTLValidator


@dataclass
class ValidationIssue:
    """验证问题数据类"""
    severity: str  # 'error', 'warning', 'info'
    message: str
    subgoal_id: Optional[str] = None
    suggestion: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class OptimizationResult:
    """优化结果数据类"""
    optimized_result: DecompositionResult
    improvements: List[str]
    performance_gain: float
    validation_issues_resolved: int
    metadata: Dict


class SubgoalValidator:
    """
    子目标验证器类
    负责验证分解结果的正确性
    """
    
    def __init__(self):
        """初始化验证器"""
        self.ltl_validator = LTLValidator()
        self.logger = logging.getLogger(__name__)
    
    def validate_decomposition(self, result: DecompositionResult) -> List[ValidationIssue]:
        """
        验证分解结果
        
        Args:
            result: 分解结果
            
        Returns:
            List[ValidationIssue]: 验证问题列表
        """
        issues = []
        
        # 验证基本结构
        issues.extend(self._validate_basic_structure(result))
        
        # 验证LTL公式
        issues.extend(self._validate_ltl_formulas(result))
        
        # 验证依赖关系
        issues.extend(self._validate_dependencies(result))
        
        # 验证执行顺序
        issues.extend(self._validate_execution_order(result))
        
        # 验证成本估计
        issues.extend(self._validate_costs(result))
        
        # 验证语义一致性
        issues.extend(self._validate_semantic_consistency(result))
        
        return issues
    
    def _validate_basic_structure(self, result: DecompositionResult) -> List[ValidationIssue]:
        """验证基本结构"""
        issues = []
        
        if not result.subgoals:
            issues.append(ValidationIssue(
                severity='error',
                message="分解结果为空",
                suggestion="确保输入的LTL公式有效"
            ))
            return issues
        
        if not result.root_subgoal:
            issues.append(ValidationIssue(
                severity='warning',
                message="缺少根子目标",
                suggestion="设置一个根子目标作为分解的起点"
            ))
        
        if not result.execution_order:
            issues.append(ValidationIssue(
                severity='error',
                message="缺少执行顺序",
                suggestion="计算子目标的执行顺序"
            ))
        
        # 检查子目标ID唯一性
        subgoal_ids = [sg.id for sg in result.subgoals]
        if len(subgoal_ids) != len(set(subgoal_ids)):
            issues.append(ValidationIssue(
                severity='error',
                message="子目标ID不唯一",
                suggestion="确保每个子目标都有唯一的ID"
            ))
        
        return issues
    
    def _validate_ltl_formulas(self, result: DecompositionResult) -> List[ValidationIssue]:
        """验证LTL公式"""
        issues = []
        
        for subgoal in result.subgoals:
            if not subgoal.ltl_formula:
                issues.append(ValidationIssue(
                    severity='error',
                    message=f"子目标 {subgoal.id} 缺少LTL公式",
                    subgoal_id=subgoal.id,
                    suggestion="为子目标设置有效的LTL公式"
                ))
                continue
            
            # 使用LTL验证器验证公式
            try:
                validation_result = self.ltl_validator.validate_formula(subgoal.ltl_formula)
                if not validation_result.is_valid:
                    issues.append(ValidationIssue(
                        severity='error',
                        message=f"子目标 {subgoal.id} 的LTL公式无效: {validation_result.error_message}",
                        subgoal_id=subgoal.id,
                        suggestion="修正LTL公式语法错误"
                    ))
            except Exception as e:
                issues.append(ValidationIssue(
                    severity='warning',
                    message=f"无法验证子目标 {subgoal.id} 的LTL公式: {str(e)}",
                    subgoal_id=subgoal.id,
                    suggestion="检查LTL公式格式"
                ))
        
        return issues
    
    def _validate_dependencies(self, result: DecompositionResult) -> List[ValidationIssue]:
        """验证依赖关系"""
        issues = []
        
        subgoal_ids = {sg.id for sg in result.subgoals}
        
        for subgoal in result.subgoals:
            # 检查依赖的子目标是否存在
            for dep_id in subgoal.dependencies:
                if dep_id not in subgoal_ids:
                    issues.append(ValidationIssue(
                        severity='error',
                        message=f"子目标 {subgoal.id} 依赖不存在的子目标 {dep_id}",
                        subgoal_id=subgoal.id,
                        suggestion=f"移除不存在的依赖 {dep_id} 或创建对应的子目标"
                    ))
            
            # 检查循环依赖
            if self._has_circular_dependency(subgoal.id, subgoal.dependencies, result.subgoals):
                issues.append(ValidationIssue(
                    severity='error',
                    message=f"子目标 {subgoal.id} 存在循环依赖",
                    subgoal_id=subgoal.id,
                    suggestion="重新设计子目标依赖关系以避免循环"
                ))
        
        return issues
    
    def _validate_execution_order(self, result: DecompositionResult) -> List[ValidationIssue]:
        """验证执行顺序"""
        issues = []
        
        if not result.execution_order:
            return issues
        
        # 检查执行顺序是否包含所有子目标
        order_ids = set(result.execution_order)
        subgoal_ids = {sg.id for sg in result.subgoals}
        
        missing_ids = subgoal_ids - order_ids
        if missing_ids:
            issues.append(ValidationIssue(
                severity='warning',
                message=f"执行顺序缺少子目标: {missing_ids}",
                suggestion="确保所有子目标都包含在执行顺序中"
            ))
        
        extra_ids = order_ids - subgoal_ids
        if extra_ids:
            issues.append(ValidationIssue(
                severity='warning',
                message=f"执行顺序包含不存在的子目标: {extra_ids}",
                suggestion="从执行顺序中移除不存在的子目标"
            ))
        
        # 检查依赖关系是否在执行顺序中得到满足
        for i, subgoal_id in enumerate(result.execution_order):
            subgoal = next((sg for sg in result.subgoals if sg.id == subgoal_id), None)
            if subgoal:
                for dep_id in subgoal.dependencies:
                    if dep_id in result.execution_order:
                        dep_index = result.execution_order.index(dep_id)
                        if dep_index > i:
                            issues.append(ValidationIssue(
                                severity='error',
                                message=f"子目标 {subgoal_id} 的依赖 {dep_id} 在执行顺序中位于其后",
                                subgoal_id=subgoal_id,
                                suggestion="调整执行顺序以满足依赖关系"
                            ))
        
        return issues
    
    def _validate_costs(self, result: DecompositionResult) -> List[ValidationIssue]:
        """验证成本估计"""
        issues = []
        
        total_cost = sum(sg.estimated_cost for sg in result.subgoals)
        
        if abs(total_cost - result.total_cost) > 0.01:
            issues.append(ValidationIssue(
                severity='warning',
                message=f"总成本不一致: 计算值 {total_cost} vs 记录值 {result.total_cost}",
                suggestion="更新总成本以匹配子目标成本之和"
            ))
        
        for subgoal in result.subgoals:
            if subgoal.estimated_cost < 0:
                issues.append(ValidationIssue(
                    severity='warning',
                    message=f"子目标 {subgoal.id} 的成本为负值: {subgoal.estimated_cost}",
                    subgoal_id=subgoal.id,
                    suggestion="设置非负的成本估计"
                ))
            elif subgoal.estimated_cost == 0:
                issues.append(ValidationIssue(
                    severity='info',
                    message=f"子目标 {subgoal.id} 的成本为零",
                    subgoal_id=subgoal.id,
                    suggestion="确认该子目标确实不需要成本"
                ))
        
        return issues
    
    def _validate_semantic_consistency(self, result: DecompositionResult) -> List[ValidationIssue]:
        """验证语义一致性"""
        issues = []
        
        # 检查原子子目标的语义
        atomic_subgoals = [sg for sg in result.subgoals if sg.subgoal_type == SubgoalType.ATOMIC]
        for subgoal in atomic_subgoals:
            if len(subgoal.ltl_formula.split()) > 3:
                issues.append(ValidationIssue(
                    severity='warning',
                    message=f"原子子目标 {subgoal.id} 的LTL公式过于复杂: {subgoal.ltl_formula}",
                    subgoal_id=subgoal.id,
                    suggestion="考虑将复杂的原子子目标进一步分解"
                ))
        
        # 检查并行子目标的一致性
        parallel_subgoals = [sg for sg in result.subgoals if sg.subgoal_type == SubgoalType.PARALLEL]
        for subgoal in parallel_subgoals:
            if subgoal.dependencies:
                issues.append(ValidationIssue(
                    severity='info',
                    message=f"并行子目标 {subgoal.id} 具有依赖关系",
                    subgoal_id=subgoal.id,
                    suggestion="确认并行子目标的依赖关系是否合理"
                ))
        
        return issues
    
    def _has_circular_dependency(self, subgoal_id: str, dependencies: List[str], 
                                all_subgoals: List[Subgoal], visited: Set[str] = None) -> bool:
        """检查是否存在循环依赖"""
        if visited is None:
            visited = set()
        
        if subgoal_id in visited:
            return True
        
        visited.add(subgoal_id)
        
        subgoal = next((sg for sg in all_subgoals if sg.id == subgoal_id), None)
        if subgoal:
            for dep_id in subgoal.dependencies:
                if self._has_circular_dependency(dep_id, [], all_subgoals, visited.copy()):
                    return True
        
        return False


class SubgoalOptimizer:
    """
    子目标优化器类
    负责优化子目标序列
    """
    
    def __init__(self):
        """初始化优化器"""
        self.logger = logging.getLogger(__name__)
    
    def optimize_decomposition(self, result: DecompositionResult, 
                            validation_issues: List[ValidationIssue] = None) -> OptimizationResult:
        """
        优化分解结果
        
        Args:
            result: 原始分解结果
            validation_issues: 验证问题列表
            
        Returns:
            OptimizationResult: 优化结果
        """
        if validation_issues is None:
            validation_issues = []
        
        improvements = []
        optimized_subgoals = result.subgoals.copy()
        
        # 修复错误
        fixed_issues = self._fix_errors(optimized_subgoals, validation_issues)
        improvements.extend(fixed_issues)
        
        # 优化执行顺序
        order_improvements = self._optimize_execution_order(optimized_subgoals)
        improvements.extend(order_improvements)
        
        # 优化成本估计
        cost_improvements = self._optimize_cost_estimates(optimized_subgoals)
        improvements.extend(cost_improvements)
        
        # 合并相似子目标
        merge_improvements = self._merge_similar_subgoals(optimized_subgoals)
        improvements.extend(merge_improvements)
        
        # 创建优化后的结果
        optimized_result = DecompositionResult(
            subgoals=optimized_subgoals,
            root_subgoal=result.root_subgoal,
            execution_order=self._compute_execution_order(optimized_subgoals),
            total_cost=sum(sg.estimated_cost for sg in optimized_subgoals),
            decomposition_strategy=result.decomposition_strategy,
            metadata={
                **result.metadata,
                'optimized': True,
                'original_subgoal_count': len(result.subgoals),
                'optimized_subgoal_count': len(optimized_subgoals)
            }
        )
        
        # 计算性能增益
        performance_gain = self._calculate_performance_gain(result, optimized_result)
        
        return OptimizationResult(
            optimized_result=optimized_result,
            improvements=improvements,
            performance_gain=performance_gain,
            validation_issues_resolved=len([i for i in improvements if '修复' in i or '移除' in i]),
            metadata={
                'optimization_time': 'unknown',
                'optimization_strategy': 'comprehensive'
            }
        )
    
    def _fix_errors(self, subgoals: List[Subgoal], issues: List[ValidationIssue]) -> List[str]:
        """修复错误"""
        improvements = []
        
        # 移除无效子目标
        valid_subgoals = []
        for subgoal in subgoals:
            is_valid = True
            
            # 检查是否有关于此子目标的严重错误
            for issue in issues:
                if (issue.severity == 'error' and 
                    issue.subgoal_id == subgoal.id and 
                    'LTL公式无效' in issue.message):
                    is_valid = False
                    improvements.append(f"移除无效子目标: {subgoal.id}")
                    break
            
            if is_valid:
                valid_subgoals.append(subgoal)
        
        subgoals.clear()
        subgoals.extend(valid_subgoals)
        
        # 修复依赖关系
        subgoal_ids = {sg.id for sg in subgoals}
        for subgoal in subgoals:
            original_deps = subgoal.dependencies.copy()
            subgoal.dependencies = [dep for dep in subgoal.dependencies if dep in subgoal_ids]
            
            if len(subgoal.dependencies) != len(original_deps):
                improvements.append(f"修复子目标 {subgoal.id} 的依赖关系")
        
        return improvements
    
    def _optimize_execution_order(self, subgoals: List[Subgoal]) -> List[str]:
        """优化执行顺序"""
        improvements = []
        
        # 按优先级和依赖关系排序
        def sort_key(subgoal):
            return (subgoal.priority, len(subgoal.dependencies), subgoal.estimated_cost)
        
        sorted_subgoals = sorted(subgoals, key=sort_key)
        
        # 检查是否有改进
        original_order = [sg.id for sg in subgoals]
        optimized_order = [sg.id for sg in sorted_subgoals]
        
        if original_order != optimized_order:
            improvements.append("优化子目标执行顺序")
            subgoals.clear()
            subgoals.extend(sorted_subgoals)
        
        return improvements
    
    def _optimize_cost_estimates(self, subgoals: List[Subgoal]) -> List[str]:
        """优化成本估计"""
        improvements = []
        
        for subgoal in subgoals:
            # 基于子目标类型和复杂度调整成本
            base_cost = subgoal.estimated_cost
            
            if subgoal.subgoal_type == SubgoalType.ATOMIC:
                # 原子子目标成本应该较低
                if subgoal.estimated_cost > 2.0:
                    subgoal.estimated_cost = 1.0
                    improvements.append(f"调整原子子目标 {subgoal.id} 的成本")
            
            elif subgoal.subgoal_type == SubgoalType.PARALLEL:
                # 并行子目标成本基于依赖数量
                estimated_cost = len(subgoal.dependencies) * 0.5 + 1.0
                if abs(subgoal.estimated_cost - estimated_cost) > 0.5:
                    subgoal.estimated_cost = estimated_cost
                    improvements.append(f"调整并行子目标 {subgoal.id} 的成本")
            
            elif subgoal.subgoal_type == SubgoalType.SEQUENTIAL:
                # 顺序子目标成本基于依赖和复杂度
                formula_complexity = len(subgoal.ltl_formula.split())
                estimated_cost = len(subgoal.dependencies) * 0.3 + formula_complexity * 0.1 + 1.0
                if abs(subgoal.estimated_cost - estimated_cost) > 0.5:
                    subgoal.estimated_cost = estimated_cost
                    improvements.append(f"调整顺序子目标 {subgoal.id} 的成本")
        
        return improvements
    
    def _merge_similar_subgoals(self, subgoals: List[Subgoal]) -> List[str]:
        """合并相似子目标"""
        improvements = []
        
        # 简单的合并策略：合并相同类型的原子子目标
        atomic_subgoals = [sg for sg in subgoals if sg.subgoal_type == SubgoalType.ATOMIC]
        
        # 按LTL公式分组
        formula_groups = {}
        for subgoal in atomic_subgoals:
            formula = subgoal.ltl_formula.strip()
            if formula not in formula_groups:
                formula_groups[formula] = []
            formula_groups[formula].append(subgoal)
        
        # 合并相同公式的子目标
        merged_count = 0
        for formula, group in formula_groups.items():
            if len(group) > 1:
                # 保留第一个，移除其他的
                main_subgoal = group[0]
                for duplicate in group[1:]:
                    if duplicate in subgoals:
                        subgoals.remove(duplicate)
                        merged_count += 1
                
                # 更新主子目标的描述
                main_subgoal.description = f"Merged atomic action: {formula}"
        
        if merged_count > 0:
            improvements.append(f"合并了 {merged_count} 个重复的原子子目标")
        
        return improvements
    
    def _compute_execution_order(self, subgoals: List[Subgoal]) -> List[str]:
        """计算执行顺序"""
        # 创建子目标ID到子目标的映射
        subgoal_map = {sg.id: sg for sg in subgoals}
        
        # 拓扑排序
        visited = set()
        temp_visited = set()
        order = []
        
        def dfs(subgoal_id: str):
            if subgoal_id in temp_visited:
                return  # 检测到循环，跳过
            if subgoal_id in visited:
                return
            
            temp_visited.add(subgoal_id)
            
            if subgoal_id in subgoal_map:
                for dep_id in subgoal_map[subgoal_id].dependencies:
                    dfs(dep_id)
            
            temp_visited.remove(subgoal_id)
            visited.add(subgoal_id)
            order.append(subgoal_id)
        
        # 对所有子目标进行DFS
        for subgoal in subgoals:
            if subgoal.id not in visited:
                dfs(subgoal.id)
        
        return order
    
    def _calculate_performance_gain(self, original: DecompositionResult, 
                                  optimized: DecompositionResult) -> float:
        """计算性能增益"""
        # 基于多个因素计算性能增益
        cost_reduction = (original.total_cost - optimized.total_cost) / original.total_cost if original.total_cost > 0 else 0
        
        subgoal_reduction = (len(original.subgoals) - len(optimized.subgoals)) / len(original.subgoals) if original.subgoals else 0
        
        # 综合性能增益
        performance_gain = (cost_reduction * 0.6 + subgoal_reduction * 0.4) * 100
        
        return round(performance_gain, 2)


class SubgoalAnalyzer:
    """
    子目标分析器类
    负责分析子目标的复杂度和特征
    """
    
    def __init__(self):
        """初始化分析器"""
        self.logger = logging.getLogger(__name__)
    
    def analyze_complexity(self, result: DecompositionResult) -> Dict:
        """
        分析分解结果的复杂度
        
        Args:
            result: 分解结果
            
        Returns:
            Dict: 复杂度分析结果
        """
        analysis = {
            'overall_complexity': 'medium',
            'subgoal_count': len(result.subgoals),
            'max_depth': 0,
            'dependency_complexity': 0,
            'type_distribution': {},
            'cost_distribution': {},
            'recommendations': []
        }
        
        # 分析子目标类型分布
        type_counts = {}
        for subgoal in result.subgoals:
            subgoal_type = subgoal.subgoal_type.value
            type_counts[subgoal_type] = type_counts.get(subgoal_type, 0) + 1
        analysis['type_distribution'] = type_counts
        
        # 分析深度
        max_depth = 0
        for subgoal in result.subgoals:
            depth = subgoal.metadata.get('depth', 0)
            max_depth = max(max_depth, depth)
        analysis['max_depth'] = max_depth
        
        # 分析依赖复杂度
        total_dependencies = sum(len(sg.dependencies) for sg in result.subgoals)
        analysis['dependency_complexity'] = total_dependencies / len(result.subgoals) if result.subgoals else 0
        
        # 分析成本分布
        costs = [sg.estimated_cost for sg in result.subgoals]
        if costs:
            analysis['cost_distribution'] = {
                'min': min(costs),
                'max': max(costs),
                'avg': sum(costs) / len(costs),
                'total': sum(costs)
            }
        
        # 生成建议
        analysis['recommendations'] = self._generate_complexity_recommendations(analysis)
        
        # 确定整体复杂度
        analysis['overall_complexity'] = self._determine_overall_complexity(analysis)
        
        return analysis
    
    def _generate_complexity_recommendations(self, analysis: Dict) -> List[str]:
        """生成复杂度建议"""
        recommendations = []
        
        if analysis['subgoal_count'] > 15:
            recommendations.append("子目标数量较多，考虑进一步简化或合并")
        
        if analysis['max_depth'] > 5:
            recommendations.append("分解深度较深，考虑减少层次结构")
        
        if analysis['dependency_complexity'] > 3:
            recommendations.append("依赖关系复杂，考虑简化依赖结构")
        
        atomic_ratio = analysis['type_distribution'].get('atomic', 0) / analysis['subgoal_count']
        if atomic_ratio > 0.8:
            recommendations.append("原子子目标比例过高，考虑增加更高层次的抽象")
        
        return recommendations
    
    def _determine_overall_complexity(self, analysis: Dict) -> str:
        """确定整体复杂度"""
        complexity_score = 0
        
        # 基于子目标数量
        if analysis['subgoal_count'] > 20:
            complexity_score += 3
        elif analysis['subgoal_count'] > 10:
            complexity_score += 2
        elif analysis['subgoal_count'] > 5:
            complexity_score += 1
        
        # 基于深度
        if analysis['max_depth'] > 6:
            complexity_score += 3
        elif analysis['max_depth'] > 4:
            complexity_score += 2
        elif analysis['max_depth'] > 2:
            complexity_score += 1
        
        # 基于依赖复杂度
        if analysis['dependency_complexity'] > 4:
            complexity_score += 3
        elif analysis['dependency_complexity'] > 2:
            complexity_score += 2
        elif analysis['dependency_complexity'] > 1:
            complexity_score += 1
        
        # 确定复杂度等级
        if complexity_score >= 7:
            return 'high'
        elif complexity_score >= 4:
            return 'medium'
        else:
            return 'low'