#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Module Integration Test Script
Tests the integration between Goal Interpretation, Subgoal Decomposition, and Action Sequencing modules
for English natural language instruction processing
"""

import sys
import os
import pandas as pd
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import asdict

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from goal_interpretation import EnhancedGoalInterpreter
    from subgoal_decomposition import SubgoalDecomposer
    from action_sequencing import ActionSequencer, SequencingConfig, SequencingRequest, Action, ActionType, ActionStatus
    from subgoal_decomposition.subgoal_decomposer import DecompositionStrategy
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all module dependencies are available")
    sys.exit(1)


class CrossModuleIntegrationTester:
    """
    Cross-module integration tester for English natural language processing
    """
    
    def __init__(self, dataset_path: str):
        """
        Initialize the integration tester
        
        Args:
            dataset_path: Path to the parquet dataset
        """
        self.dataset_path = dataset_path
        self.goal_interpreter = EnhancedGoalInterpreter()
        self.subgoal_decomposer = SubgoalDecomposer(strategy=DecompositionStrategy.TEMPORAL_HIERARCHICAL)
        self.action_sequencer = ActionSequencer(SequencingConfig())
        
        # Test results storage
        self.test_results = {
            'total_tests': 0,
            'successful_integrations': 0,
            'failed_integrations': 0,
            'error_details': [],
            'performance_metrics': {
                'goal_interpretation_time': [],
                'subgoal_decomposition_time': [],
                'action_sequencing_time': [],
                'total_pipeline_time': []
            }
        }
    
    def load_test_data(self, limit: int = 5) -> List[Dict]:
        """
        Load test data from parquet dataset
        
        Args:
            limit: Number of test cases to load
            
        Returns:
            List[Dict]: Test data samples
        """
        try:
            df = pd.read_parquet(self.dataset_path)
            test_data = []
            
            for idx, row in df.head(limit).iterrows():
                test_sample = {
                    'index': idx,
                    'natural_language_description': row.get('natural_language_description', ''),
                    'tl_goal': row.get('tl_goal', ''),
                    'action_trajectory': row.get('action_trajectory', []),
                    'transition_model': row.get('transition_model', {})
                }
                test_data.append(test_sample)
            
            return test_data
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return []
    
    def test_goal_interpretation(self, natural_language_text: str) -> Dict[str, Any]:
        """
        Test Goal Interpretation module
        
        Args:
            natural_language_text: Input natural language text
            
        Returns:
            Dict: Goal interpretation result
        """
        start_time = time.time()
        
        try:
            result = self.goal_interpreter.interpret(natural_language_text)
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'ltl_formula': result.get('ltl_formula', ''),
                'validation_result': result.get('validation_result', {})
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def test_subgoal_decomposition(self, ltl_formula: str) -> Dict[str, Any]:
        """
        Test Subgoal Decomposition module
        
        Args:
            ltl_formula: Input LTL formula from goal interpretation
            
        Returns:
            Dict: Subgoal decomposition result
        """
        start_time = time.time()
        
        try:
            result = self.subgoal_decomposer.decompose(ltl_formula)
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'subgoals_count': len(result.subgoals),
                'execution_order': result.execution_order,
                'total_cost': result.total_cost
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def test_action_sequencing(self, subgoals: List, initial_state: Dict = None) -> Dict[str, Any]:
        """
        Test Action Sequencing module
        
        Args:
            subgoals: List of subgoals from decomposition
            initial_state: Initial state for action sequencing
            
        Returns:
            Dict: Action sequencing result
        """
        start_time = time.time()
        
        try:
            # Convert subgoals to actions
            actions = []
            for i, subgoal in enumerate(subgoals):
                action = Action(
                    id=f"action_{i}",
                    name=f"Execute_{subgoal.description.replace(' ', '_')}",
                    action_type=ActionType.MANIPULATION,
                    parameters={'subgoal_id': subgoal.id},
                    preconditions=subgoal.preconditions,
                    effects=subgoal.effects,
                    duration=subgoal.estimated_cost
                )
                actions.append(action)
            
            # Create initial state if not provided
            if initial_state is None:
                initial_state = {'agent_ready': True}
            
            # Create goal state
            goal_state = {'all_subgoals_completed': True}
            
            # Create sequencing request
            request = SequencingRequest(
                initial_state=initial_state,
                goal_state=goal_state,
                available_actions=actions
            )
            
            # Generate action sequence
            response = self.action_sequencer.generate_sequence(request)
            execution_time = time.time() - start_time
            
            return {
                'success': response.success,
                'result': response,
                'execution_time': execution_time,
                'action_sequence': response.action_sequence,
                'planning_result': response.planning_result,
                'error_message': response.error_message
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def run_full_pipeline_test(self, test_sample: Dict) -> Dict[str, Any]:
        """
        Run full pipeline test: Goal Interpretation → Subgoal Decomposition → Action Sequencing
        
        Args:
            test_sample: Test data sample
            
        Returns:
            Dict: Full pipeline test result
        """
        pipeline_start_time = time.time()
        nl_text = test_sample['natural_language_description']
        
        print(f"\n=== Testing Pipeline for: '{nl_text[:100]}...' ===")
        
        # Step 1: Goal Interpretation
        print("Step 1: Goal Interpretation...")
        goal_result = self.test_goal_interpretation(nl_text)
        
        if not goal_result['success']:
            error_msg = f"Goal Interpretation failed: {goal_result.get('error', 'Unknown error')}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'stage': 'goal_interpretation',
                'test_sample': test_sample
            }
        
        print(f"✅ Goal Interpretation completed in {goal_result['execution_time']:.3f}s")
        print(f"   LTL Formula: {goal_result['ltl_formula']}")
        
        # Step 2: Subgoal Decomposition
        print("Step 2: Subgoal Decomposition...")
        subgoal_result = self.test_subgoal_decomposition(goal_result['ltl_formula'])
        
        if not subgoal_result['success']:
            error_msg = f"Subgoal Decomposition failed: {subgoal_result.get('error', 'Unknown error')}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'stage': 'subgoal_decomposition',
                'goal_result': goal_result,
                'test_sample': test_sample
            }
        
        print(f"✅ Subgoal Decomposition completed in {subgoal_result['execution_time']:.3f}s")
        print(f"   Generated {subgoal_result['subgoals_count']} subgoals")
        
        # Step 3: Action Sequencing
        print("Step 3: Action Sequencing...")
        action_result = self.test_action_sequencing(subgoal_result['result'].subgoals)
        
        if not action_result['success']:
            error_msg = f"Action Sequencing failed: {action_result.get('error', 'Unknown error')}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'stage': 'action_sequencing',
                'goal_result': goal_result,
                'subgoal_result': subgoal_result,
                'test_sample': test_sample
            }
        
        print(f"✅ Action Sequencing completed in {action_result['execution_time']:.3f}s")
        
        total_pipeline_time = time.time() - pipeline_start_time
        print(f"🎉 Full pipeline completed successfully in {total_pipeline_time:.3f}s")
        
        return {
            'success': True,
            'goal_result': goal_result,
            'subgoal_result': subgoal_result,
            'action_result': action_result,
            'total_pipeline_time': total_pipeline_time,
            'test_sample': test_sample
        }
    
    def run_comprehensive_tests(self, test_limit: int = 5) -> Dict[str, Any]:
        """
        Run comprehensive integration tests
        
        Args:
            test_limit: Number of test cases to run
            
        Returns:
            Dict: Comprehensive test results
        """
        print("=== Cross-Module Integration Test Suite ===")
        print(f"Loading test data from: {self.dataset_path}")
        
        test_data = self.load_test_data(test_limit)
        
        if not test_data:
            return {
                'success': False,
                'error': 'No test data available'
            }
        
        print(f"Loaded {len(test_data)} test samples")
        
        self.test_results['total_tests'] = len(test_data)
        
        for i, test_sample in enumerate(test_data):
            print(f"\n{'='*60}")
            print(f"Test Case {i+1}/{len(test_data)}")
            print(f"{'='*60}")
            
            result = self.run_full_pipeline_test(test_sample)
            
            if result['success']:
                self.test_results['successful_integrations'] += 1
                
                # Store performance metrics
                self.test_results['performance_metrics']['goal_interpretation_time'].append(
                    result['goal_result']['execution_time']
                )
                self.test_results['performance_metrics']['subgoal_decomposition_time'].append(
                    result['subgoal_result']['execution_time']
                )
                self.test_results['performance_metrics']['action_sequencing_time'].append(
                    result['action_result']['execution_time']
                )
                self.test_results['performance_metrics']['total_pipeline_time'].append(
                    result['total_pipeline_time']
                )
            else:
                self.test_results['failed_integrations'] += 1
                self.test_results['error_details'].append({
                    'test_index': i,
                    'error': result['error'],
                    'stage': result.get('stage', 'unknown'),
                    'natural_language': test_sample['natural_language_description'][:100]
                })
        
        # Generate summary report
        self.generate_summary_report()
        
        return self.test_results
    
    def generate_summary_report(self):
        """Generate summary report of test results"""
        print(f"\n{'='*60}")
        print("INTEGRATION TEST SUMMARY REPORT")
        print(f"{'='*60}")
        
        success_rate = (self.test_results['successful_integrations'] / 
                       self.test_results['total_tests']) * 100 if self.test_results['total_tests'] > 0 else 0
        
        print(f"Total Tests: {self.test_results['total_tests']}")
        print(f"Successful Integrations: {self.test_results['successful_integrations']}")
        print(f"Failed Integrations: {self.test_results['failed_integrations']}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.test_results['performance_metrics']['total_pipeline_time']:
            avg_pipeline_time = sum(self.test_results['performance_metrics']['total_pipeline_time']) / len(self.test_results['performance_metrics']['total_pipeline_time'])
            print(f"Average Pipeline Time: {avg_pipeline_time:.3f}s")
        
        # Performance breakdown
        if self.test_results['successful_integrations'] > 0:
            print(f"\nPerformance Breakdown (averages):")
            
            if self.test_results['performance_metrics']['goal_interpretation_time']:
                avg_goal_time = sum(self.test_results['performance_metrics']['goal_interpretation_time']) / len(self.test_results['performance_metrics']['goal_interpretation_time'])
                print(f"  Goal Interpretation: {avg_goal_time:.3f}s")
            
            if self.test_results['performance_metrics']['subgoal_decomposition_time']:
                avg_subgoal_time = sum(self.test_results['performance_metrics']['subgoal_decomposition_time']) / len(self.test_results['performance_metrics']['subgoal_decomposition_time'])
                print(f"  Subgoal Decomposition: {avg_subgoal_time:.3f}s")
            
            if self.test_results['performance_metrics']['action_sequencing_time']:
                avg_action_time = sum(self.test_results['performance_metrics']['action_sequencing_time']) / len(self.test_results['performance_metrics']['action_sequencing_time'])
                print(f"  Action Sequencing: {avg_action_time:.3f}s")
        
        # Error details
        if self.test_results['error_details']:
            print(f"\nError Details:")
            for error in self.test_results['error_details']:
                print(f"  Test {error['test_index'] + 1}: {error['error']}")
                print(f"    Stage: {error['stage']}")
                print(f"    Input: {error['natural_language']}...")
        
        print(f"\n{'='*60}")


def main():
    """Main function to run integration tests"""
    # Dataset path
    dataset_path = 'virtualhome-00000-of-00001.parquet'
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file not found: {dataset_path}")
        print("Please ensure the parquet dataset is in the current directory")
        return
    
    # Create tester
    tester = CrossModuleIntegrationTester(dataset_path)
    
    # Run comprehensive tests
    results = tester.run_comprehensive_tests(test_limit=3)
    
    # Save results to file
    try:
        with open('integration_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nDetailed results saved to: integration_test_results.json")
    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    main()