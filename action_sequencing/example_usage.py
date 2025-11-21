#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Sequencing Module 使用示例
演示如何使用动作序列生成模块的各种功能

包含以下示例:
1. 基础动作序列生成
2. 多种规划算法比较
3. 数据集加载和处理
4. 复杂场景规划
5. 性能测试和优化

作者: EAI Challenge Team
"""

import sys
import os
import time
from typing import Dict, List, Any

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from action_sequencing import (
    ActionSequencer, ActionPlanner, StateManager, DataLoader,
    Action, ActionSequence, ActionType, ActionStatus,
    SequencingConfig, SequencingRequest, SequencingResponse,
    PlanningAlgorithm, HeuristicType,
    DatasetConfig, VirtualHomeRecord, BehaviorRecord,
    create_action_sequencer, create_data_loader, quick_sequence_generation
)


def example_1_basic_sequencing():
    """示例1: 基础动作序列生成"""
    print("=" * 60)
    print("示例1: 基础动作序列生成")
    print("=" * 60)
    
    # 定义可用动作
    actions = [
        Action(
            id="walk_to_kitchen",
            name="WalkToKitchen",
            action_type=ActionType.NAVIGATION,
            parameters={"target": "kitchen"},
            preconditions=["agent_in_living_room"],
            effects=["agent_in_kitchen"],
            duration=3.0,
            success_probability=0.95
        ),
        Action(
            id="pick_up_cup",
            name="PickUpCup",
            action_type=ActionType.MANIPULATION,
            parameters={"object": "cup"},
            preconditions=["agent_in_kitchen", "cup_on_counter"],
            effects=["holding_cup"],
            duration=1.5,
            success_probability=0.90
        ),
        Action(
            id="pour_water",
            name="PourWater",
            action_type=ActionType.MANIPULATION,
            parameters={"source": "sink", "target": "cup"},
            preconditions=["holding_cup", "near_sink"],
            effects=["cup_with_water"],
            duration=2.0,
            success_probability=0.85
        )
    ]
    
    # 定义初始状态和目标状态
    initial_state = {
        "agent_in_living_room": True,
        "agent_in_kitchen": False,
        "cup_on_counter": True,
        "holding_cup": False,
        "near_sink": False,
        "cup_with_water": False
    }
    
    goal_state = {
        "cup_with_water": True
    }
    
    # 创建序列生成器
    sequencer = create_action_sequencer(
        algorithm=PlanningAlgorithm.ASTAR,
        max_time=10.0
    )
    
    # 生成动作序列
    request = SequencingRequest(
        initial_state=initial_state,
        goal_state=goal_state,
        available_actions=actions,
        description="制作一杯水"
    )
    
    response = sequencer.generate_sequence(request)
    
    # 输出结果
    print(f"规划成功: {response.success}")
    if response.success:
        print(f"执行时间: {response.execution_time:.3f}秒")
        print(f"动作序列长度: {len(response.action_sequence.actions)}")
        print("\n生成的动作序列:")
        for i, action in enumerate(response.action_sequence.actions, 1):
            print(f"{i}. {action.name} (ID: {action.id})")
            print(f"   类型: {action.action_type.value}")
            print(f"   参数: {action.parameters}")
            print(f"   持续时间: {action.duration}秒")
            print(f"   前置条件: {action.preconditions}")
            print(f"   效果: {action.effects}")
            print()
    else:
        print(f"规划失败: {response.error_message}")
    
    print()


def example_2_algorithm_comparison():
    """示例2: 多种规划算法比较"""
    print("=" * 60)
    print("示例2: 多种规划算法比较")
    print("=" * 60)
    
    # 创建测试场景
    actions = [
        Action("move_a", "MoveA", ActionType.NAVIGATION, {}, ["start"], ["pos_a"], 1.0),
        Action("move_b", "MoveB", ActionType.NAVIGATION, {}, ["pos_a"], ["pos_b"], 2.0),
        Action("move_c", "MoveC", ActionType.NAVIGATION, {}, ["pos_b"], ["pos_c"], 1.5),
        Action("grab", "Grab", ActionType.MANIPULATION, {}, ["pos_c"], ["has_object"], 1.0)
    ]
    
    initial_state = {"start": True, "pos_a": False, "pos_b": False, "pos_c": False, "has_object": False}
    goal_state = {"has_object": True}
    
    algorithms = [
        PlanningAlgorithm.BFS,
        PlanningAlgorithm.DFS,
        PlanningAlgorithm.ASTAR,
        PlanningAlgorithm.GREEDY
    ]
    
    results = {}
    
    for algorithm in algorithms:
        print(f"测试算法: {algorithm.value}")
        
        sequencer = create_action_sequencer(
            algorithm=algorithm,
            max_time=5.0
        )
        
        request = SequencingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_actions=actions
        )
        
        start_time = time.time()
        response = sequencer.generate_sequence(request)
        end_time = time.time()
        
        if response.success:
            results[algorithm.value] = {
                'success': True,
                'execution_time': response.execution_time,
                'total_time': end_time - start_time,
                'sequence_length': len(response.action_sequence.actions),
                'total_duration': response.action_sequence.get_total_duration()
            }
            
            print(f"  ✅ 成功 - 序列长度: {results[algorithm.value]['sequence_length']}")
            print(f"  执行时间: {results[algorithm.value]['execution_time']:.3f}秒")
            print(f"  总时间: {results[algorithm.value]['total_time']:.3f}秒")
        else:
            results[algorithm.value] = {
                'success': False,
                'error': response.error_message
            }
            print(f"  ❌ 失败 - {response.error_message}")
        
        print()
    
    # 输出比较结果
    print("算法比较总结:")
    print("-" * 40)
    for algo, result in results.items():
        if result['success']:
            print(f"{algo:12} | 长度: {result['sequence_length']:2} | "
                  f"时间: {result['execution_time']:6.3f}s | "
                  f"总时长: {result['total_duration']:5.1f}s")
        else:
            print(f"{algo:12} | 失败 - {result['error']}")
    
    print()


def example_3_data_loading():
    """示例3: 数据集加载和处理"""
    print("=" * 60)
    print("示例3: 数据集加载和处理")
    print("=" * 60)
    
    # 模拟数据集路径 (实际使用时替换为真实路径)
    virtualhome_path = "virtualhome-00000-of-00001.parquet"
    behavior_path = "behavior-00000-of-00001.parquet"
    
    print("注意: 此示例使用模拟数据，实际使用时请提供真实的数据集路径")
    print()
    
    # 创建数据加载器配置
    config = DatasetConfig(
        virtualhome_path=virtualhome_path,
        behavior_path=behavior_path,
        max_samples=10,  # 限制样本数量用于演示
        cache_data=False
    )
    
    try:
        # 创建数据加载器
        loader = create_data_loader(
            virtualhome_path=virtualhome_path,
            behavior_path=behavior_path,
            max_samples=10
        )
        
        print("数据加载器创建成功")
        print(f"配置信息:")
        print(f"  VirtualHome路径: {config.virtualhome_path}")
        print(f"  Behavior路径: {config.behavior_path}")
        print(f"  最大样本数: {config.max_samples}")
        print(f"  启用缓存: {config.cache_data}")
        
        # 尝试加载统计数据 (如果文件存在)
        try:
            stats = loader.get_dataset_statistics()
            print(f"\n数据集统计:")
            print(f"  VirtualHome记录数: {stats.get('virtualhome_count', 0)}")
            print(f"  Behavior记录数: {stats.get('behavior_count', 0)}")
        except Exception as e:
            print(f"\n无法加载数据集统计 (文件可能不存在): {e}")
        
        # 创建示例记录
        print(f"\n创建示例数据记录:")
        
        # VirtualHome示例
        vh_record = VirtualHomeRecord(
            task_id="demo_task_001",
            task_description="Make breakfast",
            actions='[{"name": "walk", "type": "navigation", "parameters": {"target": "kitchen"}}]',
            initial_state='{"agent_location": "bedroom"}',
            goal_state='{"agent_location": "kitchen"}',
            difficulty="easy"
        )
        print(f"  VirtualHome记录: {vh_record.task_description}")
        
        # Behavior示例
        behavior_record = BehaviorRecord(
            behavior_id="demo_behavior_001",
            behavior_type="social",
            actions='[{"name": "greet", "type": "communication", "parameters": {"target": "person"}}]',
            context='{"location": "living_room", "people": ["friend"]}',
            outcomes='{"response": "positive"}'
        )
        print(f"  Behavior记录: {behavior_record.behavior_type}")
        
    except Exception as e:
        print(f"数据加载器创建失败: {e}")
        print("这通常是因为数据集文件不存在，属于正常情况")
    
    print()


def example_4_complex_planning():
    """示例4: 复杂场景规划"""
    print("=" * 60)
    print("示例4: 复杂场景规划")
    print("=" * 60)
    
    # 定义复杂的家庭环境场景
    actions = [
        # 导航动作
        Action("to_bedroom", "ToBedroom", ActionType.NAVIGATION, {}, 
               ["anywhere"], ["in_bedroom"], 2.0),
        Action("to_kitchen", "ToKitchen", ActionType.NAVIGATION, {}, 
               ["anywhere"], ["in_kitchen"], 3.0),
        Action("to_living_room", "ToLivingRoom", ActionType.NAVIGATION, {}, 
               ["anywhere"], ["in_living_room"], 1.5),
        
        # 操作动作
        Action("open_fridge", "OpenFridge", ActionType.MANIPULATION, {}, 
               ["in_kitchen", "fridge_closed"], ["fridge_open"], 1.0),
        Action("take_milk", "TakeMilk", ActionType.MANIPULATION, {}, 
               ["fridge_open"], ["has_milk"], 1.5),
        Action("close_fridge", "CloseFridge", ActionType.MANIPULATION, {}, 
               ["fridge_open"], ["fridge_closed"], 0.5),
        Action("pour_cereal", "PourCereal", ActionType.MANIPULATION, {}, 
               ["in_kitchen", "has_bowl", "has_cereal_box"], ["cereal_in_bowl"], 2.0),
        Action("pour_milk", "PourMilk", ActionType.MANIPULATION, {}, 
               ["has_milk", "cereal_in_bowl"], ["ready_cereal"], 1.0),
        
        # 观察动作
        Action("find_bowl", "FindBowl", ActionType.OBSERVATION, {}, 
               ["in_kitchen"], ["has_bowl"], 2.0),
        Action("find_cereal", "FindCereal", ActionType.OBSERVATION, {}, 
               ["in_kitchen"], ["has_cereal_box"], 3.0)
    ]
    
    # 初始状态
    initial_state = {
        "anywhere": True,
        "in_bedroom": True,
        "in_kitchen": False,
        "in_living_room": False,
        "fridge_closed": True,
        "fridge_open": False,
        "has_milk": False,
        "has_bowl": False,
        "has_cereal_box": False,
        "cereal_in_bowl": False,
        "ready_cereal": False
    }
    
    # 目标状态
    goal_state = {
        "ready_cereal": True
    }
    
    print("场景: 准备早餐")
    print("目标: 制作一碗麦片")
    print()
    
    # 使用不同算法进行规划
    sequencer = create_action_sequencer(
        algorithm=PlanningAlgorithm.ASTAR,
        heuristic_type=HeuristicType.GOAL_DISTANCE,
        max_depth=20,
        max_time=15.0
    )
    
    request = SequencingRequest(
        initial_state=initial_state,
        goal_state=goal_state,
        available_actions=actions,
        description="制作早餐麦片"
    )
    
    print("开始规划...")
    start_time = time.time()
    response = sequencer.generate_sequence(request)
    end_time = time.time()
    
    if response.success:
        print(f"✅ 规划成功!")
        print(f"规划时间: {response.execution_time:.3f}秒")
        print(f"总耗时: {end_time - start_time:.3f}秒")
        print(f"动作序列长度: {len(response.action_sequence.actions)}")
        print(f"预计执行时间: {response.action_sequence.get_total_duration():.1f}秒")
        print()
        
        print("详细动作序列:")
        for i, action in enumerate(response.action_sequence.actions, 1):
            print(f"{i:2d}. {action.name:15} | {action.action_type.value:12} | "
                  f"{action.duration:4.1f}s | {action.parameters}")
        
        # 显示状态变化
        print(f"\n状态跟踪:")
        current_state = initial_state.copy()
        print(f"初始状态: {sum(current_state.values())} 个条件满足")
        
        for action in response.action_sequence.actions:
            if action.can_execute(current_state):
                current_state = action.execute(current_state)
                print(f"执行 {action.name}: {sum(current_state.values())} 个条件满足")
        
        # 检查目标达成
        goal_achieved = all(current_state.get(k, False) for k in goal_state.keys())
        print(f"目标达成: {'✅' if goal_achieved else '❌'}")
        
    else:
        print(f"❌ 规划失败: {response.error_message}")
    
    print()


def example_5_quick_api():
    """示例5: 快速API使用"""
    print("=" * 60)
    print("示例5: 快速API使用")
    print("=" * 60)
    
    # 使用快速API函数
    print("使用 quick_sequence_generation 函数:")
    
    # 简单的动作定义
    simple_actions = [
        {
            'id': 'walk',
            'name': 'WalkToTarget',
            'type': 'navigation',
            'parameters': {'target': 'goal'},
            'preconditions': ['at_start'],
            'effects': ['at_goal'],
            'duration': 2.0
        },
        {
            'id': 'pick',
            'name': 'PickObject',
            'type': 'manipulation',
            'parameters': {'object': 'item'},
            'preconditions': ['at_goal', 'object_available'],
            'effects': ['holding_object'],
            'duration': 1.0
        }
    ]
    
    initial_state = {'at_start': True, 'at_goal': False, 'object_available': True, 'holding_object': False}
    goal_state = {'holding_object': True}
    
    # 测试不同算法
    for algorithm in [PlanningAlgorithm.BFS, PlanningAlgorithm.ASTAR]:
        print(f"\n使用 {algorithm.value} 算法:")
        
        response = quick_sequence_generation(
            initial_state=initial_state,
            goal_state=goal_state,
            available_actions=simple_actions,
            algorithm=algorithm
        )
        
        if response.success:
            print(f"  ✅ 成功生成序列 ({len(response.action_sequence.actions)} 个动作)")
            for i, action in enumerate(response.action_sequence.actions, 1):
                print(f"    {i}. {action.name}")
        else:
            print(f"  ❌ 失败: {response.error_message}")
    
    print()


def example_6_performance_test():
    """示例6: 性能测试"""
    print("=" * 60)
    print("示例6: 性能测试")
    print("=" * 60)
    
    # 创建不同规模的测试场景
    test_scenarios = [
        {
            'name': '小型场景',
            'num_actions': 5,
            'max_depth': 10
        },
        {
            'name': '中型场景', 
            'num_actions': 10,
            'max_depth': 15
        },
        {
            'name': '大型场景',
            'num_actions': 20,
            'max_depth': 25
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n测试 {scenario['name']} ({scenario['num_actions']} 个动作):")
        
        # 生成随机动作
        actions = []
        for i in range(scenario['num_actions']):
            action = Action(
                id=f"action_{i}",
                name=f"Action{i}",
                action_type=ActionType.NAVIGATION if i % 2 == 0 else ActionType.MANIPULATION,
                parameters={"step": i},
                preconditions=[f"state_{i-1}"] if i > 0 else ["start"],
                effects=[f"state_{i}"],
                duration=1.0 + i * 0.1
            )
            actions.append(action)
        
        # 设置状态
        initial_state = {"start": True, **{f"state_{i}": False for i in range(scenario['num_actions'])}}
        goal_state = {f"state_{scenario['num_actions']-1}": True}
        
        # 测试A*算法性能
        sequencer = create_action_sequencer(
            algorithm=PlanningAlgorithm.ASTAR,
            max_depth=scenario['max_depth'],
            max_time=10.0
        )
        
        request = SequencingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_actions=actions
        )
        
        start_time = time.time()
        response = sequencer.generate_sequence(request)
        end_time = time.time()
        
        if response.success:
            print(f"  ✅ 成功 | 时间: {response.execution_time:.3f}s | "
                  f"序列长度: {len(response.action_sequence.actions)} | "
                  f"总耗时: {end_time - start_time:.3f}s")
        else:
            print(f"  ❌ 失败 | {response.error_message}")
    
    print()


def main():
    """主函数 - 运行所有示例"""
    print("Action Sequencing Module 使用示例")
    print("=" * 60)
    print()
    
    examples = [
        example_1_basic_sequencing,
        example_2_algorithm_comparison,
        example_3_data_loading,
        example_4_complex_planning,
        example_5_quick_api,
        example_6_performance_test
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"示例 {i} 执行出错: {e}")
            print("继续执行下一个示例...")
            print()
    
    print("=" * 60)
    print("所有示例执行完成!")
    print()
    
    # Ubuntu系统运行提示
    print("🐧 Ubuntu系统运行说明:")
    print("1. 确保安装了依赖包:")
    print("   pip install numpy pandas")
    print()
    print("2. 运行示例:")
    print("   cd /path/to/action_sequencing")
    print("   python3 example_usage.py")
    print()
    print("3. 运行测试:")
    print("   python3 test_action_sequencing.py")
    print()
    print("4. 数据集文件路径:")
    print("   - virtualhome-00000-of-00001.parquet")
    print("   - behavior-00000-of-00001.parquet")


if __name__ == '__main__':
    main()