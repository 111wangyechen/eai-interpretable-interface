(base) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface$ python -m pytest tests/test_four_module_integration.py -v 
========================================================================================================================= test session starts =========================================================================================================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0 -- /home/yeah/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /home/yeah/eai-interpretable-interface
plugins: anyio-4.7.0
collected 1 item                                                                                                                                                                                                                                                      

tests/test_four_module_integration.py::test_four_module_integration FAILED                                                                                                                                                                                      [100%]

============================================================================================================================== FAILURES ===============================================================================================================================
____________________________________________________________________________________________________________________ test_four_module_integration _____________________________________________________________________________________________________________________

    def test_four_module_integration():
        """测试四模块集成功能，供pytest识别"""
        tester = FourModuleIntegrationTester()
        success = tester.run_comprehensive_integration_test()
    
        # 检查是否至少有50%的测试通过
>       assert success, "四模块集成测试未达到预期成功率"
E       AssertionError: 四模块集成测试未达到预期成功率
E       assert None

tests/test_four_module_integration.py:1202: AssertionError
------------------------------------------------------------------------------------------------------------------------ Captured stdout call -------------------------------------------------------------------------------------------------------------------------
================================================================================
Complete Four-Module Integration Test
Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing
================================================================================

1. Testing Module Initialization...
   ✓ Goal Interpretation module initialized
   ✓ Subgoal Decomposition module initialized
   ✓ Transition Modeling module initialized
   ✓ Action Sequencing module initialized
   ✓ Module initialization: 4/4 modules ready

2. Testing Goal Interpretation to Transition Modeling Flow...
   Processing goal: Put the red ball on the table
   ✓ Goal interpretation completed in 0.001s
   Generated LTL formula: (red_put -> F(furniture_table))
   ✓ 1 subgoals generated: ['Execute atomic action: (red_put->F(furniture_table))']
   ✓ Goal→Transition flow: 1 sequences generated in 0.000s

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✓ 8 subgoals generated: ['Execute atomic action: ball_move', 'Eventually: ball_move', 'Execute atomic action: locations_kitchen', 'Eventually: locations_kitchen', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Parallel: F(locations_kitchen) & F(furniture_table)', 'Parallel: F(ball_move) & F(locations_kitchen)&F(furniture_table)']
   Debug: Processing subgoal 1: Execute atomic action: ball_move
   Debug: Failed to generate action sequence for subgoal 1
   Debug: Processing subgoal 2: Eventually: ball_move
   Debug: Failed to generate action sequence for subgoal 2
   Debug: Processing subgoal 3: Execute atomic action: locations_kitchen
   Debug: Failed to generate action sequence for subgoal 3
   Debug: Processing subgoal 4: Eventually: locations_kitchen
   Debug: Failed to generate action sequence for subgoal 4
   Debug: Processing subgoal 5: Execute atomic action: furniture_table
   Debug: Failed to generate action sequence for subgoal 5
   Debug: Processing subgoal 6: Eventually: furniture_table
   Debug: Failed to generate action sequence for subgoal 6
   Debug: Processing subgoal 7: Parallel: F(locations_kitchen) & F(furniture_table)
   Debug: Failed to generate action sequence for subgoal 7
   Debug: Processing subgoal 8: Parallel: F(ball_move) & F(locations_kitchen)&F(furniture_table)
   Debug: Failed to generate action sequence for subgoal 8
   ✓ Subgoal→Action flow: 8 subgoals → 8 action sequences

4. Testing End-to-End Workflow...

   Processing scenario: Basic Operation Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 1 subgoals
         Subgoal 1: Execute atomic action: (red_put->F(furniture_table))
           - ID: atomic_1
           - LTL: (red_put->F(furniture_table))
           - Type: SubgoalType.ATOMIC
     Step 3: Transition Modeling
       Available transitions count: 4
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
       Available actions: ['move', 'pickup', 'place']
       ✗ Error in scenario Basic Operation Scenario: Action sequence generation failed

   Processing scenario: Multi-step Scenario
     Step 1: Goal Interpretation
       ✓ Goal interpretation successful
     Step 2: Subgoal Decomposition
       ✓ Subgoal decomposition successful, created 1 subgoals
         Subgoal 1: Execute atomic action: (((open->F(appliances_refrigerator))->F(locations_door))->F(relative_time_then))
           - ID: atomic_1
           - LTL: (((open->F(appliances_refrigerator))->F(locations_door))->F(relative_time_then))
           - Type: SubgoalType.ATOMIC
     Step 3: Transition Modeling
       Available transitions count: 4
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
       Available actions: ['move', 'pickup', 'place', 'open_door']
       ✗ Error in scenario Multi-step Scenario: Action sequence generation failed

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
     ✗ Multi-Goal Scenario: Failed - Action sequence generation failed
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
     ✗ Conditional Constraint Scenario: Failed - Action sequence generation failed
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 1 subgoals (0.000s)
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
     ✗ Sequential Constraint Scenario: Failed - Action sequence generation failed
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
         - Total time: 0.001s
         - Response time: 0.001s
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
         - Total time: 0.000s
         - Response time: 0.000s
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
         - Total time: 0.001s
         - Response time: 0.001s
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
         - Total time: 0.001s
         - Response time: 0.001s
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
   ✓ Error handling: 4 error cases tested

================================================================================
INTEGRATION TEST REPORT
================================================================================
Total Tests: 7
Successful Tests: 4
Success Rate: 57.1%
Total Time: 0.09 seconds

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
  "goal_interpretation_time": 0.0008702278137207031,
  "subgoal_decomposition_time": 6.246566772460938e-05,
  "modeling_time": 0.00019097328186035156,
  "total_time": 0.001123666763305664
}

