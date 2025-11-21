(eai-eval) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface$ python inspect_parquet_datasets.py 
🚀 Parquet Dataset Inspection Tool
==================================================

----------------------------------------------------------------------

🔍 Inspecting file: /home/yeah/eai-interpretable-interface/data/behavior-00000-of-00001.parquet
📏 File size: 0.1 MB
📖 Reading Parquet file...
📊 Shape: (100, 8) (rows × columns)
📋 Columns: scene_id, task_id, task_name, natural_language_description, original_goal, tl_goal, action_trajectory, transition_model
🔢 Data types: scene_id: object, task_id: object, task_name: object, natural_language_description: object, original_goal: object, tl_goal: object, action_trajectory: object, transition_model: object

📈 Column statistics:
  🔹 scene_id:
     - Non-null: 100/100 (100.0%)
     - Unique values: 1
  🔹 task_id:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 task_name:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 natural_language_description:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 original_goal:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 tl_goal:
     - Non-null: 100/100 (100.0%)
     - Unique values: 99
  🔹 action_trajectory:
     - Non-null: 100/100 (100.0%)
     - Unique values: 99
  🔹 transition_model:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100

🔍 Sample data preview:
  scene_id: default | task_id: assembling_gift_baskets_0_Beec... | task_name: assembling_gift_baskets
  scene_id: default | task_id: brushing_lint_off_clothing_0_P... | task_name: brushing_lint_off_clothing
  scene_id: default | task_id: boxing_books_up_for_storage_0_... | task_name: boxing_books_up_for_storage
  scene_id: default | task_id: collecting_aluminum_cans_0_Ihl... | task_name: collecting_aluminum_cans
  scene_id: default | task_id: mopping_floors_0_Benevolence_2... | task_name: mopping_floors

----------------------------------------------------------------------

🔍 Inspecting file: /home/yeah/eai-interpretable-interface/data/virtualhome-00000-of-00001.parquet
📏 File size: 0.11 MB
📖 Reading Parquet file...
📊 Shape: (338, 8) (rows × columns)
📋 Columns: scene_id, task_id, task_name, natural_language_description, original_goal, tl_goal, action_trajectory, transition_model
🔢 Data types: scene_id: object, task_id: object, task_name: object, natural_language_description: object, original_goal: object, tl_goal: object, action_trajectory: object, transition_model: object

📈 Column statistics:
  🔹 scene_id:
     - Non-null: 338/338 (100.0%)
     - Unique values: 1
  🔹 task_id:
     - Non-null: 338/338 (100.0%)
     - Unique values: 338
  🔹 task_name:
     - Non-null: 338/338 (100.0%)
     - Unique values: 26
  🔹 natural_language_description:
     - Non-null: 338/338 (100.0%)
     - Unique values: 334
  🔹 original_goal:
     - Non-null: 338/338 (100.0%)
     - Unique values: 82
  🔹 tl_goal:
     - Non-null: 338/338 (100.0%)
     - Unique values: 92
  🔹 action_trajectory:
     - Non-null: 338/338 (100.0%)
     - Unique values: 287
  🔹 transition_model:
     - Non-null: 338/338 (100.0%)
     - Unique values: 283

🔍 Sample data preview:
  scene_id: scene_1 | task_id: 27_2 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 417_1 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 850_1 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 954_2 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 11_1 | task_name: Turn on light

======================================================================

🔄 Comparing files: behavior-00000-of-00001.parquet vs virtualhome-00000-of-00001.parquet

🔍 Inspecting file: /home/yeah/eai-interpretable-interface/data/behavior-00000-of-00001.parquet
📏 File size: 0.1 MB
📖 Reading Parquet file...
📊 Shape: (100, 8) (rows × columns)
📋 Columns: scene_id, task_id, task_name, natural_language_description, original_goal, tl_goal, action_trajectory, transition_model
🔢 Data types: scene_id: object, task_id: object, task_name: object, natural_language_description: object, original_goal: object, tl_goal: object, action_trajectory: object, transition_model: object

📈 Column statistics:
  🔹 scene_id:
     - Non-null: 100/100 (100.0%)
     - Unique values: 1
  🔹 task_id:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 task_name:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 natural_language_description:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 original_goal:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100
  🔹 tl_goal:
     - Non-null: 100/100 (100.0%)
     - Unique values: 99
  🔹 action_trajectory:
     - Non-null: 100/100 (100.0%)
     - Unique values: 99
  🔹 transition_model:
     - Non-null: 100/100 (100.0%)
     - Unique values: 100

🔍 Sample data preview:
  scene_id: default | task_id: assembling_gift_baskets_0_Beec... | task_name: assembling_gift_baskets
  scene_id: default | task_id: brushing_lint_off_clothing_0_P... | task_name: brushing_lint_off_clothing
  scene_id: default | task_id: boxing_books_up_for_storage_0_... | task_name: boxing_books_up_for_storage
  scene_id: default | task_id: collecting_aluminum_cans_0_Ihl... | task_name: collecting_aluminum_cans
  scene_id: default | task_id: mopping_floors_0_Benevolence_2... | task_name: mopping_floors

🔍 Inspecting file: /home/yeah/eai-interpretable-interface/data/virtualhome-00000-of-00001.parquet
📏 File size: 0.11 MB
📖 Reading Parquet file...
📊 Shape: (338, 8) (rows × columns)
📋 Columns: scene_id, task_id, task_name, natural_language_description, original_goal, tl_goal, action_trajectory, transition_model
🔢 Data types: scene_id: object, task_id: object, task_name: object, natural_language_description: object, original_goal: object, tl_goal: object, action_trajectory: object, transition_model: object

📈 Column statistics:
  🔹 scene_id:
     - Non-null: 338/338 (100.0%)
     - Unique values: 1
  🔹 task_id:
     - Non-null: 338/338 (100.0%)
     - Unique values: 338
  🔹 task_name:
     - Non-null: 338/338 (100.0%)
     - Unique values: 26
  🔹 natural_language_description:
     - Non-null: 338/338 (100.0%)
     - Unique values: 334
  🔹 original_goal:
     - Non-null: 338/338 (100.0%)
     - Unique values: 82
  🔹 tl_goal:
     - Non-null: 338/338 (100.0%)
     - Unique values: 92
  🔹 action_trajectory:
     - Non-null: 338/338 (100.0%)
     - Unique values: 287
  🔹 transition_model:
     - Non-null: 338/338 (100.0%)
     - Unique values: 283

🔍 Sample data preview:
  scene_id: scene_1 | task_id: 27_2 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 417_1 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 850_1 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 954_2 | task_name: Wash clothes
  scene_id: scene_1 | task_id: 11_1 | task_name: Turn on light

📊 Comparison Results:
🔢 Row count difference: 238 rows
📋 Common columns: 8
📋 Columns only in first file: 0
📋 Columns only in second file: 0

🔍 Common columns:
  - task_name
  - natural_language_description
  - transition_model
  - task_id
  - action_trajectory
  - tl_goal
  - original_goal
  - scene_id

💾 Results saved to: /home/yeah/eai-interpretable-interface/parquet_inspection_results.json

--------------------------------------------------
✅ Dataset inspection completed
📋 Summary:
  - behavior-00000-of-00001.parquet: 100 rows, 8 columns
  - virtualhome-00000-of-00001.parquet: 338 rows, 8 columns