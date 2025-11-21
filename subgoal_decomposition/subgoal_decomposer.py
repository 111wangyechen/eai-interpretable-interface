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
            return self._temporal_hierarchical_decompose(formula_str, max_depth, max_subgoals)
        elif self.strategy == DecompositionStrategy.TASK_DEPENDENCY:
            return self._task_dependency_decompose(formula_str, max_depth, max_subgoals)
        elif self.strategy == DecompositionStrategy.SEMANTIC_CLUSTERING:
            return self._semantic_clustering_decompose(formula_str, max_depth, max_subgoals)
        else:  # HYBRID
            return self._hybrid_decompose(formula_str, max_depth, max_subgoals)
    
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
        
        subgoal = Subgoal(
            id=subgoal_id,
            description=f"Execute atomic action: {formula}",
            ltl_formula=formula,
            subgoal_type=SubgoalType.ATOMIC,
            dependencies=[],
            priority=depth,
            estimated_cost=1.0,
            preconditions=[],
            effects=[formula],
            metadata={'depth': depth, 'type': 'atomic'}
        )
        
        subgoals.append(subgoal)
        return subgoal_id
    
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