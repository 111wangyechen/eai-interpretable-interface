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
        
        # PDDL格式验证配置
        self.enable_pddl_validation = self.config.get('enable_pddl_validation', True)
        self.max_transition_complexity = self.config.get('max_transition_complexity', 20)
        
        # 验证统计
        self.validation_stats = {
            'total_validations': 0,
            'successful_validations': 0,
            'failed_validations': 0,
            'common_errors': defaultdict(int),
            'pddl_format_errors': 0,
            'consistency_errors': 0,
            'complexity_warnings': 0
        }
        
        self.logger.info("Transition Validator initialized with PDDL validation support")
    
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
        
        # 检查输入类型
        if not isinstance(transition, StateTransition):
            self.validation_stats['failed_validations'] += 1
            error_msg = f"Invalid transition: {transition}. Must be an instance of StateTransition"
            self.validation_stats['common_errors'][error_msg] += 1
            return ValidationResult(False, error_msg)
        
        try:
            # 1. 基本结构验证
            structure_result = self._validate_transition_structure(transition)
            if not structure_result.is_valid:
                self.validation_stats['failed_validations'] += 1
                self.validation_stats['common_errors'][structure_result.message] += 1
                return structure_result
            
            # 2. 前提条件验证
            precondition_result = self._validate_preconditions(transition, current_state)
            if not precondition_result.is_valid:
                self.validation_stats['failed_validations'] += 1
                self.validation_stats['common_errors'][precondition_result.message] += 1
                return precondition_result
            
            # 3. 效果一致性验证
            effect_result = self._validate_effects(transition, current_state)
            if not effect_result.is_valid:
                self.validation_stats['failed_validations'] += 1
                self.validation_stats['common_errors'][effect_result.message] += 1
                return effect_result
            
            # 4. 资源约束验证
            if self.check_resource_constraints:
                resource_result = self._validate_resource_constraints(transition, current_state, context)
                if not resource_result.is_valid:
                    self.validation_stats['failed_validations'] += 1
                    self.validation_stats['common_errors'][resource_result.message] += 1
                    return resource_result
            
            # 5. 时序一致性验证
            if self.check_temporal_consistency:
                temporal_result = self._validate_temporal_consistency(transition, current_state, context)
                if not temporal_result.is_valid:
                    self.validation_stats['failed_validations'] += 1
                    self.validation_stats['common_errors'][temporal_result.message] += 1
                    return temporal_result
            
            self.validation_stats['successful_validations'] += 1
            return ValidationResult(True, "Transition validation passed")
            
        except Exception as e:
            self.validation_stats['failed_validations'] += 1
            error_msg = f"Validation error in transition {transition.id} ({transition.name}): {str(e)}"
            self.validation_stats['common_errors'][error_msg] += 1
            return ValidationResult(False, error_msg)
    
    def _validate_transition_structure(self, transition: StateTransition) -> ValidationResult:
        """验证转换结构 - 增强PDDL格式验证和类型校验"""
        # 检查必要字段
        if not transition.id or not isinstance(transition.id, str):
            return ValidationResult(False, f"Invalid ID: {transition.id}. Must be a non-empty string")
        
        if not transition.name or not isinstance(transition.name, str):
            return ValidationResult(False, f"Invalid name: {transition.name}. Must be a non-empty string")
        
        # 检查转换类型
        if not isinstance(transition.transition_type, TransitionType):
            return ValidationResult(False, f"Invalid transition type: {transition.transition_type}. Must be an instance of TransitionType")
        
        # 检查数值范围和类型
        if not isinstance(transition.duration, (int, float)):
            return ValidationResult(False, f"Invalid duration: {transition.duration}. Must be a numeric value")
        if transition.duration < 0:
            return ValidationResult(False, f"Duration cannot be negative: {transition.duration}")
        
        if not isinstance(transition.cost, (int, float)):
            return ValidationResult(False, f"Invalid cost: {transition.cost}. Must be a numeric value")
        if transition.cost < 0:
            return ValidationResult(False, f"Cost cannot be negative: {transition.cost}")
        
        # 检查PDDL格式的名称合规性
        if self.enable_pddl_validation and not self._is_valid_pddl_name(transition.name):
            return ValidationResult(False, f"Invalid PDDL name format: {transition.name}. Use only letters, numbers, and underscores/dashes.")
        
        # 检查前提条件列表类型和内容
        if not isinstance(transition.preconditions, list):
            return ValidationResult(False, f"Invalid preconditions: {transition.preconditions}. Must be a list of StateCondition objects")
        
        for i, condition in enumerate(transition.preconditions):
            if not isinstance(condition, StateCondition):
                return ValidationResult(False, f"Invalid precondition at index {i}: {condition}. Must be a StateCondition object")
            
            if not condition.predicate or not isinstance(condition.predicate, str):
                return ValidationResult(False, f"Empty or invalid condition predicate at index {i}")
            
            # 验证PDDL格式的条件
            if self.enable_pddl_validation:
                try:
                    if hasattr(condition, 'to_pddl'):
                        condition.to_pddl()
                except Exception as e:
                    return ValidationResult(False, f"Invalid PDDL condition at index {i}: {condition.predicate}. Error: {str(e)}")
        
        # 检查效果列表类型和内容
        if not isinstance(transition.effects, list):
            return ValidationResult(False, f"Invalid effects: {transition.effects}. Must be a list of StateEffect objects")
        
        for i, effect in enumerate(transition.effects):
            if not isinstance(effect, StateEffect):
                return ValidationResult(False, f"Invalid effect at index {i}: {effect}. Must be a StateEffect object")
            
            if not effect.predicate or not isinstance(effect.predicate, str):
                return ValidationResult(False, f"Empty or invalid effect predicate at index {i}")
            
            # 验证效果概率
            if not isinstance(effect.probability, (int, float)) or effect.probability < 0 or effect.probability > 1:
                return ValidationResult(False, f"Invalid probability for effect {effect.predicate} at index {i}: {effect.probability}. Must be between 0 and 1")
            
            # 验证PDDL格式的效果
            if self.enable_pddl_validation:
                try:
                    if hasattr(effect, 'to_pddl'):
                        effect.to_pddl()
                except Exception as e:
                    return ValidationResult(False, f"Invalid PDDL effect at index {i}: {effect.predicate}. Error: {str(e)}")
        
        # 检查转换复杂度
        complexity = len(transition.preconditions) + len(transition.effects)
        if complexity > self.max_transition_complexity:
            self.validation_stats['complexity_warnings'] += 1
            if self.strict_mode:
                return ValidationResult(False, f"Transition complexity exceeds maximum: {complexity} > {self.max_transition_complexity}")
            else:
                self.logger.warning(f"High transition complexity: {complexity} (recommended max: {self.max_transition_complexity})")
        
        return ValidationResult(True, "Structure validation passed")
    
    def _is_valid_pddl_name(self, name: str) -> bool:
        """检查是否为有效的PDDL名称格式"""
        # PDDL名称应该只包含字母、数字和连字符
        import re
        return bool(re.match(r'^[a-zA-Z0-9\-_]+$', name))
    
    def _validate_preconditions(self, 
                              transition: StateTransition, 
                              state: Dict[str, Any]) -> ValidationResult:
        """验证前提条件 - 增强类型校验"""
        # 检查状态类型
        if not isinstance(state, dict):
            return ValidationResult(False, f"Invalid state: {state}. Must be a dictionary")
        
        for i, condition in enumerate(transition.preconditions):
            try:
                if not condition.evaluate(state):
                    return ValidationResult(
                        False, 
                        f"Precondition not satisfied at index {i}: {condition.predicate}. Current state: {state.get(condition.predicate)}"
                    )
            except Exception as e:
                return ValidationResult(
                    False, 
                    f"Error evaluating precondition {condition.predicate} at index {i}: {str(e)}. State: {state}"
                )
        
        return ValidationResult(True, "Preconditions validation passed")
    
    def _validate_effects(self, 
                        transition: StateTransition, 
                        state: Dict[str, Any]) -> ValidationResult:
        """验证效果一致性 - 增强PDDL格式验证和类型校验"""
        # 检查状态类型
        if not isinstance(state, dict):
            return ValidationResult(False, f"Invalid state: {state}. Must be a dictionary")
        
        predicted_state = transition.apply_effects(state)
        
        # 检查预测状态类型
        if not isinstance(predicted_state, dict):
            return ValidationResult(False, f"Invalid predicted state: {predicted_state}. Must be a dictionary")
        
        # 检查状态变化是否合理
        for i, effect in enumerate(transition.effects):
            if effect.predicate in predicted_state:
                # 检查效果值类型
                if not self._is_valid_effect_value(effect.value):
                    return ValidationResult(
                        False, 
                        f"Invalid effect value at index {i} for {effect.predicate}: {effect.value}. Must be a bool, int, float, or string"
                    )
        
        # 收集谓词信息（支持参数化）
        predicate_info = defaultdict(list)
        for i, effect in enumerate(transition.effects):
            if hasattr(effect, 'params') and effect.params:
                if not isinstance(effect.params, (list, tuple)):
                    return ValidationResult(
                        False, 
                        f"Invalid params at index {i} for {effect.predicate}: {effect.params}. Must be a list or tuple"
                    )
                pred_key = f"{effect.predicate}_{'_'.join(str(p) for p in effect.params)}"
            else:
                pred_key = effect.predicate
            
            effect_info = {
                'index': i,
                'value': effect.value,
                'probability': effect.probability,
                'effect_type': getattr(effect, 'effect_type', 'assign')
            }
            predicate_info[pred_key].append(effect_info)
        
        # 检查重复的效果谓词
        duplicate_predicates = [p for p, effects in predicate_info.items() if len(effects) > 1]
        if duplicate_predicates:
            duplicate_details = []
            for pred in duplicate_predicates:
                effect_indices = [str(e['index']) for e in predicate_info[pred]]
                duplicate_details.append(f"{pred} (indices: {', '.join(effect_indices)})")
            return ValidationResult(
                False, 
                f"Duplicate effect predicates found: {'; '.join(duplicate_details)}"
            )
        
        # 检查PDDL格式的效果冲突
        for pred_key, effects_info in predicate_info.items():
            # 检查效果类型冲突（add和delete不能同时存在）
            effect_types = [e['effect_type'] for e in effects_info]
            if 'add' in effect_types and 'delete' in effect_types:
                return ValidationResult(
                    False, 
                    f"Conflicting effect types for {pred_key}: both add and delete found"
                )
            
            # 检查概率效果的一致性
            high_prob_effects = [e for e in effects_info if e['probability'] > 0.5]
            if len(high_prob_effects) > 1:
                values = [e['value'] for e in high_prob_effects if e['value'] is not None]
                if len(set(values)) > 1:
                    return ValidationResult(
                        False, 
                        f"Conflicting high-probability effects for {pred_key}: {values}"
                    )
        
        # 检查效果的PDDL语义一致性
        if hasattr(transition, 'get_consistency_report'):
            report = transition.get_consistency_report()
            if report['has_conflicting_effects']:
                return ValidationResult(
                    False, 
                    f"Conflicting effects found: {report['conflicting_effects']}"
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
        验证模型一致性 - 增强PDDL格式检查
        
        Args:
            transitions: 转换列表
            
        Returns:
            验证结果
        """
        validation_details = {
            'duplicate_ids': [],
            'orphaned_transitions': [],
            'deadlock_potential': [],
            'conflicting_transitions': [],
            'pddl_format_issues': [],
            'consistency_reports': []
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
        
        # 检查重复名称（PDDL动作名必须唯一）
        names = [t.name.lower() for t in transitions]
        name_counts = defaultdict(int)
        for name in names:
            name_counts[name] += 1
        
        duplicate_names = [name for name, count in name_counts.items() if count > 1]
        if duplicate_names:
            validation_details['pddl_format_issues'].append(f"Duplicate PDDL action names: {duplicate_names}")
            if self.strict_mode:
                return ValidationResult(
                    False, 
                    f"Duplicate PDDL action names found: {duplicate_names}",
                    validation_details
                )
        
        # 检查PDDL格式合规性
        if self.enable_pddl_validation:
            for transition in transitions:
                try:
                    if hasattr(transition, 'to_pddl'):
                        transition.to_pddl()
                except Exception as e:
                    issue = f"Transition {transition.name} (ID: {transition.id}) has invalid PDDL format: {str(e)}"
                    validation_details['pddl_format_issues'].append(issue)
                    self.validation_stats['pddl_format_errors'] += 1
                    if self.strict_mode:
                        return ValidationResult(False, issue, validation_details)
        
        # 收集一致性报告
        for transition in transitions:
            if hasattr(transition, 'get_consistency_report'):
                report = transition.get_consistency_report()
                validation_details['consistency_reports'].append(report)
                if report['has_conflicting_preconditions'] or report['has_conflicting_effects']:
                    validation_details['conflicting_transitions'].append(transition.id)
                    self.validation_stats['consistency_errors'] += 1
        
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
        
        # 生成综合报告消息
        message = f"Model consistency validation passed with {len(transitions)} transitions"
        if validation_details['conflicting_transitions']:
            message += f" (Warning: {len(validation_details['conflicting_transitions'])} transitions have consistency issues)"
        if validation_details['pddl_format_issues']:
            message += f" (Warning: {len(validation_details['pddl_format_issues'])} PDDL format issues)"
        
        return ValidationResult(
            True, 
            message,
            validation_details
        )
    
    def generate_comprehensive_validation_report(self, 
                                               transitions: List[StateTransition],
                                               initial_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        生成综合验证报告
        
        Args:
            transitions: 转换列表
            initial_state: 初始状态（可选）
            
        Returns:
            详细的验证报告
        """
        report = {
            'summary': {
                'total_transitions': len(transitions),
                'valid_transitions': 0,
                'invalid_transitions': 0,
                'consistency_issues': 0,
                'pddl_compliant': True
            },
            'transition_reports': [],
            'model_consistency': None
        }
        
        # 验证每个转换
        for transition in transitions:
            trans_report = {
                'id': transition.id,
                'name': transition.name,
                'is_valid': True,
                'issues': []
            }
            
            # 基本结构验证
            structure_result = self._validate_transition_structure(transition)
            if not structure_result.is_valid:
                trans_report['is_valid'] = False
                trans_report['issues'].append(f"Structure: {structure_result.message}")
                report['summary']['pddl_compliant'] = False
            
            # 前提条件和效果验证
            if initial_state:
                precond_result = self._validate_preconditions(transition, initial_state)
                if not precond_result.is_valid:
                    trans_report['issues'].append(f"Preconditions: {precond_result.message}")
                
                effect_result = self._validate_effects(transition, initial_state)
                if not effect_result.is_valid:
                    trans_report['is_valid'] = False
                    trans_report['issues'].append(f"Effects: {effect_result.message}")
            
            # 一致性报告
            if hasattr(transition, 'get_consistency_report'):
                consistency = transition.get_consistency_report()
                trans_report['consistency'] = consistency
                if consistency['has_conflicting_preconditions'] or consistency['has_conflicting_effects']:
                    trans_report['is_valid'] = False
                    report['summary']['consistency_issues'] += 1
            
            # 更新统计
            if trans_report['is_valid']:
                report['summary']['valid_transitions'] += 1
            else:
                report['summary']['invalid_transitions'] += 1
            
            report['transition_reports'].append(trans_report)
        
        # 模型一致性验证
        model_result = self.validate_model_consistency(transitions)
        report['model_consistency'] = model_result.to_dict()
        
        return report
    
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