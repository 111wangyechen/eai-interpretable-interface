#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EAI Challenge: Basic Final Submission Script
This script processes goals from the parquet files in the data directory
and generates submission results according to competition requirements.

Features:
1. Process parquet files from the data directory
2. Generate submission results according to competition requirements
3. Automatically save terminal output to a log file
"""

import os
import sys
import json
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional


class OutputLogger:
    """Class to simultaneously write output to terminal and log file"""
    
    def __init__(self, log_file: str):
        """
        Initialize OutputLogger
        
        Args:
            log_file (str): Path to the log file
        """
        self.terminal = sys.stdout
        self.log = open(log_file, "a", encoding="utf-8")
    
    def write(self, message: str):
        """
        Write message to both terminal and log file
        
        Args:
            message (str): Message to write
        """
        self.terminal.write(message)
        self.log.write(message)
    
    def flush(self):
        """Flush both terminal and log file buffers"""
        self.terminal.flush()
        self.log.flush()
        os.fsync(self.log.fileno())
    
    def close(self):
        """Close the log file"""
        if self.log:
            self.log.close()

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import four core modules
try:
    from goal_interpretation import EnhancedGoalInterpreter as GoalInterpreter
    from subgoal_decomposition import SubgoalLTLIntegration
    from transition_modeling import TransitionModeler, ModelingRequest
    from action_sequencing import ActionSequencer, SequencingRequest, Action, ActionType
    print("✓ All four modules imported successfully")
except ImportError as e:
    print(f"✗ Module import failed: {e}")
    sys.exit(1)


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle non-serializable objects"""
    def default(self, obj):
        # Handle custom objects
        if hasattr(obj, '__class__'):
            # Try to use to_dict method if available
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            # Otherwise return string representation
            try:
                return str(obj)
            except:
                return {"type": obj.__class__.__name__, "message": "Non-serializable object"}
        # Call the parent class default method if all else fails
        return super().default(obj)


