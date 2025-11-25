#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BEHAVIOR官方动作库
定义标准的BEHAVIOR动作集，包括导航、操作、感知等多种动作类型
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

from .action_data import Action, ActionType, ActionStatus


@dataclass
class ActionDefinition:
    """动作定义数据类"""
    name: str
    action_type: ActionType
    description: str
    parameters_schema: Dict[str, Dict[str, Any]]
    preconditions: List[str]
    effects: List[str]
    default_duration: float = 1.0
    default_success_prob: float = 0.95
    examples: List[Dict[str, Any]] = field(default_factory=list)


class BEHAVIORActionLibrary:
    """BEHAVIOR动作库类"""
    
    def __init__(self):
        """初始化BEHAVIOR动作库"""
        self.actions: Dict[str, ActionDefinition] = {}
        self._initialize_standard_actions()
    
    def _initialize_standard_actions(self):
        """初始化标准动作库"""
        # 导航类动作
        self._add_navigation_actions()
        
        # 操作类动作
        self._add_manipulation_actions()
        
        # 感知类动作
        self._add_perception_actions()
        
        # 通信类动作
        self._add_communication_actions()
        
        # 等待类动作
        self._add_wait_actions()
        
        # 条件类动作
        self._add_conditional_actions()
    
    def _add_navigation_actions(self):
        """添加导航类动作"""
        navigation_actions = [
            ActionDefinition(
                name="WalkToLocation",
                action_type=ActionType.NAVIGATION,
                description="走到指定位置",
                parameters_schema={
                    "target_location": {
                        "type": "string",
                        "required": True,
                        "description": "目标位置名称或坐标"
                    },
                    "approach_distance": {
                        "type": "float",
                        "required": False,
                        "default": 0.5,
                        "description": "接近目标的距离阈值"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "agent.energy > 0.1"
                ],
                effects=[
                    "agent.location = target_location",
                    "agent.energy -= 0.01"
                ],
                default_duration=2.0,
                examples=[
                    {"parameters": {"target_location": "kitchen"}},
                    {"parameters": {"target_location": "living_room", "approach_distance": 0.3}}
                ]
            ),
            ActionDefinition(
                name="NavigateToObject",
                action_type=ActionType.NAVIGATION,
                description="导航到指定物体附近",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "目标物体ID"
                    },
                    "distance": {
                        "type": "float",
                        "required": False,
                        "default": 1.0,
                        "description": "与物体的距离"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "exists(object_id)",
                    "agent.energy > 0.1"
                ],
                effects=[
                    "agent.location = object_location(object_id)",
                    "agent.energy -= 0.01"
                ],
                default_duration=3.0,
                examples=[
                    {"parameters": {"object_id": "table_1"}},
                    {"parameters": {"object_id": "fridge", "distance": 0.8}}
                ]
            ),
            ActionDefinition(
                name="TurnTowards",
                action_type=ActionType.NAVIGATION,
                description="转身朝向指定方向或物体",
                parameters_schema={
                    "target": {
                        "type": ["string", "object"],
                        "required": True,
                        "description": "目标物体ID或方向"
                    }
                },
                preconditions=[
                    "agent.alive == True"
                ],
                effects=[
                    "agent.orientation = target_orientation",
                    "agent.energy -= 0.005"
                ],
                default_duration=0.5,
                examples=[
                    {"parameters": {"target": "door_1"}},
                    {"parameters": {"target": "north"}}
                ]
            )
        ]
        
        for action_def in navigation_actions:
            self.actions[action_def.name] = action_def
    
    def _add_manipulation_actions(self):
        """添加操作类动作"""
        manipulation_actions = [
            ActionDefinition(
                name="GraspObject",
                action_type=ActionType.MANIPULATION,
                description="抓取指定物体",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要抓取的物体ID"
                    },
                    "grasp_type": {
                        "type": "string",
                        "required": False,
                        "default": "power_grip",
                        "description": "抓取类型"
                    },
                    "hand": {
                        "type": "string",
                        "required": False,
                        "default": "right",
                        "description": "使用的手（left/right/both）"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "exists(object_id)",
                    "is_reachable(object_id)",
                    "agent.hands_free(hand) == True"
                ],
                effects=[
                    "agent.holding_right_hand = object_id",
                    "object.is_held = True",
                    "agent.energy -= 0.02"
                ],
                default_duration=1.0,
                examples=[
                    {"parameters": {"object_id": "cup_1"}},
                    {"parameters": {"object_id": "book_1", "hand": "left"}}
                ]
            ),
            ActionDefinition(
                name="ReleaseObject",
                action_type=ActionType.MANIPULATION,
                description="释放手中的物体",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要释放的物体ID"
                    },
                    "hand": {
                        "type": "string",
                        "required": False,
                        "default": "right",
                        "description": "使用的手（left/right）"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    f"agent.holding_{'right' if '{hand}' == 'right' else 'left'}_hand == object_id"
                ],
                effects=[
                    f"agent.holding_{'right' if '{hand}' == 'right' else 'left'}_hand = None",
                    "object.is_held = False",
                    "object.location = agent.location",
                    "agent.energy -= 0.01"
                ],
                default_duration=0.5,
                examples=[
                    {"parameters": {"object_id": "cup_1"}},
                    {"parameters": {"object_id": "book_1", "hand": "left"}}
                ]
            ),
            ActionDefinition(
                name="OpenObject",
                action_type=ActionType.MANIPULATION,
                description="打开指定物体（如门、抽屉、容器等）",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要打开的物体ID"
                    },
                    "open_percentage": {
                        "type": "float",
                        "required": False,
                        "default": 1.0,
                        "description": "打开程度（0.0-1.0）"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "exists(object_id)",
                    "is_reachable(object_id)",
                    "can_open(object_id) == True",
                    "object.is_open == False"
                ],
                effects=[
                    "object.is_open = True",
                    "object.open_percentage = open_percentage",
                    "agent.energy -= 0.015"
                ],
                default_duration=0.8,
                examples=[
                    {"parameters": {"object_id": "fridge"}},
                    {"parameters": {"object_id": "drawer_1", "open_percentage": 0.5}}
                ]
            ),
            ActionDefinition(
                name="CloseObject",
                action_type=ActionType.MANIPULATION,
                description="关闭指定物体",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要关闭的物体ID"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "exists(object_id)",
                    "is_reachable(object_id)",
                    "object.is_open == True"
                ],
                effects=[
                    "object.is_open = False",
                    "object.open_percentage = 0.0",
                    "agent.energy -= 0.015"
                ],
                default_duration=0.8,
                examples=[
                    {"parameters": {"object_id": "door_1"}},
                    {"parameters": {"object_id": "window_2"}}
                ]
            ),
            ActionDefinition(
                name="PickupObject",
                action_type=ActionType.MANIPULATION,
                description="拾取物体并保持在手中",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要拾取的物体ID"
                    },
                    "hand": {
                        "type": "string",
                        "required": False,
                        "default": "right",
                        "description": "使用的手"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "exists(object_id)",
                    "is_reachable(object_id)",
                    "agent.hands_free(hand) == True",
                    "object.weight < agent.strength"
                ],
                effects=[
                    f"agent.holding_{'right' if '{hand}' == 'right' else 'left'}_hand = object_id",
                    "object.is_held = True",
                    "agent.energy -= 0.03"
                ],
                default_duration=1.2,
                examples=[
                    {"parameters": {"object_id": "apple_1"}},
                    {"parameters": {"object_id": "key_1", "hand": "left"}}
                ]
            ),
            ActionDefinition(
                name="PlaceObject",
                action_type=ActionType.MANIPULATION,
                description="将手中的物体放置到指定位置",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要放置的物体ID"
                    },
                    "target_location": {
                        "type": "string",
                        "required": True,
                        "description": "目标位置或表面"
                    },
                    "hand": {
                        "type": "string",
                        "required": False,
                        "default": "right",
                        "description": "使用的手"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    f"agent.holding_{'right' if '{hand}' == 'right' else 'left'}_hand == object_id",
                    "exists(target_location)",
                    "is_reachable(target_location)"
                ],
                effects=[
                    f"agent.holding_{'right' if '{hand}' == 'right' else 'left'}_hand = None",
                    "object.is_held = False",
                    "object.location = target_location",
                    "agent.energy -= 0.025"
                ],
                default_duration=1.5,
                examples=[
                    {"parameters": {"object_id": "cup_1", "target_location": "table_1"}},
                    {"parameters": {"object_id": "book_1", "target_location": "shelf_2", "hand": "left"}}
                ]
            )
        ]
        
        for action_def in manipulation_actions:
            self.actions[action_def.name] = action_def
    
    def _add_perception_actions(self):
        """添加感知类动作"""
        perception_actions = [
            ActionDefinition(
                name="LookAt",
                action_type=ActionType.PERCEPTION,
                description="查看指定物体或区域",
                parameters_schema={
                    "target": {
                        "type": ["string", "object"],
                        "required": True,
                        "description": "查看目标"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "is_visible(target)"
                ],
                effects=[
                    "agent.last_observed = target",
                    "agent.has_visual_info(target) = True",
                    "agent.energy -= 0.005"
                ],
                default_duration=0.5,
                examples=[
                    {"parameters": {"target": "window"}},
                    {"parameters": {"target": "person_1"}}
                ]
            ),
            ActionDefinition(
                name="ListenTo",
                action_type=ActionType.PERCEPTION,
                description="聆听指定声音来源",
                parameters_schema={
                    "source": {
                        "type": ["string", "object"],
                        "required": True,
                        "description": "声音来源"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "is_audible(source)"
                ],
                effects=[
                    "agent.last_heard = source",
                    "agent.has_audio_info(source) = True",
                    "agent.energy -= 0.005"
                ],
                default_duration=1.0,
                examples=[
                    {"parameters": {"source": "radio"}},
                    {"parameters": {"source": "person_2"}}
                ]
            ),
            ActionDefinition(
                name="InspectObject",
                action_type=ActionType.PERCEPTION,
                description="仔细检查物体的详细信息",
                parameters_schema={
                    "object_id": {
                        "type": "string",
                        "required": True,
                        "description": "要检查的物体ID"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "exists(object_id)",
                    "is_reachable(object_id)"
                ],
                effects=[
                    "agent.has_detailed_info(object_id) = True",
                    "agent.last_inspected = object_id",
                    "agent.energy -= 0.01"
                ],
                default_duration=2.0,
                examples=[
                    {"parameters": {"object_id": "document_1"}},
                    {"parameters": {"object_id": "device_1"}}
                ]
            )
        ]
        
        for action_def in perception_actions:
            self.actions[action_def.name] = action_def
    
    def _add_communication_actions(self):
        """添加通信类动作"""
        communication_actions = [
            ActionDefinition(
                name="Speak",
                action_type=ActionType.COMMUNICATION,
                description="说话或发出声音",
                parameters_schema={
                    "message": {
                        "type": "string",
                        "required": True,
                        "description": "要说的内容"
                    },
                    "target": {
                        "type": ["string", "object"],
                        "required": False,
                        "default": "everyone",
                        "description": "交流目标"
                    },
                    "volume": {
                        "type": "string",
                        "required": False,
                        "default": "normal",
                        "description": "音量级别"
                    }
                },
                preconditions=[
                    "agent.alive == True"
                ],
                effects=[
                    "agent.last_spoke = message",
                    "agent.energy -= 0.01"
                ],
                default_duration=1.5,
                examples=[
                    {"parameters": {"message": "Hello!"}},
                    {"parameters": {"message": "Follow me", "target": "person_1", "volume": "loud"}}
                ]
            ),
            ActionDefinition(
                name="Gesture",
                action_type=ActionType.COMMUNICATION,
                description="做出手势动作",
                parameters_schema={
                    "gesture_type": {
                        "type": "string",
                        "required": True,
                        "description": "手势类型"
                    },
                    "target": {
                        "type": ["string", "object"],
                        "required": False,
                        "default": "everyone",
                        "description": "手势目标"
                    }
                },
                preconditions=[
                    "agent.alive == True",
                    "agent.hands_free() == True"
                ],
                effects=[
                    "agent.last_gesture = gesture_type",
                    "agent.energy -= 0.008"
                ],
                default_duration=0.8,
                examples=[
                    {"parameters": {"gesture_type": "wave"}},
                    {"parameters": {"gesture_type": "point", "target": "door"}}
                ]
            )
        ]
        
        for action_def in communication_actions:
            self.actions[action_def.name] = action_def
    
    def _add_wait_actions(self):
        """添加等待类动作"""
        wait_actions = [
            ActionDefinition(
                name="Wait",
                action_type=ActionType.WAIT,
                description="等待指定时间",
                parameters_schema={
                    "duration": {
                        "type": "float",
                        "required": True,
                        "description": "等待时长（秒）"
                    }
                },
                preconditions=[
                    "agent.alive == True"
                ],
                effects=[
                    "world.time += duration",
                    "agent.energy -= duration * 0.001"
                ],
                default_duration=1.0,
                examples=[
                    {"parameters": {"duration": 2.0}},
                    {"parameters": {"duration": 5.0}}
                ]
            ),
            ActionDefinition(
                name="WaitForCondition",
                action_type=ActionType.WAIT,
                description="等待直到条件满足",
                parameters_schema={
                    "condition": {
                        "type": "string",
                        "required": True,
                        "description": "等待条件表达式"
                    },
                    "max_wait_time": {
                        "type": "float",
                        "required": False,
                        "default": 10.0,
                        "description": "最大等待时间"
                    }
                },
                preconditions=[
                    "agent.alive == True"
                ],
                effects=[
                    "world.time += actual_wait_time",
                    "agent.energy -= actual_wait_time * 0.001"
                ],
                default_duration=5.0,
                examples=[
                    {"parameters": {"condition": "door_1.is_open == True"}},
                    {"parameters": {"condition": "person_1.arrived == True", "max_wait_time": 20.0}}
                ]
            )
        ]
        
        for action_def in wait_actions:
            self.actions[action_def.name] = action_def
    
    def _add_conditional_actions(self):
        """添加条件类动作"""
        conditional_actions = [
            ActionDefinition(
                name="IfThenElse",
                action_type=ActionType.CONDITIONAL,
                description="条件执行动作",
                parameters_schema={
                    "condition": {
                        "type": "string",
                        "required": True,
                        "description": "条件表达式"
                    },
                    "then_actions": {
                        "type": "array",
                        "required": True,
                        "description": "条件为真时执行的动作列表"
                    },
                    "else_actions": {
                        "type": "array",
                        "required": False,
                        "default": [],
                        "description": "条件为假时执行的动作列表"
                    }
                },
                preconditions=[
                    "agent.alive == True"
                ],
                effects=[
                    "agent.executed_conditional = True",
                    "agent.last_condition_result = condition_result"
                ],
                default_duration=0.2,
                examples=[
                    {
                        "parameters": {
                            "condition": "light.is_on == True",
                            "then_actions": [{"name": "NavigateToObject", "parameters": {"object_id": "light"}}],
                            "else_actions": [{"name": "Wait", "parameters": {"duration": 1.0}}]
                        }
                    }
                ]
            )
        ]
        
        for action_def in conditional_actions:
            self.actions[action_def.name] = action_def
    
    def get_action(self, name: str) -> Optional[ActionDefinition]:
        """
        获取动作定义
        
        Args:
            name: 动作名称
            
        Returns:
            ActionDefinition或None
        """
        return self.actions.get(name)
    
    def create_action(self, name: str, parameters: Dict[str, Any] = None) -> Optional[Action]:
        """创建动作实例
        
        Args:
            name: 动作名称
            parameters: 动作参数
            
        Returns:
            创建的动作实例，如果动作不存在则返回None
        """
        if name not in self.actions:
            return None
        
        action_def = self.actions[name]
        
        # 验证并处理参数
        validated_params = self._validate_parameters(action_def, parameters or {})
        
        # 生成唯一ID
        action_id = f"{name}_{int(time.time() * 1000)}"
        
        # 创建动作实例
        action = Action(
            id=action_id,
            name=action_def.name,
            action_type=action_def.action_type,
            parameters=validated_params,
            preconditions=action_def.preconditions.copy(),
            effects=action_def.effects.copy(),
            duration=action_def.default_duration,
            success_probability=action_def.default_success_prob
        )
        
        # 添加元数据
        action.metadata['definition'] = action_def.name
        action.metadata['creation_time'] = time.time()
        action.metadata['official_behavior_action'] = True
        
        # 增强前置条件，根据参数动态生成前置条件
        self._enhance_preconditions(action)
        
        return action
    
    def _enhance_preconditions(self, action: Action):
        """根据参数和动作类型增强前置条件
        
        Args:
            action: 要增强前置条件的动作实例
        """
        # 根据动作名称和参数动态生成前置条件
        if action.name == "GraspObject" and "hand" in action.parameters:
            hand = action.parameters["hand"]
            # 移除通用前置条件并添加具体的手部前置条件
            action.preconditions = [pc for pc in action.preconditions if "agent.hands_free" not in pc]
            if hand == "right":
                action.preconditions.append("agent.right_hand_free == True")
            elif hand == "left":
                action.preconditions.append("agent.left_hand_free == True")
            elif hand == "both":
                action.preconditions.append("agent.right_hand_free == True")
                action.preconditions.append("agent.left_hand_free == True")
            
            # 增强object_id相关的前置条件
            if "object_id" in action.parameters:
                obj_id = action.parameters["object_id"]
                action.preconditions.append(f"exists({obj_id}) == True")
                action.preconditions.append(f"object_type({obj_id}) != 'fixed'")
                action.preconditions.append(f"object_weight({obj_id}) < agent.strength")
                
                # 基于物体类型添加更具体的前置条件
                action.preconditions.append(f"can_grasp_object({obj_id}) == True")
        
        elif action.name == "NavigateToObject" and "object_id" in action.parameters:
            obj_id = action.parameters["object_id"]
            action.preconditions.append(f"object_reachable({obj_id}) == True")
            action.preconditions.append(f"agent.energy > 0.1")
        
        # 添加通用的安全前置条件
        safety_preconditions = [
            "agent.alive == True",
            "agent.conscious == True"
        ]
        
        for condition in safety_preconditions:
            if condition not in action.preconditions:
                action.preconditions.append(condition)
    
    def validate_action_preconditions(self, action: Action, state: Dict[str, Any]) -> Dict[str, bool]:
        """验证动作在当前状态下的所有前置条件
        
        Args:
            action: 要验证的动作
            state: 当前环境状态
            
        Returns:
            前置条件验证结果字典，键为前置条件，值为验证结果
        """
        results = {}
        for precondition in action.preconditions:
            results[precondition] = self._evaluate_precondition(precondition, state, action)
        return results
    
    def _evaluate_precondition(self, precondition: str, state: Dict[str, Any], action: Action) -> bool:
        """评估单个前置条件
        
        Args:
            precondition: 前置条件字符串
            state: 当前环境状态
            action: 相关动作
            
        Returns:
            前置条件是否满足
        """
        try:
            # 处理特殊函数调用格式，如 exists(object_id), is_reachable(object_id) 等
            if precondition.startswith("exists(") and precondition.endswith(")"):
                obj_id = precondition[7:-1].strip()
                # 处理参数引用
                if obj_id.startswith("{}") and obj_id.endswith("}"):
                    param_name = obj_id[2:-1].strip()
                    obj_id = action.parameters.get(param_name, "")
                return obj_id in state or f"object_{obj_id}" in state
            
            elif precondition.startswith("is_reachable(") and precondition.endswith(")"):
                obj_id = precondition[13:-1].strip()
                # 检查对象是否在可到达范围内
                if f"object_{obj_id}_reachable" in state:
                    return state[f"object_{obj_id}_reachable"]
                # 简单判断：如果存在且距离合理，则认为可到达
                return obj_id in state and state.get(f"distance_to_{obj_id}", float('inf')) < 2.0
            
            elif precondition.startswith("object_type(") and ":=" in precondition:
                # 例如: object_type(cup_1) != 'fixed'
                parts = precondition.split(":=")
                if len(parts) == 2:
                    obj_expr = parts[0].strip()
                    expected_type = parts[1].strip().strip("'")
                    if obj_expr.startswith("object_type(") and obj_expr.endswith(")"):
                        obj_id = obj_expr[12:-1].strip()
                        actual_type = state.get(f"object_{obj_id}_type", "")
                        return actual_type != expected_type
            
            # 处理标准比较操作
            elif '==' in precondition:
                key, value = precondition.split('==', 1)
                key = key.strip()
                value = value.strip().strip("'\" ")
                
                # 尝试转换为布尔值
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                
                return state.get(key) == value
            
            elif '!=' in precondition:
                key, value = precondition.split('!=', 1)
                key = key.strip()
                value = value.strip().strip("'\" ")
                return state.get(key) != value
            
            elif '>' in precondition:
                key, value = precondition.split('>', 1)
                key = key.strip()
                try:
                    return float(state.get(key, 0)) > float(value.strip())
                except:
                    return False
            
            elif '<' in precondition:
                key, value = precondition.split('<', 1)
                key = key.strip()
                try:
                    return float(state.get(key, 0)) < float(value.strip())
                except:
                    return False
            
            # 简单的布尔条件
            else:
                return state.get(precondition.strip(), False)
        except Exception:
            # 如果解析失败，返回False
            return False
    
    def _validate_parameters(self, action_def: ActionDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证动作参数
        
        Args:
            action_def: 动作定义
            parameters: 传入的参数
            
        Returns:
            验证后的参数
        """
        validated = {}
        
        for param_name, param_schema in action_def.parameters_schema.items():
            # 检查参数是否必需
            if param_schema.get('required', False) and param_name not in parameters:
                if 'default' in param_schema:
                    validated[param_name] = param_schema['default']
                else:
                    # 如果是必需参数且没有默认值，则使用None
                    validated[param_name] = None
            elif param_name in parameters:
                # 验证类型
                expected_type = param_schema.get('type')
                if expected_type:
                    # 简单类型验证
                    param_value = parameters[param_name]
                    if isinstance(expected_type, str):
                        # 单一类型
                        if expected_type == 'string' and not isinstance(param_value, str):
                            validated[param_name] = str(param_value)
                        elif expected_type == 'float' and not isinstance(param_value, (int, float)):
                            try:
                                validated[param_name] = float(param_value)
                            except:
                                validated[param_name] = param_schema.get('default', None)
                        elif expected_type == 'int' and not isinstance(param_value, int):
                            try:
                                validated[param_name] = int(param_value)
                            except:
                                validated[param_name] = param_schema.get('default', None)
                        elif expected_type == 'bool' and not isinstance(param_value, bool):
                            validated[param_name] = bool(param_value)
                        else:
                            validated[param_name] = param_value
                    elif isinstance(expected_type, list):
                        # 多类型
                        validated[param_name] = param_value
                else:
                    validated[param_name] = parameters[param_name]
            elif 'default' in param_schema:
                validated[param_name] = param_schema['default']
        
        return validated
    
    def get_actions_by_type(self, action_type: ActionType) -> List[ActionDefinition]:
        """
        获取指定类型的所有动作
        
        Args:
            action_type: 动作类型
            
        Returns:
            动作定义列表
        """
        return [action for action in self.actions.values() if action.action_type == action_type]
    
    def save_to_file(self, file_path: str):
        """
        保存动作库到文件
        
        Args:
            file_path: 文件路径
        """
        actions_data = []
        for action_def in self.actions.values():
            action_dict = {
                'name': action_def.name,
                'action_type': action_def.action_type.value,
                'description': action_def.description,
                'parameters_schema': action_def.parameters_schema,
                'preconditions': action_def.preconditions,
                'effects': action_def.effects,
                'default_duration': action_def.default_duration,
                'default_success_prob': action_def.default_success_prob,
                'examples': action_def.examples
            }
            actions_data.append(action_dict)
        
        # 确保目录存在
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 保存到JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(actions_data, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, file_path: str):
        """
        从文件加载动作库
        
        Args:
            file_path: 文件路径
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"动作库文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            actions_data = json.load(f)
        
        self.actions.clear()
        for action_data in actions_data:
            action_def = ActionDefinition(
                name=action_data['name'],
                action_type=ActionType(action_data['action_type']),
                description=action_data['description'],
                parameters_schema=action_data['parameters_schema'],
                preconditions=action_data['preconditions'],
                effects=action_data['effects'],
                default_duration=action_data.get('default_duration', 1.0),
                default_success_prob=action_data.get('default_success_prob', 0.95),
                examples=action_data.get('examples', [])
            )
            self.actions[action_def.name] = action_def


# 导入必要的模块
import time

# 创建全局动作库实例
global_action_library = BEHAVIORActionLibrary()


def get_behavior_action_library() -> BEHAVIORActionLibrary:
    """获取全局BEHAVIOR动作库实例
    
    Returns:
        BEHAVIOR动作库实例
    """
    return global_action_library

def create_behavior_action(name: str, parameters: Dict[str, Any] = None) -> Optional[Action]:
    """创建BEHAVIOR动作实例
    
    Args:
        name: 动作名称
        parameters: 动作参数
        
    Returns:
        创建的动作实例，如果动作不存在则返回None
    """
    action = global_action_library.create_action(name, parameters)
    if action:
        # 标记为官方BEHAVIOR动作
        action.metadata['is_official_behavior_action'] = True
    return action

def register_custom_action(action_def: ActionDefinition):
    """注册自定义动作到全局动作库
    
    Args:
        action_def: 动作定义
    """
    # 确保自定义动作不会覆盖官方动作
    if action_def.name in global_action_library.actions:
        official_action = global_action_library.actions[action_def.name]
        # 在自定义动作名称后添加后缀以避免冲突
        action_def.name = f"{action_def.name}_custom"
    global_action_library.actions[action_def.name] = action_def

def validate_action_against_behavior_library(action: Action) -> Dict[str, Any]:
    """验证动作是否符合BEHAVIOR动作库规范
    
    Args:
        action: 要验证的动作
        
    Returns:
        验证结果字典，包含有效性和详细信息
    """
    result = {
        'is_valid': True,  # 默认所有动作都是有效的，即使不在官方库中
        'is_official_action': False,
        'issues': [],
        'suggestions': []
    }
    
    # 检查是否为官方动作
    library = get_behavior_action_library()
    official_def = library.get_action(action.name)
    
    if official_def:
        result['is_official_action'] = True
        
        # 验证参数是否符合官方定义
        for param_name, param_schema in official_def.parameters_schema.items():
            if param_schema.get('required', False) and param_name not in action.parameters:
                result['issues'].append(f"Missing required parameter: {param_name}")
        
        # 验证前置条件是否完整
        if len(action.preconditions) < len(official_def.preconditions):
            result['issues'].append("Missing required preconditions")
        
        # 验证动作类型是否匹配
        if action.action_type != official_def.action_type:
            result['issues'].append(f"Action type mismatch: expected {official_def.action_type}, got {action.action_type}")
        
        # 如果有问题，标记为无效
        if result['issues']:
            result['is_valid'] = False
    else:
        # 非官方动作只记录警告，不标记为无效
        result['issues'].append(f"Action '{action.name}' not found in BEHAVIOR official library")
        # 寻找相似的官方动作作为建议
        similar_actions = []
        for def_name in library.actions:
            if def_name.lower() == action.name.lower():
                similar_actions.append(def_name)
        if similar_actions:
            result['suggestions'].append(f"Did you mean: {', '.join(similar_actions)}")
    
    return result