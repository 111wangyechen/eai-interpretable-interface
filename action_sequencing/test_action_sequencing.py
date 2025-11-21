#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Sequencing模块测试文件
包含单元测试和集成测试
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from action_data import Action, ActionSequence, ActionType, ActionStatus
from state_manager import EnvironmentState, StateManager, StateTransition
from action_planner import ActionPlanner, PlanningAlgorithm, HeuristicType, PlanningResult
from action_sequencer import ActionSequencer, SequencingConfig, SequencingRequest, SequencingResponse
from data_loader import DataLoader, DatasetConfig, VirtualHomeRecord, BehaviorRecord


class TestActionData(unittest.TestCase):
    """测试Action和ActionSequence数据类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_action = Action(
            id="test_action_1",
            name="MoveToLocation",
            action_type=ActionType.NAVIGATION,
            parameters={"location": "kitchen", "speed": 1.0},
            preconditions=["agent_at_start=True"],
            effects=["agent_location=kitchen", "agent_at_kitchen=True"],
            duration=2.0,
            success_probability=0.95
        )
        
        self.test_actions = [self.test_action]
        self.test_sequence = ActionSequence(
            id="test_sequence_1",
            actions=self.test_actions,
            initial_state={"agent_location": "start"},
            goal_state={"agent_location": "kitchen"}
        )
    
    def test_action_creation(self):
        """测试Action对象创建"""
        self.assertEqual(self.test_action.id, "test_action_1")
        self.assertEqual(self.test_action.name, "MoveToLocation")
        self.assertEqual(self.test_action.action_type, ActionType.NAVIGATION)
        self.assertEqual(self.test_action.duration, 2.0)
        self.assertEqual(self.test_action.success_probability, 0.95)
    
    def test_action_execution(self):
        """测试动作执行"""
        state = {"agent_location": "start", "agent_at_start": True}
        new_state = self.test_action.execute(state)
        
        # 检查状态变化
        self.assertEqual(new_state["agent_location"], "kitchen")
        self.assertTrue(new_state.get("agent_at_kitchen", False))
    
    def test_action_preconditions(self):
        """测试前置条件检查"""
        # 满足前置条件 - 使用字符串格式匹配preconditions格式
        state = {"agent_at_start": "True"}
        self.assertTrue(self.test_action.can_execute(state))
        
        # 不满足前置条件
        state = {"agent_at_start": "False"}
        self.assertFalse(self.test_action.can_execute(state))
        
        # 测试缺少前置条件的情况
        state = {}
        self.assertFalse(self.test_action.can_execute(state))
    
    def test_action_sequence_creation(self):
        """测试ActionSequence对象创建"""
        self.assertEqual(self.test_sequence.id, "test_sequence_1")
        self.assertEqual(len(self.test_sequence.actions), 1)
        self.assertEqual(self.test_sequence.initial_state["agent_location"], "start")
        self.assertEqual(self.test_sequence.goal_state["agent_location"], "kitchen")
    
    def test_action_sequence_methods(self):
        """测试ActionSequence方法"""
        # 测试转换为字典
        sequence_dict = self.test_sequence.to_dict()
        self.assertIn('id', sequence_dict)
        self.assertIn('actions', sequence_dict)
        self.assertEqual(sequence_dict['id'], "test_sequence_1")
        
        # 测试状态检查
        self.assertTrue(self.test_sequence.is_valid())
        self.assertEqual(self.test_sequence.get_total_duration(), 2.0)


class TestStateManager(unittest.TestCase):
    """测试状态管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.state_manager = StateManager()
        self.test_state = {"agent_location": "living_room", "holding_object": None}
    
    def test_state_manager_initialization(self):
        """测试状态管理器初始化"""
        self.assertIsNotNone(self.state_manager.current_state)
        self.assertEqual(len(self.state_manager.state_history), 1)
    
    def test_state_update(self):
        """测试状态更新"""
        new_state = {"agent_location": "kitchen", "holding_object": "cup"}
        self.state_manager.update_state(new_state)
        
        current_state_dict = self.state_manager.current_state.get_state_dict()
        self.assertEqual(current_state_dict["agent_location"], "kitchen")
        self.assertEqual(current_state_dict["holding_object"], "cup")
    
    def test_state_transition(self):
        """测试状态转换"""
        # 设置初始状态
        self.state_manager.update_state({"agent_location": "start", "agent_at_start": "True"})
        
        transition = StateTransition(
            from_state={"agent_location": "start"},
            to_state={"agent_location": "kitchen"},
            action_name="move_action",
            preconditions=["agent_at_start=True"],
            effects=["agent_at_kitchen=True"]
        )
        
        self.state_manager.add_transition(transition)
        self.assertEqual(len(self.state_manager.state_transitions), 1)
        
        # 测试转换执行
        result = self.state_manager.apply_action("move_action")
        self.assertTrue(result)
        self.assertEqual(self.state_manager.get_current_state().get_value("agent_location"), "kitchen")


