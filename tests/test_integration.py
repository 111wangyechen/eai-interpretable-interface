#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三个模块联动测试脚本
测试goal_interpretation、subgoal_decomposition和action_sequencing的集成效果
"""

import sys
import os
from typing import Dict, List, Any
import traceback
import re

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入三个模块的核心组件
from goal_interpretation.goal_interpreter import GoalInterpreter, LTLFormula
from subgoal_decomposition.subgoal_decomposer import SubgoalDecomposer, DecompositionStrategy, Subgoal, SubgoalType
from subgoal_decomposition.subgoal_ltl_integration import SubgoalLTLIntegration
from action_sequencing.action_sequencer import ActionSequencer, SequencingRequest, SequencingConfig
from action_sequencing.action_data import Action, ActionType, ActionStatus
from action_sequencing.state_manager import EnvironmentState


class ModuleIntegrationTester:
    """三个模块集成测试类"""
    
    def __init__(self):
        """初始化测试器"""
        self.goal_interpreter = GoalInterpreter()
        self.subgoal_decomposer = SubgoalDecomposer(DecompositionStrategy.TEMPORAL_HIERARCHICAL)
        self.action_sequencer = ActionSequencer()
        self.integration = SubgoalLTLIntegration()
        
        print("🔧 初始化三个模块集成测试器")
        print(f"   - 目标解释器: {type(self.goal_interpreter).__name__}")
        print(f"   - 子目标分解器: {type(self.subgoal_decomposer).__name__}")
        print(f"   - 动作序列器: {type(self.action_sequencer).__name__}")
        print(f"   - 集成接口: {type(self.integration).__name__}")
    
    def test_goal_interpretation(self, natural_goal: str) -> LTLFormula:
        """测试目标解释模块"""
        print(f"\n📝 测试目标解释: '{natural_goal}'")
        
        try:
            ltl_formula = self.goal_interpreter.interpret(natural_goal)
            print(f"✅ 目标解释成功")
            print(f"   LTL公式: {ltl_formula.formula}")
            print(f"   有效性: {ltl_formula.is_valid()}")
            if hasattr(ltl_formula, 'semantics') and ltl_formula.semantics:
                print(f"   语义信息: {len(ltl_formula.semantics)} 个字段")
            
            return ltl_formula
            
        except Exception as e:
            print(f"❌ 目标解释失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def test_subgoal_decomposition(self, ltl_formula: LTLFormula) -> Any:
        """测试子目标分解模块"""
        print(f"\n🎯 测试子目标分解: '{ltl_formula.formula}'")
        
        try:
            decomposition_result = self.subgoal_decomposer.decompose(ltl_formula)
            print(f"✅ 子目标分解成功")
            print(f"   子目标数量: {len(decomposition_result.subgoals)}")
            print(f"   根子目标: {decomposition_result.root_subgoal}")
            print(f"   执行顺序: {decomposition_result.execution_order}")
            print(f"   总成本: {decomposition_result.total_cost:.2f}")
            
            # 显示子目标详情
            for i, subgoal in enumerate(decomposition_result.subgoals):
                print(f"   子目标 {i+1}: {subgoal.description}")
                print(f"     类型: {subgoal.subgoal_type}")
                print(f"     优先级: {subgoal.priority}")
                print(f"     LTL: {subgoal.ltl_formula}")
            
            return decomposition_result
            
        except Exception as e:
            print(f"❌ 子目标分解失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def subgoal_to_action(self, subgoal: Any) -> Any:
        """将子目标转换为动作"""
        action_id = f"action_{subgoal.id}"
        action_name = subgoal.description
        
        # 将子目标的前提条件转换为动作的前置条件（字符串列表）
        preconditions = []
        for cond in subgoal.preconditions:
            if '=' in cond:
                # 保持原始格式
                preconditions.append(cond.strip())
            else:
                # 如果不是key=value格式，转换为布尔条件格式
                preconditions.append(f"condition_{cond}=true")
        
        # 将子目标的效果转换为动作的效果（字符串列表）
        effects = []
        for effect in subgoal.effects:
            if '=' in effect:
                # 保持原始格式
                effects.append(effect.strip())
            else:
                # 如果不是key=value格式，转换为状态变量格式
                effects.append(f"{effect}=completed")
        
        # 如果效果为空，至少添加一个基于LTL公式的效果
        if not effects and subgoal.ltl_formula:
            formula = subgoal.ltl_formula
            # 简化公式，移除操作符
            clean_formula = re.sub(r'[F&|()!->]', '', formula).strip()
            if clean_formula:
                effects.append(f"{clean_formula}=true")
            else:
                effects.append("goal_achieved=true")
        
        # 根据子目标类型选择动作类型
        if subgoal.subgoal_type == SubgoalType.ATOMIC:
            action_type = ActionType.MANIPULATION  # 使用MANIPULATION替代ATOMIC
        elif subgoal.subgoal_type == SubgoalType.SEQUENTIAL:
            action_type = ActionType.NAVIGATION
        elif subgoal.subgoal_type == SubgoalType.CONDITIONAL:
            action_type = ActionType.CONDITIONAL
        elif subgoal.subgoal_type == SubgoalType.PARALLEL:
            action_type = ActionType.PERCEPTION
        else:
            action_type = ActionType.MANIPULATION  # 默认使用MANIPULATION
        
        return Action(
            id=action_id,
            name=action_name,
            action_type=action_type,
            preconditions=preconditions,
            effects=effects,
            duration=1.0,
            success_probability=1.0
        )
    
    def test_action_sequencing(self, decomposition_result: Any) -> Any:
        """测试动作序列模块"""
        print(f"\n⚡ 测试动作序列生成")
        
        try:
            # 将子目标转换为动作
            actions = []
            for subgoal in decomposition_result.subgoals:
                action = self.subgoal_to_action(subgoal)
                actions.append(action)
            
            print(f"   转换得到 {len(actions)} 个动作")
            
            # 创建初始状态和目标状态
            initial_state = EnvironmentState()
            goal_state = EnvironmentState()
            
            # 从子目标中提取状态信息
            for subgoal in decomposition_result.subgoals:
                # 添加子目标的效果到目标状态
                for effect in subgoal.effects:
                    if '=' in effect:
                        key, value = effect.split('=', 1)
                        # 先添加状态变量，然后设置值
                        from action_sequencing.state_manager import StateVariable, StateType
                        var = StateVariable(name=key.strip(), value=value.strip(), state_type=StateType.BOOLEAN)
                        goal_state.add_variable(var)
                    else:
                        # 如果不是key=value格式，将效果作为状态变量
                        from action_sequencing.state_manager import StateVariable, StateType
                        var = StateVariable(name=effect, value="completed", state_type=StateType.BOOLEAN)
                        goal_state.add_variable(var)
                
                # 如果没有效果，使用LTL公式
                if not subgoal.effects and subgoal.ltl_formula:
                    formula = subgoal.ltl_formula
                    # 简化公式，移除操作符
                    clean_formula = re.sub(r'[F&|()!->]', '', formula).strip()
                    if clean_formula:
                        from action_sequencing.state_manager import StateVariable, StateType
                        var = StateVariable(name=clean_formula, value="true", state_type=StateType.BOOLEAN)
                        goal_state.add_variable(var)
                    else:
                        from action_sequencing.state_manager import StateVariable, StateType
                        var = StateVariable(name="goal_achieved", value="true", state_type=StateType.BOOLEAN)
                        goal_state.add_variable(var)
            
            # 创建序列请求 - 使用字典而不是EnvironmentState对象
            request = SequencingRequest(
                initial_state=initial_state.get_state_dict(),
                goal_state=goal_state.get_state_dict(),
                available_actions=actions
            )
            
            # 生成动作序列
            response = self.action_sequencer.generate_sequence(request)
            
            print(f"✅ 动作序列生成成功")
            print(f"   状态: {'成功' if response.success else '失败'}")
            if response.action_sequence:
                print(f"   动作数量: {len(response.action_sequence.actions)}")
            else:
                print(f"   动作数量: 0")
            print(f"   执行时间: {response.execution_time:.3f}秒")
            
            # 显示动作序列
            if response.action_sequence and response.action_sequence.actions:
                for i, action in enumerate(response.action_sequence.actions):
                    print(f"   动作 {i+1}: {action.name} ({action.id})")
            
            return response
            
        except Exception as e:
            print(f"❌ 动作序列生成失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def test_end_to_end_integration(self, natural_goal: str) -> Dict:
        """测试端到端集成"""
        print(f"\n🚀 测试端到端集成: '{natural_goal}'")
        print("=" * 60)
        
        result = {
            "natural_goal": natural_goal,
            "success": False,
            "ltl_formula": None,
            "decomposition_result": None,
            "action_sequence": None,
            "errors": []
        }
        
        try:
            # 步骤1: 目标解释
            ltl_formula = self.test_goal_interpretation(natural_goal)
            if not ltl_formula:
                result["errors"].append("目标解释失败")
                return result
            
            result["ltl_formula"] = ltl_formula.formula
            
            # 步骤2: 子目标分解
            decomposition_result = self.test_subgoal_decomposition(ltl_formula)
            if not decomposition_result:
                result["errors"].append("子目标分解失败")
                return result
            
            result["decomposition_result"] = {
                "subgoal_count": len(decomposition_result.subgoals),
                "execution_order": decomposition_result.execution_order,
                "total_cost": decomposition_result.total_cost
            }
            
            # 步骤3: 动作序列生成
            action_sequence = self.test_action_sequencing(decomposition_result)
            if not action_sequence:
                result["errors"].append("动作序列生成失败")
                return result
            
            result["action_sequence"] = {
                "action_count": len(action_sequence.action_sequence.actions) if action_sequence.action_sequence else 0,
                "success": action_sequence.success,
                "execution_time": action_sequence.execution_time
            }
            
            result["success"] = True
            print(f"\n🎉 端到端集成测试成功!")
            
        except Exception as e:
            result["errors"].append(f"集成测试异常: {str(e)}")
            print(f"\n❌ 端到端集成测试失败: {str(e)}")
            traceback.print_exc()
        
        return result
    
    def test_with_builtin_goals(self):
        """使用内置目标测试"""
        test_goals = [
            "最终要到达客厅",
            "先去厨房然后去卧室",
            "总是保持客厅干净",
            "如果门开了就关上门",
            "重复打扫房间三次"
        ]
        
        print(f"\n🧪 使用内置目标进行测试")
        print("=" * 60)
        
        results = []
        for i, goal in enumerate(test_goals, 1):
            print(f"\n--- 测试 {i}/{len(test_goals)} ---")
            result = self.test_end_to_end_integration(goal)
            results.append(result)
        
        # 统计结果
        successful_tests = sum(1 for r in results if r["success"])
        print(f"\n📊 测试结果统计:")
        print(f"   总测试数: {len(results)}")
        print(f"   成功数: {successful_tests}")
        print(f"   失败数: {len(results) - successful_tests}")
        print(f"   成功率: {successful_tests/len(results)*100:.1f}%")
        
        return results


def main():
    """主函数"""
    print("🔬 三个模块联动测试")
    print("=" * 60)
    
    try:
        # 创建测试器
        tester = ModuleIntegrationTester()
        
        # 运行内置目标测试
        results = tester.test_with_builtin_goals()
        
        print(f"\n✅ 测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    main()