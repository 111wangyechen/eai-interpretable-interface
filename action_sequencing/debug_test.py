#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细调试测试脚本 - 用于诊断Action Sequencing问题
"""

import sys
import os
import logging
from typing import Dict, Any

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from action_data import Action, ActionType
from state_manager import StateManager, EnvironmentState, StateTransition

# 设置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def debug_action_execution():
    """详细调试动作执行问题"""
    print("=" * 60)
    print("🔍 调试动作执行问题")
    print("=" * 60)
    
    # 创建测试动作
    action = Action(
        id="test_action_1",
        name="TestAction",
        action_type=ActionType.NAVIGATION,
        parameters={"target": "kitchen"},
        preconditions=["agent_at_living_room=True"],
        effects=["agent_at_kitchen=True"],
        duration=1.0
    )
    
    print(f"📋 动作信息:")
    print(f"   ID: {action.id}")
    print(f"   名称: {action.name}")
    print(f"   类型: {action.action_type}")
    print(f"   前置条件: {action.preconditions}")
    print(f"   效果: {action.effects}")
    
    # 测试不同的状态格式
    test_states = [
        {"agent_at_living_room": True},  # 原始布尔值
        {"agent_at_living_room": "True"},  # 字符串格式
        {"agent_at_living_room": True, "agent_at_kitchen": False},  # 完整状态
        {"agent_at_living_room": "True", "agent_at_kitchen": "False"},  # 字符串完整状态
    ]
    
    for i, state in enumerate(test_states, 1):
        print(f"\n🧪 测试状态 {i}: {state}")
        
        # 检查前置条件
        can_execute = action.can_execute(state)
        print(f"   前置条件检查结果: {can_execute}")
        
        if can_execute:
            try:
                new_state = action.execute(state)
                print(f"   ✅ 执行成功: {new_state}")
            except Exception as e:
                print(f"   ❌ 执行失败: {e}")
        else:
            print(f"   ⚠️  前置条件不满足，无法执行")

def debug_state_transition():
    """调试状态转换问题"""
    print("\n" + "=" * 60)
    print("🔍 调试状态转换问题")
    print("=" * 60)
    
    # 创建状态管理器
    state_manager = StateManager()
    
    # 创建转换
    transition = StateTransition(
        from_state={"agent_location": "start"},
        to_state={"agent_location": "kitchen"},
        action_name="move_action",
        preconditions=["agent_at_start=True"],
        effects=["agent_at_kitchen=True"]
    )
    
    print(f"📋 转换信息:")
    print(f"   动作名称: {transition.action_name}")
    print(f"   前置条件: {transition.preconditions}")
    print(f"   效果: {transition.effects}")
    
    state_manager.add_transition(transition)
    
    # 测试不同状态
    test_states = [
        {"agent_location": "start", "agent_at_start": True},
        {"agent_location": "start", "agent_at_start": "True"},
        {"agent_location": "start"},
    ]
    
    for i, state_dict in enumerate(test_states, 1):
        print(f"\n🧪 测试状态 {i}: {state_dict}")
        
        # 更新状态
        state_manager.update_state(state_dict)
        current_state = state_manager.get_current_state()
        print(f"   当前状态: {current_state.to_dict()}")
        
        # 检查转换适用性
        is_applicable = transition.is_applicable(current_state.get_state_dict())
        print(f"   转换适用性: {is_applicable}")
        
        if is_applicable:
            try:
                result = state_manager.apply_action("move_action")
                print(f"   ✅ 应用成功: {result}")
                new_state = state_manager.get_current_state()
                print(f"   新状态: {new_state.to_dict()}")
            except Exception as e:
                print(f"   ❌ 应用失败: {e}")
        else:
            print(f"   ⚠️  转换不适用")

def debug_planning():
    """调试规划问题"""
    print("\n" + "=" * 60)
    print("🔍 调试规划问题")
    print("=" * 60)
    
    from action_planner import ActionPlanner
    from action_sequencer import SequencingRequest
    
    # 创建规划器
    planner = ActionPlanner()
    
    # 创建简单的动作
    actions = [
        Action(
            id="move_to_kitchen",
            name="MoveToKitchen",
            action_type=ActionType.NAVIGATION,
            parameters={"target": "kitchen"},
            preconditions=["agent_at_living_room=True"],
            effects=["agent_at_living_room=False", "agent_at_kitchen=True"],
            duration=2.0
        )
    ]
    
    # 测试请求
    request = SequencingRequest(
        initial_state={"agent_at_living_room": "True", "agent_at_kitchen": "False"},
        goal_state={"agent_at_kitchen": "True"},
        available_actions=actions
    )
    
    print(f"📋 规划请求:")
    print(f"   初始状态: {request.initial_state}")
    print(f"   目标状态: {request.goal_state}")
    print(f"   可用动作数: {len(request.available_actions)}")
    
    for action in request.available_actions:
        print(f"     - {action.id}: {action.preconditions} -> {action.effects}")
    
    try:
        print(f"\n🧪 开始规划...")
        result = planner.plan(request)
        
        if result and result.action_sequence:
            print(f"   ✅ 规划成功!")
            print(f"   序列长度: {len(result.action_sequence)}")
            print(f"   总成本: {result.total_cost}")
            print(f"   动作序列: {[action.id for action in result.action_sequence]}")
        else:
            print(f"   ❌ 规划失败: 无解")
            
    except Exception as e:
        print(f"   ❌ 规划异常: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🚀 Action Sequencing 详细调试测试")
    print("=" * 60)
    
    try:
        # 调试各个组件
        debug_action_execution()
        debug_state_transition()
        debug_planning()
        
        print("\n" + "=" * 60)
        print("✅ 调试测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 调试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()