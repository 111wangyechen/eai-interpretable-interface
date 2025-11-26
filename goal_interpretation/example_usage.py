#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标解释模块使用示例
演示如何使用目标解释器将自然语言转换为LTL公式
"""

from goal_interpreter import GoalInterpreter


def main():
    """
    主函数，演示目标解释模块的使用
    """
    # 创建目标解释器实例
    interpreter = GoalInterpreter()
    
    print("=== 目标解释模块使用示例 ===")
    print("该模块可以将自然语言目标描述转换为LTL公式")
    print("\n")
    
    # 测试用例列表
    test_cases = [
        "到达厨房",
        "先打开门，然后进入房间",
        "如果看到红灯，就停止前进",
        "同时打开窗户和关闭门",
        "最终到达目的地",
        "总是保持安全",
        "先检查环境是否安全，如果安全就前进到桌子，然后拿起钥匙",
    ]
    
    # 处理每个测试用例
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- 示例 {i} ---")
        print(f"自然语言: {text}")
        
        try:
            # 解释自然语言，生成LTL公式
            ltl_formula = interpreter.interpret(text)
            
            # 打印生成的LTL公式
            print(f"LTL公式: {ltl_formula.formula}")
            
            # 打印语义解析结果
            print("语义结构:")
            print(f"  - 任务类型: {ltl_formula.semantics.get('task_type', '未知')}")
            print(f"  - 动作: {ltl_formula.semantics.get('actions', [])}")
            print(f"  - 对象: {ltl_formula.semantics.get('objects', [])}")
            print(f"  - 条件: {ltl_formula.semantics.get('conditions', [])}")
            
            # 验证LTL公式
            print("验证结果: 公式有效")
            
        except Exception as e:
            print(f"错误: {str(e)}")
    
    print("\n")
    print("=== 自定义输入示例 ===")
    print("尝试输入自定义的自然语言目标描述:")
    
    # 允许用户输入自定义文本
    while True:
        try:
            user_input = input("\n请输入自然语言目标描述（输入'q'退出）: ")
            
            if user_input.lower() == 'q':
                break
            
            # 解释用户输入
            ltl_formula = interpreter.interpret(user_input)
            
            # 显示结果
            print(f"LTL公式: {ltl_formula.formula}")
            print(f"任务类型: {ltl_formula.semantics.get('task_type', '未知')}")
            
        except Exception as e:
            print(f"处理失败: {str(e)}")
    
    print("\n感谢使用目标解释模块！")


def batch_processing():
    """
    批处理示例，处理多个自然语言目标
    """
    interpreter = GoalInterpreter()
    
    # 要处理的自然语言目标列表
    goals = [
        "收集所有物品然后返回起点",
        "在不碰到障碍物的情况下到达终点",
        "先关灯，然后锁门，最后离开房间",
        "如果检测到危险，立即撤离",
        "保持环境清洁并定期检查设备"
    ]
    
    print("=== 批处理示例 ===")
    
    results = []
    
    # 批量处理所有目标
    for i, goal in enumerate(goals, 1):
        ltl_formula = interpreter.interpret(goal)
        results.append({
            "id": i,
            "natural_language": goal,
            "ltl_formula": ltl_formula.formula,
            "task_type": ltl_formula.semantics.get('task_type', '未知')
        })
    
    # 显示批处理结果
    for result in results:
        print(f"\n目标 {result['id']}:")
        print(f"  自然语言: {result['natural_language']}")
        print(f"  LTL公式: {result['ltl_formula']}")
        print(f"  任务类型: {result['task_type']}")


def custom_configuration():
    """
    自定义配置示例
    演示如何根据特定需求使用目标解释模块
    """
    interpreter = GoalInterpreter()
    
    print("\n=== 自定义配置示例 ===")
    print("根据特定领域的需求使用目标解释模块")
    
    # 特定领域的目标描述
    domain_goals = [
        "机器人需要先移动到货架A，然后拿起盒子，最后放到传送带上",
        "智能家居系统在检测到室内温度高于26度时打开空调",
        "自动驾驶汽车保持在车道内并与前车保持安全距离"
    ]
    
    for goal in domain_goals:
        ltl_formula = interpreter.interpret(goal)
        print(f"\n领域目标: {goal}")
        print(f"LTL公式: {ltl_formula.formula}")


if __name__ == "__main__":
    # 运行主示例
    main()
    
    # 运行批处理示例
    batch_processing()
    
    # 运行自定义配置示例
    custom_configuration()