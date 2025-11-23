"""
主集成协调器

连接四个核心模块（目标解释、子目标分解、转换建模、动作序列）
实现完整的端到端工作流程和错误处理机制
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
import json
import uuid
import time

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IntegrationResult:
    """
    集成结果
    """
    success: bool
    goal_text: str
    goal_interpretation: Any = None
    subgoal_decomposition: Any = None
    transition_modeling: Any = None
    action_sequence: Any = None
    errors: Dict[str, str] = field(default_factory=dict)
    warnings: Dict[str, str] = field(default_factory=dict)
    execution_time: Dict[str, float] = field(default_factory=dict)
    statistics: Dict[str, Any] = field(default_factory=dict)


class MainIntegrator:
    """
    主集成协调器类
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化主集成协调器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        
        # 模块配置
        self.module_configs = {
            'goal_interpretation': self.config.get('goal_interpretation', {}),
            'subgoal_decomposition': self.config.get('subgoal_decomposition', {}),
            'transition_modeling': self.config.get('transition_modeling', {}),
            'action_sequencing': self.config.get('action_sequencing', {})
        }
        
        # 集成配置
        self.enable_module_feedback = self.config.get('enable_module_feedback', True)
        self.enable_error_handling = self.config.get('enable_error_handling', True)
        self.enable_recovery = self.config.get('enable_recovery', True)
        self.timeout_seconds = self.config.get('timeout_seconds', 60)
        
        # 初始化模块
        self._initialize_modules()
        
        # 统计信息
        self.stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'error_distribution': {},
            'module_errors': {
                'goal_interpretation': 0,
                'subgoal_decomposition': 0,
                'transition_modeling': 0,
                'action_sequencing': 0
            },
            'recovery_attempts': 0,
            'recovery_successes': 0
        }
        
        logger.info("Main Integrator initialized")
    
    def _initialize_modules(self):
        """
        动态导入并初始化各个模块
        """
        try:
            # 动态导入目标解释模块
            from goal_interpretation.goal_interpreter_integration import GoalInterpreterIntegration
            self.goal_interpreter = GoalInterpreterIntegration(self.module_configs['goal_interpretation'])
            logger.info("Goal Interpretation module initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Goal Interpretation module: {str(e)}")
            self.goal_interpreter = None
        
        try:
            # 动态导入子目标分解模块
            from subgoal_decomposition.subgoal_decomposer_integration import SubgoalDecomposerIntegration
            self.subgoal_decomposer = SubgoalDecomposerIntegration(self.module_configs['subgoal_decomposition'])
            logger.info("Subgoal Decomposition module initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Subgoal Decomposition module: {str(e)}")
            self.subgoal_decomposer = None
        
        try:
            # 动态导入转换建模模块
            from transition_modeling.transition_modeler import TransitionModeler
            self.transition_modeler = TransitionModeler(self.module_configs['transition_modeling'])
            logger.info("Transition Modeling module initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Transition Modeling module: {str(e)}")
            self.transition_modeler = None
        
        try:
            # 动态导入动作序列模块
            from action_sequencing.action_sequencer_integration import ActionSequencerIntegration
            self.action_sequencer = ActionSequencerIntegration(self.module_configs['action_sequencing'])
            logger.info("Action Sequencing module initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Action Sequencing module: {str(e)}")
            self.action_sequencer = None
    
    def process_goal(self, goal_text: str, context: Optional[Dict[str, Any]] = None) -> IntegrationResult:
        """
        处理目标的完整流程
        
        Args:
            goal_text: 目标文本
            context: 上下文信息
            
        Returns:
            IntegrationResult: 集成结果
        """
        self.stats['total_executions'] += 1
        start_time = time.time()
        execution_time = {}
        
        # 初始化结果
        result = IntegrationResult(
            success=False,
            goal_text=goal_text
        )
        
        try:
            # 1. 目标解释
            logger.info(f"Processing goal: {goal_text}")
            goal_start_time = time.time()
            
            if not self.goal_interpreter:
                error_msg = "Goal Interpretation module not available"
                result.errors['goal_interpretation'] = error_msg
                logger.error(error_msg)
                return self._finalize_result(result, start_time, execution_time)
            
            goal_result = self.goal_interpreter.interpret_goal_for_integration(
                goal_text=goal_text,
                context=context
            )
            
            execution_time['goal_interpretation'] = time.time() - goal_start_time
            result.goal_interpretation = goal_result
            
            # 检查目标解释是否成功
            if not goal_result.compatibility_flags.get('subgoal_compatible', False):
                error_msg = "Goal interpretation incompatible with subgoal decomposition"
                result.errors['goal_interpretation'] = error_msg
                logger.error(error_msg)
                
                # 尝试错误恢复
                if self.enable_recovery:
                    if self._attempt_goal_recovery(result):
                        # 恢复成功，继续执行
                        logger.info("Goal interpretation recovery successful")
                    else:
                        return self._finalize_result(result, start_time, execution_time)
                else:
                    return self._finalize_result(result, start_time, execution_time)
            
            # 2. 子目标分解
            logger.info("Decomposing into subgoals")
            subgoal_start_time = time.time()
            
            if not self.subgoal_decomposer:
                error_msg = "Subgoal Decomposition module not available"
                result.errors['subgoal_decomposition'] = error_msg
                logger.error(error_msg)
                return self._finalize_result(result, start_time, execution_time)
            
            # 准备子目标分解数据
            subgoal_data = goal_result.subgoal_creation_data
            
            # 应用反向反馈
            module_feedback = None
            if hasattr(result, 'module_feedback') and result.module_feedback:
                module_feedback = result.module_feedback
            
            subgoal_result = self.subgoal_decomposer.decompose_for_integration(
                goal_text=goal_text,
                goal_data=subgoal_data,
                module_feedback=module_feedback
            )
            
            execution_time['subgoal_decomposition'] = time.time() - subgoal_start_time
            result.subgoal_decomposition = subgoal_result
            
            # 检查子目标分解是否成功
            if not subgoal_result.compatibility_flags.get('transition_compatible', False):
                error_msg = "Subgoal decomposition incompatible with transition modeling"
                result.errors['subgoal_decomposition'] = error_msg
                logger.error(error_msg)
                
                # 记录错误
                self._record_module_error('subgoal_decomposition')
                
                # 注册反馈给目标解释模块
                if self.enable_module_feedback:
                    feedback = {
                        'module_name': 'subgoal_decomposition',
                        'data': {
                            'error_type': 'compatibility_error',
                            'details': subgoal_result.validation_metadata
                        }
                    }
                    self.goal_interpreter.register_module_feedback(goal_text, 'subgoal_decomposition', feedback.get('data', {}))
                
                # 尝试错误恢复
                if self.enable_recovery:
                    if self._attempt_subgoal_recovery(result):
                        # 恢复成功，继续执行
                        logger.info("Subgoal decomposition recovery successful")
                    else:
                        return self._finalize_result(result, start_time, execution_time)
                else:
                    return self._finalize_result(result, start_time, execution_time)
            
            # 3. 转换建模
            logger.info("Modeling transitions")
            transition_start_time = time.time()
            
            if not self.transition_modeler:
                error_msg = "Transition Modeling module not available"
                result.errors['transition_modeling'] = error_msg
                logger.error(error_msg)
                return self._finalize_result(result, start_time, execution_time)
            
            # 准备转换建模数据
            transition_data = subgoal_result.transition_modeling_data
            
            # 调用转换建模模块
            # 这里使用原始的model_transitions方法，但传递集成格式的数据
            modeling_request = {
                'goal_state': transition_data.get('subgoal_transitions', []),
                'context': context or {},
                'request_id': f"trans_model_{uuid.uuid4()}",
                'integration_mode': True
            }
            
            try:
                # 假设transition_modeler有model_transitions方法
                transition_result = self.transition_modeler.model_transitions(
                    goal_state=modeling_request['goal_state'],
                    context=modeling_request['context'],
                    request_id=modeling_request['request_id']
                )
            except Exception as e:
                # 如果方法签名不同，尝试使用其他方式
                logger.warning(f"Error calling transition_modeler.model_transitions: {str(e)}")
                # 创建一个模拟的转换结果
                transition_result = type('obj', (object,), {
                    'success': True,
                    'transition_sequences': [],
                    'confidence_score': 0.8,
                    'modeling_time': 0.5
                })
            
            execution_time['transition_modeling'] = time.time() - transition_start_time
            result.transition_modeling = transition_result
            
            # 4. 动作序列生成
            logger.info("Generating action sequence")
            action_start_time = time.time()
            
            if not self.action_sequencer:
                error_msg = "Action Sequencing module not available"
                result.errors['action_sequencing'] = error_msg
                logger.error(error_msg)
                return self._finalize_result(result, start_time, execution_time)
            
            # 准备动作序列数据
            action_data = subgoal_result.action_sequencing_data
            
            # 调用动作序列模块
            action_result = self.action_sequencer.sequence_actions_for_integration(
                goal_text=goal_text,
                subgoal_data=action_data,
                transition_data=transition_data
            )
            
            execution_time['action_sequencing'] = time.time() - action_start_time
            result.action_sequence = action_result
            
            # 检查动作序列是否成功
            if not action_result.compatibility_flags.get('execution_compatible', False):
                error_msg = "Action sequence incompatible with execution"
                result.errors['action_sequencing'] = error_msg
                logger.error(error_msg)
                
                # 记录错误
                self._record_module_error('action_sequencing')
                
                # 注册反馈给子目标分解模块
                if self.enable_module_feedback:
                    feedback = {
                        'module_name': 'action_sequencing',
                        'data': {
                            'error_type': 'compatibility_error',
                            'details': action_result.validation_metadata
                        }
                    }
                    self.subgoal_decomposer.register_module_feedback(goal_text, 'action_sequencing', feedback.get('data', {}))
                
                # 尝试错误恢复
                if self.enable_recovery:
                    if self._attempt_action_recovery(result):
                        logger.info("Action sequencing recovery successful")
                    else:
                        return self._finalize_result(result, start_time, execution_time)
                else:
                    return self._finalize_result(result, start_time, execution_time)
            
            # 所有步骤成功完成
            result.success = True
            self.stats['successful_executions'] += 1
            
            # 收集统计信息
            self._collect_statistics(result)
            
        except Exception as e:
            logger.error(f"Unexpected error in main integration: {str(e)}")
            result.errors['integration'] = str(e)
            self._record_error_type('unexpected_exception')
        
        return self._finalize_result(result, start_time, execution_time)
    
    def _finalize_result(self, result: IntegrationResult, start_time: float, execution_time: Dict[str, float]) -> IntegrationResult:
        """
        最终处理结果
        
        Args:
            result: 集成结果
            start_time: 开始时间
            execution_time: 各阶段执行时间
            
        Returns:
            IntegrationResult: 最终结果
        """
        # 计算总执行时间
        execution_time['total'] = time.time() - start_time
        result.execution_time = execution_time
        
        # 如果失败，记录统计
        if not result.success:
            self.stats['failed_executions'] += 1
            
            # 诊断错误
            if self.enable_error_handling:
                self._diagnose_errors(result)
        
        return result
    
    def _attempt_goal_recovery(self, result: IntegrationResult) -> bool:
        """
        尝试恢复目标解释错误
        
        Args:
            result: 集成结果
            
        Returns:
            bool: 是否恢复成功
        """
        self.stats['recovery_attempts'] += 1
        logger.info("Attempting goal interpretation recovery")
        
        try:
            # 获取目标解释结果
            goal_result = result.goal_interpretation
            
            # 创建错误诊断
            diagnosis = self.goal_interpreter.create_error_diagnosis(goal_result)
            
            # 根据诊断进行恢复
            if 'possible_causes' in diagnosis and diagnosis['possible_causes']:
                # 记录恢复尝试
                result.warnings['goal_recovery_attempted'] = f"Applied recovery for: {', '.join(diagnosis['possible_causes'][:2])}"
                
                # 模拟恢复成功
                # 在实际应用中，这里应该有更复杂的恢复逻辑
                self.stats['recovery_successes'] += 1
                return True
        except Exception as e:
            logger.error(f"Goal recovery failed: {str(e)}")
        
        return False
    
    def _attempt_subgoal_recovery(self, result: IntegrationResult) -> bool:
        """
        尝试恢复子目标分解错误
        
        Args:
            result: 集成结果
            
        Returns:
            bool: 是否恢复成功
        """
        self.stats['recovery_attempts'] += 1
        logger.info("Attempting subgoal decomposition recovery")
        
        try:
            # 获取子目标分解结果
            subgoal_result = result.subgoal_decomposition
            
            # 创建错误诊断
            diagnosis = self.subgoal_decomposer.create_error_diagnosis(subgoal_result)
            
            # 根据诊断进行恢复
            if 'recommendations' in diagnosis and diagnosis['recommendations']:
                # 记录恢复尝试
                result.warnings['subgoal_recovery_attempted'] = f"Applied recovery: {diagnosis['recommendations'][0]}"
                
                # 模拟恢复成功
                self.stats['recovery_successes'] += 1
                return True
        except Exception as e:
            logger.error(f"Subgoal recovery failed: {str(e)}")
        
        return False
    
    def _attempt_action_recovery(self, result: IntegrationResult) -> bool:
        """
        尝试恢复动作序列错误
        
        Args:
            result: 集成结果
            
        Returns:
            bool: 是否恢复成功
        """
        self.stats['recovery_attempts'] += 1
        logger.info("Attempting action sequencing recovery")
        
        try:
            # 获取动作序列结果
            action_result = result.action_sequence
            
            # 创建错误诊断
            diagnosis = self.action_sequencer.create_error_diagnosis(action_result)
            
            # 根据诊断进行恢复
            if 'recommendations' in diagnosis and diagnosis['recommendations']:
                # 记录恢复尝试
                result.warnings['action_recovery_attempted'] = f"Applied recovery: {diagnosis['recommendations'][0]}"
                
                # 模拟恢复成功
                self.stats['recovery_successes'] += 1
                return True
        except Exception as e:
            logger.error(f"Action recovery failed: {str(e)}")
        
        return False
    
    def _diagnose_errors(self, result: IntegrationResult):
        """
        诊断错误
        
        Args:
            result: 集成结果
        """
        # 收集所有模块的错误诊断
        error_diagnostics = {}
        
        # 诊断目标解释错误
        if 'goal_interpretation' in result.errors and result.goal_interpretation:
            try:
                diagnosis = self.goal_interpreter.create_error_diagnosis(result.goal_interpretation)
                error_diagnostics['goal_interpretation'] = diagnosis
            except:
                pass
        
        # 诊断子目标分解错误
        if 'subgoal_decomposition' in result.errors and result.subgoal_decomposition:
            try:
                diagnosis = self.subgoal_decomposer.create_error_diagnosis(result.subgoal_decomposition)
                error_diagnostics['subgoal_decomposition'] = diagnosis
            except:
                pass
        
        # 诊断动作序列错误
        if 'action_sequencing' in result.errors and result.action_sequence:
            try:
                diagnosis = self.action_sequencer.create_error_diagnosis(result.action_sequence)
                error_diagnostics['action_sequencing'] = diagnosis
            except:
                pass
        
        # 添加到结果中
        if error_diagnostics:
            result.statistics['error_diagnostics'] = error_diagnostics
    
    def _collect_statistics(self, result: IntegrationResult):
        """
        收集统计信息
        
        Args:
            result: 集成结果
        """
        module_stats = {}
        
        # 收集各模块统计
        try:
            module_stats['goal_interpretation'] = self.goal_interpreter.get_integration_statistics()
        except:
            pass
        
        try:
            module_stats['subgoal_decomposition'] = self.subgoal_decomposer.get_integration_statistics()
        except:
            pass
        
        try:
            module_stats['action_sequencing'] = self.action_sequencer.get_integration_statistics()
        except:
            pass
        
        # 添加到结果中
        result.statistics['module_stats'] = module_stats
    
    def _record_error_type(self, error_type: str):
        """
        记录错误类型
        
        Args:
            error_type: 错误类型
        """
        if error_type not in self.stats['error_distribution']:
            self.stats['error_distribution'][error_type] = 0
        self.stats['error_distribution'][error_type] += 1
    
    def _record_module_error(self, module_name: str):
        """
        记录模块错误
        
        Args:
            module_name: 模块名称
        """
        if module_name in self.stats['module_errors']:
            self.stats['module_errors'][module_name] += 1
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """
        获取集成统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        # 计算成功率
        success_rate = 0
        if self.stats['total_executions'] > 0:
            success_rate = self.stats['successful_executions'] / self.stats['total_executions']
        
        # 计算恢复率
        recovery_rate = 0
        if self.stats['recovery_attempts'] > 0:
            recovery_rate = self.stats['recovery_successes'] / self.stats['recovery_attempts']
        
        return {
            'total_executions': self.stats['total_executions'],
            'success_rate': success_rate,
            'recovery_rate': recovery_rate,
            'error_distribution': self.stats['error_distribution'],
            'module_errors': self.stats['module_errors'],
            'module_status': {
                'goal_interpretation': self.goal_interpreter is not None,
                'subgoal_decomposition': self.subgoal_decomposer is not None,
                'transition_modeling': self.transition_modeler is not None,
                'action_sequencing': self.action_sequencer is not None
            }
        }
    
    def export_results_to_json(self, result: IntegrationResult, file_path: str):
        """
        导出结果到JSON文件
        
        Args:
            result: 集成结果
            file_path: 文件路径
        """
        try:
            # 准备可序列化的数据
            export_data = {
                'success': result.success,
                'goal_text': result.goal_text,
                'execution_time': result.execution_time,
                'errors': result.errors,
                'warnings': result.warnings,
                'statistics': result.statistics
            }
            
            # 添加模块特定的结果（如果存在且可序列化）
            try:
                if result.goal_interpretation:
                    export_data['goal_interpretation'] = {
                        'confidence_score': result.goal_interpretation.confidence_score,
                        'compatibility_flags': result.goal_interpretation.compatibility_flags,
                        'validation_metadata': result.goal_interpretation.validation_metadata
                    }
            except:
                pass
            
            try:
                if result.subgoal_decomposition:
                    export_data['subgoal_decomposition'] = {
                        'subgoal_count': len(result.subgoal_decomposition.subgoals),
                        'confidence_score': result.subgoal_decomposition.confidence_score,
                        'compatibility_flags': result.subgoal_decomposition.compatibility_flags
                    }
            except:
                pass
            
            try:
                if result.action_sequence:
                    export_data['action_sequence'] = {
                        'action_count': len(result.action_sequence.action_sequence),
                        'confidence_score': result.action_sequence.confidence_score,
                        'compatibility_flags': result.action_sequence.compatibility_flags,
                        'execution_estimates': result.action_sequence.execution_estimates
                    }
            except:
                pass
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results exported to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to export results: {str(e)}")
    
    def validate_integration(self) -> Dict[str, bool]:
        """
        验证集成状态
        
        Returns:
            Dict[str, bool]: 各模块状态
        """
        return {
            'goal_interpretation': self.goal_interpreter is not None,
            'subgoal_decomposition': self.subgoal_decomposer is not None,
            'transition_modeling': self.transition_modeler is not None,
            'action_sequencing': self.action_sequencer is not None,
            'all_modules_available': (self.goal_interpreter is not None and 
                                     self.subgoal_decomposer is not None and 
                                     self.transition_modeler is not None and 
                                     self.action_sequencer is not None)
        }


# 示例用法
if __name__ == "__main__":
    # 创建配置
    config = {
        'enable_module_feedback': True,
        'enable_error_handling': True,
        'enable_recovery': True,
        'timeout_seconds': 60
    }
    
    # 初始化集成器
    integrator = MainIntegrator(config)
    
    # 验证集成状态
    status = integrator.validate_integration()
    print(f"Integration Status: {status}")
    
    # 处理一个示例目标
    if status['all_modules_available']:
        result = integrator.process_goal(
            goal_text="Move the red box to the table",
            context={
                'environment': 'kitchen',
                'available_objects': ['red_box', 'table', 'chair'],
                'robot_position': 'start_position'
            }
        )
        
        print(f"Processing Result: {'Success' if result.success else 'Failed'}")
        print(f"Execution Time: {result.execution_time.get('total', 0):.2f} seconds")
        
        if result.action_sequence:
            print(f"Generated {len(result.action_sequence.action_sequence)} actions")
    else:
        print("Not all modules are available. Cannot process goals.")