class TestActionPlanner(unittest.TestCase):
    """测试动作规划器"""
    
    def setUp(self):
        """测试前准备"""
        self.planner = ActionPlanner(
            algorithm=PlanningAlgorithm.ASTAR,
            heuristic_type=HeuristicType.GOAL_DISTANCE
        )
        
        # 创建测试动作
        self.actions = [
            Action(
                id="move_to_kitchen",
                name="MoveToKitchen",
                action_type=ActionType.NAVIGATION,
                parameters={"target": "kitchen"},
                preconditions=["agent_at_living_room=True"],
                effects=["agent_at_living_room=False", "agent_at_kitchen=True"],
                duration=2.0
            ),
            Action(
                id="pick_up_cup",
                name="PickUpCup",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "cup"},
                preconditions=["agent_at_kitchen=True", "cup_on_table=True"],
                effects=["holding_cup=True", "cup_on_table=False"],
                duration=1.0
            )
        ]
        
        self.initial_state = {
            "agent_at_living_room": "True",
            "agent_at_kitchen": "False",
            "cup_on_table": "True",
            "holding_cup": "False"
        }
        
        self.goal_state = {
            "holding_cup": "True",
            "agent_at_kitchen": "True"  # 添加更明确的目标
        }
    
    def test_planner_initialization(self):
        """测试规划器初始化"""
        self.assertEqual(self.planner.algorithm, PlanningAlgorithm.ASTAR)
        self.assertEqual(self.planner.heuristic_calculator.heuristic_type, HeuristicType.GOAL_DISTANCE)
    
    def test_simple_planning(self):
        """测试简单规划"""
        result = self.planner.plan(
            initial_state=self.initial_state,
            goal_state=self.goal_state,
            available_actions=self.actions
        )
        
        self.assertIsInstance(result, PlanningResult)
        self.assertIsNotNone(result.action_sequence)
        self.assertGreater(result.planning_time, 0)
    
    def test_bfs_planning(self):
        """测试BFS规划"""
        self.planner.algorithm = PlanningAlgorithm.BFS
        result = self.planner.plan(
            initial_state=self.initial_state,
            goal_state=self.goal_state,
            available_actions=self.actions
        )
        
        self.assertIsInstance(result, PlanningResult)
    
    def test_greedy_planning(self):
        """测试贪心规划"""
        self.planner.algorithm = PlanningAlgorithm.GREEDY
        result = self.planner.plan(
            initial_state=self.initial_state,
            goal_state=self.goal_state,
            available_actions=self.actions
        )
        
        self.assertIsInstance(result, PlanningResult)


