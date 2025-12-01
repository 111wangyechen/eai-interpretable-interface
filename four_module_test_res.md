python tests/test_four_module_integration.py
✓ 所有模块及数据结构导入成功
2025-12-01 09:16:31,226 - AuDeRe - INFO - AuDeRe engine initialized
2025-12-01 09:16:31,226 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
================================================================================
增强版四模块集成测试（含接口与数据校验）
目标解释 → 子目标分解 → 转换建模 → 动作序列
================================================================================

1. 增强版模块初始化测试...
   ✓ 目标解释模块接口验证通过
   ✓ 子目标分解模块接口验证通过
2025-12-01 09:16:31,244 - transition_modeling.transition_modeler - INFO - Processing modeling request with 1 available transitions
2025-12-01 09:16:31,244 - transition_modeling.transition_predictor - INFO - Generated 1 transition predictions
2025-12-01 09:16:31,244 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-12-01 09:16:31,244 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-12-01 09:16:31,244 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-12-01 09:16:31,244 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764551791244127, creating fallback
2025-12-01 09:16:31,244 - transition_modeling.transition_predictor - INFO - Updated historical data for move_atomic: 0.550
2025-12-01 09:16:31,244 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ 转换建模模块接口验证通过
2025-12-01 09:17:16,269 - action_sequencing.action_sequencer - WARNING - Generated sequence failed validation: ["Goal not fully achieved. Unmet goals: ['at (expected: shelf, actual: start)']", 'No official BEHAVIOR actions found in sequence']
2025-12-01 09:17:16,269 - action_sequencing.action_sequencer - INFO - Generating fallback action sequence with available actions
2025-12-01 09:17:16,270 - action_sequencing.action_sequencer - INFO - Successfully generated action sequence with 1 actions
   ✓ 动作序列模块接口验证通过

2. 目标→子目标数据传输测试...
   ✓ 目标→子目标数据传输格式验证通过

3. 子目标→转换建模接口测试...
2025-12-01 09:17:16,271 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-12-01 09:17:16,271 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-12-01 09:17:16,271 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-12-01 09:17:16,271 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-12-01 09:17:16,271 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764551836271745, creating fallback
2025-12-01 09:17:16,272 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ 子目标→转换建模接口适配通过

