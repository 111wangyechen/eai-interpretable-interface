#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试transition_modeling模块
"""

import unittest
import json
import sys
import os
from typing import Dict, List

# 添加项目根目录到Python路径，确保可以正确导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 现在可以使用绝对导入
from transition_modeling.state_transition import (
    StateTransition, 
    TransitionType, 
    TransitionStatus,
    StateCondition,
    StateEffect,
    TransitionSequence,
    TransitionModel
)
from transition_modeling.transition_validator import TransitionValidator, ValidationResult


class TestStateCondition(unittest.TestCase):
    """测试状态条件类"""
    
    def test_evaluate_simple_condition(self):
        """测试简单条件评估"""
        # 创建条件
        condition = StateCondition(predicate="at_start")
        
        # 测试匹配
        state_true = {"at_start": "True"}
        state_false = {"at_start": "False"}
        state_missing = {}
        
        # 注意：使用字符串形式的布尔值
        self.assertTrue(condition.evaluate(state_true))
        self.assertFalse(condition.evaluate(state_false))
        self.assertFalse(condition.evaluate(state_missing))
    
    def test_evaluate_with_parameters(self):
        """测试带参数的条件评估"""
        # 创建带参数的条件
        condition = StateCondition(
            predicate="object_state",
            parameters={"name": "cup", "location": "table"}
        )
        
        # 测试匹配
        state_match = {"object_state": {"name": "cup", "location": "table"}}
        state_mismatch = {"object_state": {"name": "cup", "location": "floor"}}
        state_simple = {"object_state": "cup_on_table"}
        
        self.assertTrue(condition.evaluate(state_match))
        self.assertFalse(condition.evaluate(state_mismatch))
        # 测试单参数直接比较
        self.assertFalse(condition.evaluate(state_simple))  # 因为参数有多个
        
        # 测试单参数情况
        condition_single = StateCondition(
            predicate="object_state",
            parameters={"value": "cup_on_table"}
        )
        # 这应该可以直接比较
        state_single = {"object_state": "cup_on_table"}
        self.assertTrue(condition_single.evaluate(state_single))


class TestStateEffect(unittest.TestCase):
    """测试状态效果类"""
    
    def test_apply_effect(self):
        """测试应用效果"""
        effect = StateEffect(predicate="at_goal", value="True")
        state = {"at_start": "True"}
        
        new_state = effect.apply(state)
        
        self.assertEqual(new_state["at_goal"], "True")
        self.assertEqual(new_state["at_start"], "True")  # 原状态保持不变
    
    def test_apply_multiple_effects(self):
        """测试应用多个效果"""
        effects = [
            StateEffect(predicate="at_goal", value="True"),
            StateEffect(predicate="at_start", value="False")
        ]
        
        state = {"at_start": "True", "counter": 0}
        
        for effect in effects:
            state = effect.apply(state)
        
        self.assertEqual(state["at_goal"], "True")
        self.assertEqual(state["at_start"], "False")
        self.assertEqual(state["counter"], 0)  # 未修改的状态保持不变


class TestStateTransition(unittest.TestCase):
    """测试状态转换类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建一个简单的转换
        precondition = StateCondition(predicate="at_start")
        effect = StateEffect(predicate="at_goal", value="True")
        
        self.transition = StateTransition(
            name="move_to_goal",
            preconditions=[precondition],
            effects=[effect],
            duration=2.0,
            cost=1.5
        )
    
    def test_is_applicable(self):
        """测试转换是否适用"""
        state_applicable = {"at_start": "True"}
        state_not_applicable = {"at_start": "False"}
        
        self.assertTrue(self.transition.is_applicable(state_applicable))
        self.assertFalse(self.transition.is_applicable(state_not_applicable))
    
    def test_apply_effects(self):
        """测试应用转换效果"""
        state = {"at_start": "True"}
        
        # 由于概率设置为1.0，效果应该总是应用
        new_state = self.transition.apply_effects(state)
        
        self.assertEqual(new_state["at_goal"], "True")
        self.assertEqual(new_state["at_start"], "True")  # 原条件保持不变
    
    def test_execution_lifecycle(self):
        """测试转换执行生命周期"""
        # 初始状态应该是PENDING
        self.assertEqual(self.transition.status, TransitionStatus.PENDING)
        
        # 开始执行
        self.transition.start_execution()
        self.assertEqual(self.transition.status, TransitionStatus.EXECUTING)
        self.assertIsNotNone(self.transition.started_at)
        
        # 完成执行
        self.transition.complete_execution(success=True)
        self.assertEqual(self.transition.status, TransitionStatus.COMPLETED)
        self.assertIsNotNone(self.transition.completed_at)
        
        # 获取执行时间
        execution_time = self.transition.get_execution_time()
        self.assertIsNotNone(execution_time)
        self.assertGreaterEqual(execution_time, 0)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        # 序列化为字典
        transition_dict = self.transition.to_dict()
        
        # 验证必要字段
        self.assertIn('id', transition_dict)
        self.assertEqual(transition_dict['name'], 'move_to_goal')
        self.assertEqual(len(transition_dict['preconditions']), 1)
        self.assertEqual(len(transition_dict['effects']), 1)
        
        # 反序列化
        restored_transition = StateTransition.from_dict(transition_dict)
        
        # 验证相等性
        self.assertEqual(restored_transition.name, self.transition.name)
        self.assertEqual(len(restored_transition.preconditions), len(self.transition.preconditions))
        self.assertEqual(len(restored_transition.effects), len(self.transition.effects))


