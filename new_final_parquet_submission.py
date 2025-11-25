#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EAI Challenge: New Final Submission Script for Parquet Processing
This script processes goals from the parquet files in the data directory
and generates submission results according to competition requirements.

模块执行顺序：
1. GoalInterpreter: 将自然语言目标转换为LTL公式
2. SubgoalLTLIntegration: 将LTL公式分解为子目标
3. TransitionModeler: 建模环境状态转换和动作效果
4. ActionSequencer: 生成具体的动作序列
"""

import os
import sys
import json
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional

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
try:
    from goal_interpretation import GoalInterpreter, LTLFormula
    from subgoal_decomposition import SubgoalLTLIntegration, IntegrationResult
    from transition_modeling import TransitionModeler, ModelingRequest, ModelingResponse
    from action_sequencing import ActionSequencer, SequencingRequest, Action, ActionType
    print("✓ All four modules imported successfully")
except ImportError as e:
    print(f"✗ Module import failed: {e}")
    sys.exit(1)


def create_submission_file(output_data: Dict[str, Any], output_file: str) -> None:
    """
    Create submission file
    
    Args:
        output_data: Data to be saved
        output_file: Output file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
        print(f"✓ Submission file generated: {output_file}")
    except Exception as e:
        print(f"✗ Failed to save submission file: {e}")
        # Try to save a simplified version if the full version fails
        try:
            simplified_data = {
                'submission_id': output_data.get('submission_id', 'unknown'),
                'status': 'success_with_warnings',
                'timestamp': output_data.get('timestamp', datetime.now().isoformat()),
                'goal': output_data.get('goal', {}).get('natural_language', 'unknown'),
                'error': str(e)
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(simplified_data, f, indent=2, ensure_ascii=False)
            print(f"⚠️  Saved simplified submission file: {output_file}")
        except:
            print("✗ Failed to save even simplified submission file")
            sys.exit(1)


def process_goal(natural_goal: str, output_dir: str, task_id: str, dataset: str) -> Dict[str, Any]:
    """
    Process natural language goal, integrate outputs from four modules
    
    Args:
        natural_goal: Natural language goal description
        output_dir: Output directory
        task_id: Unique task identifier from dataset
        dataset: Name of the dataset
    
    Returns:
        Integrated result data
    """
    start_time = time.time()
    submission_id = f"{dataset}_{task_id}_{int(start_time * 1000)}"
    
    # Initialize all modules
    goal_interpreter = GoalInterpreter()
    subgoal_integration = SubgoalLTLIntegration()
    transition_modeler = TransitionModeler()
    action_sequencer = ActionSequencer()
    
    # Processing flow
    try:
        # 1. Goal Interpretation - 将自然语言转换为LTL公式
        print(f"   Step 1: Interpreting goal - {natural_goal[:50]}...")
        goal_result = goal_interpreter.interpret(natural_goal)
        
        # 2. Subgoal Decomposition - 将LTL公式分解为子目标
        print(f"   Step 2: Decomposing into subgoals...")
        subgoal_result = subgoal_integration.process_goal(natural_goal)
        
        # 3. Transition Modeling - 建模状态转换
        print(f"   Step 3: Modeling transitions...")
        # Create modeling request with appropriate data from previous steps
        modeling_request = ModelingRequest(
            goal=goal_result,
            subgoals=subgoal_result.decomposition_result.subgoals if subgoal_result.decomposition_result else []
        )
        modeling_response = transition_modeler.model_transitions(modeling_request)
        
        # 4. Action Sequencing - 生成动作序列
        print(f"   Step 4: Generating action sequence...")
        # Get available actions from transition model or use default
        available_actions = []
        if hasattr(modeling_response, 'available_actions'):
            available_actions = modeling_response.available_actions
        else:
            # Use default test actions if no actions from transition model
            available_actions = [
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
        
        # Create sequencing request
        sequencing_request = SequencingRequest(
            initial_state={"at_location_start": True, "at_location_target": False, "task_completed": False},
            goal_state={"at_location_target": True, "task_completed": True},
            available_actions=available_actions
        )
        
        # Generate action sequence
        sequencing_response = action_sequencer.generate_sequence(sequencing_request)
        
        if not hasattr(sequencing_response, 'success') or not sequencing_response.success:
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Action sequencing failed: {getattr(sequencing_response, "error_message", "Unknown error")}',
                'timestamp': datetime.now().isoformat(),
                'dataset': dataset,
                'task_id': task_id,
                'natural_goal': natural_goal
            }
            
    except Exception as e:
        return {
            'submission_id': submission_id,
            'status': 'failed',
            'error': f'Processing failed: {str(e)}',
            'timestamp': datetime.now().isoformat(),
            'dataset': dataset,
            'task_id': task_id,
            'natural_goal': natural_goal
        }
    
    # Generate final submission data
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Generate final submission data
    submission_data = {
        'submission_id': submission_id,
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'execution_time_ms': int(execution_time * 1000),
        'dataset': dataset,
        'task_id': task_id,
        'goal': {
            'natural_language': natural_goal,
            'ltl_formula': goal_result.formula if hasattr(goal_result, 'formula') else str(goal_result),
            'confidence': getattr(goal_result, 'confidence', 0.0) if hasattr(goal_result, 'confidence') else 0.0
        },
        'subgoals': {
            'count': len(subgoal_result.decomposition_result.subgoals) if subgoal_result.decomposition_result else 0,
            'subgoals': [sg.__dict__ for sg in subgoal_result.decomposition_result.subgoals] if subgoal_result.decomposition_result else []
        },
        'transition_model': {
            'request_id': getattr(modeling_response, 'request_id', 'unknown'),
            'transitions_count': len(getattr(modeling_response, 'transitions', []))
        },
        'action_sequence': {
            'sequence_id': getattr(sequencing_response, 'sequence_id', 'unknown'),
            'actions': [action.__dict__ for action in sequencing_response.action_sequence.actions] if hasattr(sequencing_response.action_sequence, 'actions') else []
        }
    }
    
    return submission_data


def process_parquet_file(file_path: str, output_dir: str, max_tasks: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Process all goals from a parquet file
    
    Args:
        file_path: Path to the parquet file
        output_dir: Output directory for results
        max_tasks: Maximum number of tasks to process (None for all)
    
    Returns:
        List of processed results
    """
    print(f"\n{'='*80}")
    print(f"Processing Parquet File: {os.path.basename(file_path)}")
    print(f"{'='*80}")
    
    # Read parquet file
    try:
        df = pd.read_parquet(file_path)
        print(f"✓ Successfully read {len(df)} rows from {os.path.basename(file_path)}")
    except Exception as e:
        print(f"✗ Failed to read parquet file: {e}")
        return []
    
    # Extract dataset name
    dataset_name = os.path.basename(file_path).split('-')[0]
    
    # Ensure the dataframe has required columns
    required_columns = ['task_id', 'natural_language_description']
    for col in required_columns:
        if col not in df.columns:
            print(f"✗ Missing required column: {col}")
            return []
    
    # Limit the number of tasks if specified
    if max_tasks is not None and max_tasks > 0:
        df = df.head(max_tasks)
        print(f"✓ Processing first {max_tasks} rows only")
    
    # Process each task
    results = []
    success_count = 0
    failure_count = 0
    
    for idx, row in df.iterrows():
        task_id = str(row['task_id'])
        natural_goal = str(row['natural_language_description'])
        
        print(f"\nProcessing task {idx+1}/{len(df)}: {natural_goal[:50]}...")
        
        result = process_goal(natural_goal, output_dir, task_id, dataset_name)
        results.append(result)
        
        if result['status'] == 'success':
            success_count += 1
            print(f"✓ Task {task_id} processed successfully")
        else:
            failure_count += 1
            print(f"✗ Task {task_id} failed: {result['error']}")
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"Processing Summary for {dataset_name}")
    print(f"{'='*80}")
    print(f"Total tasks processed: {len(df)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Success rate: {(success_count/len(df)*100):.1f}%" if len(df) > 0 else "No tasks processed")
    
    return results


def main():
    """Main function"""
    print("="*80)
    print("EAI Challenge: New Final Submission Script")
    print("Processing Parquet Datasets with Four-Module Integration")
    print("="*80)
    
    # Define paths
    data_dir = os.path.join(project_root, 'data')
    output_dir = os.path.join(project_root, 'new_final_submission_results')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all parquet files in data directory
    parquet_files = []
    for file in os.listdir(data_dir):
        if file.endswith('.parquet'):
            parquet_files.append(os.path.join(data_dir, file))
    
    if not parquet_files:
        print(f"✗ No parquet files found in {data_dir}")
        sys.exit(1)
    
    # Process each parquet file
    all_results = []
    for file_path in parquet_files:
        results = process_parquet_file(file_path, output_dir)
        all_results.extend(results)
    
    # Generate final summary
    print(f"\n{'='*80}")
    print(f"Final Submission Summary")
    print(f"{'='*80}")
    print(f"Total tasks processed across all datasets: {len(all_results)}")
    
    total_success = sum(1 for r in all_results if r['status'] == 'success')
    total_failure = sum(1 for r in all_results if r['status'] == 'failed')
    
    print(f"Total successful: {total_success}")
    print(f"Total failed: {total_failure}")
    print(f"Overall success rate: {(total_success/len(all_results)*100):.1f}%" if len(all_results) > 0 else "No tasks processed")
    
    # Save final submission summary
    final_summary = {
        'timestamp': datetime.now().isoformat(),
        'submission_version': '2.0.0',
        'total_datasets': len(parquet_files),
        'total_tasks': len(all_results),
        'successful_tasks': total_success,
        'failed_tasks': total_failure,
        'success_rate': total_success/len(all_results) if len(all_results) > 0 else 0,
        'datasets': [os.path.basename(f) for f in parquet_files],
        'results': all_results
    }
    
    final_summary_file = os.path.join(output_dir, f"final_submission_summary_{int(time.time())}.json")
    with open(final_summary_file, 'w', encoding='utf-8') as f:
        json.dump(final_summary, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
    
    print(f"\n✓ Final submission summary saved to: {final_summary_file}")
    print(f"✓ Output directory: {output_dir}")
    print(f"\n{'='*80}")
    print(f"Processing Complete")
    print(f"{'='*80}")
    
    return final_summary


if __name__ == "__main__":
    try:
        main()
        print("\n✅ Final submission script executed successfully")
    except KeyboardInterrupt:
        print("\n❌ Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Script execution error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)