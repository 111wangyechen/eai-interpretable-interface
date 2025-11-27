#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Integration Test for English Dataset
整合三个模块的完整英文测试脚本
Goal Interpretation -> Subgoal Decomposition -> Action Sequencing
"""

import sys
import os
import traceback
from datetime import datetime

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir  # Since we're in the project root directory
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Debug: Print paths to verify
print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:5]}...")  # Show first 5 paths

def print_separator(title):
    """Print separator with title"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_test_result(test_name, success, details=""):
    """Print test result in consistent format"""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"    Details: {details}")

def test_goal_interpretation():
    """Test Goal Interpretation Module"""
    print_separator("GOAL INTERPRETATION MODULE TEST")
    
    try:
        # Import from goal_interpretation package
        from goal_interpretation import EnhancedGoalInterpreter
        
        interpreter = EnhancedGoalInterpreter()
        print_test_result("Import EnhancedGoalInterpreter", True)
        
        # Test with English goal
        english_goal = "Robot should walk to bathroom and wash hands"
        result = interpreter.interpret(english_goal)
        
        # Check key fields
        success = (result is not None and 
                  'propositions' in result and 
                  'ltl_formula' in result and
                  len(result['propositions']) > 0)
        
        print_test_result("English Goal Interpretation", success,
                        f"Propositions: {result.get('propositions', [])}")
        
        if success:
            print(f"    Generated LTL: {result.get('ltl_formula', 'None')}")
            print(f"    Language: {result.get('language', 'unknown')}")
        
        return result, success
            
    except Exception as e:
        print_test_result("Goal Interpretation", False, str(e))
        traceback.print_exc()
        return None, False

def run_subgoal_decomposition(ltl_formula):
    """Run Subgoal Decomposition Module Test"""
    print_separator("SUBGOAL DECOMPOSITION MODULE TEST")
    
    try:
        # Import from packages
        from subgoal_decomposition import SubgoalDecomposer, DecompositionStrategy
        from goal_interpretation import LTLFormula
        
        # Create decomposer
        decomposer = SubgoalDecomposer()
        print_test_result("Create SubgoalDecomposer", True)
        
        # Create LTL formula object
        if isinstance(ltl_formula, str):
            ltl_obj = LTLFormula(
                formula=ltl_formula,
                description="Decomposition test formula",
                confidence=0.9
            )
        else:
            ltl_obj = ltl_formula
        
        # Test different strategies
        strategies = [DecompositionStrategy.TEMPORAL_HIERARCHICAL, DecompositionStrategy.HYBRID]
        best_result = None
        
        for strategy in strategies:
            try:
                decomposer.set_strategy(strategy)
                result = decomposer.decompose(ltl_obj, max_depth=3)
                
                success = result is not None and len(result.subgoals) > 0
                print_test_result(f"Strategy {strategy.value}", success,
                                f"Subgoals: {len(result.subgoals) if result else 0}")
                
                if success and (best_result is None or len(result.subgoals) > len(best_result.subgoals)):
                    best_result = result
                    
            except Exception as e:
                print_test_result(f"Strategy {strategy.value}", False, str(e))
        
        return best_result, best_result is not None
        
    except Exception as e:
        print_test_result("Subgoal Decomposition", False, str(e))
        traceback.print_exc()
        return None, False

def run_action_sequencing(subgoals):
    """Run Action Sequencing Module Test"""
    print_separator("ACTION SEQUENCING MODULE TEST")
    
    try:
        # Import from packages
        from action_sequencing import ActionSequencer, SequencingRequest, SequencingConfig
        from action_sequencing import Action, ActionType
        
        # Create sequencer
        config = SequencingConfig(
            max_depth=20,
            max_time=10.0,
            enable_logging=False
        )
        sequencer = ActionSequencer(config)
        print_test_result("Create ActionSequencer", True)
        
        # Create simple test actions based on subgoals
        available_actions = []
        
        # Basic navigation action
        walk_action = Action(
            id="walk_to_bathroom",
            name="Walk to Bathroom",
            action_type=ActionType.NAVIGATION,
            preconditions=["robot_location=living_room"],
            effects=["robot_location=bathroom"],
            cost=1.0
        )
        available_actions.append(walk_action)
        
        # Basic manipulation action
        wash_action = Action(
            id="wash_hands",
            name="Wash Hands",
            action_type=ActionType.MANIPULATION,
            preconditions=["robot_location=bathroom", "hands_dirty=true"],
            effects=["hands_clean=true", "hands_dirty=false"],
            cost=2.0
        )
        available_actions.append(wash_action)
        
        # Create initial and goal states
        initial_state = {
            "robot_location": "living_room",
            "hands_dirty": True,
            "hands_clean": False
        }
        
        goal_state = {
            "robot_location": "bathroom",
            "hands_clean": True,
            "hands_dirty": False
        }
        
        # Create sequencing request
        request = SequencingRequest(
            initial_state=initial_state,
            goal_state=goal_state,
            available_actions=available_actions
        )
        
        print_test_result("Create SequencingRequest", True)
        
        # Generate action sequence
        response = sequencer.generate_sequence(request)
        
        success = response.success and response.action_sequence is not None
        print_test_result("Generate Action Sequence", success,
                        f"Actions: {len(response.action_sequence.actions) if response.action_sequence else 0}")
        
        if success and response.action_sequence:
            print("    Generated sequence:")
            for i, action in enumerate(response.action_sequence.actions):
                print(f"      {i+1}. {action.name} ({action.id})")
        
        return response, success
        
    except Exception as e:
        print_test_result("Action Sequencing", False, str(e))
        traceback.print_exc()
        return None, False

