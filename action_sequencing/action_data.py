#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动作序列模块数据类
定义Action和ActionSequence的核心数据结构
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
import json
import time


class ActionType(Enum):
    """动作类型枚举"""
    NAVIGATION = "navigation"      # 导航动作
    MANIPULATION = "manipulation"  # 操作动作
    PERCEPTION = "perception"      # 感知动作
    COMMUNICATION = "communication"  # 通信动作
    WAIT = "wait"                 # 等待动作
    CONDITIONAL = "conditional"    # 条件动作
    OBSERVATION = "observation"    # 观察动作


class ActionStatus(Enum):
    """动作状态枚举"""
    PENDING = "pending"           # 待执行
    EXECUTING = "executing"       # 执行中
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 执行失败
    SKIPPED = "skipped"           # 跳过


@dataclass
class Action:
    """动作数据类"""
    id: str
    name: str
    action_type: ActionType
    parameters: Dict[str, Any] = field(default_factory=dict)
    preconditions: List[str] = field(default_factory=list)
    effects: List[str] = field(default_factory=list)
    duration: float = 1.0
    success_probability: float = 1.0
    status: ActionStatus = ActionStatus.PENDING
    execution_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """后处理初始化"""
        if self.parameters is None:
            self.parameters = {}
        if self.preconditions is None:
            self.preconditions = []
        if self.effects is None:
            self.effects = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'action_type': self.action_type.value,
            'parameters': self.parameters,
            'preconditions': self.preconditions,
            'effects': self.effects,
            'duration': self.duration,
            'success_probability': self.success_probability,
            'status': self.status.value,
            'execution_time': self.execution_time,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Action':
        """从字典创建Action对象"""
        # 处理枚举类型
        action_type = ActionType(data['action_type'])
        status = ActionStatus(data['status'])
        
        return cls(
            id=data['id'],
            name=data['name'],
            action_type=action_type,
            parameters=data.get('parameters', {}),
            preconditions=data.get('preconditions', []),
            effects=data.get('effects', []),
            duration=data.get('duration', 1.0),
            success_probability=data.get('success_probability', 1.0),
            status=status,
            execution_time=data.get('execution_time'),
            metadata=data.get('metadata', {})
        )
    
    def can_execute(self, current_state: Dict[str, Any]) -> bool:
        """检查动作是否可以执行"""
        # 检查前提条件是否满足
        for precondition in self.preconditions:
            if not self._evaluate_condition(precondition, current_state):
                return False
        return True
    
    def _evaluate_condition(self, condition: str, state: Dict[str, Any]) -> bool:
        """评估单个条件"""
        # 简单的条件评估逻辑
        # 支持格式: "key=value", "key!=value", "key>value", "key<value", 或者简单的布尔键
        try:
            if '=' in condition and '!=' not in condition:
                key, value = condition.split('=', 1)
                return state.get(key.strip()) == value.strip()
            elif '!=' in condition:
                key, value = condition.split('!=', 1)
                return state.get(key.strip()) != value.strip()
            elif '>' in condition:
                key, value = condition.split('>', 1)
                return float(state.get(key.strip(), 0)) > float(value.strip())
            elif '<' in condition:
                key, value = condition.split('<', 1)
                return float(state.get(key.strip(), 0)) < float(value.strip())
            else:
                # 简单的布尔检查 - 检查条件是否存在于状态中且为True
                value = state.get(condition.strip())
                return bool(value)
        except Exception:
            return False
    
    def execute(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """执行动作并返回新状态"""
        if not self.can_execute(current_state):
            raise ValueError(f"Action {self.id} cannot be executed in current state")
        
        self.status = ActionStatus.EXECUTING
        self.execution_time = time.time()
        
        # 模拟动作执行
        new_state = current_state.copy()
        
        # 应用效果
        for effect in self.effects:
            new_state = self._apply_effect(effect, new_state)
        
        # 更新状态
        self.status = ActionStatus.COMPLETED
        
        return new_state
    
    def _apply_effect(self, effect: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """应用动作效果"""
        new_state = state.copy()
        
        # 简单的效果应用逻辑
        # 支持格式: "key=value", "key+=value", "key-=value"
        try:
            if '=' in effect and '+' not in effect and '-' not in effect:
                key, value = effect.split('=', 1)
                new_state[key.strip()] = value.strip()
            elif '+=' in effect:
                key, value = effect.split('+=', 1)
                current_val = float(new_state.get(key.strip(), 0))
                new_state[key.strip()] = current_val + float(value.strip())
            elif '-=' in effect:
                key, value = effect.split('-=', 1)
                current_val = float(new_state.get(key.strip(), 0))
                new_state[key.strip()] = current_val - float(value.strip())
        except Exception:
            pass
        
        return new_state


@dataclass
class ActionSequence:
    """动作序列数据类"""
    id: str
    actions: List[Action] = field(default_factory=list)
    initial_state: Dict[str, Any] = field(default_factory=dict)
    goal_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """后处理初始化"""
        if self.actions is None:
            self.actions = []
        if self.initial_state is None:
            self.initial_state = {}
        if self.goal_state is None:
            self.goal_state = {}
        if self.metadata is None:
            self.metadata = {}
    
    def add_action(self, action: Action, position: Optional[int] = None):
        """添加动作到序列"""
        if position is None:
            self.actions.append(action)
        else:
            self.actions.insert(position, action)
    
    def remove_action(self, action_id: str) -> bool:
        """从序列中移除动作"""
        for i, action in enumerate(self.actions):
            if action.id == action_id:
                del self.actions[i]
                return True
        return False
    
    def get_action(self, action_id: str) -> Optional[Action]:
        """获取指定ID的动作"""
        for action in self.actions:
            if action.id == action_id:
                return action
        return None
    
    def get_executable_actions(self, current_state: Dict[str, Any]) -> List[Action]:
        """获取当前可执行的动作"""
        executable = []
        for action in self.actions:
            if (action.status == ActionStatus.PENDING and 
                action.can_execute(current_state)):
                executable.append(action)
        return executable
    
    def is_valid(self) -> bool:
        """检查动作序列是否有效"""
        if not self.actions:
            return False
        
        # 检查是否有重复的ID
        action_ids = [action.id for action in self.actions]
        if len(action_ids) != len(set(action_ids)):
            return False
        
        # 检查初始状态和目标状态是否有效
        if not isinstance(self.initial_state, dict) or not isinstance(self.goal_state, dict):
            return False
        
        return True
    
    def is_completed(self) -> bool:
        """检查序列是否完成"""
        return all(action.status in [ActionStatus.COMPLETED, ActionStatus.SKIPPED] 
                  for action in self.actions)
    
    def is_failed(self) -> bool:
        """检查序列是否失败"""
        return any(action.status == ActionStatus.FAILED for action in self.actions)
    
    def get_next_action(self) -> Optional[Action]:
        """获取下一个待执行的动作"""
        for action in self.actions:
            if action.status == ActionStatus.PENDING:
                return action
        return None
    
    def execute_next(self, current_state: Dict[str, Any]) -> Tuple[Optional[Action], Dict[str, Any]]:
        """执行下一个动作"""
        next_action = self.get_next_action()
        if next_action and next_action.can_execute(current_state):
            new_state = next_action.execute(current_state)
            return next_action, new_state
        return None, current_state
    
    def get_total_duration(self) -> float:
        """获取动作序列总时长"""
        return sum(action.duration for action in self.actions)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取序列统计信息"""
        total_actions = len(self.actions)
        completed = sum(1 for a in self.actions if a.status == ActionStatus.COMPLETED)
        failed = sum(1 for a in self.actions if a.status == ActionStatus.FAILED)
        pending = sum(1 for a in self.actions if a.status == ActionStatus.PENDING)
        
        return {
            'total_actions': total_actions,
            'completed': completed,
            'failed': failed,
            'pending': pending,
            'completion_rate': completed / total_actions if total_actions > 0 else 0,
            'total_duration': sum(a.duration for a in self.actions),
            'estimated_success_probability': self._calculate_success_probability()
        }
    
    def _calculate_success_probability(self) -> float:
        """计算整体成功概率"""
        if not self.actions:
            return 1.0
        
        probability = 1.0
        for action in self.actions:
            probability *= action.success_probability
        
        return probability
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'actions': [action.to_dict() for action in self.actions],
            'initial_state': self.initial_state,
            'goal_state': self.goal_state,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'statistics': self.get_statistics()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionSequence':
        """从字典创建ActionSequence对象"""
        actions = [Action.from_dict(action_data) for action_data in data['actions']]
        
        return cls(
            id=data['id'],
            actions=actions,
            initial_state=data.get('initial_state', {}),
            goal_state=data.get('goal_state', {}),
            metadata=data.get('metadata', {}),
            created_at=data.get('created_at', time.time())
        )
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ActionSequence':
        """从JSON字符串创建ActionSequence对象"""
        data = json.loads(json_str)
        return cls.from_dict(data)