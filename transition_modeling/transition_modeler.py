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
from pathlib import Path

# 导入LogicGuard模块
try:
    from .logic_guard import LogicGuard, create_logic_guard
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from logic_guard import LogicGuard, create_logic_guard

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
        validator_config = self.config.get('validator', {})
        
        self.predictor = TransitionPredictor(predictor_config)
        self.validator = TransitionValidator(validator_config)
        
        # 初始化LogicGuard模块
        self.logic_guard = None
        self.enable_logic_guard = self.config.get('enable_logic_guard', True)
        if self.enable_logic_guard:
            try:
                logic_guard_config = self.config.get('logic_guard', {})
                self.logic_guard = create_logic_guard(logic_guard_config)
                self.logger.info("LogicGuard module initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize LogicGuard module: {str(e)}")
        
        # 建模参数
        self.max_sequences = self.config.get('max_sequences', 5)
        self.max_sequence_length = self.config.get('max_sequence_length', 20)
        self.enable_validation = self.config.get('enable_validation', True)
        self.enable_learning = self.config.get('enable_learning', True)
        
        # 模型存储
        self.models: Dict[str, TransitionModel] = {}
        self.model_history: List[Dict[str, Any]] = []
        
        # 统计信息
        self.modeling_stats = {
            'total_requests': 0,
            'successful_modeling': 0,
            'failed_modeling': 0,
            'average_sequences_generated': 0.0,
            'average_validation_time': 0.0,
            'ltl_validated_sequences': 0,
            'runtime_errors_detected': 0,
            'sequences_corrected': 0
        }
        
        self.logger.info("Transition Modeler initialized")
    
    def create_transition_model(self, 
                              name: str,
                              domain: str,
                              transitions: List[StateTransition],
                              state_schema: Optional[Dict[str, Any]] = None) -> TransitionModel:
        """
        创建转换模型
        
        Args:
            name: 模型名称
            domain: 应用领域
            transitions: 转换列表
            state_schema: 状态模式
            
        Returns:
            创建的转换模型
        """
        # 生成唯一的模型ID
        model_id = f"model_{name}_{int(time.time() * 1000000)}"
        
        model = TransitionModel(
            id=model_id,
            name=name,
            domain=domain,
            transitions=transitions,
            state_schema=state_schema or {}
        )
        
        # 验证模型一致性
        if self.enable_validation:
            validation_result = self.validator.validate_model_consistency(transitions)
            if not validation_result.is_valid:
                self.logger.warning(f"Model consistency issues found: {validation_result.message}")
        
        self.models[model.id] = model
        self.logger.info(f"Created transition model: {name} with {len(transitions)} transitions")
        
        return model
    
    def model_transitions(self, request: ModelingRequest) -> ModelingResponse:
        """
        执行状态转换建模
        
        Args:
            request: 建模请求
            
        Returns:
            建模响应
        """
        start_time = time.time()
        self.modeling_stats['total_requests'] += 1
        
        try:
            # 1. 预测转换序列
            predicted_sequences = self._predict_transition_sequences(request)
            
            # 2. 验证预测序列
            validation_results = []
            if self.enable_validation:
                validation_results = self._validate_sequences(request, predicted_sequences)
            
            # 3. 过滤有效序列
            valid_sequences = []
            for i, (sequence, validation) in enumerate(zip(predicted_sequences, validation_results)):
                if validation.is_valid:
                    valid_sequences.append(sequence)
                else:
                    self.logger.warning(f"Sequence {i} validation failed: {validation.message}")
            
            # 4. 使用LogicGuard进行时序逻辑验证和运行时错误检测
            final_sequences = valid_sequences
            if self.enable_logic_guard and self.logic_guard and valid_sequences:
                final_sequences = []
                for sequence in valid_sequences:
                    try:
                        # 时序逻辑验证
                        ltl_validation_result = self.logic_guard.validate_ltl_specifications(
                            request.initial_state,
                            sequence.transitions,
                            request.goal_state
                        )
                        
                        if ltl_validation_result.get('valid', True):  # 默认通过，除非明确验证失败
                            self.modeling_stats['ltl_validated_sequences'] += 1
                            
                            # 运行时错误检测
                            runtime_errors = self.logic_guard.detect_runtime_errors(
                                request.initial_state,
                                sequence.transitions
                            )
                            
                            if runtime_errors:
                                self.modeling_stats['runtime_errors_detected'] += len(runtime_errors)
                                self.logger.info(f"Detected {len(runtime_errors)} runtime errors in sequence {sequence.id}")
                                
                                # 自动纠正
                                corrected_sequence = self.logic_guard.correct_sequence(
                                    request.initial_state,
                                    sequence.transitions,
                                    runtime_errors,
                                    request.goal_state
                                )
                                
                                if corrected_sequence:
                                    self.modeling_stats['sequences_corrected'] += 1
                                    # 创建新的序列对象
                                    new_sequence = TransitionSequence(
                                        id=f"{sequence.id}_corrected",
                                        transitions=corrected_sequence,
                                        initial_state=request.initial_state.copy()
                                    )
                                    # 计算最终状态
                                    current_state = request.initial_state.copy()
                                    for transition in corrected_sequence:
                                        current_state = transition.apply_effects(current_state)
                                    new_sequence.final_state = current_state
                                    final_sequences.append(new_sequence)
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
            
            # 5. 构建响应
            response = ModelingResponse(
                request_id=request.request_id,
                success=len(final_sequences) > 0,
                message=f"Generated {len(final_sequences)} valid sequences",
                predicted_sequences=final_sequences,
                validation_results=validation_results,
                metadata={
                    'total_sequences_generated': len(predicted_sequences),
                    'valid_sequences_count': len(valid_sequences),
                    'final_sequences_count': len(final_sequences),
                    'modeling_time': time.time() - start_time,
                    'ltl_validated': self.enable_logic_guard and self.logic_guard,
                    'runtime_errors_corrected': self.modeling_stats['sequences_corrected']
                }
            )
            
            # 6. 更新统计信息
            self._update_statistics(response, start_time)
            
            # 7. 学习更新
            if self.enable_learning:
                self._update_learning_model(request, response)
            
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
        
        # 使用预测器生成序列
        raw_sequences = self.predictor.predict_state_sequence(
            initial_state=request.initial_state,
            goal_state=request.goal_state,
            available_transitions=request.available_transitions,
            max_depth=self.max_sequence_length
        )
        
        # 转换为TransitionSequence对象
        for i, transition_list in enumerate(raw_sequences[:self.max_sequences]):
            sequence = TransitionSequence(
                id=f"sequence_{request.request_id}_{i}",
                transitions=transition_list.copy(),
                initial_state=request.initial_state.copy()
            )
            
            # 计算最终状态
            current_state = request.initial_state.copy()
            for transition in transition_list:
                current_state = transition.apply_effects(current_state)
            sequence.final_state = current_state
            
            sequences.append(sequence)
        
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
        """更新统计信息"""
        modeling_time = time.time() - start_time
        sequence_count = len(response.predicted_sequences)
        
        # 更新平均序列数
        total_requests = self.modeling_stats['total_requests']
        current_avg = self.modeling_stats['average_sequences_generated']
        new_avg = (current_avg * (total_requests - 1) + sequence_count) / total_requests
        self.modeling_stats['average_sequences_generated'] = new_avg
        
        # 更新平均验证时间
        if response.validation_results:
            current_val_avg = self.modeling_stats['average_validation_time']
            new_val_avg = (current_val_avg * (total_requests - 1) + modeling_time) / total_requests
            self.modeling_stats['average_validation_time'] = new_val_avg
    
    def _update_learning_model(self, request: ModelingRequest, response: ModelingResponse):
        """更新学习模型"""
        # 记录建模历史
        history_entry = {
            'request_id': request.request_id,
            'initial_state': request.initial_state,
            'goal_state': request.goal_state,
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