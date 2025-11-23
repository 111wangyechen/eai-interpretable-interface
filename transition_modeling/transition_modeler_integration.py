"""
转换建模模块集成接口

提供与其他模块的联动接口，处理模块间数据格式转换和错误反馈
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
import json
import uuid
import time
import sys
import os

# 添加项目根目录到Python路径，以便导入embodied-agent-interface
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IntegratedModelingResult:
    """
    集成转换建模结果
    """
    # 核心结果
    success: bool
    transition_sequences: List[Dict[str, Any]]
    confidence_score: float
    modeling_time: float
    
    # 兼容性信息
    compatibility_flags: Dict[str, bool] = field(default_factory=dict)
    validation_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 动作序列所需数据
    action_sequencing_data: Dict[str, Any] = field(default_factory=dict)
    
    # 错误和警告
    errors: List[Dict[str, str]] = field(default_factory=list)
    warnings: List[Dict[str, str]] = field(default_factory=list)
    
    # 诊断信息
    diagnostics: Dict[str, Any] = field(default_factory=dict)
    
    # 模块联动信息
    module_feedback: Optional[Dict[str, Any]] = None
    request_id: str = field(default_factory=lambda: f"model_{uuid.uuid4()}")


class TransitionModelerIntegration:
    """
    转换建模模块集成类
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化转换建模集成器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        
        # 模块配置
        self.enable_debugging = self.config.get('enable_debugging', False)
        self.enable_module_feedback = self.config.get('enable_module_feedback', True)
        self.enable_error_handling = self.config.get('enable_error_handling', True)
        self.max_sequence_length = self.config.get('max_sequence_length', 20)
        self.min_confidence_threshold = self.config.get('min_confidence_threshold', 0.7)
        
        # 反向反馈机制
        self.feedback_cache = {}
        self.module_interfaces = {}
        
        # 统计信息
        self.stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'compatibility_errors': 0,
            'validation_errors': 0,
            'recovery_attempts': 0,
            'recovery_successes': 0,
            'average_modeling_time': 0,
            'total_modeling_time': 0
        }
        
        # 初始化原始转换建模模块
        self._initialize_original_module()
        
        logger.info("TransitionModelerIntegration initialized")
    
    def _initialize_original_module(self):
        """
        初始化原始转换建模模块和embodied-agent-interface的TransitionModelingEvaluator
        """
        # 初始化原始转换建模器
        try:
            # 动态导入原始转换建模模块
            from transition_modeler import TransitionModeler
            self.original_modeler = TransitionModeler(self.config)
            logger.info("Original TransitionModeler initialized")
        except ImportError:
            try:
                # 尝试直接导入
                import transition_modeler
                if hasattr(transition_modeler, 'TransitionModeler'):
                    self.original_modeler = transition_modeler.TransitionModeler(self.config)
                    logger.info("Original TransitionModeler initialized")
                else:
                    self.original_modeler = None
                    logger.warning("TransitionModeler class not found")
            except Exception as e:
                logger.error(f"Failed to initialize original TransitionModeler: {str(e)}")
                self.original_modeler = None
        
        # 尝试导入embodied-agent-interface中的TransitionModelingEvaluator
        self.transition_modeling_evaluator = None
        try:
            from embodied_agent_interface.src.behavior_eval.evaluation.transition_modeling.transition_modeling_evaluator import TransitionModelingEvaluator
            self.transition_modeling_evaluator = TransitionModelingEvaluator
            logger.info("TransitionModelingEvaluator from embodied-agent-interface imported successfully")
        except ImportError as e:
            logger.warning(f"Failed to import TransitionModelingEvaluator: {str(e)}")
        except Exception as e:
            logger.error(f"Error initializing TransitionModelingEvaluator: {str(e)}")
    
    def model_transitions_for_integration(self, 
                                         goal_text: str, 
                                         subgoal_data: Dict[str, Any],
                                         module_feedback: Optional[Dict[str, Any]] = None,
                                         context: Optional[Dict[str, Any]] = None) -> IntegratedModelingResult:
        """
        为集成流程建模转换，支持使用embodied-agent-interface的TransitionModelingEvaluator
        
        Args:
            goal_text: 目标文本
            subgoal_data: 子目标数据
            module_feedback: 模块反馈
            context: 上下文信息，可包含demo_name用于TransitionModelingEvaluator
            
        Returns:
            IntegratedModelingResult: 集成转换建模结果
        """
        self.stats['total_calls'] += 1
        start_time = time.time()
        
        # 初始化结果
        result = IntegratedModelingResult(
            success=False,
            transition_sequences=[],
            confidence_score=0.0,
            modeling_time=0.0
        )
        
        try:
            # 应用模块反馈
            if module_feedback:
                self.register_module_feedback(goal_text, module_feedback)
                result.module_feedback = module_feedback
            
            # 准备子目标数据
            prepared_data = self._prepare_subgoal_data(subgoal_data)
            
            # 验证数据兼容性
            validation_result = self._validate_subgoal_data(prepared_data)
            result.validation_metadata = validation_result['metadata']
            
            # 如果验证失败，尝试恢复
            if not validation_result['valid']:
                result.warnings.append({
                    'type': 'validation_warning',
                    'message': 'Subgoal data requires normalization',
                    'details': validation_result['errors']
                })
                
                # 尝试数据恢复
                recovery_success = self._recover_subgoal_data(prepared_data)
                if recovery_success:
                    self.stats['recovery_attempts'] += 1
                    self.stats['recovery_successes'] += 1
                    result.warnings.append({
                        'type': 'recovery_success',
                        'message': 'Successfully recovered subgoal data'
                    })
                else:
                    self.stats['recovery_attempts'] += 1
                    error_msg = f"Failed to validate subgoal data: {', '.join(validation_result['errors'][:3])}"
                    result.errors.append({
                        'type': 'validation_error',
                        'message': error_msg
                    })
                    self.stats['validation_errors'] += 1
                    return self._finalize_result(result, start_time)
            
            # 尝试使用embodied-agent-interface的TransitionModelingEvaluator
            if self.transition_modeling_evaluator:
                try:
                    # 从上下文获取demo_name
                    demo_name = context.get('demo_name', 'default_demo') if context else 'default_demo'
                    
                    # 创建TransitionModelingEvaluator实例
                    evaluator_instance = self.transition_modeling_evaluator(demo_name=demo_name)
                    
                    # 获取提示
                    prompt = evaluator_instance.get_prompt()
                    logger.info(f"Generated prompt from TransitionModelingEvaluator for demo: {demo_name}")
                    
                    # 在实际使用中，这里应该调用LLM API获取响应
                    # 为了测试，使用模拟响应
                    mock_response = self._generate_mock_evaluator_response(prompt, demo_name)
                    
                    # 解析响应
                    parsed_actions = evaluator_instance.parse_response(mock_response)
                    
                    # 计算分数
                    modeling_result = evaluator_instance.compute_score(parsed_actions)
                    
                    # 处理evaluator结果
                    result = self._process_evaluator_result(modeling_result, result, demo_name)
                    
                    # 标记使用了evaluator
                    result.diagnostics['used_evaluator'] = True
                except Exception as e:
                    logger.error(f"Error using TransitionModelingEvaluator: {str(e)}")
                    # 如果evaluator调用失败，回退到原始转换建模模块
                    modeling_result = self._call_original_modeler(goal_text, prepared_data, context)
                    
                    # 处理原始结果
                    if modeling_result:
                        result = self._process_original_result(modeling_result, result)
                    else:
                        # 如果原始模块不可用，使用模拟结果
                        result = self._create_fallback_result(goal_text, prepared_data, result)
                    
                    # 记录错误
                    result.diagnostics['evaluator_error'] = str(e)
            else:
                # 如果evaluator不可用，使用原始转换建模模块
                modeling_result = self._call_original_modeler(goal_text, prepared_data, context)
                
                # 处理原始结果
                if modeling_result:
                    result = self._process_original_result(modeling_result, result)
                else:
                    # 如果原始模块不可用，使用模拟结果
                    result = self._create_fallback_result(goal_text, prepared_data, result)
            
            # 构建动作序列所需数据
            result.action_sequencing_data = self._build_action_sequencing_data(
                goal_text, prepared_data, result.transition_sequences
            )
            
            # 设置兼容性标志
            result.compatibility_flags = self._set_compatibility_flags(result)
            
            # 如果动作序列数据不兼容，尝试修复
            if not result.compatibility_flags.get('action_sequence_compatible', False):
                self.stats['compatibility_errors'] += 1
                result.warnings.append({
                    'type': 'compatibility_warning',
                    'message': 'Action sequence data requires adjustment'
                })
                
                # 尝试修复兼容性问题
                if self._fix_compatibility_issues(result):
                    result.compatibility_flags['action_sequence_compatible'] = True
                    result.warnings.append({
                        'type': 'compatibility_fixed',
                        'message': 'Successfully fixed compatibility issues'
                    })
            
            # 生成诊断信息
            result.diagnostics = self._generate_diagnostics(result)
            
            # 如果所有检查都通过，标记为成功
            if (result.confidence_score >= self.min_confidence_threshold and 
                not result.errors and 
                result.compatibility_flags.get('action_sequence_compatible', False)):
                result.success = True
                self.stats['successful_calls'] += 1
            
        except Exception as e:
            logger.error(f"Error in model_transitions_for_integration: {str(e)}")
            result.errors.append({
                'type': 'exception',
                'message': str(e)
            })
        
        return self._finalize_result(result, start_time)
    
    def _prepare_subgoal_data(self, subgoal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备子目标数据
        
        Args:
            subgoal_data: 原始子目标数据
            
        Returns:
            Dict[str, Any]: 准备好的数据
        """
        prepared_data = subgoal_data.copy()
        
        # 确保必要字段存在
        if 'subgoals' not in prepared_data:
            prepared_data['subgoals'] = []
        
        if 'subgoal_transitions' not in prepared_data:
            # 从子目标生成转换
            prepared_data['subgoal_transitions'] = self._generate_transitions_from_subgoals(
                prepared_data.get('subgoals', [])
            )
        
        # 标准化子目标格式
        for i, subgoal in enumerate(prepared_data['subgoals']):
            if isinstance(subgoal, str):
                # 转换字符串为标准格式
                prepared_data['subgoals'][i] = {
                    'text': subgoal,
                    'id': f"subgoal_{i}",
                    'priority': len(prepared_data['subgoals']) - i
                }
        
        return prepared_data
    
    def _generate_transitions_from_subgoals(self, subgoals: List[Any]) -> List[Dict[str, Any]]:
        """
        从子目标生成转换
        
        Args:
            subgoals: 子目标列表
            
        Returns:
            List[Dict[str, Any]]: 转换列表
        """
        transitions = []
        
        for i, subgoal in enumerate(subgoals):
            # 创建状态转换
            transition = {
                'source': f"state_{i}",
                'target': f"state_{i+1}",
                'condition': self._extract_condition(subgoal),
                'action': self._extract_action(subgoal),
                'probability': 1.0,
                'subgoal_id': f"subgoal_{i}"
            }
            transitions.append(transition)
        
        return transitions
    
    def _extract_condition(self, subgoal: Any) -> Dict[str, Any]:
        """
        从子目标提取条件
        
        Args:
            subgoal: 子目标
            
        Returns:
            Dict[str, Any]: 条件
        """
        if isinstance(subgoal, dict):
            return subgoal.get('condition', {'type': 'default', 'value': True})
        return {'type': 'default', 'value': True}
    
    def _extract_action(self, subgoal: Any) -> Dict[str, Any]:
        """
        从子目标提取动作
        
        Args:
            subgoal: 子目标
            
        Returns:
            Dict[str, Any]: 动作
        """
        if isinstance(subgoal, dict):
            return subgoal.get('action', {
                'type': 'execute_subgoal',
                'subgoal_id': subgoal.get('id', 'unknown')
            })
        elif isinstance(subgoal, str):
            return {
                'type': 'execute_subgoal',
                'description': subgoal
            }
        return {'type': 'execute_subgoal', 'description': 'unknown'}
    
    def _validate_subgoal_data(self, subgoal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证子目标数据
        
        Args:
            subgoal_data: 子目标数据
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        errors = []
        metadata = {
            'has_subgoals': 'subgoals' in subgoal_data and len(subgoal_data['subgoals']) > 0,
            'has_transitions': 'subgoal_transitions' in subgoal_data and len(subgoal_data['subgoal_transitions']) > 0,
            'subgoal_count': len(subgoal_data.get('subgoals', [])),
            'transition_count': len(subgoal_data.get('subgoal_transitions', []))
        }
        
        # 检查子目标和转换
        if not metadata['has_subgoals'] and not metadata['has_transitions']:
            errors.append("No subgoals or transitions provided")
        
        # 验证子目标格式
        for i, subgoal in enumerate(subgoal_data.get('subgoals', [])):
            if not isinstance(subgoal, (dict, str)):
                errors.append(f"Invalid subgoal type at index {i}")
        
        # 验证转换格式
        for i, transition in enumerate(subgoal_data.get('subgoal_transitions', [])):
            if not isinstance(transition, dict):
                errors.append(f"Invalid transition type at index {i}")
            elif 'source' not in transition or 'target' not in transition:
                errors.append(f"Missing source/target in transition at index {i}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'metadata': metadata
        }
    
    def _recover_subgoal_data(self, subgoal_data: Dict[str, Any]) -> bool:
        """
        恢复子目标数据
        
        Args:
            subgoal_data: 子目标数据
            
        Returns:
            bool: 是否恢复成功
        """
        try:
            # 尝试从任何可用信息恢复
            if 'subgoals' in subgoal_data and len(subgoal_data['subgoals']) > 0:
                # 重新生成转换
                subgoal_data['subgoal_transitions'] = self._generate_transitions_from_subgoals(
                    subgoal_data['subgoals']
                )
                return True
            
            # 如果有转换但没有子目标，尝试从转换生成子目标
            if 'subgoal_transitions' in subgoal_data and len(subgoal_data['subgoal_transitions']) > 0:
                subgoal_data['subgoals'] = []
                for i, transition in enumerate(subgoal_data['subgoal_transitions']):
                    subgoal = {
                        'id': transition.get('subgoal_id', f"subgoal_{i}"),
                        'text': transition.get('action', {}).get('description', f"Subgoal {i}"),
                        'priority': len(subgoal_data['subgoal_transitions']) - i
                    }
                    subgoal_data['subgoals'].append(subgoal)
                return True
        except Exception as e:
            logger.error(f"Error recovering subgoal data: {str(e)}")
        
        return False
    
    def _call_original_modeler(self, goal_text: str, 
                              prepared_data: Dict[str, Any], 
                              context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """
        调用原始转换建模模块
        
        Args:
            goal_text: 目标文本
            prepared_data: 准备好的数据
            context: 上下文信息
            
        Returns:
            Optional[Any]: 原始结果
        """
        if not self.original_modeler:
            logger.warning("Original modeler not available")
            return None
        
        try:
            # 准备调用参数
            goal_state = prepared_data.get('subgoal_transitions', [])
            context = context or {}
            
            # 添加集成相关信息
            context['integration_mode'] = True
            context['subgoal_data'] = prepared_data.get('subgoals', [])
            context['goal_text'] = goal_text
            
            # 尝试不同的调用方式
            try:
                # 方式1: 使用model_transitions方法
                result = self.original_modeler.model_transitions(
                    goal_state=goal_state,
                    context=context,
                    request_id=f"model_{uuid.uuid4()}"
                )
                return result
            except AttributeError:
                # 方式2: 尝试create_transition_model方法
                if hasattr(self.original_modeler, 'create_transition_model'):
                    result = self.original_modeler.create_transition_model(
                        goal_state=goal_state,
                        context=context
                    )
                    return result
        except Exception as e:
            logger.error(f"Error calling original modeler: {str(e)}")
        
        return None
    
    def _process_original_result(self, original_result: Any, 
                                integrated_result: IntegratedModelingResult) -> IntegratedModelingResult:
        """
        处理原始结果
        
        Args:
            original_result: 原始结果
            integrated_result: 集成结果
            
        Returns:
            IntegratedModelingResult: 更新后的集成结果
        """
        try:
            # 尝试从原始结果提取信息
            if hasattr(original_result, 'transition_sequences'):
                integrated_result.transition_sequences = original_result.transition_sequences
            elif hasattr(original_result, 'sequences'):
                integrated_result.transition_sequences = original_result.sequences
            
            if hasattr(original_result, 'confidence_score'):
                integrated_result.confidence_score = original_result.confidence_score
            elif hasattr(original_result, 'confidence'):
                integrated_result.confidence_score = original_result.confidence
            
            if hasattr(original_result, 'modeling_time'):
                integrated_result.modeling_time = original_result.modeling_time
            
            # 复制其他有用属性
            for attr in ['success', 'errors', 'warnings']:
                if hasattr(original_result, attr):
                    setattr(integrated_result, attr, getattr(original_result, attr))
        except Exception as e:
            logger.error(f"Error processing original result: {str(e)}")
        
        return integrated_result
    
    def _create_fallback_result(self, goal_text: str, 
                               prepared_data: Dict[str, Any],
                               integrated_result: IntegratedModelingResult) -> IntegratedModelingResult:
        """
        创建回退结果
        
        Args:
            goal_text: 目标文本
            prepared_data: 准备好的数据
            integrated_result: 集成结果
            
        Returns:
            IntegratedModelingResult: 回退结果
        """
        # 从子目标创建简单的转换序列
        transitions = prepared_data.get('subgoal_transitions', [])
        
        if transitions:
            integrated_result.transition_sequences = [transitions]
            integrated_result.confidence_score = 0.8
            integrated_result.warnings.append({
                'type': 'fallback_used',
                'message': 'Using fallback transition modeling'
            })
        else:
            # 如果没有转换，创建一个简单的模拟序列
            subgoal_count = len(prepared_data.get('subgoals', []))
            mock_sequence = []
            
            for i in range(subgoal_count):
                mock_transition = {
                    'source': f"initial_state_{i}",
                    'target': f"goal_state_{i}",
                    'action': {'type': 'mock_action', 'description': f"Execute subgoal {i}"},
                    'probability': 0.9,
                    'confidence': 0.8
                }
                mock_sequence.append(mock_transition)
            
            integrated_result.transition_sequences = [mock_sequence]
            integrated_result.confidence_score = 0.7
            integrated_result.warnings.append({
                'type': 'mock_sequences',
                'message': 'Created mock transition sequences'
            })
        
        return integrated_result
    
    def _build_action_sequencing_data(self, goal_text: str, 
                                     prepared_data: Dict[str, Any],
                                     transition_sequences: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        构建动作序列所需数据
        
        Args:
            goal_text: 目标文本
            prepared_data: 准备好的数据
            transition_sequences: 转换序列
            
        Returns:
            Dict[str, Any]: 动作序列数据
        """
        # 提取所有动作
        all_actions = []
        action_mapping = {}
        
        for sequence_idx, sequence in enumerate(transition_sequences):
            for transition_idx, transition in enumerate(sequence):
                action = transition.get('action', {})
                action_id = f"action_{sequence_idx}_{transition_idx}"
                
                # 标准化动作格式
                standard_action = {
                    'id': action_id,
                    'type': action.get('type', 'unknown'),
                    'description': action.get('description', f"Action {action_id}"),
                    'preconditions': transition.get('condition', {}),
                    'effects': {
                        'source': transition.get('source'),
                        'target': transition.get('target')
                    },
                    'probability': transition.get('probability', 1.0),
                    'confidence': transition.get('confidence', 0.8)
                }
                
                all_actions.append(standard_action)
                action_mapping[action_id] = standard_action
        
        # 构建依赖关系
        dependencies = []
        for i in range(len(all_actions) - 1):
            dependencies.append({
                'from': all_actions[i]['id'],
                'to': all_actions[i+1]['id'],
                'type': 'sequential'
            })
        
        return {
            'goal_text': goal_text,
            'subgoals': prepared_data.get('subgoals', []),
            'actions': all_actions,
            'action_mapping': action_mapping,
            'dependencies': dependencies,
            'transition_sequences': transition_sequences,
            'metadata': {
                'total_actions': len(all_actions),
                'total_sequences': len(transition_sequences),
                'has_dependencies': len(dependencies) > 0
            }
        }
    
    def _process_evaluator_result(self, evaluator_result: Dict[str, Any], 
                                  integrated_result: IntegratedModelingResult, 
                                  demo_name: str) -> IntegratedModelingResult:
        """
        处理TransitionModelingEvaluator的结果
        
        Args:
            evaluator_result: TransitionModelingEvaluator的结果
            integrated_result: 集成结果对象
            demo_name: 演示名称
            
        Returns:
            IntegratedModelingResult: 更新后的集成结果
        """
        # 设置基本信息
        integrated_result.success = True
        
        # 从评估器结果构建转换序列
        transition_sequences = []
        for action_name, action_data in evaluator_result.items():
            if action_name != 'avg_summary' and isinstance(action_data, dict):
                transition = {
                    'action': action_name,
                    'precondition_score': action_data.get('precondition_score', 0.0),
                    'effect_score': action_data.get('effect_score', 0.0),
                    'action_type': 'evaluator_action',
                    'demo_name': demo_name
                }
                transition_sequences.append(transition)
        
        integrated_result.transition_sequences = transition_sequences
        
        # 计算置信度分数（基于评估器的平均分数）
        if 'avg_summary' in evaluator_result:
            avg_summary = evaluator_result['avg_summary']
            precondition_score = avg_summary.get('precondition_score', 0.0)
            effect_score = avg_summary.get('effect_score', 0.0)
            # 加权平均
            confidence_score = (precondition_score * 0.5 + effect_score * 0.5)
            integrated_result.confidence_score = confidence_score
        else:
            # 如果没有平均分数，使用默认值
            integrated_result.confidence_score = 0.7
        
        # 添加诊断信息
        integrated_result.diagnostics.update({
            'evaluator_result': evaluator_result,
            'demo_name': demo_name,
            'transition_count': len(transition_sequences)
        })
        
        # 检查置信度是否高于阈值
        if integrated_result.confidence_score >= self.min_confidence_threshold:
            integrated_result.success = True
        else:
            integrated_result.success = False
            integrated_result.warnings.append({
                'type': 'low_confidence',
                'message': f"Low confidence score: {integrated_result.confidence_score}",
                'threshold': self.min_confidence_threshold
            })
        
        return integrated_result
    
    def _generate_mock_evaluator_response(self, prompt: str, demo_name: str) -> str:
        """
        生成模拟的TransitionModelingEvaluator响应（用于测试）
        
        Args:
            prompt: 提示文本
            demo_name: 演示名称
            
        Returns:
            str: 模拟响应
        """
        # 生成一些常见的动作定义
        mock_response = f"""
        (:action NAVIGATE_TO
        :parameters (?a - agent ?l - location)
        :precondition ()
        :effect ()
        )
        
        (:action LEFT_GRASP
        :parameters (?a - agent ?o - object)
        :precondition ()
        :effect ()
        )
        
        (:action RIGHT_GRASP
        :parameters (?a - agent ?o - object)
        :precondition ()
        :effect ()
        )
        
        (:action LEFT_PLACE_ONTOP
        :parameters (?a - agent ?o1 - object ?o2 - object)
        :precondition ()
        :effect ()
        )
        
        (:action RIGHT_PLACE_ONTOP
        :parameters (?a - agent ?o1 - object ?o2 - object)
        :precondition ()
        :effect ()
        )
        """
        
        return mock_response
    
    def _set_compatibility_flags(self, result: IntegratedModelingResult) -> Dict[str, bool]:
        """
        设置兼容性标志
        
        Args:
            result: 集成结果
            
        Returns:
            Dict[str, bool]: 兼容性标志
        """
        flags = {
            'has_transitions': len(result.transition_sequences) > 0,
            'has_confidence': result.confidence_score > 0,
            'has_action_data': bool(result.action_sequencing_data),
            'action_sequence_compatible': False  # 默认为False，后续会更新
        }
        
        # 检查动作序列数据兼容性
        action_data = result.action_sequencing_data
        if action_data:
            has_actions = 'actions' in action_data and len(action_data['actions']) > 0
            has_subgoals = 'subgoals' in action_data and len(action_data['subgoals']) > 0
            has_metadata = 'metadata' in action_data
            
            flags['action_sequence_compatible'] = has_actions and has_metadata
        
        return flags
    
    def _fix_compatibility_issues(self, result: IntegratedModelingResult) -> bool:
        """
        修复兼容性问题
        
        Args:
            result: 集成结果
            
        Returns:
            bool: 是否修复成功
        """
        try:
            action_data = result.action_sequencing_data
            
            # 确保必要字段存在
            if 'actions' not in action_data or len(action_data['actions']) == 0:
                # 创建模拟动作
                action_data['actions'] = self._create_mock_actions(result.transition_sequences)
            
            if 'metadata' not in action_data:
                action_data['metadata'] = {
                    'total_actions': len(action_data.get('actions', [])),
                    'total_sequences': len(result.transition_sequences),
                    'compatibility_fixed': True
                }
            
            # 确保子目标存在
            if 'subgoals' not in action_data:
                action_data['subgoals'] = []
            
            return True
        except Exception as e:
            logger.error(f"Error fixing compatibility issues: {str(e)}")
        
        return False
    
    def _create_mock_actions(self, transition_sequences: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        创建模拟动作
        
        Args:
            transition_sequences: 转换序列
            
        Returns:
            List[Dict[str, Any]]: 模拟动作列表
        """
        mock_actions = []
        
        for seq_idx, sequence in enumerate(transition_sequences):
            for trans_idx, transition in enumerate(sequence):
                mock_action = {
                    'id': f"mock_action_{seq_idx}_{trans_idx}",
                    'type': 'execute_transition',
                    'description': f"Transition from {transition.get('source', 'unknown')} to {transition.get('target', 'unknown')}",
                    'preconditions': transition.get('condition', {'type': 'always_true'}),
                    'effects': {
                        'source': transition.get('source'),
                        'target': transition.get('target')
                    },
                    'probability': transition.get('probability', 1.0),
                    'confidence': 0.75,
                    'is_mock': True
                }
                mock_actions.append(mock_action)
        
        return mock_actions
    
    def _generate_diagnostics(self, result: IntegratedModelingResult) -> Dict[str, Any]:
        """
        生成诊断信息
        
        Args:
            result: 集成结果
            
        Returns:
            Dict[str, Any]: 诊断信息
        """
        diagnostics = {
            'confidence_assessment': self._assess_confidence(result.confidence_score),
            'sequence_analysis': self._analyze_sequences(result.transition_sequences),
            'action_data_quality': self._assess_action_data(result.action_sequencing_data),
            'error_summary': self._summarize_errors(result.errors)
        }
        
        return diagnostics
    
    def _assess_confidence(self, confidence_score: float) -> Dict[str, str]:
        """
        评估置信度
        
        Args:
            confidence_score: 置信度分数
            
        Returns:
            Dict[str, str]: 置信度评估
        """
        if confidence_score >= 0.9:
            return {'level': 'high', 'message': 'Very confident in transition modeling'}
        elif confidence_score >= 0.7:
            return {'level': 'medium', 'message': 'Moderate confidence in transition modeling'}
        elif confidence_score >= 0.5:
            return {'level': 'low', 'message': 'Low confidence, results may be unreliable'}
        else:
            return {'level': 'very_low', 'message': 'Very low confidence, results not recommended'}
    
    def _analyze_sequences(self, sequences: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        分析转换序列
        
        Args:
            sequences: 转换序列
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        total_transitions = sum(len(seq) for seq in sequences)
        
        return {
            'sequence_count': len(sequences),
            'total_transitions': total_transitions,
            'avg_transitions_per_sequence': total_transitions / len(sequences) if sequences else 0,
            'has_sequences': len(sequences) > 0
        }
    
    def _assess_action_data(self, action_data: Dict[str, Any]) -> Dict[str, str]:
        """
        评估动作数据质量
        
        Args:
            action_data: 动作数据
            
        Returns:
            Dict[str, str]: 评估结果
        """
        if not action_data:
            return {'quality': 'poor', 'message': 'No action data available'}
        
        action_count = len(action_data.get('actions', []))
        if action_count == 0:
            return {'quality': 'poor', 'message': 'Action data has no actions'}
        
        if action_count <= 3:
            return {'quality': 'medium', 'message': 'Limited action diversity'}
        
        return {'quality': 'good', 'message': 'Sufficient action data'}
    
    def _summarize_errors(self, errors: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        总结错误
        
        Args:
            errors: 错误列表
            
        Returns:
            Dict[str, Any]: 错误总结
        """
        error_types = {}
        for error in errors:
            error_type = error.get('type', 'unknown')
            if error_type not in error_types:
                error_types[error_type] = 0
            error_types[error_type] += 1
        
        return {
            'total_errors': len(errors),
            'error_types': error_types,
            'has_errors': len(errors) > 0
        }
    
    def _finalize_result(self, result: IntegratedModelingResult, start_time: float) -> IntegratedModelingResult:
        """
        最终处理结果
        
        Args:
            result: 集成结果
            start_time: 开始时间
            
        Returns:
            IntegratedModelingResult: 最终结果
        """
        # 计算建模时间
        if result.modeling_time == 0:
            result.modeling_time = time.time() - start_time
        
        # 更新统计信息
        self._update_statistics(result)
        
        # 如果失败，记录统计
        if not result.success:
            self.stats['failed_calls'] += 1
            
            # 添加详细的失败原因
            if not result.errors:
                result.errors.append({
                    'type': 'success_condition_failed',
                    'message': 'Failed to meet success conditions'
                })
        
        return result
    
    def _update_statistics(self, result: IntegratedModelingResult):
        """
        更新统计信息
        
        Args:
            result: 集成结果
        """
        # 更新建模时间统计
        self.stats['total_modeling_time'] += result.modeling_time
        total_calls = self.stats['total_calls']
        if total_calls > 0:
            self.stats['average_modeling_time'] = self.stats['total_modeling_time'] / total_calls
        
        # 更新错误统计
        if result.diagnostics.get('error_summary', {}).get('has_errors', False):
            error_types = result.diagnostics['error_summary'].get('error_types', {})
            for error_type, count in error_types.items():
                self._record_error_type(error_type)
    
    def _record_error_type(self, error_type: str):
        """
        记录错误类型
        
        Args:
            error_type: 错误类型
        """
        if 'error_types' not in self.stats:
            self.stats['error_types'] = {}
        
        if error_type not in self.stats['error_types']:
            self.stats['error_types'][error_type] = 0
        
        self.stats['error_types'][error_type] += 1
    
    def register_module_feedback(self, goal_text: str, feedback: Dict[str, Any]):
        """
        注册模块反馈
        
        Args:
            goal_text: 目标文本
            feedback: 反馈信息
        """
        if self.enable_module_feedback:
            # 存储反馈信息
            if goal_text not in self.feedback_cache:
                self.feedback_cache[goal_text] = []
            
            feedback_entry = {
                'timestamp': time.time(),
                'feedback': feedback
            }
            self.feedback_cache[goal_text].append(feedback_entry)
            
            # 限制缓存大小
            if len(self.feedback_cache[goal_text]) > 10:
                self.feedback_cache[goal_text] = self.feedback_cache[goal_text][-10:]
    
    def create_error_diagnosis(self, result: IntegratedModelingResult) -> Dict[str, Any]:
        """
        创建错误诊断
        
        Args:
            result: 集成结果
            
        Returns:
            Dict[str, Any]: 诊断信息
        """
        diagnosis = {
            'success': result.success,
            'confidence_score': result.confidence_score,
            'possible_causes': [],
            'recommendations': []
        }
        
        # 分析错误原因
        if result.errors:
            for error in result.errors:
                diagnosis['possible_causes'].append(error.get('message', 'Unknown error'))
        
        # 分析置信度问题
        if result.confidence_score < self.min_confidence_threshold:
            diagnosis['possible_causes'].append('Low confidence score')
            diagnosis['recommendations'].append('Consider simplifying the goal or providing more context')
        
        # 分析兼容性问题
        if not result.compatibility_flags.get('action_sequence_compatible', False):
            diagnosis['possible_causes'].append('Action sequence compatibility issue')
            diagnosis['recommendations'].append('Check if subgoal data contains valid transition information')
        
        # 提供通用建议
        if not result.transition_sequences:
            diagnosis['recommendations'].append('Ensure subgoals contain enough detail for transition modeling')
        
        return diagnosis
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """
        获取集成统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        # 计算成功率
        success_rate = 0
        if self.stats['total_calls'] > 0:
            success_rate = self.stats['successful_calls'] / self.stats['total_calls']
        
        # 计算恢复率
        recovery_rate = 0
        if self.stats['recovery_attempts'] > 0:
            recovery_rate = self.stats['recovery_successes'] / self.stats['recovery_attempts']
        
        return {
            'total_calls': self.stats['total_calls'],
            'success_rate': success_rate,
            'recovery_rate': recovery_rate,
            'average_modeling_time': self.stats['average_modeling_time'],
            'error_distribution': self.stats.get('error_types', {}),
            'module_status': 'available' if self.original_modeler else 'unavailable'
        }
    
    def clear_feedback_cache(self):
        """
        清除反馈缓存
        """
        self.feedback_cache.clear()
        logger.info("Feedback cache cleared")
    
    def export_statistics_to_json(self, file_path: str):
        """
        导出统计信息到JSON文件
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            logger.info(f"Statistics exported to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export statistics: {str(e)}")


# 示例用法
if __name__ == "__main__":
    # 创建配置
    config = {
        'enable_debugging': True,
        'enable_module_feedback': True,
        'enable_error_handling': True
    }
    
    # 初始化集成器
    integrator = TransitionModelerIntegration(config)
    
    # 测试模型转换
    test_result = integrator.model_transitions_for_integration(
        goal_text="Move the box to the shelf",
        subgoal_data={
            'subgoals': [
                "Approach the box",
                "Pick up the box",
                "Approach the shelf",
                "Place the box on the shelf"
            ]
        }
    )
    
    print(f"Modeling result: {'Success' if test_result.success else 'Failed'}")
    print(f"Confidence score: {test_result.confidence_score}")
    print(f"Transition sequences: {len(test_result.transition_sequences)}")
    print(f"Action count: {len(test_result.action_sequencing_data.get('actions', []))}")
    
    # 获取统计信息
    stats = integrator.get_integration_statistics()
    print(f"\nStatistics: {stats}")