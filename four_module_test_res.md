python -m pytest tests/test_four_module_integration.py -v
================================================================================================================= test session starts ==================================================================================================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0 -- /home/yeah/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /home/yeah/eai-interpretable-interface
plugins: anyio-4.7.0
collected 1 item                                                                                                                                                                                                                                       

tests/test_four_module_integration.py::test_four_module_integration FAILED                                                                                                                                                                       [100%]

======================================================================================================================= FAILURES =======================================================================================================================
_____________________________________________________________________________________________________________ test_four_module_integration _____________________________________________________________________________________________________________

    def test_four_module_integration():
        """测试四模块集成功能，供pytest识别"""
        tester = FourModuleIntegrationTester()
        success = tester.run_comprehensive_integration_test()
    
        # 检查是否至少有50%的测试通过
>       assert success, "四模块集成测试未达到预期成功率"
E       AssertionError: 四模块集成测试未达到预期成功率
E       assert None

tests/test_four_module_integration.py:1206: AssertionError
----------------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------------
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
   Generated LTL formula: (place_red -> F(furniture_table))
   ✓ 4 subgoals generated: ['Execute atomic action: place_red', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Conditional: place_red -> F(furniture_table)']
   ✓ Goal→Transition flow: 1 sequences generated in 0.000s

3. Testing Subgoal Decomposition to Action Sequencing Flow...
   ✓ 8 subgoals generated: ['Execute atomic action: move_ball', 'Eventually: move_ball', 'Execute atomic action: locations_kitchen', 'Eventually: locations_kitchen', 'Execute atomic action: furniture_table', 'Eventually: furniture_table', 'Parallel
: F(locations_kitchen) & F(furniture_table)', 'Parallel: F(move_ball) & F(locations_kitchen)&F(furniture_table)']                                                                                                                                          Debug: Processing subgoal 1: Execute atomic action: move_ball
   Debug: Failed to generate action sequence for subgoal 1
   Debug: Processing subgoal 2: Eventually: move_ball
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
   Debug: Processing subgoal 8: Parallel: F(move_ball) & F(locations_kitchen)&F(furniture_table)
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
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
       Available actions: ['move', 'pickup', 'place']
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
       ✓ Transition modeling successful, created 1 sequences
     Step 4: Action Sequencing
       Available actions: ['move', 'pickup', 'place', 'open_door']
       ✗ Error in scenario Multi-step Scenario: Action sequence generation failed

   ✗ End-to-End workflow test FAIL: 0/2 scenarios successful (0.0%)

5. Testing Complex Scenarios...
   Processing scenario: Multi-Goal Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 4 subgoals (0.000s)
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
     ✗ Multi-Goal Scenario: Failed - Action sequence generation failed
   Processing scenario: Conditional Constraint Scenario
     ✓ Goal interpretation completed (0.002s)
     ✓ Subgoal decomposition completed, generated 7 subgoals (0.000s)
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
     ✗ Conditional Constraint Scenario: Failed - Action sequence generation failed
   Processing scenario: Sequential Constraint Scenario
     ✓ Goal interpretation completed (0.001s)
     ✓ Subgoal decomposition completed, generated 10 subgoals (0.000s)
     ✓ Transition modeling completed, generated 1 sequences (0.000s)
     ✗ Sequential Constraint Scenario: Failed - Action sequence generation failed
   ✗ Complex scenarios: 0/3 successful

6. Testing Performance and Stability...
   Preheating system...
   Running 10 performance test iterations...
     Iteration 1/10: Testing low complexity goal
       Iteration 1 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 20.0%
     Iteration 2/10: Testing medium complexity goal
       Iteration 2 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 30.0%
     Iteration 3/10: Testing low complexity goal
       Iteration 3 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 40.0%
     Iteration 4/10: Testing medium complexity goal
       Iteration 4 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 65.0%
     Iteration 5/10: Testing low complexity goal
       Iteration 5 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 70.0%
     Iteration 6/10: Testing medium complexity goal
       Iteration 6 metrics:
         - Total time: 0.005s
         - Response time: 0.005s
         - Success rate: 100.0%
         - Estimated cache hit rate: 75.0%
     Iteration 7/10: Testing low complexity goal
       Iteration 7 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 80.0%
     Iteration 8/10: Testing medium complexity goal
       Iteration 8 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 85.0%
     Iteration 9/10: Testing low complexity goal
       Iteration 9 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
     Iteration 10/10: Testing medium complexity goal
       Iteration 10 metrics:
         - Total time: 0.004s
         - Response time: 0.004s
         - Success rate: 100.0%
         - Estimated cache hit rate: 90.0%
   ✓ Performance: avg workflow time 0.00s, p95 response time 0.01s, success rate 100.0%, cache hit rate 64.5%
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
Total Time: 0.13 seconds

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
  "goal_interpretation_time": 0.0009679794311523438,
  "subgoal_decomposition_time": 0.0002651214599609375,
  "modeling_time": 0.0002231597900390625,
  "total_time": 0.0014562606811523438
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
   Message: End-to-End workflow: 0/2 scenarios successful (0.0%) in 0.01s
   Details: {
  "total_scenarios": 2,
  "successful_scenarios": 0,
  "success_rate": 0.0,
  "workflow_time": 0.009575366973876953,
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
          "time": 0.0008957386016845703,
          "result": "{'original_text': 'Put the red ball on the table', 'parse_result': {'original_text': 'put the red ball on the table', 'language': 'en', 'task_complexity': 'simple', 'semantic_structure': {'main_clause': '', 'subordinate_clauses
': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'temporal_info': [], 'conditions': [], 'constraints': [], 'propositions': ['place_red', 'furniture_table'], 'structure': 'simple', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'put', 'modified': 'the', 'position': 0}, {'type': 'adjective', 'modifier': 'ball', 'modified': 'on', 'position': 12}]}, 'ltl_formula': '(place_red -> F(furniture_table))', 'optimized_formula': '(place_red ->Ffurniture_table)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': [], 'entity_issues': [], 'temporal_checks': {'operators_used': ['F', ' '], 'has_f_operator': True}}, 'structure': 'simple', 'task_complexity': 'simple', 'language': 'en', 'actions': [{'type': 'place', 'verb': 'put', 'object': 'red', 'position': 0, 'context': 'put the red b'}], 'objects': [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 20, 'context': 'd ball on the table'}], 'conditions': [], 'constraints': [], 'temporal_info': [], 'propositions': ['place_red', 'furniture_table'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'destination': [], 'source': [], 'time': [{'marker': 'on', 'filler': 'the table', 'position': 17}], 'purpose': [], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-29T15:06:58.834681', 'proposition_count': 2, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"                                                                                                                                                                                                                        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.00017976760864257812
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00024437904357910156
        },
        "action_sequencing": {
          "success": false,
          "time": 0.002644777297973633
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
          "time": 0.0010268688201904297,
          "result": "{'original_text': 'Walk to the refrigerator first, then open the refrigerator door', 'parse_result': {'original_text': 'walk to the refrigerator first ,  then open the refrigerator door', 'language': 'en', 'task_complexity': 'c
omplex', 'semantic_structure': {'main_clause': '', 'subordinate_clauses': [], 'connectors': [], 'modifiers': []}, 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'conditions': [], 'constraints': [], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'structure': 'sequential', 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'dependencies': [], 'modifiers': [{'type': 'adjective', 'modifier': 'walk', 'modified': 'to', 'position': 0}, {'type': 'adjective', 'modifier': 'then', 'modified': 'open', 'position': 34}]}, 'ltl_formula': '(((open -> F(appliances_refrigerator)) -> F(locations_door)) -> F(relative_time_then))', 'optimized_formula': '(((open ->Fappliances_refrigerator)->Flocations_door)->Frelative_time_then)', 'validation_result': {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': [], 'entity_issues': [], 'temporal_checks': {'operators_used': ['F', ' '], 'has_f_operator': True}}, 'structure': 'sequential', 'task_complexity': 'complex', 'language': 'en', 'actions': [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 39, 'context': 'rigerator first ,  then open the refri', 'sequential_order': 2, 'sequential_pattern': True}], 'objects': [{'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 8, 'context': 'walk to the refrigerator first ,  '}, {'name': 'refrigerator', 'category': 'appliances', 'modifier': 'the ', 'position': 44, 'context': 'then open the refrigerator door'}, {'name': 'door', 'category': 'locations', 'modifier': 'refrigerator ', 'position': 48, 'context': ' open the refrigerator door'}], 'conditions': [], 'constraints': [], 'temporal_info': [{'type': 'relative_time', 'expression': 'then', 'position': 34, 'end_position': 38}], 'propositions': ['open', 'appliances_refrigerator', 'locations_door', 'relative_time_then'], 'dependencies': [], 'semantic_roles': {'agent': [], 'patient': [], 'instrument': [], 'location': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'destination': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'source': [], 'time': [], 'purpose': [{'marker': 'to', 'filler': 'the refrigerator first', 'position': 5}], 'condition': []}, 'interpretation_metadata': {'timestamp': '2025-11-29T15:06:58.839045', 'proposition_count': 4, 'condition_count': 0, 'constraint_count': 0, 'dependency_count': 0}}"                                                                                                          },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0002639293670654297
        },
        "transition_modeling": {
          "success": true,
          "time": 0.0002491474151611328
        },
        "action_sequencing": {
          "success": false,
          "time": 0.003481149673461914
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
          "time": 0.0010519027709960938
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.00016164779663085938
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00016617774963378906
        },
        "action_sequencing": {
          "success": false,
          "time": 0.005499362945556641
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
          "time": 0.0015702247619628906
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.0002391338348388672
        },
        "transition_modeling": {
          "success": true,
          "time": 0.00018930435180664062
        },
        "action_sequencing": {
          "success": false,
          "time": 0.0064127445220947266
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
          "time": 0.0007996559143066406
        },
        "subgoal_decomposition": {
          "success": true,
          "time": 0.00028014183044433594
        },
        "transition_modeling": {
          "success": true,
          "time": 0.000171661376953125
        },
        "action_sequencing": {
          "success": false,
          "time": 0.006066560745239258
        }
      },
      "success": false,
      "error": "Action sequence generation failed",
      "exception_type": "Exception"
    }
  ]
}

