python tests/test_four_module_integration.py
✓ All four modules imported successfully
2025-11-27 09:36:30,660 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-27 09:36:30,660 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
================================================================================
Complete Four-Module Integration Test
Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing
================================================================================

1. Testing Module Initialization...
   ✓ Goal Interpretation module initialized
   ✓ Subgoal Decomposition module initialized
   ✓ Transition Modeling module initialized
2025-11-27 09:36:30,677 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
   ✓ Action Sequencing module initialized
   ✓ Module initialization: 4/4 modules ready

2. Testing Goal Interpretation to Transition Modeling Flow...
   Processing goal: Put the red ball on the table
   ✓ Goal interpretation completed in 0.001s
   ✗ Goal to transition flow test failed: expected string or bytes-like object, got 'dict'

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✗ Subgoal to action flow test failed: expected string or bytes-like object, got 'dict'

4. Testing End-to-End Workflow...

   Processing scenario: Basic Operation Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✗ Error in scenario Basic Operation Scenario: expected string or bytes-like object, got 'dict'

   Processing scenario: Multi-step Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✗ Error in scenario Multi-step Scenario: expected string or bytes-like object, got 'dict'

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.001s)
     ✗ Multi-Goal Scenario: Failed - expected string or bytes-like object, got 'dict'
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✗ Conditional Constraint Scenario: Failed - expected string or bytes-like object, got 'dict'
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✗ Sequential Constraint Scenario: Failed - expected string or bytes-like object, got 'dict'
   ✗ Complex scenarios: 0/3 successful

6. Testing Performance and Stability...
   Preheating system...
   Running 10 performance test iterations...
     Iteration 1/10: Testing low complexity goal
       Error in iteration 1: expected string or bytes-like object, got 'dict'
       Iteration 1 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 20.0%
     Iteration 2/10: Testing medium complexity goal
       Error in iteration 2: expected string or bytes-like object, got 'dict'
       Iteration 2 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 30.0%
     Iteration 3/10: Testing low complexity goal
       Error in iteration 3: expected string or bytes-like object, got 'dict'
       Iteration 3 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 40.0%
     Iteration 4/10: Testing medium complexity goal
       Error in iteration 4: expected string or bytes-like object, got 'dict'
       Iteration 4 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 65.0%
     Iteration 5/10: Testing low complexity goal
       Error in iteration 5: expected string or bytes-like object, got 'dict'
       Iteration 5 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 70.0%
     Iteration 6/10: Testing medium complexity goal
       Error in iteration 6: expected string or bytes-like object, got 'dict'
       Iteration 6 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 75.0%
     Iteration 7/10: Testing low complexity goal
       Error in iteration 7: expected string or bytes-like object, got 'dict'
       Iteration 7 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 80.0%
     Iteration 8/10: Testing medium complexity goal
       Error in iteration 8: expected string or bytes-like object, got 'dict'
       Iteration 8 metrics:
         - Total time: 0.001s
         - Response time: 0.001s
         - Success rate: 100.0%
         - Estimated cache hit rate: 85.0%
     Iteration 9/10: Testing low complexity goal
       Error in iteration 9: expected string or bytes-like object, got 'dict'
       Iteration 9 metrics:
         - Total time: 0.000s
         - Response time: 0.000s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
     Iteration 10/10: Testing medium complexity goal
       Error in iteration 10: expected string or bytes-like object, got 'dict'
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
2025-11-27 09:36:30,690 - transition_modeling.transition_modeler - INFO - Processing modeling request with 0 available transitions
2025-11-27 09:36:30,690 - transition_modeling.transition_modeler - WARNING - No available transitions provided in request request_1764207390690687
2025-11-27 09:36:30,690 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ Error handling: 4 error cases tested

================================================================================
INTEGRATION TEST REPORT
================================================================================
Total Tests: 7
Successful Tests: 2
Success Rate: 28.6%
Total Time: 0.03 seconds

1. module_initialization: ✓ PASS
   Message: Module initialization: 4/4 modules ready
   Details: {
  "goal_interpretation": true,
  "subgoal_decomposition": true,
  "transition_modeling": true,
  "action_sequencing": true
}

2. goal_to_transition_flow: ✗ FAIL
   Message: Goal→Transition flow error: expected string or bytes-like object, got 'dict'
   Details: {
  "error": "expected string or bytes-like object, got 'dict'",
  "exception_type": "TypeError"
}

3. subgoal_to_action_flow: ✗ FAIL
   Message: expected string or bytes-like object, got 'dict'

