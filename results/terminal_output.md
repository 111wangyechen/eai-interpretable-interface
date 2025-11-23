python combine_results_en.py --batch sample_goals_en.json --output-dir ./results
✓ All four modules imported successfully
================================================================================
EAI Challenge Submission Script
Integrated Interface for Embodied Agents
================================================================================

============================================================
Starting batch processing
Goals file: sample_goals_en.json
Output directory: ./results
============================================================
Loaded 20 goals for processing

Processing goal 1/20: Make coffee in the kitchen

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,065 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,065 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Make coffee in the kitchen
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: make_coffee
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,068 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Make coffee in the kitchen
2025-11-23 16:16:59,068 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: make_coffee
2025-11-23 16:16:59,068 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,068 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,069 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,069 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,069 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819064_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,069 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,069 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,069 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,069 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,069 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819069371, creating fallback
2025-11-23 16:16:59,069 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819069371 failed LTL validation
2025-11-23 16:16:59,069 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819064_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,072 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 2/20: Wash clothes and hang them to dry

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,072 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,072 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,072 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,072 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,072 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,072 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,072 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Wash clothes and hang them to dry
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: wash_clothes
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,072 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Wash clothes and hang them to dry
2025-11-23 16:16:59,073 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: wash_clothes
2025-11-23 16:16:59,073 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,073 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,073 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,073 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,073 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819072_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,073 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,073 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,073 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,073 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,073 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819073410, creating fallback
2025-11-23 16:16:59,073 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819073410 failed LTL validation
2025-11-23 16:16:59,073 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819072_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,075 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 3/20: Clean the living room and arrange the sofa cushions

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,075 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,075 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,075 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,075 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,076 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,076 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,076 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Clean the living room and arrange the sofa cushions
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: clean_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Clean the living room and arrange the sofa cushions
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: clean_the
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,076 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819075_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,076 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,076 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,076 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,076 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,076 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819076717, creating fallback
2025-11-23 16:16:59,076 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819076717 failed LTL validation
2025-11-23 16:16:59,076 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819075_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,078 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 4/20: Find my keys and take them to the bedroom

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,078 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,078 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,078 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,078 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,078 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,078 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,078 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Find my keys and take them to the bedroom
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: find_my
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,078 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Find my keys and take them to the bedroom
2025-11-23 16:16:59,079 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: find_my
2025-11-23 16:16:59,079 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,079 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,079 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,079 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,079 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819078_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,079 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,079 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,079 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,079 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,079 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819079749, creating fallback
2025-11-23 16:16:59,079 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819079749 failed LTL validation
2025-11-23 16:16:59,079 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819078_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,081 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 5/20: Prepare a sandwich for lunch

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,081 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,081 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,081 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,081 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,081 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,081 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,081 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Prepare a sandwich for lunch
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: prepare_a
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Prepare a sandwich for lunch
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: prepare_a
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,082 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819081_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,082 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,082 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,082 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,082 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,082 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819082538, creating fallback
2025-11-23 16:16:59,082 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819082538 failed LTL validation
2025-11-23 16:16:59,082 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819081_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,084 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 6/20: Read a book and then turn off the lights

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,084 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,084 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,084 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,084 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,084 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,084 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,084 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Read a book and then turn off the lights
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: read_a
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,084 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Read a book and then turn off the lights
2025-11-23 16:16:59,084 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: read_a
2025-11-23 16:16:59,084 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,084 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,084 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,085 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,085 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819084_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,085 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,085 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,085 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,085 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,085 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819085191, creating fallback
2025-11-23 16:16:59,085 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819085191 failed LTL validation
2025-11-23 16:16:59,085 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819084_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,086 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 7/20: Open the window and let in some fresh air

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,087 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,087 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,087 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,087 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,087 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,087 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,087 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Open the window and let in some fresh air
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: open_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Open the window and let in some fresh air
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: open_the
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,087 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819087_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,087 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,087 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,087 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,087 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,087 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819087869, creating fallback
2025-11-23 16:16:59,088 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819087869 failed LTL validation
2025-11-23 16:16:59,088 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819087_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,089 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 8/20: Cook pasta and serve it with sauce

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,090 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,090 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,090 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,090 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,090 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Cook pasta and serve it with sauce
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: cook_pasta
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Cook pasta and serve it with sauce
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: cook_pasta
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,090 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819089_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,090 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,090 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819090810, creating fallback
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819090810 failed LTL validation
2025-11-23 16:16:59,090 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819089_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,092 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 9/20: Water the plants in the garden

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,092 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,092 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,092 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,092 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,092 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,092 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,092 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Water the plants in the garden
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: water_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Water the plants in the garden
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: water_the
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,093 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819092_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,093 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,093 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,093 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,093 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,093 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819093782, creating fallback
2025-11-23 16:16:59,093 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819093782 failed LTL validation
2025-11-23 16:16:59,093 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819092_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,095 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 10/20: Take out the trash and recycling

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,095 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,095 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,095 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,095 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,095 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,095 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,095 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Take out the trash and recycling
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: take_out
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Take out the trash and recycling
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: take_out
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,096 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819095_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,096 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,096 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,096 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,096 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,096 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819096515, creating fallback
2025-11-23 16:16:59,096 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819096515 failed LTL validation
2025-11-23 16:16:59,096 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819095_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,098 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 11/20: Charge my phone and laptop

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,098 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,098 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,098 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,098 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,098 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,098 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,098 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Charge my phone and laptop
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: charge_my
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,098 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Charge my phone and laptop
2025-11-23 16:16:59,098 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: charge_my
2025-11-23 16:16:59,098 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,098 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,098 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,099 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,099 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819098_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,099 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,099 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,099 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,099 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,099 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819099779, creating fallback
2025-11-23 16:16:59,099 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819099779 failed LTL validation
2025-11-23 16:16:59,100 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819098_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,102 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 12/20: Set the table for dinner with plates, forks, and glasses

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,102 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,102 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,102 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,102 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,102 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,102 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,102 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Set the table for dinner with plates, forks, and glasses
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: set_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Set the table for dinner with plates, forks, and glasses
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: set_the
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,102 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819102_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,103 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,103 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,103 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,103 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,103 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819103086, creating fallback
2025-11-23 16:16:59,103 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819103086 failed LTL validation
2025-11-23 16:16:59,103 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819102_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,104 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 13/20: Fold the laundry and put it away in the closet

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,105 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,105 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,105 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,105 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,105 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,105 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,105 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Fold the laundry and put it away in the closet
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: fold_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Fold the laundry and put it away in the closet
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: fold_the
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,105 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819105_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,106 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,106 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,106 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,106 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,106 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819106008, creating fallback
2025-11-23 16:16:59,106 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819106008 failed LTL validation
2025-11-23 16:16:59,106 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819105_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,107 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 14/20: Check the mail and sort it into important and junk

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,108 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,108 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,108 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,108 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,108 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,108 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,108 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Check the mail and sort it into important and junk
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: check_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Check the mail and sort it into important and junk
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: check_the
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,108 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819108_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,108 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,109 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,109 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,109 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,109 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819108959, creating fallback
2025-11-23 16:16:59,109 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819108959 failed LTL validation
2025-11-23 16:16:59,109 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819108_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,110 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 15/20: Vacuum the carpet and then dust the furniture

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,111 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,111 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,111 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,111 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,111 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,111 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,111 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Vacuum the carpet and then dust the furniture
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: vacuum_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Vacuum the carpet and then dust the furniture
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: vacuum_the
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,111 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819110_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,112 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,112 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,112 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,112 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,112 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819112238, creating fallback
2025-11-23 16:16:59,112 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819112238 failed LTL validation
2025-11-23 16:16:59,112 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819110_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,114 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 16/20: Mix flour, sugar, and eggs to make cake batter

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,114 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,114 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,114 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,114 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,114 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,114 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,114 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Mix flour, sugar, and eggs to make cake batter
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: mix_flour
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,114 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Mix flour, sugar, and eggs to make cake batter
2025-11-23 16:16:59,114 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: mix_flour
2025-11-23 16:16:59,114 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,115 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,115 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,115 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,115 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819114_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,115 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,115 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,115 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,115 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,115 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819115806, creating fallback
2025-11-23 16:16:59,116 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819115806 failed LTL validation
2025-11-23 16:16:59,116 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819114_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,117 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 17/20: Drive to the grocery store and buy milk and bread

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,118 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,118 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,118 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,118 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,118 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,118 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,118 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Drive to the grocery store and buy milk and bread
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: drive_to
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Drive to the grocery store and buy milk and bread
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: drive_to
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,118 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819117_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,119 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,119 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,119 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,119 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,119 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819119060, creating fallback
2025-11-23 16:16:59,119 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819119060 failed LTL validation
2025-11-23 16:16:59,119 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819117_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,121 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 18/20: Answer the phone and take a message

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,121 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,121 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,121 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,121 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,121 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,122 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,122 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Answer the phone and take a message
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: answer_the
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Answer the phone and take a message
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: answer_the
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,122 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819121_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,122 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,122 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,122 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,122 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,122 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819122768, creating fallback
2025-11-23 16:16:59,122 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819122768 failed LTL validation
2025-11-23 16:16:59,122 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819121_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,125 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 19/20: Turn on the TV and watch the news

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,125 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,125 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,125 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,125 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,125 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,125 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,125 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Turn on the TV and watch the news
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: turn_on
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,125 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Turn on the TV and watch the news
2025-11-23 16:16:59,125 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: turn_on
2025-11-23 16:16:59,125 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,125 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,125 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,125 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,126 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819125_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,126 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,126 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,126 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,126 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,126 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819126171, creating fallback
2025-11-23 16:16:59,126 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819126171 failed LTL validation
2025-11-23 16:16:59,126 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819125_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,128 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

