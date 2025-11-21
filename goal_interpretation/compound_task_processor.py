#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复合任务结构处理器
支持复杂任务结构的分解和处理
"""

from typing import Dict, List, Optional, Tuple, Union, Any
import re
from dataclasses import dataclass
from enum import Enum


class TaskStructureType(Enum):
    """任务结构类型枚举"""
    SIMPLE = "simple"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    ITERATIVE = "iterative"
    NESTED_CONDITIONAL = "nested_conditional"
    TEMPORAL_CHAIN = "temporal_chain"
    PRIORITY_BASED = "priority_based"
    RESOURCE_CONSTRAINED = "resource_constrained"
    HIERARCHICAL = "hierarchical"


@dataclass
class TaskComponent:
    """任务组件数据类"""
    id: str
    description: str
    type: str
    dependencies: List[str]
    constraints: List[str]
    priority: int
    estimated_duration: Optional[float] = None
    required_resources: List[str] = None
    
    def __post_init__(self):
        if self.required_resources is None:
            self.required_resources = []


@dataclass
class TaskStructure:
    """任务结构数据类"""
    id: str
    type: TaskStructureType
    description: str
    components: List[TaskComponent]
    temporal_relations: Dict[str, str]
    logical_relations: Dict[str, str]
    global_constraints: List[str]
    metadata: Dict


class CompoundTaskProcessor:
    """
    复合任务处理器
    支持复杂任务结构的分析和处理
    """
    
    def __init__(self):
        """
        初始化复合任务处理器
        """
        self._init_structure_patterns()
        self._init_decomposition_strategies()
        self._init_constraint_handlers()
        self._init_optimization_rules()
    
    def _init_structure_patterns(self):
        """
        初始化结构模式
        """
        self.structure_patterns = {
            # 层次结构模式
            "hierarchical": {
                "patterns": [
                    r"(main|primary|root).*?(sub|secondary|child).*?(sub|secondary|child)",
                    r"(主要|根|主).*?(子|次|从).*?(子|次|从)",
                    r"(level\s*\d+).*?(level\s*\d+).*?(level\s*\d+)"
                ],
                "description": "层次化任务结构"
            },
            
            # 优先级结构模式
            "priority_based": {
                "patterns": [
                    r"(urgent|critical|high|medium|low).*?(urgent|critical|high|medium|low)",
                    r"(紧急|重要|高|中|低).*?(紧急|重要|高|中|低)",
                    r"(priority\s*\d+).*?(priority\s*\d+)"
                ],
                "description": "基于优先级的任务结构"
            },
            
            # 资源约束结构模式
            "resource_constrained": {
                "patterns": [
                    r"(using|with|require).*?(resource|tool|equipment)",
                    r"(使用|需要|依赖).*?(资源|工具|设备)",
                    r"(resource|tool|equipment).*?(constraint|limit|restriction)"
                ],
                "description": "资源约束的任务结构"
            },
            
            # 时间链结构模式
            "temporal_chain": {
                "patterns": [
                    r"(before|after|during|while).*?(before|after|during|while)",
                    r"(在.*?之前|在.*?之后|在.*?期间|当.*?时).*?(在.*?之前|在.*?之后|在.*?期间|当.*?时)",
                    r"(step\s*\d+).*?(step\s*\d+).*?(step\s*\d+)"
                ],
                "description": "时间链式任务结构"
            },
            
            # 条件嵌套模式
            "nested_conditional": {
                "patterns": [
                    r"if.*?and.*?then.*?else",
                    r"如果.*?并且.*?那么.*?否则",
                    r"when.*?and.*?then.*?otherwise"
                ],
                "description": "嵌套条件任务结构"
            }
        }
    
    def _init_decomposition_strategies(self):
        """
        初始化分解策略
        """
        self.decomposition_strategies = {
            TaskStructureType.HIERARCHICAL: self._decompose_hierarchical,
            TaskStructureType.PRIORITY_BASED: self._decompose_priority_based,
            TaskStructureType.RESOURCE_CONSTRAINED: self._decompose_resource_constrained,
            TaskStructureType.TEMPORAL_CHAIN: self._decompose_temporal_chain,
            TaskStructureType.NESTED_CONDITIONAL: self._decompose_nested_conditional,
            TaskStructureType.SEQUENTIAL: self._decompose_sequential,
            TaskStructureType.PARALLEL: self._decompose_parallel,
            TaskStructureType.CONDITIONAL: self._decompose_conditional,
            TaskStructureType.ITERATIVE: self._decompose_iterative,
            TaskStructureType.SIMPLE: self._decompose_simple
        }
    
    def _init_constraint_handlers(self):
        """
        初始化约束处理器
        """
        self.constraint_handlers = {
            "temporal": self._handle_temporal_constraint,
            "resource": self._handle_resource_constraint,
            "precedence": self._handle_precedence_constraint,
            "mutual_exclusion": self._handle_mutual_exclusion_constraint,
            "cardinality": self._handle_cardinality_constraint
        }
    
    def _init_optimization_rules(self):
        """
        初始化优化规则
        """
        self.optimization_rules = {
            "merge_parallel": self._merge_parallel_tasks,
            "split_complex": self._split_complex_tasks,
            "reorder_dependencies": self._reorder_dependencies,
            "eliminate_redundant": self._eliminate_redundant_tasks,
            "balance_load": self._balance_task_load
        }
    
    def analyze_task_structure(self, text: str) -> TaskStructure:
        """
        分析任务结构
        
        Args:
            text: 任务描述文本
            
        Returns:
            TaskStructure: 分析结果
        """
        # 识别结构类型
        structure_type = self._identify_structure_type(text)
        
        # 提取组件
        components = self._extract_task_components(text, structure_type)
        
        # 分析时间关系
        temporal_relations = self._analyze_temporal_relations(text, components)
        
        # 分析逻辑关系
        logical_relations = self._analyze_logical_relations(text, components)
        
        # 提取全局约束
        global_constraints = self._extract_global_constraints(text)
        
        # 生成元数据
        metadata = self._generate_metadata(text, structure_type, components)
        
        return TaskStructure(
            id=f"task_{hash(text) % 10000}",
            type=structure_type,
            description=text,
            components=components,
            temporal_relations=temporal_relations,
            logical_relations=logical_relations,
            global_constraints=global_constraints,
            metadata=metadata
        )
    
    def _identify_structure_type(self, text: str) -> TaskStructureType:
        """
        识别任务结构类型
        """
        for structure_type, pattern_info in self.structure_patterns.items():
            for pattern in pattern_info["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    return TaskStructureType(structure_type)
        
        # 默认检查基本模式
        if re.search(r'\b(if|when|then|else|如果|当|那么|否则)\b', text, re.IGNORECASE):
            return TaskStructureType.CONDITIONAL
        elif re.search(r'\b(and|also|simultaneously|并且|同时|也)\b', text, re.IGNORECASE):
            return TaskStructureType.PARALLEL
        elif re.search(r'\b(first|then|next|finally|先|然后|最后)\b', text, re.IGNORECASE):
            return TaskStructureType.SEQUENTIAL
        elif re.search(r'\b(repeat|until|while|重复|直到|当)\b', text, re.IGNORECASE):
            return TaskStructureType.ITERATIVE
        else:
            return TaskStructureType.SIMPLE
    
    def _extract_task_components(self, text: str, structure_type: TaskStructureType) -> List[TaskComponent]:
        """
        提取任务组件
        """
        components = []
        
        # 根据结构类型使用不同的提取策略
        if structure_type == TaskStructureType.HIERARCHICAL:
            components = self._extract_hierarchical_components(text)
        elif structure_type == TaskStructureType.PRIORITY_BASED:
            components = self._extract_priority_components(text)
        elif structure_type == TaskStructureType.RESOURCE_CONSTRAINED:
            components = self._extract_resource_components(text)
        elif structure_type == TaskStructureType.TEMPORAL_CHAIN:
            components = self._extract_temporal_components(text)
        elif structure_type == TaskStructureType.NESTED_CONDITIONAL:
            components = self._extract_nested_conditional_components(text)
        else:
            components = self._extract_basic_components(text)
        
        return components
    
    def _extract_hierarchical_components(self, text: str) -> List[TaskComponent]:
        """
        提取层次化组件
        """
        components = []
        
        # 识别层次关键词
        level_patterns = [
            r"(main|primary|root)\s+(task|goal|objective):\s*(.+)",
            r"(主要|根|主)\s*(任务|目标):\s*(.+)",
            r"(sub|secondary|child)\s+(task|goal|objective):\s*(.+)",
            r"(子|次|从)\s*(任务|目标):\s*(.+)"
        ]
        
        for i, pattern in enumerate(level_patterns):
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                component_id = f"comp_{len(components) + 1}"
                description = match.group(3).strip()
                component_type = "main" if i < 2 else "sub"
                priority = 1 if i < 2 else 2
                
                component = TaskComponent(
                    id=component_id,
                    description=description,
                    type=component_type,
                    dependencies=[],
                    constraints=[],
                    priority=priority
                )
                components.append(component)
        
        # 如果没有找到明确的层次结构，尝试自动分解
        if not components:
            components = self._auto_decompose_hierarchical(text)
        
        return components
    
    def _extract_priority_components(self, text: str) -> List[TaskComponent]:
        """
        提取优先级组件
        """
        components = []
        
        # 优先级关键词映射
        priority_keywords = {
            "urgent": 1, "critical": 1, "紧急": 1, "重要": 1,
            "high": 2, "高": 2,
            "medium": 3, "中": 3,
            "low": 4, "低": 4
        }
        
        # 分割任务描述
        task_parts = re.split(r'[,;，；]', text)
        
        for i, part in enumerate(task_parts):
            part = part.strip()
            if not part:
                continue
            
            # 确定优先级
            priority = 3  # 默认中等优先级
            for keyword, prio in priority_keywords.items():
                if keyword in part.lower():
                    priority = prio
                    break
            
            component = TaskComponent(
                id=f"comp_{i + 1}",
                description=part,
                type="priority_task",
                dependencies=[],
                constraints=[],
                priority=priority
            )
            components.append(component)
        
        return components
    
    def _extract_resource_components(self, text: str) -> List[TaskComponent]:
        """
        提取资源约束组件
        """
        components = []
        
        # 资源模式
        resource_patterns = [
            r"(.+?)\s+(using|with|require)\s+(.+)",
            r"(.+?)\s+(使用|需要|依赖)\s+(.+)"
        ]
        
        for i, pattern in enumerate(resource_patterns):
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                task_desc = match.group(1).strip()
                resource = match.group(3).strip()
                
                component = TaskComponent(
                    id=f"comp_{len(components) + 1}",
                    description=task_desc,
                    type="resource_task",
                    dependencies=[],
                    constraints=[f"require_{resource.replace(' ', '_')}"],
                    priority=3,
                    required_resources=[resource]
                )
                components.append(component)
        
        return components
    
    def _extract_temporal_components(self, text: str) -> List[TaskComponent]:
        """
        提取时间链组件
        """
        components = []
        
        # 时间连接词
        temporal_connectors = [
            (r"(.+?)\s+before\s+(.+)", "before"),
            (r"(.+?)\s+after\s+(.+)", "after"),
            (r"(.+?)\s+during\s+(.+)", "during"),
            (r"(.+?)\s+while\s+(.+)", "while"),
            (r"(.+?)\s+在.*?之前\s+(.+)", "before"),
            (r"(.+?)\s+在.*?之后\s+(.+)", "after"),
            (r"(.+?)\s+在.*?期间\s+(.+)", "during"),
            (r"(.+?)\s+当.*?时\s+(.+)", "while")
        ]
        
        for pattern, relation in temporal_connectors:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                first_task = match.group(1).strip()
                second_task = match.group(2).strip()
                
                # 创建第一个任务组件
                comp1 = TaskComponent(
                    id=f"comp_{len(components) + 1}",
                    description=first_task,
                    type="temporal_task",
                    dependencies=[],
                    constraints=[],
                    priority=3
                )
                
                # 创建第二个任务组件
                comp2 = TaskComponent(
                    id=f"comp_{len(components) + 2}",
                    description=second_task,
                    type="temporal_task",
                    dependencies=[comp1.id] if relation in ["before", "在...之前"] else [],
                    constraints=[],
                    priority=3
                )
                
                components.extend([comp1, comp2])
        
        return components
    
    def _extract_nested_conditional_components(self, text: str) -> List[TaskComponent]:
        """
        提取嵌套条件组件
        """
        components = []
        
        # 嵌套条件模式
        nested_patterns = [
            r"if\s+(.+?)\s+and\s+(.+?)\s+then\s+(.+?)\s+else\s+(.+)",
            r"如果\s+(.+?)\s+并且\s+(.+?)\s+那么\s+(.+?)\s+否则\s+(.+)",
            r"when\s+(.+?)\s+and\s+(.+?)\s+then\s+(.+?)\s+otherwise\s+(.+)"
        ]
        
        for pattern in nested_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                condition1 = match.group(1).strip()
                condition2 = match.group(2).strip()
                true_action = match.group(3).strip()
                false_action = match.group(4).strip()
                
                # 创建条件组件
                cond_comp = TaskComponent(
                    id=f"cond_{len(components) + 1}",
                    description=f"if_{condition1}_and_{condition2}",
                    type="condition",
                    dependencies=[],
                    constraints=[],
                    priority=1
                )
                
                # 创建真分支组件
                true_comp = TaskComponent(
                    id=f"true_{len(components) + 2}",
                    description=true_action,
                    type="action",
                    dependencies=[cond_comp.id],
                    constraints=[],
                    priority=2
                )
                
                # 创建假分支组件
                false_comp = TaskComponent(
                    id=f"false_{len(components) + 3}",
                    description=false_action,
                    type="action",
                    dependencies=[cond_comp.id],
                    constraints=[],
                    priority=2
                )
                
                components.extend([cond_comp, true_comp, false_comp])
        
        return components
    
    def _extract_basic_components(self, text: str) -> List[TaskComponent]:
        """
        提取基本组件
        """
        components = []
        
        # 简单分割
        parts = re.split(r'[,;，;and|和|并且|or|或|或者]', text)
        
        for i, part in enumerate(parts):
            part = part.strip()
            if part:
                component = TaskComponent(
                    id=f"comp_{i + 1}",
                    description=part,
                    type="basic",
                    dependencies=[],
                    constraints=[],
                    priority=3
                )
                components.append(component)
        
        return components
    
    def _auto_decompose_hierarchical(self, text: str) -> List[TaskComponent]:
        """
        自动层次化分解
        """
        components = []
        
        # 尝试识别主要任务和子任务
        sentences = re.split(r'[.!?。！？]', text)
        
        main_tasks = []
        sub_tasks = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 简单启发式：较长的句子可能是主要任务
            if len(sentence.split()) > 5:
                main_tasks.append(sentence)
            else:
                sub_tasks.append(sentence)
        
        # 创建主要任务组件
        for i, task in enumerate(main_tasks):
            component = TaskComponent(
                id=f"main_{i + 1}",
                description=task,
                type="main",
                dependencies=[],
                constraints=[],
                priority=1
            )
            components.append(component)
        
        # 创建子任务组件
        for i, task in enumerate(sub_tasks):
            component = TaskComponent(
                id=f"sub_{i + 1}",
                description=task,
                type="sub",
                dependencies=[f"main_1"] if main_tasks else [],
                constraints=[],
                priority=2
            )
            components.append(component)
        
        return components
    
    def _analyze_temporal_relations(self, text: str, components: List[TaskComponent]) -> Dict[str, str]:
        """
        分析时间关系
        """
        relations = {}
        
        # 时间关系关键词
        temporal_keywords = {
            "before": "precedes",
            "after": "follows", 
            "during": "overlaps",
            "while": "overlaps",
            "until": "precedes_until",
            "在...之前": "precedes",
            "在...之后": "follows",
            "在...期间": "overlaps",
            "当...时": "overlaps",
            "直到": "precedes_until"
        }
        
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components):
                if i >= j:
                    continue
                
                for keyword, relation in temporal_keywords.items():
                    pattern = f"{comp1.description}.*?{keyword}.*?{comp2.description}"
                    if re.search(pattern, text, re.IGNORECASE):
                        relations[f"{comp1.id}_{comp2.id}"] = relation
                        break
        
        return relations
    
    def _analyze_logical_relations(self, text: str, components: List[TaskComponent]) -> Dict[str, str]:
        """
        分析逻辑关系
        """
        relations = {}
        
        # 逻辑关系关键词
        logical_keywords = {
            "and": "conjunction",
            "or": "disjunction",
            "xor": "exclusive",
            "和": "conjunction",
            "并且": "conjunction",
            "或": "disjunction",
            "或者": "disjunction",
            "要么...要么": "exclusive"
        }
        
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components):
                if i >= j:
                    continue
                
                for keyword, relation in logical_keywords.items():
                    pattern = f"{comp1.description}.*?{keyword}.*?{comp2.description}"
                    if re.search(pattern, text, re.IGNORECASE):
                        relations[f"{comp1.id}_{comp2.id}"] = relation
                        break
        
        return relations
    
    def _extract_global_constraints(self, text: str) -> List[str]:
        """
        提取全局约束
        """
        constraints = []
        
        # 约束模式
        constraint_patterns = [
            r"(must|should|need to|have to)\s+(.+)",
            r"(必须|需要|应该)\s+(.+)",
            r"(not|never|do not)\s+(.+)",
            r"(不要|避免|防止)\s+(.+)",
            r"(within|before|after|by)\s+(.+)",
            r"(在.*?之内|在.*?之前|在.*?之后|在.*?之前)\s+(.+)"
        ]
        
        for pattern in constraint_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                constraint = match.group(0).strip()
                constraints.append(constraint)
        
        return constraints
    
    def _generate_metadata(self, text: str, structure_type: TaskStructureType, components: List[TaskComponent]) -> Dict:
        """
        生成元数据
        """
        return {
            "text_length": len(text),
            "component_count": len(components),
            "structure_type": structure_type.value,
            "has_dependencies": any(comp.dependencies for comp in components),
            "has_constraints": any(comp.constraints for comp in components) or len(self._extract_global_constraints(text)) > 0,
            "avg_priority": sum(comp.priority for comp in components) / len(components) if components else 0,
            "complexity_score": self._calculate_complexity_score(text, structure_type, components)
        }
    
    def _calculate_complexity_score(self, text: str, structure_type: TaskStructureType, components: List[TaskComponent]) -> float:
        """
        计算复杂度分数
        """
        score = 0.0
        
        # 基础分数
        score += len(text) * 0.01
        score += len(components) * 0.5
        
        # 结构类型分数
        structure_scores = {
            TaskStructureType.SIMPLE: 1,
            TaskStructureType.SEQUENTIAL: 2,
            TaskStructureType.PARALLEL: 2,
            TaskStructureType.CONDITIONAL: 3,
            TaskStructureType.ITERATIVE: 3,
            TaskStructureType.NESTED_CONDITIONAL: 4,
            TaskStructureType.TEMPORAL_CHAIN: 4,
            TaskStructureType.PRIORITY_BASED: 3,
            TaskStructureType.RESOURCE_CONSTRAINED: 4,
            TaskStructureType.HIERARCHICAL: 5
        }
        
        score += structure_scores.get(structure_type, 1)
        
        # 依赖关系分数
        dependency_count = sum(len(comp.dependencies) for comp in components)
        score += dependency_count * 0.3
        
        # 约束分数
        constraint_count = sum(len(comp.constraints) for comp in components)
        score += constraint_count * 0.2
        
        return score
    
    def decompose_task(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """
        分解任务
        """
        strategy = self.decomposition_strategies.get(task_structure.type)
        if strategy:
            return strategy(task_structure)
        else:
            return task_structure.components
    
    def _decompose_hierarchical(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解层次化任务"""
        components = []
        main_components = [c for c in task_structure.components if c.type == "main"]
        sub_components = [c for c in task_structure.components if c.type == "sub"]
        
        # 先添加主要组件
        components.extend(main_components)
        
        # 然后添加子组件，并建立依赖关系
        for sub_comp in sub_components:
            if main_components:
                sub_comp.dependencies = [main_components[0].id]
            components.append(sub_comp)
        
        return components
    
    def _decompose_priority_based(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解基于优先级的任务"""
        return sorted(task_structure.components, key=lambda x: x.priority)
    
    def _decompose_resource_constrained(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解资源约束任务"""
        # 按资源需求分组
        resource_groups = {}
        for comp in task_structure.components:
            for resource in comp.required_resources:
                if resource not in resource_groups:
                    resource_groups[resource] = []
                resource_groups[resource].append(comp)
        
        # 串行化同一资源的任务
        result = []
        for resource, comps in resource_groups.items():
            for comp in comps:
                if result:
                    comp.dependencies = [result[-1].id]
                result.append(comp)
        
        return result
    
    def _decompose_temporal_chain(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解时间链任务"""
        components = task_structure.components.copy()
        
        # 根据时间关系建立依赖
        for relation_key, relation_type in task_structure.temporal_relations.items():
            comp1_id, comp2_id = relation_key.split('_')
            
            if relation_type in ["precedes", "precedes_until"]:
                # comp1 必须在 comp2 之前
                for comp in components:
                    if comp.id == comp2_id and comp1_id not in comp.dependencies:
                        comp.dependencies.append(comp1_id)
        
        return components
    
    def _decompose_nested_conditional(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解嵌套条件任务"""
        return task_structure.components
    
    def _decompose_sequential(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解顺序任务"""
        components = task_structure.components.copy()
        
        # 建立链式依赖
        for i in range(1, len(components)):
            if components[i-1].id not in components[i].dependencies:
                components[i].dependencies.append(components[i-1].id)
        
        return components
    
    def _decompose_parallel(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解并行任务"""
        # 并行任务没有依赖关系
        return task_structure.components.copy()
    
    def _decompose_conditional(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解条件任务"""
        return task_structure.components.copy()
    
    def _decompose_iterative(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解迭代任务"""
        return task_structure.components.copy()
    
    def _decompose_simple(self, task_structure: TaskStructure) -> List[TaskComponent]:
        """分解简单任务"""
        return task_structure.components.copy()
    
    def optimize_task_structure(self, task_structure: TaskStructure) -> TaskStructure:
        """
        优化任务结构
        """
        optimized_components = task_structure.components.copy()
        
        # 应用优化规则
        for rule_name, rule_func in self.optimization_rules.items():
            optimized_components = rule_func(optimized_components)
        
        # 更新任务结构
        optimized_structure = TaskStructure(
            id=task_structure.id,
            type=task_structure.type,
            description=task_structure.description,
            components=optimized_components,
            temporal_relations=task_structure.temporal_relations,
            logical_relations=task_structure.logical_relations,
            global_constraints=task_structure.global_constraints,
            metadata=task_structure.metadata
        )
        
        return optimized_structure
    
    def _merge_parallel_tasks(self, components: List[TaskComponent]) -> List[TaskComponent]:
        """合并并行任务"""
        # 简单实现：查找没有依赖关系的任务
        parallel_groups = []
        current_group = []
        
        for comp in components:
            if not comp.dependencies:
                current_group.append(comp)
            else:
                if current_group:
                    parallel_groups.append(current_group)
                    current_group = []
                parallel_groups.append([comp])
        
        if current_group:
            parallel_groups.append(current_group)
        
        # 如果有多个并行任务，可以考虑合并
        result = []
        for group in parallel_groups:
            if len(group) > 1:
                # 创建合并后的任务
                merged_desc = " and ".join([comp.description for comp in group])
                merged_comp = TaskComponent(
                    id=f"merged_{group[0].id}",
                    description=merged_desc,
                    type="merged_parallel",
                    dependencies=group[0].dependencies,
                    constraints=list(set([c for comp in group for c in comp.constraints])),
                    priority=min(comp.priority for comp in group)
                )
                result.append(merged_comp)
            else:
                result.extend(group)
        
        return result
    
    def _split_complex_tasks(self, components: List[TaskComponent]) -> List[TaskComponent]:
        """拆分复杂任务"""
        result = []
        
        for comp in components:
            # 如果任务描述过长，尝试拆分
            if len(comp.description.split()) > 10:
                # 简单拆分：按连接词分割
                parts = re.split(r'\b(and|or|but|和|或|但是)\b', comp.description, flags=re.IGNORECASE)
                
                if len(parts) > 1:
                    for i, part in enumerate(parts):
                        part = part.strip()
                        if part and part not in ['and', 'or', 'but', '和', '或', '但是']:
                            new_comp = TaskComponent(
                                id=f"{comp.id}_part_{i+1}",
                                description=part,
                                type=comp.type,
                                dependencies=comp.dependencies.copy(),
                                constraints=comp.constraints.copy(),
                                priority=comp.priority
                            )
                            result.append(new_comp)
                else:
                    result.append(comp)
            else:
                result.append(comp)
        
        return result
    
    def _reorder_dependencies(self, components: List[TaskComponent]) -> List[TaskComponent]:
        """重新排序依赖关系"""
        # 简单的拓扑排序
        in_degree = {comp.id: len(comp.dependencies) for comp in components}
        queue = [comp.id for comp in components if in_degree[comp.id] == 0]
        result = []
        
        while queue:
            current_id = queue.pop(0)
            current_comp = next(comp for comp in components if comp.id == current_id)
            result.append(current_comp)
            
            # 更新依赖此任务的其他任务的入度
            for comp in components:
                if current_id in comp.dependencies:
                    in_degree[comp.id] -= 1
                    if in_degree[comp.id] == 0:
                        queue.append(comp.id)
        
        # 如果还有剩余任务（可能有循环依赖），直接添加
        remaining = [comp for comp in components if comp not in result]
        result.extend(remaining)
        
        return result
    
    def _eliminate_redundant_tasks(self, components: List[TaskComponent]) -> List[TaskComponent]:
        """消除冗余任务"""
        result = []
        seen_descriptions = set()
        
        for comp in components:
            desc_lower = comp.description.lower()
            if desc_lower not in seen_descriptions:
                seen_descriptions.add(desc_lower)
                result.append(comp)
        
        return result
    
    def _balance_task_load(self, components: List[TaskComponent]) -> List[TaskComponent]:
        """平衡任务负载"""
        # 简单实现：根据优先级和复杂度重新分配
        return sorted(components, key=lambda x: (x.priority, len(x.description)))
    
    def _handle_temporal_constraint(self, constraint: Dict[str, Any], components: List[TaskComponent]) -> List[TaskComponent]:
        """
        处理时间约束
        
        Args:
            constraint: 时间约束信息
            components: 任务组件列表
            
        Returns:
            List[TaskComponent]: 处理后的任务组件
        """
        constraint_type = constraint.get('type', 'before')
        target_task = constraint.get('target_task')
        source_task = constraint.get('source_task')
        
        if not target_task or not source_task:
            return components
        
        # 查找对应的任务组件
        target_comp = None
        source_comp = None
        
        for comp in components:
            if target_task.lower() in comp.description.lower():
                target_comp = comp
            if source_task.lower() in comp.description.lower():
                source_comp = comp
        
        if target_comp and source_comp:
            if constraint_type == 'before':
                # source_task 必须在 target_task 之前完成
                if target_comp.id not in source_comp.dependencies:
                    source_comp.dependencies.append(target_comp.id)
            elif constraint_type == 'after':
                # source_task 必须在 target_task 之后完成
                if source_comp.id not in target_comp.dependencies:
                    target_comp.dependencies.append(source_comp.id)
            elif constraint_type == 'during':
                # source_task 必须在 target_task 执行期间完成
                # 添加特殊约束标记
                source_comp.constraints.append(f"during_{target_comp.id}")
        
        return components
    
    def _handle_resource_constraint(self, constraint: Dict[str, Any], components: List[TaskComponent]) -> List[TaskComponent]:
        """
        处理资源约束
        
        Args:
            constraint: 资源约束信息
            components: 任务组件列表
            
        Returns:
            List[TaskComponent]: 处理后的任务组件
        """
        resource_type = constraint.get('resource_type')
        resource_capacity = constraint.get('capacity', 1)
        affected_tasks = constraint.get('affected_tasks', [])
        
        # 为受影响的任务添加资源约束
        for comp in components:
            for task in affected_tasks:
                if task.lower() in comp.description.lower():
                    # 添加资源约束信息
                    resource_constraint = f"resource_{resource_type}_{resource_capacity}"
                    if resource_constraint not in comp.constraints:
                        comp.constraints.append(resource_constraint)
        
        return components
    
    def _handle_precedence_constraint(self, constraint: Dict[str, Any], components: List[TaskComponent]) -> List[TaskComponent]:
        """
        处理优先级约束
        
        Args:
            constraint: 优先级约束信息
            components: 任务组件列表
            
        Returns:
            List[TaskComponent]: 处理后的任务组件
        """
        precedence_type = constraint.get('type', 'before')
        high_priority_task = constraint.get('high_priority_task')
        low_priority_task = constraint.get('low_priority_task')
        
        if not high_priority_task or not low_priority_task:
            return components
        
        # 查找对应的任务组件
        high_comp = None
        low_comp = None
        
        for comp in components:
            if high_priority_task.lower() in comp.description.lower():
                high_comp = comp
            if low_priority_task.lower() in comp.description.lower():
                low_comp = comp
        
        if high_comp and low_comp:
            if precedence_type == 'before':
                # 高优先级任务必须在低优先级任务之前
                if low_comp.id not in high_comp.dependencies:
                    high_comp.dependencies.append(low_comp.id)
                # 调整优先级数值
                if high_comp.priority >= low_comp.priority:
                    high_comp.priority = low_comp.priority - 1
        
        return components
    
    def _handle_mutual_exclusion_constraint(self, constraint: Dict[str, Any], components: List[TaskComponent]) -> List[TaskComponent]:
        """
        处理互斥约束
        
        Args:
            constraint: 互斥约束信息
            components: 任务组件列表
            
        Returns:
            List[TaskComponent]: 处理后的任务组件
        """
        excluded_tasks = constraint.get('excluded_tasks', [])
        
        # 为互斥任务添加互斥约束
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components):
                if i >= j:  # 避免重复处理
                    continue
                
                # 检查两个任务是否互斥
                for task_pair in excluded_tasks:
                    if len(task_pair) == 2:
                        task1, task2 = task_pair
                        if ((task1.lower() in comp1.description.lower() and task2.lower() in comp2.description.lower()) or
                            (task2.lower() in comp1.description.lower() and task1.lower() in comp2.description.lower())):
                            
                            # 添加互斥约束
                            mutex_constraint = f"mutex_{comp2.id}"
                            if mutex_constraint not in comp1.constraints:
                                comp1.constraints.append(mutex_constraint)
                            
                            mutex_constraint = f"mutex_{comp1.id}"
                            if mutex_constraint not in comp2.constraints:
                                comp2.constraints.append(mutex_constraint)
        
        return components
    
    def _handle_cardinality_constraint(self, constraint: Dict[str, Any], components: List[TaskComponent]) -> List[TaskComponent]:
        """
        处理基数约束
        
        Args:
            constraint: 基数约束信息
            components: 任务组件列表
            
        Returns:
            List[TaskComponent]: 处理后的任务组件
        """
        cardinality_type = constraint.get('type', 'at_most')
        target_count = constraint.get('count', 1)
        task_category = constraint.get('task_category')
        
        if not task_category:
            return components
        
        # 统计指定类别的任务数量
        category_tasks = []
        for comp in components:
            if task_category.lower() in comp.description.lower():
                category_tasks.append(comp)
        
        # 根据约束类型处理
        if cardinality_type == 'at_most' and len(category_tasks) > target_count:
            # 移除多余的任务（保留优先级最高的）
            category_tasks.sort(key=lambda x: x.priority)
            for task in category_tasks[target_count:]:
                components.remove(task)
        
        elif cardinality_type == 'at_least' and len(category_tasks) < target_count:
            # 添加基数约束标记，由上层处理
            for comp in category_tasks:
                cardinality_constraint = f"cardinality_{cardinality_type}_{target_count}"
                if cardinality_constraint not in comp.constraints:
                    comp.constraints.append(cardinality_constraint)
        
        elif cardinality_type == 'exactly':
            if len(category_tasks) > target_count:
                # 移除多余的任务
                category_tasks.sort(key=lambda x: x.priority)
                for task in category_tasks[target_count:]:
                    components.remove(task)
            elif len(category_tasks) < target_count:
                # 添加约束标记
                for comp in category_tasks:
                    cardinality_constraint = f"cardinality_{cardinality_type}_{target_count}"
                    if cardinality_constraint not in comp.constraints:
                        comp.constraints.append(cardinality_constraint)
        
        return components
    
    def generate_ltl_from_structure(self, task_structure: TaskStructure) -> str:
        """
        从任务结构生成LTL公式
        """
        components = self.decompose_task(task_structure)
        
        if not components:
            return "true"
        
        # 根据结构类型生成不同的LTL公式
        if task_structure.type == TaskStructureType.SEQUENTIAL:
            return self._generate_sequential_ltl(components)
        elif task_structure.type == TaskStructureType.PARALLEL:
            return self._generate_parallel_ltl(components)
        elif task_structure.type == TaskStructureType.CONDITIONAL:
            return self._generate_conditional_ltl(components)
        elif task_structure.type == TaskStructureType.ITERATIVE:
            return self._generate_iterative_ltl(components)
        else:
            return self._generate_simple_ltl(components)
    
    def _generate_sequential_ltl(self, components: List[TaskComponent]) -> str:
        """生成顺序LTL公式"""
        if len(components) == 1:
            return f"F({components[0].description.replace(' ', '_')})"
        
        formula = components[0].description.replace(' ', '_')
        for comp in components[1:]:
            formula = f"({formula} -> F({comp.description.replace(' ', '_')}))"
        
        return formula
    
    def _generate_parallel_ltl(self, components: List[TaskComponent]) -> str:
        """生成并行LTL公式"""
        props = [f"F({comp.description.replace(' ', '_')})" for comp in components]
        return " & ".join(props)
    
    def _generate_conditional_ltl(self, components: List[TaskComponent]) -> str:
        """生成条件LTL公式"""
        if len(components) >= 2:
            condition = components[0].description.replace(' ', '_')
            action = components[1].description.replace(' ', '_')
            return f"({condition} -> F({action}))"
        else:
            return self._generate_simple_ltl(components)
    
    def _generate_iterative_ltl(self, components: List[TaskComponent]) -> str:
        """生成迭代LTL公式"""
        if components:
            task = components[0].description.replace(' ', '_')
            return f"G(!done -> (F({task}) -> X(!done)))"
        else:
            return "true"
    
    def _generate_simple_ltl(self, components: List[TaskComponent]) -> str:
        """生成简单LTL公式"""
        if components:
            return f"F({components[0].description.replace(' ', '_')})"
        else:
            return "true"


def main():
    """
    主函数，用于测试复合任务处理器
    """
    processor = CompoundTaskProcessor()
    
    # 测试用例
    test_cases = [
        "Main task: Clean the house. Sub tasks: Clean the kitchen, Clean the bathroom",
        "Urgent: Fix the leak. High: Repair the roof. Low: Paint the walls",
        "Use the vacuum cleaner to clean the carpet. Use the mop to clean the floor",
        "Turn on the lights before opening the door. Close the door after entering",
        "If it's raining and I have an umbrella, then go outside, otherwise stay inside",
        "First prepare breakfast, then eat breakfast, finally wash dishes"
    ]
    
    print("=== 复合任务处理器测试 ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case}")
        print("-" * 60)
        
        try:
            # 分析任务结构
            task_structure = processor.analyze_task_structure(test_case)
            
            print(f"结构类型: {task_structure.type.value}")
            print(f"组件数量: {len(task_structure.components)}")
            print(f"复杂度分数: {task_structure.metadata['complexity_score']:.2f}")
            
            # 分解任务
            decomposed = processor.decompose_task(task_structure)
            print(f"\n分解后的任务:")
            for j, comp in enumerate(decomposed, 1):
                print(f"  {j}. {comp.description} (优先级: {comp.priority})")
                if comp.dependencies:
                    print(f"     依赖: {comp.dependencies}")
                if comp.constraints:
                    print(f"     约束: {comp.constraints}")
            
            # 生成LTL公式
            ltl_formula = processor.generate_ltl_from_structure(task_structure)
            print(f"\n生成的LTL公式: {ltl_formula}")
            
            # 优化任务结构
            optimized = processor.optimize_task_structure(task_structure)
            print(f"\n优化后组件数量: {len(optimized.components)}")
            
        except Exception as e:
            print(f"处理失败: {e}")
        
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()