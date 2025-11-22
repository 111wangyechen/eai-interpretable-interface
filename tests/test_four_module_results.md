(eai-eval) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface/tests$ python test_four_module_integration.py 
✓ All four modules imported successfully
2025-11-22 18:01:10,764 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-22 18:01:10,764 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
================================================================================
Complete Four-Module Integration Test
Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing
================================================================================

1. Testing Module Initialization...
   ✓ Goal Interpretation module initialized
   ✓ Subgoal Decomposition module initialized
   ✓ Transition Modeling module initialized
2025-11-22 18:01:10,767 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
   ✓ Action Sequencing module initialized
   ✓ Module initialization: 4/4 modules ready

2. Testing Goal Interpretation to Transition Modeling Flow...
   Processing goal: Put the red ball on the table
   ✓ Goal interpretation completed in 0.000s
   ✓ 1 subgoals generated: ['Execute atomic action: put_the']
2025-11-22 18:01:10,767 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,767 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,767 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,767 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,767 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670767627, creating fallback
2025-11-22 18:01:10,767 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670767627: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,767 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ Goal→Transition flow: 1 sequences generated in 0.000s

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✓ 1 subgoals generated: ['Execute atomic action: move_red']
   Debug: Processing subgoal 1: Execute atomic action: move_red
2025-11-22 18:01:10,768 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
   Debug: Failed to generate action sequence for subgoal 1
   ✓ Subgoal→Action flow: 1 subgoals → 1 action sequences

4. Testing End-to-End Workflow...

   Processing scenario: Basic Operation Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 1 subgoals
     Step 3: Transition Modeling
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,768 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,768 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670768268, creating fallback
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670768268: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
2025-11-22 18:01:10,768 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       ✗ Error in scenario Basic Operation Scenario: Action sequence generation failed

   Processing scenario: Multi-step Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 1 subgoals
     Step 3: Transition Modeling
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,768 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,768 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670768727, creating fallback
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670768727: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,768 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
2025-11-22 18:01:10,769 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       ✗ Error in scenario Multi-step Scenario: Action sequence generation failed

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.000s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
2025-11-22 18:01:10,769 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,769 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,769 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,769 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,769 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670769648, creating fallback
2025-11-22 18:01:10,769 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670769648: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,769 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
2025-11-22 18:01:10,770 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
     ✗ Multi-Goal Scenario: Failed - Action sequence generation failed
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.000s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,770 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,770 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670770261, creating fallback
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670770261: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
2025-11-22 18:01:10,770 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
     ✗ Conditional Constraint Scenario: Failed - Action sequence generation failed
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.000s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,770 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,770 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670770768, creating fallback
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670770768: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,770 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
2025-11-22 18:01:10,771 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
     ✗ Sequential Constraint Scenario: Failed - Action sequence generation failed
   ✗ Complex scenarios: 0/3 successful

6. Testing Performance and Stability...
   Preheating system...
   Running 10 performance test iterations...
     Iteration 1/10: Testing low complexity goal
2025-11-22 18:01:10,771 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,771 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,771 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,771 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,771 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670771454, creating fallback
2025-11-22 18:01:10,771 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670771454: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,771 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,771 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 1 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 20.0%
     Iteration 2/10: Testing medium complexity goal
2025-11-22 18:01:10,771 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,772 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,772 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670771957, creating fallback
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670771957: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,772 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 2 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 30.0%
     Iteration 3/10: Testing low complexity goal
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,772 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,772 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670772488, creating fallback
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670772488: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,772 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 3 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 40.0%
     Iteration 4/10: Testing medium complexity goal
2025-11-22 18:01:10,772 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,772 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,773 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670772929, creating fallback
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670772929: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,773 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 4 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 65.0%
     Iteration 5/10: Testing low complexity goal
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,773 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,773 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670773383, creating fallback
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670773383: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,773 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 5 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 70.0%
     Iteration 6/10: Testing medium complexity goal
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,773 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,773 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,773 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670773875, creating fallback
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670773875: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,774 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 6 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 75.0%
     Iteration 7/10: Testing low complexity goal
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,774 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,774 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670774342, creating fallback
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670774342: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,774 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 7 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 80.0%
     Iteration 8/10: Testing medium complexity goal
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,774 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,774 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,774 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670774840, creating fallback
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670774840: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,775 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 8 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 85.0%
     Iteration 9/10: Testing low complexity goal
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,775 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,775 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670775371, creating fallback
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670775371: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,775 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 9 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
     Iteration 10/10: Testing medium complexity goal
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-22 18:01:10,775 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-22 18:01:10,775 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763805670775749, creating fallback
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_fallback_sequence_request_1763805670775749: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,775 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-22 18:01:10,776 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 10 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
   ✓ Performance: avg workflow time 0.00s, p95 response time 0.00s, success rate 100.0%, cache hit rate 64.5%
   Performance criteria met: 4/4
     - Time criteria: ✓ (avg < 3s)
     - P95 response time: ✓ (< 5s)
     - Success rate: ✓ (> 90%)
     - Cache hit rate: ✓ (> 50%)

7. Testing Error Handling and Recovery...
2025-11-22 18:01:10,776 - transition_modeling.transition_modeler - INFO - Processing modeling request with 0 available transitions
2025-11-22 18:01:10,776 - transition_modeling.transition_modeler - WARNING - No available transitions provided in request request_1763805670776241
2025-11-22 18:01:10,776 - transition_modeling.transition_modeler - WARNING - Error during LogicGuard processing for sequence empty_sequence_request_1763805670776241: 'LogicGuard' object has no attribute 'validate_ltl_specifications'
2025-11-22 18:01:10,776 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ Error handling: 4 error cases tested