Processing goal 20/20: Write a shopping list for tomorrow

============================================================
Initializing modules...
============================================================
2025-11-23 16:16:59,128 - transition_modeling.transition_predictor - INFO - Transition Predictor initialized
2025-11-23 16:16:59,128 - transition_modeling.transition_validator - INFO - Transition Validator initialized
2025-11-23 16:16:59,128 - transition_modeling.logic_guard - INFO - LogicGuard initialized
2025-11-23 16:16:59,128 - transition_modeling.transition_modeler - INFO - LogicGuard module initialized successfully
2025-11-23 16:16:59,128 - transition_modeling.transition_modeler - INFO - Transition Modeler initialized
2025-11-23 16:16:59,128 - AuDeRe - INFO - AuDeRe engine initialized
2025-11-23 16:16:59,128 - action_sequencing.action_sequencer - INFO - AuDeRe module initialized successfully
✓ All modules initialized successfully

============================================================
Processing goal: Write a shopping list for tomorrow
============================================================

Step 1: Goal Interpretation
✓ Goal interpretation successful
  LTL Formula: write_a
  Formula valid: True

Step 2: Subgoal Decomposition
2025-11-23 16:16:59,128 - subgoal_decomposition.subgoal_ltl_integration - INFO - 开始处理目标: Write a shopping list for tomorrow
2025-11-23 16:16:59,129 - subgoal_decomposition.subgoal_ltl_integration - INFO - 生成的LTL公式: write_a
2025-11-23 16:16:59,129 - subgoal_decomposition.subgoal_ltl_integration - INFO - 分解得到 1 个子目标
2025-11-23 16:16:59,129 - subgoal_decomposition.subgoal_ltl_integration - INFO - 验证发现 1 个问题
2025-11-23 16:16:59,129 - subgoal_decomposition.subgoal_ltl_integration - INFO - 优化完成，性能提升: 0.0%
2025-11-23 16:16:59,129 - subgoal_decomposition.subgoal_ltl_integration - INFO - 复杂度分析完成: low
2025-11-23 16:16:59,129 - subgoal_decomposition.subgoal_ltl_integration - INFO - 目标处理完成
✓ Subgoal decomposition successful, generated 1 subgoals
  Subgoal decomposition results saved to: ./results/submission_1763885819128_subgoals.json

