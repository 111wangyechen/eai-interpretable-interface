(eai-eval) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface$ python goal_interpretation/example_usage.py 
=== Goal Interpretation Module Usage Example ===
This module can convert natural language goal descriptions into LTL formulas



--- Example 1 ---
Natural Language: Reach the kitchen
LTL Formula: (reach_kitchen -> F(locations_kitchen))
Semantic Structure:
  - Task Type: simple_task
  - Actions: [{'type': 'movement', 'verb': 'reach', 'object': 'kitchen', 'position': 0, 'context': 'reach the kitch'}]
  - Objects: [{'name': 'kitchen', 'category': 'locations', 'modifier': 'the ', 'position': 6, 'context': 'reach the kitchen'}]
  - Conditions: []
Validation Result: Valid Formula

--- Example 2 ---
Natural Language: First open the door, then enter the room
LTL Formula: ((((open -> F(enter)) -> F(locations_door)) -> F(locations_room)) -> F(relative_time_then))
Semantic Structure:
  - Task Type: sequential_task
  - Actions: [{'type': 'operation', 'verb': 'open', 'object': 'the', 'position': 6, 'context': 'first open the door ', 'sequential_order': 1, 'sequential_pattern': True}, {'type': 'movement', 'verb': 'enter', 'object': 'the', 'position': 28, 'context': ' open the door ,  then enter the room', 'sequential_order': 2, 'sequential_pattern': True}]
  - Objects: [{'name': 'door', 'category': 'locations', 'modifier': 'the ', 'position': 11, 'context': 'irst open the door ,  then e'}, {'name': 'room', 'category': 'locations', 'modifier': 'the ', 'position': 34, 'context': 'hen enter the room'}]
  - Conditions: []
Validation Result: Valid Formula

--- Example 3 ---
Natural Language: If you see a red light, stop moving forward
LTL Formula: ((see_red -> F(stop_forward)) -> F(appliances_light))
Semantic Structure:
  - Task Type: conditional_task
  - Actions: [{'type': 'observe', 'verb': 'see', 'object': 'red', 'position': 7, 'context': 'if you see a red lig'}, {'type': 'operation', 'verb': 'stop', 'object': 'forward', 'position': 26, 'context': ' light ,  stop moving fo'}]
  - Objects: [{'name': 'light', 'category': 'appliances', 'modifier': 'red ', 'position': 13, 'context': 'you see a red light ,  stop m'}]
  - Conditions: []
Validation Result: Valid Formula

--- Example 4 ---
Natural Language: Open the window and close the door at the same time
LTL Formula: F(open_window) & F(close_door) & F(locations_door)
Semantic Structure:
  - Task Type: complex_task
  - Actions: [{'type': 'operation', 'verb': 'open', 'object': 'window', 'position': 0, 'context': 'open the windo'}, {'type': 'operation', 'verb': 'close', 'object': 'door', 'position': 20, 'context': 'indow and close the door '}]
  - Objects: [{'name': 'door', 'category': 'locations', 'modifier': 'the ', 'position': 26, 'context': 'and close the door at the sa'}]
  - Conditions: []
Validation Result: Valid Formula

--- Example 5 ---
Natural Language: Eventually reach the destination
LTL Formula: (reach_destination -> F(relative_time_eventually))
Semantic Structure:
  - Task Type: simple_task
  - Actions: [{'type': 'movement', 'verb': 'reach', 'object': 'destination', 'position': 11, 'context': 'ventually reach the desti'}]
  - Objects: []
  - Conditions: []
Validation Result: Valid Formula

--- Example 6 ---
Natural Language: Always stay safe
LTL Formula: (stay_safe -> F(frequency_always))
Semantic Structure:
  - Task Type: simple_task
  - Actions: [{'type': 'wait', 'verb': 'stay', 'object': 'safe', 'position': 7, 'context': 'always stay safe'}]
  - Objects: []
  - Conditions: []
Validation Result: Valid Formula

--- Example 7 ---
Natural Language: First check if the environment is safe, if safe then proceed to the table, then pick up the key
LTL Formula: ((the_environment_is_safe -> check_if) & (safe -> pick_up))
Semantic Structure:
  - Task Type: conditional_task
  - Actions: [{'type': 'observe', 'verb': 'check', 'object': 'if', 'position': 6, 'context': 'first check if the en', 'sequential_order': 1, 'sequential_pattern': True}, {'type': 'take', 'verb': 'pick', 'object': 'up', 'position': 84, 'context': 'ed to the table ,  then pick up the ke', 'sequential_order': 2, 'sequential_pattern': True}]
  - Objects: [{'name': 'table', 'category': 'furniture', 'modifier': 'the ', 'position': 66, 'context': 'roceed to the table ,  then p'}, {'name': 'key', 'category': 'tools', 'modifier': 'the ', 'position': 92, 'context': 'n pick up the key'}]
  - Conditions: [{'type': 'complex_if_then', 'condition': 'the environment is safe', 'consequence': 'if safe', 'position': 12}, {'type': 'if_then', 'condition': 'safe', 'consequence': 'proceed to the table', 'position': 42}]
Validation Result: Valid Formula


=== Custom Input Example ===
Try entering a custom natural language goal description:

Please enter a natural language goal description (enter 'q' to exit): q

Thank you for using the Goal Interpretation Module!
=== Batch Processing Example ===

Goal 1:
  Natural Language: Collect all items and return to the starting point
  LTL Formula: F(collect_items) & F(return) & F(frequency_all)
  Task Type: complex_task

Goal 2:
  Natural Language: Reach the end without hitting any obstacles
  LTL Formula: (reach_end -> F(end_hitting))
  Task Type: complex_task

Goal 3:
  Natural Language: First turn off the lights, then lock the door, and finally leave the room
  LTL Formula: (((((turn_off -> F(lock)) -> F(locations_door)) -> F(locations_room)) -> F(relative_time_then)) -> F(relative_time_finally))
  Task Type: sequential_task

Goal 4:
  Natural Language: If danger is detected, evacuate immediately
  LTL Formula: F(relative_time_immediately)
  Task Type: conditional_task

Goal 5:
  Natural Language: Keep the environment clean and check equipment regularly
  LTL Formula: F(keep_environment) & F(check_clean) & F(check_regularly)
  Task Type: complex_task

=== Custom Configuration Example ===
Using the goal interpretation module for specific domain requirements

Domain Goal: The robot needs to first move to shelf A, then pick up the box, and finally place it on the conveyor belt
LTL Formula: ((((to_move -> F(pick_up)) -> F(containers_box)) -> F(relative_time_then)) -> F(relative_time_finally))

Domain Goal: The smart home system turns on the air conditioner when it detects the indoor temperature is above 26 degrees
LTL Formula: F(appliances_air conditioner)

Domain Goal: The autonomous vehicle stays in the lane and maintains a safe distance from the vehicle ahead
LTL Formula: F(task_autonomous_vehicle_stays)