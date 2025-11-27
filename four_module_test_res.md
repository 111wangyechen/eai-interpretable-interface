python tests/test_four_module_integration.py
✓ All four modules imported successfully
2025-11-27 16:28:30,522 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-27 16:28:30,522 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
================================================================================
Complete Four-Module Integration Test
Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing
================================================================================

1. Testing Module Initialization...
   ✓ Goal Interpretation module initialized
   ✓ Subgoal Decomposition module initialized
   ✓ Transition Modeling module initialized
2025-11-27 16:28:30,544 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   ✓ Action Sequencing module initialized
   ✓ Module initialization: 4/4 modules ready

2. Testing Goal Interpretation to Transition Modeling Flow...
   Processing goal: Put the red ball on the table
   ✓ Goal interpretation completed in 0.001s
   Generated LTL formula: (place_red -> F(furniture_table))
   ✓ 4 subgoals generated: ['Execute atomic action: place_red', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Conditional: place_red -> F(furniture_table)']
2025-11-27 16:28:30,545 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,545 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,545 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,545 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,545 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110545759, creating fallback
2025-11-27 16:28:30,546 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ Goal→Transition flow: 1 sequences generated in 0.000s

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✓ 8 subgoals generated: ['Execute atomic action: move_ball', 'Eventually: move_ball', 'Execute atomic action: locations_kitchen', 'Eventually: locations_kitchen', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Parallel
: F(locations_kitchen) & F(furniture_table)', 'Parallel: F(move_ball) & F(locations_kitchen)&F(furniture_table)']                                                                                                                                          Debug: Processing subgoal 1: Execute atomic action: move_ball
2025-11-27 16:28:30,551 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 1
   Debug: Processing subgoal 2: Eventually: move_ball
2025-11-27 16:28:30,556 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 2
   Debug: Processing subgoal 3: Execute atomic action: locations_kitchen
2025-11-27 16:28:30,561 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 3
   Debug: Processing subgoal 4: Eventually: locations_kitchen
2025-11-27 16:28:30,567 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 4
   Debug: Processing subgoal 5: Execute atomic action: furniture_table
2025-11-27 16:28:30,571 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 5
   Debug: Processing subgoal 6: Eventually: furniture_table
2025-11-27 16:28:30,576 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 6
   Debug: Processing subgoal 7: Parallel: F(locations_kitchen) & F(furniture_table)
2025-11-27 16:28:30,581 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 7
   Debug: Processing subgoal 8: Parallel: F(move_ball) & F(locations_kitchen)&F(furniture_table)
2025-11-27 16:28:30,587 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 8
   ✓ Subgoal→Action flow: 8 subgoals → 8 action sequences

4. Testing End-to-End Workflow...

   Processing scenario: Basic Operation Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 4 subgoals
         Subgoal 1: Execute atomic action: place_red
           - ID: atomic_2
           - LTL: place_red
           - Type: SubgoalType.ATOMIC
         Subgoal 2: Execute atomic action: furniture_table
           - ID: atomic_5
           - LTL: furniture_table
           - Type: SubgoalType.ATOMIC
         Subgoal 3: Eventually: furniture_table
           - ID: temporal_6
           - LTL: F(furniture_table)
           - Type: SubgoalType.TEMPORAL
         Subgoal 4: Conditional: place_red -> F(furniture_table)
           - ID: logical_7
           - LTL: (place_red -> F(furniture_table))
           - Type: SubgoalType.CONDITIONAL
     Step 3: Transition Modeling
       Available transitions count: 4
2025-11-27 16:28:30,589 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,589 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,589 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,589 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,589 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110589642, creating fallback
2025-11-27 16:28:30,590 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
       Available actions: ['move', 'pickup', 'place']
2025-11-27 16:28:30,595 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       ✗ Error in scenario Basic Operation Scenario: Action sequence generation failed

   Processing scenario: Multi-step Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 7 subgoals
         Subgoal 1: Execute atomic action: perform_open
           - ID: atomic_3
           - LTL: perform_open
           - Type: SubgoalType.ATOMIC
         Subgoal 2: Execute atomic action: appliances_refrigerator
           - ID: atomic_6
           - LTL: appliances_refrigerator
           - Type: SubgoalType.ATOMIC
         Subgoal 3: Eventually: appliances_refrigerator
           - ID: temporal_7
           - LTL: F(appliances_refrigerator)
           - Type: SubgoalType.TEMPORAL
         Subgoal 4: Conditional: open -> F(appliances_refrigerator)
           - ID: logical_8
           - LTL: (open -> F(appliances_refrigerator))
           - Type: SubgoalType.CONDITIONAL
         Subgoal 5: Execute atomic action: locations_door
           - ID: atomic_11
           - LTL: locations_door
           - Type: SubgoalType.ATOMIC
         Subgoal 6: Eventually: locations_door
           - ID: temporal_12
           - LTL: F(locations_door))->F(relative_time_then
           - Type: SubgoalType.TEMPORAL
         Subgoal 7: Conditional: (open->F(appliances_refrigerator)) -> F(locations_door))->F(relative_time_then
           - ID: logical_13
           - LTL: ((open->F(appliances_refrigerator)) -> F(locations_door))->F(relative_time_then)
           - Type: SubgoalType.CONDITIONAL
     Step 3: Transition Modeling
       Available transitions count: 4
2025-11-27 16:28:30,598 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,599 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,599 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,599 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,599 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110598903, creating fallback
2025-11-27 16:28:30,599 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
       Available actions: ['move', 'pickup', 'place', 'open_door']
2025-11-27 16:28:30,607 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       ✗ Error in scenario Multi-step Scenario: Action sequence generation failed

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.002s)
     ✓ Subgoal decomposition completed, generated 4 subgoals (0.000s)
2025-11-27 16:28:30,609 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,609 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,609 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,609 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,609 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110609431, creating fallback
2025-11-27 16:28:30,609 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
     ✓ Transition modeling completed, generated 1 sequences (0.001s)
2025-11-27 16:28:30,616 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
     ✗ Multi-Goal Scenario: Failed - Action sequence generation failed
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 7 subgoals (0.000s)
2025-11-27 16:28:30,618 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,618 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,618 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,618 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,618 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110618447, creating fallback
2025-11-27 16:28:30,618 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
2025-11-27 16:28:30,625 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
     ✗ Conditional Constraint Scenario: Failed - Action sequence generation failed
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 10 subgoals (0.000s)
2025-11-27 16:28:30,627 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,627 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,627 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,627 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,627 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110627154, creating fallback
2025-11-27 16:28:30,627 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
     ✓ Transition modeling completed, generated 1 sequences (0.001s)
2025-11-27 16:28:30,635 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
     ✗ Sequential Constraint Scenario: Failed - Action sequence generation failed
   ✗ Complex scenarios: 0/3 successful

6. Testing Performance and Stability...
   Preheating system...
   Running 10 performance test iterations...
     Iteration 1/10: Testing low complexity goal
2025-11-27 16:28:30,636 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,637 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,637 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,637 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,637 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110636876, creating fallback
2025-11-27 16:28:30,637 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,640 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 1 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 20.0%
     Iteration 2/10: Testing medium complexity goal
2025-11-27 16:28:30,641 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,642 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,642 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,642 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,642 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110641958, creating fallback
2025-11-27 16:28:30,642 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,647 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 2 metrics:
         - Total time: 0.007s
         - Response time: 0.007s
         - Success rate: 100.0%
         - Estimated cache hit rate: 30.0%
     Iteration 3/10: Testing low complexity goal
2025-11-27 16:28:30,648 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,649 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,649 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,649 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,649 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110648908, creating fallback
2025-11-27 16:28:30,649 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,653 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 3 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 40.0%
     Iteration 4/10: Testing medium complexity goal
2025-11-27 16:28:30,654 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,654 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,654 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,654 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,654 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110654123, creating fallback
2025-11-27 16:28:30,654 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,659 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 4 metrics:
         - Total time: 0.006s
         - Response time: 0.006s
         - Success rate: 100.0%
         - Estimated cache hit rate: 65.0%
     Iteration 5/10: Testing low complexity goal
2025-11-27 16:28:30,660 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,660 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,660 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,660 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,660 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110660406, creating fallback
2025-11-27 16:28:30,660 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,665 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 5 metrics:
         - Total time: 0.006s
         - Response time: 0.006s
         - Success rate: 100.0%
         - Estimated cache hit rate: 70.0%
     Iteration 6/10: Testing medium complexity goal
2025-11-27 16:28:30,666 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,666 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,666 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,666 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,667 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110666770, creating fallback
2025-11-27 16:28:30,667 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,671 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 6 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 75.0%
     Iteration 7/10: Testing low complexity goal
2025-11-27 16:28:30,672 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,672 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,672 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,672 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,672 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110672165, creating fallback
2025-11-27 16:28:30,672 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,676 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 7 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 80.0%
     Iteration 8/10: Testing medium complexity goal
2025-11-27 16:28:30,677 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,677 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,677 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,677 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,677 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110677339, creating fallback
2025-11-27 16:28:30,677 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,681 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 8 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 85.0%
     Iteration 9/10: Testing low complexity goal
2025-11-27 16:28:30,682 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,682 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,682 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,682 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,682 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110682464, creating fallback
2025-11-27 16:28:30,682 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,686 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 9 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
     Iteration 10/10: Testing medium complexity goal
2025-11-27 16:28:30,687 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-27 16:28:30,687 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-27 16:28:30,687 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-27 16:28:30,687 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-27 16:28:30,687 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764232110687571, creating fallback
2025-11-27 16:28:30,687 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-11-27 16:28:30,692 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
       Iteration 10 metrics:
         - Total time: 0.006s
         - Response time: 0.006s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
   ✓ Performance: avg workflow time 0.01s, p95 response time 0.01s, success rate 100.0%, cache hit rate 64.5%
   Performance criteria met: 4/4
     - Time criteria: ✓ (avg < 3s)
     - P95 response time: ✓ (< 5s)
     - Success rate: ✓ (> 90%)
     - Cache hit rate: ✓ (> 50%)

7. Testing Error Handling and Recovery...
2025-11-27 16:28:30,694 - transition_modeling.transition_modeler - INFO - Processing modeling request with 0 available transitions
2025-11-27 16:28:30,694 - transition_modeling.transition_modeler - WARNING - No available transitions provided in request request_1764232110694011
2025-11-27 16:28:30,694 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ Error handling: 4 error cases tested

================================================================================
INTEGRATION TEST REPORT
================================================================================
Total Tests: 7
Successful Tests: 4
Success Rate: 57.1%
Total Time: 0.17 seconds

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
  "goal_interpretation_time": 0.0007238388061523438,
  "subgoal_decomposition_time": 0.00017499923706054688,
  "modeling_time": 0.0003230571746826172,
  "total_time": 0.0012218952178955078
}

