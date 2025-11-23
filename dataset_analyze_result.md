(eai-eval) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface$ python analyze_datasets.py 
EAI Challenge 数据集分析工具
用于分析behavior和virtualhome数据集
================================================================================

================================================================================
                                    数据目录结构分析                                    
================================================================================
✓ 找到数据目录: /home/yeah/eai-interpretable-interface/data
✓ 目录中的文件数量: 3

文件列表:
  1. README.md (0.00 MB)
  2. behavior-00000-of-00001.parquet (0.10 MB)
  3. virtualhome-00000-of-00001.parquet (0.11 MB)

================================================================================
                                   README文件分析                                   
================================================================================
✓ 找到README.md文件: /home/yeah/eai-interpretable-interface/data/README.md

README内容:
---
# 数据文件

## 模块说明
数据文件

## 文件列表
- behavior-00000-of-00001.parquet
- virtualhome-00000-of-00001.parquet

---
✓ README内容似乎完整

================================================================================
                                  PARQUET文件分析                                   
================================================================================
✓ 找到 2 个.parquet文件

--------------------------------------------------------------------------------
                     分析文件: behavior-00000-of-00001.parquet                      
--------------------------------------------------------------------------------
✓ 成功读取文件: behavior-00000-of-00001.parquet
✓ 数据行数: 100
✓ 数据列数: 8
✓ 文件大小: 0.10 MB

列信息:
  1. scene_id (object)
  2. task_id (object)
  3. task_name (object)
  4. natural_language_description (object)
  5. original_goal (object)
  6. tl_goal (object)
  7. action_trajectory (object)
  8. transition_model (object)

