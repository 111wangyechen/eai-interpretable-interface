#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EAI Challenge 提交脚本
整合四个模块的输出并生成最终的提交文件

该脚本将：
1. 导入所有四个模块（目标解释、子目标分解、状态转换建模、动作序列生成）
2. 处理输入的自然语言目标
3. 整合各个模块的输出
4. 生成符合比赛要求的JSON格式提交文件
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    # 导入四个核心模块
    from goal_interpretation import GoalInterpreter
    from subgoal_decomposition import SubgoalLTLIntegration
    from transition_modeling import TransitionModeler, ModelingRequest
    from action_sequencing import ActionSequencer, SequencingRequest, Action, ActionType
    print("✓ 所有四个模块导入成功")
except ImportError as e:
    print(f"✗ 模块导入失败: {e}")
    sys.exit(1)


def create_submission_file(output_data: Dict[str, Any], output_file: str) -> None:
    """
    创建提交文件
    
    Args:
        output_data: 要保存的数据
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"✓ 提交文件已生成: {output_file}")
    except Exception as e:
        print(f"✗ 保存提交文件失败: {e}")
        sys.exit(1)


def process_goal(natural_goal: str, output_dir: str = ".") -> Dict[str, Any]:
    """
    处理自然语言目标，整合四个模块的输出
    
    Args:
        natural_goal: 自然语言目标描述
        output_dir: 输出目录
    
    Returns:
        整合后的结果数据
    """
    start_time = time.time()
    submission_id = f"submission_{int(start_time * 1000)}"
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化所有模块
    print("\n" + "="*60)
    print("初始化模块...")
    print("="*60)
    
    # 1. 目标解释模块
    goal_interpreter = GoalInterpreter()
    
    # 2. 子目标分解模块
    subgoal_integration = SubgoalLTLIntegration()
    
    # 3. 状态转换建模模块
    transition_modeler = TransitionModeler()
    
    # 4. 动作序列生成模块
    action_sequencer = ActionSequencer()
    
    print("✓ 所有模块初始化完成")
    
    # 处理流程
    print("\n" + "="*60)
    print(f"处理目标: {natural_goal}")
    print("="*60)
    
    # 1. 目标解释
    print("\n步骤1: 目标解释")
    try:
        goal_result = goal_interpreter.interpret(natural_goal)
        print(f"✓ 目标解释成功")
        print(f"  LTL公式: {goal_result.formula}")
        print(f"  置信度: {goal_result.confidence}")
    except Exception as e:
        print(f"✗ 目标解释失败: {e}")
        return {
            'submission_id': submission_id,
            'status': 'failed',
            'error': f'Goal interpretation failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    # 2. 子目标分解
    print("\n步骤2: 子目标分解")
    try:
        subgoal_result = subgoal_integration.process_goal(natural_goal)
        subgoals_count = len(subgoal_result.decomposition_result.subgoals)
        print(f"✓ 子目标分解成功，生成 {subgoals_count} 个子目标")
        
        # 保存子目标分解结果
        subgoal_json = subgoal_integration.export_result(subgoal_result, 'json')
        subgoal_file = os.path.join(output_dir, f"{submission_id}_subgoals.json")
        with open(subgoal_file, 'w', encoding='utf-8') as f:
            f.write(subgoal_json)
        print(f"  子目标分解结果已保存到: {subgoal_file}")
        
    except Exception as e:
        print(f"✗ 子目标分解失败: {e}")
        return {
            'submission_id': submission_id,
            'status': 'failed',
            'error': f'Subgoal decomposition failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    # 3. 状态转换建模
    print("\n步骤3: 状态转换建模")
    try:
        # 创建示例初始状态和目标状态
        initial_state = {'at_location': 'start', 'task_completed': False}
        goal_state = {'at_location': 'target', 'task_completed': True}
        
        # 获取可用转换
        available_transitions = transition_modeler.create_sample_transitions()
        print(f"  可用转换数量: {len(available_transitions)}")
        
        # 创建建模请求
        modeling_request = ModelingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_transitions=available_transitions
        )
        
        # 执行建模
        modeling_response = transition_modeler.model_transitions(modeling_request)
        sequences_count = len(modeling_response.predicted_sequences)
        print(f"✓ 状态转换建模完成，生成 {sequences_count} 个序列")
        
        # 保存建模结果
        modeling_file = os.path.join(output_dir, f"{submission_id}_modeling.json")
        with open(modeling_file, 'w', encoding='utf-8') as f:
            json.dump(modeling_response.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"  状态转换建模结果已保存到: {modeling_file}")
        
    except Exception as e:
        print(f"✗ 状态转换建模失败: {e}")
        return {
            'submission_id': submission_id,
            'status': 'failed',
            'error': f'Transition modeling failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    # 4. 动作序列生成
    print("\n步骤4: 动作序列生成")
    try:
        # 定义测试动作
        test_actions = [
            Action(
                id="move", 
                name="MoveToLocation", 
                action_type=ActionType.NAVIGATION,
                parameters={"target": "target"},
                preconditions=["at_location_start"],
                effects=["at_location_target"]
            ),
            Action(
                id="complete_task", 
                name="CompleteTask", 
                action_type=ActionType.MANIPULATION,
                parameters={},
                preconditions=["at_location_target"],
                effects=["task_completed"]
            )
        ]
        
        # 创建序列请求
        sequencing_request = SequencingRequest(
            initial_state={"at_location_start": True, "at_location_target": False, "task_completed": False},
            goal_state={"at_location_target": True, "task_completed": True},
            available_actions=test_actions
        )
        
        # 生成动作序列
        sequencing_response = action_sequencer.generate_sequence(sequencing_request)
        
        if sequencing_response.success and sequencing_response.action_sequence:
            actions_count = len(sequencing_response.action_sequence.actions)
            print(f"✓ 动作序列生成成功，包含 {actions_count} 个动作")
            
            # 保存动作序列
            sequence_file = os.path.join(output_dir, f"{submission_id}_sequence.json")
            action_sequencer.export_sequence_to_json(sequencing_response.action_sequence, sequence_file)
            print(f"  动作序列已保存到: {sequence_file}")
        else:
            print(f"⚠️  动作序列生成失败或为空: {sequencing_response.error_message}")
            
    except Exception as e:
        print(f"✗ 动作序列生成失败: {e}")
        return {
            'submission_id': submission_id,
            'status': 'failed',
            'error': f'Action sequencing failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    # 整合所有结果
    print("\n" + "="*60)
    print("整合结果...")
    print("="*60)
    
    combined_result = {
        'submission_id': submission_id,
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'processing_time': time.time() - start_time,
        'original_goal': natural_goal,
        'goal_interpretation': {
            'ltl_formula': goal_result.formula,
            'confidence': goal_result.confidence,
            'description': goal_result.description
        },
        'subgoal_decomposition': {
            'subgoals_count': subgoals_count,
            'file_path': os.path.abspath(subgoal_file)
        },
        'transition_modeling': {
            'sequences_generated': sequences_count,
            'file_path': os.path.abspath(modeling_file)
        },
        'action_sequencing': {
            'actions_generated': actions_count if sequencing_response.success and sequencing_response.action_sequence else 0,
            'file_path': os.path.abspath(sequence_file) if sequencing_response.success and sequencing_response.action_sequence else None
        },
        'metadata': {
            'project_version': '1.0.0',
            'modules': [
                {'name': 'goal_interpretation', 'status': 'working'},
                {'name': 'subgoal_decomposition', 'status': 'working'},
                {'name': 'transition_modeling', 'status': 'working'},
                {'name': 'action_sequencing', 'status': 'working' if sequencing_response.success else 'partial'}
            ]
        }
    }
    
    print("✓ 结果整合完成")
    return combined_result


def batch_process_goals(goals_file: str, output_dir: str) -> None:
    """
    批量处理目标文件
    
    Args:
        goals_file: 包含目标列表的JSON文件
        output_dir: 输出目录
    """
    try:
        # 读取目标文件
        with open(goals_file, 'r', encoding='utf-8') as f:
            goals_data = json.load(f)
        
        goals = goals_data.get('goals', [])
        if not goals:
            print(f"✗ 目标文件中没有找到目标列表: {goals_file}")
            return
        
        print(f"✓ 已加载 {len(goals)} 个目标")
        
        # 批量处理每个目标
        batch_results = []
        for i, goal in enumerate(goals, 1):
            print(f"\n" + "="*80)
            print(f"处理目标 {i}/{len(goals)}: {goal}")
            print("="*80)
            
            result = process_goal(goal, output_dir)
            batch_results.append({
                'goal': goal,
                'result': result
            })
        
        # 生成批量报告
        batch_report = {
            'batch_id': f"batch_{int(time.time() * 1000)}",
            'timestamp': datetime.now().isoformat(),
            'total_goals': len(goals),
            'successful_processing': sum(1 for r in batch_results if r['result'].get('status') == 'success'),
            'results': batch_results
        }
        
        # 保存批量报告
        batch_file = os.path.join(output_dir, f"batch_processing_report.json")
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n" + "="*80)
        print(f"批量处理完成")
        print(f"总目标数: {len(goals)}")
        print(f"成功处理: {sum(1 for r in batch_results if r['result'].get('status') == 'success')}")
        print(f"报告文件: {batch_file}")
        print("="*80)
        
    except Exception as e:
        print(f"✗ 批量处理失败: {e}")


def create_sample_goals_file(output_file: str) -> None:
    """
    创建示例目标文件
    
    Args:
        output_file: 输出文件路径
    """
    sample_goals = {
        "goals": [
            "机器人应该先检查传感器状态，然后移动到目标位置",
            "把红色球和蓝色球都放在桌子上",
            "如果房间有光，就捡起红球；否则，先开灯，然后再捡球",
            "先打开电脑，然后查看邮件，最后关闭电脑"
        ]
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_goals, f, indent=2, ensure_ascii=False)
        print(f"✓ 示例目标文件已创建: {output_file}")
    except Exception as e:
        print(f"✗ 创建示例目标文件失败: {e}")


def main():
    """
    主函数
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='EAI Challenge 提交脚本')
    
    # 子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 单个目标处理命令
    single_parser = subparsers.add_parser('single', help='处理单个目标')
    single_parser.add_argument('--goal', '-g', type=str, required=True, help='自然语言目标描述')
    single_parser.add_argument('--output', '-o', type=str, default='submission.json', help='输出文件路径')
    single_parser.add_argument('--output-dir', '-d', type=str, default='./submission_data', help='中间结果输出目录')
    
    # 批量处理命令
    batch_parser = subparsers.add_parser('batch', help='批量处理目标')
    batch_parser.add_argument('--goals-file', '-f', type=str, required=True, help='包含目标列表的JSON文件')
    batch_parser.add_argument('--output-dir', '-d', type=str, default='./batch_submission_data', help='输出目录')
    
    # 创建示例目标文件命令
    sample_parser = subparsers.add_parser('create-sample', help='创建示例目标文件')
    sample_parser.add_argument('--output', '-o', type=str, default='sample_goals.json', help='输出文件路径')
    
    # 解析参数
    args = parser.parse_args()
    
    # 根据命令执行不同操作
    if args.command == 'single':
        # 处理单个目标
        print("EAI Challenge 单个目标处理")
        print("="*60)
        
        result = process_goal(args.goal, args.output_dir)
        create_submission_file(result, args.output)
        
    elif args.command == 'batch':
        # 批量处理目标
        print("EAI Challenge 批量目标处理")
        print("="*60)
        
        batch_process_goals(args.goals_file, args.output_dir)
        
    elif args.command == 'create-sample':
        # 创建示例目标文件
        create_sample_goals_file(args.output)
        
    else:
        # 显示帮助信息
        parser.print_help()


if __name__ == "__main__":
    print("="*80)
    print("EAI Challenge 提交脚本")
    print("Integrated Interface for Embodied Agents")
    print("="*80)
    
    try:
        main()
        print("\n✅ 脚本执行完成")
    except KeyboardInterrupt:
        print("\n❌ 脚本被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 脚本执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)