class TestActionSequencer(unittest.TestCase):
    """测试动作序列生成器"""
    
    def setUp(self):
        """测试前准备"""
        self.config = SequencingConfig(
            planning_algorithm=PlanningAlgorithm.ASTAR,
            heuristic_type=HeuristicType.GOAL_DISTANCE,
            max_depth=10,
            max_time=5.0
        )
        self.sequencer = ActionSequencer(self.config)
        
        # 创建测试请求
        self.test_actions = [
            Action(
                id="move_to_kitchen",
                name="MoveToKitchen",
                action_type=ActionType.NAVIGATION,
                parameters={"target": "kitchen"},
                preconditions=["agent_at_living_room=True"],
                effects=["agent_at_living_room=False", "agent_at_kitchen=True"],
                duration=2.0
            ),
            Action(
                id="pick_up_cup",
                name="PickUpCup",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "cup"},
                preconditions=["agent_at_kitchen=True", "cup_on_table=True"],
                effects=["holding_cup=True", "cup_on_table=False"],
                duration=1.0
            )
        ]
        
        self.test_request = SequencingRequest(
            initial_state={
                "agent_at_living_room": "True",
                "agent_at_kitchen": "False",
                "cup_on_table": "True",
                "holding_cup": "False"
            },
            goal_state={
                "holding_cup": "True",
                "agent_at_kitchen": "True"
            },
            available_actions=self.test_actions
        )
    
    def test_sequencer_initialization(self):
        """测试序列生成器初始化"""
        self.assertIsNotNone(self.sequencer.config)
        self.assertIsNotNone(self.sequencer.action_planner)
        self.assertIsNotNone(self.sequencer.state_manager)
    
    def test_generate_sequence(self):
        """测试生成动作序列"""
        response = self.sequencer.generate_sequence(self.test_request)
        
        self.assertIsInstance(response, SequencingResponse)
        self.assertIsNotNone(response.action_sequence)
        self.assertGreater(response.execution_time, 0)
    
    def test_invalid_request(self):
        """测试无效请求"""
        invalid_request = SequencingRequest(
            initial_state={},
            goal_state={},
            available_actions=[]
        )
        
        response = self.sequencer.generate_sequence(invalid_request)
        self.assertFalse(response.success)
        self.assertIsNotNone(response.error_message)
    
    def test_statistics(self):
        """测试统计信息"""
        stats = self.sequencer.get_statistics()
        self.assertIn('stats', stats)
        self.assertIn('config', stats)
        self.assertIn('cache_size', stats)