def process_single_goal(natural_goal: str, task_id: str, dataset: str) -> Dict[str, Any]:
    """
    Process a single natural language goal through all four modules
    
    Args:
        natural_goal: Natural language goal description
        task_id: Unique task identifier
        dataset: Dataset name
    
    Returns:
        Processed result dictionary
    """
    start_time = time.time()
    
    # Initialize modules
    goal_interpreter = GoalInterpreter()
    subgoal_integration = SubgoalLTLIntegration()
    transition_modeler = TransitionModeler()
    action_sequencer = ActionSequencer()
    
    result = {
        'task_id': task_id,
        'dataset': dataset,
        'natural_goal': natural_goal,
        'status': 'success',
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # 1. Goal Interpretation
        print(f"   1. Interpreting goal: {natural_goal[:30]}...")
        goal_result = goal_interpreter.interpret(natural_goal)
        result['goal_interpretation'] = {
            'ltl_formula': getattr(goal_result, 'formula', getattr(goal_result, 'ltl_formula', '')),
            'confidence': getattr(goal_result, 'confidence', 0.0)
        }
        
        # 2. Subgoal Decomposition
        print("   2. Decomposing into subgoals...")
        subgoal_result = subgoal_integration.process_goal(natural_goal)
        if hasattr(subgoal_result, 'decomposition_result'):
            result['subgoals'] = subgoal_result.decomposition_result
        
        # 3. Transition Modeling
        print("   3. Modeling state transitions...")
        # Create a comprehensive modeling request with detailed states
        initial_state = {
            'at_location': 'desk', 
            'task_completed': False,
            'computer_state': 'closed',
            'email_checked': False,
            'has_ball': False,
            'door_state': 'closed',
            # 物体属性
            'rag_n_01_1': {'location': 'cabinet', 'state': 'clean', 'is_graspable': True},
            'pot_plant_n_01_2': {'location': 'window_sill', 'state': 'healthy', 'is_graspable': True},
            'carton_66': {'location': 'floor', 'state': 'empty', 'is_openable': True},
            'computer': {'location': 'desk', 'state': 'closed', 'is_operable': True},
            'sink_n_01_1': {'location': 'kitchen', 'state': 'empty', 'is_usable': True},
            'fridge': {'location': 'kitchen', 'state': 'closed', 'is_openable': True},
            'pot': {'location': 'stove', 'state': 'clean', 'is_usable': True},
            # 环境细节
            'lights': {'state': 'off'},
            'temperature': 22,
            'time_of_day': 'morning'
        }
        goal_state = {
            'at_location': 'desk', 
            'task_completed': True,
            'computer_state': 'closed',
            'email_checked': True,
            'has_ball': False,
            'door_state': 'closed',
            # 物体属性（目标状态）
            'rag_n_01_1': {'location': 'cabinet', 'state': 'clean', 'is_graspable': True},
            'pot_plant_n_01_2': {'location': 'window_sill', 'state': 'healthy', 'is_graspable': True},
            'carton_66': {'location': 'floor', 'state': 'full', 'is_openable': True},
            'computer': {'location': 'desk', 'state': 'closed', 'is_operable': True},
            'sink_n_01_1': {'location': 'kitchen', 'state': 'empty', 'is_usable': True},
            'fridge': {'location': 'kitchen', 'state': 'closed', 'is_openable': True},
            'pot': {'location': 'stove', 'state': 'clean', 'is_usable': True},
            # 环境细节（目标状态）
            'lights': {'state': 'off'},
            'temperature': 22,
            'time_of_day': 'morning'
        }
        available_transitions = transition_modeler.create_sample_transitions()
        
        modeling_request = ModelingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_transitions=available_transitions
        )
        
        modeling_response = transition_modeler.model_transitions(modeling_request)
        result['transition_model'] = {
            'request_id': getattr(modeling_response, 'request_id', ''),
            'predicted_sequences_count': len(getattr(modeling_response, 'predicted_sequences', []))
        }
        
        # 4. Action Sequencing
        print("   4. Generating action sequence...")
        # Define comprehensive actions with proper preconditions and effects
        available_actions = [
            # 导航与位置相关动作
            Action(
                id="navigate_to_desk",
                name="NavigateTo",
                action_type=ActionType.NAVIGATION,
                parameters={"target": "desk"},
                preconditions=["at_location != desk"],
                effects=["at_location = desk"]
            ),
            Action(
                id="navigate_to_kitchen",
                name="NavigateTo",
                action_type=ActionType.NAVIGATION,
                parameters={"target": "kitchen"},
                preconditions=["at_location != kitchen"],
                effects=["at_location = kitchen"]
            ),
            # 物体抓取与释放
            Action(
                id="grasp_rag",
                name="Grasp",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "rag_n_01_1"},
                preconditions=["at_location = cabinet", "rag_n_01_1.is_graspable = True"],
                effects=["has_rag = True"]
            ),
            Action(
                id="release_rag",
                name="Release",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "rag_n_01_1"},
                preconditions=["has_rag = True"],
                effects=["has_rag = False"]
            ),
            # 物体放置与空间操作
            Action(
                id="place_inside_carton",
                name="PlaceInside",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "book", "container": "carton_66"},
                preconditions=["has_book = True", "carton_66.state = open"],
                effects=["carton_66.state = full", "has_book = False"]
            ),
            Action(
                id="place_nextto_pot",
                name="PlaceNextTo",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "spoon", "target": "pot"},
                preconditions=["has_spoon = True", "at_location = stove"],
                effects=["has_spoon = False"]
            ),
            # 开关与状态切换
            Action(
                id="open_computer",
                name="Open",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "computer"},
                preconditions=["at_location == desk", "computer_state == closed"],
                effects=["computer_state = open"]
            ),
            Action(
                id="close_computer",
                name="Close",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "computer"},
                preconditions=["at_location == desk", "computer_state == open"],
                effects=["computer_state = closed"]
            ),
            Action(
                id="toggle_on_lights",
                name="ToggleOn",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "lights"},
                preconditions=["lights.state == off"],
                effects=["lights.state = on"]
            ),
            # 清洁与维护动作
            Action(
                id="soak_rag",
                name="Soak",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "rag_n_01_1", "container": "sink_n_01_1"},
                preconditions=["has_rag = True", "at_location = kitchen", "sink_n_01_1.is_usable = True"],
                effects=["rag_n_01_1.state = soaked"]
            ),
            Action(
                id="clean_dusty_rag_table",
                name="CleanDustyRag",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "table", "tool": "rag_n_01_1"},
                preconditions=["has_rag = True", "table.state = dusty"],
                effects=["table.state = clean"]
            ),
            # 其他操作动作
            Action(
                id="slice_bread",
                name="Slice",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "bread"},
                preconditions=["at_location = kitchen", "has_knife = True"],
                effects=["bread.state = sliced"]
            ),
            Action(
                id="cook_soup",
                name="Cook",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "soup", "container": "pot"},
                preconditions=["at_location = stove", "pot.state = empty"],
                effects=["soup.state = cooked"]
            ),
            # 原有的任务相关动作
            Action(
                id="check_email",
                name="CheckEmail",
                action_type=ActionType.MANIPULATION,
                parameters={"object": "computer"},
                preconditions=["at_location == desk", "computer_state == open", "email_checked == False"],
                effects=["email_checked = True"]
            ),
            Action(
                id="complete_task",
                name="CompleteTask",
                action_type=ActionType.MANIPULATION,
                parameters={},
                preconditions=["email_checked == True"],
                effects=["task_completed = True"]
            )
        ]
        
        sequencing_request = SequencingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_actions=available_actions
        )
        
        sequencing_response = action_sequencer.generate_sequence(sequencing_request)
        
        if sequencing_response.success and hasattr(sequencing_response, 'action_sequence'):
            result['action_sequence'] = sequencing_response.action_sequence
        else:
            result['status'] = 'failed'
            result['error'] = f"Action sequencing failed: {getattr(sequencing_response, 'error_message', 'Unknown error')}"
        
    except Exception as e:
        result['status'] = 'failed'
        result['error'] = f"Processing failed: {str(e)}"
    
    # Calculate execution time
    end_time = time.time()
    result['execution_time_ms'] = int((end_time - start_time) * 1000)
    
    return result


