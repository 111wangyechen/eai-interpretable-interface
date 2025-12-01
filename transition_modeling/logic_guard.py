#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LogicGuard模块
基于时序逻辑的状态转换错误检测与纠正
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import logging
import time
import re

# 尝试相对导入，如果失败则使用绝对导入
try:
    from .state_transition import StateTransition, TransitionSequence, StateCondition, StateEffect
    from .transition_validator import ValidationResult
    from .transition_predictor import TransitionPredictor
except ImportError:
    from state_transition import StateTransition, TransitionSequence, StateCondition, StateEffect
    from transition_validator import ValidationResult
    from transition_predictor import TransitionPredictor


class LTLSpecification:
    """LTL规范类"""
    
    def __init__(self, name: str, formula: str, priority: str = "medium"):
        self.name = name
        self.formula = formula
        self.priority = priority
        self.violations = []
    
    def add_violation(self, step: int, state: Dict[str, Any], message: str):
        """添加违反记录"""
        self.violations.append({
            'step': step,
            'state': state,
            'message': message,
            'timestamp': time.time()
        })
    
    def is_satisfied(self) -> bool:
        """检查是否满足"""
        return len(self.violations) == 0


class RuntimeErrorInfo:
    """运行时错误信息"""
    
    def __init__(self, error_type: str, step: int, state: Dict[str, Any], transition: Optional[StateTransition] = None):
        self.error_type = error_type
        self.step = step
        self.state = state
        self.transition = transition
        self.timestamp = time.time()
        # 明确初始化所有依赖属性
        self.severity = "medium"  # 错误严重性：low, medium, high
        self.correction_applied = False  # 是否已应用纠正
        self.correction_strategy = None  # 应用的纠正策略
        self.correction_result = None  # 纠正结果：success, failure, partial