列统计信息:
  scene_id: 非空值=100, 唯一值=1
    示例值: default
  task_id: 非空值=100, 唯一值=100
    示例值: assembling_gift_baskets_0_Beechwood_0_int_0_2021-10-26_12-46-37, brushing_lint_off_clothing_0_Pomaria_2_int_0_2021-06-04_17-41-56, boxing_books_up_for_storage_0_Benevolence_1_int_0_2021-09-10_15-35-47, ...
  task_name: 非空值=100, 唯一值=100
    示例值: assembling_gift_baskets, brushing_lint_off_clothing, boxing_books_up_for_storage, ...
  natural_language_description: 非空值=100, 唯一值=100
    示例值: Put one candle, one cheese, one cookie, and one bow into each basket., Check every sweater for lint, make sure none of them are dusty, and put them on the bed., Place the books into the carton for storage., ...
  original_goal: 非空值=100, 唯一值=100
    示例值: (define (problem assembling_gift_baskets_0)
    (:domain igibson)

    (:objects
        basket.n.01_1 basket.n.01_2 basket.n.01_3 basket.n.01_4 - basket.n.01
        floor.n.01_1 - floor.n.01
        candle.n.01_1 candle.n.01_2 candle.n.01_3 candle.n.01_4 - candle.n.01
        cookie.n.01_1 cookie.n.01_2 cookie.n.01_3 cookie.n.01_4 - cookie.n.01
        cheese.n.01_1 cheese.n.01_2 cheese.n.01_3 cheese.n.01_4 - cheese.n.01
        bow.n.08_1 bow.n.08_2 bow.n.08_3 bow.n.08_4 - bow.n.08
        table.n.02_1 table.n.02_2 - table.n.02
        agent.n.01_1 - agent.n.01
    )
    
    (:init 
        (onfloor basket.n.01_1 floor.n.01_1) 
        (onfloor basket.n.01_2 floor.n.01_1) 
        (onfloor basket.n.01_3 floor.n.01_1) 
        (onfloor basket.n.01_4 floor.n.01_1) 
        (ontop candle.n.01_1 table.n.02_1) 
        (ontop candle.n.01_2 table.n.02_1) 
        (ontop candle.n.01_3 table.n.02_1) 
        (ontop candle.n.01_4 table.n.02_1) 
        (ontop cookie.n.01_1 table.n.02_1) 
        (ontop cookie.n.01_2 table.n.02_1) 
        (ontop cookie.n.01_3 table.n.02_1) 
        (ontop cookie.n.01_4 table.n.02_1) 
        (ontop cheese.n.01_1 table.n.02_2) 
        (ontop cheese.n.01_2 table.n.02_2) 
        (ontop cheese.n.01_3 table.n.02_2) 
        (ontop cheese.n.01_4 table.n.02_2) 
        (ontop bow.n.08_1 table.n.02_2) 
        (ontop bow.n.08_2 table.n.02_2) 
        (ontop bow.n.08_3 table.n.02_2) 
        (ontop bow.n.08_4 table.n.02_2) 
        (inroom floor.n.01_1 living_room) 
        (inroom table.n.02_1 living_room) 
        (inroom table.n.02_2 living_room) 
        (onfloor agent.n.01_1 floor.n.01_1)
    )
    
    (:goal 
        (and 
            (forpairs 
                (?basket.n.01 - basket.n.01) 
                (?candle.n.01 - candle.n.01) 
                (inside ?candle.n.01 ?basket.n.01)
            ) 
            (forpairs 
                (?basket.n.01 - basket.n.01) 
                (?cheese.n.01 - cheese.n.01) 
                (inside ?cheese.n.01 ?basket.n.01)
            ) 
            (forpairs 
                (?basket.n.01 - basket.n.01) 
                (?cookie.n.01 - cookie.n.01) 
                (inside ?cookie.n.01 ?basket.n.01)
            ) 
            (forpairs 
                (?basket.n.01 - basket.n.01) 
                (?bow.n.08 - bow.n.08) 
                (inside ?bow.n.08 ?basket.n.01)
            )
        )
    )
), (define (problem brushing_lint_off_clothing_0)
    (:domain igibson)

    (:objects
        sweater.n.01_1 sweater.n.01_2 sweater.n.01_3 sweater.n.01_4 - sweater.n.01
        floor.n.01_1 - floor.n.01
        bed.n.01_1 - bed.n.01
        scrub_brush.n.01_1 - scrub_brush.n.01
        agent.n.01_1 - agent.n.01
    )
    
    (:init 
        (onfloor sweater.n.01_1 floor.n.01_1) 
        (onfloor sweater.n.01_2 floor.n.01_1) 
        (ontop sweater.n.01_3 bed.n.01_1) 
        (ontop sweater.n.01_4 bed.n.01_1) 
        (dusty sweater.n.01_1) 
        (dusty sweater.n.01_2) 
        (dusty sweater.n.01_3) 
        (dusty sweater.n.01_4) 
        (onfloor scrub_brush.n.01_1 floor.n.01_1) 
        (not 
            (dusty scrub_brush.n.01_1)
        ) 
        (inroom floor.n.01_1 bedroom) 
        (inroom bed.n.01_1 bedroom) 
        (onfloor agent.n.01_1 floor.n.01_1)
    )
    
    (:goal 
        (and 
            (forall 
                (?sweater.n.01 - sweater.n.01) 
                (not 
                    (dusty ?sweater.n.01)
                )
            ) 
            (forall 
                (?sweater.n.01 - sweater.n.01) 
                (ontop ?sweater.n.01 ?bed.n.01_1)
            )
        )
    )
), (define (problem boxing_books_up_for_storage_0)
    (:domain igibson)

    (:objects
        book.n.02_1 book.n.02_2 book.n.02_3 book.n.02_4 book.n.02_5 book.n.02_6 book.n.02_7 - book.n.02
        floor.n.01_1 - floor.n.01
        shelf.n.01_1 - shelf.n.01
        carton.n.02_1 - carton.n.02
        agent.n.01_1 - agent.n.01
    )
    
    (:init 
        (onfloor book.n.02_1 floor.n.01_1) 
        (onfloor book.n.02_2 floor.n.01_1) 
        (onfloor book.n.02_3 floor.n.01_1) 
        (onfloor book.n.02_4 floor.n.01_1) 
        (onfloor book.n.02_5 floor.n.01_1) 
        (ontop book.n.02_6 shelf.n.01_1) 
        (ontop book.n.02_7 shelf.n.01_1) 
        (onfloor carton.n.02_1 floor.n.01_1) 
        (inroom floor.n.01_1 living_room) 
        (inroom shelf.n.01_1 living_room) 
        (onfloor agent.n.01_1 floor.n.01_1)
    )
    
    (:goal 
        (and 
            (forall 
                (?book.n.02 - book.n.02) 
                (inside ?book.n.02 ?carton.n.02_1)
            )
        )
    )
), ...
  tl_goal: 非空值=100, 唯一值=99
    示例值: forall x0. (not basket_n_01(x0) or forn 1. x1. (not candle_n_01(x1) or inside(x1, x0))) and forall x1. (not candle_n_01(x1) or forn 1. x0. (not basket_n_01(x0) or inside(x1, x0))) and forall x0. (not basket_n_01(x0) or forn 1. x1. (not cheese_n_01(x1) or inside(x1, x0))) and forall x1. (not cheese_n_01(x1) or forn 1. x0. (not basket_n_01(x0) or inside(x1, x0))) and forall x0. (not basket_n_01(x0) or forn 1. x1. (not cookie_n_01(x1) or inside(x1, x0))) and forall x1. (not cookie_n_01(x1) or forn 1. x0. (not basket_n_01(x0) or inside(x1, x0))) and forall x0. (not basket_n_01(x0) or forn 1. x1. (not bow_n_08(x1) or inside(x1, x0))) and forall x1. (not bow_n_08(x1) or forn 1. x0. (not basket_n_01(x0) or inside(x1, x0))), forall x0. (not sweater_n_01(x0) or (not dusty(x0))) and forall x0. (not sweater_n_01(x0) or ontop(x0, bed.11)), forall x0. (not book_n_02(x0) or inside(x0, carton.66)), ...
  action_trajectory: 非空值=100, 唯一值=99
    示例值: [{'action': 'RIGHT_GRASP', 'object': 'bow_0'}, {'action': 'LEFT_GRASP', 'object': 'bow_1'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_0'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_1'}, {'action': 'RIGHT_GRASP', 'object': 'bow_2'}, {'action': 'LEFT_GRASP', 'object': 'bow_3'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_2'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_3'}, {'action': 'RIGHT_GRASP', 'object': 'cheese_0'}, {'action': 'LEFT_GRASP', 'object': 'cheese_1'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_0'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_1'}, {'action': 'RIGHT_GRASP', 'object': 'cheese_2'}, {'action': 'LEFT_GRASP', 'object': 'cheese_3'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_2'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_3'}, {'action': 'RIGHT_GRASP', 'object': 'cookie_0'}, {'action': 'LEFT_GRASP', 'object': 'cookie_1'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_0'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_1'}, {'action': 'RIGHT_GRASP', 'object': 'cookie_2'}, {'action': 'LEFT_GRASP', 'object': 'cookie_3'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_2'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_3'}, {'action': 'RIGHT_GRASP', 'object': 'candle_0'}, {'action': 'LEFT_GRASP', 'object': 'candle_1'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_0'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_1'}, {'action': 'RIGHT_GRASP', 'object': 'candle_2'}, {'action': 'LEFT_GRASP', 'object': 'candle_3'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'basket_2'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'basket_3'}], [{'action': 'RIGHT_GRASP', 'object': 'scrub_brush_40'}, {'action': 'CLEAN', 'object': 'sweater_36'}, {'action': 'LEFT_GRASP', 'object': 'sweater_36'}, {'action': 'LEFT_PLACE_ONTOP', 'object': 'bed_11'}, {'action': 'CLEAN', 'object': 'sweater_37'}, {'action': 'LEFT_GRASP', 'object': 'sweater_37'}, {'action': 'LEFT_PLACE_ONTOP', 'object': 'bed_11'}, {'action': 'CLEAN', 'object': 'sweater_38'}, {'action': 'LEFT_GRASP', 'object': 'sweater_38'}, {'action': 'LEFT_PLACE_ONTOP', 'object': 'bed_11'}, {'action': 'CLEAN', 'object': 'sweater_39'}, {'action': 'LEFT_GRASP', 'object': 'sweater_39'}, {'action': 'LEFT_PLACE_ONTOP', 'object': 'bed_11'}], [{'action': 'RIGHT_GRASP', 'object': 'notebook_60'}, {'action': 'LEFT_GRASP', 'object': 'hardback_65'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'RIGHT_GRASP', 'object': 'hardback_64'}, {'action': 'LEFT_GRASP', 'object': 'notebook_59'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'RIGHT_GRASP', 'object': 'notebook_62'}, {'action': 'LEFT_GRASP', 'object': 'hardback_65'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'RIGHT_GRASP', 'object': 'notebook_63'}, {'action': 'LEFT_GRASP', 'object': 'notebook_61'}, {'action': 'RIGHT_PLACE_INSIDE', 'object': 'carton_66'}, {'action': 'LEFT_PLACE_INSIDE', 'object': 'carton_66'}], ...
  transition_model: 非空值=100, 唯一值=100
    示例值: (define (problem assembling_gift_baskets)
    (:domain igibson)
    (:objects agent_n_01_1 - agent basket_n_01_1 basket_n_01_2 - basket_n_01 bow_n_08_2 - bow_n_08 candle_n_01_1 - candle_n_01 cheese_n_01_1 - cheese_n_01 cookie_n_01_1 - cookie_n_01 floor_n_01_1 - floor_n_01 table_n_02_1 table_n_02_2 - table_n_02)
    (:init (onfloor basket_n_01_1 floor_n_01_1) (onfloor basket_n_01_2 floor_n_01_1) (ontop bow_n_08_2 table_n_02_2) (ontop candle_n_01_1 table_n_02_1) (ontop cheese_n_01_1 table_n_02_2) (ontop cookie_n_01_1 table_n_02_1) (same_obj basket_n_01_1 basket_n_01_1) (same_obj basket_n_01_2 basket_n_01_2) (same_obj bow_n_08_2 bow_n_08_2) (same_obj candle_n_01_1 candle_n_01_1) (same_obj cheese_n_01_1 cheese_n_01_1) (same_obj cookie_n_01_1 cookie_n_01_1) (same_obj floor_n_01_1 floor_n_01_1) (same_obj table_n_02_1 table_n_02_1) (same_obj table_n_02_2 table_n_02_2))
    (:goal (and (inside bow_n_08_2 basket_n_01_2) (inside candle_n_01_1 basket_n_01_2) (inside cheese_n_01_1 basket_n_01_1) (inside cookie_n_01_1 basket_n_01_1)))
), (define (problem brushing_lint_off_clothing)
    (:domain igibson)
    (:objects agent_n_01_1 - agent bed_n_01_1 - bed_n_01 floor_n_01_1 - floor_n_01 scrub_brush_n_01_1 - scrub_brush_n_01 sweater_n_01_1 sweater_n_01_2 sweater_n_01_3 sweater_n_01_4 - sweater_n_01)
    (:init (dusty sweater_n_01_1) (dusty sweater_n_01_2) (dusty sweater_n_01_3) (not (dusty scrub_brush_n_01_1)) (onfloor scrub_brush_n_01_1 floor_n_01_1) (onfloor sweater_n_01_1 floor_n_01_1) (onfloor sweater_n_01_2 floor_n_01_1) (ontop sweater_n_01_3 bed_n_01_1) (ontop sweater_n_01_4 bed_n_01_1) (same_obj bed_n_01_1 bed_n_01_1) (same_obj floor_n_01_1 floor_n_01_1) (same_obj scrub_brush_n_01_1 scrub_brush_n_01_1) (same_obj sweater_n_01_1 sweater_n_01_1) (same_obj sweater_n_01_2 sweater_n_01_2) (same_obj sweater_n_01_3 sweater_n_01_3) (same_obj sweater_n_01_4 sweater_n_01_4))
    (:goal (and (ontop sweater_n_01_1 bed_n_01_1) (not (dusty sweater_n_01_1)) (ontop sweater_n_01_2 bed_n_01_1) (ontop sweater_n_01_3 bed_n_01_1)))
), (define (problem boxing_books_up_for_storage)
    (:domain igibson)
    (:objects agent_n_01_1 - agent book_n_02_2 book_n_02_5 book_n_02_6 book_n_02_7 - book_n_02 carton_n_02_1 - carton_n_02 floor_n_01_1 - floor_n_01 shelf_n_01_1 - shelf_n_01)
    (:init (onfloor book_n_02_2 floor_n_01_1) (onfloor book_n_02_5 floor_n_01_1) (onfloor carton_n_02_1 floor_n_01_1) (ontop book_n_02_6 shelf_n_01_1) (ontop book_n_02_7 shelf_n_01_1) (same_obj book_n_02_2 book_n_02_2) (same_obj book_n_02_5 book_n_02_5) (same_obj book_n_02_6 book_n_02_6) (same_obj book_n_02_7 book_n_02_7) (same_obj carton_n_02_1 carton_n_02_1) (same_obj floor_n_01_1 floor_n_01_1) (same_obj shelf_n_01_1 shelf_n_01_1))
    (:goal (and (inside book_n_02_5 carton_n_02_1) (inside book_n_02_2 carton_n_02_1) (inside book_n_02_7 carton_n_02_1) (inside book_n_02_6 carton_n_02_1)))
), ...

