#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境状态管理器
负责管理环境状态、状态转换和状态验证
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import copy
import time


class StateType(Enum):
    """状态类型枚举"""
    BOOLEAN = "boolean"      # 布尔状态
    NUMERIC = "numeric"      # 数值状态
    LOCATION = "location"    # 位置状态
    INVENTORY = "inventory"   # 库存状态
    RELATION = "relation"    # 关系状态
    TEMPORAL = "temporal"    # 时序状态


@dataclass
class StateVariable:
    """状态变量数据类"""
    name: str
    value: Any
    state_type: StateType
    domain: Optional[List[Any]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """后处理初始化"""
        if self.metadata is None:
            self.metadata = {}
    
    def is_valid(self) -> bool:
        """验证状态变量值是否有效"""
        if self.state_type == StateType.BOOLEAN:
            return isinstance(self.value, bool)
        elif self.state_type == StateType.NUMERIC:
            if not isinstance(self.value, (int, float)):
                return False
            if self.min_value is not None and self.value < self.min_value:
                return False
            if self.max_value is not None and self.value > self.max_value:
                return False
            return True
        elif self.state_type == StateType.LOCATION:
            return isinstance(self.value, (str, tuple, list))
        elif self.state_type == StateType.INVENTORY:
            return isinstance(self.value, dict)
        elif self.state_type == StateType.RELATION:
            return isinstance(self.value, (str, tuple))
        elif self.state_type == StateType.TEMPORAL:
            return isinstance(self.value, (int, float))
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'value': self.value,
            'state_type': self.state_type.value,
            'domain': self.domain,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'description': self.description,
            'metadata': self.metadata
        }


@dataclass
class StateTransition:
    """状态转换数据类"""
    from_state: Dict[str, Any]
    to_state: Dict[str, Any]
    action_name: str
    probability: float = 1.0
    cost: float = 1.0
    duration: float = 1.0
    preconditions: List[str] = field(default_factory=list)
    effects: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """后处理初始化"""
        if self.preconditions is None:
            self.preconditions = []
        if self.effects is None:
            self.effects = []
        if self.metadata is None:
            self.metadata = {}
    
    def is_applicable(self, current_state: Dict[str, Any]) -> bool:
        """检查转换是否适用于当前状态"""
        for precondition in self.preconditions:
            if not self._evaluate_condition(precondition, current_state):
                return False
        return True
    
    def _evaluate_condition(self, condition: str, state: Dict[str, Any]) -> bool:
        """评估条件"""
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
                return state.get(condition.strip(), False)
        except Exception:
            return False


