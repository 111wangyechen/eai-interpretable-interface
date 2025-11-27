python tests/test_four_module_integration.py
✓ All four modules imported successfully
2025-11-27 09:09:31,333 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-27 09:09:31,333 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
================================================================================
Complete Four-Module Integration Test
Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing
================================================================================

1. Testing Module Initialization...
   ✓ Goal Interpretation module initialized
   ✓ Subgoal Decomposition module initialized
   ✗ Transition Modeling module failed: name 'defaultdict' is not defined
2025-11-27 09:09:31,387 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   ✓ Action Sequencing module initialized
   ✓ Module initialization: 3/4 modules ready

2. Testing Goal Interpretation to Transition Modeling Flow...
   Processing goal: Put the red ball on the table
   ✓ Goal interpretation completed in 0.001s
   ✓ 4 subgoals generated: ['Execute atomic action: (red_put', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Conditional: (red_put -> F(furniture_table))']
   ✗ Goal to transition flow test failed: name 'defaultdict' is not defined

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✓ 7 subgoals generated: ['Execute atomic action: ball_move', 'Eventually: ball_move', 'Execute atomic action: locations_kitchen', 'Eventually: locations_kitchen', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Parallel: F(ball_move) 
& F(locations_kitchen) & F(furniture_table)']                                                                                                                                                                                                                             Debug: Processing subgoal 1: Execute atomic action: ball_move
2025-11-27 09:09:31,393 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 1
   Debug: Processing subgoal 2: Eventually: ball_move
2025-11-27 09:09:31,397 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 2
   Debug: Processing subgoal 3: Execute atomic action: locations_kitchen
2025-11-27 09:09:31,400 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 3
   Debug: Processing subgoal 4: Eventually: locations_kitchen
2025-11-27 09:09:31,404 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 4
   Debug: Processing subgoal 5: Execute atomic action: furniture_table
2025-11-27 09:09:31,408 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 5
   Debug: Processing subgoal 6: Eventually: furniture_table
2025-11-27 09:09:31,412 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 6
   Debug: Processing subgoal 7: Parallel: F(ball_move) & F(locations_kitchen) & F(furniture_table)
2025-11-27 09:09:31,416 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   Debug: Failed to generate action sequence for subgoal 7
   ✓ Subgoal→Action flow: 7 subgoals → 7 action sequences

4. Testing End-to-End Workflow...

   Processing scenario: Basic Operation Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 4 subgoals
         Subgoal 1: Execute atomic action: (red_put
           - ID: atomic_2
           - LTL: (red_put
           - Type: SubgoalType.ATOMIC
         Subgoal 2: Execute atomic action: furniture_table
           - ID: atomic_5
           - LTL: furniture_table
           - Type: SubgoalType.ATOMIC
         Subgoal 3: Eventually: furniture_table
           - ID: temporal_6
           - LTL: F(furniture_table))
           - Type: SubgoalType.TEMPORAL
         Subgoal 4: Conditional: (red_put -> F(furniture_table))
           - ID: logical_7
           - LTL: (red_put->F(furniture_table))
           - Type: SubgoalType.CONDITIONAL
     Step 3: Transition Modeling
       ✗ Error in scenario Basic Operation Scenario: name 'defaultdict' is not defined

   Processing scenario: Multi-step Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 8 subgoals
         Subgoal 1: Execute atomic action: perform_(((open
           - ID: atomic_2
           - LTL: perform_(((open
           - Type: SubgoalType.ATOMIC
         Subgoal 2: Execute atomic action: appliances_refrigerator
           - ID: atomic_5
           - LTL: appliances_refrigerator
           - Type: SubgoalType.ATOMIC
         Subgoal 3: Eventually: appliances_refrigerator
           - ID: temporal_6
           - LTL: F(appliances_refrigerator))
           - Type: SubgoalType.TEMPORAL
         Subgoal 4: Execute atomic action: locations_door
           - ID: atomic_9
           - LTL: locations_door
           - Type: SubgoalType.ATOMIC
         Subgoal 5: Eventually: locations_door
           - ID: temporal_10
           - LTL: F(locations_door))
           - Type: SubgoalType.TEMPORAL
         Subgoal 6: Execute atomic action: relative_time_then
           - ID: atomic_13
           - LTL: relative_time_then
           - Type: SubgoalType.ATOMIC
         Subgoal 7: Eventually: relative_time_then
           - ID: temporal_14
           - LTL: F(relative_time_then))
           - Type: SubgoalType.TEMPORAL
         Subgoal 8: Conditional: (((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))
           - ID: logical_15
           - LTL: (((open->F(appliances_refrigerator))->F(locations_door))->F(relative_time_then))
           - Type: SubgoalType.CONDITIONAL
     Step 3: Transition Modeling
       ✗ Error in scenario Multi-step Scenario: name 'defaultdict' is not defined

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 4 subgoals (0.000s)
     ✗ Multi-Goal Scenario: Failed - name 'defaultdict' is not defined
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 8 subgoals (0.000s)
     ✗ Conditional Constraint Scenario: Failed - name 'defaultdict' is not defined
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 14 subgoals (0.000s)
     ✗ Sequential Constraint Scenario: Failed - name 'defaultdict' is not defined
   ✗ Complex scenarios: 0/3 successful

6. Testing Performance and Stability...
   Preheating system...
   Running 10 performance test iterations...
     Iteration 1/10: Testing low complexity goal
       Error in iteration 1: name 'defaultdict' is not defined
       Iteration 1 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 20.0%
     Iteration 2/10: Testing medium complexity goal
       Error in iteration 2: name 'defaultdict' is not defined
       Iteration 2 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 30.0%
     Iteration 3/10: Testing low complexity goal
       Error in iteration 3: name 'defaultdict' is not defined
       Iteration 3 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 40.0%
     Iteration 4/10: Testing medium complexity goal
       Error in iteration 4: name 'defaultdict' is not defined
       Iteration 4 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 65.0%
     Iteration 5/10: Testing low complexity goal
       Error in iteration 5: name 'defaultdict' is not defined
       Iteration 5 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 70.0%
     Iteration 6/10: Testing medium complexity goal
       Error in iteration 6: name 'defaultdict' is not defined
       Iteration 6 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 75.0%
     Iteration 7/10: Testing low complexity goal
       Error in iteration 7: name 'defaultdict' is not defined
       Iteration 7 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 80.0%
     Iteration 8/10: Testing medium complexity goal
       Error in iteration 8: name 'defaultdict' is not defined
       Iteration 8 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 85.0%
     Iteration 9/10: Testing low complexity goal
       Error in iteration 9: name 'defaultdict' is not defined
       Iteration 9 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
     Iteration 10/10: Testing medium complexity goal
       Error in iteration 10: name 'defaultdict' is not defined
       Iteration 10 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
   ✓ Performance: avg workflow time 0.00s, p95 response time 0.00s, success rate 100.0%, cache hit rate 64.5%
   Performance criteria met: 4/4
     - Time criteria: ✓ (avg < 3s)
     - P95 response time: ✓ (< 5s)
     - Success rate: ✓ (> 90%)
     - Cache hit rate: ✓ (> 50%)

7. Testing Error Handling and Recovery...
2025-11-27 09:09:31,434 - transition_modeling.transition_modeler - INFO - Processing modeling request with 0 available transitions
2025-11-27 09:09:31,434 - transition_modeling.transition_modeler - WARNING - No available transitions provided in request request_1764205771434395
2025-11-27 09:09:31,434 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ Error handling: 4 error cases tested

================================================================================
INTEGRATION TEST REPORT
================================================================================
Total Tests: 7
Successful Tests: 2
Success Rate: 28.6%
Total Time: 0.10 seconds

1. module_initialization: ✗ FAIL
   Message: Module initialization: 3/4 modules ready
   Details: {
  "goal_interpretation": true,
  "subgoal_decomposition": true,
  "transition_modeling": false,
  "action_sequencing": true
}

2. goal_to_transition_flow: ✗ FAIL
   Message: Goal→Transition flow error: name 'defaultdict' is not defined
   Details: {
  "error": "name 'defaultdict' is not defined",
  "exception_type": "NameError"
}

3. subgoal_to_action_flow: ✓ PASS
   Message: Subgoal→Action flow: 7 subgoals → 7 action sequences
   Details: {
  "subgoals_count": 7,
  "action_sequences_count": 7,
  "subgoals": [
    "Execute atomic action: ball_move",
    "Eventually: ball_move",
    "Execute atomic action: locations_kitchen",
    "Eventually: locations_kitchen",
    "Execute atomic action: furniture_table",
    "Eventually: furniture_table",
    "Parallel: F(ball_move) & F(locations_kitchen) & F(furniture_table)"
  ],
  "action_sequences": [
    [],
    [],
    []
  ]
}

4. end_to_end_workflow: ✗ FAIL
   Message: End-to-End workflow: 0/2 scenarios successful (0.0%) in 0.00s
   Details: {
  "total_scenarios": 2,
  "successful_scenarios": 0,
  "success_rate": 0.0,
  "workflow_time": 0.003895282745361328,
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
          "time": 0.0019185543060302734,
          "result": "(red_put -> F(furniture_table))"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0001785755157470703
        }
      },
      "subgoals_count": 4,
      "subgoals_details": [
        {
          "id": "atomic_2",
          "description": "Execute atomic action: (red_put",
          "ltl_formula": "(red_put",
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
          "ltl_formula": "F(furniture_table))",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_5"
          ]
        },
        {
          "id": "logical_7",
          "description": "Conditional: (red_put -> F(furniture_table))",
          "ltl_formula": "(red_put->F(furniture_table))",
          "type": "CONDITIONAL",
          "dependencies": [
            "atomic_2",
            "temporal_6"
          ]
        }
      ],
      "success": false,
      "error": "name 'defaultdict' is not defined",
      "exception_type": "NameError"
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
          "time": 0.0007913112640380859,
          "result": "(((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.00024127960205078125
        }
      },
      "subgoals_count": 8,
      "subgoals_details": [
        {
          "id": "atomic_2",
          "description": "Execute atomic action: perform_(((open",
          "ltl_formula": "perform_(((open",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "atomic_5",
          "description": "Execute atomic action: appliances_refrigerator",
          "ltl_formula": "appliances_refrigerator",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "temporal_6",
          "description": "Eventually: appliances_refrigerator",
          "ltl_formula": "F(appliances_refrigerator))",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_5"
          ]
        },
        {
          "id": "atomic_9",
          "description": "Execute atomic action: locations_door",
          "ltl_formula": "locations_door",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "temporal_10",
          "description": "Eventually: locations_door",
          "ltl_formula": "F(locations_door))",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_9"
          ]
        },
        {
          "id": "atomic_13",
          "description": "Execute atomic action: relative_time_then",
          "ltl_formula": "relative_time_then",
          "type": "ATOMIC",
          "dependencies": []
        },
        {
          "id": "temporal_14",
          "description": "Eventually: relative_time_then",
          "ltl_formula": "F(relative_time_then))",
          "type": "TEMPORAL",
          "dependencies": [
            "atomic_13"
          ]
        },
        {
          "id": "logical_15",
          "description": "Conditional: (((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))",
          "ltl_formula": "(((open->F(appliances_refrigerator))->F(locations_door))->F(relative_time_then))",
          "type": "CONDITIONAL",
          "dependencies": [
            "atomic_2",
            "temporal_6",
            "temporal_10",
            "temporal_14"
          ]
        }
      ],
      "success": false,
      "error": "name 'defaultdict' is not defined",
      "exception_type": "NameError"
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
          "time": 0.0008976459503173828
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.00012135505676269531
        }
      },
      "success": false,
      "error": "name 'defaultdict' is not defined",
      "exception_type": "NameError"
    },
    {
      "name": "Conditional Constraint Scenario",
      "goal": "If the room has light, pick up the red ball; otherwise, turn on the light first, then pick up the ball",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.000957489013671875
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.00024199485778808594
        }
      },
      "success": false,
      "error": "name 'defaultdict' is not defined",
      "exception_type": "NameError"
    },
    {
      "name": "Sequential Constraint Scenario",
      "goal": "First open the computer, then check email, finally close the computer",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.0006875991821289062
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0004229545593261719
        }
      },
      "success": false,
      "error": "name 'defaultdict' is not defined",
      "exception_type": "NameError"
    }
  ]
}

6. performance_and_stability: ✓ PASS
   Message: Performance: avg workflow time 0.00s, p95 response time 0.00s, success rate 100.0%, cache hit rate 64.5%
   Details: {
  "iterations": 10,
  "average_times": {
    "goal_interpretation": 0.0006111860275268555,
    "subgoal_decomposition": 0.00011067390441894531,
    "transition_modeling": 0,
    "action_sequencing": 0,
    "total_workflow": 0.0007642030715942383,
    "p95_response_time": 0.0009911060333251953
  },
  "performance_criteria": {
    "time_criteria": true,
    "p95_criteria": true,
    "success_criteria": true,
    "cache_criteria": true,
    "criteria_met": 4
  },
  "cache_performance": {
    "avg_hit_rate": 0.645
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
❌ POOR: Significant integration issues need to be resolved

⚠️  Could not save report file: Object of type SubgoalType is not JSON serializable

⚠️  Four-module integration test completed with issues.
