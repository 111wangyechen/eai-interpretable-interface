#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State Transition Data Structures
状态转换数据结构定义
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import time


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


@dataclass
class StateCondition:
    """状态条件类"""
    predicate: str                    # 谓词表达式
    parameters: Dict[str, Any] = field(default_factory=dict)  # 参数
    confidence: float = 1.0          # 置信度
    
    def evaluate(self, state: Dict[str, Any]) -> bool:
        """评估条件是否满足"""
        # 检查谓词是否在状态中
        if self.predicate not in state:
            return False
        
        state_value = state[self.predicate]
        
        # 如果没有参数，检查布尔值（包括字符串形式的布尔值）
        if not self.parameters:
            # 处理字符串形式的布尔值
            if isinstance(state_value, str):
                return state_value.lower() == "true"
            # 处理其他类型的布尔值
            return bool(state_value)
        
        # 处理复杂参数匹配
        for param_key, param_value in self.parameters.items():
            if isinstance(state_value, dict):
                # 如果状态值是字典，检查参数匹配
                if param_key not in state_value or state_value[param_key] != param_value:
                    return False
            else:
                # 如果状态值不是字典但参数只有一个，直接比较
                if len(self.parameters) == 1 and state_value == param_value:
                    continue
                # 否则不匹配
                elif state_value != param_value:
                    return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'predicate': self.predicate,
            'parameters': self.parameters,
            'confidence': self.confidence
        }


@dataclass
class StateEffect:
    """状态效果类"""
    predicate: str                    # 谓词表达式
    value: Any                       # 效果值
    parameters: Dict[str, Any] = field(default_factory=dict)  # 参数
    probability: float = 1.0         # 发生概率
    
    def apply(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """应用效果到状态"""
        new_state = state.copy()
        new_state[self.predicate] = self.value
        return new_state
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'predicate': self.predicate,
            'value': self.value,
            'parameters': self.parameters,
            'probability': self.probability
        }


@dataclass
class StateTransition:
    """状态转换类"""
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
    
    # 时间戳信息
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def __post_init__(self):
        """后处理初始化"""
        if not self.id:
            self.id = f"transition_{int(time.time() * 1000000)}"
    
    def is_applicable(self, state: Dict[str, Any]) -> bool:
        """检查转换是否适用于当前状态"""
        for condition in self.preconditions:
            if not condition.evaluate(state):
                return False
        return True
    
    def apply_effects(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """应用转换效果到状态"""
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
            created_at=data.get('created_at', time.time()),
            started_at=data.get('started_at'),
            completed_at=data.get('completed_at')
        )
        
        # 重建前提条件
        for cond_data in data.get('preconditions', []):
            condition = StateCondition(
                predicate=cond_data['predicate'],
                parameters=cond_data.get('parameters', {}),
                confidence=cond_data.get('confidence', 1.0)
            )
            transition.preconditions.append(condition)
        
        # 重建效果
        for effect_data in data.get('effects', []):
            effect = StateEffect(
                predicate=effect_data['predicate'],
                value=effect_data['value'],
                parameters=effect_data.get('parameters', {}),
                probability=effect_data.get('probability', 1.0)
            )
            transition.effects.append(effect)
        
        return transition


@dataclass
class TransitionSequence:
    """转换序列类"""
    id: str                          # 序列ID
    transitions: List[StateTransition] = field(default_factory=list)  # 转换列表
    initial_state: Dict[str, Any] = field(default_factory=dict)       # 初始状态
    final_state: Optional[Dict[str, Any]] = None                      # 最终状态
    
    def __post_init__(self):
        """后处理初始化"""
        if not self.id:
            self.id = f"sequence_{int(time.time() * 1000000)}"
    
    def add_transition(self, transition: StateTransition):
        """添加转换到序列"""
        self.transitions.append(transition)
    
    def get_total_duration(self) -> float:
        """获取总执行时间"""
        return sum(t.duration for t in self.transitions)
    
    def get_total_cost(self) -> float:
        """获取总成本"""
        return sum(t.cost for t in self.transitions)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'transitions': [t.to_dict() for t in self.transitions],
            'initial_state': self.initial_state,
            'final_state': self.final_state,
            'total_duration': self.get_total_duration(),
            'total_cost': self.get_total_cost()
        }


@dataclass
class TransitionModel:
    """转换模型类"""
    id: str                          # 模型ID
    name: str                        # 模型名称
    domain: str                      # 应用领域
    transitions: List[StateTransition] = field(default_factory=list)  # 转换集合
    state_schema: Dict[str, Any] = field(default_factory=dict)        # 状态模式
    
    def __post_init__(self):
        """后处理初始化"""
        if not self.id:
            self.id = f"model_{int(time.time() * 1000000)}"
    
    def add_transition(self, transition: StateTransition):
        """添加转换到模型"""
        self.transitions.append(transition)
    
    def find_applicable_transitions(self, state: Dict[str, Any]) -> List[StateTransition]:
        """查找适用于当前状态的转换"""
        applicable = []
        for transition in self.transitions:
            if transition.is_applicable(state):
                applicable.append(transition)
        return applicable
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'transitions': [t.to_dict() for t in self.transitions],
            'state_schema': self.state_schema,
            'transition_count': len(self.transitions)
        }