class EnvironmentState:
    """环境状态类"""
    
    def __init__(self, state_dict: Optional[Dict[str, Any]] = None):
        """
        初始化环境状态
        
        Args:
            state_dict: 初始状态字典
        """
        self.state_variables: Dict[str, StateVariable] = {}
        self.state_history: List[Dict[str, Any]] = []
        self.transition_history: List[StateTransition] = []
        self.timestamp = time.time()
        
        if state_dict:
            self.load_state(state_dict)
    
    def add_variable(self, variable: StateVariable):
        """添加状态变量"""
        self.state_variables[variable.name] = variable
    
    def get_variable(self, name: str) -> Optional[StateVariable]:
        """获取状态变量"""
        return self.state_variables.get(name)
    
    def set_value(self, name: str, value: Any) -> bool:
        """设置状态变量值"""
        if name in self.state_variables:
            old_value = self.state_variables[name].value
            self.state_variables[name].value = value
            
            # 验证新值
            if not self.state_variables[name].is_valid():
                self.state_variables[name].value = old_value
                return False
            return True
        return False
    
    def get_value(self, name: str, default: Any = None) -> Any:
        """获取状态变量值"""
        if name in self.state_variables:
            return self.state_variables[name].value
        return default
    
    def get_state_dict(self) -> Dict[str, Any]:
        """获取状态字典"""
        return {name: var.value for name, var in self.state_variables.items()}
    
    def load_state(self, state_dict: Dict[str, Any]):
        """从字典加载状态"""
        # 保存当前状态到历史
        if self.state_variables:
            self.state_history.append(self.get_state_dict())
        
        # 清空当前状态
        self.state_variables.clear()
        
        # 创建新的状态变量
        for name, value in state_dict.items():
            # 根据值推断状态类型
            state_type = self._infer_state_type(value)
            variable = StateVariable(name=name, value=value, state_type=state_type)
            self.add_variable(variable)
    
    def _infer_state_type(self, value: Any) -> StateType:
        """推断状态类型"""
        if isinstance(value, bool):
            return StateType.BOOLEAN
        elif isinstance(value, (int, float)):
            return StateType.NUMERIC
        elif isinstance(value, str):
            # 简单的位置推断
            if any(loc in value.lower() for loc in ['room', 'kitchen', 'bedroom', 'bathroom']):
                return StateType.LOCATION
            return StateType.RELATION
        elif isinstance(value, dict):
            return StateType.INVENTORY
        elif isinstance(value, (list, tuple)):
            return StateType.LOCATION
        else:
            return StateType.RELATION
    
    def apply_transition(self, transition: StateTransition) -> bool:
        """应用状态转换"""
        if not transition.is_applicable(self.get_state_dict()):
            return False
        
        # 保存当前状态到历史
        self.state_history.append(self.get_state_dict())
        
        # 应用转换
        for key, value in transition.to_state.items():
            self.set_value(key, value)
        
        # 记录转换历史
        self.transition_history.append(transition)
        self.timestamp = time.time()
        
        return True
    
    def get_state_diff(self, other_state: Dict[str, Any]) -> Dict[str, Tuple[Any, Any]]:
        """获取状态差异"""
        current_state = self.get_state_dict()
        diff = {}
        
        all_keys = set(current_state.keys()) | set(other_state.keys())
        
        for key in all_keys:
            current_val = current_state.get(key)
            other_val = other_state.get(key)
            
            if current_val != other_val:
                diff[key] = (current_val, other_val)
        
        return diff
    
    def is_goal_achieved(self, goal_state: Dict[str, Any]) -> bool:
        """检查目标状态是否达成"""
        current_state = self.get_state_dict()
        
        # 添加类型检查，确保goal_state是字典类型
        if not isinstance(goal_state, dict):
            # 如果不是字典，记录错误并返回False
            print(f"Error: goal_state is not a dictionary, got {type(goal_state).__name__}")
            return False
        
        try:
            for key, goal_value in goal_state.items():
                current_value = current_state.get(key)
                
                if current_value != goal_value:
                    return False
        except Exception as e:
            # 捕获任何可能的异常
            print(f"Error checking goal state: {str(e)}")
            return False
        
        return True
    
    def get_valid_actions(self, transitions: List[StateTransition]) -> List[StateTransition]:
        """获取当前状态下可用的动作"""
        valid_actions = []
        current_state = self.get_state_dict()
        
        for transition in transitions:
            if transition.is_applicable(current_state):
                valid_actions.append(transition)
        
        return valid_actions
    
    def validate_state(self) -> List[str]:
        """验证状态，返回错误列表"""
        errors = []
        
        for name, variable in self.state_variables.items():
            if not variable.is_valid():
                errors.append(f"Invalid value for variable {name}: {variable.value}")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'state_variables': {name: var.to_dict() for name, var in self.state_variables.items()},
            'state_history': self.state_history,
            'transition_count': len(self.transition_history),
            'timestamp': self.timestamp
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)