3. subgoal_to_action_flow: ✓ PASS
   Message: Subgoal→Action flow: 8 subgoals → 8 action sequences
   Details: {
  "subgoals_count": 8,
  "action_sequences_count": 8,
  "subgoals": [
    "Execute atomic action: ball_move",
    "Eventually: ball_move",
    "Execute atomic action: locations_kitchen",
    "Eventually: locations_kitchen",
    "Execute atomic action: furniture_table",
    "Eventually: furniture_table",
    "Parallel: F(locations_kitchen) & F(furniture_table)",
    "Parallel: F(ball_move) & F(locations_kitchen)&F(furniture_table)"
  ],
  "action_sequences": [
    [],
    [],
    []
  ]
}

4. end_to_end_workflow: ✗ FAIL
   Message: End-to-End workflow: 0/2 scenarios successful (0.0%) in 0.01s
   Details: {
  "total_scenarios": 2,
  "successful_scenarios": 0,
  "success_rate": 0.0,
  "workflow_time": 0.009307622909545898,
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
          "time": 0.0009503364562988281,
          "result": "{'original_text': 'Put the red ball on the table', 'parse_result': {'original_text': 'put the red ball on the table', 'language': 'en', 'task_complexity': 'simple', 'semantic_structure': {'main_clause': '', 'subordinate_clauses': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'temporal_info': [], 'conditions': [], 'constraints': [], 'propositions': ['red_put', 'furniture_table'], 'structure': 'simple', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'put', 'modified': 'the', 'position': 0}, {'type': 'adjective', 'modifier': 'ball', 'modified': 'on', 'position': 12}]}, 'ltl_formula': '(red_put -> F(furniture_table))', 'optimized_formula': '(red_put ->Ffurniture_table)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': ['发现 2 个未映射实体'], 'suggestions': [], 'entity_issues': ['未映射的实体: red_put', '未映射的实体: furniture_table'], 'temporal_checks': {'operators_used': [' ', 'F'], 'has_f_operator': True}}, 'structure': 'simple', 'task_complexity': 'simple', 'language': 'en', 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'conditions': [], 'constraints': [], 'temporal_info': [], 'propositions': ['red_put', 'furniture_table'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-27T10:48:31.057768', 'proposition_count': 2, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 9.131431579589844e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00019693374633789062
        },
        "action_sequencing": {
          "success": false,
          "time": 0.002917766571044922
        }
      },
      "subgoals_count": 1,
      "subgoals_details": [
        {
          "id": "atomic_1",
          "description": "Execute atomic action: (red_put->F(furniture_table))",
          "ltl_formula": "(red_put->F(furniture_table))",
          "type": "ATOMIC",
          "dependencies": []
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
          "time": 0.0009560585021972656,
          "result": "{'original_text': 'Walk to the refrigerator first, then open the refrigerator door', 'parse_result': {'original_text': 'walk to the refrigerator first ,  then open the refrigerator door', 'language': 'en', 'task_complexity': 'complex', 'semantic_structure': {'main_clause': '', 'subordinate_clauses': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'conditions': [], 'constraints': [], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'structure': 'sequential', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'walk', 'modified': 'to', 'position': 0}, {'type': 'adjective', 'modifier': 'then', 'modified': 'open', 'position': 34}]}, 'ltl_formula': '(((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))', 'optimized_formula': '(((open ->Fappliances_refrigerator)->Flocations_door)->Frelative_time_then)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': ['发现 3 个未映射实体'], 'suggestions': [], 'entity_issues': ['未映射的实体: appliances_refrigerator', '未映射的实体: locations_door', '未映射的实体: relative_time_then'], 'temporal_checks': {'operators_used': [' ', 'F'], 'has_f_operator': True}}, 'structure': 'sequential', 'task_complexity': 'complex', 'language': 'en', 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'conditions': [], 'constraints': [], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-27T10:48:31.062102', 'proposition_count': 4, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 7.700920104980469e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00017404556274414062
        },
        "action_sequencing": {
          "success": false,
          "time": 0.0036156177520751953
        }
      },
      "subgoals_count": 1,
      "subgoals_details": [
        {
          "id": "atomic_1",
          "description": "Execute atomic action: (((open->F(appliances_refrigerator))->F(locations_door))->F(relative_time_then))",
          "ltl_formula": "(((open->F(appliances_refrigerator))->F(locations_door))->F(relative_time_then))",
          "type": "ATOMIC",
          "dependencies": []
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
          "time": 0.0009584426879882812
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 5.054473876953125e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0001366138458251953
        },
        "action_sequencing": {
          "success": false,
          "time": 0.0055828094482421875
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
          "time": 0.0009479522705078125
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 5.245208740234375e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00016832351684570312
        },
        "action_sequencing": {
          "success": false,
          "time": 0.005786418914794922
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
          "time": 0.0007987022399902344
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 6.794929504394531e-05
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0001690387725830078
        },
        "action_sequencing": {
          "success": false,
          "time": 0.005280017852783203
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
    "goal_interpretation": 0.0005737781524658203,
    "subgoal_decomposition": 0,
    "transition_modeling": 0,
    "action_sequencing": 0,
    "total_workflow": 0.0005844354629516602,
    "p95_response_time": 0.0007674694061279297
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
⚠️  FAIR: Partial integration, some modules need attention

⚠️  Could not save report file: Object of type SubgoalType is not JSON serializable
-------------------------------------------------------------------------------------------------------------------------- Captured log call --------------------------------------------------------------------------------------------------------------------------
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764211711026012, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764211711058039, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764211711062336, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764211711067255, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764211711074059, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764211711080944, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:404 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:503 No available transitions provided in request request_1764211711094330
======================================================================================================================= short test summary info =======================================================================================================================
FAILED tests/test_four_module_integration.py::test_four_module_integration - AssertionError: 四模块集成测试未达到预期成功率
========================================================================================================================== 1 failed in 0.54s ==========================================================================================================================
