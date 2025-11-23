(eai-eval) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface/tests$ python test_four_module_integration.py 
✓ All four modules imported successfully
2025-11-23 10:18:09,825 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 10:18:09,826 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
================================================================================
Complete Four-Module Integration Test
Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing
================================================================================

1. Testing Module Initialization...
   ✓ Goal Interpretation module initialized
   ✓ Subgoal Decomposition module initialized
   ✓ Transition Modeling module initialized
2025-11-23 10:18:09,829 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
   ✓ Action Sequencing module initialized
   ✓ Module initialization: 4/4 modules ready

2. Testing Goal Interpretation to Transition Modeling Flow...
   Processing goal: Put the red ball on the table
   ✓ Goal interpretation completed in 0.000s
   ✓ 1 subgoals generated: ['Execute atomic action: perform_put']
2025-11-23 10:18:09,829 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,830 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,830 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,830 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,830 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289829771, creating fallback
2025-11-23 10:18:09,830 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289829771 failed LTL validation
2025-11-23 10:18:09,830 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
   ✗ Transition modeling failed or returned unsuccessful response
   ✗ Goal→Transition flow: 0 sequences generated in 0.001s

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✓ 1 subgoals generated: ['Execute atomic action: move_red']
   Debug: Processing subgoal 1: Execute atomic action: move_red
2025-11-23 10:18:09,830 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
   Debug: Failed to generate action sequence for subgoal 1
   ✓ Subgoal→Action flow: 1 subgoals → 1 action sequences

4. Testing End-to-End Workflow...

   Processing scenario: Basic Operation Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 1 subgoals
         Subgoal 1: Execute atomic action: perform_put
           - ID: atomic_1
           - LTL: perform_put
           - Type: SubgoalType.ATOMIC
     Step 3: Transition Modeling
       Available transitions count: 4
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,831 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,831 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289831036, creating fallback
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289831036 failed LTL validation
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
       ✗ Error in scenario Basic Operation Scenario: Transition modeling failed

   Processing scenario: Multi-step Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 1 subgoals
         Subgoal 1: Execute atomic action: walk_to
           - ID: atomic_1
           - LTL: walk_to
           - Type: SubgoalType.ATOMIC
     Step 3: Transition Modeling
       Available transitions count: 4
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,831 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,831 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289831479, creating fallback
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289831479 failed LTL validation
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
       ✗ Error in scenario Multi-step Scenario: Transition modeling failed

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.000s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,831 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,831 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,831 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289831869, creating fallback
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289831869 failed LTL validation
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
     ✗ Multi-Goal Scenario: Failed - Transition modeling failed
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.000s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,832 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,832 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289832250, creating fallback
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289832250 failed LTL validation
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
     ✗ Conditional Constraint Scenario: Failed - Transition modeling failed
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.000s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,832 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,832 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289832628, creating fallback
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289832628 failed LTL validation
2025-11-23 10:18:09,832 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
     ✗ Sequential Constraint Scenario: Failed - Transition modeling failed
   ✗ Complex scenarios: 0/3 successful

6. Testing Performance and Stability...
   Preheating system...
   Running 10 performance test iterations...
     Iteration 1/10: Testing low complexity goal
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,833 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,833 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289833120, creating fallback
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289833120 failed LTL validation
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,833 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 1 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 20.0%
     Iteration 2/10: Testing medium complexity goal
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,833 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,833 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289833679, creating fallback
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289833679 failed LTL validation
2025-11-23 10:18:09,833 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,833 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 2 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 30.0%
     Iteration 3/10: Testing low complexity goal
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,834 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,834 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289834123, creating fallback
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289834123 failed LTL validation
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,834 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 3 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 40.0%
     Iteration 4/10: Testing medium complexity goal
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,834 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,834 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289834595, creating fallback
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289834595 failed LTL validation
2025-11-23 10:18:09,834 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,834 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 4 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 65.0%
     Iteration 5/10: Testing low complexity goal
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,835 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,835 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289835002, creating fallback
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289835002 failed LTL validation
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,835 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 5 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 70.0%
     Iteration 6/10: Testing medium complexity goal
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,835 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,835 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289835430, creating fallback
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289835430 failed LTL validation
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,835 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 6 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 75.0%
     Iteration 7/10: Testing low complexity goal
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,835 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,835 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289835829, creating fallback
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289835829 failed LTL validation
2025-11-23 10:18:09,835 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,836 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 7 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 80.0%
     Iteration 8/10: Testing medium complexity goal
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,836 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,836 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289836224, creating fallback
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289836224 failed LTL validation
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,836 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 8 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 85.0%
     Iteration 9/10: Testing low complexity goal
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,836 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,836 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289836588, creating fallback
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289836588 failed LTL validation
2025-11-23 10:18:09,836 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,836 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
       Iteration 9 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
     Iteration 10/10: Testing medium complexity goal
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 10:18:09,837 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 10:18:09,837 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763864289837018, creating fallback
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763864289837018 failed LTL validation
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
2025-11-23 10:18:09,837 - action_sequencing.action_sequencer - ERROR - Error generating action sequence: 'list' object has no attribute 'items'
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
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - INFO - Processing modeling request with 0 available transitions
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - WARNING - No available transitions provided in request request_1763864289837484
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - WARNING - Sequence empty_sequence_request_1763864289837484 failed LTL validation
2025-11-23 10:18:09,837 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
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