class StateManager:
    """状态管理器类"""
    
    def __init__(self):
        """初始化状态管理器"""
        self.current_state = EnvironmentState()
        self.state_transitions: List[StateTransition] = []
        self.state_templates: Dict[str, Dict[str, Any]] = {}
        self.state_history: List[Dict[str, Any]] = []
        
        # 初始化时添加一个空状态到历史
        self.state_history.append({})
    
    def add_transition(self, transition: StateTransition):
        """添加状态转换"""
        self.state_transitions.append(transition)
    
    def add_state_template(self, name: str, state_dict: Dict[str, Any]):
        """添加状态模板"""
        self.state_templates[name] = state_dict
    
    def load_state_template(self, template_name: str) -> bool:
        """加载状态模板"""
        if template_name in self.state_templates:
            self.current_state.load_state(self.state_templates[template_name])
            return True
        return False
    
    def update_state(self, new_state: Dict[str, Any]):
        """更新当前状态"""
        # 保存当前状态到历史
        self.state_history.append(self.current_state.get_state_dict())
        
        # 加载新状态
        self.current_state.load_state(new_state)
    
    def get_current_state(self) -> EnvironmentState:
        """获取当前状态"""
        return self.current_state
    
    def apply_action(self, action_name: str, parameters: Optional[Dict[str, Any]] = None) -> bool:
        """应用动作"""
        # 查找匹配的转换
        applicable_transitions = []
        for transition in self.state_transitions:
            if transition.action_name == action_name:
                if transition.is_applicable(self.current_state.get_state_dict()):
                    applicable_transitions.append(transition)
        
        if not applicable_transitions:
            return False
        
        # 选择第一个适用的转换（简单策略）
        # 在实际应用中，可以使用更复杂的选择策略
        selected_transition = applicable_transitions[0]
        
        # 应用参数修改（如果有）
        if parameters:
            modified_transition = self._modify_transition_with_params(
                selected_transition, parameters
            )
            return self.current_state.apply_transition(modified_transition)
        
        return self.current_state.apply_transition(selected_transition)
    
    def _modify_transition_with_params(self, transition: StateTransition, 
                                     parameters: Dict[str, Any]) -> StateTransition:
        """使用参数修改转换"""
        # 创建转换的深拷贝
        new_transition = StateTransition(
            from_state=copy.deepcopy(transition.from_state),
            to_state=copy.deepcopy(transition.to_state),
            action_name=transition.action_name,
            probability=transition.probability,
            cost=transition.cost,
            duration=transition.duration,
            preconditions=copy.deepcopy(transition.preconditions),
            effects=copy.deepcopy(transition.effects),
            metadata=copy.deepcopy(transition.metadata)
        )
        
        # 应用参数
        for key, value in parameters.items():
            if key in new_transition.to_state:
                new_transition.to_state[key] = value
        
        return new_transition
    
    def get_possible_actions(self) -> List[str]:
        """获取可能的动作列表"""
        current_state = self.current_state.get_state_dict()
        possible_actions = set()
        
        for transition in self.state_transitions:
            if transition.is_applicable(current_state):
                possible_actions.add(transition.action_name)
        
        return list(possible_actions)
    
    def simulate_action(self, action_name: str, parameters: Optional[Dict[str, Any]] = None) -> Optional[EnvironmentState]:
        """模拟动作执行，返回新状态但不改变当前状态"""
        # 创建当前状态的副本
        simulated_state = EnvironmentState(self.current_state.get_state_dict())
        simulated_state.state_variables = copy.deepcopy(self.current_state.state_variables)
        
        # 查找并应用转换
        for transition in self.state_transitions:
            if transition.action_name == action_name:
                if transition.is_applicable(simulated_state.get_state_dict()):
                    if parameters:
                        modified_transition = self._modify_transition_with_params(
                            transition, parameters
                        )
                        simulated_state.apply_transition(modified_transition)
                    else:
                        simulated_state.apply_transition(transition)
                    return simulated_state
        
        return None
    
    def reset_to_initial_state(self, initial_state: Dict[str, Any]):
        """重置到初始状态"""
        self.current_state.load_state(initial_state)
    
    def get_state_statistics(self) -> Dict[str, Any]:
        """获取状态统计信息"""
        current_state_dict = self.current_state.get_state_dict()
        
        return {
            'total_variables': len(current_state_dict),
            'boolean_variables': sum(1 for var in self.current_state.state_variables.values() 
                                   if var.state_type == StateType.BOOLEAN),
            'numeric_variables': sum(1 for var in self.current_state.state_variables.values() 
                                   if var.state_type == StateType.NUMERIC),
            'location_variables': sum(1 for var in self.current_state.state_variables.values() 
                                    if var.state_type == StateType.LOCATION),
            'total_transitions': len(self.state_transitions),
            'possible_actions': self.get_possible_actions(),
            'state_history_length': len(self.current_state.state_history),
            'validation_errors': self.current_state.validate_state()
        }