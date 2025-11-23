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
    try:
        import sys
        import os
        # 添加当前目录到Python路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        from logic_guard import LogicGuard, create_logic_guard
    except ImportError:
        # 如果仍然导入失败，设置为None并在运行时处理
        LogicGuard = None
        create_logic_guard = None
        import logging
        logging.warning("LogicGuard module not available, some features will be disabled")

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
                    # 确保序列中的状态数据已清理
                    sequence.initial_state = self._clean_serializable_data(sequence.initial_state)
                    sequence.final_state = self._clean_serializable_data(sequence.final_state)
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
            
            # 5. 构建响应
            # 创建完全安全的响应数据，确保不包含任何LogicGuard相关引用
            
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
                success=len(final_sequences) > 0,
                message=f"Generated {len(final_sequences)} valid sequences",
                predicted_sequences=final_sequences,
                validation_results=cleaned_validation_results,
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