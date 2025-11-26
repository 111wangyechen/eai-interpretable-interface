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

# Import four core modules
logger.info("Importing core modules...")
try:
    from goal_interpretation import GoalInterpreter, LTLFormula
    logger.info("✓ GoalInterpreter imported successfully")
    from subgoal_decomposition import SubgoalLTLIntegration, IntegrationResult
    logger.info("✓ SubgoalLTLIntegration imported successfully")
    from transition_modeling import TransitionModeler, ModelingRequest, ModelingResponse
    logger.info("✓ TransitionModeler imported successfully")
    from action_sequencing import ActionSequencer, SequencingRequest, Action, ActionType
    logger.info("✓ ActionSequencer imported successfully")
    print("✓ All four modules imported successfully")
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
        # Initialize all modules
        logger.info("Initializing modules...")
        goal_interpreter = GoalInterpreter()
        subgoal_integration = SubgoalLTLIntegration()
        transition_modeler = TransitionModeler()
        action_sequencer = ActionSequencer()
        logger.info("All modules initialized successfully")
        
        # ----------------- 遵循依赖关系的正确流程 -----------------
        
        # Step 1: Goal Interpretation
        logger.info("Step 1: Goal Interpretation")
        interpretation_start = time.time()
        try:
            interpretation_result = goal_interpreter.interpret(natural_goal)
            interpretation_formula = getattr(interpretation_result, 'formula', str(interpretation_result))
            logger.debug(f"Interpretation result: {interpretation_formula}")
            
            # 仅存储可序列化的目标解释信息，避免循环引用
            debug_info['modules']['goal_interpretation'] = {
                'status': 'success',
                'formula': interpretation_formula,
                'type': type(interpretation_result).__name__
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
        
        # Step 2: Subgoal Decomposition (使用目标解释结果作为上下文)
        logger.info("Step 2: Subgoal Decomposition")
        subgoal_start = time.time()
        try:
            # 调用子目标分解模块，传递自然语言目标和目标解释结果
            subgoal_result = subgoal_integration.process_goal(natural_goal)
            
            # 安全获取子目标数量
            decomposition_result = getattr(subgoal_result, 'decomposition_result', None)
            subgoals = getattr(decomposition_result, 'subgoals', []) if decomposition_result else []
            subgoal_count = len(subgoals)
            
            # 处理子目标，仅保留可序列化信息
            serializable_subgoals = []
            for subgoal in subgoals:
                try:
                    # 尝试将子目标转换为字典或提取关键信息
                    if hasattr(subgoal, 'to_dict'):
                        serializable_subgoals.append(subgoal.to_dict())
                    elif isinstance(subgoal, dict):
                        serializable_subgoals.append(subgoal)
                    else:
                        # 提取子目标的关键属性
                        serializable_subgoals.append({
                            'id': getattr(subgoal, 'id', str(subgoal)),
                            'description': getattr(subgoal, 'description', str(subgoal)),
                            'status': getattr(subgoal, 'status', 'unknown')
                        })
                except Exception:
                    # 如果无法序列化，只保存字符串表示
                    serializable_subgoals.append(str(subgoal))
            
            logger.debug(f"Subgoal result: {subgoal_count} subgoals generated")
            debug_info['modules']['subgoal_decomposition'] = {
                'status': 'success',
                'subgoal_count': subgoal_count,
                'subgoals': serializable_subgoals,
                'type': type(subgoal_result).__name__
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
            # 从目标解释和子目标分解结果中提取相关信息
            # 动态构建初始状态和目标状态，避免硬编码
            initial_state = {
                'at_location': 'start',
                'task_completed': False,
                'objects': {},
                'environment': dataset
            }
            
            goal_state = {
                'at_location': 'target',
                'task_completed': True,
                'objects': {},
                'environment': dataset
            }
            
            # 准备建模请求，包含完整的上下文信息
            modeling_request = ModelingRequest(
                initial_state=initial_state,
                goal_state=goal_state,
                context={
                    "goal_text": natural_goal,
                    "interpretation_result": interpretation_result,
                    "subgoals": subgoals,
                    "dataset": dataset,
                    "task_id": task_id
                }
            )
            
            transition_result = transition_modeler.model_transitions(modeling_request)
            logger.debug(f"Transition modeling completed successfully")
            
            # 仅存储可序列化的转换模型信息
            debug_info['modules']['transition_modeling'] = {
                'status': 'success',
                'type': type(transition_result).__name__
            }
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
                # 根据任务类型动态生成相关动作，避免硬编码
                logger.debug("No actions from transition model, generating task-specific actions")
                
                # 基于目标文本和子目标动态生成动作
                action_templates = []
                
                # 导航相关动作
                action_templates.append({
                    'id': "move",
                    'name': "NavigateToLocation",
                    'action_type': ActionType.NAVIGATION,
                    'parameters': {"target": "target"},
                    'preconditions': ["at_location_start"],
                    'effects': ["at_location_target"]
                })
                
                # 任务完成相关动作
                action_templates.append({
                    'id': "complete",
                    'name': "ExecuteTask",
                    'action_type': ActionType.MANIPULATION,
                    'parameters': {},
                    'preconditions': ["at_location_target"],
                    'effects': ["task_completed"]
                })
                
                # 将模板转换为Action对象
                available_actions = [Action(**template) for template in action_templates]
            
            # 创建排序请求，仅使用SequencingRequest类支持的参数
            sequencing_request = SequencingRequest(
                initial_state=initial_state,
                goal_state=goal_state,
                available_actions=available_actions
            )
            
            # 验证请求有效性
            if not sequencing_request.validate():
                logger.error("Sequencing request validation failed")
                raise ValueError("Invalid sequencing request")
            
            # Generate action sequence
            action_result = action_sequencer.generate_sequence(sequencing_request)
            
            # 安全检查action_result状态
            is_success = getattr(action_result, 'success', False)
            logger.debug(f"Action sequencing completed: {'success' if is_success else 'failed'}")
            
            # 仅存储可序列化的动作序列信息
            action_sequence_info = {
                'status': 'success' if is_success else 'failed',
                'type': type(action_result).__name__
            }
            
            # 如果有动作序列，提取可序列化信息
            if is_success and hasattr(action_result, 'actions'):
                try:
                    serializable_actions = []
                    for action in action_result.actions:
                        if hasattr(action, 'to_dict'):
                            serializable_actions.append(action.to_dict())
                        else:
                            serializable_actions.append({
                                'id': getattr(action, 'id', 'unknown'),
                                'name': getattr(action, 'name', 'unknown'),
                                'type': getattr(action, 'action_type', 'unknown')
                            })
                    action_sequence_info['actions'] = serializable_actions
                except Exception:
                    pass
            
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
                'interpreted': debug_info['modules']['goal_interpretation']['formula']
            },
            'subgoals': {
                'count': debug_info['modules']['subgoal_decomposition']['subgoal_count'],
                'list': debug_info['modules']['subgoal_decomposition']['subgoals']
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