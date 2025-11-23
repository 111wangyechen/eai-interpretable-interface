#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成评估测试脚本
测试更新后的子目标分解评估和动作序列生成评估功能
"""

import sys
import os
import json
from typing import Dict, List, Any
import traceback
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入集成模块
from goal_interpretation.goal_interpreter import GoalInterpreter
from subgoal_decomposition.subgoal_decomposer_integration import SubgoalDecomposerIntegration
from action_sequencing.action_sequencer_integration import ActionSequencerIntegration

class IntegrationEvaluationTester:
    """集成评估测试类"""
    
    def __init__(self):
        """初始化测试器"""
        self.goal_interpreter = GoalInterpreter()
        self.subgoal_integration = SubgoalDecomposerIntegration(config={
            'evaluate_results': True,
            'evaluator_config': {
                'enabled': True,
                'metrics': ['completeness', 'coherence', 'efficiency', 'correctness']
            }
        })
        self.action_integration = ActionSequencerIntegration(config={
            'evaluate_results': True,
            'evaluator_config': {
                'enabled': True,
                'metrics': ['sequence_quality', 'execution_feasibility', 'resource_efficiency']
            }
        })
        
        print("🔧 初始化集成评估测试器")
        print(f"   - 目标解释器: {type(self.goal_interpreter).__name__}")
        print(f"   - 子目标分解集成: {type(self.subgoal_integration).__name__}")
        print(f"   - 动作序列集成: {type(self.action_integration).__name__}")
    
    def test_goal_interpretation(self, natural_goal: str) -> Any:
        """测试目标解释模块"""
        print(f"\n📝 测试目标解释: '{natural_goal}'")
        
        try:
            ltl_formula = self.goal_interpreter.interpret(natural_goal)
            print(f"✅ 目标解释成功")
            print(f"   LTL公式: {ltl_formula.formula}")
            return ltl_formula
            
        except Exception as e:
            print(f"❌ 目标解释失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def test_subgoal_decomposition_evaluation(self, ltl_formula: Any) -> Any:
        """测试子目标分解评估功能"""
        print(f"\n🎯 测试子目标分解评估: '{ltl_formula.formula}'")
        
        try:
            # 使用评估功能进行子目标分解
            decomposition_result = self.subgoal_integration.decompose_with_evaluation(
                ltl_formula, 
                evaluate=True
            )
            
            print(f"✅ 子目标分解评估成功")
            print(f"   子目标数量: {len(decomposition_result.subgoals)}")
            print(f"   执行顺序: {decomposition_result.execution_order}")
            print(f"   总成本: {decomposition_result.total_cost:.2f}")
            
            # 检查评估结果
            if hasattr(decomposition_result, 'evaluation_results') and decomposition_result.evaluation_results:
                print(f"   评估结果:")
                for metric, value in decomposition_result.evaluation_results.items():
                    print(f"     - {metric}: {value}")
            else:
                print(f"   ⚠️  未找到评估结果")
            
            return decomposition_result
            
        except Exception as e:
            print(f"❌ 子目标分解评估失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def test_action_sequence_evaluation(self, decomposition_result: Any) -> Any:
        """测试动作序列生成评估功能"""
        print(f"\n⚡ 测试动作序列生成评估")
        
        try:
            # 准备请求参数
            request_params = {
                'decomposition_result': decomposition_result,
                'initial_state': {},
                'context': {
                    'goal': decomposition_result.original_goal,
                    'execution_environment': 'simulation'
                }
            }
            
            # 使用评估功能生成动作序列
            sequence_result = self.action_integration.sequence_actions_for_integration(
                request_params, 
                evaluate=True
            )
            
            print(f"✅ 动作序列生成评估成功")
            print(f"   动作数量: {len(sequence_result.action_sequence)}")
            print(f"   置信度: {sequence_result.confidence_score:.2f}")
            
            # 检查评估结果
            if hasattr(sequence_result, 'evaluation_results') and sequence_result.evaluation_results:
                print(f"   评估结果:")
                for metric, value in sequence_result.evaluation_results.items():
                    print(f"     - {metric}: {value}")
            else:
                print(f"   ⚠️  未找到评估结果")
            
            # 显示动作序列
            for i, action in enumerate(sequence_result.action_sequence):
                print(f"   动作 {i+1}: {action['name']} (类型: {action['type']})")
            
            return sequence_result
            
        except Exception as e:
            print(f"❌ 动作序列生成评估失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def test_end_to_end_evaluation(self, natural_goal: str) -> Dict:
        """测试端到端评估流程"""
        print(f"\n🚀 测试端到端评估: '{natural_goal}'")
        print("=" * 60)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "natural_goal": natural_goal,
            "success": False,
            "ltl_formula": None,
            "subgoal_evaluation": None,
            "action_evaluation": None,
            "errors": []
        }
        
        try:
            # 步骤1: 目标解释
            ltl_formula = self.test_goal_interpretation(natural_goal)
            if not ltl_formula:
                result["errors"].append("目标解释失败")
                return result
            
            result["ltl_formula"] = ltl_formula.formula
            
            # 步骤2: 子目标分解评估
            decomposition_result = self.test_subgoal_decomposition_evaluation(ltl_formula)
            if not decomposition_result:
                result["errors"].append("子目标分解评估失败")
                return result
            
            result["subgoal_evaluation"] = {
                "subgoal_count": len(decomposition_result.subgoals),
                "evaluation": getattr(decomposition_result, 'evaluation_results', None)
            }
            
            # 步骤3: 动作序列生成评估
            action_result = self.test_action_sequence_evaluation(decomposition_result)
            if not action_result:
                result["errors"].append("动作序列生成评估失败")
                return result
            
            result["action_evaluation"] = {
                "action_count": len(action_result.action_sequence),
                "confidence": action_result.confidence_score,
                "evaluation": getattr(action_result, 'evaluation_results', None)
            }
            
            result["success"] = True
            print(f"\n🎉 端到端评估测试成功!")
            
        except Exception as e:
            result["errors"].append(f"评估测试异常: {str(e)}")
            print(f"\n❌ 端到端评估测试失败: {str(e)}")
            traceback.print_exc()
        
        return result
    
    def test_with_builtin_goals(self):
        """使用内置目标测试评估功能"""
        test_goals = [
            "先去厨房拿杯子，然后到客厅喝水",
            "如果下雨，就带伞出门",
            "每天早上先刷牙，然后洗脸，最后吃早餐",
            "将书从书架拿到桌子上，然后打开电脑"
        ]
        
        print(f"\n🧪 使用内置目标进行评估测试")
        print("=" * 60)
        
        results = []
        for i, goal in enumerate(test_goals, 1):
            print(f"\n--- 测试 {i}/{len(test_goals)} ---\n")
            result = self.test_end_to_end_evaluation(goal)
            results.append(result)
        
        # 统计结果
        successful_tests = sum(1 for r in results if r["success"])
        print(f"\n📊 评估测试结果统计:")
        print(f"   总测试数: {len(results)}")
        print(f"   成功数: {successful_tests}")
        print(f"   失败数: {len(results) - successful_tests}")
        print(f"   成功率: {successful_tests/len(results)*100:.1f}%")
        
        # 保存结果
        self._save_test_results(results)
        
        return results
    
    def _save_test_results(self, results: List[Dict]):
        """保存测试结果到文件"""
        try:
            result_dir = os.path.join(project_root, 'test_results')
            os.makedirs(result_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(result_dir, f"evaluation_test_results_{timestamp}.json")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 测试结果已保存到: {filename}")
            
        except Exception as e:
            print(f"⚠️  保存测试结果失败: {str(e)}")
    
    def test_evaluation_metrics(self):
        """测试不同评估指标的有效性"""
        print(f"\n📈 测试评估指标")
        print("=" * 60)
        
        # 测试场景1: 简单目标
        simple_goal = "到达客厅"
        # 测试场景2: 复杂目标
        complex_goal = "如果下雨，带伞去超市买牛奶和面包，然后回家"
        
        print(f"\n场景1: 简单目标 '{simple_goal}'")
        simple_result = self.test_end_to_end_evaluation(simple_goal)
        
        print(f"\n场景2: 复杂目标 '{complex_goal}'")
        complex_result = self.test_end_to_end_evaluation(complex_goal)
        
        # 比较结果
        print(f"\n🔍 评估指标比较:")
        
        if simple_result.get("subgoal_evaluation") and complex_result.get("subgoal_evaluation"):
            simple_eval = simple_result["subgoal_evaluation"].get("evaluation", {})
            complex_eval = complex_result["subgoal_evaluation"].get("evaluation", {})
            
            print(f"\n子目标分解评估比较:")
            metrics = set(simple_eval.keys()) | set(complex_eval.keys())
            for metric in metrics:
                simple_val = simple_eval.get(metric, "N/A")
                complex_val = complex_eval.get(metric, "N/A")
                print(f"   {metric}: 简单目标={simple_val}, 复杂目标={complex_val}")
        
        return {"simple_goal": simple_result, "complex_goal": complex_result}

def main():
    """主函数"""
    print("🔬 集成评估功能测试")
    print("=" * 60)
    
    try:
        # 创建测试器
        tester = IntegrationEvaluationTester()
        
        # 运行内置目标测试
        print("\n第一部分: 基本评估功能测试")
        results = tester.test_with_builtin_goals()
        
        # 运行评估指标测试
        print("\n\n第二部分: 评估指标有效性测试")
        metrics_results = tester.test_evaluation_metrics()
        
        print(f"\n✅ 所有测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()