3. subgoal_to_action_flow: ✓ PASS
   Message: Subgoal→Action flow: 8 subgoals → 8 action sequences
   Details: {
  "subgoals_count": 8,
  "action_sequences_count": 8,
  "subgoals": [
    "Execute atomic action: move_ball",
    "Eventually: move_ball",
    "Execute atomic action: locations_kitchen",
    "Eventually: locations_kitchen",
    "Execute atomic action: furniture_table",
    "Eventually: furniture_table",
    "Parallel: F(locations_kitchen) & F(furniture_table)",
    "Parallel: F(move_ball) & F(locations_kitchen)&F(furniture_table)"
  ],
  "action_sequences": [
    [],
    [],
    []
  ]
}

4. end_to_end_workflow: ✗ FAIL
   Message: End-to-End workflow: 0/2 scenarios successful (0.0%) in 0.02s
   Details: {
  "total_scenarios": 2,
  "successful_scenarios": 0,
  "success_rate": 0.0,
  "workflow_time": 0.019547462463378906,
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
          "time": 0.001298666000366211,
          "result": "{'original_text': 'Put the red ball on the table', 'parse_result': {'original_text': 'put the red ball on the table', 'language': 'en', 'task_complexity': 'simple', 'semantic_structure': {'main_clause': '', 'subordinate_clauses
': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'temporal_info': [], 'conditions': [], 'constraints': [], 'propositions': ['place_red', 'furniture_table'], 'structure': 'simple', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'put', 'modified': 'the', 'position': 0}, {'type': 'adjective', 'modifier': 'ball', 'modified': 'on', 'position': 12}]}, 'ltl_formula': '(place_red -> F(furniture_table))', 'optimized_formula': '(place_red ->Ffurniture_table)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': ['发现 2 个未映射实体'], 'suggestions': [], 'entity_issues': ['未映射的实体: place_red', '未映射的实体: furniture_table'], 'temporal_checks': {'operators_used': [' ', 'F'], 'has_f_operator': True}}, 'structure': 'simple', 'task_complexity': 'simple', 'language': 'en', 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'conditions': [], 'constraints': [], 'temporal_info': [], 'propositions': ['place_red', 'furniture_table'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-27T16:28:30.588957', 'proposition_count': 2, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"                                                                                                                                         },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0003485679626464844
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0005803108215332031
        },
        "action_sequencing": {
          "success": false,
          "time": 0.005803346633911133
        }
      },
      "subgoals_count": 4,
      "subgoals_details": [
        {
          "id": "atomic_2",
          "description": "Execute atomic action: place_red",
          "ltl_formula": "place_red",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "atomic_5",
          "description": "Execute atomic action: furniture_table",
          "ltl_formula": "furniture_table",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "temporal_6",
          "description": "Eventually: furniture_table",
          "ltl_formula": "F(furniture_table)",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_5"
          ]
        },
        {
          "id": "logical_7",
          "description": "Conditional: place_red -> F(furniture_table)",
          "ltl_formula": "(place_red -> F(furniture_table))",
          "type": "CONDITIONAL",
          "dependencies": [
            "atomic_2",
            "temporal_6"
          ]
        }
      ],
      "sequences_count": 1,
      "sequences_info": [
        {
          "index": 0,
          "length": 0
        }
      ],
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
          "time": 0.0013608932495117188,
          "result": "{'original_text': 'Walk to the refrigerator first, then open the refrigerator door', 'parse_result': {'original_text': 'walk to the refrigerator first ,  then open the refrigerator door', 'language': 'en', 'task_complexity': 'c