6. performance_and_stability: ✓ PASS
   Message: Performance: avg workflow time 0.00s, p95 response time 0.01s, success rate 100.0%, cache hit rate 64.5%
   Details: {
  "iterations": 10,
  "average_times": {
    "goal_interpretation": 0.0006420373916625977,
    "subgoal_decomposition": 0.00015358924865722657,
    "transition_modeling": 0.0001764535903930664,
    "action_sequencing": 0.0033597946166992188,
    "total_workflow": 0.004334640502929687,
    "p95_response_time": 0.0050411224365234375
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
------------------------------------------------------------------------------------------------------------------ Captured log call -------------------------------------------------------------------------------------------------------------------
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018803850, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018835177, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018839637, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018844680, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018852238, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018859982, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018868122, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018872360, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018877399, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018881755, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018885955, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018889998, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018894455, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018898947, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018903287, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:555 No sequences were generated for request request_1764400018907786, creating fallback
WARNING  action_sequencing.action_sequencer:action_sequencer.py:443 Failed to generate action sequence: No solution found within time/depth limits
WARNING  transition_modeling.transition_modeler:transition_modeler.py:503 No available transitions provided in request request_1764400018912187
=============================================================================================================== short test summary info ================================================================================================================
FAILED tests/test_four_module_integration.py::test_four_module_integration - AssertionError: 四模块集成测试未达到预期成功率
================================================================================================================== 1 failed in 1.23s ===================================================================================================================