def process_parquet_files(data_dir: str, output_dir: str) -> List[Dict[str, Any]]:
    """
    Process all parquet files in the data directory
    
    Args:
        data_dir: Directory containing parquet files
        output_dir: Directory to save output files
    
    Returns:
        List of processed results
    """
    # Get all parquet files
    parquet_files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
    if not parquet_files:
        print(f"✗ No parquet files found in {data_dir}")
        return []
    
    all_results = []
    
    for file_name in parquet_files:
        file_path = os.path.join(data_dir, file_name)
        dataset_name = file_name.split('-')[0]  # Extract dataset name from filename
        
        print(f"\n{'='*80}")
        print(f"Processing file: {file_name}")
        print(f"Dataset: {dataset_name}")
        print(f"{'='*80}")
        
        # Read parquet file
        try:
            df = pd.read_parquet(file_path)
            print(f"✓ Successfully read {len(df)} rows")
        except Exception as e:
            print(f"✗ Failed to read parquet file: {e}")
            continue
        
        # Ensure required columns are present
        required_columns = ['task_id', 'natural_language_description']
        if not all(col in df.columns for col in required_columns):
            print(f"✗ Missing required columns. Expected: {required_columns}, Got: {list(df.columns)}")
            continue
        
        # Process each row
        for idx, row in df.iterrows():
            task_id = str(row['task_id'])
            natural_goal = str(row['natural_language_description'])
            
            print(f"\nProcessing task {idx+1}/{len(df)}: {task_id}")
            print(f"Goal: {natural_goal}")
            
            result = process_single_goal(natural_goal, task_id, dataset_name)
            all_results.append(result)
            
            status = "✓ SUCCESS" if result['status'] == 'success' else "✗ FAILED"
            print(f"   {status} in {result['execution_time_ms']}ms")
    
    return all_results


def generate_final_submission(results: List[Dict[str, Any]], output_file: str) -> None:
    """
    Generate the final submission file
    
    Args:
        results: List of processed results
        output_file: Path to save the final submission file
    """
    # Calculate summary statistics
    total_tasks = len(results)
    successful_tasks = sum(1 for r in results if r['status'] == 'success')
    failed_tasks = total_tasks - successful_tasks
    
    submission_data = {
        "submission_info": {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "generator": "basic_final_submission.py",
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0.0
        },
        "results": results
    }
    
    # Save the final submission file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(submission_data, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
        print(f"\n{'='*80}")
        print(f"✓ Final submission file generated: {output_file}")
        print(f"✓ Total tasks processed: {total_tasks}")
        print(f"✓ Successful: {successful_tasks} ({successful_tasks/total_tasks*100:.1f}%)")
        print(f"✓ Failed: {failed_tasks} ({failed_tasks/total_tasks*100:.1f}%)")
        print(f"{'='*80}")
    except Exception as e:
        print(f"✗ Failed to generate submission file: {e}")
        sys.exit(1)


def main():
    """Main function"""
    start_time = datetime.now()
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    
    # Configuration
    data_dir = os.path.join(project_root, 'data')
    output_dir = os.path.join(project_root, 'final_submission_results')
    final_output_file = os.path.join(project_root, 'final_submission.json')
    log_dir = os.path.join(project_root, 'submission_outputs')
    log_file = os.path.join(log_dir, f'terminal_output_{timestamp}.log')
    
    # Create necessary directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    
    # Initialize output logger
    logger = OutputLogger(log_file)
    sys.stdout = logger
    
    # Print header
    print("="*80)
    print("EAI Challenge: Basic Final Submission Script")
    print("="*80)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: {log_file}")
    print(f"Output directory: {output_dir}")
    
    try:
        # Process all parquet files
        print(f"\nProcessing parquet files from: {data_dir}")
        results = process_parquet_files(data_dir, output_dir)
        
        # Generate final submission
        if results:
            generate_final_submission(results, final_output_file)
            print(f"\n✅ Final submission file generated: {final_output_file}")
        else:
            print("✗ No results to generate submission")
            sys.exit(1)
        
        end_time = datetime.now()
        print(f"\n✅ Basic final submission script completed successfully")
        print(f"\n=== Script completed ===")
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {end_time - start_time}")
        print("="*80)
    finally:
        # Restore original stdout and close logger
        sys.stdout = logger.terminal
        logger.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Script execution error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)