Step 3: Transition Modeling
  Number of available transitions: 4
2025-11-23 16:16:59,129 - transition_modeling.transition_modeler - INFO - Processing modeling request with 4 available transitions
2025-11-23 16:16:59,129 - transition_modeling.transition_predictor - INFO - Generated 0 transition predictions
2025-11-23 16:16:59,129 - transition_modeling.transition_predictor - INFO - Generated 0 possible sequences
2025-11-23 16:16:59,129 - transition_modeling.transition_modeler - INFO - Predictor generated 0 raw sequences
2025-11-23 16:16:59,129 - transition_modeling.transition_modeler - WARNING - No sequences were generated for request request_1763885819129378, creating fallback
2025-11-23 16:16:59,129 - transition_modeling.transition_modeler - WARNING - Sequence empty_fallback_sequence_request_1763885819129378 failed LTL validation
2025-11-23 16:16:59,129 - transition_modeling.transition_modeler - INFO - Modeling completed: 0 final valid sequences
✓ State transition modeling completed, generated 0 sequences
  State transition modeling results saved to: ./results/submission_1763885819128_modeling.json

Step 4: Action Sequencing
2025-11-23 16:16:59,131 - action_sequencing.action_sequencer - WARNING - Failed to generate action sequence: No solution found within time/depth limits
✗ Action sequence generation failed: None

================================================================================
Batch Processing Summary
Total goals processed: 20
Successful: 0
Failed: 20
Success rate: 0.0%
================================================================================
Batch summary saved to: ./results/batch_summary_1763885819131.json

✅ Script execution completed