class TestDataLoader(unittest.TestCase):
    """测试数据加载器"""
    
    def setUp(self):
        """测试前准备"""
        self.config = DatasetConfig(
            virtualhome_path="data/virtualhome.parquet",
            behavior_path="data/behavior.parquet",
            max_samples=5,
            cache_data=False
        )
        
        # 创建模拟数据
        self.mock_virtualhome_data = [
            {
                'task_id': 'task_1',
                'task_description': 'Make coffee',
                'actions': '[{"name": "walk", "type": "navigation"}]',
                'initial_state': '{"agent_location": "bedroom"}',
                'goal_state': '{"agent_location": "kitchen"}'
            }
        ]
        
        self.mock_behavior_data = [
            {
                'behavior_id': 'behavior_1',
                'behavior_type': 'social',
                'actions': '[{"name": "greet", "type": "communication"}]',
                'context': '{"location": "living_room"}',
                'outcomes': '{"response": "positive"}'
            }
        ]
    
    @patch('pandas.read_parquet')
    @patch('pathlib.Path.exists')
    def test_virtualhome_loading(self, mock_exists, mock_read_parquet):
        """测试VirtualHome数据加载"""
        # 模拟文件存在
        mock_exists.return_value = True
        
        # 模拟pandas返回数据
        import pandas as pd
        mock_df = pd.DataFrame(self.mock_virtualhome_data)
        mock_read_parquet.return_value = mock_df
        
        loader = DataLoader(self.config)
        records = loader.load_virtualhome_data()
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].task_id, 'task_1')
        self.assertEqual(records[0].task_description, 'Make coffee')
    
    @patch('pandas.read_parquet')
    @patch('pathlib.Path.exists')
    def test_behavior_loading(self, mock_exists, mock_read_parquet):
        """测试Behavior数据加载"""
        # 模拟文件存在
        mock_exists.return_value = True
        
        # 模拟pandas返回数据
        import pandas as pd
        mock_df = pd.DataFrame(self.mock_behavior_data)
        mock_read_parquet.return_value = mock_df
        
        loader = DataLoader(self.config)
        records = loader.load_behavior_data()
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].behavior_id, 'behavior_1')
        self.assertEqual(records[0].behavior_type, 'social')
    
    def test_action_conversion(self):
        """测试动作转换"""
        loader = DataLoader(self.config)
        
        action_dicts = [
            {
                'id': 'action_1',
                'name': 'Walk',
                'type': 'navigation',
                'parameters': {'target': 'kitchen'},
                'duration': 2.0
            }
        ]
        
        actions = loader.convert_to_actions(action_dicts)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].id, 'action_1')
        self.assertEqual(actions[0].action_type, ActionType.NAVIGATION)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.config = SequencingConfig(
            planning_algorithm=PlanningAlgorithm.ASTAR,
            max_time=2.0
        )
        self.sequencer = ActionSequencer(self.config)
    
    def test_end_to_end_planning(self):
        """测试端到端规划流程"""
        # 创建复杂的场景
        actions = [
            Action(
                id="walk_to_kitchen",
                name="WalkToKitchen",
                action_type=ActionType.NAVIGATION,
                parameters={},
                preconditions=["in_living_room"],
                effects=["in_kitchen"],
                duration=3.0
            ),
            Action(
                id="pick_cup",
                name="PickCup",
                action_type=ActionType.MANIPULATION,
                parameters={},
                preconditions=["in_kitchen", "cup_available"],
                effects=["holding_cup"],
                duration=1.0
            ),
            Action(
                id="pour_water",
                name="PourWater",
                action_type=ActionType.MANIPULATION,
                parameters={},
                preconditions=["holding_cup", "near_sink"],
                effects=["cup_with_water"],
                duration=2.0
            )
        ]
        
        request = SequencingRequest(
            initial_state={
                "in_living_room": True,
                "in_kitchen": False,
                "cup_available": True,
                "holding_cup": False,
                "near_sink": False,
                "cup_with_water": False
            },
            goal_state={
                "cup_with_water": True
            },
            available_actions=actions
        )
        
        response = self.sequencer.generate_sequence(request)
        
        # 验证结果
        if response.success:
            self.assertIsNotNone(response.action_sequence)
            self.assertGreater(len(response.action_sequence.actions), 0)
            
            # 验证序列有效性
            validation_result = self.sequencer._validate_sequence(
                response.action_sequence,
                request.initial_state,
                request.goal_state
            )
            self.assertTrue(validation_result['valid'], 
                          f"Validation failed: {validation_result.get('errors', [])}")
    
    def test_multiple_scenarios(self):
        """测试多个场景"""
        scenarios = [
            {
                'name': 'simple_navigation',
                'initial': {'at_start': True, 'at_target': False},
                'goal': {'at_target': True},
                'actions': [
                    Action('move', 'Move', ActionType.NAVIGATION, {}, 
                          ['at_start'], ['at_target'], 1.0)
                ]
            },
            {
                'name': 'multi_step',
                'initial': {'at_door': True, 'has_key': False, 'door_open': False},
                'goal': {'door_open': True},
                'actions': [
                    Action('find_key', 'FindKey', ActionType.PERCEPTION, {}, 
                          ['at_door'], ['has_key'], 2.0),
                    Action('open_door', 'OpenDoor', ActionType.MANIPULATION, {}, 
                          ['has_key'], ['door_open'], 1.0)
                ]
            }
        ]
        
        for scenario in scenarios:
            with self.subTest(scenario=scenario['name']):
                request = SequencingRequest(
                    initial_state=scenario['initial'],
                    goal_state=scenario['goal'],
                    available_actions=scenario['actions']
                )
                
                response = self.sequencer.generate_sequence(request)
                
                # 基本验证
                self.assertIsInstance(response, SequencingResponse)
                self.assertIsNotNone(response.planning_result)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestActionData,
        TestStateManager,
        TestActionPlanner,
        TestActionSequencer,
        TestDataLoader,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Running Action Sequencing Module Tests...")
    print("=" * 60)
    
    success = run_tests()
    
    print("=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    print(f"\nTest Summary:")
    print(f"- Total test classes: 6")
    print(f"- Integration tests included: Yes")
    print(f"- Mock data tests included: Yes")
    
    # Ubuntu系统运行提示
    print(f"\n🐧 Ubuntu运行说明:")
    print(f"在Ubuntu系统中运行测试:")
    print(f"cd /path/to/action_sequencing")
    print(f"python3 test_action_sequencing.py")