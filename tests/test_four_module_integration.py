#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版四模块集成测试
强化模块接口校验与数据传输一致性验证
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import pytest

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入四个模块及核心数据结构
try:
    from goal_interpretation import (
        EnhancedGoalInterpreter as GoalInterpreter,
        LTLFormula  # 明确导入目标解释模块的数据结构
    )
    from subgoal_decomposition import (
        SubgoalDecomposer,
        DecompositionResult  # 子目标分解结果的数据结构
    )
    from transition_modeling import (
        TransitionModeler,
        ModelingRequest,
        ModelingResponse,
        StateTransition,
        StateCondition,
        StateEffect  # 转换模型核心数据结构
    )
    from action_sequencing import (
        ActionSequencer,
        ActionType,
        Action,
        SequencingRequest,
        SequencingResponse,
        ActionSequence  # 动作序列核心数据结构
    )
    print("✓ 所有模块及数据结构导入成功")
except ImportError as e:
    print(f"✗ 模块导入失败: {e}")
    sys.exit(1)


class FourModuleIntegrationTester:
    """增强版四模块集成测试器，强化接口与数据校验"""
    
    def __init__(self):
        self.goal_interpreter = GoalInterpreter()
        self.subgoal_decomposer = SubgoalDecomposer()
        self.transition_modeler = TransitionModeler()
        self.action_sequencer = ActionSequencer()
        
        self.test_results = []
        self.start_time = time.time()
        # 记录模块间数据传输格式校验结果
        self.data_format_checks = {
            "goal_to_subgoal": True,
            "subgoal_to_transition": True,
            "transition_to_action": True
        }

    def run_comprehensive_integration_test(self):
        """运行增强版全面集成测试"""
        print("=" * 80)
        print("增强版四模块集成测试（含接口与数据校验）")
        print("目标解释 → 子目标分解 → 转换建模 → 动作序列")
        print("=" * 80)
        
        # 1. 模块初始化与接口可用性测试（增强版）
        self.test_module_initialization_enhanced()
        
        # 2. 目标解释到子目标分解的数据传输测试
        self.test_goal_to_subgoal_data_flow()
        
        # 3. 子目标分解到转换建模的接口适配测试
        self.test_subgoal_to_transition_interface()
        
        # 4. 转换建模到动作序列的参数传递测试
        self.test_transition_to_action_param_pass()
        
        # 5. 完整端到端流程（含全链路数据校验）
        self.test_end_to_end_with_data_validation()
        
        # 6. 异常场景数据容错测试
        self.test_data_fault_tolerance()
        
        # 7. 性能与稳定性（含模块交互延迟监控）
        self.test_performance_with_interaction_latency()
        
        # 生成增强版测试报告
        self.generate_enhanced_report()

    def test_module_initialization_enhanced(self):
        """增强版模块初始化测试：验证核心接口方法存在性与参数合法性"""
        print("\n1. 增强版模块初始化测试...")
        initialization_results = {}
        
        # 目标解释模块：验证核心方法与参数
        try:
            # 检查核心解释方法
            assert hasattr(self.goal_interpreter, "interpret"), "目标解释模块缺少interpret方法"
            # 测试参数合法性（空输入处理）
            empty_result = self.goal_interpreter.interpret("")
            assert empty_result is None or isinstance(empty_result, dict), "空目标处理返回格式错误"
            # 正常输入测试
            sample_goal = "将蓝色方块移到架子上"
            goal_result = self.goal_interpreter.interpret(sample_goal)
            assert isinstance(goal_result, dict), "目标解释结果应为字典"
            assert "ltl_formula" in goal_result, "目标解释结果缺少ltl_formula字段"
            assert isinstance(goal_result["ltl_formula"], (str, LTLFormula)), "ltl_formula格式错误"
            initialization_results["goal_interpretation"] = True
            print("   ✓ 目标解释模块接口验证通过")
        except Exception as e:
            initialization_results["goal_interpretation"] = False
            print(f"   ✗ 目标解释模块验证失败: {e}")

        # 子目标分解模块：验证输入输出格式
        try:
            assert hasattr(self.subgoal_decomposer, "decompose"), "子目标模块缺少decompose方法"
            # 测试LTLFormula输入兼容性
            test_ltl = LTLFormula("F(blue_block_on_shelf)")
            subgoal_result = self.subgoal_decomposer.decompose(ltl_formula=test_ltl)
            assert isinstance(subgoal_result, DecompositionResult), "子目标分解结果应为DecompositionResult类型"
            assert hasattr(subgoal_result, "subgoals"), "DecompositionResult缺少subgoals属性"
            assert all(hasattr(sg, "description") for sg in subgoal_result.subgoals), "子目标缺少description字段"
            initialization_results["subgoal_decomposition"] = True
            print("   ✓ 子目标分解模块接口验证通过")
        except Exception as e:
            initialization_results["subgoal_decomposition"] = False
            print(f"   ✗ 子目标分解模块验证失败: {e}")

        # 转换建模模块：验证请求响应机制
        try:
            assert hasattr(self.transition_modeler, "model_transitions"), "转换建模缺少model_transitions方法"
            # 测试ModelingRequest构造与处理
            # 创建一个符合StateTransition类定义的转换
            test_transition = StateTransition(
                name="move",
                description="移动到目标位置",
                preconditions=[StateCondition(predicate="at", value="start")],
                effects=[StateEffect(predicate="at", value="shelf")]
            )
            test_request = ModelingRequest(
                initial_state={"at": "start", "holding": None},
                goal_state={"at": "shelf", "holding": "blue_block"},
                available_transitions=[test_transition]
            )
            transition_result = self.transition_modeler.model_transitions(test_request)
            assert isinstance(transition_result, ModelingResponse), "转换建模结果应为ModelingResponse类型"
            assert hasattr(transition_result, "predicted_sequences"), "转换结果缺少predicted_sequences"
            initialization_results["transition_modeling"] = True
            print("   ✓ 转换建模模块接口验证通过")
        except Exception as e:
            initialization_results["transition_modeling"] = False
            print(f"   ✗ 转换建模模块验证失败: {e}")

        # 动作序列模块：验证序列生成接口
        try:
            assert hasattr(self.action_sequencer, "generate_sequence"), "动作序列模块缺少generate_sequence方法"
            # 测试SequencingRequest处理
            test_actions = [Action(id="move1", name="move", action_type=ActionType.NAVIGATION)]
            test_request = SequencingRequest(
                initial_state={"at": "start"},
                goal_state={"at": "shelf"},
                available_actions=test_actions
            )
            sequence_result = self.action_sequencer.generate_sequence(test_request)
            assert isinstance(sequence_result, SequencingResponse), "动作序列结果应为SequencingResponse类型"
            assert hasattr(sequence_result, "action_sequence"), "动作序列结果缺少action_sequence"
            initialization_results["action_sequencing"] = True
            print("   ✓ 动作序列模块接口验证通过")
        except Exception as e:
            initialization_results["action_sequencing"] = False
            print(f"   ✗ 动作序列模块验证失败: {e}")

        # 记录结果
        self.test_results.append({
            "test": "module_initialization_enhanced",
            "success": all(initialization_results.values()),
            "message": f"模块初始化验证: {sum(initialization_results.values())}/4 模块通过",
            "details": initialization_results
        })

    def test_goal_to_subgoal_data_flow(self):
        """验证目标解释到子目标分解的数据传输格式一致性"""
        print("\n2. 目标→子目标数据传输测试...")
        try:
            # 1. 生成目标解释结果
            goal_text = "把红色球放进盒子，再放到桌子上"
            goal_result = self.goal_interpreter.interpret(goal_text)
            assert goal_result is not None, "目标解释失败"
            assert "ltl_formula" in goal_result, "目标结果缺少LTL公式"
            
            # 2. 验证LTL公式格式（兼容字符串和LTLFormula对象）
            ltl_input = goal_result["ltl_formula"]
            if isinstance(ltl_input, str):
                # 转换为LTLFormula对象（模拟子目标模块的预期输入）
                ltl_formula = LTLFormula(ltl_input)
            elif isinstance(ltl_input, LTLFormula):
                ltl_formula = ltl_input
            else:
                raise TypeError(f"LTL公式格式错误，预期str或LTLFormula，实际{type(ltl_input)}")
            
            # 3. 传递给子目标分解模块
            subgoal_result = self.subgoal_decomposer.decompose(ltl_formula=ltl_formula)
            assert isinstance(subgoal_result, DecompositionResult), "子目标分解结果类型错误"
            assert len(subgoal_result.subgoals) > 0, "未生成子目标"
            
            # 4. 验证子目标数据结构
            for sg in subgoal_result.subgoals:
                assert hasattr(sg, "id"), "子目标缺少id"
                assert hasattr(sg, "description"), "子目标缺少description"
                assert hasattr(sg, "preconditions"), "子目标缺少preconditions"
                assert isinstance(sg.preconditions, list), "preconditions应为列表类型"
            
            self.data_format_checks["goal_to_subgoal"] = True
            print("   ✓ 目标→子目标数据传输格式验证通过")
            self.test_results.append({
                "test": "goal_to_subgoal_flow",
                "success": True,
                "message": f"成功传输并分解为{len(subgoal_result.subgoals)}个子目标"
            })
        except Exception as e:
            self.data_format_checks["goal_to_subgoal"] = False
            print(f"   ✗ 目标→子目标数据传输失败: {e}")
            self.test_results.append({
                "test": "goal_to_subgoal_flow",
                "success": False,
                "message": str(e)
            })

    def test_subgoal_to_transition_interface(self):
        """验证子目标分解到转换建模的接口适配性"""
        print("\n3. 子目标→转换建模接口测试...")
        try:
            # 1. 准备测试数据（模拟前序流程）
            test_goal = "移动绿色积木到指定区域"
            ltl_formula = LTLFormula(f"F(green_block_at_target)")
            subgoal_set = self.subgoal_decomposer.decompose(ltl_formula=ltl_formula)
            assert len(subgoal_set.subgoals) > 0, "未生成测试用子目标"
            
            # 2. 构造转换建模请求（验证子目标数据的适配性）
            subgoal_states = {
                "initial_state": {"block_position": "origin", "robot_position": "start"},
                "goal_state": {"block_position": "target", "robot_position": "target"}
            }
            # 从子目标提取状态约束
            for sg in subgoal_set.subgoals:
                if "pick" in sg.description.lower():
                    subgoal_states["mid_state_pick"] = {"holding": "green_block"}
                if "place" in sg.description.lower():
                    subgoal_states["mid_state_place"] = {"holding": None}
            
            # 3. 验证转换建模接口对复杂状态的处理
            modeling_request = ModelingRequest(
                initial_state=subgoal_states["initial_state"],
                goal_state=subgoal_states["goal_state"],
                available_transitions=self.transition_modeler.create_sample_transitions()
            )
            transition_response = self.transition_modeler.model_transitions(modeling_request)
            
            # 4. 验证转换建模输出格式
            assert transition_response.success, "转换建模失败"
            assert isinstance(transition_response.predicted_sequences, list), "转换序列应为列表"
            assert all(isinstance(seq, list) for seq in transition_response.predicted_sequences), "序列项应为列表"
            assert all(isinstance(t, StateTransition) for seq in transition_response.predicted_sequences for t in seq), \
                "序列项应为StateTransition类型"
            
            self.data_format_checks["subgoal_to_transition"] = True
            print("   ✓ 子目标→转换建模接口适配通过")
            self.test_results.append({
                "test": "subgoal_to_transition_interface",
                "success": True,
                "message": f"生成{len(transition_response.predicted_sequences)}个转换序列"
            })
        except Exception as e:
            self.data_format_checks["subgoal_to_transition"] = False
            print(f"   ✗ 子目标→转换建模接口适配失败: {e}")
            self.test_results.append({
                "test": "subgoal_to_transition_interface",
                "success": False,
                "message": str(e)
            })

    def test_transition_to_action_param_pass(self):
        """验证转换建模到动作序列的参数传递准确性"""
        print("\n4. 转换→动作序列参数传递测试...")
        try:
            # 1. 生成转换建模结果（含详细参数）
            test_transitions = [
                StateTransition(
                    name="move",
                    description="从A移动到B",
                    preconditions=[StateCondition(predicate="at", value="A"), StateCondition(predicate="holding", value=None)],
                    effects=[StateEffect(predicate="at", value="B"), StateEffect(predicate="holding", value=None)],
                    parameters={"speed": 1.2, "path": "A→B"}
                ),
                StateTransition(
                    name="pick",
                    description="在B位置拾取盒子",
                    preconditions=[StateCondition(predicate="at", value="B"), StateCondition(predicate="holding", value=None)],
                    effects=[StateEffect(predicate="at", value="B"), StateEffect(predicate="holding", value="box")],
                    parameters={"object": "box", "force": 5.0}
                )
            ]
            modeling_request = ModelingRequest(
                initial_state={"at": "A", "holding": None},
                goal_state={"at": "B", "holding": "box"},
                available_transitions=test_transitions
            )
            transition_result = self.transition_modeler.model_transitions(modeling_request)
            assert transition_result.success, "转换建模失败"
            
            # 2. 构造动作序列请求（验证参数提取准确性）
            sequencing_request = SequencingRequest(
                initial_state=modeling_request.initial_state,
                goal_state=modeling_request.goal_state,
                available_actions=[
                    Action(
                        id="move",
                        name="move",
                        action_type=ActionType.NAVIGATION,
                        parameters={}
                    ),
                    Action(
                        id="pick",
                        name="pick",
                        action_type=ActionType.MANIPULATION,
                        parameters={}
                    )
                ],
                state_transitions=transition_result.predicted_sequences[0]  # 取第一个预测序列
            )
            
            # 3. 生成动作序列并验证参数传递
            sequence_response = self.action_sequencer.generate_sequence(sequencing_request)
            assert sequence_response.success, "动作序列生成失败"
            assert len(sequence_response.action_sequence) >= 2, "动作序列长度不足"
            
            # 验证参数准确性（转换中的参数应被正确传递到动作）
            move_action = next(a for a in sequence_response.action_sequence if a.name == "move")
            assert move_action.parameters.get("speed") == 1.2, "move动作参数传递错误"
            assert move_action.parameters.get("path") == "A→B", "move动作路径参数丢失"
            
            pick_action = next(a for a in sequence_response.action_sequence if a.name == "pick")
            assert pick_action.parameters.get("object") == "box", "pick动作对象参数错误"
            
            self.data_format_checks["transition_to_action"] = True
            print("   ✓ 转换→动作序列参数传递准确")
            self.test_results.append({
                "test": "transition_to_action_param_pass",
                "success": True,
                "message": f"动作序列参数验证通过，共{len(sequence_response.action_sequence)}个动作"
            })
        except Exception as e:
            self.data_format_checks["transition_to_action"] = False
            print(f"   ✗ 转换→动作序列参数传递失败: {e}")
            self.test_results.append({
                "test": "transition_to_action_param_pass",
                "success": False,
                "message": str(e)
            })

    def test_end_to_end_with_data_validation(self):
        """完整端到端流程测试，含全链路数据格式校验"""
        print("\n5. 端到端全链路测试...")
        try:
            # 1. 目标解释
            goal_text = "打开冰箱，取出牛奶，倒入杯子"
            print(f"   测试目标: {goal_text}")
            
            goal_result = self.goal_interpreter.interpret(goal_text)
            assert goal_result and "ltl_formula" in goal_result, "目标解释失败"
            ltl_formula = goal_result["ltl_formula"]
            print(f"   目标解释生成LTL: {ltl_formula}")
            
            # 2. 子目标分解
            subgoal_result = self.subgoal_decomposer.decompose(ltl_formula=ltl_formula)
            assert isinstance(subgoal_result, DecompositionResult) and len(subgoal_result.subgoals) > 0, "子目标分解失败"
            subgoal_descriptions = [sg.description for sg in subgoal_result.subgoals]
            print(f"   子目标分解结果: {subgoal_descriptions}")
            
            # 3. 转换建模
            modeling_request = ModelingRequest(
                initial_state={
                    "robot_position": "kitchen_door",
                    "fridge_state": "closed",
                    "holding": None,
                    "cup_has_milk": False
                },
                goal_state={
                    "robot_position": "counter",
                    "fridge_state": "closed",
                    "holding": None,
                    "cup_has_milk": True
                },
                available_transitions=self.transition_modeler.create_sample_transitions()
            )
            transition_result = self.transition_modeler.model_transitions(modeling_request)
            assert transition_result.success, "转换建模失败"
            
            # 4. 动作序列生成
            sequencing_request = SequencingRequest(
                initial_state=modeling_request.initial_state,
                goal_state=modeling_request.goal_state,
                available_actions=[
                    Action(id="open_fridge", name="open_fridge", action_type=ActionType.MANIPULATION),
                    Action(id="take_milk", name="take_milk", action_type=ActionType.MANIPULATION),
                    Action(id="pour_milk", name="pour_milk", action_type=ActionType.MANIPULATION),
                    Action(id="close_fridge", name="close_fridge", action_type=ActionType.MANIPULATION)
                ],
                state_transitions=transition_result.predicted_sequences[0]
            )
            sequence_result = self.action_sequencer.generate_sequence(sequencing_request)
            assert sequence_result.success and len(sequence_result.action_sequence) > 0, "动作序列生成失败"
            
            # 5. 全链路数据一致性最终验证
            assert all(self.data_format_checks.values()), "存在数据格式不一致问题"
            print(f"   端到端流程完成，生成动作序列: {[a.name for a in sequence_result.action_sequence]}")
            
            self.test_results.append({
                "test": "end_to_end_with_validation",
                "success": True,
                "message": "全链路流程及数据验证通过",
                "details": {
                    "subgoal_count": len(subgoal_result.subgoals),
                    "action_count": len(sequence_result.action_sequence)
                }
            })
        except Exception as e:
            print(f"   ✗ 端到端流程失败: {e}")
            self.test_results.append({
                "test": "end_to_end_with_validation",
                "success": False,
                "message": str(e),
                "data_format_issues": [k for k, v in self.data_format_checks.items() if not v]
            })

    def test_data_fault_tolerance(self):
        """测试模块对异常数据的容错能力"""
        print("\n6. 数据容错能力测试...")
        fault_tolerance_results = {}
        
        # 测试目标解释模块接收无效输入
        try:
            invalid_goal = 123  # 非字符串输入
            result = self.goal_interpreter.interpret(invalid_goal)
            assert result is None or isinstance(result, dict), "目标解释对无效输入容错不足"
            fault_tolerance_results["invalid_goal_input"] = True
        except Exception as e:
            fault_tolerance_results["invalid_goal_input"] = False
            print(f"   ✗ 目标解释模块容错失败: {e}")
        
        # 测试子目标分解接收空LTL
        try:
            empty_ltl = LTLFormula("")
            result = self.subgoal_decomposer.decompose(ltl_formula=empty_ltl)
            assert result is None or len(result.subgoals) == 0, "子目标分解对空LTL容错不足"
            fault_tolerance_results["empty_ltl_input"] = True
        except Exception as e:
            fault_tolerance_results["empty_ltl_input"] = False
            print(f"   ✗ 子目标分解模块容错失败: {e}")
        
        # 测试转换建模接收冲突状态
        try:
            conflicting_request = ModelingRequest(
                initial_state={"at": "A", "at": "B"},  # 冲突状态
                goal_state={"at": "C"},
                available_transitions=[]
            )
            result = self.transition_modeler.model_transitions(conflicting_request)
            assert not result.success and result.error_message, "转换建模对冲突状态处理不足"
            fault_tolerance_results["conflicting_state_input"] = True
        except Exception as e:
            fault_tolerance_results["conflicting_state_input"] = False
            print(f"   ✗ 转换建模模块容错失败: {e}")
        
        self.test_results.append({
            "test": "data_fault_tolerance",
            "success": all(fault_tolerance_results.values()),
            "message": f"数据容错测试: {sum(fault_tolerance_results.values())}/{len(fault_tolerance_results)} 项通过",
            "details": fault_tolerance_results
        })

    def test_performance_with_interaction_latency(self):
        """测试性能与模块交互延迟"""
        print("\n7. 性能与交互延迟测试...")
        performance_data = {}
        
        # 测量目标→子目标延迟
        start = time.time()
        goal_result = self.goal_interpreter.interpret("把书放到书架第三层")
        subgoal_result = self.subgoal_decomposer.decompose(ltl_formula=goal_result["ltl_formula"])
        performance_data["goal_to_subgoal_latency"] = time.time() - start
        
        # 测量转换建模延迟
        start = time.time()
        modeling_request = ModelingRequest(
            initial_state={"book_position": "desk", "shelf_layer": 3},
            goal_state={"book_position": "shelf_3"},
            available_transitions=self.transition_modeler.create_sample_transitions()
        )
        self.transition_modeler.model_transitions(modeling_request)
        performance_data["transition_modeling_latency"] = time.time() - start
        
        # 测量动作序列生成延迟
        start = time.time()
        sequencing_request = SequencingRequest(
            initial_state=modeling_request.initial_state,
            goal_state=modeling_request.goal_state,
            available_actions=[Action(id="move_book", name="move_book", action_type=ActionType.MANIPULATION)]
        )
        self.action_sequencer.generate_sequence(sequencing_request)
        performance_data["action_sequencing_latency"] = time.time() - start
        
        # 验证延迟阈值（可根据实际需求调整）
        latency_thresholds = {
            "goal_to_subgoal_latency": 2.0,  # 2秒
            "transition_modeling_latency": 3.0,  # 3秒
            "action_sequencing_latency": 2.0   # 2秒
        }
        latency_checks = {k: v < latency_thresholds[k] for k, v in performance_data.items()}
        
        print(f"   交互延迟: {json.dumps(performance_data, indent=2)}")
        self.test_results.append({
            "test": "performance_with_latency",
            "success": all(latency_checks.values()),
            "message": "模块交互延迟测试完成",
            "details": {
                "latency_data": performance_data,
                "threshold_checks": latency_checks
            }
        })

    def generate_enhanced_report(self):
        """生成增强版测试报告，含数据传输校验结果"""
        print("\n" + "=" * 80)
        print("增强版四模块集成测试报告")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        
        print(f"测试总览: {passed_tests}/{total_tests} 测试通过")
        print("\n数据传输格式校验结果:")
        for link, status in self.data_format_checks.items():
            print(f"   {link}: {'✓ 正常' if status else '✗ 异常'}")
        
        print("\n详细测试结果:")
        for i, result in enumerate(self.test_results, 1):
            status = "✓ 成功" if result["success"] else "✗ 失败"
            print(f"\n{i}. {result['test']}: {status}")
            print(f"   消息: {result['message']}")
            if "details" in result:
                print(f"   详情: {json.dumps(result['details'], ensure_ascii=False, indent=2)}")
        
        print("\n" + "=" * 80)
        print("测试完成" + " " * 68 + f"耗时: {time.time() - self.start_time:.2f}s")


if __name__ == "__main__":
    tester = FourModuleIntegrationTester()
    tester.run_comprehensive_integration_test()