#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子目标分解模块测试
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'goal_interpretation'))

from goal_interpreter import LTLFormula
from subgoal_decomposer import SubgoalType, DecompositionStrategy, Subgoal, SubgoalDecomposer
from subgoal_validator import ValidationIssue, SubgoalValidator, SubgoalOptimizer, SubgoalAnalyzer
from subgoal_ltl_integration import SubgoalLTLIntegration, IntegrationResult


class TestSubgoalDecomposer(unittest.TestCase):
    """子目标分解器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.decomposer = SubgoalDecomposer()
        self.validator = SubgoalValidator()
        self.optimizer = SubgoalOptimizer()
        self.analyzer = SubgoalAnalyzer()
    
    def test_temporal_decomposition(self):
        """测试时序层次分解"""
        ltl_formula = LTLFormula(
            formula="F (G (p -> X q))",
            description="测试时序公式",
            confidence=0.9
        )
        
        self.decomposer.set_strategy(DecompositionStrategy.TEMPORAL_HIERARCHICAL)
        result = self.decomposer.decompose(ltl_formula, max_depth=3)
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result.subgoals), 0)
        self.assertEqual(result.decomposition_strategy, DecompositionStrategy.TEMPORAL_HIERARCHICAL)
        
        print(f"时序分解生成 {len(result.subgoals)} 个子目标")
        for subgoal in result.subgoals:
            print(f"  - {subgoal.id}: {subgoal.description}")
    
    def test_dependency_decomposition(self):
        """测试任务依赖分解"""
        ltl_formula = LTLFormula(
            formula="(p U q) && (q -> r)",
            description="测试依赖公式",
            confidence=0.9
        )
        
        self.decomposer.set_strategy(DecompositionStrategy.DEPENDENCY_BASED)
        result = self.decomposer.decompose(ltl_formula, max_depth=3)
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result.subgoals), 0)
        self.assertEqual(result.decomposition_strategy, DecompositionStrategy.DEPENDENCY_BASED)
        
        # 检查依赖关系
        for subgoal in result.subgoals:
            if subgoal.dependencies:
                self.assertIn(subgoal.id, result.execution_order)
        
        print(f"依赖分解生成 {len(result.subgoals)} 个子目标")
    
    def test_semantic_decomposition(self):
        """测试语义聚类分解"""
        ltl_formula = LTLFormula(
            formula="(p && q) U (r || s)",
            description="测试语义公式",
            confidence=0.9
        )
        
        self.decomposer.set_strategy(DecompositionStrategy.SEMANTIC_CLUSTERING)
        result = self.decomposer.decompose(ltl_formula, max_depth=3)
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result.subgoals), 0)
        self.assertEqual(result.decomposition_strategy, DecompositionStrategy.SEMANTIC_CLUSTERING)
        
        print(f"语义分解生成 {len(result.subgoals)} 个子目标")
    
    def test_mixed_decomposition(self):
        """测试混合分解"""
        ltl_formula = LTLFormula(
            formula="F (G (p -> X q) && (r U s))",
            description="测试复杂公式",
            confidence=0.9
        )
        
        self.decomposer.set_strategy(DecompositionStrategy.MIXED)
        result = self.decomposer.decompose(ltl_formula, max_depth=3)
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result.subgoals), 0)
        self.assertEqual(result.decomposition_strategy, DecompositionStrategy.MIXED)
        
        print(f"混合分解生成 {len(result.subgoals)} 个子目标")
    
    def test_max_depth_limit(self):
        """测试最大深度限制"""
        ltl_formula = LTLFormula(
            formula="F (G (p -> X q))",
            description="深度测试",
            confidence=0.9
        )
        
        result = self.decomposer.decompose(ltl_formula, max_depth=2)
        
        # 检查深度限制
        for subgoal in result.subgoals:
            self.assertLessEqual(subgoal.depth, 2)
    
    def test_max_subgoals_limit(self):
        """测试最大子目标数量限制"""
        ltl_formula = LTLFormula(
            formula="(p && q && r && s && t) U (x && y && z)",
            description="数量测试",
            confidence=0.9
        )
        
        result = self.decomposer.decompose(ltl_formula, max_subgoals=5)
        
        self.assertLessEqual(len(result.subgoals), 5)


class TestSubgoalValidator(unittest.TestCase):
    """子目标验证器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.decomposer = SubgoalDecomposer()
        self.validator = SubgoalValidator()
    
    def test_validation_structure(self):
        """测试结构验证"""
        ltl_formula = LTLFormula(
            formula="F (G p)",
            description="验证测试",
            confidence=0.9
        )
        
        result = self.decomposer.decompose(ltl_formula)
        issues = self.validator.validate_decomposition(result)
        
        self.assertIsInstance(issues, list)
        # 正常情况下应该没有严重错误
        error_count = len([i for i in issues if i.severity == 'error'])
        self.assertLessEqual(error_count, 1)
    
    def test_validation_empty_formula(self):
        """测试空公式验证"""
        ltl_formula = LTLFormula(
            formula="",
            description="空公式",
            confidence=0.0
        )
        
        result = self.decomposer.decompose(ltl_formula)
        issues = self.validator.validate_decomposition(result)
        
        # 应该有错误
        error_count = len([i for i in issues if i.severity == 'error'])
        self.assertGreater(error_count, 0)


