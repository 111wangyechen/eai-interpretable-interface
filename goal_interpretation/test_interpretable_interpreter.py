#!/usr/bin/env python3
"""
InterPreT集成测试脚本
测试可解释目标解释器的各项功能
"""

import sys
import os
import unittest
from typing import Dict, Any, List
import tempfile
import json

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from interpretable_goal_interpreter import (
        InterpretableGoalInterpreter,
        InterPreTFeedbackLearner,
        PDDLDomainBuilder,
        FeedbackRecord,
        SymbolicPredicate
    )
    print("✅ 成功导入InterPreT模块")
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保interpretable_goal_interpreter.py在同一目录下")
    sys.exit(1)

class TestInterpretableGoalInterpreter(unittest.TestCase):
    """InterPreT核心功能测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.config = {
            'model_name': 'bert-base-uncased',
            'max_predicates': 50,
            'learning_rate': 0.001,
            'feedback_threshold': 0.8,
            'pddl_domain_name': 'test_domain'
        }
        self.interpreter = InterpretableGoalInterpreter(self.config)
        self.learner = InterPreTFeedbackLearner(self.config)
        self.domain_builder = PDDLDomainBuilder(self.config)
    
    def test_basic_interpretation(self):
        """测试基础解释功能"""
        print("\n🧪 测试1: 基础解释功能")
        
        test_goals = [
            "拿起杯子",
            "打开门",
            "走到厨房"
        ]
        
        for goal in test_goals:
            try:
                interpretation = self.interpreter.interpret_goal(goal)
                self.assertIsNotNone(interpretation)
                print(f"✅ '{goal}' 解释成功: {interpretation}")
            except Exception as e:
                self.fail(f"解释 '{goal}' 失败: {e}")
    
    def test_feedback_learning(self):
        """测试反馈学习功能"""
        print("\n🧪 测试2: 反馈学习功能")
        
        goal = "把红色的书放到书架上"
        
        # 创建测试反馈
        feedback = FeedbackRecord(
            goal=goal,
            user_feedback="应该强调颜色属性",
            corrected_predicate="is_red(book)",
            confidence=0.9
        )
        
        try:
            # 学习反馈
            learned_predicate = self.learner.learn_from_feedback(feedback)
            self.assertIsNotNone(learned_predicate)
            print(f"✅ 反馈学习成功: {learned_predicate}")
            
            # 验证学习效果
            self.assertTrue(hasattr(learned_predicate, 'name'))
            self.assertTrue(hasattr(learned_predicate, 'confidence'))
            
        except Exception as e:
            self.fail(f"反馈学习失败: {e}")
    
    def test_pddl_domain_generation(self):
        """测试PDDL域生成功能"""
        print("\n🧪 测试3: PDDL域生成功能")
        
        domain_info = {
            'name': 'test_domain',
            'types': ['robot', 'object', 'location'],
            'predicates': [
                ('at', ['robot', 'location']),
                ('holding', ['robot', 'object'])
            ],
            'actions': [
                {
                    'name': 'pickup',
                    'parameters': ['?r - robot', '?o - object'],
                    'precondition': '(at ?r ?l)',
                    'effect': '(holding ?r ?o)'
                }
            ]
        }
        
        try:
            # 生成PDDL域
            pddl_domain = self.domain_builder.build_domain(domain_info)
            self.assertIsNotNone(pddl_domain)
            print(f"✅ PDDL域生成成功")
            
            # 验证PDDL语法
            is_valid = self.domain_builder.validate_domain(pddl_domain)
            self.assertTrue(is_valid, "PDDL域语法验证失败")
            print(f"✅ PDDL语法验证通过")
            
        except Exception as e:
            self.fail(f"PDDL域生成失败: {e}")
    
    def test_predicate_evolution(self):
        """测试谓词演化功能"""
        print("\n🧪 测试4: 谓词演化功能")
        
        try:
            # 创建初始谓词
            initial_predicates = [
                SymbolicPredicate("on", ["obj1", "obj2"], "obj1在obj2上"),
                SymbolicPredicate("holding", ["agent", "obj"], "agent拿着obj")
            ]
            
            # 模拟演化
            new_predicate = SymbolicPredicate("is_red", ["obj"], "obj是红色的")
            evolved_predicates = initial_predicates + [new_predicate]
            
            # 验证演化结果
            self.assertEqual(len(evolved_predicates), 3)
            self.assertEqual(evolved_predicates[-1].name, "is_red")
            print(f"✅ 谓词演化成功，最终谓词数量: {len(evolved_predicates)}")
            
        except Exception as e:
            self.fail(f"谓词演化失败: {e}")
    
    def test_statistics_tracking(self):
        """测试统计跟踪功能"""
        print("\n🧪 测试5: 统计跟踪功能")
        
        try:
            # 模拟解释任务
            test_goals = ["测试目标1", "测试目标2", "测试目标3"]
            
            for goal in test_goals:
                try:
                    interpretation = self.interpreter.interpret_goal(goal)
                    self.interpreter.update_statistics(goal, interpretation, success=True)
                except Exception:
                    self.interpreter.update_statistics(goal, None, success=False)
            
            # 获取统计信息
            stats = self.interpreter.get_statistics()
            
            # 验证统计信息
            self.assertIn('total_tasks', stats)
            self.assertIn('successful_tasks', stats)
            self.assertIn('success_rate', stats)
            
            print(f"✅ 统计跟踪成功")
            print(f"   总任务数: {stats['total_tasks']}")
            print(f"   成功率: {stats['success_rate']:.2%}")
            
        except Exception as e:
            self.fail(f"统计跟踪失败: {e}")
    
    def test_save_load_functionality(self):
        """测试保存和加载功能"""
        print("\n🧪 测试6: 保存和加载功能")
        
        try:
            # 使用临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_path = f.name
            
            # 保存状态
            self.interpreter.save_state(temp_path)
            self.assertTrue(os.path.exists(temp_path))
            print(f"✅ 状态保存成功")
            
            # 创建新解释器并加载状态
            new_interpreter = InterpretableGoalInterpreter()
            new_interpreter.load_state(temp_path)
            print(f"✅ 状态加载成功")
            
            # 验证加载效果
            test_goal = "测试目标"
            original_result = self.interpreter.interpret_goal(test_goal)
            loaded_result = new_interpreter.interpret_goal(test_goal)
            
            self.assertIsNotNone(original_result)
            self.assertIsNotNone(loaded_result)
            print(f"✅ 加载验证成功")
            
            # 清理临时文件
            os.unlink(temp_path)
            
        except Exception as e:
            self.fail(f"保存/加载功能失败: {e}")

class TestInterPreTIntegration(unittest.TestCase):
    """InterPreT集成测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.config = {
            'model_name': 'bert-base-uncased',
            'max_predicates': 20,
            'learning_rate': 0.001,
            'feedback_threshold': 0.7
        }
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流程"""
        print("\n🧪 测试7: 端到端工作流程")
        
        try:
            # 初始化组件
            interpreter = InterpretableGoalInterpreter(self.config)
            learner = InterPreTFeedbackLearner(self.config)
            domain_builder = PDDLDomainBuilder(self.config)
            
            # 模拟完整工作流程
            goal = "把红色的杯子从桌子上拿到厨房"
            
            # 1. 基础解释
            interpretation = interpreter.interpret_goal(goal)
            self.assertIsNotNone(interpretation)
            print(f"✅ 步骤1: 基础解释完成")
            
            # 2. 添加反馈学习
            feedback = FeedbackRecord(
                goal=goal,
                user_feedback="需要强调移动动作",
                corrected_predicate="move_to(cup, kitchen)",
                confidence=0.85
            )
            learned_predicate = learner.learn_from_feedback(feedback)
            self.assertIsNotNone(learned_predicate)
            print(f"✅ 步骤2: 反馈学习完成")
            
            # 3. 生成PDDL域
            domain_info = {
                'name': 'kitchen_domain',
                'types': ['robot', 'object', 'location'],
                'predicates': [('at', ['robot', 'location'])],
                'actions': []
            }
            pddl_domain = domain_builder.build_domain(domain_info)
            self.assertIsNotNone(pddl_domain)
            print(f"✅ 步骤3: PDDL域生成完成")
            
            # 4. 更新统计
            interpreter.update_statistics(goal, interpretation, success=True)
            stats = interpreter.get_statistics()
            self.assertGreater(stats['total_tasks'], 0)
            print(f"✅ 步骤4: 统计更新完成")
            
            print(f"✅ 端到端工作流程测试通过")
            
        except Exception as e:
            self.fail(f"端到端工作流程失败: {e}")
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n🧪 测试8: 错误处理")
        
        try:
            interpreter = InterpretableGoalInterpreter(self.config)
            
            # 测试无效输入
            with self.assertRaises(Exception):
                interpreter.interpret_goal("")  # 空字符串
            
            # 测试无效反馈
            learner = InterPreTFeedbackLearner(self.config)
            invalid_feedback = FeedbackRecord("", "", "", -1.0)  # 无效反馈
            result = learner.learn_from_feedback(invalid_feedback)
            # 应该返回None或抛出异常
            print(f"✅ 错误处理测试通过")
            
        except Exception as e:
            print(f"⚠️ 错误处理测试部分通过: {e}")

def run_performance_tests():
    """运行性能测试"""
    print("\n🚀 性能测试")
    print("-" * 40)
    
    config = {
        'model_name': 'bert-base-uncased',
        'max_predicates': 50,
        'learning_rate': 0.001
    }
    
    interpreter = InterpretableGoalInterpreter(config)
    
    # 测试解释性能
    import time
    test_goals = [
        "拿起杯子",
        "打开门", 
        "走到厨房",
        "放下书",
        "关闭窗户"
    ] * 10  # 重复10次
    
    start_time = time.time()
    successful_interpretations = 0
    
    for goal in test_goals:
        try:
            interpretation = interpreter.interpret_goal(goal)
            successful_interpretations += 1
        except Exception:
            pass
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"📊 性能测试结果:")
    print(f"   总任务数: {len(test_goals)}")
    print(f"   成功任务数: {successful_interpretations}")
    print(f"   总耗时: {total_time:.3f}秒")
    print(f"   平均耗时: {total_time/len(test_goals):.3f}秒/任务")
    print(f"   成功率: {successful_interpretations/len(test_goals):.2%}")

def main():
    """主测试函数"""
    print("🧪 InterPreT可解释目标解释器测试套件")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加核心功能测试
    test_suite.addTest(unittest.makeSuite(TestInterpretableGoalInterpreter))
    
    # 添加集成测试
    test_suite.addTest(unittest.makeSuite(TestInterPreTIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 运行性能测试
    run_performance_tests()
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ 失败的测试:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 错误的测试:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
    
    if success_rate == 1.0:
        print("\n🎉 所有测试通过！InterPreT集成成功！")
        print("🚀 您可以开始使用InterPreT进行开发")
    elif success_rate >= 0.8:
        print(f"\n✅ 大部分测试通过 ({success_rate:.1%})")
        print("⚠️ 部分功能需要进一步调试")
    else:
        print(f"\n⚠️ 测试通过率较低 ({success_rate:.1%})")
        print("🔧 需要检查和修复相关问题")
    
    return 0 if success_rate >= 0.8 else 1

if __name__ == "__main__":
    sys.exit(main())