#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script for EAI Challenge Parquet Processing
This script extracts 10 records from each parquet file and processes them with detailed logging
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
        logging.FileHandler('debug_parquet_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('debug_script')

# Custom JSON encoder to handle non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle LogicGuard objects
        if hasattr(obj, '__class__') and obj.__class__.__name__ == 'LogicGuard':
            return {"type": "LogicGuard", "description": "Logic guard condition"}
        # Handle other custom objects by converting to string representation
        try:
            return str(obj)
        except:
            return {"type": obj.__class__.__name__, "message": "Non-serializable object"}
        # Call the parent class default method if all else fails
        return super().default(obj)

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import four core modules
logger.info("Importing core modules...")
try:
    from goal_interpretation import GoalInterpreter
    logger.info("✓ GoalInterpreter imported successfully")
    from subgoal_decomposition import SubgoalLTLIntegration
    logger.info("✓ SubgoalLTLIntegration imported successfully")
    from transition_modeling import TransitionModeler, ModelingRequest
    logger.info("✓ TransitionModeler imported successfully")
    from action_sequencing import ActionSequencer, SequencingRequest, Action, ActionType
    logger.info("✓ ActionSequencer imported successfully")
    print("✓ All four modules imported successfully")
except ImportError as e:
    logger.error(f"✗ Module import failed: {e}")
    print(f"✗ Module import failed: {e}")
    sys.exit(1)


def load_parquet_samples(file_path: str, num_samples: int = 10) -> List[Dict[str, Any]]:
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
        'modules': {}
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
        
        # Step 1: Goal Interpretation
        logger.info("Step 1: Goal Interpretation")
        try:
            interpretation_result = goal_interpreter.interpret(natural_goal)
            logger.debug(f"Interpretation result: {json.dumps(interpretation_result, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)[:1000]}...")
            debug_info['modules']['goal_interpretation'] = {
                'status': 'success',
                'result': interpretation_result,
                'execution_time': time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Goal interpretation failed: {e}")
            debug_info['modules']['goal_interpretation'] = {
                'status': 'failed',
                'error': str(e),
                'execution_time': time.time() - start_time
            }
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Goal interpretation failed: {e}',
                'debug_info': debug_info
            }
        
        # Step 2: Subgoal Decomposition
        logger.info("Step 2: Subgoal Decomposition")
        subgoal_start = time.time()
        try:
            subgoal_result = subgoal_integration.process_goal(natural_goal)
            logger.debug(f"Subgoal result: {json.dumps(subgoal_result, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)[:1000]}...")
            debug_info['modules']['subgoal_decomposition'] = {
                'status': 'success',
                'result': subgoal_result,
                'execution_time': time.time() - subgoal_start
            }
        except Exception as e:
            logger.error(f"Subgoal decomposition failed: {e}")
            debug_info['modules']['subgoal_decomposition'] = {
                'status': 'failed',
                'error': str(e),
                'execution_time': time.time() - subgoal_start
            }
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Subgoal decomposition failed: {e}',
                'debug_info': debug_info
            }
        
        # Step 3: Transition Modeling
        logger.info("Step 3: Transition Modeling")
        modeling_start = time.time()
        try:
            # Prepare modeling request
            modeling_request = ModelingRequest(
                goal=interpretation_result,
                subgoals=subgoal_result.get('subgoals', [])
            )
            transition_result = transition_modeler.model_transitions(modeling_request)
            logger.debug(f"Transition result: {json.dumps(transition_result, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)[:1000]}...")
            debug_info['modules']['transition_modeling'] = {
                'status': 'success',
                'result': transition_result,
                'execution_time': time.time() - modeling_start
            }
        except Exception as e:
            logger.error(f"Transition modeling failed: {e}")
            debug_info['modules']['transition_modeling'] = {
                'status': 'failed',
                'error': str(e),
                'execution_time': time.time() - modeling_start
            }
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Transition modeling failed: {e}',
                'debug_info': debug_info
            }
        
        # Step 4: Action Sequencing
        logger.info("Step 4: Action Sequencing")
        sequencing_start = time.time()
        try:
            # Prepare sequencing request
            sequencing_request = SequencingRequest(
                goal=interpretation_result,
                subgoals=subgoal_result.get('subgoals', []),
                transitions=transition_result.get('transitions', [])
            )
            action_result = action_sequencer.sequence_actions(sequencing_request)
            logger.debug(f"Action result: {json.dumps(action_result, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)[:1000]}...")
            debug_info['modules']['action_sequencing'] = {
                'status': 'success',
                'result': action_result,
                'execution_time': time.time() - sequencing_start
            }
        except Exception as e:
            logger.error(f"Action sequencing failed: {e}")
            debug_info['modules']['action_sequencing'] = {
                'status': 'failed',
                'error': str(e),
                'execution_time': time.time() - sequencing_start
            }
            return {
                'submission_id': submission_id,
                'status': 'failed',
                'error': f'Action sequencing failed: {e}',
                'debug_info': debug_info
            }
        
        # Compile final result
        final_result = {
            'submission_id': submission_id,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'goal': {
                'natural_language': natural_goal,
                'interpreted': interpretation_result
            },
            'subgoals': subgoal_result.get('subgoals', []),
            'transitions': transition_result.get('transitions', []),
            'actions': action_result.get('actions', []),
            'execution_time': time.time() - start_time,
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
    logger.info("Starting debug script...")
    
    # Define data files
    data_dir = os.path.join(project_root, 'data')
    parquet_files = {
        'behavior': os.path.join(data_dir, 'behavior-00000-of-00001.parquet'),
        'virtualhome': os.path.join(data_dir, 'virtualhome-00000-of-00001.parquet')
    }
    
    # Create output directory
    output_dir = os.path.join(project_root, 'debug_results')
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file
    all_results = []
    for dataset_name, file_path in parquet_files.items():
        logger.info(f"Processing dataset: {dataset_name}")
        
        # Load samples
        samples = load_parquet_samples(file_path, num_samples=10)
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
    logger.info(f"Detailed logs saved to: debug_parquet_processing.log")
    
    print(f"\n=== Debug Processing Results ===")
    print(f"Total tasks: {len(all_results)}")
    print(f"Successful tasks: {sum(1 for r in all_results if r['status'] == 'success')}")
    print(f"Failed tasks: {sum(1 for r in all_results if r['status'] == 'failed')}")
    print(f"Summary file: {summary_file}")
    print(f"Log file: debug_parquet_processing.log")
    print(f"Intermediate results in: {output_dir}")


if __name__ == "__main__":
    main()