前5行数据:
  scene_id                                            task_id  ...                                  action_trajectory                                   transition_model
0  default  assembling_gift_baskets_0_Beechwood_0_int_0_20...  ...  [{'action': 'RIGHT_GRASP', 'object': 'bow_0'},...  (define (problem assembling_gift_baskets)\n   ...
1  default  brushing_lint_off_clothing_0_Pomaria_2_int_0_2...  ...  [{'action': 'RIGHT_GRASP', 'object': 'scrub_br...  (define (problem brushing_lint_off_clothing)\n...
2  default  boxing_books_up_for_storage_0_Benevolence_1_in...  ...  [{'action': 'RIGHT_GRASP', 'object': 'notebook...  (define (problem boxing_books_up_for_storage)\...
3  default  collecting_aluminum_cans_0_Ihlen_1_int_0_2021-...  ...  [{'action': 'RIGHT_GRASP', 'object': 'pop_113'...  (define (problem collecting_aluminum_cans)\n  ...
4  default  mopping_floors_0_Benevolence_2_int_0_2021-10-2...  ...  [{'action': 'RIGHT_GRASP', 'object': 'bucket_0...  (define (problem mopping_floors)\n    (:domain...

[5 rows x 8 columns]

检查嵌套JSON数据:
  未发现嵌套JSON格式数据

--------------------------------------------------------------------------------
                    分析文件: virtualhome-00000-of-00001.parquet                    
--------------------------------------------------------------------------------
✓ 成功读取文件: virtualhome-00000-of-00001.parquet
✓ 数据行数: 338
✓ 数据列数: 8
✓ 文件大小: 0.11 MB

列信息:
  1. scene_id (object)
  2. task_id (object)
  3. task_name (object)
  4. natural_language_description (object)
  5. original_goal (object)
  6. tl_goal (object)
  7. action_trajectory (object)
  8. transition_model (object)

列统计信息:
  scene_id: 非空值=338, 唯一值=1
    示例值: scene_1
  task_id: 非空值=338, 唯一值=338
    示例值: 27_2, 417_1, 850_1, ...
  task_name: 非空值=338, 唯一值=26
    示例值: Wash clothes, Turn on light, Brush teeth, ...
  natural_language_description: 非空值=338, 唯一值=334
    示例值: Walk to the kitchen and find the basket of clothes. Put the soap and clothes into the washing machine. Turn on the washing machine., I will load the dirty clothes into the washing machine., Walk into laundry room. Open washing machine door. Put dirty clothes into washing machine. Measure laundry detergent and place into washing machine. Turn dial to appropriate wash setting. Power on., ...
  original_goal: 非空值=338, 唯一值=82
    示例值: {'actions': [], 'goal': [{'id': 1001, 'class_name': 'washing_machine', 'state': 'CLOSED'}, {'id': 1001, 'class_name': 'washing_machine', 'state': 'ON'}, {'id': 1001, 'class_name': 'washing_machine', 'state': 'PLUGGED_IN'}, {'from_id': 1003, 'relation_type': 'ON', 'to_id': 1001}, {'from_id': 1002, 'relation_type': 'ON', 'to_id': 1001}]}, {'actions': [], 'goal': [{'id': 1000, 'class_name': 'washing_machine', 'state': 'CLOSED'}, {'id': 1000, 'class_name': 'washing_machine', 'state': 'ON'}, {'id': 1000, 'class_name': 'washing_machine', 'state': 'PLUGGED_IN'}, {'from_id': 1001, 'relation_type': 'ON', 'to_id': 1000}, {'from_id': 1004, 'relation_type': 'ON', 'to_id': 1000}, {'from_id': 1003, 'relation_type': 'ON', 'to_id': 1000}, {'from_id': 1002, 'relation_type': 'ON', 'to_id': 1000}, {'from_id': 1005, 'relation_type': 'ON', 'to_id': 1000}]}, {'actions': [], 'goal': [{'id': 1000, 'class_name': 'washing_machine', 'state': 'CLOSED'}, {'id': 1000, 'class_name': 'washing_machine', 'state': 'ON'}, {'id': 1000, 'class_name': 'washing_machine', 'state': 'PLUGGED_IN'}, {'from_id': 1001, 'relation_type': 'ON', 'to_id': 1000}, {'from_id': 1002, 'relation_type': 'ON', 'to_id': 1000}]}, ...
  tl_goal: 非空值=338, 唯一值=92
    示例值: (CLOSED(washing_machine.1001) and ON(washing_machine.1001) and PLUGGED_IN(washing_machine.1001) and ONTOP(clothes_jacket.1003, washing_machine.1001) and ONTOP(soap.1002, washing_machine.1001)), (CLOSED(washing_machine.1000) and ON(washing_machine.1000) and PLUGGED_IN(washing_machine.1000) and ONTOP(clothes_pants.1001, washing_machine.1000) and ONTOP(clothes_shirt.1004, washing_machine.1000) and ONTOP(clothes_shirt.1003, washing_machine.1000) and ONTOP(clothes_pants.1002, washing_machine.1000) and ONTOP(soap.1005, washing_machine.1000)), (CLOSED(washing_machine.1000) and ON(washing_machine.1000) and PLUGGED_IN(washing_machine.1000) and ONTOP(clothes_pants.1001, washing_machine.1000) and ONTOP(laundry_detergent.1002, washing_machine.1000)), ...
  action_trajectory: 非空值=338, 唯一值=287
    示例值: ['[WALK] <dining_room> (201)', '[WALK] <basket_for_clothes> (1000)', '[FIND] <basket_for_clothes> (1000)', '[FIND] <washing_machine> (1001)', '[TURNTO] <washing_machine> (1001)', '[FIND] <soap> (1002)', '[GRAB] <soap> (1002)', '[OPEN] <washing_machine> (1001)', '[PUTBACK] <soap> (1002) <washing_machine> (1001)', '[FIND] <clothes_jacket> (1003)', '[GRAB] <clothes_jacket> (1003)', '[PUTBACK] <clothes_jacket> (1003) <washing_machine> (1001)', '[CLOSE] <washing_machine> (1001)', '[SWITCHON] <washing_machine> (1001)'], ['[FIND] <washing_machine> (1000)', '[OPEN] <washing_machine> (1000)', '[FIND] <clothes_pants> (1001)', '[GRAB] <clothes_pants> (1001)', '[PUTBACK] <clothes_pants> (1001) <washing_machine> (1000)', '[FIND] <clothes_pants> (2.1002)', '[GRAB] <clothes_pants> (2.1002)', '[PUTBACK] <clothes_pants> (2.1002) <washing_machine> (1000)', '[FIND] <clothes_shirt> (1003)', '[GRAB] <clothes_shirt> (1003)', '[PUTBACK] <clothes_shirt> (1003) <washing_machine> (1000)', '[FIND] <clothes_shirt> (2.1004)', '[GRAB] <clothes_shirt> (2.1004)', '[PUTBACK] <clothes_shirt> (2.1004) <washing_machine> (1000)', '[FIND] <soap> (1005)', '[GRAB] <soap> (1005)', '[PUTBACK] <soap> (1005) <washing_machine> (1000)', '[CLOSE] <washing_machine> (1000)', '[SWITCHON] <washing_machine> (1000)'], ['[WALK] <bathroom> (1)', '[WALK] <washing_machine> (1000)', '[FIND] <washing_machine> (1000)', '[OPEN] <washing_machine> (1000)', '[FIND] <clothes_pants> (1001)', '[GRAB] <clothes_pants> (1001)', '[PUTBACK] <clothes_pants> (1001) <washing_machine> (1000)', '[CLOSE] <washing_machine> (1000)', '[FIND] <laundry_detergent> (1002)', '[GRAB] <laundry_detergent> (1002)', '[OPEN] <washing_machine> (1000)', '[PUTBACK] <laundry_detergent> (1002) <washing_machine> (1000)', '[CLOSE] <washing_machine> (1000)', '[SWITCHON] <washing_machine> (1000)'], ...
  transition_model: 非空值=338, 唯一值=283
    示例值: (define (problem Wash_clothes)
    (:domain virtualhome)
    (:objects
    character - character
    bathroom clothes_jacket washing_machine basket_for_clothes dining_room soap - object
)
    (:init
    (obj_next_to soap basket_for_clothes)
    (grabbable clothes_jacket)
    (off washing_machine)
    (movable clothes_jacket)
    (inside_room basket_for_clothes dining_room)
    (hangable clothes_jacket)
    (containers washing_machine)
    (plugged_in washing_machine)
    (can_open basket_for_clothes)
    (obj_next_to washing_machine basket_for_clothes)
    (inside_room washing_machine dining_room)
    (has_switch washing_machine)
    (obj_next_to basket_for_clothes soap)
    (grabbable basket_for_clothes)
    (movable soap)
    (has_plug washing_machine)
    (containers basket_for_clothes)
    (can_open washing_machine)
    (clothes clothes_jacket)
    (inside_room soap dining_room)
    (closed washing_machine)
    (clean washing_machine)
    (obj_inside basket_for_clothes basket_for_clothes)
    (inside_room clothes_jacket dining_room)
    (obj_next_to clothes_jacket basket_for_clothes)
    (obj_inside clothes_jacket washing_machine)
    (obj_ontop washing_machine basket_for_clothes)
    (recipient washing_machine)
    (obj_next_to basket_for_clothes washing_machine)
    (obj_next_to basket_for_clothes basket_for_clothes)
    (obj_next_to basket_for_clothes clothes_jacket)
    (inside character bathroom)
    (movable basket_for_clothes)
    (cream soap)
    (grabbable soap)
)
    (:goal
    (and
        (closed washing_machine)
        (on washing_machine)
        (plugged_in washing_machine)
        (obj_ontop soap washing_machine)
        (obj_ontop clothes_jacket washing_machine)
    )
)
    )
    , (define (problem Wash_clothes)
    (:domain virtualhome)
    (:objects
    character - character
    clothes_shirt clothes_pants soap washing_machine - object
)
    (:init
    (clothes clothes_pants)
    (movable clothes_pants)
    (obj_inside clothes_shirt washing_machine)
    (off washing_machine)
    (hangable clothes_shirt)
    (grabbable soap)
    (containers washing_machine)
    (plugged_in washing_machine)
    (has_switch washing_machine)
    (movable soap)
    (has_plug washing_machine)
    (obj_inside soap washing_machine)
    (can_open washing_machine)
    (closed washing_machine)
    (clean washing_machine)
    (grabbable clothes_pants)
    (grabbable clothes_shirt)
    (obj_inside clothes_pants washing_machine)
    (hangable clothes_pants)
    (recipient washing_machine)
    (clothes clothes_shirt)
    (cream soap)
    (movable clothes_shirt)
)
    (:goal
    (and
        (closed washing_machine)
        (on washing_machine)
        (plugged_in washing_machine)
        (obj_ontop soap washing_machine)
        (obj_ontop clothes_shirt washing_machine)
        (obj_ontop clothes_pants washing_machine)
    )
)
    )
    , (define (problem Wash_clothes)
    (:domain virtualhome)
    (:objects
    character - character
    bathroom clothes_pants washing_machine dining_room laundry_detergent - object
)
    (:init
    (clothes clothes_pants)
    (movable clothes_pants)
    (inside_room clothes_pants bathroom)
    (off washing_machine)
    (containers washing_machine)
    (plugged_in washing_machine)
    (has_switch washing_machine)
    (inside_room washing_machine bathroom)
    (movable laundry_detergent)
    (obj_next_to clothes_pants washing_machine)
    (has_plug washing_machine)
    (obj_next_to washing_machine clothes_pants)
    (can_open washing_machine)
    (closed washing_machine)
    (clean washing_machine)
    (grabbable clothes_pants)
    (pourable laundry_detergent)
    (obj_inside clothes_pants washing_machine)
    (hangable clothes_pants)
    (recipient washing_machine)
    (obj_next_to laundry_detergent washing_machine)
    (inside character dining_room)
    (obj_next_to washing_machine laundry_detergent)
    (inside_room laundry_detergent bathroom)
    (grabbable laundry_detergent)
)
    (:goal
    (and
        (closed washing_machine)
        (on washing_machine)
        (plugged_in washing_machine)
        (obj_ontop clothes_pants washing_machine)
        (obj_ontop laundry_detergent washing_machine)
    )
)
    )
    , ...

前5行数据:
  scene_id task_id  ...                                  action_trajectory                                   transition_model
0  scene_1    27_2  ...  ['[WALK] <dining_room> (201)', '[WALK] <basket...  (define (problem Wash_clothes)\n    (:domain v...
1  scene_1   417_1  ...  ['[FIND] <washing_machine> (1000)', '[OPEN] <w...  (define (problem Wash_clothes)\n    (:domain v...
2  scene_1   850_1  ...  ['[WALK] <bathroom> (1)', '[WALK] <washing_mac...  (define (problem Wash_clothes)\n    (:domain v...
3  scene_1   954_2  ...  ['[WALK] <basket_for_clothes> (1000)', '[WALK]...  (define (problem Wash_clothes)\n    (:domain v...
4  scene_1    11_1  ...  ['[WALK] <bedroom> (67)', '[WALK] <floor_lamp>...  (define (problem Turn_on_light)\n    (:domain ...

[5 rows x 8 columns]

检查嵌套JSON数据:
  未发现嵌套JSON格式数据

================================================================================
                                    生成数据集摘要                                     
================================================================================
✓ 已处理文件: behavior-00000-of-00001.parquet (100 行)
✓ 已处理文件: virtualhome-00000-of-00001.parquet (338 行)
✓ 数据集摘要已保存到: /home/yeah/eai-interpretable-interface/dataset_summary.json

================================================================================
                                    数据集分析完成                                     
================================================================================