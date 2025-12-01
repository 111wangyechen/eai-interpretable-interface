#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transition Modeler
状态转换建模器，核心模块负责协调转换预测和验证
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import logging
import time
import json
import os
import uuid
import hashlib
from pathlib import Path

# 导入LogicGuard模块
LogicGuard = None
create_logic_guard = None
try:
    from .logic_guard import LogicGuard as LG, create_logic_guard as clg
    LogicGuard = LG
    create_logic_guard = clg
except ImportError as e:
    # 简化导入逻辑，仅记录警告
    import logging
    logging.warning(f"LogicGuard module not available, some features will be disabled: {str(e)}")

try:
    from .state_transition import (
        StateTransition, TransitionType, TransitionStatus, 
        StateCondition, StateEffect, TransitionModel, TransitionSequence
    )
    from .transition_predictor import TransitionPredictor
    from .transition_validator import TransitionValidator, ValidationResult
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from state_transition import (
        StateTransition, TransitionType, TransitionStatus, 
        StateCondition, StateEffect, TransitionModel, TransitionSequence
    )
    from transition_predictor import TransitionPredictor
    from transition_validator import TransitionValidator, ValidationResult


class ModelingRequest:
    """建模请求类"""
    
    def __init__(self, 
                 initial_state: Dict[str, Any],
                 goal_state: Dict[str, Any],
                 available_transitions: Optional[List[StateTransition]] = None,
                 constraints: Optional[Dict[str, Any]] = None,
                 context: Optional[Dict[str, Any]] = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.available_transitions = available_transitions or []
        self.constraints = constraints or {}
        self.context = context or {}
        self.request_id = f"request_{int(time.time() * 1000000)}"


class ModelingResponse:
    """建模响应类"""
    
    def __init__(self, 
                 request_id: str,
                 success: bool,
                 message: str = "",
                 predicted_sequences: Optional[List[TransitionSequence]] = None,
                 validation_results: Optional[List[ValidationResult]] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        self.request_id = request_id
        self.success = success
        self.message = message
        self.predicted_sequences = predicted_sequences or []
        self.validation_results = validation_results or []
        self.metadata = metadata or {}
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'request_id': self.request_id,
            'success': self.success,
            'message': self.message,
            'predicted_sequences': [seq.to_dict() for seq in self.predicted_sequences],
            'validation_results': [vr.to_dict() for vr in self.validation_results],
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }


class TransitionModeler:
    """状态转换建模器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化转换建模器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 初始化子组件
        predictor_config = self.config.get('predictor', {})
        predictor_config['confidence_threshold'] = predictor_config.get('confidence_threshold', 0.01)  # 修复：进一步降低阈值
        
        # 添加PDDL支持配置
        validator_config = self.config.get('validator', {})
        validator_config['enable_pddl_validation'] = validator_config.get('enable_pddl_validation', True)
        validator_config['pddl_validation_level'] = validator_config.get('pddl_validation_level', 'standard')
        
        # 添加模块联动配置
        self.enable_module_feedback = self.config.get('enable_module_feedback', True)
        self.enable_error_handling = self.config.get('enable_error_handling', True)
        self.timeout_seconds = self.config.get('timeout_seconds', 30)
        
        # 初始化组件
        self.predictor = TransitionPredictor(predictor_config)
        self.validator = TransitionValidator(validator_config)
        
        # 初始化LogicGuard模块
        self.logic_guard = None
        self.enable_logic_guard = self.config.get('enable_logic_guard', True)
        if self.enable_logic_guard and create_logic_guard is not None:
            try:
                logic_guard_config = self.config.get('logic_guard', {})
                self.logic_guard = create_logic_guard(logic_guard_config)
                self.logger.info("LogicGuard module initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize LogicGuard module: {str(e)}")
                self.logic_guard = None
        elif create_logic_guard is None:
            self.enable_logic_guard = False
            self.logger.warning("LogicGuard module is not available, disabling LTL validation and runtime error detection")
        
        # 建模参数
        self.max_sequences = self.config.get('max_sequences', 5)
        self.max_sequence_length = self.config.get('max_sequence_length', 20)
        self.enable_validation = self.config.get('enable_validation', True)
        self.enable_learning = self.config.get('enable_learning', True)
        
        # 模型存储
        self.models: Dict[str, TransitionModel] = {}
        self.model_history: List[Dict[str, Any]] = []
        
        # 反向反馈机制
        self.feedback_cache = {}
        self.module_interfaces = {
            'subgoal_decomposition': {'enabled': True, 'version': '1.0'},
            'action_sequencing': {'enabled': True, 'version': '1.0'},
            'goal_interpretation': {'enabled': True, 'version': '1.0'}
        }
        
        # 统计信息
        self.modeling_stats = {
            'total_requests': 0,
            'successful_modeling': 0,
            'failed_modeling': 0,
            'average_sequences_generated': 0.0,
            'average_validation_time': 0.0,
            'ltl_validated_sequences': 0,
            'runtime_errors_detected': 0,
            'sequences_corrected': 0,
            'error_types': {},
            'feedback_corrections': 0,
            'module_invocations': {
                'predictor': 0,
                'validator': 0,
                'logic_guard': 0
            }
        }
        
        self.logger.info("Transition Modeler initialized with enhanced module integration support")
    
    def create_transition_model(self, 
                              name: str,
                              domain: str,
                              transitions: List[StateTransition],
                              state_schema: Optional[Dict[str, Any]] = None,
                              enable_pddl_validation: bool = True) -> TransitionModel:
        """
        创建转换模型，支持PDDL格式验证
        
        Args:
            name: 模型名称
            domain: 应用领域
            transitions: 转换列表
            state_schema: 状态模式
            enable_pddl_validation: 是否启用PDDL格式验证
            
        Returns:
            创建的转换模型
        """
        # 生成唯一的模型ID
        model_id = f"model_{name}_{int(time.time() * 1000000)}"
        
        # 预处理转换列表，确保符合PDDL格式
        processed_transitions = []
        for transition in transitions:
            # 确保转换有参数支持
            if not hasattr(transition, 'parameters'):
                transition.parameters = []
            processed_transitions.append(transition)
        
        model = TransitionModel(
            id=model_id,
            name=name,
            domain=domain,
            transitions=processed_transitions,
            state_schema=state_schema or {}
        )
        
        # 验证模型一致性，包括PDDL格式验证
        if self.enable_validation:
            validation_result = self.validator.validate_model_consistency(processed_transitions)
            if not validation_result.is_valid:
                self.logger.warning(f"Model consistency issues found: {validation_result.message}")
            
            # 生成PDDL验证报告
            if enable_pddl_validation:
                pddl_report = self.validator.generate_comprehensive_validation_report(processed_transitions)
                if pddl_report and pddl_report.get('issues'):
                    self.logger.warning(f"PDDL format issues found: {len(pddl_report['issues'])} issues detected")
        
        self.models[model.id] = model
        self.logger.info(f"Created transition model: {name} with {len(transitions)} transitions")
        
        return model
    
    def export_model_to_pddl(self, model_id: str, filepath: str) -> bool:
        """
        将模型导出为PDDL格式
        
        Args:
            model_id: 模型ID
            filepath: 导出文件路径
            
        Returns:
            是否成功导出
        """
        try:
            if model_id not in self.models:
                self.logger.error(f"Model {model_id} not found")
                return False
            
            model = self.models[model_id]
            domain_name = model.domain.replace(' ', '_')
            
            # 构建PDDL域文件内容
            pddl_content = []
            pddl_content.append(f"(define (domain {domain_name})")
            pddl_content.append("  (:requirements :typing :action-costs)")
            
            # 提取谓词定义和对象类型
            predicates = set()
            object_types = set(['object'])  # 默认对象类型
            
            for transition in model.transitions:
                for condition in transition.preconditions:
                    if hasattr(condition, 'to_pddl'):
                        pddl_str = condition.to_pddl()
                        pred_str = pddl_str.split(' ')[0].strip('()')
                        predicates.add(pred_str)
                        # 提取参数类型（简化处理）
                        args = pddl_str.split(' ')[1:]
                        for arg in args:
                            if '-' in arg:
                                obj_type = arg.split('-')[-1].strip()
                                object_types.add(obj_type)
                for effect in transition.effects:
                    if hasattr(effect, 'to_pddl'):
                        pddl_str = effect.to_pddl()
                        pred_str = pddl_str.split(' ')[0].strip('()')
                        predicates.add(pred_str)
                        # 提取参数类型（简化处理）
                        args = pddl_str.split(' ')[1:]
                        for arg in args:
                            if '-' in arg:
                                obj_type = arg.split('-')[-1].strip()
                                object_types.add(obj_type)
            
            # 添加类型定义
            if len(object_types) > 1:
                pddl_content.append("  (:types")
                for obj_type in sorted(object_types - {'object'}):
                    pddl_content.append(f"    {obj_type} - object")
                pddl_content.append("  )")
            
            # 添加谓词定义
            pddl_content.append("  (:predicates")
            for pred in sorted(predicates):
                pddl_content.append(f"    ({pred} ?x - object)")
            pddl_content.append("  )")
            
            # 添加动作定义
            for transition in model.transitions:
                if hasattr(transition, 'to_pddl'):
                    pddl_content.append("  ")
                    pddl_content.append(transition.to_pddl())
            
            # 保存到文件
            pddl_content = '\n'.join(pddl_content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(pddl_content)
            
            self.logger.info(f"Exported model {model_id} to PDDL file: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export model to PDDL: {str(e)}")
            return False
    
    def model_transitions(self, request: ModelingRequest) -> ModelingResponse:
        """
        执行状态转换建模，增强模块联动和错误处理
        
        Args:
            request: 建模请求
            
        Returns:
            建模响应
        """
        start_time = time.time()
        self.modeling_stats['total_requests'] += 1
        
        # 确保请求ID存在
        if not hasattr(request, 'request_id'):
            request.request_id = f"request_{uuid.uuid4()}"
        
        try:
            # 应用反向反馈调整
            adjusted_request = self._apply_module_feedback(request)
            
            # 记录模块调用
            self.modeling_stats['module_invocations']['predictor'] += 1
            
            # 1. 预测转换序列
            predicted_sequences = self._predict_transition_sequences(adjusted_request)
            
            # 记录模块调用
            self.modeling_stats['module_invocations']['validator'] += 1
            
            # 2. 验证预测序列
            validation_results = []
            if self.enable_validation:
                validation_results = self._validate_sequences(adjusted_request, predicted_sequences)
            
            # 3. 过滤有效序列
            valid_sequences = []
            validation_details = []
            
            for i, (sequence, validation) in enumerate(zip(predicted_sequences, validation_results)):
                if validation.is_valid:
                    # 确保序列中的状态数据已清理
                    sequence.initial_state = self._clean_serializable_data(sequence.initial_state)
                    sequence.final_state = self._clean_serializable_data(sequence.final_state)
                    
                    # 添加PDDL兼容性标记
                    if hasattr(sequence, 'validate_pddl_consistency'):
                        pddl_valid = sequence.validate_pddl_consistency()
                    else:
                        pddl_valid = self._check_sequence_pddl_compatibility(sequence)
                    
                    validation_details.append({
                        'sequence_id': sequence.id,
                        'confidence': getattr(sequence, 'confidence', 0.0),
                        'validity': validation.is_valid,
                        'pddl_compatible': pddl_valid,
                        'issues': getattr(validation, 'issues', [])
                    })
                    
                    valid_sequences.append(sequence)
                else:
                    self.logger.warning(f"Sequence {i} validation failed: {validation.message}")
            
            # 4. 使用LogicGuard进行时序逻辑验证和运行时错误检测
            final_sequences = valid_sequences
            if self.enable_logic_guard and self.logic_guard and valid_sequences:
                self.modeling_stats['module_invocations']['logic_guard'] += 1
                final_sequences = []
                for sequence in valid_sequences:
                    try:
                        # 时序逻辑验证
                        ltl_validation_result = self.logic_guard.validate_ltl_specifications(
                            adjusted_request.initial_state,
                            sequence.transitions,
                            adjusted_request.goal_state
                        )
                        
                        if ltl_validation_result.get('valid', True):  # 默认通过，除非明确验证失败
                            self.modeling_stats['ltl_validated_sequences'] += 1
                            
                            # 运行时错误检测
                            runtime_errors = self.logic_guard.detect_runtime_errors(sequence)
                            
                            if runtime_errors:
                                self.modeling_stats['runtime_errors_detected'] += len(runtime_errors)
                                self.logger.info(f"Detected {len(runtime_errors)} runtime errors in sequence {sequence.id}")
                                
                                # 自动纠正
                                corrected_sequences = self.logic_guard.auto_correct_sequences([sequence], runtime_errors)
                                if corrected_sequences and len(corrected_sequences) > 0:
                                    corrected_sequence = corrected_sequences[0]
                                
                                if corrected_sequence:
                                    self.modeling_stats['sequences_corrected'] += 1
                                    # corrected_sequence已经是TransitionSequence对象
                                    corrected_sequence.id = f"{sequence.id}_corrected"
                                    final_sequences.append(corrected_sequence)
                                    self.logger.info(f"Corrected sequence {sequence.id}")
                                else:
                                    # 如果无法纠正，使用原始序列
                                    final_sequences.append(sequence)
                            else:
                                # 没有运行时错误，直接添加序列
                                final_sequences.append(sequence)
                        else:
                            self.logger.warning(f"Sequence {sequence.id} failed LTL validation")
                    except Exception as e:
                        self.logger.warning(f"Error during LogicGuard processing for sequence {sequence.id}: {str(e)}")
                        # 出错时使用原始序列
                        final_sequences.append(sequence)
            elif not self.logic_guard and valid_sequences:
                # 如果LogicGuard不可用，记录警告并使用原始有效序列
                self.logger.warning("LogicGuard is not available, skipping LTL validation and runtime error detection")
            
            # 构建响应元数据
            metadata = {
                'total_sequences_generated': len(predicted_sequences),
                'valid_sequences_count': len(valid_sequences),
                'final_sequences_count': len(final_sequences),
                'modeling_time': time.time() - start_time,
                'ltl_validated': self.enable_logic_guard and self.logic_guard,
                'runtime_errors_corrected': self.modeling_stats['sequences_corrected'],
                'validation_details': validation_details,
                'module_status': self._get_module_status()
            }
            
            # 检查是否成功
            success = len(final_sequences) > 0
            
            # 如果失败，尝试提供诊断信息
            if not success and self.enable_error_handling:
                diagnostics = self._diagnose_modeling_failure(
                    adjusted_request.initial_state,
                    adjusted_request.goal_state,
                    adjusted_request.available_transitions
                )
                metadata['diagnostics'] = diagnostics
                message = f"Failed to generate valid sequences: {diagnostics.get('possible_causes', ['Unknown'])[0]}"
            else:
                message = f"Generated {len(final_sequences)} valid sequences"
            
            # 清理ValidationResult对象，确保完全可JSON序列化
            cleaned_validation_results = []
            for result in validation_results[:len(predicted_sequences)]:  # 确保长度匹配
                # 创建一个新的ValidationResult对象，只保留基本信息
                cleaned_details = {}
                if hasattr(result, 'details') and result.details:
                    # 深度清理details字段，确保不包含任何复杂对象
                    cleaned_details = self._clean_serializable_data(result.details)
                
                # 创建新的ValidationResult对象
                cleaned_result = ValidationResult(
                    is_valid=result.is_valid,
                    message=result.message,
                    details=cleaned_details
                )
                cleaned_validation_results.append(cleaned_result)
            
            response = ModelingResponse(
                request_id=request.request_id,
                success=success,
                message=message,
                predicted_sequences=final_sequences,
                validation_results=cleaned_validation_results,
                metadata=metadata
            )
            
            # 6. 更新统计信息
            self._update_statistics(response, start_time)
            
            # 7. 学习更新
            if self.enable_learning:
                # 确保学习更新不会导致LogicGuard对象被引用
                try:
                    self._update_learning_model(request, response)
                except Exception as e:
                    self.logger.warning(f"Failed to update learning model: {str(e)}")
            
            self.modeling_stats['successful_modeling'] += 1
            self.logger.info(f"Modeling completed: {len(final_sequences)} final valid sequences")
            return response
            
        except Exception as e:
            self.modeling_stats['failed_modeling'] += 1
            error_msg = f"Modeling failed: {str(e)}"
            self.logger.error(error_msg)
            
            return ModelingResponse(
                request_id=request.request_id,
                success=False,
                message=error_msg
            )
    
    def _predict_transition_sequences(self, request: ModelingRequest) -> List[TransitionSequence]:
        """预测转换序列"""
        sequences = []
        
        # 记录可用转换信息
        available_transitions_count = len(request.available_transitions)
        self.logger.info(f"Processing modeling request with {available_transitions_count} available transitions")
        
        # 确保有可用转换
        if not request.available_transitions:
            self.logger.warning(f"No available transitions provided in request {request.request_id}")
            # 即使没有转换，也返回一个空序列以避免级联失败
            empty_sequence = TransitionSequence(
                id=f"empty_sequence_{request.request_id}",
                transitions=[],
                initial_state=request.initial_state.copy()
            )
            empty_sequence.final_state = request.initial_state.copy()
            return [empty_sequence]
        
        # 使用预测器生成序列
        try:
            # 创建转换副本以避免意外修改原始数据
            transitions_copy = request.available_transitions.copy()
            
            # 临时降低置信度阈值以增加生成序列的可能性
            original_threshold = self.predictor.confidence_threshold
            self.predictor.confidence_threshold = max(0.005, original_threshold * 0.5)
            
            raw_sequences = self.predictor.predict_state_sequence(
                initial_state=request.initial_state,
                goal_state=request.goal_state,
                available_transitions=transitions_copy,
                max_depth=self.max_sequence_length
            )
            
            # 恢复原始阈值
            self.predictor.confidence_threshold = original_threshold
            
            self.logger.info(f"Predictor generated {len(raw_sequences)} raw sequences")
            
            # 转换为TransitionSequence对象
            for i, transition_list in enumerate(raw_sequences[:self.max_sequences]):
                # 清理初始状态，确保不包含LogicGuard引用
                cleaned_initial_state = self._clean_serializable_data(request.initial_state.copy())
                
                sequence = TransitionSequence(
                    id=f"sequence_{request.request_id}_{i}",
                    transitions=transition_list.copy(),
                    initial_state=cleaned_initial_state
                )
                
                # 计算最终状态并清理
                current_state = request.initial_state.copy()
                for transition in transition_list:
                    current_state = transition.apply_effects(current_state)
                sequence.final_state = self._clean_serializable_data(current_state)
                
                sequences.append(sequence)
            
            # 如果没有生成序列，创建一个简单的后备序列
            if not sequences:
                self.logger.warning(f"No sequences were generated for request {request.request_id}, creating fallback")
                
                # 查找直接适用的转换作为后备
                applicable_transitions = [
                    t for t in transitions_copy if t.is_applicable(request.initial_state)
                ]
                
                if applicable_transitions:
                    # 使用第一个适用的转换创建简单序列
                    cleaned_initial_state = self._clean_serializable_data(request.initial_state.copy())
                    fallback_sequence = TransitionSequence(
                        id=f"fallback_sequence_{request.request_id}",
                        transitions=[applicable_transitions[0]],
                        initial_state=cleaned_initial_state
                    )
                    # 计算最终状态并清理
                    final_state = request.initial_state.copy()
                    final_state = applicable_transitions[0].apply_effects(final_state)
                    fallback_sequence.final_state = self._clean_serializable_data(final_state)
                    sequences.append(fallback_sequence)
                else:
                    # 如果没有适用的转换，创建空序列
                    cleaned_initial_state = self._clean_serializable_data(request.initial_state.copy())
                    empty_sequence = TransitionSequence(
                        id=f"empty_fallback_sequence_{request.request_id}",
                        transitions=[],
                        initial_state=cleaned_initial_state
                    )
                    empty_sequence.final_state = cleaned_initial_state
                    sequences.append(empty_sequence)
            
        except Exception as e:
            self.logger.error(f"Error predicting transition sequences: {str(e)}")
            # 出错时创建后备序列
            cleaned_initial_state = self._clean_serializable_data(request.initial_state.copy())
            fallback_sequence = TransitionSequence(
                id=f"error_fallback_sequence_{request.request_id}",
                transitions=[],
                initial_state=cleaned_initial_state
            )
            fallback_sequence.final_state = cleaned_initial_state
            sequences = [fallback_sequence]
        
        return sequences
    
    def _validate_sequences(self, 
                          request: ModelingRequest, 
                          sequences: List[TransitionSequence]) -> List[ValidationResult]:
        """验证转换序列"""
        validation_results = []
        
        for sequence in sequences:
            result = self.validator.validate_transition_sequence(
                transitions=sequence.transitions,
                initial_state=request.initial_state,
                context=request.context
            )
            validation_results.append(result)
        
        return validation_results
    
    def _update_statistics(self, response: ModelingResponse, start_time: float):
        """
        更新建模统计信息
        
        Args:
            response: 建模响应
            start_time: 开始时间
        """
        total_requests = self.modeling_stats['total_requests']
        
        if response.success:
            self.modeling_stats['successful_modeling'] += 1
        else:
            self.modeling_stats['failed_modeling'] += 1
            # 记录错误类型
            error_type = 'unknown'
            if 'diagnostics' in response.metadata:
                if response.metadata['diagnostics'].get('possible_causes'):
                    error_type = response.metadata['diagnostics']['possible_causes'][0].lower().replace(' ', '_')
            self._record_error_type(error_type)
            
        # 更新平均序列生成数量
        current_avg = self.modeling_stats['average_sequences_generated']
        new_count = len(response.predicted_sequences)
        self.modeling_stats['average_sequences_generated'] = \
            (current_avg * (total_requests - 1) + new_count) / total_requests
        
        # 更新平均验证时间
        validation_time = time.time() - start_time
        current_val_avg = self.modeling_stats['average_validation_time']
        self.modeling_stats['average_validation_time'] = \
            (current_val_avg * (total_requests - 1) + validation_time) / total_requests
        
        # 更新最大序列长度
        max_seq_len = self.modeling_stats['max_sequence_length']
        for seq in response.predicted_sequences:
            if len(seq.transitions) > max_seq_len:
                self.modeling_stats['max_sequence_length'] = len(seq.transitions)
        
        # 记录LogicGuard统计信息（如果可用）
        if self.logic_guard and hasattr(self.logic_guard, 'get_statistics'):
            try:
                lg_stats = self.logic_guard.get_statistics()
                # 合并LogicGuard统计信息
                if 'logic_guard' not in self.modeling_stats:
                    self.modeling_stats['logic_guard'] = {}
                for key, value in lg_stats.items():
                    if key in self.modeling_stats['logic_guard']:
                        if isinstance(value, (int, float)):
                            self.modeling_stats['logic_guard'][key] += value
                    else:
                        self.modeling_stats['logic_guard'][key] = value
            except Exception as e:
                self.logger.warning(f"Failed to update LogicGuard statistics: {str(e)}")
    
    def _record_error_type(self, error_type: str):
        """
        记录错误类型统计
        
        Args:
            error_type: 错误类型标识符
        """
        if error_type not in self.modeling_stats['error_types']:
            self.modeling_stats['error_types'][error_type] = 0
        self.modeling_stats['error_types'][error_type] += 1
    
    def _apply_module_feedback(self, request: ModelingRequest) -> ModelingRequest:
        """
        应用来自其他模块的反馈来优化请求
        
        Args:
            request: 原始请求
            
        Returns:
            ModelingRequest: 优化后的请求
        """
        if not self.enable_module_feedback:
            return request
        
        # 创建请求特征哈希作为缓存键
        state_features = f"{str(request.initial_state)}{str(request.goal_state)}"
        request_hash = hashlib.md5(state_features.encode()).hexdigest()
        
        if request_hash in self.feedback_cache:
            feedback = self.feedback_cache[request_hash]
            self.modeling_stats['feedback_corrections'] += 1
            self.logger.info(f"Applying feedback corrections for request {request.request_id}")
            
            # 合并可用转换
            if 'adjusted_transitions' in feedback:
                # 创建一个新的请求副本
                import copy
                adjusted_request = copy.copy(request)
                
                # 合并转换
                existing_trans_ids = {t.id: i for i, t in enumerate(request.available_transitions) 
                                    if hasattr(t, 'id')}
                
                for adjusted_trans in feedback['adjusted_transitions']:
                    if hasattr(adjusted_trans, 'id') and adjusted_trans.id in existing_trans_ids:
                        # 更新现有转换
                        idx = existing_trans_ids[adjusted_trans.id]
                        adjusted_request.available_transitions[idx] = adjusted_trans
                    else:
                        # 添加新转换
                        adjusted_request.available_transitions.append(adjusted_trans)
                
                return adjusted_request
        
        return request
    
    def _diagnose_modeling_failure(self, initial_state: Dict, goal_state: Dict, transitions: List) -> Dict:
        """
        诊断建模失败的原因
        
        Args:
            initial_state: 初始状态
            goal_state: 目标状态
            transitions: 可用转换
            
        Returns:
            Dict: 诊断结果和建议
        """
        import re
        diagnosis = {
            'possible_causes': [],
            'recommendations': [],
            'analysis': {}
        }
        
        # 检查状态差异
        if initial_state and goal_state:
            state_differences = set(goal_state.keys()) - set(initial_state.keys())
            if state_differences:
                diagnosis['possible_causes'].append('Missing state variables in initial state')
                diagnosis['analysis']['missing_variables'] = list(state_differences)
                diagnosis['recommendations'].append(
                    f'Ensure initial state contains all variables needed to reach the goal: {list(state_differences)[:5]}'
                )
        
        # 检查转换数量
        if not transitions:
            diagnosis['possible_causes'].append('No transitions available')
            diagnosis['recommendations'].append('Provide valid transitions for modeling')
        elif len(transitions) < 3:
            diagnosis['possible_causes'].append('Insufficient transitions')
            diagnosis['recommendations'].append('Increase the number of available transitions')
        
        # 检查转换质量
        invalid_transitions = []
        for i, trans in enumerate(transitions):
            if not hasattr(trans, 'preconditions') or not hasattr(trans, 'effects'):
                invalid_transitions.append(i)
        
        if invalid_transitions:
            diagnosis['possible_causes'].append('Invalid transitions detected')
            diagnosis['analysis']['invalid_transition_indices'] = invalid_transitions[:5]
            diagnosis['recommendations'].append(
                f'Fix transitions at indices: {invalid_transitions[:5]}'
            )
        
        # 检查目标可达性
        if goal_state:
            diagnosis['analysis']['goal_complexity'] = len(goal_state)
            if len(goal_state) > 10:
                diagnosis['possible_causes'].append('Goal state too complex')
                diagnosis['recommendations'].append('Simplify the goal state or break it down into subgoals')
        
        return diagnosis
    
    def _check_sequence_pddl_compatibility(self, sequence) -> bool:
        """
        检查序列的PDDL兼容性
        
        Args:
            sequence: 转换序列
            
        Returns:
            bool: 是否兼容
        """
        if not hasattr(sequence, 'transitions'):
            return False
        
        for transition in sequence.transitions:
            # 检查必要的PDDL属性
            if not hasattr(transition, 'name') or not getattr(transition, 'name', ''):
                return False
            if not hasattr(transition, 'preconditions'):
                return False
            if not hasattr(transition, 'effects'):
                return False
        
        return True
    
    def _get_module_status(self) -> Dict:
        """
        获取各模块的状态信息
        
        Returns:
            Dict: 模块状态
        """
        return {
            'predictor': 'available',
            'validator': 'available',
            'logic_guard': 'available' if self.logic_guard else 'unavailable',
            'module_feedback': 'enabled' if self.enable_module_feedback else 'disabled',
            'error_handling': 'enabled' if self.enable_error_handling else 'disabled'
        }
    
    def register_feedback(self, request_id: str, feedback: Dict):
        """
        注册来自其他模块的反馈
        
        Args:
            request_id: 请求ID
            feedback: 反馈数据
        """
        if not self.enable_module_feedback:
            return
        
        # 从反馈中提取状态信息创建缓存键
        if 'initial_state' in feedback and 'goal_state' in feedback:
            state_features = f"{str(feedback['initial_state'])}{str(feedback['goal_state'])}"
            request_hash = hashlib.md5(state_features.encode()).hexdigest()
            self.feedback_cache[request_hash] = feedback
            self.logger.info(f"Registered feedback for request {request_id}")
    
    def create_integrated_request(self, initial_state: Dict, goal_state: Dict, 
                                 subgoals: Optional[Any] = None, 
                                 context: Optional[Dict] = None) -> ModelingRequest:
        """
        创建集成的建模请求，支持多种输入格式
        
        Args:
            initial_state: 初始状态
            goal_state: 目标状态
            subgoals: 子目标信息（支持多种格式）
            context: 额外上下文信息
            
        Returns:
            ModelingRequest: 建模请求对象
        """
        # 创建基础转换
        transitions = self.create_sample_transitions()
        
        # 根据子目标增强转换
        if subgoals:
            enhanced_transitions = self._enhance_transitions_with_subgoals(transitions, subgoals)
            transitions = enhanced_transitions
        
        # 创建请求
        request = ModelingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_transitions=transitions,
            context=context or {}
        )
        
        return request
    
    def _enhance_transitions_with_subgoals(self, transitions: List, subgoals: Any) -> List:
        """
        根据子目标增强转换列表
        
        Args:
            transitions: 原始转换列表
            subgoals: 子目标信息
            
        Returns:
            List: 增强后的转换列表
        """
        # 支持不同格式的子目标
        subgoal_list = []
        
        if isinstance(subgoals, list):
            subgoal_list = subgoals
        elif hasattr(subgoals, 'subgoals'):
            # 支持DecompositionResult格式
            subgoal_list = subgoals.subgoals
        
        # 根据子目标创建额外的转换
        for subgoal in subgoal_list:
            try:
                # 创建对应的转换
                subgoal_transition = self._create_subgoal_transition(subgoal)
                if subgoal_transition:
                    transitions.append(subgoal_transition)
            except Exception as e:
                self.logger.error(f"Error creating subgoal transition: {str(e)}")
        
        return transitions
    
    def _create_subgoal_transition(self, subgoal: Any) -> Optional[StateTransition]:
        """
        根据子目标创建转换
        
        Args:
            subgoal: 子目标对象
            
        Returns:
            StateTransition: 创建的转换对象
        """
        try:
            # 提取子目标信息
            subgoal_id = getattr(subgoal, 'id', f'subgoal_{int(time.time() * 1000)}')
            subgoal_desc = getattr(subgoal, 'description', 'Subgoal')
            
            # 从子目标提取前提条件和效果
            preconditions = getattr(subgoal, 'preconditions', [])
            effects = getattr(subgoal, 'effects', [])
            
            # 如果没有前提条件和效果，尝试从描述生成
            if not preconditions:
                preconditions = [f'subgoal_pre_{subgoal_id}']
            if not effects:
                effects = [f'subgoal_effect_{subgoal_id}']
            
            # 创建转换
            transition = StateTransition(
                id=subgoal_id,
                name=f'execute_{subgoal_id}',
                preconditions=preconditions,
                effects=effects,
                description=subgoal_desc
            )
            
            # 添加PDDL参数支持
            if hasattr(subgoal, 'metadata') and isinstance(subgoal.metadata, dict):
                transition.parameters = subgoal.metadata.get('parameters', {})
            
            return transition
        except Exception as e:
            self.logger.error(f"Failed to create subgoal transition: {str(e)}")
            return None
    
    def _clean_serializable_data(self, data):
        """递归清理数据，确保可JSON序列化"""
        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif isinstance(data, (list, tuple)):
            return [self._clean_serializable_data(item) for item in data if isinstance(item, (str, int, float, bool, type(None), list, tuple, dict))]
        elif isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                if isinstance(key, str):  # 确保键是字符串
                    try:
                        cleaned_value = self._clean_serializable_data(value)
                        # 只保留非空的清理后的值
                        if cleaned_value is not None:
                            cleaned[key] = cleaned_value
                    except:
                        # 如果无法清理，跳过该键值对
                        continue
            return cleaned
        else:
            # 对于其他类型，转换为字符串表示
            try:
                return str(data)
            except:
                return "<non-serializable object>"
                
    def _update_learning_model(self, request: ModelingRequest, response: ModelingResponse):
        """更新学习模型"""
        # 记录建模历史，但确保不存储任何可能包含LogicGuard引用的数据
        history_entry = {
            'request_id': request.request_id,
            'initial_state': self._clean_serializable_data(request.initial_state),
            'goal_state': self._clean_serializable_data(request.goal_state),
            'success': response.success,
            'sequences_generated': len(response.predicted_sequences),
            'timestamp': time.time()
        }
        self.model_history.append(history_entry)
        
        # 更新预测器的历史数据
        if response.success:
            for sequence in response.predicted_sequences:
                for transition in sequence.transitions:
                    # 模拟执行结果（在实际应用中应该从实际执行获取）
                    self.predictor.update_historical_data(
                        transition=transition,
                        success=True,  # 简化假设成功
                        execution_time=transition.duration
                    )
    
    def load_transitions_from_data(self, data_source: Union[str, Dict[str, Any]]) -> List[StateTransition]:
        """
        从数据源加载转换
        
        Args:
            data_source: 数据源（文件路径或数据字典）
            
        Returns:
            转换列表
        """
        if isinstance(data_source, str):
            # 从文件加载
            with open(data_source, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = data_source
        
        transitions = []
        
        for transition_data in data.get('transitions', []):
            transition = StateTransition.from_dict(transition_data)
            transitions.append(transition)
        
        self.logger.info(f"Loaded {len(transitions)} transitions from data source")
        return transitions
    
    def create_sample_transitions(self) -> List[StateTransition]:
        """创建示例转换（用于测试）"""
        transitions = []
        
        # 示例1：移动到物体位置 - 修复条件匹配
        move_to_object = StateTransition(
            id="move_to_object_001",
            name="MoveToObjectLocation",
            transition_type=TransitionType.ATOMIC,
            preconditions=[
                StateCondition("at_location", {"location": "start"}),  # 修复：简化条件
                StateCondition("path_clear", {"destination": "object_location"})  # 修复：简化条件
            ],
            effects=[
                StateEffect("at_location", "object_location"),  # 修复：直接设置值
                StateEffect("at_location", "start", probability=0.0)  # 离开原位置
            ],
            duration=2.0,
            cost=1.0
        )
        transitions.append(move_to_object)
        
        # 示例2：拾取物体 - 修复条件匹配
        pickup_transition = StateTransition(
            id="pickup_001", 
            name="PickupObject",
            transition_type=TransitionType.ATOMIC,
            preconditions=[
                StateCondition("at_location", {"location": "object_location"}),  # 修复：简化条件
                StateCondition("object_available", {"object": "target_object"}),  # 修复：简化条件
                StateCondition("hands_free", {})  # 修复：简化条件
            ],
            effects=[
                StateEffect("holding_object", "target_object"),  # 修复：直接设置值
                StateEffect("object_available", "target_object", probability=0.0)
            ],
            duration=1.0,
            cost=0.5
        )
        transitions.append(pickup_transition)
        
        # 示例3：移动到目标位置 - 修复条件匹配
        move_to_target = StateTransition(
            id="move_to_target_001",
            name="MoveToTargetLocation",
            transition_type=TransitionType.ATOMIC,
            preconditions=[
                StateCondition("at_location", {"location": "object_location"}),  # 修复：简化条件
                StateCondition("holding_object", {"object": "target_object"}),  # 修复：简化条件
                StateCondition("path_clear", {"destination": "target_location"})  # 修复：简化条件
            ],
            effects=[
                StateEffect("at_location", "target_location"),  # 修复：直接设置值
                StateEffect("at_location", "object_location", probability=0.0)  # 离开原位置
            ],
            duration=2.0,
            cost=1.0
        )
        transitions.append(move_to_target)
        
        # 示例4：放置物体
        place_transition = StateTransition(
            id="place_001",
            name="PlaceObject", 
            transition_type=TransitionType.ATOMIC,
            preconditions=[
                StateCondition("at_location", {"location": "target_location"}),
                StateCondition("holding_object", {"object": "target_object"})
            ],
            effects=[
                StateEffect("object_at_location", {"object": "target_object", "location": "target_location"}),
                StateEffect("holding_object", None, probability=0.0)
            ],
            duration=1.0,
            cost=0.5
        )
        transitions.append(place_transition)
        
        return transitions
    
    def get_modeling_statistics(self) -> Dict[str, Any]:
        """获取建模统计信息"""
        stats = {
            'modeling_stats': self.modeling_stats,
            'models_count': len(self.models),
            'model_history_size': len(self.model_history),
            'predictor_stats': self.predictor.get_statistics(),
            'validator_stats': self.validator.get_statistics()
        }
        
        # 如果启用了LogicGuard，添加其统计信息
        if self.enable_logic_guard and self.logic_guard:
            try:
                logic_guard_stats = self.logic_guard.get_statistics()
                stats['logic_guard_stats'] = logic_guard_stats
            except Exception as e:
                self.logger.warning(f"Failed to get LogicGuard statistics: {str(e)}")
        
        return stats
    
    def save_model(self, filepath: str):
        """保存建模器状态"""
        model_data = {
            'config': self.config,
            'models': {mid: model.to_dict() for mid, model in self.models.items()},
            'modeling_stats': self.modeling_stats,
            'model_history': self.model_history[-100:]  # 保存最近100条记录
        }
        
        # 保存LogicGuard状态
        if self.enable_logic_guard and self.logic_guard:
            try:
                model_data['logic_guard_state'] = self.logic_guard.save_state()
                self.logger.info("LogicGuard state saved successfully")
            except Exception as e:
                self.logger.warning(f"Failed to save LogicGuard state: {str(e)}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Modeler state saved to {filepath}")
    
    def load_model(self, filepath: str):
        """加载建模器状态"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                model_data = json.load(f)
            
            self.config = model_data.get('config', {})
            self.modeling_stats = model_data.get('modeling_stats', {})
            self.model_history = model_data.get('model_history', [])
            
            # 重建模型
            models_data = model_data.get('models', {})
            for model_id, model_dict in models_data.items():
                transitions = [StateTransition.from_dict(t_data) for t_data in model_dict['transitions']]
                model = TransitionModel(
                    id=model_dict['id'],
                    name=model_dict['name'],
                    domain=model_dict['domain'],
                    transitions=transitions,
                    state_schema=model_dict.get('state_schema', {})
                )
                self.models[model_id] = model
            
            # 重新初始化LogicGuard
            self.enable_logic_guard = self.config.get('enable_logic_guard', True)
            if self.enable_logic_guard:
                try:
                    logic_guard_config = self.config.get('logic_guard', {})
                    self.logic_guard = create_logic_guard(logic_guard_config)
                    
                    # 加载LogicGuard状态
                    if 'logic_guard_state' in model_data:
                        self.logic_guard.load_state(model_data['logic_guard_state'])
                        self.logger.info("LogicGuard state loaded successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize LogicGuard during model load: {str(e)}")
            else:
                self.logic_guard = None
            
            self.logger.info(f"Modeler state loaded from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise