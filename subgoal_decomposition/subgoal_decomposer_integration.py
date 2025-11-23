"""
子目标分解模块集成接口

提供与其他模块（目标解释、转换建模、动作序列）的集成功能
实现错误处理和反向反馈机制
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
import json
import uuid
import hashlib
import time
from enum import Enum

from subgoal_decomposition.subgoal_decomposer import SubgoalDecomposer, DecompositionResult, SubgoalType
from subgoal_decomposition.models import Subgoal, DecompositionStrategy

# 设置日志
logger = logging.getLogger(__name__)


@dataclass
class IntegratedDecompositionResult:
    """
    集成分解结果，包含与其他模块交互所需的完整信息
    """
    original_goal: str
    subgoals: List[Subgoal]
    decomposition_strategy: str
    transition_modeling_data: Dict[str, Any] = field(default_factory=dict)
    action_sequencing_data: Dict[str, Any] = field(default_factory=dict)
    validation_metadata: Dict[str, Any] = field(default_factory=dict)
    compatibility_flags: Dict[str, bool] = field(default_factory=dict)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    confidence_score: float = 0.0


class SubgoalDecomposerIntegration:
    """
    子目标分解器集成类，负责与其他模块的交互
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化子目标分解器集成组件
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        
        # 初始化子目标分解器
        decomposer_config = self.config.get('decomposer', {})
        self.decomposer = SubgoalDecomposer(decomposer_config)
        
        # 模块联动配置
        self.enable_module_feedback = self.config.get('enable_module_feedback', True)
        self.enable_error_handling = self.config.get('enable_error_handling', True)
        self.timeout_seconds = self.config.get('timeout_seconds', 30)
        
        # 反向反馈缓存
        self.feedback_cache = {}
        self.module_interfaces = {
            'goal_interpretation': {'enabled': True, 'version': '1.0'},
            'transition_modeling': {'enabled': True, 'version': '1.0'},
            'action_sequencing': {'enabled': True, 'version': '1.0'}
        }
        
        # 统计信息
        self.stats = {
            'total_decompositions': 0,
            'successful_decompositions': 0,
            'failed_decompositions': 0,
            'feedback_applied': 0,
            'error_types': {},
            'average_subgoal_count': 0.0,
            'average_confidence': 0.0
        }
        
        logger.info("Subgoal Decomposer Integration initialized")
    
    def decompose_for_integration(self, 
                                 goal_text: str, 
                                 goal_data: Dict[str, Any],
                                 module_feedback: Optional[Dict[str, Any]] = None) -> IntegratedDecompositionResult:
        """
        为模块集成分解目标
        
        Args:
            goal_text: 目标文本
            goal_data: 来自目标解释模块的数据
            module_feedback: 来自其他模块的反馈
            
        Returns:
            IntegratedDecompositionResult: 集成分解结果
        """
        self.stats['total_decompositions'] += 1
        
        try:
            # 应用反向反馈
            if self.enable_module_feedback and module_feedback:
                self._apply_module_feedback(goal_text, module_feedback)
            
            # 准备分解请求
            decomposition_request = self._prepare_integration_request(goal_text, goal_data)
            
            # 执行分解
            decomposition_response = self.decomposer.decompose(
                goal=goal_data.get('goal_variables', {}),
                constraints=goal_data.get('goal_constraints', []),
                strategy=decomposition_request['strategy'],
                goal_type=decomposition_request['goal_type']
            )
            
            # 构建集成结果
            result = self._build_integrated_result(
                goal_text, 
                decomposition_response,
                goal_data
            )
            
            # 验证与其他模块的兼容性
            compatibility_flags = self._validate_module_compatibility(result)
            result.compatibility_flags = compatibility_flags
            
            if decomposition_response.success:
                self.stats['successful_decompositions'] += 1
                self._update_subgoal_stats(len(result.subgoals))
                self._update_confidence_stats(result.confidence_score)
            else:
                self.stats['failed_decompositions'] += 1
                self._record_error_type('decomposition_failed')
            
            return result
            
        except Exception as e:
            logger.error(f"Error in subgoal decomposition for integration: {str(e)}")
            self.stats['failed_decompositions'] += 1
            self._record_error_type('exception')
            
            # 返回错误时的默认结果
            return IntegratedDecompositionResult(
                original_goal=goal_text,
                subgoals=[],
                decomposition_strategy='unknown',
                confidence_score=0.0,
                compatibility_flags={'error_occurred': True},
                validation_metadata={'error_message': str(e)}
            )
    
    def _prepare_integration_request(self, goal_text: str, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备集成请求
        
        Args:
            goal_text: 目标文本
            goal_data: 目标数据
            
        Returns:
            Dict[str, Any]: 分解请求数据
        """
        # 获取目标变量和约束
        goal_variables = goal_data.get('goal_variables', {})
        goal_constraints = goal_data.get('goal_constraints', [])
        goal_type = goal_data.get('goal_type', 'UNKNOWN')
        
        # 确定分解策略
        strategy = goal_data.get('decomposition_strategy', 'sequential')
        
        # 检查是否有缓存的反馈
        feedback_applied = False
        goal_hash = hashlib.md5((goal_text + str(goal_variables)).encode()).hexdigest()
        
        if goal_hash in self.feedback_cache:
            cached_feedback = self.feedback_cache[goal_hash]
            logger.info(f"Applying cached feedback for decomposition: {goal_text[:30]}...")
            self.stats['feedback_applied'] += 1
            feedback_applied = True
            
            # 使用反馈优化策略
            if 'strategy_improvements' in cached_feedback:
                strategy = cached_feedback['strategy_improvements'].get('preferred_strategy', strategy)
        
        # 返回分解请求数据
        return {
            'strategy': strategy,
            'goal_type': goal_type,
            'goal_variables': goal_variables,
            'goal_constraints': goal_constraints,
            'feedback_applied': feedback_applied,
            'integration_mode': True
        }
    
    def _build_integrated_result(self, 
                                goal_text: str,
                                decomposition_response: DecompositionResult,
                                goal_data: Dict[str, Any]) -> IntegratedDecompositionResult:
        """
        构建集成结果
        
        Args:
            goal_text: 原始目标文本
            decomposition_response: 分解响应
            goal_data: 目标数据
            
        Returns:
            IntegratedDecompositionResult: 集成结果
        """
        # 提取分解结果
        subgoals = decomposition_response.subgoals
        confidence_score = getattr(decomposition_response, 'confidence_score', 0.0)
        
        # 获取分解策略
        decomposition_strategy = goal_data.get('decomposition_strategy', 'sequential')
        
        # 构建依赖图
        dependency_graph = self._build_dependency_graph(subgoals)
        
        # 构建转换建模所需数据
        transition_modeling_data = self._build_transition_data(subgoals, dependency_graph)
        
        # 构建动作序列所需数据
        action_sequencing_data = self._build_action_data(subgoals, dependency_graph)
        
        # 构建验证元数据
        validation_metadata = {
            'decomposition_time': getattr(decomposition_response, 'decomposition_time', 0.0),
            'strategy_used': decomposition_strategy,
            'subgoal_types_distribution': self._count_subgoal_types(subgoals),
            'dependency_complexity': self._calculate_dependency_complexity(dependency_graph)
        }
        
        return IntegratedDecompositionResult(
            original_goal=goal_text,
            subgoals=subgoals,
            decomposition_strategy=decomposition_strategy,
            transition_modeling_data=transition_modeling_data,
            action_sequencing_data=action_sequencing_data,
            validation_metadata=validation_metadata,
            dependency_graph=dependency_graph,
            confidence_score=confidence_score
        )
    
    def _validate_module_compatibility(self, result: IntegratedDecompositionResult) -> Dict[str, bool]:
        """
        验证与其他模块的兼容性
        
        Args:
            result: 集成分解结果
            
        Returns:
            Dict[str, bool]: 兼容性标志
        """
        compatibility = {
            'transition_compatible': True,
            'action_compatible': True,
            'pddl_compatible': True,
            'dependency_valid': True
        }
        
        # 验证子目标数量
        if len(result.subgoals) == 0:
            compatibility['transition_compatible'] = False
            compatibility['action_compatible'] = False
        
        # 验证依赖图
        if self._has_cyclic_dependencies(result.dependency_graph):
            compatibility['dependency_valid'] = False
        
        # 检查每个子目标的PDDL兼容性
        for subgoal in result.subgoals:
            if not self._is_subgoal_pddl_compatible(subgoal):
                compatibility['pddl_compatible'] = False
                break
        
        return compatibility
    
    def _build_transition_data(self, subgoals: List[Subgoal], dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        构建转换建模所需数据
        
        Args:
            subgoals: 子目标列表
            dependency_graph: 依赖图
            
        Returns:
            Dict[str, Any]: 转换数据
        """
        transition_goals = []
        
        for i, subgoal in enumerate(subgoals):
            # 提取子目标的状态信息
            subgoal_state = {
                'id': f'subgoal_{i}',
                'variables': getattr(subgoal, 'variables', {}),
                'constraints': getattr(subgoal, 'constraints', []),
                'type': getattr(subgoal, 'type', SubgoalType.UNKNOWN).value if hasattr(subgoal, 'type') else 'UNKNOWN',
                'priority': getattr(subgoal, 'priority', 0),
                'estimated_duration': getattr(subgoal, 'estimated_duration', 0),
                'required_resources': getattr(subgoal, 'required_resources', [])
            }
            
            transition_goals.append(subgoal_state)
        
        return {
            'subgoal_transitions': transition_goals,
            'dependency_graph': dependency_graph,
            'subgoal_count': len(subgoals),
            'transition_sequence': self._generate_transition_sequence(subgoals, dependency_graph)
        }
    
    def _build_action_data(self, subgoals: List[Subgoal], dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        构建动作序列所需数据
        
        Args:
            subgoals: 子目标列表
            dependency_graph: 依赖图
            
        Returns:
            Dict[str, Any]: 动作数据
        """
        action_requirements = []
        
        for i, subgoal in enumerate(subgoals):
            # 为每个子目标生成动作需求
            requirements = self._generate_subgoal_action_requirements(subgoal)
            
            action_requirements.append({
                'subgoal_id': f'subgoal_{i}',
                'requirements': requirements,
                'sequencing_priority': getattr(subgoal, 'priority', 0),
                'estimated_actions': len(requirements),
                'dependencies': dependency_graph.get(f'subgoal_{i}', [])
            })
        
        return {
            'subgoal_action_requirements': action_requirements,
            'global_action_constraints': self._generate_global_action_constraints(subgoals),
            'dependency_constraints': self._convert_dependencies_to_constraints(dependency_graph)
        }
    
    def register_module_feedback(self, 
                               goal_text: str,
                               module_name: str,
                               feedback: Dict[str, Any]):
        """
        注册来自其他模块的反馈
        
        Args:
            goal_text: 目标文本
            module_name: 模块名称
            feedback: 反馈数据
        """
        if not self.enable_module_feedback or module_name not in self.module_interfaces:
            return
        
        # 创建目标哈希作为缓存键
        goal_hash = hashlib.md5(goal_text.encode()).hexdigest()
        
        # 初始化或更新反馈缓存
        if goal_hash not in self.feedback_cache:
            self.feedback_cache[goal_hash] = {
                'module_feedback': {},
                'strategy_improvements': {},
                'last_updated': time.time()
            }
        
        # 添加模块反馈
        self.feedback_cache[goal_hash]['module_feedback'][module_name] = {
            'feedback': feedback,
            'timestamp': time.time()
        }
        
        # 提取策略改进建议
        if 'strategy_suggestions' in feedback:
            self.feedback_cache[goal_hash]['strategy_improvements'].update(feedback['strategy_suggestions'])
        
        # 更新最后更新时间
        self.feedback_cache[goal_hash]['last_updated'] = time.time()
        
        logger.info(f"Registered feedback from {module_name} for subgoal decomposition: {goal_text[:30]}...")
    
    def _apply_module_feedback(self, goal_text: str, feedback: Dict[str, Any]):
        """
        应用来自其他模块的反馈
        
        Args:
            goal_text: 目标文本
            feedback: 反馈数据
        """
        module_name = feedback.get('module_name')
        if module_name:
            self.register_module_feedback(goal_text, module_name, feedback.get('data', {}))
    
    def _build_dependency_graph(self, subgoals: List[Subgoal]) -> Dict[str, List[str]]:
        """
        构建子目标依赖图
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            Dict[str, List[str]]: 依赖图，格式为 {subgoal_id: [依赖的subgoal_id列表]}
        """
        dependency_graph = {}
        
        for i, subgoal in enumerate(subgoals):
            subgoal_id = f'subgoal_{i}'
            dependencies = []
            
            # 获取子目标的依赖
            subgoal_dependencies = getattr(subgoal, 'dependencies', [])
            if isinstance(subgoal_dependencies, list):
                # 假设dependencies是索引列表
                for dep_idx in subgoal_dependencies:
                    if isinstance(dep_idx, int) and 0 <= dep_idx < len(subgoals):
                        dependencies.append(f'subgoal_{dep_idx}')
            
            dependency_graph[subgoal_id] = dependencies
        
        # 如果没有明确依赖，基于优先级创建依赖
        if all(len(deps) == 0 for deps in dependency_graph.values()):
            sorted_subgoals = sorted(
                enumerate(subgoals),
                key=lambda x: getattr(x[1], 'priority', 0),
                reverse=True
            )
            
            for i in range(1, len(sorted_subgoals)):
                current_idx = sorted_subgoals[i][0]
                prev_idx = sorted_subgoals[i-1][0]
                dependency_graph[f'subgoal_{current_idx}'].append(f'subgoal_{prev_idx}')
        
        return dependency_graph
    
    def _generate_transition_sequence(self, subgoals: List[Subgoal], dependency_graph: Dict[str, List[str]]) -> List[str]:
        """
        生成转换序列
        
        Args:
            subgoals: 子目标列表
            dependency_graph: 依赖图
            
        Returns:
            List[str]: 转换序列
        """
        # 使用拓扑排序生成序列
        visited = set()
        sequence = []
        
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in dependency_graph.get(node, []):
                dfs(neighbor)
            sequence.append(node)
        
        # 对所有节点执行DFS
        for node in dependency_graph.keys():
            dfs(node)
        
        # 反转得到正确的拓扑顺序
        sequence.reverse()
        
        return sequence
    
    def _generate_subgoal_action_requirements(self, subgoal: Subgoal) -> List[str]:
        """
        为子目标生成动作需求
        
        Args:
            subgoal: 子目标
            
        Returns:
            List[str]: 动作需求列表
        """
        requirements = []
        
        # 根据子目标类型生成需求
        subgoal_type = getattr(subgoal, 'type', SubgoalType.UNKNOWN)
        
        if subgoal_type == SubgoalType.NAVIGATION:
            requirements.extend(['move_to_action', 'navigate_action'])
        elif subgoal_type == SubgoalType.MANIPULATION:
            requirements.extend(['grasp_action', 'move_action', 'place_action'])
        elif subgoal_type == SubgoalType.OBSERVATION:
            requirements.extend(['detect_action', 'classify_action'])
        else:
            # 默认需求
            requirements.extend(['generic_action'])
        
        # 根据子目标变量添加额外需求
        variables = getattr(subgoal, 'variables', {})
        for key in variables.keys():
            if 'position' in key.lower():
                requirements.append('position_update_action')
            elif 'gripper' in key.lower():
                requirements.append('gripper_control_action')
        
        return requirements
    
    def _generate_global_action_constraints(self, subgoals: List[Subgoal]) -> List[Dict[str, Any]]:
        """
        生成全局动作约束
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[Dict[str, Any]]: 约束列表
        """
        constraints = []
        
        # 检查是否有导航子目标
        has_navigation = any(
            getattr(sg, 'type', SubgoalType.UNKNOWN) == SubgoalType.NAVIGATION
            for sg in subgoals
        )
        
        # 检查是否有操作子目标
        has_manipulation = any(
            getattr(sg, 'type', SubgoalType.UNKNOWN) == SubgoalType.MANIPULATION
            for sg in subgoals
        )
        
        if has_navigation and has_manipulation:
            # 添加导航优先约束
            constraints.append({
                'type': 'priority_constraint',
                'action_category1': 'navigation',
                'action_category2': 'manipulation',
                'relation': 'before'
            })
        
        return constraints
    
    def _convert_dependencies_to_constraints(self, dependency_graph: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """
        将依赖图转换为约束
        
        Args:
            dependency_graph: 依赖图
            
        Returns:
            List[Dict[str, Any]]: 约束列表
        """
        constraints = []
        
        for node, dependencies in dependency_graph.items():
            for dep in dependencies:
                constraints.append({
                    'type': 'dependency_constraint',
                    'predecessor': dep,
                    'successor': node,
                    'relation': 'must_complete_before'
                })
        
        return constraints
    
    def _count_subgoal_types(self, subgoals: List[Subgoal]) -> Dict[str, int]:
        """
        统计子目标类型分布
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            Dict[str, int]: 类型统计
        """
        type_count = {}
        
        for subgoal in subgoals:
            sg_type = getattr(subgoal, 'type', SubgoalType.UNKNOWN)
            type_str = sg_type.value if hasattr(sg_type, 'value') else str(sg_type)
            type_count[type_str] = type_count.get(type_str, 0) + 1
        
        return type_count
    
    def _calculate_dependency_complexity(self, dependency_graph: Dict[str, List[str]]) -> float:
        """
        计算依赖复杂度
        
        Args:
            dependency_graph: 依赖图
            
        Returns:
            float: 复杂度分数
        """
        if not dependency_graph:
            return 0.0
        
        total_dependencies = sum(len(deps) for deps in dependency_graph.values())
        node_count = len(dependency_graph)
        
        if node_count == 0:
            return 0.0
        
        # 平均每个节点的依赖数
        avg_dependencies = total_dependencies / node_count
        
        return avg_dependencies
    
    def _has_cyclic_dependencies(self, dependency_graph: Dict[str, List[str]]) -> bool:
        """
        检查是否存在循环依赖
        
        Args:
            dependency_graph: 依赖图
            
        Returns:
            bool: 是否存在循环依赖
        """
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in dependency_graph.get(node, []):
                if has_cycle(neighbor):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in dependency_graph.keys():
            if has_cycle(node):
                return True
        
        return False
    
    def _is_subgoal_pddl_compatible(self, subgoal: Subgoal) -> bool:
        """
        检查子目标是否兼容PDDL
        
        Args:
            subgoal: 子目标
            
        Returns:
            bool: 是否兼容
        """
        # 检查变量是否存在
        variables = getattr(subgoal, 'variables', {})
        if not variables:
            return False
        
        # 检查变量值是否可序列化
        try:
            for value in variables.values():
                json.dumps(value)
            return True
        except:
            return False
    
    def _update_subgoal_stats(self, subgoal_count: int):
        """
        更新子目标统计
        
        Args:
            subgoal_count: 子目标数量
        """
        total = self.stats['total_decompositions']
        current_avg = self.stats['average_subgoal_count']
        self.stats['average_subgoal_count'] = (
            (current_avg * (total - 1)) + subgoal_count
        ) / total
    
    def _update_confidence_stats(self, confidence: float):
        """
        更新置信度统计
        
        Args:
            confidence: 置信度分数
        """
        total = self.stats['total_decompositions']
        current_avg = self.stats['average_confidence']
        self.stats['average_confidence'] = (
            (current_avg * (total - 1)) + confidence
        ) / total
    
    def _record_error_type(self, error_type: str):
        """
        记录错误类型
        
        Args:
            error_type: 错误类型
        """
        if error_type not in self.stats['error_types']:
            self.stats['error_types'][error_type] = 0
        self.stats['error_types'][error_type] += 1
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """
        获取集成统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        return {
            'total_decompositions': self.stats['total_decompositions'],
            'success_rate': self.stats['successful_decompositions'] / max(self.stats['total_decompositions'], 1),
            'average_subgoal_count': self.stats['average_subgoal_count'],
            'average_confidence': self.stats['average_confidence'],
            'feedback_applied': self.stats['feedback_applied'],
            'error_distribution': self.stats['error_types'],
            'module_interfaces': {k: v['enabled'] for k, v in self.module_interfaces.items()}
        }
    
    def create_error_diagnosis(self, result: IntegratedDecompositionResult) -> Dict[str, Any]:
        """
        创建错误诊断
        
        Args:
            result: 集成分解结果
            
        Returns:
            Dict[str, Any]: 诊断信息
        """
        diagnosis = {
            'possible_causes': [],
            'recommendations': [],
            'module_specific_issues': {}
        }
        
        # 检查兼容性标志
        if not result.compatibility_flags.get('transition_compatible'):
            diagnosis['possible_causes'].append('No valid subgoals generated for transition modeling')
            diagnosis['recommendations'].append('Adjust decomposition strategy or provide more specific goals')
            diagnosis['module_specific_issues']['transition_modeling'] = 'No valid subgoals'
        
        if not result.compatibility_flags.get('dependency_valid'):
            diagnosis['possible_causes'].append('Cyclic dependencies detected in subgoals')
            diagnosis['recommendations'].append('Review subgoal dependencies and remove cycles')
            diagnosis['module_specific_issues']['dependency'] = 'Cyclic dependencies'
        
        if not result.compatibility_flags.get('pddl_compatible'):
            diagnosis['possible_causes'].append('Subgoals contain non-PDDL compatible elements')
            diagnosis['recommendations'].append('Simplify subgoal variables to basic data types')
            diagnosis['module_specific_issues']['pddl'] = 'Incompatible structure'
        
        if len(result.subgoals) > 10:
            diagnosis['possible_causes'].append('Too many subgoals may cause planning inefficiency')
            diagnosis['recommendations'].append('Merge similar subgoals or use hierarchical decomposition')
        
        if result.confidence_score < 0.5:
            diagnosis['possible_causes'].append('Low confidence in subgoal decomposition')
            diagnosis['recommendations'].append('Adjust decomposition strategy or provide more context')
        
        return diagnosis