4. end_to_end_workflow: ✗ FAIL
   Message: End-to-End workflow: 0/2 scenarios successful (0.0%) in 0.00s
   Details: {
  "total_scenarios": 2,
  "successful_scenarios": 0,
  "success_rate": 0.0,
  "workflow_time": 0.0015554428100585938,
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
          "time": 0.0007007122039794922,
          "result": "{'original_text': 'Put the red ball on the table', 'parse_result': {'original_text': 'put the red ball on the table', 'language': 'en', 'task_complexity': 'simple', 'semantic_structure': {'main_clause': '', 'subordinate_clauses': [], 'connect
ors': [], 'modifiers': []}, 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'temporal_info': [], 'conditions': [], 'constraints': [], 'propositions': ['red_put', 'furniture_table'], 'structure': 'simple', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'put', 'modified': 'the', 'position': 0}, {'type': 'adjective', 'modifier': 'ball', 'modified': 'on', 'position': 12}]}, 'ltl_formula': '(red_put -> F(furniture_table))', 'optimized_formula': '(red_put ->Ffurniture_table)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': ['发现 2 个未映射实体'], 'suggestions': [], 'entity_issues': ['未映射的实体: red_put', '未映射的实体: furniture_table'], 'temporal_checks': {'operators_used': [' ', 'F'], 'has_f_operator': True}}, 'structure': 'simple', 'task_complexity': 'simple', 'language': 'en', 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'conditions': [], 'constraints': [], 'temporal_info': [], 'propositions': ['red_put', 'furniture_table'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-27T09:36:30.680034', 'proposition_count': 2, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"                                  }
      },
      "success": false,
      "error": "expected string or bytes-like object, got 'dict'",
      "exception_type": "TypeError"
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
          "time": 0.0007388591766357422,
          "result": "{'original_text': 'Walk to the refrigerator first, then open the refrigerator door', 'parse_result': {'original_text': 'walk to the refrigerator first ,  then open the refrigerator door', 'language': 'en', 'task_complexity': 'complex', 'seman
tic_structure': {'main_clause': '', 'subordinate_clauses': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'conditions': [], 'constraints': [], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'structure': 'sequential', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'walk', 'modified': 'to', 'position': 0}, {'type': 'adjective', 'modifier': 'then', 'modified': 'open', 'position': 34}]}, 'ltl_formula': '(((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))', 'optimized_formula': '(((open ->Fappliances_refrigerator)->Flocations_door)->Frelative_time_then)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': ['发现 3 个未映射实体'], 'suggestions': [], 'entity_issues': ['未映射的实体: appliances_refrigerator', '未映射的实体: locations_door', '未映射的实体: relative_time_then'], 'temporal_checks': {'operators_used': [' ', 'F'], 'has_f_operator': True}}, 'structure': 'sequential', 'task_complexity': 'complex', 'language': 'en', 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'conditions': [], 'constraints': [], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-27T09:36:30.680819', 'proposition_count': 4, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"                                                                                                                                                                                                           }
      },
      "success": false,
      "error": "expected string or bytes-like object, got 'dict'",
      "exception_type": "TypeError"
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
          "time": 0.0009322166442871094
        }
      },
      "success": false,
      "error": "expected string or bytes-like object, got 'dict'",
      "exception_type": "TypeError"
    },
    {
      "name": "Conditional Constraint Scenario",
      "goal": "If the room has light, pick up the red ball; otherwise, turn on the light first, then pick up the ball",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.0008988380432128906
        }
      },
      "success": false,
      "error": "expected string or bytes-like object, got 'dict'",
      "exception_type": "TypeError"
    },
    {
      "name": "Sequential Constraint Scenario",
      "goal": "First open the computer, then check email, finally close the computer",
      "steps": {
        "goal_interpretation": {
          "success": true,
          "time": 0.0007033348083496094
        }
      },
      "success": false,
      "error": "expected string or bytes-like object, got 'dict'",
      "exception_type": "TypeError"
    }
  ]
}

6. performance_and_stability: ✓ PASS
   Message: Performance: avg workflow time 0.00s, p95 response time 0.00s, success rate 100.0%, cache hit rate 64.5%
   Details: {
  "iterations": 10,
  "average_times": {
    "goal_interpretation": 0.0005359888076782226,
    "subgoal_decomposition": 0,
    "transition_modeling": 0,
    "action_sequencing": 0,
    "total_workflow": 0.0005457878112792968,
    "p95_response_time": 0.0006303787231445312
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

📄 Detailed report saved to: four_module_integration_test_results.json

⚠️  Four-module integration test completed with issues.
