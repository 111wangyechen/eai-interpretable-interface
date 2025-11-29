#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
New Debug script for EAI Challenge Parquet Processing
This script extracts 20 records from each parquet file and processes them with detailed logging
"""

import os
import sys
import json
import time
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('new_debug_parquet_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('new_debug_script')

# Custom JSON encoder to handle non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle custom objects by converting to string representation
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        try:
            return str(obj)
        except:
            return {"type": obj.__class__.__name__, "message": "Non-serializable object"}
        return super().default(obj)

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import four core modules (integrated versions)
logger.info("Importing core modules...")
try:
    from goal_interpretation import EnhancedGoalInterpreter as GoalInterpreter, LTLFormula
    logger.info("✓ GoalInterpreter (enhanced) imported successfully")
    from subgoal_decomposition.subgoal_decomposer_integration import SubgoalDecomposerIntegration
    logger.info("✓ SubgoalDecomposerIntegration imported successfully")
    from transition_modeling.transition_modeler_integration import TransitionModelerIntegration
    logger.info("✓ TransitionModelerIntegration imported successfully")
    from action_sequencing.action_sequencer_integration import ActionSequencerIntegration
    logger.info("✓ ActionSequencerIntegration imported successfully")
    from action_sequencing.action_data import ActionType, Action
    logger.info("✓ ActionType and Action imported successfully")
    print("✓ All four integrated modules imported successfully")
except ImportError as e:
    logger.error(f"✗ Module import failed: {e}")
    print(f"✗ Module import failed: {e}")
    sys.exit(1)


def load_parquet_samples(file_path: str, num_samples: int = 20) -> List[Dict[str, Any]]:
    """
    Load sample records from parquet file
    
    Args:
        file_path: Path to parquet file
        num_samples: Number of samples to load
        
    Returns:
        List of sample records
    """
    logger.info(f"Loading {num_samples} samples from {file_path}")
    try:
        df = pd.read_parquet(file_path)
        logger.info(f"Total records in file: {len(df)}")
        
        # Convert to list of dictionaries
        records = df.head(num_samples).to_dict('records')
        logger.info(f"Loaded {len(records)} samples successfully")
        return records
    except Exception as e:
        logger.error(f"Failed to load parquet file: {e}")
        return []


def process_goal_with_debug(natural_goal: str, task_id: str, dataset: str) -> Dict[str, Any]:
    """
    Process natural language goal with detailed debugging
    
    Args:
        natural_goal: Natural language goal description
        task_id: Unique task identifier from dataset
        dataset: Name of the dataset
    
    Returns:
        Integrated result data with debug information
    """
    start_time = time.time()
    submission_id = f"{dataset}_{task_id}_{int(start_time * 1000)}"
    debug_info = {
        'submission_id': submission_id,
        'task_id': task_id,
        'dataset': dataset,
        'natural_goal': natural_goal,
        'start_time': datetime.now().isoformat(),
        'modules': {},
        'execution_times': {}
    }
    
    logger.info(f"=== Processing task {task_id} from {dataset}: {natural_goal[:50]}... ===")
    
    try:
        # Initialize all modules with integrated versions
        logger.info("Initializing integrated modules...")
        goal_interpreter = GoalInterpreter()
        subgoal_decomposer = SubgoalDecomposerIntegration()
        transition_modeler = TransitionModelerIntegration()
        action_sequencer = ActionSequencerIntegration()
        logger.info("All integrated modules initialized successfully")
        
        # ----------------- 遵循依赖关系的正确流程 -----------------
        
        # Step 1: Goal Interpretation (自然语言转形式化表示)
        logger.info("Step 1: Goal Interpretation")
        interpretation_start = time.time()
        try:
            # 调用目标解释器处理自然语言目标
            interpretation_result = goal_interpreter.interpret(natural_goal)
            
            # 安全获取LTL公式和有效性信息
            # 注意：interpret方法返回的是LTLFormula对象，它有formula属性和is_valid方法
            if isinstance(interpretation_result, dict):
                formula = interpretation_result.get('formula', '')
                ltl_formula = interpretation_result.get('ltl_formula', '')
            else:
                formula = getattr(interpretation_result, 'formula', '')
                ltl_formula = getattr(interpretation_result, 'ltl_formula', '')
            
            # 确保获取到完整的LTL公式
            final_formula = ltl_formula if ltl_formula else formula
            
            # 检查公式有效性，is_valid可能是方法或属性
            is_valid = interpretation_result.is_valid() if hasattr(interpretation_result, 'is_valid') and callable(getattr(interpretation_result, 'is_valid')) else getattr(interpretation_result, 'is_valid', True)
            
            logger.debug(f"Goal interpreted: {final_formula}, valid: {is_valid}")
            
            # 仅存储可序列化的解释结果
            debug_info['modules']['goal_interpretation'] = {
                'status': 'success',
                'type': type(interpretation_result).__name__,  # 记录结果类型
                'ltl_formula': final_formula,
                'is_valid': is_valid
            }
            debug_info['execution_times']['goal_interpretation'] = time.time() - interpretation_start
        except AttributeError as e:
            logger.error(f"Goal interpretation failed due to attribute error: {e}")
            debug_info['modules']['goal_interpretation'] = {
                'status': 'failed',
                'error': f'Attribute error: {e}'
            }
            debug_info['execution_times']['goal_interpretation'] = time.time() - interpretation_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Goal interpretation failed: {e}',
                'debug_info': debug_info
            }
        except Exception as e:
            logger.error(f"Goal interpretation failed: {e}")
            debug_info['modules']['goal_interpretation'] = {
                'status': 'failed',
                'error': str(e)
            }
            debug_info['execution_times']['goal_interpretation'] = time.time() - interpretation_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Goal interpretation failed: {e}',
                'debug_info': debug_info
            }
        
        # Step 2: Subgoal Decomposition (使用目标解释结果)
        logger.info("Step 2: Subgoal Decomposition")
        subgoal_start = time.time()
        try:
            # 使用集成版本的子目标分解方法
            logger.debug(f"Using integrated subgoal decomposition for: {natural_goal}")
            
            # 准备集成请求数据
            goal_data = {
                'goal_variables': {},
                'goal_constraints': [],
                'formula': getattr(interpretation_result, 'formula', ''),
                'ltl_formula': getattr(interpretation_result, 'ltl_formula', ''),
                'is_valid': interpretation_result.is_valid() if hasattr(interpretation_result, 'is_valid') and callable(getattr(interpretation_result, 'is_valid')) else getattr(interpretation_result, 'is_valid', True)
            }
            
            # 调用集成版本的分解方法
            subgoal_result = subgoal_decomposer.decompose_for_integration(
                goal_text=natural_goal,
                goal_data=goal_data
            )
            
            # 安全获取子目标数量和实际子目标
            if hasattr(subgoal_result, 'subgoals'):
                subgoals = subgoal_result.subgoals
            elif hasattr(subgoal_result, 'decomposition_result'):
                decomposition_result = subgoal_result.decomposition_result
                subgoals = getattr(decomposition_result, 'subgoals', []) if decomposition_result else []
            else:
                # 尝试直接获取分解结果
                subgoals = getattr(subgoal_result, 'result', []) if isinstance(subgoal_result, dict) else []
            
            subgoal_count = len(subgoals)
            
            # 处理子目标，仅保留可序列化信息
            serializable_subgoals = []
            if subgoals:
                for subgoal in subgoals:
                    try:
                        # 提取子目标的关键属性，确保获取完整信息
                        subgoal_info = {
                            'id': getattr(subgoal, 'id', f"subgoal_{len(serializable_subgoals)}"),
                            'description': getattr(subgoal, 'description', getattr(subgoal, 'natural_language', str(subgoal))),
                            'ltl_formula': getattr(subgoal, 'ltl_formula', getattr(subgoal, 'formula', '')),
                            'subgoal_type': getattr(subgoal, 'type', 'atomic').name if hasattr(getattr(subgoal, 'type', None), 'name') else 'atomic',
                            'preconditions': getattr(subgoal, 'preconditions', []),
                            'effects': getattr(subgoal, 'effects', [])
                        }
                        serializable_subgoals.append(subgoal_info)
                    except Exception as e:
                        # 如果无法序列化，保存字符串表示和错误信息
                        serializable_subgoals.append({
                            'error': str(e),
                            'raw_representation': str(subgoal)
                        })
            
            # 如果子目标数量太少，尝试使用备用方法
            if len(serializable_subgoals) < 1:
                logger.info("Trying alternative subgoal generation method")
                # 基于目标文本生成简单子目标
                serializable_subgoals = [
                    {
                        'id': "subgoal_0",
                        'description': f"完成主要任务: {natural_goal}",
                        'ltl_formula': interpretation_result.formula,
                        'subgoal_type': "atomic",
                        'preconditions': ["agent_available"],
                        'effects': ["task_completed"]
                    }
                ]
            
            logger.debug(f"Subgoal result: {len(serializable_subgoals)} subgoals generated")
            debug_info['modules']['subgoal_decomposition'] = {
                'status': 'success',
                'subgoal_count': len(serializable_subgoals),
                'subgoals': serializable_subgoals,
                'type': type(subgoal_result).__name__,
                'ltl_formula_used': ltl_formula
            }
            debug_info['execution_times']['subgoal_decomposition'] = time.time() - subgoal_start
        except AttributeError as e:
            logger.error(f"Subgoal decomposition failed due to attribute error: {e}")
            debug_info['modules']['subgoal_decomposition'] = {
                'status': 'failed',
                'error': f'Attribute error: {e}'
            }
            debug_info['execution_times']['subgoal_decomposition'] = time.time() - subgoal_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Subgoal decomposition failed: {e}',
                'debug_info': debug_info
            }
        except Exception as e:
            logger.error(f"Subgoal decomposition failed: {e}")
            debug_info['modules']['subgoal_decomposition'] = {
                'status': 'failed',
                'error': str(e)
            }
            debug_info['execution_times']['subgoal_decomposition'] = time.time() - subgoal_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Subgoal decomposition failed: {e}',
                'debug_info': debug_info
            }
        
        # Step 3: Transition Modeling (使用目标解释和子目标分解结果)
        logger.info("Step 3: Transition Modeling")
        modeling_start = time.time()
        try:
            # 从子目标分解结果中提取相关信息，构建更准确的状态
            initial_state = {
                'at_location': 'start',
                'task_completed': False,
                'objects': {},
                'environment': dataset,
                'subgoals_completed': []
            }
            
            goal_state = {
                'at_location': 'target',
                'task_completed': True,
                'objects': {},
                'environment': dataset,
                'subgoals_completed': [subgoal['id'] for subgoal in serializable_subgoals]
            }
            
            # 从子目标中提取可用的状态变量和转换
            available_transitions = []
            for subgoal in serializable_subgoals:
                if 'preconditions' in subgoal and 'effects' in subgoal:
                    available_transitions.append({
                        'subgoal_id': subgoal['id'],
                        'preconditions': subgoal['preconditions'],
                        'effects': subgoal['effects']
                    })
            
            # 使用集成版本的转换建模方法
            logger.debug(f"Using integrated transition modeling for goal: {natural_goal}")
            
            # 准备集成请求数据
            subgoal_data = {
                'subgoals': serializable_subgoals,
                'original_goal': natural_goal,
                'goal_data': goal_data
            }
            
            # 调用集成版本的转换建模方法
            transition_result = transition_modeler.model_transitions_for_integration(
                goal_text=natural_goal,
                subgoal_data=subgoal_data,
                context={
                    "dataset": dataset,
                    "task_id": task_id,
                    "initial_state": initial_state,
                    "goal_state": goal_state,
                    "available_transitions": available_transitions
                }
            )
            
            # 记录转换模型的结果，包括可用动作
            transition_info = {
                'status': 'success',
                'type': type(transition_result).__name__
            }
            
            # 提取转换模型生成的可用动作
            if hasattr(transition_result, 'available_actions'):
                transition_info['available_actions_count'] = len(transition_result.available_actions)
            elif hasattr(transition_result, 'transitions'):
                transition_info['transitions_count'] = len(transition_result.transitions)
            
            logger.debug(f"Transition modeling completed successfully: {transition_info}")
            
            debug_info['modules']['transition_modeling'] = transition_info
            debug_info['execution_times']['transition_modeling'] = time.time() - modeling_start
        except AttributeError as e:
            logger.error(f"Transition modeling failed due to attribute error: {e}")
            debug_info['modules']['transition_modeling'] = {
                'status': 'failed',
                'error': f'Attribute error: {e}'
            }
            debug_info['execution_times']['transition_modeling'] = time.time() - modeling_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Transition modeling failed: {e}',
                'debug_info': debug_info
            }
        except Exception as e:
            logger.error(f"Transition modeling failed: {e}")
            debug_info['modules']['transition_modeling'] = {
                'status': 'failed',
                'error': str(e)
            }
            debug_info['execution_times']['transition_modeling'] = time.time() - modeling_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Transition modeling failed: {e}',
                'debug_info': debug_info
            }
        
        # Step 4: Action Sequencing (使用前序所有模块的结果)
        logger.info("Step 4: Action Sequencing")
        sequencing_start = time.time()
        try:
            # 从转换模型结果中获取可用动作，或使用基于任务上下文生成的动作
            available_actions = []
            
            # 优先使用转换模型提供的动作
            if hasattr(transition_result, 'available_actions') and transition_result.available_actions:
                available_actions = transition_result.available_actions
                logger.debug(f"Using {len(available_actions)} actions from transition model")
            else:
                # 根据任务类型和子目标动态生成相关动作
                logger.debug("No actions from transition model, generating task-specific actions based on subgoals")
                
                # 基于目标文本和子目标动态生成动作
                action_templates = []
                
                # 为每个子目标生成对应的动作
                for i, subgoal in enumerate(serializable_subgoals):
                    # 导航动作
                    action_templates.append({
                        'id': f"navigate_{i}",
                        'name': "NavigateToLocation",
                        'action_type': ActionType.NAVIGATION,
                        'parameters': {"target": "location_for_subgoal"},
                        'preconditions': ["agent_available", "path_clear"] + subgoal.get('preconditions', []),
                        'effects': ["agent_position_changed", f"subgoal_{subgoal['id']}_reachable"]
                    })
                    
                    # 执行子目标的动作
                    action_templates.append({
                        'id': f"execute_{i}",
                        'name': "ExecuteSubgoal",
                        'action_type': ActionType.MANIPULATION,
                        'parameters': {"subgoal_id": subgoal['id']},
                        'preconditions': [f"subgoal_{subgoal['id']}_reachable"] + subgoal.get('preconditions', []),
                        'effects': subgoal.get('effects', []) + [f"subgoal_{subgoal['id']}_completed"]
                    })
                
                # 最终完成任务的动作
                action_templates.append({
                    'id': "final_complete",
                    'name': "CompleteTask",
                    'action_type': ActionType.MANIPULATION,
                    'parameters': {},
                    'preconditions': [f"subgoal_{subgoal['id']}_completed" for subgoal in serializable_subgoals],
                    'effects': ["task_completed"]
                })
                
                # 将模板转换为Action对象
                available_actions = [Action(**template) for template in action_templates]
                logger.debug(f"Generated {len(available_actions)} actions based on subgoals")
            
            # 使用集成版本的动作排序方法
            logger.debug(f"Using integrated action sequencing for goal: {natural_goal}")
            
            # 准备集成请求数据
            subgoal_data = {
                'subgoals': serializable_subgoals,
                'original_goal': natural_goal,
                'goal_data': goal_data
            }
            
            transition_data = {
                'initial_state': initial_state,
                'goal_state': goal_state,
                'available_actions': available_actions
            }
            
            # 调用集成版本的动作排序方法
            action_result = action_sequencer.sequence_actions_for_integration(
                goal_text=natural_goal,
                subgoal_data=subgoal_data,
                transition_data=transition_data
            )
            
            # 安全检查action_result状态
            is_success = getattr(action_result, 'success', False)
            
            # 提取动作序列的详细信息
            action_sequence_info = {
                'status': 'success' if is_success else 'failed',
                'type': type(action_result).__name__
            }
            
            # 如果有动作序列，提取可序列化信息
            if hasattr(action_result, 'action_sequence') and action_result.action_sequence:
                try:
                    serializable_actions = []
                    for action in action_result.action_sequence:
                        serializable_actions.append({
                            'id': getattr(action, 'id', 'unknown'),
                            'name': getattr(action, 'name', 'unknown'),
                            'action_type': getattr(action, 'action_type', 'unknown'),
                            'parameters': getattr(action, 'parameters', {}),
                            'preconditions': getattr(action, 'preconditions', []),
                            'effects': getattr(action, 'effects', [])
                        })
                    action_sequence_info['actions'] = serializable_actions
                    action_sequence_info['action_count'] = len(serializable_actions)
                except Exception as e:
                    action_sequence_info['action_extraction_error'] = str(e)
            
            # 记录额外的结果信息
            if hasattr(action_result, 'execution_plan'):
                action_sequence_info['execution_plan'] = str(action_result.execution_plan)
            
            logger.debug(f"Action sequencing completed: {'success' if is_success else 'failed'}, generated {action_sequence_info.get('action_count', 0)} actions")
            
            debug_info['modules']['action_sequencing'] = action_sequence_info
            debug_info['execution_times']['action_sequencing'] = time.time() - sequencing_start
        except AttributeError as e:
            logger.error(f"Action sequencing failed due to attribute error: {e}")
            debug_info['modules']['action_sequencing'] = {
                'status': 'failed',
                'error': f'Attribute error: {e}'
            }
            debug_info['execution_times']['action_sequencing'] = time.time() - sequencing_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Action sequencing failed: {e}',
                'debug_info': debug_info
            }
        except Exception as e:
            logger.error(f"Action sequencing failed: {e}")
            debug_info['modules']['action_sequencing'] = {
                'status': 'failed',
                'error': str(e)
            }
            debug_info['execution_times']['action_sequencing'] = time.time() - sequencing_start
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Action sequencing failed: {e}',
                'debug_info': debug_info
            }
        
        # ----------------- 流程结束 -----------------
        
        # Compile final result
        final_result = {
            'submission_id': submission_id,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'goal': {
                'natural_language': natural_goal,
                'interpreted': debug_info['modules']['goal_interpretation'].get('ltl_formula', '')
            },
            'subgoals': {
                'count': debug_info['modules']['subgoal_decomposition'].get('subgoal_count', 0),
                'list': debug_info['modules']['subgoal_decomposition'].get('subgoals', [])
            },
            'execution_time': time.time() - start_time,
            'execution_times': debug_info['execution_times'],
            'debug_info': debug_info
        }
        
        logger.info(f"Task {task_id} processed successfully in {time.time() - start_time:.2f} seconds")
        return final_result
        
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")
        debug_info['error'] = str(e)
        return {
            'submission_id': submission_id,
            'status': 'failed',
            'error': f'Unexpected error: {e}',
            'debug_info': debug_info
        }


def main():
    """
    Main function to run the debug script
    """
    logger.info("Starting new debug script...")
    
    # Define data files
    data_dir = os.path.join(project_root, 'data')
    parquet_files = {}
    
    # Get all parquet files in data directory
    for file in os.listdir(data_dir):
        if file.endswith('.parquet'):
            dataset_name = file.split('-')[0]
            parquet_files[dataset_name] = os.path.join(data_dir, file)
    
    logger.info(f"Found {len(parquet_files)} parquet files: {list(parquet_files.keys())}")
    
    # Create output directory
    output_dir = os.path.join(project_root, 'new_debug_results')
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file
    all_results = []
    for dataset_name, file_path in parquet_files.items():
        logger.info(f"Processing dataset: {dataset_name}")
        
        # Load samples
        samples = load_parquet_samples(file_path, num_samples=20)
        if not samples:
            logger.error(f"No samples loaded from {file_path}")
            continue
        
        # Process each sample
        for sample in samples:
            natural_goal = sample.get('natural_language_description', '')
            task_id = str(sample.get('task_id', f'unknown_{int(time.time())}'))
            
            if not natural_goal:
                logger.warning(f"Sample {task_id} has no natural language goal, skipping")
                continue
            
            # Process goal
            result = process_goal_with_debug(natural_goal, task_id, dataset_name)
            all_results.append(result)
            
            # Save intermediate result
            intermediate_file = os.path.join(output_dir, f"{dataset_name}_task_{task_id}_result.json")
            with open(intermediate_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
            logger.info(f"Intermediate result saved to {intermediate_file}")
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_tasks': len(all_results),
        'successful_tasks': sum(1 for r in all_results if r['status'] == 'success'),
        'failed_tasks': sum(1 for r in all_results if r['status'] == 'failed'),
        'results': all_results
    }
    
    summary_file = os.path.join(output_dir, f"debug_summary_{int(time.time())}.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
    
    logger.info(f"=== Debug processing complete ===")
    logger.info(f"Total tasks: {len(all_results)}")
    logger.info(f"Successful tasks: {sum(1 for r in all_results if r['status'] == 'success')}")
    logger.info(f"Failed tasks: {sum(1 for r in all_results if r['status'] == 'failed')}")
    logger.info(f"Summary saved to: {summary_file}")
    logger.info(f"Detailed logs saved to: new_debug_parquet_processing.log")
    
    print(f"\n=== Debug Processing Results ===")
    print(f"Total tasks: {len(all_results)}")
    print(f"Successful tasks: {sum(1 for r in all_results if r['status'] == 'success')}")
    print(f"Failed tasks: {sum(1 for r in all_results if r['status'] == 'failed')}")
    print(f"Summary file: {summary_file}")
    print(f"Log file: new_debug_parquet_processing.log")
    print(f"Intermediate results in: {output_dir}")


if __name__ == "__main__":
    main()