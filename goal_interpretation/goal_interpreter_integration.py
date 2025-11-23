"""
目标解释模块集成接口

提供与其他模块（子目标分解、转换建模、动作序列）的集成功能
实现错误处理和反向反馈机制
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
import json
import uuid
import hashlib
import time

from goal_interpretation.goal_interpreter import GoalInterpreter, InterpretationRequest, InterpretationResponse
from goal_interpretation.models import GoalType, GoalState, ContextInfo

# 尝试导入embodied-agent-interface中的目标解释评估器
try:
    from embodied_agent_interface.src.behavior_eval.evaluation.goal_interpretation.scripts.evaluate_results import (
        evaluate_goals,
        dataset_error_analysis,
        parse_json,
        goal_interpretation_data
    )
    GOAL_INTERPRETATION_EVALUATOR_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Failed to import goal interpretation evaluator: {e}")
    GOAL_INTERPRETATION_EVALUATOR_AVAILABLE = False

# 设置日志
logger = logging.getLogger(__name__)


@dataclass
class IntegratedInterpretationResult:
    """
    集成解释结果，包含与其他模块交互所需的完整信息
    """
    original_goal: str
    interpreted_goal: GoalState
    goal_type: GoalType
    subgoal_creation_data: Dict[str, Any] = field(default_factory=dict)
    transition_modeling_data: Dict[str, Any] = field(default_factory=dict)
    action_sequencing_data: Dict[str, Any] = field(default_factory=dict)
    validation_metadata: Dict[str, Any] = field(default_factory=dict)
    compatibility_flags: Dict[str, bool] = field(default_factory=dict)
    confidence_score: float = 0.0


class GoalInterpreterIntegration:
    """
    目标解释器集成类，负责与其他模块的交互
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化目标解释器集成组件
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        
        # 初始化目标解释器
        interpreter_config = self.config.get('interpreter', {})
        self.interpreter = GoalInterpreter(interpreter_config)
        
        # 模块联动配置
        self.enable_module_feedback = self.config.get('enable_module_feedback', True)
        self.enable_error_handling = self.config.get('enable_error_handling', True)
        self.timeout_seconds = self.config.get('timeout_seconds', 30)
        
        # 反向反馈缓存
        self.feedback_cache = {}
        self.module_interfaces = {
            'subgoal_decomposition': {'enabled': True, 'version': '1.0'},
            'transition_modeling': {'enabled': True, 'version': '1.0'},
            'action_sequencing': {'enabled': True, 'version': '1.0'}
        }
        
        # 统计信息
        self.stats = {
            'total_interpretations': 0,
            'successful_interpretations': 0,
            'failed_interpretations': 0,
            'feedback_applied': 0,
            'error_types': {},
            'average_confidence': 0.0
        }
        
        # 评估器配置
        self.use_evaluator = self.config.get('use_evaluator', False)
        self.evaluator_data = None
        
        logger.info("Goal Interpreter Integration initialized")
    
    def interpret_goal_for_integration(self, 
                                      goal_text: str, 
                                      context: Optional[Dict[str, Any]] = None,
                                      module_feedback: Optional[Dict[str, Any]] = None) -> IntegratedInterpretationResult:
        """
        为模块集成解释目标
        
        Args:
            goal_text: 目标文本
            context: 上下文信息
            module_feedback: 来自其他模块的反馈
            
        Returns:
            IntegratedInterpretationResult: 集成解释结果
        """
        self.stats['total_interpretations'] += 1
        
        try:
            # 应用反向反馈
            if self.enable_module_feedback and module_feedback:
                self._apply_module_feedback(goal_text, module_feedback)
            
            # 准备解释请求
            interpretation_request = self._prepare_integration_request(goal_text, context)
            
            # 执行解释
            interpretation_response = self.interpreter.interpret(interpretation_request)
            
            # 构建集成结果
            result = self._build_integrated_result(
                goal_text, 
                interpretation_response,
                context
            )
            
            # 验证与其他模块的兼容性
            compatibility_flags = self._validate_module_compatibility(result)
            result.compatibility_flags = compatibility_flags
            
            if interpretation_response.success:
                self.stats['successful_interpretations'] += 1
                self._update_confidence_stats(result.confidence_score)
            else:
                self.stats['failed_interpretations'] += 1
                self._record_error_type('interpretation_failed')
            
            return result
            
        except Exception as e:
            logger.error(f"Error in goal interpretation for integration: {str(e)}")
            self.stats['failed_interpretations'] += 1
            self._record_error_type('exception')
            
            # 返回错误时的默认结果
            return IntegratedInterpretationResult(
                original_goal=goal_text,
                interpreted_goal=GoalState(variables={}, constraints=[]),
                goal_type=GoalType.UNKNOWN,
                confidence_score=0.0,
                compatibility_flags={'error_occurred': True},
                validation_metadata={'error_message': str(e)}
            )
    
    def _prepare_integration_request(self, goal_text: str, context: Optional[Dict[str, Any]]) -> InterpretationRequest:
        """
        准备集成请求
        
        Args:
            goal_text: 目标文本
            context: 上下文信息
            
        Returns:
            InterpretationRequest: 解释请求
        """
        # 应用上下文增强
        enhanced_context = self._enhance_context(context)
        
        # 检查是否有缓存的反馈
        feedback_applied = False
        goal_hash = hashlib.md5(goal_text.encode()).hexdigest()
        
        if goal_hash in self.feedback_cache:
            cached_feedback = self.feedback_cache[goal_hash]
            logger.info(f"Applying cached feedback for goal: {goal_text[:30]}...")
            self.stats['feedback_applied'] += 1
            feedback_applied = True
            
            # 使用反馈优化上下文
            if 'context_enhancements' in cached_feedback:
                for key, value in cached_feedback['context_enhancements'].items():
                    enhanced_context[key] = value
        
        # 创建请求
        request = InterpretationRequest(
            goal_text=goal_text,
            context=ContextInfo(**enhanced_context) if enhanced_context else None,
            request_id=f"goal_int_{uuid.uuid4()}",
            enable_advanced_parsing=True,
            enable_grounding=True,
            metadata={
                'feedback_applied': feedback_applied,
                'integration_mode': True
            }
        )
        
        return request
    
    def _build_integrated_result(self, 
                                goal_text: str,
                                interpretation_response: InterpretationResponse,
                                context: Optional[Dict[str, Any]]) -> IntegratedInterpretationResult:
        """
        构建集成结果
        
        Args:
            goal_text: 原始目标文本
            interpretation_response: 解释响应
            context: 上下文信息
            
        Returns:
            IntegratedInterpretationResult: 集成结果
        """
        # 提取解释结果
        interpreted_goal = interpretation_response.goal_state
        goal_type = interpretation_response.goal_type
        confidence_score = getattr(interpretation_response, 'confidence_score', 0.0)
        
        # 构建子目标分解所需数据
        subgoal_creation_data = self._build_subgoal_data(interpreted_goal, goal_type, context)
        
        # 构建转换建模所需数据
        transition_modeling_data = self._build_transition_data(interpreted_goal, goal_type)
        
        # 构建动作序列所需数据
        action_sequencing_data = self._build_action_data(interpreted_goal, goal_type)
        
        # 构建验证元数据
        validation_metadata = {
            'interpretation_time': getattr(interpretation_response, 'interpretation_time', 0.0),
            'grounding_success': getattr(interpretation_response, 'grounding_success', False),
            'semantic_analysis': getattr(interpretation_response, 'semantic_analysis', {}),
            'entity_extraction': getattr(interpretation_response, 'entity_extraction', {})
        }
        
        return IntegratedInterpretationResult(
            original_goal=goal_text,
            interpreted_goal=interpreted_goal,
            goal_type=goal_type,
            subgoal_creation_data=subgoal_creation_data,
            transition_modeling_data=transition_modeling_data,
            action_sequencing_data=action_sequencing_data,
            validation_metadata=validation_metadata,
            confidence_score=confidence_score
        )
    
    def _validate_module_compatibility(self, result: IntegratedInterpretationResult) -> Dict[str, bool]:
        """
        验证与其他模块的兼容性
        
        Args:
            result: 集成解释结果
            
        Returns:
            Dict[str, bool]: 兼容性标志
        """
        compatibility = {
            'subgoal_compatible': True,
            'transition_compatible': True,
            'action_compatible': True,
            'pddl_compatible': True
        }
        
        # 验证子目标兼容性
        if not result.subgoal_creation_data.get('valid_conditions'):
            compatibility['subgoal_compatible'] = False
        
        # 验证PDDL兼容性
        variables = result.interpreted_goal.variables if hasattr(result.interpreted_goal, 'variables') else {}
        if not variables:
            compatibility['pddl_compatible'] = False
        
        # 检查目标类型
        if result.goal_type == GoalType.UNKNOWN:
            compatibility['transition_compatible'] = False
            compatibility['action_compatible'] = False
        
        return compatibility
    
    def _build_subgoal_data(self, goal_state: GoalState, goal_type: GoalType, context: Optional[Dict]) -> Dict[str, Any]:
        """
        构建子目标分解所需数据
        
        Args:
            goal_state: 目标状态
            goal_type: 目标类型
            context: 上下文信息
            
        Returns:
            Dict[str, Any]: 子目标数据
        """
        variables = getattr(goal_state, 'variables', {})
        constraints = getattr(goal_state, 'constraints', [])
        
        return {
            'goal_variables': variables,
            'goal_constraints': constraints,
            'goal_type': goal_type.value,
            'context_relevant': context or {},
            'valid_conditions': len(variables) > 0 or len(constraints) > 0,
            'decomposition_strategy': self._determine_decomposition_strategy(goal_type, variables),
            'priority_order': self._determine_priority_order(variables)
        }
    
    def _build_transition_data(self, goal_state: GoalState, goal_type: GoalType) -> Dict[str, Any]:
        """
        构建转换建模所需数据
        
        Args:
            goal_state: 目标状态
            goal_type: 目标类型
            
        Returns:
            Dict[str, Any]: 转换数据
        """
        variables = getattr(goal_state, 'variables', {})
        
        # 提取目标状态作为转换的目标
        transition_goal = {}
        for key, value in variables.items():
            # 确保值是可序列化的
            if isinstance(value, (int, float, str, bool, type(None))):
                transition_goal[key] = value
            elif isinstance(value, (list, dict)):
                # 尝试转换为可序列化的形式
                try:
                    json.dumps(value)
                    transition_goal[key] = value
                except:
                    transition_goal[key] = str(value)
            else:
                transition_goal[key] = str(value)
        
        return {
            'goal_state': transition_goal,
            'goal_type': goal_type.value,
            'variable_count': len(variables),
            'suggested_initial_variables': self._suggest_initial_variables(goal_type, variables)
        }
    
    def _build_action_data(self, goal_state: GoalState, goal_type: GoalType) -> Dict[str, Any]:
        """
        构建动作序列所需数据
        
        Args:
            goal_state: 目标状态
            goal_type: 目标类型
            
        Returns:
            Dict[str, Any]: 动作数据
        """
        variables = getattr(goal_state, 'variables', {})
        
        return {
            'goal_conditions': variables,
            'goal_type': goal_type.value,
            'action_requirements': self._determine_action_requirements(goal_type),
            'sequence_constraints': self._generate_sequence_constraints(goal_type, variables)
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
                'last_updated': time.time()
            }
        
        # 添加模块反馈
        self.feedback_cache[goal_hash]['module_feedback'][module_name] = {
            'feedback': feedback,
            'timestamp': time.time()
        }
        
        # 更新最后更新时间
        self.feedback_cache[goal_hash]['last_updated'] = time.time()
        
        logger.info(f"Registered feedback from {module_name} for goal: {goal_text[:30]}...")
    
    def _apply_module_feedback(self, goal_text: str, feedback: Dict[str, Any]):
        """
        应用来自其他模块的反馈
        
        Args:
            goal_text: 目标文本
            feedback: 反馈数据
        """
        # 这是一个简化实现，实际应该根据反馈类型进行更复杂的处理
        module_name = feedback.get('module_name')
        if module_name:
            self.register_module_feedback(goal_text, module_name, feedback.get('data', {}))
    
    def _enhance_context(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        增强上下文信息
        
        Args:
            context: 原始上下文
            
        Returns:
            Dict[str, Any]: 增强后的上下文
        """
        enhanced = context.copy() if context else {}
        
        # 添加模块集成标志
        enhanced['integration_mode'] = True
        enhanced['timestamp'] = time.time()
        
        return enhanced
    
    def _evaluate_interpretation(self, 
                                interpreted_goal: GoalState, 
                                ground_truth: Dict[str, Any],
                                context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        使用embodied-agent-interface的评估器评估目标解释结果
        
        Args:
            interpreted_goal: 解释后的目标状态
            ground_truth: 真实目标状态
            context: 上下文信息
            
        Returns:
            Dict[str, Any]: 评估结果
        """
        if not self.use_evaluator or not GOAL_INTERPRETATION_EVALUATOR_AVAILABLE:
            return {'error': 'Evaluator not available'}
        
        try:
            # 将解释结果转换为评估器需要的格式
            predicted_goals = self._convert_to_evaluator_format(interpreted_goal)
            
            # 调用评估器
            satisfied_conditions, unsatisfied_conditions, false_positive_conditions, flattened_predicted_conditions = \
                evaluate_goals(predicted_goals, ground_truth)
            
            # 计算错误分析（如果有上下文信息）
            demo_name = context.get('demo_name', 'default_demo') if context else 'default_demo'
            
            # 使用统一的错误分析函数
            error_analysis = dataset_error_analysis(
                satisfied_conditions, 
                unsatisfied_conditions, 
                false_positive_conditions, 
                flattened_predicted_conditions, 
                num_object_hallucinations=0
            )
            
            # 计算综合评分
            overall_metrics = error_analysis.get('overall', {})
            confusion_metrics = overall_metrics.get('overall_confusion_metrics', {})
            
            # 计算置信度分数（基于F1分数）
            f1_score = confusion_metrics.get('f1', 0.0)
            confidence_score = float(f1_score)  # 转换为float类型
            
            return {
                'satisfied_conditions': satisfied_conditions,
                'unsatisfied_conditions': unsatisfied_conditions,
                'false_positive_conditions': false_positive_conditions,
                'error_analysis': error_analysis,
                'confidence_score': confidence_score
            }
            
        except Exception as e:
            logging.error(f"Error evaluating interpretation: {str(e)}")
            return {'error': str(e)}
    
    def _convert_to_evaluator_format(self, goal_state: GoalState) -> Dict[str, List]:
        """
        将GoalState转换为评估器所需的格式
        
        Args:
            goal_state: 目标状态
            
        Returns:
            Dict[str, List]: 评估器格式的目标表示
        """
        # 初始化节点目标和边目标
        node_goals = []
        edge_goals = []
        
        # 处理约束
        for constraint in goal_state.constraints:
            # 根据约束的长度和类型判断是节点目标还是边目标
            # 节点目标通常格式为 [object, state]
            # 边目标通常格式为 [object1, relation, object2]
            
            # 这里需要根据实际的constraint结构进行适当的转换
            # 这是一个简化的实现，实际可能需要更复杂的逻辑
            if hasattr(constraint, 'to_tuple'):
                constraint_tuple = constraint.to_tuple()
                if len(constraint_tuple) == 2:
                    node_goals.append(constraint_tuple)
                elif len(constraint_tuple) == 3:
                    edge_goals.append(constraint_tuple)
            else:
                # 尝试直接处理
                try:
                    if isinstance(constraint, (list, tuple)):
                        if len(constraint) == 2:
                            node_goals.append(constraint)
                        elif len(constraint) == 3:
                            edge_goals.append(constraint)
                except Exception as e:
                    logging.warning(f"Failed to convert constraint: {constraint}, error: {e}")
        
        return {
            "node goals": node_goals,
            "edge goals": edge_goals
        }
    
    def _generate_mock_evaluator_response(self, goal_state: GoalState) -> Dict[str, Any]:
        """
        当评估器不可用时生成模拟评估结果
        
        Args:
            goal_state: 目标状态
            
        Returns:
            Dict[str, Any]: 模拟评估结果
        """
        # 基于约束数量和复杂性生成一个简单的模拟评分
        num_constraints = len(goal_state.constraints)
        
        # 简单的启发式评分
        if num_constraints == 0:
            confidence_score = 0.1
        elif num_constraints <= 2:
            confidence_score = 0.7
        elif num_constraints <= 5:
            confidence_score = 0.8
        else:
            confidence_score = 0.9
        
        return {
            'satisfied_conditions': [],
            'unsatisfied_conditions': [],
            'false_positive_conditions': [],
            'error_analysis': {'overall': {'overall_confusion_metrics': {'f1': confidence_score}}},
            'confidence_score': confidence_score,
            'is_mock': True
        }
    
    def _determine_decomposition_strategy(self, goal_type: GoalType, variables: Dict) -> str:
        """
        确定分解策略
        
        Args:
            goal_type: 目标类型
            variables: 目标变量
            
        Returns:
            str: 分解策略
        """
        # 基于目标类型和变量数量选择策略
        if goal_type == GoalType.OBJECT_MANIPULATION:
            return 'spatial_decomposition'
        elif goal_type == GoalType.NAVIGATION:
            return 'waypoint_decomposition'
        elif len(variables) > 5:
            return 'hierarchical_decomposition'
        else:
            return 'sequential_decomposition'
    
    def _determine_priority_order(self, variables: Dict) -> List[str]:
        """
        确定变量优先顺序
        
        Args:
            variables: 变量字典
            
        Returns:
            List[str]: 优先顺序列表
        """
        # 这是一个简化实现，实际应该基于领域知识确定优先级
        priority_order = []
        
        # 通常位置和状态变量优先级更高
        position_keywords = ['position', 'location', 'pose', 'coordinate']
        state_keywords = ['state', 'status', 'mode']
        
        # 先添加位置相关变量
        for key in variables.keys():
            for keyword in position_keywords:
                if keyword in key.lower():
                    priority_order.append(key)
                    break
        
        # 再添加状态相关变量
        for key in variables.keys():
            if key not in priority_order:
                for keyword in state_keywords:
                    if keyword in key.lower():
                        priority_order.append(key)
                        break
        
        # 最后添加其他变量
        for key in variables.keys():
            if key not in priority_order:
                priority_order.append(key)
        
        return priority_order
    
    def _suggest_initial_variables(self, goal_type: GoalType, variables: Dict) -> Dict[str, Any]:
        """
        建议初始变量
        
        Args:
            goal_type: 目标类型
            variables: 目标变量
            
        Returns:
            Dict[str, Any]: 建议的初始变量
        """
        suggested = {}
        
        # 根据目标类型建议初始变量
        if goal_type == GoalType.OBJECT_MANIPULATION:
            suggested['robot_position'] = 'initial_position'
            suggested['grasp_status'] = 'open'
        elif goal_type == GoalType.NAVIGATION:
            suggested['current_location'] = 'start_point'
        
        return suggested
    
    def _determine_action_requirements(self, goal_type: GoalType) -> List[str]:
        """
        确定动作需求
        
        Args:
            goal_type: 目标类型
            
        Returns:
            List[str]: 动作需求列表
        """
        requirements = []
        
        if goal_type == GoalType.OBJECT_MANIPULATION:
            requirements.extend(['grasp_action', 'move_action', 'place_action'])
        elif goal_type == GoalType.NAVIGATION:
            requirements.extend(['move_to_action', 'navigate_action'])
        elif goal_type == GoalType.OBJECT_RECOGNITION:
            requirements.extend(['detect_action', 'classify_action'])
        
        return requirements
    
    def _generate_sequence_constraints(self, goal_type: GoalType, variables: Dict) -> List[Dict[str, Any]]:
        """
        生成序列约束
        
        Args:
            goal_type: 目标类型
            variables: 变量字典
            
        Returns:
            List[Dict[str, Any]]: 约束列表
        """
        constraints = []
        
        if goal_type == GoalType.OBJECT_MANIPULATION:
            constraints.append({
                'type': 'order_constraint',
                'action1': 'grasp_action',
                'action2': 'place_action',
                'relation': 'before'
            })
        
        return constraints
    
    def _update_confidence_stats(self, confidence: float):
        """
        更新置信度统计
        
        Args:
            confidence: 置信度分数
        """
        total = self.stats['total_interpretations']
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
            'total_interpretations': self.stats['total_interpretations'],
            'success_rate': self.stats['successful_interpretations'] / max(self.stats['total_interpretations'], 1),
            'average_confidence': self.stats['average_confidence'],
            'feedback_applied': self.stats['feedback_applied'],
            'error_distribution': self.stats['error_types'],
            'module_interfaces': {k: v['enabled'] for k, v in self.module_interfaces.items()}
        }
    
    def create_error_diagnosis(self, result: IntegratedInterpretationResult) -> Dict[str, Any]:
        """
        创建错误诊断
        
        Args:
            result: 集成解释结果
            
        Returns:
            Dict[str, Any]: 诊断信息
        """
        diagnosis = {
            'possible_causes': [],
            'recommendations': [],
            'module_specific_issues': {}
        }
        
        # 检查兼容性标志
        if not result.compatibility_flags.get('subgoal_compatible'):
            diagnosis['possible_causes'].append('Invalid goal structure for subgoal decomposition')
            diagnosis['recommendations'].append('Ensure the goal has valid variables and constraints')
            diagnosis['module_specific_issues']['subgoal_decomposition'] = 'Invalid goal structure'
        
        if not result.compatibility_flags.get('transition_compatible'):
            diagnosis['possible_causes'].append('Goal type not supported for transition modeling')
            diagnosis['recommendations'].append('Use a more specific goal or provide additional context')
            diagnosis['module_specific_issues']['transition_modeling'] = 'Unsupported goal type'
        
        if not result.compatibility_flags.get('pddl_compatible'):
            diagnosis['possible_causes'].append('Goal not compatible with PDDL representation')
            diagnosis['recommendations'].append('Simplify the goal or provide explicit state variables')
            diagnosis['module_specific_issues']['pddl'] = 'Incompatible structure'
        
        if result.confidence_score < 0.5:
            diagnosis['possible_causes'].append('Low confidence in goal interpretation')
            diagnosis['recommendations'].append('Restate the goal with more clarity')
        
        return diagnosis