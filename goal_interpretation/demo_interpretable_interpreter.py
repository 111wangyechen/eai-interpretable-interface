#!/usr/bin/env python3
"""
InterPreT集成演示脚本
展示可解释目标解释器的核心功能
"""

import sys
import os
from typing import Dict, Any, List

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

class InterPreTDemo:
    """InterPreT演示类"""
    
    def __init__(self):
        """初始化演示环境"""
        self.interpreter = None
        self.learner = None
        self.domain_builder = None
        
    def setup_demo(self):
        """设置演示环境"""
        print("🔧 初始化InterPreT演示环境...")
        
        # 创建配置
        config = {
            'model_name': 'bert-base-uncased',
            'max_predicates': 50,
            'learning_rate': 0.001,
            'feedback_threshold': 0.8,
            'pddl_domain_name': 'interprable_domain'
        }
        
        try:
            # 初始化核心组件
            self.interpreter = InterpretableGoalInterpreter(config)
            self.learner = InterPreTFeedbackLearner(config)
            self.domain_builder = PDDLDomainBuilder(config)
            
            print("✅ InterPreT组件初始化成功")
            return True
            
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            return False
    
    def demo_basic_interpretation(self):
        """演示基础目标解释功能"""
        print("\n🎯 演示1: 基础目标解释")
        print("-" * 40)
        
        goals = [
            "把杯子放到桌子上",
            "从冰箱里拿苹果",
            "打开房间的灯",
            "整理书桌上的书籍"
        ]
        
        for i, goal in enumerate(goals, 1):
            print(f"\n📝 目标{i}: {goal}")
            
            try:
                # 解释目标
                interpretation = self.interpreter.interpret_goal(goal)
                print(f"🔍 解释结果: {interpretation}")
                
                # 生成PDDL表示
                pddl_rep = self.interpreter.generate_pddl_representation(goal)
                print(f"📋 PDDL表示: {pddl_rep}")
                
            except Exception as e:
                print(f"❌ 解释失败: {e}")
    
    def demo_feedback_learning(self):
        """演示反馈学习功能"""
        print("\n🔄 演示2: 反馈学习机制")
        print("-" * 40)
        
        goal = "把红色的书放到书架上"
        print(f"📝 目标: {goal}")
        
        # 初始解释
        try:
            initial_interpretation = self.interpreter.interpret_goal(goal)
            print(f"🔍 初始解释: {initial_interpretation}")
            
            # 模拟用户反馈
            feedback_examples = [
                FeedbackRecord(
                    goal=goal,
                    user_feedback="应该强调'红色'这个属性",
                    corrected_predicate="is_red(book)",
                    confidence=0.9
                ),
                FeedbackRecord(
                    goal=goal,
                    user_feedback="动作应该是'放置'而不是'移动'",
                    corrected_predicate="place_on(book, bookshelf)",
                    confidence=0.85
                )
            ]
            
            # 学习反馈
            for feedback in feedback_examples:
                learned_predicate = self.learner.learn_from_feedback(feedback)
                print(f"📚 学到谓词: {learned_predicate}")
            
            # 更新后的解释
            updated_interpretation = self.interpreter.interpret_goal(goal)
            print(f"✨ 更新后解释: {updated_interpretation}")
            
        except Exception as e:
            print(f"❌ 反馈学习失败: {e}")
    
    def demo_predicate_evolution(self):
        """演示谓词演化功能"""
        print("\n🧬 演示3: 谓词演化")
        print("-" * 40)
        
        try:
            # 创建初始谓词
            initial_predicates = [
                SymbolicPredicate("on", ["obj1", "obj2"], "obj1在obj2上"),
                SymbolicPredicate("holding", ["agent", "obj"], "agent拿着obj"),
                SymbolicPredicate("at", ["agent", "location"], "agent在location")
            ]
            
            print("📋 初始谓词集合:")
            for pred in initial_predicates:
                print(f"   - {pred}")
            
            # 模拟演化过程
            evolution_steps = [
                ("添加颜色属性", "is_red", ["obj"], "obj是红色的"),
                ("添加容器关系", "inside", ["obj", "container"], "obj在container内"),
                ("添加状态变化", "is_open", ["container"], "container是打开的")
            ]
            
            evolved_predicates = initial_predicates.copy()
            
            for step_name, name, args, description in evolution_steps:
                print(f"\n🔄 {step_name}:")
                new_predicate = SymbolicPredicate(name, args, description)
                evolved_predicates.append(new_predicate)
                print(f"   + {new_predicate}")
            
            print(f"\n📊 最终谓词数量: {len(evolved_predicates)}")
            
        except Exception as e:
            print(f"❌ 谓词演化失败: {e}")
    
    def demo_pddl_domain_generation(self):
        """演示PDDL域生成功能"""
        print("\n🏗️ 演示4: PDDL域生成")
        print("-" * 40)
        
        try:
            # 定义域信息
            domain_info = {
                'name': 'home_robot_domain',
                'types': ['robot', 'object', 'location', 'container'],
                'predicates': [
                    ('at', ['robot', 'location']),
                    ('holding', ['robot', 'object']),
                    ('on', ['object', 'surface']),
                    ('inside', ['object', 'container']),
                    ('is_red', ['object']),
                    ('is_open', ['container'])
                ],
                'actions': [
                    {
                        'name': 'pickup',
                        'parameters': ['?r - robot', '?o - object', '?l - location'],
                        'precondition': '(at ?r ?l) (on ?o ?l)',
                        'effect': '(holding ?r ?o) (not (on ?o ?l))'
                    },
                    {
                        'name': 'place',
                        'parameters': ['?r - robot', '?o - object', '?s - surface'],
                        'precondition': '(holding ?r ?o)',
                        'effect': '(on ?o ?s) (not (holding ?r ?o))'
                    }
                ]
            }
            
            # 生成PDDL域
            pddl_domain = self.domain_builder.build_domain(domain_info)
            print("📋 生成的PDDL域:")
            print(pddl_domain)
            
            # 验证PDDL语法
            is_valid = self.domain_builder.validate_domain(pddl_domain)
            print(f"✅ PDDL语法验证: {'通过' if is_valid else '失败'}")
            
        except Exception as e:
            print(f"❌ PDDL域生成失败: {e}")
    
    def demo_statistics_tracking(self):
        """演示统计跟踪功能"""
        print("\n📊 演示5: 统计跟踪")
        print("-" * 40)
        
        try:
            # 模拟一系列解释任务
            test_goals = [
                "拿起杯子",
                "打开门", 
                "走到厨房",
                "放下书",
                "关闭窗户"
            ]
            
            print("🔄 执行解释任务并收集统计信息...")
            
            for goal in test_goals:
                try:
                    interpretation = self.interpreter.interpret_goal(goal)
                    self.interpreter.update_statistics(goal, interpretation, success=True)
                    print(f"✅ {goal}: 解释成功")
                except Exception as e:
                    self.interpreter.update_statistics(goal, None, success=False)
                    print(f"❌ {goal}: 解释失败 - {e}")
            
            # 获取统计信息
            stats = self.interpreter.get_statistics()
            print(f"\n📊 统计信息:")
            print(f"   总任务数: {stats['total_tasks']}")
            print(f"   成功任务数: {stats['successful_tasks']}")
            print(f"   成功率: {stats['success_rate']:.2%}")
            print(f"   平均解释时间: {stats['avg_interpretation_time']:.3f}s")
            
        except Exception as e:
            print(f"❌ 统计跟踪失败: {e}")
    
    def demo_save_load_functionality(self):
        """演示保存和加载功能"""
        print("\n💾 演示6: 保存和加载功能")
        print("-" * 40)
        
        try:
            # 保存当前状态
            save_path = "interpretable_state.json"
            self.interpreter.save_state(save_path)
            print(f"💾 状态已保存到: {save_path}")
            
            # 创建新的解释器并加载状态
            new_interpreter = InterpretableGoalInterpreter()
            new_interpreter.load_state(save_path)
            print("✅ 状态加载成功")
            
            # 验证加载的状态
            test_goal = "测试目标"
            original_result = self.interpreter.interpret_goal(test_goal)
            loaded_result = new_interpreter.interpret_goal(test_goal)
            
            print(f"🔍 原始解释器结果: {original_result}")
            print(f"🔍 加载解释器结果: {loaded_result}")
            
            # 清理临时文件
            if os.path.exists(save_path):
                os.remove(save_path)
                print(f"🗑️ 临时文件已清理: {save_path}")
            
        except Exception as e:
            print(f"❌ 保存/加载功能失败: {e}")
    
    def run_all_demos(self):
        """运行所有演示"""
        print("🚀 开始InterPreT完整演示")
        print("=" * 60)
        
        if not self.setup_demo():
            print("❌ 演示环境初始化失败")
            return False
        
        demos = [
            self.demo_basic_interpretation,
            self.demo_feedback_learning,
            self.demo_predicate_evolution,
            self.demo_pddl_domain_generation,
            self.demo_statistics_tracking,
            self.demo_save_load_functionality
        ]
        
        successful_demos = 0
        
        for demo_func in demos:
            try:
                demo_func()
                successful_demos += 1
            except Exception as e:
                print(f"❌ 演示失败: {e}")
        
        print("\n" + "=" * 60)
        print(f"🎉 演示完成！成功运行 {successful_demos}/{len(demos)} 个演示")
        
        if successful_demos == len(demos):
            print("🌟 所有InterPreT功能演示成功！")
        else:
            print("⚠️ 部分演示失败，请检查错误信息")
        
        return successful_demos == len(demos)

def main():
    """主函数"""
    print("🎯 InterPreT可解释目标解释器演示")
    print("=" * 50)
    
    demo = InterPreTDemo()
    success = demo.run_all_demos()
    
    if success:
        print("\n🎊 InterPreT演示全部成功！")
        print("🚀 您可以开始使用InterPreT进行目标解释开发了")
    else:
        print("\n⚠️ 部分演示失败")
        print("🔧 请检查错误信息并修复相关问题")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())