4. 转换→动作序列参数传递测试...
2025-12-01 09:17:16,272 - transition_modeling.transition_modeler - INFO - Processing modeling request with 2 available transitions
2025-12-01 09:17:16,272 - transition_modeling.transition_predictor - INFO - Generated 1 transition predictions
2025-12-01 09:17:16,272 - transition_modeling.transition_predictor - INFO - Generated 1 transition predictions
2025-12-01 09:17:16,272 - transition_modeling.transition_predictor - INFO - Generated 1 possible sequences
2025-12-01 09:17:16,272 - transition_modeling.transition_modeler - INFO - Predictor generated 1 raw sequences
2025-12-01 09:17:16,272 - transition_modeling.transition_predictor - INFO - Updated historical data for move_atomic: 0.595
2025-12-01 09:17:16,272 - transition_modeling.transition_predictor - INFO - Updated historical data for pick_atomic: 0.550
2025-12-01 09:17:16,272 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-12-01 09:18:01,287 - action_sequencing.action_sequencer - WARNING - Generated sequence failed validation: ["Goal not fully achieved. Unmet goals: ['at (expected: B, actual: A)', 'holding (expected: box, actual: None)']", 'No official BEHAVIOR 
actions found in sequence']                                                                                                                                                                                                                             2025-12-01 09:18:01,287 - action_sequencing.action_sequencer - INFO - Generating fallback action sequence with available actions
2025-12-01 09:18:01,287 - action_sequencing.action_sequencer - INFO - Successfully generated action sequence with 2 actions
   ✗ 转换→动作序列参数传递失败: move动作参数传递错误

5. 端到端全链路测试...
   测试目标: Open the fridge, take out the milk, and pour it into the cup
   目标解释生成LTL: F(open_fridge) & F(pickup) & F(appliances_fridge) & F(food_milk) & F(containers_cup)
   子目标分解结果: ['Execute atomic action: open_fridge', 'Eventually: open_fridge', 'Execute atomic action: perform_pickup', 'Eventually: pickup', 'Execute atomic action: appliances_fridge', 'Eventually: appliances_fridge', 'Execute atomic action:
 food_milk', 'Eventually: food_milk', 'Execute atomic action: containers_cup', 'Eventually: containers_cup', 'Parallel: F(food_milk) & F(containers_cup)', 'Parallel: F(appliances_fridge) & F(food_milk)&F(containers_cup)', 'Parallel: F(pickup) & F(appliances_fridge)&F(food_milk)&F(containers_cup)', 'Parallel: F(open_fridge) & F(pickup)&F(appliances_fridge)&F(food_milk)&F(containers_cup)']                                                                                                          2025-12-01 09:18:01,290 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-12-01 09:18:01,290 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-12-01 09:18:01,290 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-12-01 09:18:01,290 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-12-01 09:18:01,290 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764551881290072, creating fallback
2025-12-01 09:18:01,290 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-12-01 09:18:46,295 - action_sequencing.action_sequencer - WARNING - Generated sequence failed validation: ["Goal not fully achieved. Unmet goals: ['robot_position (expected: counter, actual: kitchen_door)', 'cup_has_milk (expected: True, actua
l: False)']", 'No official BEHAVIOR actions found in sequence']                                                                                                                                                                                         2025-12-01 09:18:46,296 - action_sequencing.action_sequencer - INFO - Generating fallback action sequence with available actions
2025-12-01 09:18:46,296 - action_sequencing.action_sequencer - INFO - Successfully generated action sequence with 3 actions
   ✗ 端到端流程失败: 存在数据格式不一致问题

6. 数据容错能力测试...
   ✓ 目标解释模块容错通过
   ✓ 子目标分解模块容错通过
2025-12-01 09:18:46,297 - transition_modeling.transition_modeler - INFO - Processing modeling request with 0 available transitions
2025-12-01 09:18:46,297 - transition_modeling.transition_modeler - WARNING - No available transitions provided in request request_1764551926297036
2025-12-01 09:18:46,297 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
   ✓ 转换建模模块对空转换列表容错通过
2025-12-01 09:18:46,297 - action_sequencing.action_sequencer - WARNING - state_transitions is a string, attempting to parse as JSON: invalid_format
2025-12-01 09:18:46,297 - action_sequencing.action_sequencer - ERROR - Error processing state_transitions: Expecting value: line 1 column 1 (char 0)
2025-12-01 09:19:31,322 - action_sequencing.action_sequencer - WARNING - Generated sequence failed validation: ["Goal not fully achieved. Unmet goals: ['at (expected: B, actual: A)']", 'No official BEHAVIOR actions found in sequence']
2025-12-01 09:19:31,322 - action_sequencing.action_sequencer - INFO - Generating fallback action sequence with available actions
2025-12-01 09:19:31,322 - action_sequencing.action_sequencer - INFO - Successfully generated action sequence with 1 actions
   ✓ 动作序列模块对无效转换格式容错通过

7. 性能与交互延迟测试...
2025-12-01 09:19:31,324 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-12-01 09:19:31,324 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-12-01 09:19:31,324 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-12-01 09:19:31,324 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-12-01 09:19:31,324 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1764551971324417, creating fallback
2025-12-01 09:19:31,324 - transition_modeling.transition_modeler - INFO - Modeling completed: 1 final valid sequences
2025-12-01 09:20:16,343 - action_sequencing.action_sequencer - WARNING - Generated sequence failed validation: ["Goal not fully achieved. Unmet goals: ['book_position (expected: shelf_3, actual: desk)']", 'No official BEHAVIOR actions found in sequ
ence']                                                                                                                                                                                                                                                  2025-12-01 09:20:16,343 - action_sequencing.action_sequencer - INFO - Generating fallback action sequence with available actions
2025-12-01 09:20:16,343 - action_sequencing.action_sequencer - INFO - Successfully generated action sequence with 1 actions
   交互延迟: {
  "goal_to_subgoal_latency": 0.001497030258178711,
  "transition_modeling_latency": 0.0003848075866699219,
  "action_sequencing_latency": 45.01889395713806
}

================================================================================
增强版四模块集成测试报告
================================================================================
测试总览: 4/7 测试通过

数据传输格式校验结果:
   goal_to_subgoal: ✓ 正常
   subgoal_to_transition: ✓ 正常
   transition_to_action: ✗ 异常

详细测试结果:

1. module_initialization_enhanced: ✓ 成功
   消息: 模块初始化验证: 4/4 模块通过
   详情: {
  "goal_interpretation": true,
  "subgoal_decomposition": true,
  "transition_modeling": true,
  "action_sequencing": true
}

2. goal_to_subgoal_flow: ✓ 成功
   消息: 成功传输并分解为7个子目标

3. subgoal_to_transition_interface: ✓ 成功
   消息: 生成1个转换序列

4. transition_to_action_param_pass: ✗ 失败
   消息: move动作参数传递错误

5. end_to_end_with_validation: ✗ 失败
   消息: 存在数据格式不一致问题

6. data_fault_tolerance: ✓ 成功
   消息: 数据容错测试: 4/4 项通过
   详情: {
  "invalid_goal_input": true,
  "empty_ltl_input": true,
  "empty_transitions_input": true,
  "invalid_transitions_format": true
}

7. performance_with_latency: ✗ 失败
   消息: 模块交互延迟测试完成
   详情: {
  "latency_data": {
    "goal_to_subgoal_latency": 0.001497030258178711,
    "transition_modeling_latency": 0.0003848075866699219,
    "action_sequencing_latency": 45.01889395713806
  },
  "threshold_checks": {
    "goal_to_subgoal_latency": true,
    "transition_modeling_latency": true,
    "action_sequencing_latency": false
  }
}

================================================================================
测试完成                                                                    耗时: 225.12s
