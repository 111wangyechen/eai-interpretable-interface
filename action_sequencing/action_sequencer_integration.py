"""
动作序列模块集成接口

提供与其他模块（目标解释、子目标分解、转换建模）的集成功能
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

from action_sequencing.action_sequencer import ActionSequencer, SequencingRequest, SequencingResponse
from action_sequencing.models import ActionType, SequencingConfig

# 设置日志
logger = logging.getLogger(__name__)


@dataclass
class IntegratedActionSequenceResult:
    """
    集成动作序列结果，包含与其他模块交互所需的完整信息
    """
    original_goal: str
    action_sequence: List[Dict[str, Any]]
    sequence_metadata: Dict[str, Any] = field(default_factory=dict)
    validation_metadata: Dict[str, Any] = field(default_factory=dict)
    compatibility_flags: Dict[str, bool] = field(default_factory=dict)
    execution_estimates: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0


class ActionSequencerIntegration:
    """
    动作序列器集成类，负责与其他模块的交互
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化动作序列器集成组件
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        
        # 初始化动作序列器
        sequencer_config = SequencingConfig(**self.config.get('sequencer', {}))
        self.sequencer = ActionSequencer(sequencer_config)
        
        # 模块联动配置
        self.enable_module_feedback = self.config.get('enable_module_feedback', True)
        self.enable_error_handling = self.config.get('enable_error_handling', True)
        self.timeout_seconds = self.config.get('timeout_seconds', 30)
        
        # 反向反馈缓存
        self.feedback_cache = {}
        self.module_interfaces = {
            'goal_interpretation': {'enabled': True, 'version': '1.0'},
            'subgoal_decomposition': {'enabled': True, 'version': '1.0'},
            'transition_modeling': {'enabled': True, 'version': '1.0'}
        }
        
        # 统计信息
        self.stats = {
            'total_sequences': 0,
            'successful_sequences': 0,
            'failed_sequences': 0,
            'feedback_applied': 0,
            'error_types': {},
            'average_action_count': 0.0,
            'average_confidence': 0.0
        }
        
        logger.info("Action Sequencer Integration initialized")
    
    def sequence_actions_for_integration(self, 
                                        goal_text: str, 
                                        subgoal_data: Dict[str, Any],
                                        transition_data: Optional[Dict[str, Any]] = None,
                                        module_feedback: Optional[Dict[str, Any]] = None) -> IntegratedActionSequenceResult:
        """
        为模块集成生成动作序列
        
        Args:
            goal_text: 目标文本
            subgoal_data: 来自子目标分解模块的数据
            transition_data: 来自转换建模模块的数据
            module_feedback: 来自其他模块的反馈
            
        Returns:
            IntegratedActionSequenceResult: 集成动作序列结果
        """
        self.stats['total_sequences'] += 1
        
        try:
            # 应用反向反馈
            if self.enable_module_feedback and module_feedback:
                self._apply_module_feedback(goal_text, module_feedback)
            
            # 准备序列请求
            sequencing_request = self._prepare_integration_request(
                goal_text, 
                subgoal_data,
                transition_data
            )
            
            # 执行序列生成
            sequencing_response = self.sequencer.generate_sequence(sequencing_request)
            
            # 构建集成结果
            result = self._build_integrated_result(
                goal_text, 
                sequencing_response,
                subgoal_data,
                transition_data
            )
            
            # 验证与执行引擎的兼容性
            compatibility_flags = self._validate_execution_compatibility(result)
            result.compatibility_flags = compatibility_flags
            
            if sequencing_response.success:
                self.stats['successful_sequences'] += 1
                self._update_action_stats(len(result.action_sequence))
                self._update_confidence_stats(result.confidence_score)
            else:
                self.stats['failed_sequences'] += 1
                self._record_error_type('sequencing_failed')
            
            return result
            
        except Exception as e:
            logger.error(f"Error in action sequencing for integration: {str(e)}")
            self.stats['failed_sequences'] += 1
            self._record_error_type('exception')
            
            # 返回错误时的默认结果
            return IntegratedActionSequenceResult(
                original_goal=goal_text,
                action_sequence=[],
                confidence_score=0.0,
                compatibility_flags={'error_occurred': True},
                validation_metadata={'error_message': str(e)}
            )
    
    def _prepare_integration_request(self, 
                                    goal_text: str, 
                                    subgoal_data: Dict[str, Any],
                                    transition_data: Optional[Dict[str, Any]]) -> SequencingRequest:
        """
        准备集成请求
        
        Args:
            goal_text: 目标文本
            subgoal_data: 子目标数据
            transition_data: 转换数据
            
        Returns:
            SequencingRequest: 序列请求
        """
        # 从子目标数据中提取动作需求
        action_requirements = subgoal_data.get('subgoal_action_requirements', [])
        global_constraints = subgoal_data.get('global_action_constraints', [])
        dependency_constraints = subgoal_data.get('dependency_constraints', [])
        
        # 从转换数据中提取信息（如果有）
        transition_sequence = []
        if transition_data:
            transition_sequence = transition_data.get('transition_sequence', [])
        
        # 检查是否有缓存的反馈
        feedback_applied = False
        goal_hash = hashlib.md5((goal_text + str(action_requirements)).encode()).hexdigest()
        
        if goal_hash in self.feedback_cache:
            cached_feedback = self.feedback_cache[goal_hash]
            logger.info(f"Applying cached feedback for sequencing: {goal_text[:30]}...")
            self.stats['feedback_applied'] += 1
            feedback_applied = True
        
        # 创建序列请求
        request = SequencingRequest(
            goal_text=goal_text,
            action_requirements=action_requirements,
            constraints=global_constraints + dependency_constraints,
            transition_sequence=transition_sequence,
            request_id=f"action_seq_{uuid.uuid4()}",
            metadata={
                'feedback_applied': feedback_applied,
                'integration_mode': True,
                'subgoal_count': len(action_requirements)
            }
        )
        
        return request
    
    def _build_integrated_result(self, 
                                goal_text: str,
                                sequencing_response: SequencingResponse,
                                subgoal_data: Dict[str, Any],
                                transition_data: Optional[Dict[str, Any]]) -> IntegratedActionSequenceResult:
        """
        构建集成结果
        
        Args:
            goal_text: 原始目标文本
            sequencing_response: 序列响应
            subgoal_data: 子目标数据
            transition_data: 转换数据
            
        Returns:
            IntegratedActionSequenceResult: 集成结果
        """
        # 提取序列结果
        action_sequence = getattr(sequencing_response, 'action_sequence', [])
        confidence_score = getattr(sequencing_response, 'confidence_score', 0.0)
        
        # 转换动作序列格式
        formatted_sequence = self._format_action_sequence(action_sequence)
        
        # 构建序列元数据
        sequence_metadata = {
            'sequence_length': len(formatted_sequence),
            'action_types_distribution': self._count_action_types(formatted_sequence),
            'execution_estimated': False
        }
        
        # 构建执行估计
        execution_estimates = self._estimate_execution_parameters(formatted_sequence)
        sequence_metadata['execution_estimated'] = True
        
        # 构建验证元数据
        validation_metadata = {
            'sequencing_time': getattr(sequencing_response, 'sequencing_time', 0.0),
            'constraint_satisfaction_rate': getattr(sequencing_response, 'constraint_satisfaction_rate', 1.0),
            'sequence_validity_score': getattr(sequencing_response, 'validity_score', 0.0),
            'resource_utilization_estimate': self._estimate_resource_utilization(formatted_sequence)
        }
        
        return IntegratedActionSequenceResult(
            original_goal=goal_text,
            action_sequence=formatted_sequence,
            sequence_metadata=sequence_metadata,
            validation_metadata=validation_metadata,
            execution_estimates=execution_estimates,
            confidence_score=confidence_score
        )
    
    def _validate_execution_compatibility(self, result: IntegratedActionSequenceResult) -> Dict[str, bool]:
        """
        验证与执行引擎的兼容性
        
        Args:
            result: 集成动作序列结果
            
        Returns:
            Dict[str, bool]: 兼容性标志
        """
        compatibility = {
            'execution_compatible': True,
            'pddl_compatible': True,
            'resource_compatible': True,
            'time_compatible': True
        }
        
        # 验证动作序列是否为空
        if len(result.action_sequence) == 0:
            compatibility['execution_compatible'] = False
            compatibility['pddl_compatible'] = False
        
        # 验证每个动作的PDDL兼容性
        for action in result.action_sequence:
            if not self._is_action_pddl_compatible(action):
                compatibility['pddl_compatible'] = False
                break
        
        # 验证资源兼容性
        estimated_resources = result.execution_estimates.get('total_resource_requirement', 0)
        if estimated_resources > 100:  # 假设100是资源阈值
            compatibility['resource_compatible'] = False
        
        # 验证时间兼容性
        estimated_time = result.execution_estimates.get('total_estimated_time', 0)
        if estimated_time > 300:  # 假设300秒是时间阈值
            compatibility['time_compatible'] = False
        
        return compatibility
    
    def _format_action_sequence(self, action_sequence: List[Any]) -> List[Dict[str, Any]]:
        """
        格式化动作序列
        
        Args:
            action_sequence: 原始动作序列
            
        Returns:
            List[Dict[str, Any]]: 格式化后的动作序列
        """
        formatted = []
        
        for i, action in enumerate(action_sequence):
            # 确保动作是字典格式
            if isinstance(action, dict):
                action_dict = action.copy()
            else:
                # 尝试从对象中提取属性
                action_dict = {}
                try:
                    action_dict['type'] = getattr(action, 'type', 'unknown')
                    action_dict['parameters'] = getattr(action, 'parameters', {})
                    action_dict['preconditions'] = getattr(action, 'preconditions', [])
                    action_dict['effects'] = getattr(action, 'effects', [])
                    action_dict['estimated_duration'] = getattr(action, 'estimated_duration', 0)
                    action_dict['required_resources'] = getattr(action, 'required_resources', [])
                except:
                    action_dict = {'type': 'unknown', 'parameters': {}}
            
            # 确保有必要的字段
            action_dict.setdefault('type', 'unknown')
            action_dict.setdefault('parameters', {})
            action_dict.setdefault('preconditions', [])
            action_dict.setdefault('effects', [])
            action_dict.setdefault('id', f'action_{i}')
            
            # 添加执行信息
            action_dict['sequence_index'] = i
            
            formatted.append(action_dict)
        
        return formatted
    
    def _count_action_types(self, action_sequence: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        统计动作类型分布
        
        Args:
            action_sequence: 动作序列
            
        Returns:
            Dict[str, int]: 类型统计
        """
        type_count = {}
        
        for action in action_sequence:
            action_type = action.get('type', 'unknown')
            # 如果类型是枚举，获取其值
            if hasattr(action_type, 'value'):
                action_type = action_type.value
            type_count[action_type] = type_count.get(action_type, 0) + 1
        
        return type_count
    
    def _estimate_execution_parameters(self, action_sequence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        估计执行参数
        
        Args:
            action_sequence: 动作序列
            
        Returns:
            Dict[str, Any]: 执行估计
        """
        total_time = 0
        total_resources = 0
        resource_types = {}
        
        # 动作类型到持续时间的映射（秒）
        duration_estimates = {
            'move_to_action': 2.0,
            'navigate_action': 5.0,
            'grasp_action': 1.5,
            'move_action': 3.0,
            'place_action': 1.5,
            'detect_action': 1.0,
            'classify_action': 0.5,
            'position_update_action': 0.5,
            'gripper_control_action': 0.5,
            'generic_action': 2.0,
            'unknown': 1.0
        }
        
        # 动作类型到资源消耗的映射
        resource_estimates = {
            'move_to_action': 10,
            'navigate_action': 20,
            'grasp_action': 15,
            'move_action': 12,
            'place_action': 15,
            'detect_action': 8,
            'classify_action': 5,
            'position_update_action': 3,
            'gripper_control_action': 7,
            'generic_action': 10,
            'unknown': 5
        }
        
        for action in action_sequence:
            action_type = action.get('type', 'unknown')
            if hasattr(action_type, 'value'):
                action_type = action_type.value
            
            # 计算时间估计
            if 'estimated_duration' in action:
                action_time = action['estimated_duration']
            else:
                action_time = duration_estimates.get(action_type, 1.0)
            total_time += action_time
            
            # 计算资源估计
            if 'required_resources' in action and action['required_resources']:
                # 使用动作自己的资源需求
                for resource in action['required_resources']:
                    if isinstance(resource, dict) and 'type' in resource:
                        resource_type = resource['type']
                        resource_types[resource_type] = resource_types.get(resource_type, 0) + 1
            else:
                # 使用默认资源估计
                total_resources += resource_estimates.get(action_type, 5)
        
        return {
            'total_estimated_time': total_time,
            'total_resource_requirement': total_resources,
            'resource_distribution': resource_types,
            'actions_per_second': len(action_sequence) / max(total_time, 1.0),
            'estimated_completion_time': time.time() + total_time
        }
    
    def _estimate_resource_utilization(self, action_sequence: List[Dict[str, Any]]) -> float:
        """
        估计资源利用率
        
        Args:
            action_sequence: 动作序列
            
        Returns:
            float: 资源利用率（0-1）
        """
        if not action_sequence:
            return 0.0
        
        # 计算平均资源需求
        total_resources = 0
        for action in action_sequence:
            if 'required_resources' in action:
                total_resources += len(action['required_resources'])
        
        avg_resources = total_resources / len(action_sequence)
        
        # 将资源需求映射到0-1范围
        # 假设平均每个动作需要0-5个资源
        utilization = min(avg_resources / 5.0, 1.0)
        
        return utilization
    
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
                'sequence_improvements': {},
                'last_updated': time.time()
            }
        
        # 添加模块反馈
        self.feedback_cache[goal_hash]['module_feedback'][module_name] = {
            'feedback': feedback,
            'timestamp': time.time()
        }
        
        # 提取序列改进建议
        if 'sequence_suggestions' in feedback:
            self.feedback_cache[goal_hash]['sequence_improvements'].update(feedback['sequence_suggestions'])
        
        # 更新最后更新时间
        self.feedback_cache[goal_hash]['last_updated'] = time.time()
        
        logger.info(f"Registered feedback from {module_name} for action sequencing: {goal_text[:30]}...")
    
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
    
    def _is_action_pddl_compatible(self, action: Dict[str, Any]) -> bool:
        """
        检查动作是否兼容PDDL
        
        Args:
            action: 动作
            
        Returns:
            bool: 是否兼容
        """
        # 检查必要字段
        required_fields = ['type', 'parameters']
        for field in required_fields:
            if field not in action:
                return False
        
        # 检查参数是否可序列化
        try:
            parameters = action.get('parameters', {})
            json.dumps(parameters)
            return True
        except:
            return False
    
    def _update_action_stats(self, action_count: int):
        """
        更新动作统计
        
        Args:
            action_count: 动作数量
        """
        total = self.stats['total_sequences']
        current_avg = self.stats['average_action_count']
        self.stats['average_action_count'] = (
            (current_avg * (total - 1)) + action_count
        ) / total
    
    def _update_confidence_stats(self, confidence: float):
        """
        更新置信度统计
        
        Args:
            confidence: 置信度分数
        """
        total = self.stats['total_sequences']
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
            'total_sequences': self.stats['total_sequences'],
            'success_rate': self.stats['successful_sequences'] / max(self.stats['total_sequences'], 1),
            'average_action_count': self.stats['average_action_count'],
            'average_confidence': self.stats['average_confidence'],
            'feedback_applied': self.stats['feedback_applied'],
            'error_distribution': self.stats['error_types'],
            'module_interfaces': {k: v['enabled'] for k, v in self.module_interfaces.items()}
        }
    
    def create_error_diagnosis(self, result: IntegratedActionSequenceResult) -> Dict[str, Any]:
        """
        创建错误诊断
        
        Args:
            result: 集成动作序列结果
            
        Returns:
            Dict[str, Any]: 诊断信息
        """
        diagnosis = {
            'possible_causes': [],
            'recommendations': [],
            'module_specific_issues': {}
        }
        
        # 检查兼容性标志
        if not result.compatibility_flags.get('execution_compatible'):
            diagnosis['possible_causes'].append('No valid action sequence generated')
            diagnosis['recommendations'].append('Check subgoal and transition data for validity')
            diagnosis['module_specific_issues']['execution'] = 'No valid action sequence'
        
        if not result.compatibility_flags.get('pddl_compatible'):
            diagnosis['possible_causes'].append('Actions contain non-PDDL compatible elements')
            diagnosis['recommendations'].append('Simplify action parameters to basic data types')
            diagnosis['module_specific_issues']['pddl'] = 'Incompatible action structure'
        
        if not result.compatibility_flags.get('resource_compatible'):
            diagnosis['possible_causes'].append('Excessive resource requirements')
            diagnosis['recommendations'].append('Optimize sequence to reduce resource usage')
            diagnosis['module_specific_issues']['resource'] = 'Resource limit exceeded'
        
        if not result.compatibility_flags.get('time_compatible'):
            diagnosis['possible_causes'].append('Estimated execution time too long')
            diagnosis['recommendations'].append('Split goal into smaller subgoals')
            diagnosis['module_specific_issues']['time'] = 'Time limit exceeded'
        
        if len(result.action_sequence) > 20:
            diagnosis['possible_causes'].append('Sequence too long, may be inefficient')
            diagnosis['recommendations'].append('Merge similar actions or reconfigure sequencing')
        
        if result.confidence_score < 0.5:
            diagnosis['possible_causes'].append('Low confidence in action sequence')
            diagnosis['recommendations'].append('Provide more specific action requirements')
        
        # 检查约束满足率
        constraint_rate = result.validation_metadata.get('constraint_satisfaction_rate', 1.0)
        if constraint_rate < 0.8:
            diagnosis['possible_causes'].append('Low constraint satisfaction rate')
            diagnosis['recommendations'].append('Adjust constraints or sequencing parameters')
            diagnosis['module_specific_issues']['constraints'] = 'Poor satisfaction'
        
        return diagnosis