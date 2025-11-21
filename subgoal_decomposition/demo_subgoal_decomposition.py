#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子目标分解算法演示
展示各种功能和使用场景
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'goal_interpretation'))

from goal_interpreter import LTLFormula
from subgoal_decomposer import DecompositionStrategy, SubgoalType
from subgoal_validator import ValidationIssue
from subgoal_ltl_integration import SubgoalLTLIntegration

from subgoal_ltl_integration import SubgoalLTLIntegration
from subgoal_decomposer import DecompositionStrategy


def demo_basic_usage():
    """基本使用演示"""
    print("="*60)
    print("基本使用演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    # 处理自然语言目标
    natural_goal = "机器人应该先检查传感器状态，然后移动到目标位置"
    print(f"自然语言目标: {natural_goal}")
    
    result = integration.process_goal(
        natural_goal,
        validate=True,
        optimize=True,
        analyze=True
    )
    
    print(f"\n生成的LTL公式: {result.ltl_formula.formula}")
    print(f"置信度: {result.ltl_formula.confidence}")
    print(f"子目标数量: {len(result.decomposition_result.subgoals)}")
    print(f"总成本: {result.decomposition_result.total_cost}")
    print(f"分解策略: {result.decomposition_result.decomposition_strategy.value}")
    
    print(f"\n子目标详情:")
    for i, subgoal in enumerate(result.decomposition_result.subgoals):
        print(f"  {i+1}. {subgoal.id}: {subgoal.description}")
        print(f"     LTL: {subgoal.ltl_formula}")
        print(f"     类型: {subgoal.subgoal_type.value}")
        print(f"     成本: {subgoal.estimated_cost}")
        if subgoal.dependencies:
            print(f"     依赖: {', '.join(subgoal.dependencies)}")
        print()


def demo_strategies_comparison():
    """分解策略比较演示"""
    print("="*60)
    print("分解策略比较演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    ltl_formula = "F (G (p -> X q) && (r U s))"
    print(f"测试LTL公式: {ltl_formula}")
    
    # 比较所有策略
    strategy_results = integration.compare_strategies(ltl_formula)
    
    print(f"\n各策略分解结果:")
    for strategy_name, result in strategy_results.items():
        print(f"\n{strategy_name} 策略:")
        print(f"  子目标数量: {len(result.decomposition_result.subgoals)}")
        print(f"  总成本: {result.decomposition_result.total_cost}")
        print(f"  验证问题: {len(result.validation_issues)}")
        
        if result.analysis_result:
            print(f"  复杂度: {result.analysis_result['overall_complexity']}")


def demo_robot_scenarios():
    """机器人场景演示"""
    print("="*60)
    print("机器人场景演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    scenarios = [
        "机器人需要从A点移动到B点，同时避开障碍物",
        "机器人应该先充电，然后执行任务，最后返回充电站",
        "在紧急情况下，机器人应该立即停止所有操作",
        "机器人需要持续监控环境，并在检测到异常时报告"
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景 {i}: {scenario}")
        
        try:
            result = integration.process_goal(
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
            
            if result.validation_issues:
                error_count = len([issue for issue in result.validation_issues if issue.severity == 'error'])
                warning_count = len([issue for issue in result.validation_issues if issue.severity == 'warning'])
                print(f"  验证问题: {error_count} 个错误, {warning_count} 个警告")
            
            if result.analysis_result:
                print(f"  复杂度: {result.analysis_result['overall_complexity']}")
            
            # 生成执行计划
            plan = integration.generate_execution_plan(result)
            print(f"  执行阶段: {len(plan['phases'])}")
            print(f"  预计时间: {plan['estimated_duration']} 分钟")
            
        except Exception as e:
            print(f"  错误: {str(e)}")


def demo_complex_formulas():
    """复杂公式演示"""
    print("="*60)
    print("复杂公式演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    complex_formulas = [
        ("简单", "p"),
        ("中等", "(p && q) U r"),
        ("复杂", "F (G (p -> X q) && (r U s))"),
        ("非常复杂", "G (F (p && (q U r)) -> X (s || (t U v)))")
    ]
    
    for complexity, formula in complex_formulas:
        print(f"\n{complexity}公式: {formula}")
        
        try:
            result = integration.process_ltl_formula(
                formula,
                validate=True,
                optimize=True,
                analyze=True
            )
            
            print(f"  分解策略: {result.decomposition_result.decomposition_strategy.value}")
            print(f"  子目标数量: {len(result.decomposition_result.subgoals)}")
            print(f"  最大深度: {max(sg.depth for sg in result.decomposition_result.subgoals)}")
            
            # 统计子目标类型
            type_counts = {}
            for subgoal in result.decomposition_result.subgoals:
                type_name = subgoal.subgoal_type.value
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            print(f"  子目标类型分布: {type_counts}")
            
        except Exception as e:
            print(f"  错误: {str(e)}")


def demo_batch_processing():
    """批量处理演示"""
    print("="*60)
    print("批量处理演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    goals = [
        "检查传感器状态",
        "移动到目标位置",
        "执行任务操作",
        "生成状态报告",
        "返回起始位置"
    ]
    
    print(f"批量处理 {len(goals)} 个目标:")
    for i, goal in enumerate(goals, 1):
        print(f"  {i}. {goal}")
    
    results = integration.batch_process_goals(goals)
    
    print(f"\n处理结果:")
    successful = 0
    total_subgoals = 0
    total_cost = 0
    
    for i, result in enumerate(results, 1):
        if not result.metadata.get('error'):
            successful += 1
            total_subgoals += len(result.decomposition_result.subgoals)
            total_cost += result.decomposition_result.total_cost
            print(f"  目标 {i}: ✓ {len(result.decomposition_result.subgoals)} 个子目标")
        else:
            print(f"  目标 {i}: ✗ {result.metadata.get('error')}")
    
    print(f"\n统计:")
    print(f"  成功: {successful}/{len(goals)}")
    print(f"  总子目标数: {total_subgoals}")
    print(f"  总成本: {total_cost:.2f}")
    print(f"  平均子目标数: {total_subgoals/successful:.1f}" if successful > 0 else "  平均子目标数: 0")


def demo_export_functions():
    """导出功能演示"""
    print("="*60)
    print("导出功能演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    goal = "机器人应该先检查传感器状态，然后移动到目标位置，最后完成任务报告"
    result = integration.process_goal(goal)
    
    # 导出为JSON
    json_export = integration.export_result(result, 'json')
    print(f"JSON导出长度: {len(json_export)} 字符")
    
    # 导出为文本
    text_export = integration.export_result(result, 'text')
    print(f"文本导出长度: {len(text_export)} 字符")
    print("文本导出预览:")
    print(text_export[:500] + "..." if len(text_export) > 500 else text_export)
    
    # 导出为HTML
    html_export = integration.export_result(result, 'html')
    print(f"HTML导出长度: {len(html_export)} 字符")
    
    # 保存导出文件
    try:
        with open('demo_result.json', 'w', encoding='utf-8') as f:
            f.write(json_export)
        with open('demo_result.txt', 'w', encoding='utf-8') as f:
            f.write(text_export)
        with open('demo_result.html', 'w', encoding='utf-8') as f:
            f.write(html_export)
        print("\n导出文件已保存: demo_result.json, demo_result.txt, demo_result.html")
    except Exception as e:
        print(f"\n保存文件时出错: {str(e)}")


def demo_execution_planning():
    """执行计划演示"""
    print("="*60)
    print("执行计划演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    goal = "机器人需要完成一个复杂的巡检任务：先检查设备状态，然后沿着预定路线巡逻，发现异常时立即报告，最后返回充电站"
    result = integration.process_goal(goal, validate=True, optimize=True)
    
    plan = integration.generate_execution_plan(result)
    
    print(f"原始目标: {plan['goal']}")
    print(f"LTL公式: {plan['ltl_formula']}")
    print(f"总成本: {plan['total_cost']}")
    print(f"预计时间: {plan['estimated_duration']} 分钟")
    print(f"执行阶段数: {len(plan['phases'])}")
    
    print(f"\n执行阶段详情:")
    for i, phase in enumerate(plan['phases'], 1):
        print(f"\n阶段 {i}: {phase['name']}")
        print(f"  子目标数: {len(phase['subgoals'])}")
        print(f"  成本: {phase['cost']}")
        print(f"  预计时间: {phase['estimated_duration']} 分钟")
        
        print("  子目标列表:")
        for j, subgoal in enumerate(phase['subgoals'], 1):
            print(f"    {j}. {subgoal['id']}: {subgoal['description']}")
            print(f"       类型: {subgoal['type']}")
            print(f"       成本: {subgoal['cost']}")
            if subgoal['dependencies']:
                print(f"       依赖: {', '.join(subgoal['dependencies'])}")
    
    if plan['risks']:
        print(f"\n识别的风险:")
        for risk in plan['risks']:
            print(f"  - {risk}")
    
    if plan['recommendations']:
        print(f"\n建议:")
        for rec in plan['recommendations']:
            print(f"  - {rec}")


def demo_validation_and_optimization():
    """验证和优化演示"""
    print("="*60)
    print("验证和优化演示")
    print("="*60)
    
    integration = SubgoalLTLIntegration()
    
    # 创建一个可能有问题的复杂目标
    problematic_goal = "机器人需要同时执行多个相互冲突的任务：既要快速移动又要保持稳定，既要节省能源又要完成所有任务"
    result = integration.process_goal(problematic_goal, validate=True, optimize=True)
    
    print(f"目标: {problematic_goal}")
    print(f"LTL公式: {result.ltl_formula.formula}")
    print(f"子目标数量: {len(result.decomposition_result.subgoals)}")
    
    # 显示验证问题
    if result.validation_issues:
        print(f"\n验证问题 ({len(result.validation_issues)} 个):")
        for issue in result.validation_issues:
            print(f"  [{issue.severity.upper()}] {issue.message}")
            if issue.suggestion:
                print(f"    建议: {issue.suggestion}")
    
    # 显示优化结果
    if result.optimization_result:
        print(f"\n优化结果:")
        print(f"  性能提升: {result.optimization_result.performance_gain}%")
        print(f"  解决问题: {result.optimization_result.validation_issues_resolved}")
        print(f"  改进措施:")
        for improvement in result.optimization_result.improvements:
            print(f"    - {improvement}")
    
    # 显示复杂度分析
    if result.analysis_result:
        print(f"\n复杂度分析:")
        analysis = result.analysis_result
        print(f"  整体复杂度: {analysis['overall_complexity']}")
        print(f"  子目标数量: {analysis['subgoal_count']}")
        print(f"  最大深度: {analysis['max_depth']}")
        print(f"  依赖复杂度: {analysis['dependency_complexity']:.2f}")
        
        if analysis['recommendations']:
            print(f"  建议:")
            for rec in analysis['recommendations']:
                print(f"    - {rec}")


def main():
    """主演示函数"""
    print("子目标分解算法演示")
    print("本演示将展示子目标分解算法的各种功能和使用场景")
    
    demos = [
        ("基本使用", demo_basic_usage),
        ("策略比较", demo_strategies_comparison),
        ("机器人场景", demo_robot_scenarios),
        ("复杂公式", demo_complex_formulas),
        ("批量处理", demo_batch_processing),
        ("导出功能", demo_export_functions),
        ("执行计划", demo_execution_planning),
        ("验证优化", demo_validation_and_optimization)
    ]
    
    print("\n可用的演示:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\n选择演示 (输入数字，或按回车运行所有演示): ")
    choice = input().strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(demos):
        # 运行选定的演示
        name, func = demos[int(choice) - 1]
        print(f"\n运行演示: {name}")
        func()
    else:
        # 运行所有演示
        print("\n运行所有演示...")
        for name, func in demos:
            try:
                func()
                print(f"\n✓ {name} 演示完成")
                input("按回车继续...")
            except Exception as e:
                print(f"\n✗ {name} 演示失败: {str(e)}")
                input("按回车继续...")
    
    print("\n演示完成！")
    print("更多信息请参考:")
    print("- 使用指南: subgoal_decomposition_guide.md")
    print("- 测试用例: test_subgoal_decomposition.py")
    print("- 技术文档: docs/technical/技术指导文档.md")


if __name__ == "__main__":
    main()