omplex', 'semantic_structure': {'main_clause': '', 'subordinate_clauses': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'conditions': [], 'constraints': [], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'structure': 'sequential', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'walk', 'modified': 'to', 'position': 0}, {'type': 'adjective', 'modifier': 'then', 'modified': 'open', 'position': 34}]}, 'ltl_formula': '(((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))', 'optimized_formula': '(((open ->Fappliances_refrigerator)->Flocations_door)->Frelative_time_then)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': ['发现 3 个未映射实体'], 'suggestions': [], 'entity_issues': ['未映射的实体: appliances_refrigerator', '未映射的实体: locations_door', '未映射的实体: relative_time_then'], 'temporal_checks': {'operators_used': [' ', 'F'], 'has_f_operator': True}}, 'structure': 'sequential', 'task_complexity': 'complex', 'language': 'en', 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'conditions': [], 'constraints': [], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-27T16:28:30.597358', 'proposition_count': 4, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"                                                                                                                                                                                                                                  },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0007605552673339844
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0008313655853271484
        },
        "action_sequencing": {
          "success": false,
          "time": 0.00787353515625
        }
      },
      "subgoals_count": 7,
      "subgoals_details": [
        {
          "id": "atomic_3",
          "description": "Execute atomic action: perform_open",
          "ltl_formula": "perform_open",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "atomic_6",
          "description": "Execute atomic action: appliances_refrigerator",
          "ltl_formula": "appliances_refrigerator",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "temporal_7",
          "description": "Eventually: appliances_refrigerator",
          "ltl_formula": "F(appliances_refrigerator)",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_6"
          ]
        },
        {
          "id": "logical_8",
          "description": "Conditional: open -> F(appliances_refrigerator)",
          "ltl_formula": "(open -> F(appliances_refrigerator))",
          "type": "CONDITIONAL",
          "dependencies": [
            "atomic_3",
            "temporal_7"
          ]
        },
        {
          "id": "atomic_11",
          "description": "Execute atomic action: locations_door",
          "ltl_formula": "locations_door",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "temporal_12",
          "description": "Eventually: locations_door",
          "ltl_formula": "F(locations_door))->F(relative_time_then",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_11"
          ]
        },
        {
          "id": "logical_13",
          "description": "Conditional: (open->F(appliances_refrigerator)) -> F(locations_door))->F(relative_time_then",
          "ltl_formula": "((open->F(appliances_refrigerator)) -> F(locations_door))->F(relative_time_then)",
          "type": "CONDITIONAL",
          "dependencies": [
            "logical_8",
            "temporal_12"
          ]
        }
      ],
      "sequences_count": 1,
      "sequences_info": [
        {
          "index": 0,
          "length": 0
        }
      ],
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
          "time": 0.0016486644744873047
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0003504753112792969
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0005278587341308594
        },
        "action_sequencing": {
          "success": false,
          "time": 0.007153511047363281
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
          "time": 0.001031637191772461
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0002772808074951172
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0003070831298828125
        },
        "action_sequencing": {
          "success": false,
          "time": 0.006645679473876953
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
          "time": 0.0011665821075439453
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0004551410675048828
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0005524158477783203
        },
        "action_sequencing": {
          "success": false,
          "time": 0.0076770782470703125
        }
      },
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    }
  ]
}

6. performance_and_stability: ✓ PASS
   Message: Performance: avg workflow time 0.01s, p95 response time 0.01s, success rate 100.0%, cache hit rate 64.5%
   Details: {
  "iterations": 10,
  "average_times": {
    "goal_interpretation": 0.0005493402481079101,
    "subgoal_decomposition": 0.0002132415771484375,
    "transition_modeling": 0.0003851652145385742,
    "action_sequencing": 0.004497075080871582,
    "total_workflow": 0.005649089813232422,
    "p95_response_time": 0.006940603256225586
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

⚠️  Could not save report file: Object of type SubgoalType is not JSON serializable

⚠️  Four-module integration test completed with issues.