2. goal_to_transition_flow: ✗ FAIL
   Message: Goal→Transition flow: 0 sequences generated in 0.001s
   Details: {
  "goal_interpretation_success": true,
  "subgoal_decomposition_success": true,
  "transition_modeling_success": false,
  "sequences_generated": 0,
  "goal_interpretation_time": 0.00010967254638671875,
  "subgoal_decomposition_time": 2.1696090698242188e-05,
  "modeling_time": 0.0007278919219970703,
  "total_time": 0.0008592605590820312
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
  "workflow_time": 0.0008983612060546875,
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
          "time": 0.000133514404296875,
          "result": "put_the"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 2.0742416381835938e-05
        },
        "transition_modeling": {
          "success": false,
          "time": 0.0002465248107910156
        }
      },
      "subgoals_count": 1,
      "subgoals_details": [
        {
          "id": "atomic_1",
          "description": "Execute atomic action: perform_put",
          "ltl_formula": "perform_put",
          "type": "ATOMIC",
          "dependencies": []
        }
      ],
      "success": false,
      "error": "Transition modeling failed",
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
          "time": 0.0001068115234375,
          "result": "walk_to"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.430511474609375e-05
        },
        "transition_modeling": {
          "success": false,
          "time": 0.00022292137145996094
        }
      },
      "subgoals_count": 1,
      "subgoals_details": [
        {
          "id": "atomic_1",
          "description": "Execute atomic action: walk_to",
          "ltl_formula": "walk_to",
          "type": "ATOMIC",
          "dependencies": []
        }
      ],
      "success": false,
      "error": "Transition modeling failed",
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
          "time": 9.369850158691406e-05
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.4066696166992188e-05
        },
        "transition_modeling": {
          "success": false,
          "time": 0.00021338462829589844
        }
      },
      "success": false,
      "error": "Transition modeling failed",
      "exception_type": "Exception"
    },
    {
      "name": "Conditional Constraint Scenario",
      "goal": "If the room has light, pick up the red ball; otherwise, turn on the light first, then pick up the ball",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.00011277198791503906
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.6689300537109375e-05
        },
        "transition_modeling": {
          "success": false,
          "time": 0.00022077560424804688
        }
      },
      "success": false,
      "error": "Transition modeling failed",
      "exception_type": "Exception"
    },
    {
      "name": "Sequential Constraint Scenario",
      "goal": "First open the computer, then check email, finally close the computer",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.00011444091796875
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 1.33514404296875e-05
        },
        "transition_modeling": {
          "success": false,
          "time": 0.00022268295288085938
        }
      },
      "success": false,
      "error": "Transition modeling failed",
      "exception_type": "Exception"
    }
  ]
}

6. performance_and_stability: ✓ PASS
   Message: Performance: avg workflow time 0.00s, p95 response time 0.00s, success rate 100.0%, cache hit rate 64.5%
   Details: {
  "iterations": 10,
  "average_times": {
    "goal_interpretation": 8.52346420288086e-05,
    "subgoal_decomposition": 2.353191375732422e-05,
    "transition_modeling": 0.00019474029541015624,
    "action_sequencing": 9.179115295410156e-05,
    "total_workflow": 0.00039751529693603515,
    "p95_response_time": 0.0005095005035400391
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

7. error_handling_and_recovery: ✓ PASS
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
      true
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

⚠️  Could not save report file: Object of type SubgoalType is not JSON serializable

⚠️  Four-module integration test completed with issues.