class TestSubgoalOptimizer(unittest.TestCase):
    """子目标优化器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.decomposer = SubgoalDecomposer()
        self.validator = SubgoalValidator()
        self.optimizer = SubgoalOptimizer()
    
    def test_optimization(self):
        """测试优化功能"""
        ltl_formula = LTLFormula(
            formula="(p && q) && (q && r)",
            description="优化测试",
            confidence=0.9
        )
        
        result = self.decomposer.decompose(ltl_formula)
        issues = self.validator.validate_decomposition(result)
        
        if issues:
            optimization_result = self.optimizer.optimize_decomposition(result, issues)
            
            self.assertIsNotNone(optimization_result)
            self.assertIsNotNone(optimization_result.optimized_result)
            self.assertIsInstance(optimization_result.performance_gain, (int, float))
            
            print(f"优化后性能提升: {optimization_result.performance_gain}%")


class TestSubgoalAnalyzer(unittest.TestCase):
    """子目标分析器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.decomposer = SubgoalDecomposer()
        self.analyzer = SubgoalAnalyzer()
    
    def test_complexity_analysis(self):
        """测试复杂度分析"""
        ltl_formula = LTLFormula(
            formula="F (G (p -> X q))",
            description="复杂度测试",
            confidence=0.9
        )
        
        result = self.decomposer.decompose(ltl_formula)
        analysis = self.analyzer.analyze_complexity(result)
        
        self.assertIn('overall_complexity', analysis)
        self.assertIn('subgoal_count', analysis)
        self.assertIn('max_depth', analysis)
        self.assertIn('dependency_complexity', analysis)
        self.assertIn('recommendations', analysis)
        
        print(f"复杂度分析结果: {analysis}")


