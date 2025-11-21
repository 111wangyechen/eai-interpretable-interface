(eai-eval) yeah@yeah-VMware-Virtual-Platform:~/eai-interpretable-interface/goal_interpretation$ python test_interpretable_interpreter_english.py 
✅ Successfully imported InterPreT modules
🧪 InterPreT Interpretable Goal Interpreter Test Suite
============================================================
test_basic_interpretation (__main__.TestInterpretableGoalInterpreter)
Test basic interpretation functionality ... 自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data

🧪 Test 1: Basic Interpretation Functionality
✅ 'pick up the cup' interpreted successfully: (<goal_interpreter.LTLFormula object at 0x7bab082af880>, PDDLDomain(name='domain_1763713274', requirements=['strips', 'typing'], types=['object', 'location', 'agent'], predicates=[SymbolicPredicate(name='at', arguments=None, parameters=['agent', 'location'], arity=2, description='Agent is at location', confidence=1.0, examples=['agent at kitchen', 'robot at living room']), SymbolicPredicate(name='holding', arguments=None, parameters=['agent', 'object'], arity=2, description='Agent is holding object', confidence=1.0, examples=['holding cup', 'robot holding book']), SymbolicPredicate(name='on', arguments=None, parameters=['object', 'surface'], arity=2, description='Object is on surface', confidence=1.0, examples=['book on table', 'cup on counter']), SymbolicPredicate(name='is_clean', arguments=None, parameters=['object'], arity=1, description='Object is clean', confidence=1.0, examples=['table is clean', 'floor is clean'])], actions=[{'name': 'move', 'parameters': '?agent - agent ?from - location ?to - location', 'precondition': '(and (at ?agent ?from))', 'effect': '(and (not (at ?agent ?from)) (at ?agent ?to))'}, {'name': 'pick', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (on ?object ?location))', 'effect': '(and (not (on ?object ?location)) (holding ?agent ?object))'}, {'name': 'place', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (holding ?agent ?object))', 'effect': '(and (not (holding ?agent ?object)) (on ?object ?location))'}, {'name': 'clean', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (on ?object ?location))', 'effect': '(is_clean ?object)'}]))
✅ 'open the door' interpreted successfully: (<goal_interpreter.LTLFormula object at 0x7bab082af940>, PDDLDomain(name='domain_1763713274', requirements=['strips', 'typing'], types=['object', 'location', 'agent'], predicates=[SymbolicPredicate(name='at', arguments=None, parameters=['agent', 'location'], arity=2, description='Agent is at location', confidence=1.0, examples=['agent at kitchen', 'robot at living room']), SymbolicPredicate(name='holding', arguments=None, parameters=['agent', 'object'], arity=2, description='Agent is holding object', confidence=1.0, examples=['holding cup', 'robot holding book']), SymbolicPredicate(name='on', arguments=None, parameters=['object', 'surface'], arity=2, description='Object is on surface', confidence=1.0, examples=['book on table', 'cup on counter']), SymbolicPredicate(name='is_clean', arguments=None, parameters=['object'], arity=1, description='Object is clean', confidence=1.0, examples=['table is clean', 'floor is clean'])], actions=[{'name': 'move', 'parameters': '?agent - agent ?from - location ?to - location', 'precondition': '(and (at ?agent ?from))', 'effect': '(and (not (at ?agent ?from)) (at ?agent ?to))'}, {'name': 'pick', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (on ?object ?location))', 'effect': '(and (not (on ?object ?location)) (holding ?agent ?object))'}, {'name': 'place', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (holding ?agent ?object))', 'effect': '(and (not (holding ?agent ?object)) (on ?object ?location))'}, {'name': 'clean', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (on ?object ?location))', 'effect': '(is_clean ?object)'}]))
✅ 'walk to the kitchen' interpreted successfully: (<goal_interpreter.LTLFormula object at 0x7bab082af880>, PDDLDomain(name='domain_1763713274', requirements=['strips', 'typing'], types=['object', 'location', 'agent'], predicates=[SymbolicPredicate(name='at', arguments=None, parameters=['agent', 'location'], arity=2, description='Agent is at location', confidence=1.0, examples=['agent at kitchen', 'robot at living room']), SymbolicPredicate(name='holding', arguments=None, parameters=['agent', 'object'], arity=2, description='Agent is holding object', confidence=1.0, examples=['holding cup', 'robot holding book']), SymbolicPredicate(name='on', arguments=None, parameters=['object', 'surface'], arity=2, description='Object is on surface', confidence=1.0, examples=['book on table', 'cup on counter']), SymbolicPredicate(name='is_clean', arguments=None, parameters=['object'], arity=1, description='Object is clean', confidence=1.0, examples=['table is clean', 'floor is clean'])], actions=[{'name': 'move', 'parameters': '?agent - agent ?from - location ?to - location', 'precondition': '(and (at ?agent ?from))', 'effect': '(and (not (at ?agent ?from)) (at ?agent ?to))'}, {'name': 'pick', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (on ?object ?location))', 'effect': '(and (not (on ?object ?location)) (holding ?agent ?object))'}, {'name': 'place', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (holding ?agent ?object))', 'effect': '(and (not (holding ?agent ?object)) (on ?object ?location))'}, {'name': 'clean', 'parameters': '?agent - agent ?object - object ?location - location', 'precondition': '(and (at ?agent ?location) (on ?object ?location))', 'effect': '(is_clean ?object)'}]))
ok
test_feedback_learning (__main__.TestInterpretableGoalInterpreter)
Test feedback learning functionality ... 自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data

🧪 Test 2: Feedback Learning Functionality
✅ Feedback learning successful: SymbolicPredicate(name='is_red', arguments=None, parameters=['book'], arity=1, description='is_red predicate', confidence=0.9, examples=['put the red book on the shelf'])
ok
test_pddl_domain_generation (__main__.TestInterpretableGoalInterpreter)
Test PDDL domain generation functionality ... 自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data

🧪 Test 3: PDDL Domain Generation Functionality
✅ PDDL domain generation successful
ok
test_predicate_evolution (__main__.TestInterpretableGoalInterpreter)
Test predicate evolution functionality ... 自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data

🧪 Test 4: Predicate Evolution Functionality
✅ Predicate evolution successful, final predicate count: 3
ok
test_save_load_functionality (__main__.TestInterpretableGoalInterpreter)
Test save and load functionality ... 自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data

🧪 Test 6: Save and Load Functionality
✅ State saved successfully
自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data
✅ State loaded successfully
✅ Loading verification successful
ok
test_statistics_tracking (__main__.TestInterpretableGoalInterpreter)
Test statistics tracking functionality ... 自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data

🧪 Test 5: Statistics Tracking Functionality
✅ Statistics tracking successful
   Total tasks: 6
   Success rate: 100.00%
ok
test_end_to_end_workflow (__main__.TestInterPreTIntegration)
Test end-to-end workflow ... 
🧪 Test 7: End-to-End Workflow
自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data
✅ Step 1: Basic interpretation completed
✅ Step 2: Feedback learning completed
✅ Step 3: PDDL domain generation completed
✅ Step 4: Statistics update completed
✅ End-to-end workflow test passed
ok
test_error_handling (__main__.TestInterPreTIntegration)
Test error handling ... 
🧪 Test 8: Error Handling
自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data
✅ Correctly handled empty string input: Expected an exception for empty string input
✅ Invalid feedback correctly raised exception: 'float' object has no attribute 'lower'
✅ Error handling test passed
ok

----------------------------------------------------------------------
Ran 8 tests in 0.008s

OK

🚀 Performance Tests
----------------------------------------
自动定位到数据目录: /home/yeah/eai-interpretable-interface/goal_interpretation/../data
📊 Performance Test Results:
   Total tasks: 50
   Successful tasks: 50
   Total time: 0.003 seconds
   Average time: 0.000 seconds/task
   Success rate: 100.00%

============================================================
📊 Test Summary
============================================================
Tests run: 8
Failures: 0
Errors: 0

🎉 All tests passed! InterPreT integration successful!
🚀 You can start developing with InterPreT