class TestTransitionValidator(unittest.TestCase):
    """测试转换验证器"""
    
    def setUp(self):
        """设置测试环境"""
        self.validator = TransitionValidator()
    
    def test_validate_valid_transition(self):
        """测试验证有效的转换"""
        # 创建有效转换
        transition = StateTransition(
            id="valid_transition",
            name="test_transition",
            preconditions=[StateCondition(predicate="ready")],
            effects=[StateEffect(predicate="done", value="True")],
            duration=1.0,
            cost=1.0
        )
        
        # 有效状态
        state = {"ready": "True"}
        
        # 验证
        result = self.validator.validate_transition(transition, state)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.message, "Transition validation passed")
    
    def test_validate_invalid_transition_structure(self):
        """测试验证无效的转换结构"""
        # 创建结构无效的转换（缺少名称）
        transition = StateTransition(
            id="invalid_transition",
            name="",  # 空名称
            preconditions=[StateCondition(predicate="ready")],
            effects=[StateEffect(predicate="done", value="True")]
        )
        
        state = {"ready": "True"}
        
        # 验证
        result = self.validator.validate_transition(transition, state)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Missing required fields", result.message)
    
    def test_validate_preconditions(self):
        """测试验证前提条件"""
        transition = StateTransition(
            id="precondition_test",
            name="precondition_test",
            preconditions=[StateCondition(predicate="ready")],
            effects=[StateEffect(predicate="done", value="True")]
        )
        
        # 前提条件不满足
        state = {"ready": "False"}
        
        # 验证
        result = self.validator.validate_transition(transition, state)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Precondition not satisfied", result.message)
    
    def test_validate_transition_sequence(self):
        """测试验证转换序列"""
        # 创建一个简单的转换序列
        transition1 = StateTransition(
            id="step1",
            name="step1",
            preconditions=[StateCondition(predicate="start")],
            effects=[StateEffect(predicate="middle", value="True")]
        )
        
        transition2 = StateTransition(
            id="step2",
            name="step2",
            preconditions=[StateCondition(predicate="middle")],
            effects=[StateEffect(predicate="end", value="True")]
        )
        
        sequence = [transition1, transition2]
        initial_state = {"start": "True"}
        
        # 验证序列
        result = self.validator.validate_transition_sequence(sequence, initial_state)
        
        self.assertTrue(result.is_valid)
        self.assertIn("Sequence validation passed", result.message)
    
    def test_validate_model_consistency(self):
        """测试验证模型一致性"""
        # 创建一组一致的转换
        transition1 = StateTransition(
            id="unique_id_1",
            name="transition1",
            preconditions=[],  # 无前提条件，作为起点
            effects=[StateEffect(predicate="state1", value="True")]
        )
        
        transition2 = StateTransition(
            id="unique_id_2",
            name="transition2",
            preconditions=[StateCondition(predicate="state1")],
            effects=[StateEffect(predicate="state2", value="True")]
        )
        
        transitions = [transition1, transition2]
        
        # 验证一致性
        result = self.validator.validate_model_consistency(transitions)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.message, "Model consistency validation passed")


class TestTransitionModel(unittest.TestCase):
    """测试转换模型类"""
    
    def test_find_applicable_transitions(self):
        """测试查找适用的转换"""
        # 创建转换模型
        model = TransitionModel(
            id="test_model",
            name="Test Model",
            domain="test"
        )
        
        # 添加转换
        transition1 = StateTransition(
            name="transition1",
            preconditions=[StateCondition(predicate="condition1")],
            effects=[StateEffect(predicate="effect1", value="True")]
        )
        
        transition2 = StateTransition(
            name="transition2",
            preconditions=[StateCondition(predicate="condition2")],
            effects=[StateEffect(predicate="effect2", value="True")]
        )
        
        model.add_transition(transition1)
        model.add_transition(transition2)
        
        # 测试查找适用转换
        state = {"condition1": "True"}
        applicable = model.find_applicable_transitions(state)
        
        self.assertEqual(len(applicable), 1)
        self.assertEqual(applicable[0].name, "transition1")


class TestIntegration(unittest.TestCase):
    """测试模块集成功能"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 创建转换
        precondition = StateCondition(predicate="ready")
        effect = StateEffect(predicate="completed", value="True")
        
        transition = StateTransition(
            name="complete_task",
            preconditions=[precondition],
            effects=[effect]
        )
        
        # 创建验证器
        validator = TransitionValidator()
        
        # 创建初始状态
        initial_state = {"ready": "True"}
        
        # 验证转换
        validation_result = validator.validate_transition(transition, initial_state)
        self.assertTrue(validation_result.is_valid)
        
        # 应用转换
        new_state = transition.apply_effects(initial_state)
        self.assertEqual(new_state["completed"], "True")
        
        # 执行转换
        transition.start_execution()
        transition.complete_execution(success=True)
        
        self.assertEqual(transition.status, TransitionStatus.COMPLETED)


if __name__ == '__main__':
    # 运行所有测试
    unittest.main()