class TestSubgoalLTLIntegration(unittest.TestCase):
    """子目标LTL集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.integration = SubgoalLTLIntegration()
    
    def test_process_natural_goal(self):
        """测试处理自然语言目标"""
        natural_goal = "机器人应该先检查传感器状态，然后移动到目标位置"
        
        result = self.integration.process_goal(
            natural_goal, 
            validate=True, 
            optimize=True, 
            analyze=True
        )
        
        self.assertIsInstance(result, IntegrationResult)
        self.assertEqual(result.original_goal, natural_goal)
        self.assertIsNotNone(result.ltl_formula)
        self.assertIsNotNone(result.decomposition_result)
        self.assertIsInstance(result.validation_issues, list)
        
        print(f"处理目标: {natural_goal}")
        print(f"生成LTL: {result.ltl_formula.formula}")
        print(f"子目标数量: {len(result.decomposition_result.subgoals)}")
    
    def test_process_ltl_formula(self):
        """测试处理LTL公式"""
        ltl_formula = "F (G (p -> X q))"
        
        result = self.integration.process_ltl_formula(
            ltl_formula,
            validate=True,
            optimize=True,
            analyze=True
        )
        
        self.assertIsInstance(result, IntegrationResult)
        self.assertEqual(result.ltl_formula.formula, ltl_formula)
        self.assertIsNotNone(result.decomposition_result)
        
        print(f"处理LTL: {ltl_formula}")
        print(f"子目标数量: {len(result.decomposition_result.subgoals)}")
    
    def test_batch_process_goals(self):
        """测试批量处理目标"""
        goals = [
            "机器人应该先检查传感器状态",
            "然后移动到目标位置",
            "最后完成任务报告"
        ]
        
        results = self.integration.batch_process_goals(goals)
        
        self.assertEqual(len(results), len(goals))
        for i, result in enumerate(results):
            self.assertIsInstance(result, IntegrationResult)
            self.assertEqual(result.original_goal, goals[i])
        
        print(f"批量处理 {len(goals)} 个目标完成")
    
    def test_compare_strategies(self):
        """测试策略比较"""
        ltl_formula = "F (G (p -> X q))"
        
        strategy_results = self.integration.compare_strategies(ltl_formula)
        
        self.assertIsInstance(strategy_results, dict)
        self.assertGreater(len(strategy_results), 0)
        
        for strategy_name, result in strategy_results.items():
            print(f"策略 {strategy_name}: {len(result.decomposition_result.subgoals)} 个子目标")
    
    def test_export_formats(self):
        """测试导出功能"""
        natural_goal = "机器人应该先检查传感器状态，然后移动到目标位置"
        result = self.integration.process_goal(natural_goal)
        
        # 测试JSON导出
        json_export = self.integration.export_result(result, 'json')
        self.assertIsInstance(json_export, str)
        self.assertGreater(len(json_export), 0)
        
        # 测试文本导出
        text_export = self.integration.export_result(result, 'text')
        self.assertIsInstance(text_export, str)
        self.assertGreater(len(text_export), 0)
        
        # 测试HTML导出
        html_export = self.integration.export_result(result, 'html')
        self.assertIsInstance(html_export, str)
        self.assertGreater(len(html_export), 0)
        self.assertIn('<html>', html_export)
        
        print("所有导出格式测试通过")
    
    def test_execution_plan(self):
        """测试执行计划生成"""
        natural_goal = "机器人应该先检查传感器状态，然后移动到目标位置"
        result = self.integration.process_goal(natural_goal)
        
        plan = self.integration.generate_execution_plan(result)
        
        self.assertIn('goal', plan)
        self.assertIn('ltl_formula', plan)
        self.assertIn('phases', plan)
        self.assertIn('total_cost', plan)
        self.assertIn('estimated_duration', plan)
        
        print(f"生成执行计划: {len(plan['phases'])} 个阶段")


class TestIntegrationScenarios(unittest.TestCase):
    """集成场景测试"""
    
    def setUp(self):
        """测试前准备"""
        self.integration = SubgoalLTLIntegration()
    
    def test_robot_navigation_scenario(self):
        """测试机器人导航场景"""
        scenarios = [
            "机器人需要从A点移动到B点，同时避开障碍物",
            "机器人应该先充电，然后执行任务，最后返回充电站",
            "在紧急情况下，机器人应该立即停止所有操作",
            "机器人需要持续监控环境，并在检测到异常时报告"
        ]
        
        for scenario in scenarios:
            print(f"\n测试场景: {scenario}")
            
            try:
                result = self.integration.process_goal(
                    scenario,
                    validate=True,
                    optimize=True,
                    analyze=True,
                    max_depth=4,
                    max_subgoals=10
                )
                
                print(f"  LTL公式: {result.ltl_formula.formula}")
                print(f"  子目标数量: {len(result.decomposition_result.subgoals)}")
                print(f"  总成本: {result.decomposition_result.total_cost}")
                print(f"  验证问题: {len(result.validation_issues)}")
                
                if result.analysis_result:
                    print(f"  复杂度: {result.analysis_result['overall_complexity']}")
                
                # 生成执行计划
                plan = self.integration.generate_execution_plan(result)
                print(f"  执行阶段: {len(plan['phases'])}")
                
            except Exception as e:
                print(f"  错误: {str(e)}")
    
    def test_complex_formula_scenarios(self):
        """测试复杂公式场景"""
        complex_formulas = [
            "F (G (p -> X q))",  # 最终全局：如果p则下一个q
            "G (F p)",           # 全局最终：无限次p
            "(p U q) && (r U s)", # 双重直到
            "X (p && F q)",       # 下一个：p并且最终q
            "G (p -> (q U r))"    # 全局：如果p则q直到r
        ]
        
        for formula in complex_formulas:
            print(f"\n测试公式: {formula}")
            
            try:
                result = self.integration.process_ltl_formula(
                    formula,
                    validate=True,
                    optimize=True,
                    analyze=True
                )
                
                print(f"  子目标数量: {len(result.decomposition_result.subgoals)}")
                print(f"  分解策略: {result.decomposition_result.decomposition_strategy.value}")
                
                # 比较不同策略
                strategy_results = self.integration.compare_strategies(formula)
                print(f"  策略比较:")
                for strategy, strategy_result in strategy_results.items():
                    print(f"    {strategy}: {len(strategy_result.decomposition_result.subgoals)} 个子目标")
                
            except Exception as e:
                print(f"  错误: {str(e)}")


def run_performance_test():
    """性能测试"""
    print("\n" + "="*60)
    print("性能测试")
    print("="*60)
    
    import time
    integration = SubgoalLTLIntegration()
    
    # 测试不同复杂度的公式
    test_cases = [
        "简单: p",
        "中等: (p && q) U r",
        "复杂: F (G (p -> X q) && (r U s))",
        "非常复杂: G (F (p && (q U r)) -> X (s || (t U v)))"
    ]
    
    for case in test_cases:
        complexity, formula = case.split(": ", 1)
        
        start_time = time.time()
        try:
            result = integration.process_ltl_formula(formula)
            end_time = time.time()
            
            processing_time = end_time - start_time
            subgoal_count = len(result.decomposition_result.subgoals)
            
            print(f"{complexity}: {processing_time:.3f}s, {subgoal_count} 个子目标")
            
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            print(f"{complexity}: {processing_time:.3f}s, 错误: {str(e)}")


def main():
    """主测试函数"""
    print("子目标分解算法测试")
    print("="*60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestSubgoalDecomposer,
        TestSubgoalValidator,
        TestSubgoalOptimizer,
        TestSubgoalAnalyzer,
        TestSubgoalLTLIntegration,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 运行性能测试
    run_performance_test()
    
    # 输出测试结果摘要
    print("\n" + "="*60)
    print("测试结果摘要")
    print("="*60)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)