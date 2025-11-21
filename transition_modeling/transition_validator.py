#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transition Validator
状态转换验证器，验证转换的正确性和一致性
"""

from typing import Dict, List, Any, Optional, Tuple, Set
import logging
import time
from collections import defaultdict
import json

try:
    from .state_transition import StateTransition, TransitionType, TransitionStatus, StateCondition, StateEffect
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from state_transition import StateTransition, TransitionType, TransitionStatus, StateCondition, StateEffect


class ValidationResult:
    """验证结果类"""
    
    def __init__(self, is_valid: bool, message: str = "", details: Optional[Dict[str, Any]] = None):
        self.is_valid = is_valid
        self.message = message
        self.details = details or {}
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'is_valid': self.is_valid,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp
        }


class TransitionValidator:
    """状态转换验证器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化转换验证器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 验证规则配置
        self.strict_mode = self.config.get('strict_mode', True)
        self.check_temporal_consistency = self.config.get('check_temporal_consistency', True)
        self.check_resource_constraints = self.config.get('check_resource_constraints', True)
        self.max_validation_depth = self.config.get('max_validation_depth', 100)
        
        # 验证统计
        self.validation_stats = {
            'total_validations': 0,
            'successful_validations': 0,
            'failed_validations': 0,
            'common_errors': defaultdict(int)
        }
        
        self.logger.info("Transition Validator initialized")
    
    def validate_transition(self, 
                          transition: StateTransition,
                          current_state: Dict[str, Any],
                          context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        验证单个状态转换
        
        Args:
            transition: 要验证的转换
            current_state: 当前状态
            context: 验证上下文
            
        Returns:
            验证结果
        """
        self.validation_stats['total_validations'] += 1
        
        try:
            # 1. 基本结构验证
            structure_result = self._validate_transition_structure(transition)
            if not structure_result.is_valid:
                return structure_result
            
            # 2. 前提条件验证
            precondition_result = self._validate_preconditions(transition, current_state)
            if not precondition_result.is_valid:
                return precondition_result
            
            # 3. 效果一致性验证
            effect_result = self._validate_effects(transition, current_state)
            if not effect_result.is_valid:
                return effect_result
            
            # 4. 资源约束验证
            if self.check_resource_constraints:
                resource_result = self._validate_resource_constraints(transition, current_state, context)
                if not resource_result.is_valid:
                    return resource_result
            
            # 5. 时序一致性验证
            if self.check_temporal_consistency:
                temporal_result = self._validate_temporal_consistency(transition, current_state, context)
                if not temporal_result.is_valid:
                    return temporal_result
            
            self.validation_stats['successful_validations'] += 1
            return ValidationResult(True, "Transition validation passed")
            
        except Exception as e:
            self.validation_stats['failed_validations'] += 1
            error_msg = f"Validation error: {str(e)}"
            self.validation_stats['common_errors'][error_msg] += 1
            return ValidationResult(False, error_msg)
    
    def _validate_transition_structure(self, transition: StateTransition) -> ValidationResult:
        """验证转换结构"""
        # 检查必要字段
        if not transition.id or not transition.name:
            return ValidationResult(False, "Missing required fields: id or name")
        
        # 检查转换类型
        if not isinstance(transition.transition_type, TransitionType):
            return ValidationResult(False, "Invalid transition type")
        
        # 检查数值范围
        if transition.duration < 0:
            return ValidationResult(False, "Duration cannot be negative")
        
        if transition.cost < 0:
            return ValidationResult(False, "Cost cannot be negative")
        
        # 检查前提条件和效果
        for condition in transition.preconditions:
            if not condition.predicate:
                return ValidationResult(False, "Empty condition predicate")
        
        for effect in transition.effects:
            if not effect.predicate:
                return ValidationResult(False, "Empty effect predicate")
        
        return ValidationResult(True, "Structure validation passed")
    
    def _validate_preconditions(self, 
                              transition: StateTransition, 
                              state: Dict[str, Any]) -> ValidationResult:
        """验证前提条件"""
        for condition in transition.preconditions:
            try:
                if not condition.evaluate(state):
                    return ValidationResult(
                        False, 
                        f"Precondition not satisfied: {condition.predicate}"
                    )
            except Exception as e:
                return ValidationResult(
                    False, 
                    f"Error evaluating precondition {condition.predicate}: {str(e)}"
                )
        
        return ValidationResult(True, "Preconditions validation passed")
    
    def _validate_effects(self, 
                        transition: StateTransition, 
                        state: Dict[str, Any]) -> ValidationResult:
        """验证效果一致性"""
        predicted_state = transition.apply_effects(state)
        
        # 检查状态变化是否合理
        for effect in transition.effects:
            if effect.predicate in predicted_state:
                # 检查效果值类型
                if not self._is_valid_effect_value(effect.value):
                    return ValidationResult(
                        False, 
                        f"Invalid effect value for {effect.predicate}: {effect.value}"
                    )
        
        # 检查是否有真正矛盾的效果（不是简单的重复谓词）
        # 允许同一谓词的多个效果，只要它们是合理的（如设置新值和移除旧值）
        effect_groups = defaultdict(list)
        for effect in transition.effects:
            effect_groups[effect.predicate].append(effect)
        
        for predicate, effects in effect_groups.items():
            if len(effects) > 1:
                # 检查是否有真正冲突的效果
                positive_effects = [e for e in effects if e.probability > 0.5]
                negative_effects = [e for e in effects if e.probability <= 0.5]
                
                # 如果有多个高概率效果设置不同值，则冲突
                if len(positive_effects) > 1:
                    values = [e.value for e in positive_effects]
                    if len(set(values)) > 1:
                        return ValidationResult(
                            False, 
                            f"Conflicting positive effects for {predicate}: {values}"
                        )
                
                # 如果有多个低概率效果移除不同值，则冲突
                if len(negative_effects) > 1:
                    values = [e.value for e in negative_effects if e.value is not None]
                    if len(set(values)) > 1:
                        return ValidationResult(
                            False, 
                            f"Conflicting negative effects for {predicate}: {values}"
                        )
        
        return ValidationResult(True, "Effects validation passed")
    
    def _validate_resource_constraints(self, 
                                     transition: StateTransition,
                                     state: Dict[str, Any],
                                     context: Optional[Dict[str, Any]]) -> ValidationResult:
        """验证资源约束"""
        if not context:
            return ValidationResult(True, "No resource constraints to validate")
        
        # 检查时间约束
        if 'time_budget' in context:
            if transition.duration > context['time_budget']:
                return ValidationResult(
                    False, 
                    f"Transition duration {transition.duration} exceeds time budget {context['time_budget']}"
                )
        
        # 检查成本约束
        if 'cost_budget' in context:
            if transition.cost > context['cost_budget']:
                return ValidationResult(
                    False, 
                    f"Transition cost {transition.cost} exceeds cost budget {context['cost_budget']}"
                )
        
        # 检查资源可用性
        if 'available_resources' in context:
            resources = context['available_resources']
            for effect in transition.effects:
                if effect.predicate.startswith('CONSUME_'):
                    resource_name = effect.predicate[8:]  # 移除'CONSUME_'前缀
                    if resource_name in resources:
                        required_amount = effect.value
                        if resources[resource_name] < required_amount:
                            return ValidationResult(
                                False, 
                                f"Insufficient resource {resource_name}: required {required_amount}, available {resources[resource_name]}"
                            )
        
        return ValidationResult(True, "Resource constraints validation passed")
    
    def _validate_temporal_consistency(self, 
                                      transition: StateTransition,
                                      state: Dict[str, Any],
                                      context: Optional[Dict[str, Any]]) -> ValidationResult:
        """验证时序一致性"""
        if not context:
            return ValidationResult(True, "No temporal constraints to validate")
        
        # 检查时间依赖
        if 'current_time' in context and 'deadline' in context:
            current_time = context['current_time']
            deadline = context['deadline']
            
            if current_time + transition.duration > deadline:
                return ValidationResult(
                    False, 
                    f"Transition would miss deadline: current {current_time} + duration {transition.duration} > deadline {deadline}"
                )
        
        # 检查前置转换依赖
        if 'completed_transitions' in context:
            completed = context['completed_transitions']
            
            # 检查是否有必要的前置转换未完成
            for condition in transition.preconditions:
                if condition.predicate.startswith('REQUIRES_'):
                    required_transition = condition.predicate[9:]  # 移除'REQUIRES_'前缀
                    if required_transition not in completed:
                        return ValidationResult(
                            False, 
                            f"Required transition not completed: {required_transition}"
                        )
        
        return ValidationResult(True, "Temporal consistency validation passed")
    
    def _is_valid_effect_value(self, value: Any) -> bool:
        """检查效果值是否有效"""
        # 允许的类型
        valid_types = (bool, int, float, str, list, dict, type(None))
        return isinstance(value, valid_types)
    
    def validate_transition_sequence(self, 
                                    transitions: List[StateTransition],
                                    initial_state: Dict[str, Any],
                                    context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        验证转换序列
        
        Args:
            transitions: 转换序列
            initial_state: 初始状态
            context: 验证上下文
            
        Returns:
            验证结果
        """
        if len(transitions) > self.max_validation_depth:
            return ValidationResult(
                False, 
                f"Sequence too long: {len(transitions)} > {self.max_validation_depth}"
            )
        
        current_state = initial_state.copy()
        validation_details = {
            'transition_validations': [],
            'state_evolution': [initial_state.copy()]
        }
        
        for i, transition in enumerate(transitions):
            # 验证单个转换
            result = self.validate_transition(transition, current_state, context)
            validation_details['transition_validations'].append(result.to_dict())
            
            if not result.is_valid:
                return ValidationResult(
                    False, 
                    f"Transition {i} ({transition.name}) failed validation: {result.message}",
                    validation_details
                )
            
            # 应用转换效果
            current_state = transition.apply_effects(current_state)
            validation_details['state_evolution'].append(current_state.copy())
        
        return ValidationResult(
            True, 
            f"Sequence validation passed: {len(transitions)} transitions",
            validation_details
        )
    
    def validate_model_consistency(self, 
                                 transitions: List[StateTransition]) -> ValidationResult:
        """
        验证模型一致性
        
        Args:
            transitions: 转换列表
            
        Returns:
            验证结果
        """
        validation_details = {
            'duplicate_ids': [],
            'orphaned_transitions': [],
            'deadlock_potential': []
        }
        
        # 检查重复ID
        ids = [t.id for t in transitions]
        id_counts = defaultdict(int)
        for transition_id in ids:
            id_counts[transition_id] += 1
        
        duplicates = [tid for tid, count in id_counts.items() if count > 1]
        if duplicates:
            validation_details['duplicate_ids'] = duplicates
            return ValidationResult(
                False, 
                f"Duplicate transition IDs found: {duplicates}",
                validation_details
            )
        
        # 检查孤立转换（没有可达路径）
        reachable_transitions = self._find_reachable_transitions(transitions)
        all_ids = set(t.id for t in transitions)
        orphaned = list(all_ids - reachable_transitions)
        
        if orphaned:
            validation_details['orphaned_transitions'] = orphaned
            if self.strict_mode:
                return ValidationResult(
                    False, 
                    f"Orphaned transitions found: {orphaned}",
                    validation_details
                )
        
        # 检查死锁可能性
        deadlock_analysis = self._analyze_deadlock_potential(transitions)
        if deadlock_analysis['has_deadlock']:
            validation_details['deadlock_potential'] = deadlock_analysis['cycles']
            if self.strict_mode:
                return ValidationResult(
                    False, 
                    "Deadlock potential detected",
                    validation_details
                )
        
        return ValidationResult(
            True, 
            "Model consistency validation passed",
            validation_details
        )
    
    def _find_reachable_transitions(self, transitions: List[StateTransition]) -> Set[str]:
        """找到可达的转换"""
        # 简化的可达性分析
        reachable = set()
        
        # 找到没有前提条件的转换作为起点
        for transition in transitions:
            if not transition.preconditions:
                reachable.add(transition.id)
        
        # 简单的传播分析
        changed = True
        while changed:
            changed = False
            for transition in transitions:
                if transition.id in reachable:
                    continue
                
                # 检查是否所有前提条件都能被已可达的转换满足
                can_reach = True
                for condition in transition.preconditions:
                    if condition.predicate.startswith('EFFECT_'):
                        required_effect = condition.predicate[7:]  # 移除'EFFECT_'前缀
                        effect_found = False
                        for tid in reachable:
                            # 检查已可达转换是否产生所需效果
                            for t in transitions:
                                if t.id == tid:
                                    for effect in t.effects:
                                        if effect.predicate == required_effect:
                                            effect_found = True
                                            break
                            if effect_found:
                                break
                        
                        if not effect_found:
                            can_reach = False
                            break
                
                if can_reach:
                    reachable.add(transition.id)
                    changed = True
        
        return reachable
    
    def _analyze_deadlock_potential(self, transitions: List[StateTransition]) -> Dict[str, Any]:
        """分析死锁可能性"""
        # 简化的死锁分析
        # 构建依赖图
        dependencies = defaultdict(set)
        
        for transition in transitions:
            for condition in transition.preconditions:
                if condition.predicate.startswith('REQUIRES_'):
                    required_transition = condition.predicate[9:]
                    dependencies[transition.id].add(required_transition)
        
        # 检测循环
        visited = set()
        rec_stack = set()
        cycles = []
        
        def has_cycle(node: str, path: List[str]) -> bool:
            if node in rec_stack:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in dependencies[node]:
                if has_cycle(neighbor, path):
                    return True
            
            rec_stack.remove(node)
            path.pop()
            return False
        
        for transition_id in dependencies:
            if transition_id not in visited:
                has_cycle(transition_id, [])
        
        return {
            'has_deadlock': len(cycles) > 0,
            'cycles': cycles
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取验证器统计信息"""
        total = self.validation_stats['total_validations']
        success = self.validation_stats['successful_validations']
        
        return {
            'validation_stats': self.validation_stats,
            'success_rate': success / total if total > 0 else 0.0,
            'common_errors': dict(self.validation_stats['common_errors'])
        }