#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子目标分解器核心模块
负责将LTL形式化目标分解为可执行的子目标序列
与现有的goal_interpreter.py和ltl_generator.py对齐
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Dict, List, Optional, Tuple, Set, Union
from dataclasses import dataclass
from enum import Enum
import re
import json

from goal_interpretation.goal_interpreter import LTLFormula


class SubgoalType(Enum):
    """子目标类型枚举"""
    SEQUENTIAL = "sequential"    # 顺序执行
    PARALLEL = "parallel"       # 并行执行
    CONDITIONAL = "conditional"  # 条件执行
    ATOMIC = "atomic"           # 原子动作
    TEMPORAL = "temporal"       # 时序约束


class DecompositionStrategy(Enum):
    """分解策略枚举"""
    TEMPORAL_HIERARCHICAL = "temporal_hierarchical"  # 时序层次分解
    TASK_DEPENDENCY = "task_dependency"              # 任务依赖分解
    SEMANTIC_CLUSTERING = "semantic_clustering"     # 语义聚类分解
    HYBRID = "hybrid"                               # 混合策略


@dataclass
class Subgoal:
    """子目标数据类"""
    id: str
    description: str
    ltl_formula: str
    subgoal_type: SubgoalType
    dependencies: List[str]  # 依赖的子目标ID列表
    priority: int  # 优先级（数字越小优先级越高）
    estimated_cost: float  # 估计执行成本
    preconditions: List[str]  # 前提条件
    effects: List[str]  # 执行效果
    metadata: Dict  # 额外元数据
    
    def __post_init__(self):
        """后处理初始化"""
        if self.dependencies is None:
            self.dependencies = []
        if self.preconditions is None:
            self.preconditions = []
        if self.effects is None:
            self.effects = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """
        将子目标转换为字典格式，处理 SubgoalType 的序列化
        
        Returns:
            Dict: 可 JSON 序列化的字典
        """
        return {
            'id': self.id,
            'description': self.description,
            'ltl_formula': self.ltl_formula,
            'subgoal_type': self.subgoal_type.name,  # 使用枚举名称而不是枚举对象
            'dependencies': self.dependencies,
            'priority': self.priority,
            'estimated_cost': self.estimated_cost,
            'preconditions': self.preconditions,
            'effects': self.effects,
            'metadata': self.metadata
        }


@dataclass
class DecompositionResult:
    """分解结果数据类"""
    subgoals: List[Subgoal]
    root_subgoal: str  # 根子目标ID
    execution_order: List[str]  # 执行顺序
    total_cost: float  # 总估计成本
    decomposition_strategy: DecompositionStrategy
    metadata: Dict  # 分解元数据
    
    def __post_init__(self):
        """后处理初始化"""
        if self.metadata is None:
            self.metadata = {}