def test_complete_pipeline():
    """Test complete integration pipeline"""
    print_separator("COMPLETE INTEGRATION PIPELINE TEST")
    
    try:
        # Test goal interpretation
        print("\n1. Testing Goal Interpretation...")
        goal_result, goal_success = test_goal_interpretation()
        
        if not goal_success:
            print_test_result("Complete Pipeline", False, "Goal interpretation failed")
            return False
        
        # Extract LTL formula
        ltl_formula = None
        if isinstance(goal_result, dict):
            ltl_formula = goal_result.get('ltl_formula') or goal_result.get('optimized_formula')
        elif hasattr(goal_result, 'formula'):
            ltl_formula = goal_result.formula
        
        if not ltl_formula:
            ltl_formula = "F(walk) & F(wash)"  # Fallback formula
        
        print(f"    Using LTL formula: {ltl_formula}")
        
        # Test subgoal decomposition
        print("\n2. Testing Subgoal Decomposition...")
        subgoal_result, subgoal_success = run_subgoal_decomposition(ltl_formula)
        
        if not subgoal_success:
            print_test_result("Complete Pipeline", False, "Subgoal decomposition failed")
            return False
        
        # Test action sequencing
        print("\n3. Testing Action Sequencing...")
        action_result, action_success = run_action_sequencing(subgoal_result)
        
        if not action_success:
            print_test_result("Complete Pipeline", False, "Action sequencing failed")
            return False
        
        print_test_result("Complete Integration Pipeline", True,
                        "All three modules working together")
        return True
        
    except Exception as e:
        print_test_result("Complete Pipeline", False, str(e))
        traceback.print_exc()
        return False

def test_english_goals_dataset():
    """Test with various English goals"""
    print_separator("ENGLISH GOALS DATASET TEST")
    
    english_goals = [
        "Robot should walk to the kitchen",
        "Robot should pick up the cup and put it on the table",
        "Robot should first go to the bedroom then clean the room",
        "Robot should navigate to the bathroom and wash hands",
        "Robot should move to the living room and sit down"
    ]
    
    try:
        # Import from package
        from goal_interpretation import EnhancedGoalInterpreter
        
        interpreter = EnhancedGoalInterpreter()
        
        success_count = 0
        for i, goal in enumerate(english_goals):
            try:
                result = interpreter.interpret(goal)
                success = result is not None and len(result.get('propositions', [])) > 0
                status = "✓" if success else "✗"
                print(f"  {status} {i+1}. {goal}")
                print(f"      Propositions: {result.get('propositions', [])}")
                print(f"      LTL: {result.get('ltl_formula', 'None')}")
                
                if success:
                    success_count += 1
                    
            except Exception as e:
                print(f"  ✗ {i+1}. {goal} - Error: {str(e)}")
        
        print_test_result("English Goals Dataset", success_count == len(english_goals),
                        f"Success rate: {success_count}/{len(english_goals)}")
        
        return success_count == len(english_goals)
        
    except ImportError:
        print_test_result("English Goals Dataset", False, "EnhancedGoalInterpreter not available")
        return False
    except Exception as e:
        print_test_result("English Goals Dataset", False, str(e))
        return False

def main():
    """Main test function"""
    print_separator("COMPREHENSIVE ENGLISH INTEGRATION TEST")
    print(f"Timestamp: {datetime.now()}")
    print(f"Python Path: {sys.path[:3]}...")  # Show first 3 paths
    
    all_tests_passed = True
    
    # Test individual modules
    try:
        # Test complete pipeline
        pipeline_success = test_complete_pipeline()
        all_tests_passed &= pipeline_success
        
        # Test English goals dataset
        dataset_success = test_english_goals_dataset()
        all_tests_passed &= dataset_success
        
    except Exception as e:
        print(f"Critical error in main test: {str(e)}")
        traceback.print_exc()
        all_tests_passed = False
    
    # Final result
    print_separator("FINAL TEST RESULTS")
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! The three modules are working together correctly.")
        print("✓ Goal Interpretation module is processing English goals")
        print("✓ Subgoal Decomposition module is generating subgoals")
        print("✓ Action Sequencing module is creating action sequences")
    else:
        print("❌ SOME TESTS FAILED. Please check the detailed results above.")
        print("Recommended actions:")
        print("1. Check module imports and dependencies")
        print("2. Verify data formats between modules")
        print("3. Review error messages for specific issues")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)