================================================================================
INTEGRATION TEST REPORT
================================================================================
Total Tests: 7
Successful Tests: 4
Success Rate: 57.1%
Total Time: 0.01 seconds

1. module_initialization: ✓ PASS
   Message: Module initialization: 4/4 modules ready
   Details: {
  "goal_interpretation": true,
  "subgoal_decomposition": true,
  "transition_modeling": true,
  "action_sequencing": true
}

2. goal_to_transition_flow: ✓ PASS
   Message: Goal→Transition flow: 1 sequences generated in 0.000s
   Details: {
  "goal_interpretation_success": true,
  "subgoal_decomposition_success": true,
  "transition_modeling_success": true,
  "sequences_generated": 1,
  "goal_interpretation_time": 0.00010251998901367188,
  "subgoal_decomposition_time": 1.71661376953125e-05,
  "modeling_time": 0.00019860267639160156,
  "total_time": 0.00031828880310058594
}

3. subgoal_to_action_flow: ✓ PASS
   Message: Subgoal→Action flow: 1 subgoals → 1 action sequences
   Details: {
  "subgoals_count": 1,
  "action_sequences_count": 1,
  "subgoals": [
    "Execute atomic action: move_red"
  ],
  "action_sequences": [
    []
  ]
}

4. end_to_end_workflow: ✗ FAIL
   Message: End-to-End workflow: 0/2 scenarios successful (0.0%) in 0.00s
   Details: {
  "total_scenarios": 2,
  "successful_scenarios": 0,
  "success_rate": 0.0,
  "workflow_time": 0.0013396739959716797,
  "scenario_results": [
    {
      "name": "Basic Operation Scenario",
      "goal": "Put the red ball on the table",
      "initial_state": {
        "at_location": "start",
        "has_ball": false
      },
      "goal_state": {
        "at_location": "table",
        "has_ball": true
      },
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 8.487701416015625e-05,
          "result": "put_the"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.33514404296875e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0002002716064453125
        },
        "action_sequencing": {
          "success": false,
          "time": 0.0001125335693359375
        }
      },
      "subgoals_count": 1,
      "sequences_count": 1,
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    },
    {
      "name": "Multi-step Scenario",
      "goal": "Walk to the refrigerator first, then open the refrigerator door",
      "initial_state": {
        "at_location": "living_room",
        "fridge_door_open": false
      },
      "goal_state": {
        "at_location": "fridge",
        "fridge_door_open": true
      },
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 9.799003601074219e-05,
          "result": "walk_to"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.2636184692382812e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0002262592315673828
        },
        "action_sequencing": {
          "success": false,
          "time": 0.0002014636993408203
        }
      },
      "subgoals_count": 1,
      "sequences_count": 1,
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    }
  ]
}

5. complex_scenarios: ✗ FAIL
   Message: Complex scenarios: 0/3 successful
   Details: {
  "total_scenarios": 3,
  "successful_scenarios": 0,
  "scenario_results": [
    {
      "name": "Multi-Goal Scenario",
      "goal": "Put both the red ball and blue ball on the table",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.00011563301086425781
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.9550323486328125e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00029850006103515625
        },
        "action_sequencing": {
          "success": false,
          "time": 0.00014543533325195312
        }
      },
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    },
    {
      "name": "Conditional Constraint Scenario",
      "goal": "If the room has light, pick up the red ball; otherwise, turn on the light first, then pick up the ball",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.0001239776611328125
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.3828277587890625e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00024247169494628906
        },
        "action_sequencing": {
          "success": false,
          "time": 0.00012135505676269531
        }
      },
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    },
    {
      "name": "Sequential Constraint Scenario",
      "goal": "First open the computer, then check email, finally close the computer",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 9.250640869140625e-05
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.2874603271484375e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00023818016052246094
        },
        "action_sequencing": {
          "success": false,
          "time": 0.00012111663818359375
        }
      },
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    }
  ]
}

6. performance_and_stability: ✓ PASS
   Message: Performance: avg workflow time 0.00s, p95 response time 0.00s, success rate 100.0%, cache hit rate 64.5%
   Details: {
  "iterations": 10,
  "average_times": {
    "goal_interpretation": 9.121894836425782e-05,
    "subgoal_decomposition": 2.1886825561523437e-05,
    "transition_modeling": 0.00022420883178710937,
    "action_sequencing": 0.00010395050048828125,
    "total_workflow": 0.0004448413848876953,
    "p95_response_time": 0.0005381107330322266
  },
  "performance_criteria": {
    "time_criteria": true,
    "p95_criteria": true,
    "success_criteria": true,
    "cache_criteria": true,
    "criteria_met": 4
  },
  "cache_performance": {
    "avg_hit_rate": 0.6449999999999999
  },
  "stability": {
    "avg_success_rate": 1.0
  }
}

7. error_handling_and_recovery: ✗ FAIL
   Message: Error handling: 4 error cases tested
   Details: {
  "error_cases": [
    [
      "empty_goal",
      true
    ],
    [
      "invalid_context",
      true
    ],
    [
      "invalid_states",
      false
    ],
    [
      "invalid_actions",
      true
    ]
  ]
}

MODULE STATUS SUMMARY:
==================================================
Goal Interpretation      : ✓ Working
Subgoal Decomposition    : ✓ Working
Transition Modeling      : ✓ Working
Action Sequencing        : ✓ Working

INTEGRATION STATUS:
⚠️  FAIR: Partial integration, some modules need attention

📄 Detailed report saved to: four_module_integration_test_results.json

⚠️  Four-module integration test completed with issues.