class SubgoalDecomposer:
    """
    子目标分解器类
    负责将LTL目标分解为结构化的子目标序列
    与现有的goal_interpreter.py和ltl_generator.py对齐
    """
    
    def __init__(self, strategy: DecompositionStrategy = DecompositionStrategy.TEMPORAL_HIERARCHICAL):
        """
        初始化子目标分解器
        
        Args:
            strategy: 分解策略
        """
        self.strategy = strategy
        self.subgoal_counter = 0
        
        # 初始化LTL操作符映射（与ltl_generator.py对齐）
        self.ltl_operators = {
            'F': 'finally',      # 最终
            'G': 'globally',     # 全局
            'X': 'next',         # 下一个
            'U': 'until',        # 直到
            '&': 'and',          # 并且
            '|': 'or',           # 或者
            '!': 'not',          # 非
            '->': 'implies',     # 蕴含
            '<->': 'equivalent'  # 等价
        }
        
        # 初始化分解模式（与goal_interpreter.py中的模式对齐）
        self.decomposition_patterns = {
            'sequential': [
                r'F\s*\(\s*(.*?)\s*->\s*F\s*\((.*?)\)\s*\)',  # F(a -> F(b))
                r'(.*?)\s*->\s*F\s*\((.*?)\)',                  # a -> F(b)
                r'G\s*\(\s*(.*?)\s*->\s*F\s*\((.*?)\)\s*\)',   # G(a -> F(b))
            ],
            'parallel': [
                r'F\s*\((.*?)\s*&\s*(.*?)\)',                  # F(a & b)
                r'(.*?)\s*&\s*(.*?)',                           # a & b
                r'G\s*\(\s*(.*?)\s*&\s*(.*?)\s*\)',            # G(a & b)
            ],
            'conditional': [
                r'(.*?)\s*->\s*(.*?)',                         # a -> b
                r'G\s*\(\s*(.*?)\s*->\s*(.*?)\s*\)',           # G(a -> b)
            ],
            'atomic': [
                r'[a-zA-Z_][a-zA-Z0-9_]*',                     # 简单命题
            ]
        }
    
    def decompose(self, ltl_formula: Union[str, LTLFormula], 
                  max_depth: int = 5, 
                  max_subgoals: int = 20) -> DecompositionResult:
        """
        分解LTL公式为子目标序列
        
        Args:
            ltl_formula: 输入的LTL公式或LTLFormula对象
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            
        Returns:
            DecompositionResult: 分解结果
        """
        # 重置计数器
        self.subgoal_counter = 0
        
        # 获取LTL公式字符串
        if isinstance(ltl_formula, LTLFormula):
            formula_str = ltl_formula.formula
        else:
            formula_str = ltl_formula
        
        # 根据策略选择分解方法
        if self.strategy == DecompositionStrategy.TEMPORAL_HIERARCHICAL:
            result = self._temporal_hierarchical_decompose(formula_str, max_depth, max_subgoals)
        elif self.strategy == DecompositionStrategy.TASK_DEPENDENCY:
            result = self._task_dependency_decompose(formula_str, max_depth, max_subgoals)
        elif self.strategy == DecompositionStrategy.SEMANTIC_CLUSTERING:
            result = self._semantic_clustering_decompose(formula_str, max_depth, max_subgoals)
        else:  # HYBRID
            result = self._hybrid_decompose(formula_str, max_depth, max_subgoals)
        
        # 增强子目标数量智能控制：如果子目标太少（少于3个），尝试进一步分解
        if len(result.subgoals) < 3 and len(result.subgoals) > 0:
            result = self._enhance_decomposition(result, max_depth, max_subgoals)
        
        # 智能合并相似子目标
        result = self._smart_merge_similar_subgoals(result)
        
        # 重新计算执行顺序和总成本
        result.execution_order = self._compute_execution_order(result.subgoals)
        result.total_cost = sum(subgoal.estimated_cost for subgoal in result.subgoals)
        
        # 添加可行性分析元数据
        feasibility = self._analyze_feasibility(result)
        result.metadata.update({
            'feasibility_analysis': feasibility,
            'decomposition_quality': self._evaluate_decomposition_quality(result)
        })
        
        return result
    
    def _enhance_decomposition(self, result: DecompositionResult, 
                              max_depth: int, max_subgoals: int) -> DecompositionResult:
        """
        增强分解结果，当子目标数量过少时进一步分解
        
        Args:
            result: 当前分解结果
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            
        Returns:
            DecompositionResult: 增强后的分解结果
        """
        enhanced_subgoals = []
        
        # 复制原结果中的子目标
        for subgoal in result.subgoals:
            # 尝试进一步分解非原子子目标
            if subgoal.subgoal_type != SubgoalType.ATOMIC:
                # 解析现有公式
                structure = self._parse_ltl_structure(subgoal.ltl_formula)
                temp_subgoals = []
                
                # 设置新的临时计数器
                temp_counter = self.subgoal_counter
                
                # 尝试分解
                self._recursive_decompose(structure, temp_subgoals, 
                                        subgoal.priority, max_depth, max_subgoals)
                
                # 如果成功分解出多个子目标，使用新子目标
                if len(temp_subgoals) > 1:
                    # 更新计数器
                    self.subgoal_counter = temp_counter + len(temp_subgoals)
                    
                    # 添加新子目标并继承原依赖
                    for new_subgoal in temp_subgoals:
                        # 继承原依赖
                        new_subgoal.dependencies = subgoal.dependencies.copy()
                        # 更新深度
                        new_subgoal.priority = subgoal.priority + new_subgoal.priority
                        enhanced_subgoals.append(new_subgoal)
                else:
                    # 无法进一步分解，保留原目标
                    enhanced_subgoals.append(subgoal)
            else:
                # 保留原子子目标
                enhanced_subgoals.append(subgoal)
        
        # 更新结果
        if len(enhanced_subgoals) > len(result.subgoals):
            result.subgoals = enhanced_subgoals
        
        return result
    
    def _smart_merge_similar_subgoals(self, result: DecompositionResult) -> DecompositionResult:
        """
        智能合并相似子目标
        
        Args:
            result: 当前分解结果
            
        Returns:
            DecompositionResult: 合并后的分解结果
        """
        if len(result.subgoals) <= 1:
            return result
        
        # 按照优先级和类型分组
        groups = {}
        for subgoal in result.subgoals:
            key = (subgoal.subgoal_type, subgoal.priority)
            if key not in groups:
                groups[key] = []
            groups[key].append(subgoal)
        
        # 合并相似子目标
        merged_subgoals = []
        processed_ids = set()
        
        for subgoal in result.subgoals:
            if subgoal.id in processed_ids:
                continue
            
            # 查找相似子目标
            similar_subgoals = []
            key = (subgoal.subgoal_type, subgoal.priority)
            
            for other in groups.get(key, []):
                if other.id == subgoal.id or other.id in processed_ids:
                    continue
                
                # 检查相似度（基于描述和公式的相似性）
                desc_similarity = self._calculate_similarity(subgoal.description, other.description)
                
                # 如果相似度高于阈值，考虑合并
                if desc_similarity > 0.6:
                    similar_subgoals.append(other)
                    processed_ids.add(other.id)
            
            # 如果找到相似子目标，进行合并
            if similar_subgoals:
                merged_subgoal = self._merge_subgoals([subgoal] + similar_subgoals)
                merged_subgoals.append(merged_subgoal)
                processed_ids.add(subgoal.id)
            else:
                merged_subgoals.append(subgoal)
        
        # 更新结果
        result.subgoals = merged_subgoals
        return result
    
    def _merge_subgoals(self, subgoals: List[Subgoal]) -> Subgoal:
        """
        合并多个子目标为一个
        
        Args:
            subgoals: 要合并的子目标列表
            
        Returns:
            Subgoal: 合并后的子目标
        """
        if not subgoals:
            raise ValueError("Cannot merge empty list of subgoals")
        
        if len(subgoals) == 1:
            return subgoals[0]
        
        # 创建新子目标ID
        merged_id = f"merged_{self.subgoal_counter}"
        self.subgoal_counter += 1
        
        # 合并描述
        base_desc = subgoals[0].description
        merged_desc = f"Combined action: {'; '.join([g.description for g in subgoals])}"
        
        # 合并LTL公式（对于原子动作，可以合并为并行执行）
        ltl_formulas = [g.ltl_formula for g in subgoals]
        merged_formula = " & ".join(ltl_formulas)
        if len(ltl_formulas) > 1:
            merged_formula = f"({merged_formula})"
        
        # 合并依赖
        merged_dependencies = []
        for subgoal in subgoals:
            merged_dependencies.extend(subgoal.dependencies)
        # 去重
        merged_dependencies = list(set(merged_dependencies))
        
        # 合并前提条件
        merged_preconditions = []
        for subgoal in subgoals:
            merged_preconditions.extend(subgoal.preconditions)
        merged_preconditions = list(set(merged_preconditions))
        
        # 合并效果
        merged_effects = []
        for subgoal in subgoals:
            merged_effects.extend(subgoal.effects)
        merged_effects = list(set(merged_effects))
        
        # 计算总成本
        total_cost = sum(g.estimated_cost for g in subgoals)
        # 合并有一定效率提升
        merged_cost = total_cost * 0.9
        
        # 合并元数据
        merged_metadata = {
            'merged_subgoals': [g.id for g in subgoals],
            'original_count': len(subgoals)
        }
        
        # 创建合并后的子目标
        merged_subgoal = Subgoal(
            id=merged_id,
            description=merged_desc,
            ltl_formula=merged_formula,
            subgoal_type=subgoals[0].subgoal_type,
            dependencies=merged_dependencies,
            priority=min(g.priority for g in subgoals),
            estimated_cost=merged_cost,
            preconditions=merged_preconditions,
            effects=merged_effects,
            metadata=merged_metadata
        )
        
        return merged_subgoal
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本之间的相似度
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            float: 相似度得分 (0.0-1.0)
        """
        # 简单的基于词袋的相似度计算
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 and not words2:
            return 0.0
        
        # Jaccard相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _analyze_feasibility(self, result: DecompositionResult) -> Dict[str, any]:
        """
        分析分解结果的可行性
        
        Args:
            result: 分解结果
            
        Returns:
            Dict: 可行性分析报告
        """
        analysis = {
            'dependency_cycles': self._check_dependency_cycles(result.subgoals),
            'unreachable_subgoals': self._find_unreachable_subgoals(result.subgoals),
            'missing_preconditions': self._identify_missing_preconditions(result.subgoals),
            'estimated_success_rate': self._estimate_success_rate(result)
        }
        
        # 综合评估
        analysis['is_feasible'] = not analysis['dependency_cycles'] and \
                                 len(analysis['unreachable_subgoals']) == 0 and \
                                 analysis['estimated_success_rate'] > 0.5
        
        return analysis
    
    def _check_dependency_cycles(self, subgoals: List[Subgoal]) -> List[List[str]]:
        """
        检查依赖循环
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[List[str]]: 循环依赖列表
        """
        # 构建依赖图
        graph = {}
        for subgoal in subgoals:
            graph[subgoal.id] = subgoal.dependencies
        
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # 找到循环
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                dfs(neighbor, path.copy())
            
            rec_stack.remove(node)
        
        for node in graph.keys():
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def _find_unreachable_subgoals(self, subgoals: List[Subgoal]) -> List[str]:
        """
        找出无法到达的子目标
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[str]: 无法到达的子目标ID列表
        """
        reachable = set()
        
        # 找出所有没有依赖的子目标（起点）
        start_subgoals = [s.id for s in subgoals if not s.dependencies]
        
        def mark_reachable(node):
            if node in reachable:
                return
            reachable.add(node)
            # 找出依赖于当前节点的所有子目标
            for subgoal in subgoals:
                if node in subgoal.dependencies:
                    mark_reachable(subgoal.id)
        
        # 从起点开始标记可达子目标
        for start in start_subgoals:
            mark_reachable(start)
        
        # 找出不可达的子目标
        all_ids = {s.id for s in subgoals}
        unreachable = list(all_ids - reachable)
        
        return unreachable
    
    def _identify_missing_preconditions(self, subgoals: List[Subgoal]) -> List[Dict[str, str]]:
        """
        识别缺失的前提条件
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[Dict]: 缺失前提条件列表
        """
        missing = []
        
        # 构建所有效果的集合
        all_effects = set()
        for subgoal in subgoals:
            all_effects.update(subgoal.effects)
        
        # 检查每个子目标的前提条件
        for subgoal in subgoals:
            for precondition in subgoal.preconditions:
                # 检查前提条件是否是某个子目标的效果，或者是否是初始条件
                if precondition not in all_effects:
                    missing.append({
                        'subgoal_id': subgoal.id,
                        'precondition': precondition,
                        'suggestion': f'Ensure {precondition} is established before executing {subgoal.description}'
                    })
        
        return missing
    
    def _estimate_success_rate(self, result: DecompositionResult) -> float:
        """
        估计成功执行率
        
        Args:
            result: 分解结果
            
        Returns:
            float: 成功执行率估计 (0.0-1.0)
        """
        # 基于多个因素的简单估计模型
        factors = {
            'depth_factor': min(1.0, 1.0 - (self._get_max_depth(result.subgoals) / 10.0)),
            'cost_factor': max(0.3, 1.0 - (result.total_cost / 50.0)),
            'dependency_factor': 0.5 if result.subgoals else 1.0,
            'subgoal_count_factor': min(1.0, 1.0 - (abs(len(result.subgoals) - 5) / 20.0))
        }
        
        # 计算依赖因子：依赖数量适中的子目标更好
        total_dependencies = sum(len(g.dependencies) for g in result.subgoals)
        avg_dependencies = total_dependencies / len(result.subgoals) if result.subgoals else 0
        factors['dependency_factor'] = max(0.3, 1.0 - abs(avg_dependencies - 1.0) / 5.0)
        
        # 加权平均
        weights = {
            'depth_factor': 0.2,
            'cost_factor': 0.2,
            'dependency_factor': 0.3,
            'subgoal_count_factor': 0.3
        }
        
        success_rate = sum(factors[k] * weights[k] for k in factors)
        return min(1.0, max(0.0, success_rate))
    
    def _evaluate_decomposition_quality(self, result: DecompositionResult) -> Dict[str, float]:
        """
        评估分解质量
        
        Args:
            result: 分解结果
            
        Returns:
            Dict: 质量评估指标
        """
        subgoals = result.subgoals
        if not subgoals:
            return {
                'granularity_score': 0.0,
                'balance_score': 0.0,
                'dependency_clarity_score': 0.0,
                'overall_score': 0.0
            }
        
        # 粒度评分：子目标数量适中
        granularity_score = min(1.0, 1.0 - (abs(len(subgoals) - 8) / 20.0))
        
        # 平衡性评分：子目标深度分布均匀
        depths = [g.priority for g in subgoals]
        max_depth = max(depths) if depths else 1
        depth_distribution = [depths.count(d) for d in range(max_depth + 1)]
        # 计算标准差（越小越平衡）
        import statistics
        if len(depth_distribution) > 1:
            std_dev = statistics.stdev(depth_distribution)
            balance_score = max(0.0, 1.0 - (std_dev / 10.0))
        else:
            balance_score = 1.0
        
        # 依赖清晰度评分：依赖关系明确
        total_possible_dependencies = len(subgoals) * (len(subgoals) - 1)
        actual_dependencies = sum(len(g.dependencies) for g in subgoals)
        dependency_ratio = actual_dependencies / total_possible_dependencies if total_possible_dependencies > 0 else 0
        # 适中的依赖比例最好
        dependency_clarity_score = max(0.0, 1.0 - abs(dependency_ratio - 0.3) / 0.5)
        
        # 综合评分
        overall_score = 0.3 * granularity_score + 0.3 * balance_score + 0.4 * dependency_clarity_score
        
        return {
            'granularity_score': round(granularity_score, 2),
            'balance_score': round(balance_score, 2),
            'dependency_clarity_score': round(dependency_clarity_score, 2),
            'overall_score': round(overall_score, 2)
        }
    
    def _temporal_hierarchical_decompose(self, formula: str, max_depth: int, max_subgoals: int) -> DecompositionResult:
        """
        时序层次分解策略
        基于LTL的时序操作符进行层次化分解
        
        Args:
            formula: LTL公式
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            DecompositionResult: 分解结果
        """
        subgoals = []
        root_id = None
        
        # 解析顶层结构
        parsed_structure = self._parse_ltl_structure(formula)
        
        # 递归分解
        root_id = self._recursive_decompose(parsed_structure, subgoals, 0, max_depth, max_subgoals)
        
        # 计算执行顺序
        execution_order = self._compute_execution_order(subgoals)
        
        # 计算总成本
        total_cost = sum(sg.estimated_cost for sg in subgoals)
        
        return DecompositionResult(
            subgoals=subgoals,
            root_subgoal=root_id,
            execution_order=execution_order,
            total_cost=total_cost,
            decomposition_strategy=self.strategy,
            metadata={
                'decomposition_method': 'temporal_hierarchical',
                'max_depth_reached': self._get_max_depth(subgoals),
                'original_formula': formula
            }
        )
    
    def _task_dependency_decompose(self, formula: str, max_depth: int, max_subgoals: int) -> DecompositionResult:
        """
        任务依赖分解策略
        基于任务间的依赖关系进行分解
        
        Args:
            formula: LTL公式
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            DecompositionResult: 分解结果
        """
        subgoals = []
        
        # 提取原子命题
        atomic_props = self._extract_atomic_propositions(formula)
        
        # 分析依赖关系
        dependencies = self._analyze_dependencies(formula, atomic_props)
        
        # 创建子目标
        for i, prop in enumerate(atomic_props):
            if len(subgoals) >= max_subgoals:
                break
                
            subgoal_id = f"subgoal_{i}"
            deps = [f"subgoal_{j}" for j, dep in enumerate(atomic_props) 
                   if dep in dependencies.get(prop, [])]
            
            subgoal = Subgoal(
                id=subgoal_id,
                description=f"Execute {prop}",
                ltl_formula=prop,
                subgoal_type=SubgoalType.ATOMIC,
                dependencies=deps,
                priority=i,
                estimated_cost=1.0,
                preconditions=dependencies.get(prop, []),
                effects=[prop],
                metadata={'source': 'task_dependency', 'atomic_prop': prop}
            )
            subgoals.append(subgoal)
        
        # 计算执行顺序
        execution_order = self._topological_sort(subgoals)
        
        return DecompositionResult(
            subgoals=subgoals,
            root_subgoal=subgoals[0].id if subgoals else None,
            execution_order=execution_order,
            total_cost=len(subgoals),
            decomposition_strategy=self.strategy,
            metadata={
                'decomposition_method': 'task_dependency',
                'dependencies_found': len(dependencies),
                'original_formula': formula
            }
        )
    
    def _semantic_clustering_decompose(self, formula: str, max_depth: int, max_subgoals: int) -> DecompositionResult:
        """
        语义聚类分解策略
        基于语义相似性对子目标进行聚类分解
        
        Args:
            formula: LTL公式
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            DecompositionResult: 分解结果
        """
        subgoals = []
        
        # 提取语义单元
        semantic_units = self._extract_semantic_units(formula)
        
        # 聚类语义单元
        clusters = self._cluster_semantic_units(semantic_units)
        
        # 为每个聚类创建子目标
        for cluster_id, cluster_units in enumerate(clusters):
            if len(subgoals) >= max_subgoals:
                break
                
            cluster_formula = " & ".join(unit['formula'] for unit in cluster_units)
            cluster_desc = f"Execute cluster {cluster_id}: {', '.join(unit['description'] for unit in cluster_units)}"
            
            subgoal = Subgoal(
                id=f"cluster_{cluster_id}",
                description=cluster_desc,
                ltl_formula=cluster_formula,
                subgoal_type=SubgoalType.PARALLEL,
                dependencies=[],
                priority=cluster_id,
                estimated_cost=len(cluster_units),
                preconditions=[],
                effects=[unit['formula'] for unit in cluster_units],
                metadata={
                    'source': 'semantic_clustering',
                    'cluster_size': len(cluster_units),
                    'units': cluster_units
                }
            )
            subgoals.append(subgoal)
        
        # 计算执行顺序（并行聚类可以同时执行）
        execution_order = [sg.id for sg in subgoals]
        
        return DecompositionResult(
            subgoals=subgoals,
            root_subgoal=subgoals[0].id if subgoals else None,
            execution_order=execution_order,
            total_cost=sum(sg.estimated_cost for sg in subgoals),
            decomposition_strategy=self.strategy,
            metadata={
                'decomposition_method': 'semantic_clustering',
                'clusters_found': len(clusters),
                'original_formula': formula
            }
        )
    
    def _hybrid_decompose(self, formula: str, max_depth: int, max_subgoals: int) -> DecompositionResult:
        """
        混合分解策略
        结合多种策略的优势
        
        Args:
            formula: LTL公式
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            DecompositionResult: 分解结果
        """
        # 首先尝试时序层次分解
        try:
            temporal_result = self._temporal_hierarchical_decompose(formula, max_depth, max_subgoals)
            if len(temporal_result.subgoals) <= max_subgoals // 2:
                return temporal_result
        except Exception:
            pass
        
        # 如果时序分解效果不佳，尝试任务依赖分解
        try:
            dependency_result = self._task_dependency_decompose(formula, max_depth, max_subgoals)
            if len(dependency_result.subgoals) <= max_subgoals * 0.8:
                return dependency_result
        except Exception:
            pass
        
        # 最后使用语义聚类分解
        return self._semantic_clustering_decompose(formula, max_depth, max_subgoals)
    
    def _parse_ltl_structure(self, formula: str) -> Dict:
        """
        解析LTL公式结构
        
        Args:
            formula: LTL公式
            
        Returns:
            Dict: 解析后的结构
        """
        # 移除多余空格
        formula = re.sub(r'\s+', '', formula)
        
        # 简单的LTL解析器
        structure = {
            'type': 'unknown',
            'operator': None,
            'operands': [],
            'raw': formula
        }
        
        # 检查时序操作符
        for op in ['F', 'G', 'X']:
            if formula.startswith(op):
                structure['type'] = 'temporal'
                structure['operator'] = op
                # 提取操作数
                if len(formula) > 1 and formula[1] == '(':
                    # 找到匹配的括号
                    depth = 1
                    end_pos = 2
                    for i, char in enumerate(formula[2:], 2):
                        if char == '(':
                            depth += 1
                        elif char == ')':
                            depth -= 1
                            if depth == 0:
                                end_pos = i
                                break
                    operand = formula[2:end_pos]
                    structure['operands'].append(operand)
                break
        
        # 检查逻辑操作符
        for op in ['&', '|', '->', '<->']:
            if op in formula:
                structure['type'] = 'logical'
                structure['operator'] = op
                parts = formula.split(op)
                structure['operands'] = [p.strip() for p in parts if p.strip()]
                break
        
        # 如果没有找到操作符，认为是原子命题
        if structure['type'] == 'unknown':
            structure['type'] = 'atomic'
            structure['operands'] = [formula]
        
        return structure
    
    def _recursive_decompose(self, structure: Dict, subgoals: List[Subgoal], 
                           depth: int, max_depth: int, max_subgoals: int) -> str:
        """
        递归分解LTL结构
        
        Args:
            structure: LTL结构
            subgoals: 子目标列表
            depth: 当前深度
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            str: 当前子目标ID
        """
        if depth >= max_depth or len(subgoals) >= max_subgoals:
            # 达到深度或数量限制，创建原子子目标
            return self._create_atomic_subgoal(structure['raw'], subgoals, depth)
        
        subgoal_id = f"subgoal_{self.subgoal_counter}"
        self.subgoal_counter += 1
        
        # 根据结构类型创建子目标
        if structure['type'] == 'atomic':
            return self._create_atomic_subgoal(structure['raw'], subgoals, depth)
        
        elif structure['type'] == 'temporal':
            return self._create_temporal_subgoal(structure, subgoals, depth, max_depth, max_subgoals)
        
        elif structure['type'] == 'logical':
            return self._create_logical_subgoal(structure, subgoals, depth, max_depth, max_subgoals)
        
        else:
            return self._create_atomic_subgoal(structure['raw'], subgoals, depth)
    
    def _create_atomic_subgoal(self, formula: str, subgoals: List[Subgoal], depth: int) -> str:
        """
        创建原子子目标
        
        Args:
            formula: 原子公式
            subgoals: 子目标列表
            depth: 深度
            
        Returns:
            str: 子目标ID
        """
        subgoal_id = f"atomic_{self.subgoal_counter}"
        self.subgoal_counter += 1
        
        # 确保生成完整的动作描述
        action_description = formula
        
        # 全面处理formula的格式问题
        if formula:
            # 移除任何位置的"_the"后缀或部分
            if "_the" in action_description:
                # 更健壮的处理：移除末尾的"_the"
                if action_description.endswith('_the'):
                    action_description = action_description[:-4]
                else:
                    # 处理中间包含"_the"的情况
                    action_description = action_description.replace('_the_', '_')
            
            # 为简单动作添加前缀，确保动作名称格式正确
            if len(action_description.split('_')) < 2 and not action_description.startswith('perform_'):
                action_description = f"perform_{action_description}"
        
        # 增强：自动推断前提条件和依赖关系
        preconditions = self._infer_preconditions(action_description)
        dependencies = self._infer_dependencies(action_description, subgoals)
        
        # 增强：基于动作类型计算更准确的成本
        estimated_cost = self._calculate_action_cost(action_description)
        
        # 增强：生成更详细的效果描述
        effects = self._generate_detailed_effects(action_description)
        
        # 增强：添加动作可行性评分
        feasibility_score = self._assess_action_feasibility(action_description)
        
        subgoal = Subgoal(
            id=subgoal_id,
            description=f"Execute atomic action: {action_description}",
            ltl_formula=action_description,  # 使用处理后的动作描述作为LTL公式
            subgoal_type=SubgoalType.ATOMIC,
            dependencies=dependencies,
            priority=depth,
            estimated_cost=estimated_cost,
            preconditions=preconditions,
            effects=effects,
            metadata={
                'depth': depth, 
                'type': 'atomic', 
                'original_formula': formula,
                'feasibility_score': feasibility_score,
                'action_type': self._classify_action_type(action_description)
            }
        )
        
        subgoals.append(subgoal)
        return subgoal_id
    
    def _infer_preconditions(self, action_description: str) -> List[str]:
        """
        自动推断动作的前提条件
        
        Args:
            action_description: 动作描述
            
        Returns:
            List[str]: 推断的前提条件列表
        """
        preconditions = []
        
        # 基于动作名称和模式推断前提条件
        action_lower = action_description.lower()
        
        # 移动相关动作
        if any(keyword in action_lower for keyword in ['move', 'walk', 'go', 'approach', 'navigate']):
            preconditions.append('agent_available')
            preconditions.append('path_clear')
        
        # 抓取相关动作
        elif any(keyword in action_lower for keyword in ['pick', 'grab', 'take', 'grasp']):
            preconditions.append('agent_available')
            preconditions.append('object_visible')
            preconditions.append('object_reachable')
        
        # 放置相关动作
        elif any(keyword in action_lower for keyword in ['place', 'put', 'drop', 'release']):
            preconditions.append('agent_available')
            preconditions.append('object_in_hand')
            preconditions.append('target_location_clear')
        
        # 操作相关动作
        elif any(keyword in action_lower for keyword in ['open', 'close', 'turn', 'activate', 'deactivate']):
            preconditions.append('agent_available')
            preconditions.append('object_visible')
            preconditions.append('object_reachable')
        
        # 检查相关动作
        elif any(keyword in action_lower for keyword in ['check', 'verify', 'inspect', 'monitor']):
            preconditions.append('agent_available')
            preconditions.append('object_visible')
        
        # 通信相关动作
        elif any(keyword in action_lower for keyword in ['communicate', 'report', 'say', 'tell']):
            preconditions.append('agent_available')
            preconditions.append('communication_channel_available')
        
        # 默认前提条件
        else:
            preconditions.append('agent_available')
        
        return preconditions
    
    def _infer_dependencies(self, action_description: str, existing_subgoals: List[Subgoal]) -> List[str]:
        """
        自动推断动作的依赖关系
        
        Args:
            action_description: 动作描述
            existing_subgoals: 已存在的子目标列表
            
        Returns:
            List[str]: 推断的依赖关系列表
        """
        dependencies = []
        
        # 基于现有子目标的效果来推断依赖
        for subgoal in existing_subgoals:
            for effect in subgoal.effects:
                # 如果现有子目标的效果是当前动作的前提条件，添加依赖
                if effect in self._infer_preconditions(action_description):
                    dependencies.append(subgoal.id)
                    break
        
        # 基于动作顺序的简单规则
        if len(existing_subgoals) > 0:
            action_lower = action_description.lower()
            
            # 放置动作通常依赖于抓取动作
            if any(place_keyword in action_lower for place_keyword in ['place', 'put', 'drop', 'release']):
                for subgoal in existing_subgoals:
                    if any(grab_keyword in subgoal.description.lower() 
                           for grab_keyword in ['pick', 'grab', 'take', 'grasp']):
                        dependencies.append(subgoal.id)
                        break
        
        return list(set(dependencies))  # 去重
    
    def _calculate_action_cost(self, action_description: str) -> float:
        """
        基于动作类型计算更准确的成本
        
        Args:
            action_description: 动作描述
            
        Returns:
            float: 估计成本
        """
        # 基础成本
        base_cost = 1.0
        
        # 动作复杂度因子
        complexity_factor = 1.0
        action_lower = action_description.lower()
        
        # 简单动作
        simple_actions = ['check', 'verify', 'observe', 'monitor', 'report']
        if any(action in action_lower for action in simple_actions):
            complexity_factor = 0.7
        
        # 中等复杂度动作
        medium_actions = ['move', 'walk', 'approach', 'open', 'close', 'turn']
        if any(action in action_lower for action in medium_actions):
            complexity_factor = 1.0
        
        # 高复杂度动作
        complex_actions = ['pick', 'grab', 'take', 'place', 'put', 'assemble', 'disassemble', 'operate']
        if any(action in action_lower for action in complex_actions):
            complexity_factor = 1.5
        
        # 非常复杂的动作
        very_complex_actions = ['repair', 'install', 'configure', 'program', 'solve']
        if any(action in action_lower for action in very_complex_actions):
            complexity_factor = 2.5
        
        # 动作长度因子（通常更长的动作描述表示更复杂的动作）
        length_factor = 1.0 + min(0.5, (len(action_description) - 10) / 50.0)
        
        # 计算总成本
        total_cost = base_cost * complexity_factor * length_factor
        
        return round(total_cost, 2)
    
    def _generate_detailed_effects(self, action_description: str) -> List[str]:
        """
        生成更详细的动作效果描述
        
        Args:
            action_description: 动作描述
            
        Returns:
            List[str]: 详细效果列表
        """
        effects = [action_description]  # 保留原始描述
        
        action_lower = action_description.lower()
        
        # 移动相关效果
        if any(keyword in action_lower for keyword in ['move', 'walk', 'go', 'approach', 'navigate']):
            effects.append('agent_position_changed')
            # 提取目标位置
            match = re.search(r'to_(\w+)', action_lower)
            if match:
                target = match.group(1)
                effects.append(f'agent_at_{target}')
        
        # 抓取相关效果
        elif any(keyword in action_lower for keyword in ['pick', 'grab', 'take', 'grasp']):
            effects.append('object_in_hand')
            effects.append('object_moved')
        
        # 放置相关效果
        elif any(keyword in action_lower for keyword in ['place', 'put', 'drop', 'release']):
            effects.append('object_placed')
            effects.append('hand_empty')
        
        # 开关相关效果
        elif 'open' in action_lower:
            effects.append('object_opened')
        elif 'close' in action_lower:
            effects.append('object_closed')
        
        # 激活相关效果
        elif 'activate' in action_lower:
            effects.append('device_active')
        elif 'deactivate' in action_lower:
            effects.append('device_inactive')
        
        # 检查相关效果
        elif any(keyword in action_lower for keyword in ['check', 'verify', 'inspect', 'monitor']):
            effects.append('information_obtained')
        
        return effects
    
    def _assess_action_feasibility(self, action_description: str) -> float:
        """
        评估动作的可行性
        
        Args:
            action_description: 动作描述
            
        Returns:
            float: 可行性评分 (0.0-1.0)
        """
        # 基于动作类型和模式的简单可行性评估
        action_lower = action_description.lower()
        
        # 常见且简单的动作通常可行性更高
        simple_feasible_actions = ['check', 'verify', 'observe', 'monitor', 'move', 'walk', 'approach']
        if any(action in action_lower for action in simple_feasible_actions):
            return 0.9
        
        # 中等复杂性的动作
        medium_actions = ['open', 'close', 'turn', 'grab', 'pick', 'place', 'put']
        if any(action in action_lower for action in medium_actions):
            return 0.7
        
        # 复杂或不太常见的动作
        complex_actions = ['assemble', 'disassemble', 'repair', 'install', 'configure']
        if any(action in action_lower for action in complex_actions):
            return 0.5
        
        # 非常复杂或罕见的动作
        very_complex_actions = ['program', 'solve', 'design', 'create', 'invent']
        if any(action in action_lower for action in very_complex_actions):
            return 0.3
        
        # 默认可行性
        return 0.6
    
    def _classify_action_type(self, action_description: str) -> str:
        """
        分类动作类型
        
        Args:
            action_description: 动作描述
            
        Returns:
            str: 动作类型
        """
        action_lower = action_description.lower()
        
        if any(keyword in action_lower for keyword in ['move', 'walk', 'go', 'approach', 'navigate']):
            return 'movement'
        elif any(keyword in action_lower for keyword in ['pick', 'grab', 'take', 'grasp', 'place', 'put', 'drop']):
            return 'manipulation'
        elif any(keyword in action_lower for keyword in ['open', 'close', 'turn', 'activate', 'deactivate']):
            return 'operation'
        elif any(keyword in action_lower for keyword in ['check', 'verify', 'inspect', 'monitor', 'observe']):
            return 'perception'
        elif any(keyword in action_lower for keyword in ['communicate', 'report', 'say', 'tell']):
            return 'communication'
        elif any(keyword in action_lower for keyword in ['assemble', 'disassemble', 'repair', 'install']):
            return 'maintenance'
        else:
            return 'general'
    
    def _create_temporal_subgoal(self, structure: Dict, subgoals: List[Subgoal], 
                                depth: int, max_depth: int, max_subgoals: int) -> str:
        """
        创建时序子目标
        
        Args:
            structure: 时序结构
            subgoals: 子目标列表
            depth: 当前深度
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            str: 子目标ID
        """
        operator = structure['operator']
        operand = structure['operands'][0] if structure['operands'] else ''
        
        # 递归分解操作数
        operand_structure = self._parse_ltl_structure(operand)
        child_id = self._recursive_decompose(operand_structure, subgoals, 
                                            depth + 1, max_depth, max_subgoals)
        
        subgoal_id = f"temporal_{self.subgoal_counter}"
        self.subgoal_counter += 1
        
        # 确定子目标类型
        if operator == 'F':
            subgoal_type = SubgoalType.TEMPORAL
            desc = f"Eventually: {operand}"
        elif operator == 'G':
            subgoal_type = SubgoalType.TEMPORAL
            desc = f"Globally: {operand}"
        elif operator == 'X':
            subgoal_type = SubgoalType.SEQUENTIAL
            desc = f"Next: {operand}"
        else:
            subgoal_type = SubgoalType.ATOMIC
            desc = f"Temporal {operator}: {operand}"
        
        subgoal = Subgoal(
            id=subgoal_id,
            description=desc,
            ltl_formula=structure['raw'],
            subgoal_type=subgoal_type,
            dependencies=[child_id] if operator in ['F', 'X'] else [],
            priority=depth,
            estimated_cost=2.0 if operator == 'F' else 1.5,
            preconditions=[],
            effects=[operand],
            metadata={
                'depth': depth,
                'type': 'temporal',
                'operator': operator,
                'child_id': child_id
            }
        )
        
        subgoals.append(subgoal)
        return subgoal_id
    
    def _create_logical_subgoal(self, structure: Dict, subgoals: List[Subgoal], 
                              depth: int, max_depth: int, max_subgoals: int) -> str:
        """
        创建逻辑子目标
        
        Args:
            structure: 逻辑结构
            subgoals: 子目标列表
            depth: 当前深度
            max_depth: 最大深度
            max_subgoals: 最大子目标数
            
        Returns:
            str: 子目标ID
        """
        operator = structure['operator']
        operands = structure['operands']
        
        # 递归分解所有操作数
        child_ids = []
        for operand in operands:
            if len(subgoals) >= max_subgoals:
                break
            operand_structure = self._parse_ltl_structure(operand)
            child_id = self._recursive_decompose(operand_structure, subgoals, 
                                                depth + 1, max_depth, max_subgoals)
            child_ids.append(child_id)
        
        subgoal_id = f"logical_{self.subgoal_counter}"
        self.subgoal_counter += 1
        
        # 确定子目标类型和描述
        if operator == '&':
            subgoal_type = SubgoalType.PARALLEL
            desc = f"Parallel: {' & '.join(operands)}"
        elif operator == '|':
            subgoal_type = SubgoalType.CONDITIONAL
            desc = f"Choice: {' | '.join(operands)}"
        elif operator == '->':
            subgoal_type = SubgoalType.CONDITIONAL
            desc = f"Conditional: {' -> '.join(operands)}"
        else:
            subgoal_type = SubgoalType.ATOMIC
            desc = f"Logical {operator}: {' '.join(operands)}"
        
        subgoal = Subgoal(
            id=subgoal_id,
            description=desc,
            ltl_formula=structure['raw'],
            subgoal_type=subgoal_type,
            dependencies=child_ids if operator == '->' else [],
            priority=depth,
            estimated_cost=len(operands) * 1.5,
            preconditions=[operands[0]] if operator == '->' else [],
            effects=operands,
            metadata={
                'depth': depth,
                'type': 'logical',
                'operator': operator,
                'child_ids': child_ids
            }
        )
        
        subgoals.append(subgoal)
        return subgoal_id
    
    def _extract_atomic_propositions(self, formula: str) -> List[str]:
        """
        提取原子命题
        
        Args:
            formula: LTL公式
            
        Returns:
            List[str]: 原子命题列表
        """
        # 简单的原子命题提取：匹配字母开头的标识符
        pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        propositions = re.findall(pattern, formula)
        
        # 过滤掉LTL操作符
        ltl_keywords = {'F', 'G', 'X', 'U', 'True', 'False'}
        atomic_props = [prop for prop in propositions if prop not in ltl_keywords]
        
        return list(set(atomic_props))  # 去重
    
    def _analyze_dependencies(self, formula: str, atomic_props: List[str]) -> Dict[str, List[str]]:
        """
        分析原子命题间的依赖关系
        
        Args:
            formula: LTL公式
            atomic_props: 原子命题列表
            
        Returns:
            Dict[str, List[str]]: 依赖关系字典
        """
        dependencies = {}
        
        # 简单的依赖分析：基于蕴含操作符
        implication_pattern = r'([^&|()]+)\s*->\s*([^&|()]+)'
        matches = re.findall(implication_pattern, formula)
        
        for antecedent, consequent in matches:
            antecedent = antecedent.strip()
            consequent = consequent.strip()
            
            if antecedent in atomic_props and consequent in atomic_props:
                if consequent not in dependencies:
                    dependencies[consequent] = []
                if antecedent not in dependencies[consequent]:
                    dependencies[consequent].append(antecedent)
        
        return dependencies
    
    def _extract_semantic_units(self, formula: str) -> List[Dict]:
        """
        提取语义单元
        
        Args:
            formula: LTL公式
            
        Returns:
            List[Dict]: 语义单元列表
        """
        units = []
        
        # 基于简单的模式匹配提取语义单元
        patterns = [
            (r'F\s*\(\s*([^()]+)\s*\)', 'finally'),
            (r'G\s*\(\s*([^()]+)\s*\)', 'globally'),
            (r'X\s*\(\s*([^()]+)\s*\)', 'next'),
            (r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', 'atomic'),
        ]
        
        for pattern, unit_type in patterns:
            matches = re.findall(pattern, formula)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                
                units.append({
                    'formula': match.strip(),
                    'description': f"{unit_type}: {match.strip()}",
                    'type': unit_type,
                    'complexity': len(match)
                })
        
        return units
    
    def _cluster_semantic_units(self, units: List[Dict]) -> List[List[Dict]]:
        """
        聚类语义单元
        
        Args:
            units: 语义单元列表
            
        Returns:
            List[List[Dict]]: 聚类结果
        """
        if not units:
            return []
        
        # 简单的聚类策略：按类型分组
        clusters = {}
        for unit in units:
            unit_type = unit['type']
            if unit_type not in clusters:
                clusters[unit_type] = []
            clusters[unit_type].append(unit)
        
        # 如果聚类太多，合并小的聚类
        if len(clusters) > 3:
            # 按复杂度排序，合并复杂度低的聚类
            sorted_clusters = sorted(clusters.items(), key=lambda x: sum(u['complexity'] for u in x[1]))
            
            merged_clusters = []
            current_cluster = []
            current_complexity = 0
            
            for cluster_type, cluster_units in sorted_clusters:
                cluster_complexity = sum(u['complexity'] for u in cluster_units)
                
                if current_complexity + cluster_complexity > 10 and current_cluster:
                    merged_clusters.append(current_cluster)
                    current_cluster = []
                    current_complexity = 0
                
                current_cluster.extend(cluster_units)
                current_complexity += cluster_complexity
            
            if current_cluster:
                merged_clusters.append(current_cluster)
            
            return merged_clusters
        
        return list(clusters.values())
    
    def _compute_execution_order(self, subgoals: List[Subgoal]) -> List[str]:
        """
        计算子目标执行顺序
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[str]: 执行顺序
        """
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
    
    def _topological_sort(self, subgoals: List[Subgoal]) -> List[str]:
        """
        拓扑排序
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[str]: 拓扑排序结果
        """
        return self._compute_execution_order(subgoals)
    
    def _get_max_depth(self, subgoals: List[Subgoal]) -> int:
        """
        获取子目标的最大深度
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            int: 最大深度
        """
        if not subgoals:
            return 0
        return max(sg.metadata.get('depth', 0) for sg in subgoals)
    
    def set_strategy(self, strategy: DecompositionStrategy):
        """
        设置分解策略
        
        Args:
            strategy: 新的分解策略
        """
        self.strategy = strategy
    
    def get_supported_strategies(self) -> List[DecompositionStrategy]:
        """
        获取支持的分解策略
        
        Returns:
            List[DecompositionStrategy]: 支持的策略列表
        """
        return list(DecompositionStrategy)
    
    def visualize_decomposition(self, result: DecompositionResult) -> str:
        """
        可视化分解结果
        
        Args:
            result: 分解结果
            
        Returns:
            str: 可视化字符串
        """
        lines = []
        lines.append("=" * 60)
        lines.append("子目标分解结果可视化")
        lines.append("=" * 60)
        lines.append(f"分解策略: {result.decomposition_strategy.value}")
        lines.append(f"子目标数量: {len(result.subgoals)}")
        lines.append(f"总估计成本: {result.total_cost:.2f}")
        lines.append(f"根子目标: {result.root_subgoal}")
        lines.append("")
        
        lines.append("执行顺序:")
        for i, subgoal_id in enumerate(result.execution_order):
            subgoal = next((sg for sg in result.subgoals if sg.id == subgoal_id), None)
            if subgoal:
                lines.append(f"  {i+1}. {subgoal_id}: {subgoal.description}")
                if subgoal.dependencies:
                    lines.append(f"     依赖: {', '.join(subgoal.dependencies)}")
                lines.append(f"     成本: {subgoal.estimated_cost:.2f}")
                lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)