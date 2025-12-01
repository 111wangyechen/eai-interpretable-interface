#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State Transition Data Structures
状态转换数据结构定义
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import json
import time
import logging
import random


class TransitionType(Enum):
    """转换类型枚举"""
    ATOMIC = "atomic"           # 原子转换
    COMPOSITE = "composite"     # 复合转换
    CONDITIONAL = "conditional" # 条件转换
    TEMPORAL = "temporal"       # 时序转换
    STOCHASTIC = "stochastic"   # 随机转换


class TransitionStatus(Enum):
    """转换状态枚举"""
    PENDING = "pending"         # 等待执行
    EXECUTING = "executing"     # 正在执行
    COMPLETED = "completed"     # 执行完成
    FAILED = "failed"          # 执行失败
    SKIPPED = "skipped"        # 跳过执行


class StateCondition:
    """状态条件类 - 符合PDDL格式"""
    
    def __init__(self, 
                 predicate: str, 
                 value: Any = None, 
                 operator: str = '=', 
                 negated: bool = False, 
                 params: Optional[List[Any]] = None, 
                 confidence: float = 1.0):
        """
        初始化状态条件
        
        Args:
            predicate: 谓词名称（符合PDDL格式）
            value: 比较值
            operator: 比较运算符，支持 =, !=, >, <, >=, <=, in, not in
            negated: 是否取反（PDDL中的not）
            params: 参数列表（支持PDDL参数化谓词）
            confidence: 置信度
        """
        self.predicate = predicate
        self.value = value
        self.operator = operator
        self.negated = negated
        self.params = params or []
        self.confidence = confidence
        self.logger = logging.getLogger(__name__)
    
    def evaluate(self, state: Dict[str, Any]) -> bool:
        """评估条件在给定状态下是否成立"""
        # PDDL格式条件评估
        try:
            # 构建完整谓词键（支持参数化）
            if self.params:
                param_str = '_'.join(str(p) for p in self.params)
                full_predicate = f"{self.predicate}_{param_str}"
            else:
                full_predicate = self.predicate
            
            # 检查谓词是否存在于状态中
            if full_predicate not in state:
                # 如果谓词不存在，返回默认值
                result = False
            else:
                state_value = state[full_predicate]
                
                # 根据运算符进行比较
                if self.operator == '=':
                    result = (state_value == self.value)
                elif self.operator == '!=':
                    result = (state_value != self.value)
                elif self.operator == '>':
                    result = (state_value > self.value)
                elif self.operator == '<':
                    result = (state_value < self.value)
                elif self.operator == '>=':
                    result = (state_value >= self.value)
                elif self.operator == '<=':
                    result = (state_value <= self.value)
                elif self.operator == 'in':
                    result = (state_value in self.value)
                elif self.operator == 'not in':
                    result = (state_value not in self.value)
                else:
                    # 未知运算符，默认返回False
                    self.logger.warning(f"Unknown operator: {self.operator}")
                    result = False
            
            # 应用取反
            return not result if self.negated else result
        except Exception as e:
            # 比较错误，返回False并记录详细错误
            self.logger.error(f"Error evaluating condition {self.to_pddl()}: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'predicate': self.predicate,
            'value': self.value,
            'operator': self.operator,
            'negated': self.negated,
            'params': self.params,
            'confidence': self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateCondition':
        """从字典创建实例"""
        return cls(
            predicate=data.get('predicate'),
            value=data.get('value'),
            operator=data.get('operator', '='),
            negated=data.get('negated', False),
            params=data.get('params', []),
            confidence=data.get('confidence', 1.0)
        )
    
    def to_pddl(self) -> str:
        """转换为PDDL格式字符串"""
        try:
            # 构建PDDL谓词表达式
            param_str = ' '.join(str(p) for p in self.params) if self.params else ''
            if param_str:
                pddl_str = f"({self.predicate} {param_str})"
            else:
                pddl_str = f"({self.predicate})"
            
            # 添加取反
            if self.negated:
                pddl_str = f"(not {pddl_str})"
            
            # 如果有值和操作符，添加比较
            if self.value is not None and self.operator in ['=', '!=']:
                if isinstance(self.value, str):
                    value_str = f'"{self.value}"'
                else:
                    value_str = str(self.value)
                pddl_str = f"(= {pddl_str} {value_str})"
            
            return pddl_str
        except Exception as e:
            logging.error(f"Failed to convert StateCondition to PDDL: {str(e)}")
            return f"({self.predicate})"


class StateEffect:
    """状态效果类 - 符合PDDL格式"""
    
    def __init__(self, 
                 predicate: str, 
                 value: Any = None, 
                 probability: float = 1.0,
                 duration: float = 0.0,
                 params: Optional[List[Any]] = None,
                 effect_type: str = 'assign'):
        """
        初始化状态效果
        
        Args:
            predicate: 谓词名称（符合PDDL格式）
            value: 设置的值
            probability: 发生概率 (0.0 - 1.0)
            duration: 效果持续时间
            params: 参数列表（支持PDDL参数化谓词）
            effect_type: 效果类型: 'assign', 'add', 'delete' (符合PDDL效果类型)
        """
        self.predicate = predicate
        self.value = value
        self.probability = max(0.0, min(1.0, probability))  # 确保在有效范围内
        self.duration = max(0.0, duration)  # 确保非负
        self.params = params or []
        self.effect_type = effect_type  # 支持PDDL效果类型
        self.logger = logging.getLogger(__name__)
    
    def apply(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """应用效果到状态 - 符合PDDL语义"""
        try:
            # 根据概率决定是否应用效果
            if self.probability < 1.0:
                # 简化处理：如果概率小于1.0且不是1.0，随机决定是否应用
                if random.random() > self.probability:
                    return state.copy()
            
            # 复制状态以避免修改原状态
            new_state = state.copy()
            
            # 构建完整谓词键（支持参数化）
            if self.params:
                param_str = '_'.join(str(p) for p in self.params)
                full_predicate = f"{self.predicate}_{param_str}"
            else:
                full_predicate = self.predicate
            
            # 根据效果类型应用效果
            if self.effect_type == 'assign':
                # 直接赋值效果
                new_state[full_predicate] = self.value
                self.logger.debug(f"Applied assign effect: {full_predicate} = {self.value}")
            
            elif self.effect_type == 'add':
                # 添加效果（PDDL中的positive effect）
                new_state[full_predicate] = True
                self.logger.debug(f"Applied add effect: {full_predicate}")
            
            elif self.effect_type == 'delete':
                # 删除效果（PDDL中的negative effect）
                if full_predicate in new_state:
                    del new_state[full_predicate]
                self.logger.debug(f"Applied delete effect: {full_predicate}")
            
            else:
                # 默认为赋值效果
                new_state[full_predicate] = self.value
                self.logger.warning(f"Unknown effect type '{self.effect_type}', using 'assign'")
            
            return new_state
        except Exception as e:
            # 应用错误，返回原状态并记录详细错误
            self.logger.error(f"Error applying effect {self.to_pddl()}: {e}")
            return state.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'predicate': self.predicate,
            'value': self.value,
            'probability': self.probability,
            'duration': self.duration,
            'params': self.params,
            'effect_type': self.effect_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateEffect':
        """从字典创建实例"""
        return cls(
            predicate=data.get('predicate'),
            value=data.get('value'),
            probability=data.get('probability', 1.0),
            duration=data.get('duration', 0.0),
            params=data.get('params', []),
            effect_type=data.get('effect_type', 'assign')
        )
    
    def to_pddl(self) -> str:
        """转换为PDDL格式字符串"""
        try:
            param_str = ' '.join(str(p) for p in self.params) if self.params else ''
            
            if self.effect_type == 'add':
                # PDDL positive effect
                if param_str:
                    pddl_str = f"({self.predicate} {param_str})"
                else:
                    pddl_str = f"({self.predicate})"
            
            elif self.effect_type == 'delete':
                # PDDL negative effect
                if param_str:
                    pddl_str = f"(not ({self.predicate} {param_str}))"
                else:
                    pddl_str = f"(not ({self.predicate}))"
            
            else:  # assign
                # PDDL assign effect
                if self.value is not None:
                    if param_str:
                        pred_str = f"({self.predicate} {param_str})"
                    else:
                        pred_str = f"({self.predicate})"
                    if isinstance(self.value, str):
                        value_str = f'"{self.value}"'
                    else:
                        value_str = str(self.value)
                    pddl_str = f"(assign {pred_str} {value_str})"
                else:
                    pddl_str = f"({self.predicate})"
            
            # 添加置信度信息作为PDDL注释
            if hasattr(self, 'confidence') and self.confidence < 1.0:
                pddl_str += f" ; confidence: {self.confidence:.2f}"
            
            return pddl_str
        except Exception as e:
            logging.error(f"Failed to convert StateEffect to PDDL: {str(e)}")
            return f"({self.predicate})"


@dataclass
class StateTransition:
    """状态转换类 - 符合PDDL格式"""
    id: Optional[str] = None         # 转换ID（可选，自动生成）
    name: str = ""                   # 转换名称
    description: Optional[str] = None # 转换描述
    transition_type: TransitionType = TransitionType.ATOMIC  # 转换类型
    preconditions: List[StateCondition] = field(default_factory=list)  # 前提条件
    effects: List[StateEffect] = field(default_factory=list)            # 执行效果
    duration: float = 1.0            # 执行时间
    cost: float = 1.0                # 执行成本
    status: TransitionStatus = TransitionStatus.PENDING  # 转换状态
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    parameters: Dict[str, Any] = field(default_factory=dict)  # PDDL风格参数定义
    
    # 时间戳信息
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def __post_init__(self):
        """后处理初始化"""
        if not self.id:
            self.id = f"transition_{int(time.time() * 1000000)}"
        # 初始化日志
        self.logger = logging.getLogger(__name__)
        # 验证转换定义的一致性
        self._validate_definition()
    
    def _validate_definition(self) -> None:
        """验证转换定义的一致性和PDDL格式合规性"""
        # 检查ID和名称
        if not self.id or not isinstance(self.id, str):
            self.id = f"transition_{int(time.time() * 1000000)}"
        
        if not self.name or not isinstance(self.name, str):
            self.logger.warning(f"Transition has invalid name: {self.name}, setting to default")
            self.name = f"transition_{self.id}"
        
        # 验证前置条件列表
        if not isinstance(self.preconditions, list):
            self.preconditions = []
        else:
            # 验证每个前置条件
            valid_preconditions = []
            for cond in self.preconditions:
                if isinstance(cond, StateCondition):
                    valid_preconditions.append(cond)
            self.preconditions = valid_preconditions
        
        # 验证效果列表
        if not isinstance(self.effects, list):
            self.effects = []
        else:
            # 验证每个效果
            valid_effects = []
            for effect in self.effects:
                if isinstance(effect, StateEffect):
                    valid_effects.append(effect)
            self.effects = valid_effects
        
        # 检查前提条件和效果
        precondition_predicates = set()
        effect_predicates = set()
        
        for cond in self.preconditions:
            if hasattr(cond, 'params') and cond.params:
                pred_key = f"{cond.predicate}_{'_'.join(str(p) for p in cond.params)}"
            else:
                pred_key = cond.predicate
            precondition_predicates.add(pred_key)
        
        for effect in self.effects:
            if hasattr(effect, 'params') and effect.params:
                pred_key = f"{effect.predicate}_{'_'.join(str(p) for p in effect.params)}"
            else:
                pred_key = effect.predicate
            effect_predicates.add(pred_key)
        
        # 检查矛盾的前提条件
        conflicting_preconditions = self._check_conflicting_preconditions()
        if conflicting_preconditions:
            self.logger.warning(f"Conflicting preconditions in transition {self.name}: {conflicting_preconditions}")
        
        # 检查矛盾的效果
        conflicting_effects = self._check_conflicting_effects()
        if conflicting_effects:
            self.logger.warning(f"Conflicting effects in transition {self.name}: {conflicting_effects}")
    
    def _check_conflicting_preconditions(self) -> List[str]:
        """检查是否有矛盾的前提条件"""
        conflicts = []
        predicate_values = defaultdict(list)
        
        for cond in self.preconditions:
            if hasattr(cond, 'params') and cond.params:
                pred_key = f"{cond.predicate}_{'_'.join(str(p) for p in cond.params)}"
            else:
                pred_key = cond.predicate
            
            if hasattr(cond, 'value') and cond.value is not None:
                predicate_values[pred_key].append((cond.value, cond.negated))
        
        # 检查同一个谓词是否有不同的值要求
        for pred_key, value_list in predicate_values.items():
            if len(value_list) > 1:
                # 检查是否有直接矛盾（同一值既有取反又有非取反）
                for i in range(len(value_list)):
                    for j in range(i+1, len(value_list)):
                        val1, neg1 = value_list[i]
                        val2, neg2 = value_list[j]
                        if val1 == val2 and neg1 != neg2:
                            conflicts.append(f"{pred_key} has conflicting conditions for value {val1}")
        
        return conflicts
    
    def _check_conflicting_effects(self) -> List[str]:
        """检查是否有矛盾的效果"""
        conflicts = []
        predicate_values = defaultdict(list)
        
        for effect in self.effects:
            if hasattr(effect, 'params') and effect.params:
                pred_key = f"{effect.predicate}_{'_'.join(str(p) for p in effect.params)}"
            else:
                pred_key = effect.predicate
            
            if hasattr(effect, 'effect_type'):
                predicate_values[pred_key].append(effect.effect_type)
        
        # 检查同一个谓词是否有添加和删除的矛盾效果
        for pred_key, effect_types in predicate_values.items():
            if 'add' in effect_types and 'delete' in effect_types:
                conflicts.append(f"{pred_key} has both add and delete effects")
        
        return conflicts
    
    def is_applicable(self, state: Dict[str, Any]) -> bool:
        """检查转换是否适用于当前状态 - 符合PDDL语义"""
        for condition in self.preconditions:
            if not condition.evaluate(state):
                # 记录不满足的前提条件
                if hasattr(condition, 'to_pddl'):
                    self.logger.debug(f"Precondition not met: {condition.to_pddl()}")
                return False
        # 检查转换状态
        if self.status == TransitionStatus.FAILED:
            self.logger.warning(f"Transition {self.name} has failed and cannot be applied")
            return False
        return True
    
    def apply_effects(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """应用转换效果到状态 - 符合PDDL语义"""
        new_state = state.copy()
        for effect in self.effects:
            # 根据概率决定是否应用效果
            import random
            if random.random() <= effect.probability:
                new_state = effect.apply(new_state)
        return new_state
    
    def start_execution(self):
        """开始执行转换"""
        self.status = TransitionStatus.EXECUTING
        self.started_at = time.time()
    
    def complete_execution(self, success: bool = True):
        """完成执行转换"""
        self.status = TransitionStatus.COMPLETED if success else TransitionStatus.FAILED
        self.completed_at = time.time()
    
    def get_execution_time(self) -> Optional[float]:
        """获取执行时间"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'transition_type': self.transition_type.value,
            'preconditions': [c.to_dict() for c in self.preconditions],
            'effects': [e.to_dict() for e in self.effects],
            'duration': self.duration,
            'cost': self.cost,
            'status': self.status.value,
            'metadata': self.metadata,
            'parameters': self.parameters,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'execution_time': self.get_execution_time()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateTransition':
        """从字典创建StateTransition"""
        transition = cls(
            id=data.get('id'),  # 使用get方法，允许id为None
            name=data.get('name', ''),
            description=data.get('description'),
            transition_type=TransitionType(data.get('transition_type', 'atomic')),
            duration=data.get('duration', 1.0),
            cost=data.get('cost', 1.0),
            status=TransitionStatus(data.get('status', 'pending')),
            metadata=data.get('metadata', {}),
            parameters=data.get('parameters', {}),
            created_at=data.get('created_at', time.time()),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at')
        )
        
        # 重建前提条件
        for cond_data in data.get('preconditions', []):
            condition = StateCondition.from_dict(cond_data)
            transition.preconditions.append(condition)
        
        # 重建效果
        for effect_data in data.get('effects', []):
            effect = StateEffect.from_dict(effect_data)
            transition.effects.append(effect)
        
        return transition
    
    def to_pddl(self) -> str:
        """转换为PDDL格式字符串"""
        try:
            # 构建参数定义
            param_str = ''
            if self.parameters:
                param_list = []
                for k, v in self.parameters.items():
                    # 确保参数类型符合PDDL规范
                    pddl_type = v if v else 'object'
                    param_list.append(f"?{k} - {pddl_type}")
                param_str = ' '.join(param_list)
            
            # 构建前置条件
            preconds_pddl = []
            for cond in self.preconditions:
                if hasattr(cond, 'to_pddl'):
                    cond_pddl = cond.to_pddl()
                    if cond_pddl:
                        preconds_pddl.append(cond_pddl)
            
            # 构建效果
            effects_pddl = []
            for effect in self.effects:
                if hasattr(effect, 'to_pddl'):
                    effect_pddl = effect.to_pddl()
                    if effect_pddl:
                        effects_pddl.append(effect_pddl)
            
            # 添加默认成本效果
            effects_pddl.append(f"(increase (total-cost) {self.cost:.2f})")
            
            # 组装完整PDDL
            pddl = f"""( :action {self.name.lower()}
    :parameters ({param_str})
    :precondition (and
        {chr(10).join(f'        {p}' for p in preconds_pddl) or '        '}
    )
    :effect (and
        {chr(10).join(f'        {e}' for e in effects_pddl) or '        '}
    )
)"""
            
            return pddl
        except Exception as e:
            logging.error(f"Failed to convert StateTransition to PDDL: {str(e)}")
            return f"( :action {self.name.lower()} :parameters () :precondition (and) :effect (and))"
    
    def get_consistency_report(self) -> Dict[str, Any]:
        """获取转换的一致性报告"""
        return {
            'transition_id': self.id,
            'transition_name': self.name,
            'has_conflicting_preconditions': len(self._check_conflicting_preconditions()) > 0,
            'conflicting_preconditions': self._check_conflicting_preconditions(),
            'has_conflicting_effects': len(self._check_conflicting_effects()) > 0,
            'conflicting_effects': self._check_conflicting_effects(),
            'precondition_count': len(self.preconditions),
            'effect_count': len(self.effects),
            'duration': self.duration,
            'cost': self.cost,
            'status': self.status.value
        }


@dataclass
class TransitionSequence:
    """转换序列类，支持PDDL格式的转换序列管理"""
    id: str                          # 序列ID
    transitions: List[StateTransition] = field(default_factory=list)  # 转换列表
    initial_state: Dict[str, Any] = field(default_factory=dict)       # 初始状态
    final_state: Optional[Dict[str, Any]] = None                      # 最终状态
    goal_state: Optional[Dict[str, Any]] = field(default_factory=dict)  # PDDL目标状态
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    
    def __post_init__(self):
        """后处理初始化"""
        if not self.id:
            self.id = f"sequence_{int(time.time() * 1000000)}"
        self.created_at = time.time()
        self.updated_at = time.time()
    
    def add_transition(self, transition: StateTransition):
        """添加转换到序列，确保符合PDDL格式"""
        # 确保转换有参数支持
        if not hasattr(transition, 'parameters'):
            transition.parameters = {}
        self.transitions.append(transition)
        self.updated_at = time.time()
    
    def insert_transition(self, index: int, transition: StateTransition):
        """在指定位置插入转换，确保符合PDDL格式"""
        # 确保转换有参数支持
        if not hasattr(transition, 'parameters'):
            transition.parameters = {}
        self.transitions.insert(index, transition)
        self.updated_at = time.time()
    
    def get_total_duration(self) -> float:
        """获取总执行时间"""
        return sum(t.duration for t in self.transitions)
    
    def get_total_cost(self) -> float:
        """获取总成本"""
        return sum(t.cost for t in self.transitions)
    
    def is_valid_sequence(self, current_state: Dict[str, Any]) -> bool:
        """验证序列是否有效，支持PDDL语义"""
        from copy import deepcopy
        temp_state = deepcopy(current_state)
        
        for transition in self.transitions:
            if not transition.is_applicable(temp_state):
                return False
            temp_state = transition.apply_effects(temp_state)
        
        return True
    
    def get_pddl_sequence(self) -> List[str]:
        """
        获取PDDL格式的转换序列
        
        Returns:
            PDDL格式的转换序列列表
        """
        pddl_sequence = []
        for transition in self.transitions:
            if hasattr(transition, 'to_pddl'):
                pddl_sequence.append(transition.to_pddl())
        return pddl_sequence
    
    def validate_pddl_consistency(self) -> Dict[str, Any]:
        """
        验证序列的PDDL一致性
        
        Returns:
            一致性验证报告
        """
        report = {
            'is_consistent': True,
            'issues': [],
            'inconsistent_transitions': []
        }
        
        # 检查每个转换的PDDL兼容性
        for i, transition in enumerate(self.transitions):
            # 检查参数支持
            if not hasattr(transition, 'parameters'):
                report['issues'].append(f"转换[{i}] {transition.id} 缺少parameters属性")
                report['inconsistent_transitions'].append(i)
                report['is_consistent'] = False
        
        return report
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'transitions': [t.to_dict() for t in self.transitions],
            'initial_state': self.initial_state,
            'final_state': self.final_state,
            'goal_state': self.goal_state,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'total_duration': self.get_total_duration(),
            'total_cost': self.get_total_cost()
        }


@dataclass
class TransitionModel:
    """转换模型类，支持PDDL格式的状态转换系统"""
    id: str                          # 模型ID
    name: str                        # 模型名称
    domain: str                      # 应用领域
    transitions: List[StateTransition] = field(default_factory=list)  # 转换集合
    state_schema: Dict[str, Any] = field(default_factory=dict)        # 状态模式
    
    def __post_init__(self):
        """后处理初始化"""
        if not self.id:
            self.id = f"model_{int(time.time() * 1000000)}"
        self.created_at = time.time()
        self.updated_at = time.time()
    
    def add_transition(self, transition: StateTransition):
        """添加转换到模型，确保符合PDDL格式"""
        # 确保转换有参数支持
        if not hasattr(transition, 'parameters'):
            transition.parameters = {}
        self.transitions.append(transition)
        self.updated_at = time.time()
    
    def remove_transition(self, transition_id: str):
        """通过ID移除转换"""
        self.transitions = [t for t in self.transitions if t.id != transition_id]
        self.updated_at = time.time()
    
    def get_transition_by_id(self, transition_id: str) -> Optional[StateTransition]:
        """通过ID获取转换"""
        for transition in self.transitions:
            if transition.id == transition_id:
                return transition
        return None
    
    def get_transitions_by_type(self, transition_type: TransitionType) -> List[StateTransition]:
        """通过类型获取转换列表"""
        return [t for t in self.transitions if t.transition_type == transition_type]
    
    def find_applicable_transitions(self, state: Dict[str, Any]) -> List[StateTransition]:
        """查找适用于当前状态的转换"""
        applicable = []
        for transition in self.transitions:
            if transition.is_applicable(state):
                applicable.append(transition)
        return applicable
    
    def export_to_pddl(self, filepath: str) -> bool:
        """
        导出模型为PDDL格式
        
        Args:
            filepath: 导出文件路径
            
        Returns:
            是否成功导出
        """
        try:
            # 构建PDDL域文件内容
            pddl_content = []
            pddl_content.append(f"(define (domain {self.domain.replace(' ', '_')})")
            pddl_content.append("  (:requirements :typing)")
            
            # 提取谓词定义
            predicates = set()
            for transition in self.transitions:
                for condition in transition.preconditions:
                    if hasattr(condition, 'to_pddl'):
                        pred_str = condition.to_pddl().split(' ')[0].strip('()')
                        predicates.add(pred_str)
                for effect in transition.effects:
                    if hasattr(effect, 'to_pddl'):
                        pred_str = effect.to_pddl().split(' ')[0].strip('()')
                        predicates.add(pred_str)
            
            # 添加谓词定义
            pddl_content.append("  (:predicates")
            for pred in sorted(predicates):
                pddl_content.append(f"    ({pred} ?x - object)")
            pddl_content.append("  )")
            
            # 添加动作定义
            for transition in self.transitions:
                if hasattr(transition, 'to_pddl'):
                    pddl_content.append("  ")
                    pddl_content.append(transition.to_pddl())
            
            # 保存到文件
            pddl_content = '\n'.join(pddl_content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(pddl_content)
            
            return True
        except Exception as e:
            import logging
            logging.error(f"Failed to export model to PDDL: {str(e)}")
            return False
    
    def validate_pddl_consistency(self) -> Dict[str, Any]:
        """
        验证模型的PDDL一致性
        
        Returns:
            一致性验证报告
        """
        report = {
            'is_consistent': True,
            'issues': [],
            'invalid_transitions': [],
            'pddl_stats': {
                'total_transitions': len(self.transitions),
                'pddl_compatible': 0,
                'parameterized_transitions': 0
            }
        }
        
        # 检查每个转换的PDDL兼容性
        for i, transition in enumerate(self.transitions):
            is_pddl_compatible = True
            
            # 检查是否有必要的PDDL方法
            if not hasattr(transition, 'to_pddl'):
                report['issues'].append(f"转换[{i}] {transition.id} 缺少to_pddl方法")
                report['invalid_transitions'].append(i)
                is_pddl_compatible = False
            
            # 检查参数支持
            if not hasattr(transition, 'parameters'):
                report['issues'].append(f"转换[{i}] {transition.id} 缺少parameters属性")
                report['invalid_transitions'].append(i)
                is_pddl_compatible = False
            elif transition.parameters:
                report['pddl_stats']['parameterized_transitions'] += 1
            
            if is_pddl_compatible:
                report['pddl_stats']['pddl_compatible'] += 1
            else:
                report['is_consistent'] = False
        
        # 检查谓词一致性
        predicate_transitions = {}
        for transition in self.transitions:
            for condition in transition.preconditions:
                if hasattr(condition, 'to_pddl'):
                    pred_str = condition.to_pddl().split(' ')[0].strip('()')
                    if pred_str not in predicate_transitions:
                        predicate_transitions[pred_str] = []
                    predicate_transitions[pred_str].append(transition.id)
        
        report['pddl_stats']['unique_predicates'] = len(predicate_transitions)
        
        return report
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'transitions': [t.to_dict() for t in self.transitions],
            'state_schema': self.state_schema,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'transition_count': len(self.transitions)
        }