class CorrectionStrategy:
    """纠正策略基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def apply(self, error: RuntimeErrorInfo, sequence: TransitionSequence) -> TransitionSequence:
        """应用纠正策略"""
        raise NotImplementedError("Subclasses must implement apply method")


class StateRecoveryStrategy(CorrectionStrategy):
    """状态恢复策略"""
    
    def __init__(self):
        super().__init__("state_recovery")
    
    def apply(self, error: RuntimeErrorInfo, sequence: TransitionSequence) -> TransitionSequence:
        """应用状态恢复"""
        # 创建新的纠正序列
        corrected_transitions = []
        
        # 添加原始序列中错误之前的转换
        for t in sequence.transitions[:error.step]:
            corrected_transitions.append(t)
        
        # 添加恢复转换
        recovery_transition = StateTransition(
            id=f"recovery_{error.error_type}_{int(time.time())}",
            name="StateRecovery",
            transition_type="recovery",
            preconditions=[StateCondition("error_detected", {"type": error.error_type})],
            effects=[StateEffect("error_state", False)],
            duration=1.0,
            cost=5.0  # 恢复操作成本较高
        )
        corrected_transitions.append(recovery_transition)
        
        # 复制剩余的转换
        for t in sequence.transitions[error.step:]:
            corrected_transitions.append(t)
        
        # 创建新的序列
        corrected_sequence = TransitionSequence(
            id=f"{sequence.id}_corrected",
            transitions=corrected_transitions,
            initial_state=sequence.initial_state
        )
        
        return corrected_sequence


class ActionReplanningStrategy(CorrectionStrategy):
    """动作重新规划策略"""
    
    def __init__(self):
        super().__init__("action_replanning")
    
    def apply(self, error: RuntimeErrorInfo, sequence: TransitionSequence) -> TransitionSequence:
        """应用动作重新规划"""
        # 创建新的纠正序列
        corrected_transitions = []
        
        # 添加原始序列中错误之前的转换
        for t in sequence.transitions[:error.step]:
            corrected_transitions.append(t)
        
        # 如果有错误的转换，尝试替换它
        if error.transition:
            # 创建替代转换（这里是简化的实现）
            replanned_transition = StateTransition(
                id=f"replanned_{error.transition.id}_{int(time.time())}",
                name=f"Replanned_{error.transition.name}",
                transition_type=error.transition.transition_type,
                preconditions=[StateCondition("replanning_needed", {"original_transition": error.transition.id})],
                effects=error.transition.effects.copy(),
                duration=error.transition.duration * 1.2,  # 增加一点持续时间
                cost=error.transition.cost * 1.5  # 增加一点成本
            )
            corrected_transitions.append(replanned_transition)
        
        # 复制剩余的转换
        for t in sequence.transitions[error.step + 1:]:
            corrected_transitions.append(t)
        
        # 创建新的序列
        corrected_sequence = TransitionSequence(
            id=f"{sequence.id}_replanned",
            transitions=corrected_transitions,
            initial_state=sequence.initial_state
        )
        
        return corrected_sequence


class LogicGuard:
    """LogicGuard主类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化LogicGuard
        
        Args:
            config: 配置参数
        """
        # 明确初始化所有依赖属性
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 基本配置参数
        self.enabled = self.config.get('enabled', True)
        self.model_path = self.config.get('model_path', './models/logic_guard')
        self.enable_logging = self.config.get('enable_logging', True)
        
        # LTL验证配置
        ltl_config = self.config.get('ltl_verification', {})
        self.ltl_enabled = ltl_config.get('enabled', True)
        self.ltl_specifications = []
        
        # 运行时检测配置
        runtime_config = self.config.get('runtime_detection', {})
        self.runtime_enabled = runtime_config.get('enabled', True)
        self.detection_interval = runtime_config.get('detection_interval', 0.1)
        self.error_types = runtime_config.get('error_types', [
            'precondition_failure', 'effect_conflict', 'invalid_state', 'cycle_detected'
        ])
        
        # 自动纠正配置
        correction_config = self.config.get('auto_correction', {})
        self.correction_enabled = correction_config.get('enabled', True)
        self.correction_strategies = correction_config.get('correction_strategies', [
            'state_recovery', 'action_replanning'
        ])
        self.max_correction_attempts = correction_config.get('max_correction_attempts', 3)
        
        # 初始化纠正策略
        self.strategy_instances = {
            'state_recovery': StateRecoveryStrategy(),
            'action_replanning': ActionReplanningStrategy()
        }
        
        # 初始化LTL规范
        if self.ltl_enabled:
            for spec_config in ltl_config.get('specifications', []):
                spec = LTLSpecification(
                    name=spec_config['name'],
                    formula=spec_config['formula'],
                    priority=spec_config.get('priority', 'medium')
                )
                self.ltl_specifications.append(spec)
        
        # 统计信息
        self.stats = {
            'ltl_verifications': 0,
            'ltl_violations': 0,
            'runtime_errors_detected': 0,
            'corrections_applied': 0,
            'correction_success': 0,
            'correction_failure': 0,
            'partial_corrections': 0,  # 新增：部分纠正计数
            'error_types': defaultdict(int),  # 新增：按错误类型统计
            'strategy_usage': defaultdict(int)  # 新增：纠正策略使用统计
        }
        
        if self.enable_logging:
            self.logger.info("LogicGuard initialized")
    
    def extract_ltl_specifications(self, context: Dict[str, Any]) -> List[LTLSpecification]:
        """
        从上下文提取LTL规范
        
        Args:
            context: 上下文信息
            
        Returns:
            LTL规范列表
        """
        # 返回预定义的规范，实际应用中可以从上下文动态提取
        return self.ltl_specifications.copy()
    
    def validate_with_ltl(self, sequence: TransitionSequence, specifications: List[LTLSpecification]) -> Dict[str, bool]:
        """
        使用LTL验证序列
        
        Args:
            sequence: 转换序列
            specifications: LTL规范列表
            
        Returns:
            验证结果字典
        """
        self.stats['ltl_verifications'] += 1
        results = {}
        
        # 简化的LTL验证实现
        # 实际应用中应该使用专门的LTL验证器
        current_state = sequence.initial_state.copy()
        
        for step, transition in enumerate(sequence.transitions):
            # 应用转换效果
            next_state = transition.apply_effects(current_state)
            
            # 验证每个规范
            for spec in specifications:
                # 这里是简化的验证逻辑
                # 实际应用中应该使用LTL模型检查器
                is_satisfied = self._check_formula(spec.formula, current_state, next_state, step)
                
                if not is_satisfied:
                    spec.add_violation(
                        step=step,
                        state=current_state,
                        message=f"LTL violation at step {step}: {spec.formula}"
                    )
                    self.stats['ltl_violations'] += 1
                
                results[spec.name] = spec.is_satisfied()
            
            current_state = next_state
        
        return results
    
    def _check_formula(self, formula: str, current_state: Dict[str, Any], next_state: Dict[str, Any], step: int) -> bool:
        """
        简化的公式检查
        
        Args:
            formula: LTL公式
            current_state: 当前状态
            next_state: 下一个状态
            step: 当前步骤
            
        Returns:
            是否满足
        """
        # 简化的检查逻辑
        # 检查安全性公式: G not (error_state)
        if 'G not (error_state)' in formula:
            return not current_state.get('error_state', False)
        
        # 其他简化的检查...
        return True
    
    def detect_runtime_errors(self, sequence: TransitionSequence) -> List[RuntimeErrorInfo]:
        """
        检测运行时错误
        
        Args:
            sequence: 转换序列
            
        Returns:
            错误信息列表
        """
        errors = []
        current_state = sequence.initial_state.copy()
        
        for step, transition in enumerate(sequence.transitions):
            # 检查前提条件
            if 'precondition_failure' in self.error_types:
                for condition in transition.preconditions:
                    if not self._check_condition(condition, current_state):
                        error = RuntimeErrorInfo(
                            error_type='precondition_failure',
                            step=step,
                            state=current_state,
                            transition=transition
                        )
                        errors.append(error)
                        self.stats['runtime_errors_detected'] += 1
            
            # 检查其他错误类型
            # ...
            
            # 应用转换效果
            current_state = transition.apply_effects(current_state)
        
        return errors
    
    def _check_condition(self, condition: StateCondition, state: Dict[str, Any]) -> bool:
        """
        检查条件是否满足
        
        Args:
            condition: 状态条件
            state: 当前状态
            
        Returns:
            是否满足
        """
        # 简化的条件检查
        if condition.name in state:
            if isinstance(condition.value, dict):
                # 检查字典值的部分匹配
                state_value = state.get(condition.name, {})
                if isinstance(state_value, dict):
                    for k, v in condition.value.items():
                        if state_value.get(k) != v:
                            return False
                    return True
            else:
                # 直接值比较
                return state.get(condition.name) == condition.value
        
        return False
    
    def auto_correct_sequences(self, sequences: List[TransitionSequence], errors: List[RuntimeErrorInfo]) -> List[TransitionSequence]:
        """
        自动纠正序列，添加详细的纠正效果评估
        
        Args:
            sequences: 原始序列
            errors: 检测到的错误
            
        Returns:
            纠正后的序列
        """
        if not self.correction_enabled or not errors:
            return sequences
        
        corrected_sequences = []
        
        for sequence in sequences:
            current_sequence = sequence
            correction_attempts = 0
            
            # 尝试纠正每个错误
            for error in errors:
                if correction_attempts >= self.max_correction_attempts:
                    break
                
                # 应用每个策略
                for strategy_name in self.correction_strategies:
                    if strategy_name in self.strategy_instances:
                        strategy = self.strategy_instances[strategy_name]
                        try:
                            corrected_sequence = strategy.apply(error, current_sequence)
                            
                            # 验证纠正结果
                            validation = self._validate_correction(corrected_sequence, error)
                            
                            if validation['success']:
                                current_sequence = corrected_sequence
                                self.stats['correction_success'] += 1
                                self.stats['strategy_usage'][strategy_name] += 1
                                
                                # 更新错误信息
                                error.correction_applied = True
                                error.correction_strategy = strategy_name
                                error.correction_result = "success"
                                
                                if self.enable_logging:
                                    self.logger.info(f"Correction successful using {strategy_name}: {validation['message']}")
                                break
                            elif validation['confidence'] > 0.5:
                                # 部分成功，接受纠正
                                current_sequence = corrected_sequence
                                self.stats['partial_corrections'] += 1
                                self.stats['strategy_usage'][strategy_name] += 1
                                
                                # 更新错误信息
                                error.correction_applied = True
                                error.correction_strategy = strategy_name
                                error.correction_result = "partial"
                                
                                if self.enable_logging:
                                    self.logger.info(f"Partial correction using {strategy_name}: {validation['message']}")
                                break
                            else:
                                self.stats['correction_failure'] += 1
                                
                                # 更新错误信息
                                error.correction_applied = True
                                error.correction_strategy = strategy_name
                                error.correction_result = "failure"
                                
                                if self.enable_logging:
                                    self.logger.warning(f"Correction failed using {strategy_name}: {validation['message']}")
                        except Exception as e:
                            if self.enable_logging:
                                self.logger.error(f"Correction failed: {e}")
                            self.stats['correction_failure'] += 1
                            
                            # 更新错误信息
                            error.correction_applied = True
                            error.correction_strategy = strategy_name
                            error.correction_result = "failure"
                
                correction_attempts += 1
            
            corrected_sequences.append(current_sequence)
        
        return corrected_sequences
    
    def _validate_correction(self, sequence: TransitionSequence, error: RuntimeErrorInfo) -> Dict[str, Any]:
        """
        验证纠正结果，添加详细的纠正效果评估
        
        Args:
            sequence: 纠正后的序列
            error: 原始错误
            
        Returns:
            纠正效果评估结果，包含success, confidence, message等
        """
        # 详细的纠正效果评估
        correction_result = {
            'success': False,
            'confidence': 0.0,
            'message': "Correction validation failed",
            'issues': [],
            'timestamp': time.time()
        }
        
        try:
            # 1. 验证序列的基本有效性
            if not sequence.is_valid_sequence():
                correction_result['message'] = "Corrected sequence is invalid"
                correction_result['issues'].append("Invalid sequence structure")
                return correction_result
            
            # 2. 验证原始错误是否已解决
            errors_after_correction = self.detect_runtime_errors(sequence)
            original_error_still_exists = any(
                e.error_type == error.error_type and e.step == error.step
                for e in errors_after_correction
            )
            
            if original_error_still_exists:
                correction_result['message'] = "Original error still exists"
                correction_result['issues'].append(f"Error {error.error_type} still present at step {error.step}")
                return correction_result
            
            # 3. 验证没有引入新的严重错误
            new_severe_errors = [
                e for e in errors_after_correction 
                if e.step >= error.step and "high" in str(e)
            ]
            
            if new_severe_errors:
                correction_result['message'] = "New severe errors introduced"
                for e in new_severe_errors:
                    correction_result['issues'].append(f"New error {e.error_type} at step {e.step}")
                return correction_result
            
            # 4. 评估纠正效果
            current_state = sequence.initial_state.copy()
            for step, transition in enumerate(sequence.transitions[:error.step + 1]):
                current_state = transition.apply_effects(current_state)
            
            # 计算纠正后的状态质量
            state_quality = self._evaluate_state_quality(current_state)
            
            # 计算成功置信度
            confidence = 0.8  # 基础置信度
            if len(errors_after_correction) == 0:
                confidence = 1.0
            elif len(errors_after_correction) < len(self.detect_runtime_errors(sequence)):
                confidence = 0.6
            
            correction_result.update({
                'success': True,
                'confidence': confidence,
                'message': "Correction validated successfully",
                'state_quality': state_quality,
                'remaining_errors': len(errors_after_correction)
            })
            
        except Exception as e:
            correction_result['message'] = f"Validation error: {str(e)}"
            correction_result['issues'].append(f"Exception during validation: {str(e)}")
        
        return correction_result
    
    def _evaluate_state_quality(self, state: Dict[str, Any]) -> float:
        """
        评估状态质量，用于纠正效果评估
        
        Args:
            state: 当前状态
            
        Returns:
            状态质量分数 (0.0 - 1.0)
        """
        # 简化的状态质量评估
        quality = 1.0
        
        # 检查是否存在错误状态
        if state.get('error_state', False):
            quality -= 0.5
        
        # 检查关键属性是否存在
        key_properties = ['status', 'position', 'temperature']
        for prop in key_properties:
            if prop not in state:
                quality -= 0.1
        
        return max(0.0, min(1.0, quality))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics information
        
        Returns:
            Dictionary containing statistics information
        """
        return self.stats.copy()
    
    def validate_ltl_specifications(self, initial_state: Dict[str, Any], 
                                   transitions: List[StateTransition], 
                                   goal_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate state transition sequences using LTL specifications
        
        Args:
            initial_state: Initial state
            transitions: List of state transitions
            goal_state: Goal state
            
        Returns:
            Dictionary containing validation results and detailed information
        """
        try:
            # Create a TransitionSequence object from the input parameters
            sequence = TransitionSequence(
                id="validation_sequence",
                initial_state=initial_state,
                transitions=transitions,
                goal_state=goal_state
            )
            
            # Get the LTL specifications
            specifications = self.extract_ltl_specifications({})
            
            # Validate using the existing validate_with_ltl method
            validation_results = self.validate_with_ltl(sequence, specifications)
            
            # Collect detailed information about each specification
            detailed_specs = []
            for spec in specifications:
                spec_info = {
                    'name': spec.name,
                    'formula': spec.formula,
                    'priority': spec.priority,
                    'satisfied': validation_results.get(spec.name, True),
                    'violations': [
                        {
                            'step': v['step'],
                            'state': v['state'],
                            'message': v['message'],
                            'timestamp': v['timestamp']
                        } for v in spec.violations
                    ]
                }
                detailed_specs.append(spec_info)
            
            # Construct the result dictionary
            result = {
                'valid': all(validation_results.values()) if validation_results else True,
                'specifications': detailed_specs,
                'total_verifications': self.stats['ltl_verifications'],
                'total_violations': self.stats['ltl_violations'],
                'timestamp': time.time()
            }
            
            if self.enable_logging:
                self.logger.info(f"LTL validation completed: valid={result['valid']}, specs_checked={len(specifications)}")
            
            return result
            
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Error during LTL validation: {str(e)}")
            
            # Return a failure result
            return {
                'valid': False,
                'specifications': [],
                'total_verifications': self.stats['ltl_verifications'],
                'total_violations': self.stats['ltl_violations'],
                'error': str(e),
                'timestamp': time.time()
            }
    
    def clear_cache(self):
        """清除缓存"""
        # 重置统计信息
        self.stats = {
            'ltl_verifications': 0,
            'ltl_violations': 0,
            'runtime_errors_detected': 0,
            'corrections_applied': 0,
            'correction_success': 0,
            'correction_failure': 0
        }
        
        # 清除违反记录
        for spec in self.ltl_specifications:
            spec.violations.clear()


def create_logic_guard(config: Optional[Dict[str, Any]] = None) -> LogicGuard:
    """
    创建LogicGuard实例
    
    Args:
        config: 配置参数
        
    Returns:
        LogicGuard实例
    """
    try:
        return LogicGuard(config)
    except Exception as e:
        logging.error(f"Failed to create LogicGuard: {e}")
        # 返回基本实例
        return LogicGuard({})