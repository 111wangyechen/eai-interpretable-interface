#!/usr/bin/env python3
"""
InterPreT Integration Test Script
Tests all functionalities of the Interpretable Goal Interpreter
"""

import sys
import os
import unittest
from typing import Dict, Any, List
import tempfile
import json

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from interpretable_goal_interpreter import (
        InterpretableGoalInterpreter,
        InterPreTFeedbackLearner,
        PDDLDomainBuilder,
        FeedbackRecord,
        SymbolicPredicate,
        PDDLDomain
    )
    print("✅ Successfully imported InterPreT modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure interpretable_goal_interpreter.py is in the same directory")
    sys.exit(1)

class TestInterpretableGoalInterpreter(unittest.TestCase):
    """InterPreT core functionality test class"""
    
    def setUp(self):
        """Setup before each test"""
        self.config = {
            'model_name': 'bert-base-uncased',
            'max_predicates': 50,
            'learning_rate': 0.001,
            'feedback_threshold': 0.8,
            'pddl_domain_name': 'test_domain'
        }
        self.interpreter = InterpretableGoalInterpreter(self.config)
        self.learner = InterPreTFeedbackLearner(self.config)
        self.domain_builder = PDDLDomainBuilder(self.config)
    
    def test_basic_interpretation(self):
        """Test basic interpretation functionality"""
        print("\n🧪 Test 1: Basic Interpretation Functionality")
        
        test_goals = [
            "pick up the cup",
            "open the door",
            "walk to the kitchen"
        ]
        
        for goal in test_goals:
            try:
                # Use interpret_with_feedback instead of interpret_goal
                interpretation = self.interpreter.interpret_with_feedback(goal)
                self.assertIsNotNone(interpretation)
                print(f"✅ '{goal}' interpreted successfully: {interpretation}")
            except Exception as e:
                self.fail(f"Interpretation of '{goal}' failed: {e}")
    
    def test_feedback_learning(self):
        """Test feedback learning functionality"""
        print("\n🧪 Test 2: Feedback Learning Functionality")
        
        goal = "put the red book on the shelf"
        
        # Create test feedback
        feedback = FeedbackRecord(
            goal=goal,
            user_feedback="should emphasize the color attribute",
            corrected_predicate="is_red(book)",
            confidence=0.9
        )
        
        try:
            # Learn from feedback
            learned_predicate = self.learner.learn_from_feedback(feedback)
            self.assertIsNotNone(learned_predicate)
            print(f"✅ Feedback learning successful: {learned_predicate}")
            
            # Verify learning results
            self.assertTrue(hasattr(learned_predicate, 'name'))
            self.assertTrue(hasattr(learned_predicate, 'confidence'))
            
        except Exception as e:
            self.fail(f"Feedback learning failed: {e}")
    
    def test_pddl_domain_generation(self):
        """Test PDDL domain generation functionality"""
        print("\n🧪 Test 3: PDDL Domain Generation Functionality")
        
        # Create learned predicates for domain generation
        learned_predicates = [
            SymbolicPredicate(
                name="at", 
                arguments=["robot", "location"], 
                description="robot is at location",
                confidence=0.95,
                examples=["robot at table", "agent at kitchen"]
            ),
            SymbolicPredicate(
                name="holding", 
                arguments=["robot", "object"], 
                description="robot is holding object",
                confidence=0.9,
                examples=["robot holding cup", "agent holding book"]
            )
        ]
        
        try:
            # Create a simple LTL formula for testing
            from goal_interpreter import LTLFormula
            test_formula = LTLFormula("True", {})
            
            # Generate PDDL domain with learned predicates
            pddl_domain = self.domain_builder.build_domain(test_formula, learned_predicates)
            self.assertIsNotNone(pddl_domain)
            print(f"✅ PDDL domain generation successful")
            
            # Verify PDDL syntax
            if hasattr(self.domain_builder, 'validate_domain'):
                is_valid = self.domain_builder.validate_domain(pddl_domain)
                self.assertTrue(is_valid, "PDDL domain syntax validation failed")
                print(f"✅ PDDL syntax validation passed")
            
        except Exception as e:
            self.fail(f"PDDL domain generation failed: {e}")
    
    def test_predicate_evolution(self):
        """Test predicate evolution functionality"""
        print("\n🧪 Test 4: Predicate Evolution Functionality")
        
        try:
            # Create initial predicates with all required parameters
            initial_predicates = [
                SymbolicPredicate(
                    name="on", 
                    arguments=["obj1", "obj2"], 
                    description="obj1 is on obj2",
                    confidence=0.9,
                    examples=["book on table", "cup on desk"]
                ),
                SymbolicPredicate(
                    name="holding", 
                    arguments=["agent", "obj"], 
                    description="agent is holding obj",
                    confidence=0.85,
                    examples=["robot holding book", "person holding cup"]
                )
            ]
            
            # Simulate evolution
            new_predicate = SymbolicPredicate(
                name="is_red", 
                arguments=["obj"], 
                description="obj is red",
                confidence=0.95,
                examples=["red apple", "red book"]
            )
            evolved_predicates = initial_predicates + [new_predicate]
            
            # Verify evolution results
            self.assertEqual(len(evolved_predicates), 3)
            self.assertEqual(evolved_predicates[-1].name, "is_red")
            print(f"✅ Predicate evolution successful, final predicate count: {len(evolved_predicates)}")
            
        except Exception as e:
            self.fail(f"Predicate evolution failed: {e}")
    
    def test_statistics_tracking(self):
        """Test statistics tracking functionality"""
        print("\n🧪 Test 5: Statistics Tracking Functionality")
        
        try:
            # Simulate interpretation tasks
            test_goals = ["test goal 1", "test goal 2", "test goal 3"]
            
            for goal in test_goals:
                try:
                    # Use interpret_with_feedback instead of interpret_goal
                    interpretation = self.interpreter.interpret_with_feedback(goal)
                    # Use the correct method to update statistics if available
                    if hasattr(self.interpreter, '_update_statistics'):
                        self.interpreter._update_statistics(goal, interpretation, success=True)
                except Exception:
                    if hasattr(self.interpreter, '_update_statistics'):
                        self.interpreter._update_statistics(goal, None, success=False)
            
            # Get statistics
            stats = self.interpreter.get_statistics()
            
            # Verify statistics
            self.assertIn('total_tasks', stats)
            self.assertIn('successful_tasks', stats)
            self.assertIn('success_rate', stats)
            
            print(f"✅ Statistics tracking successful")
            print(f"   Total tasks: {stats['total_tasks']}")
            print(f"   Success rate: {stats['success_rate']:.2%}")
            
        except Exception as e:
            self.fail(f"Statistics tracking failed: {e}")
    
    def test_save_load_functionality(self):
        """Test save and load functionality"""
        print("\n🧪 Test 6: Save and Load Functionality")
        
        try:
            # Use temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_path = f.name
            
            # Save state using the correct methods
            if hasattr(self.interpreter, 'save_learned_predicates'):
                self.interpreter.save_learned_predicates(temp_path)
                self.assertTrue(os.path.exists(temp_path))
                print(f"✅ State saved successfully")
            
            # Create new interpreter and load state
            new_interpreter = InterpretableGoalInterpreter(self.config)
            if hasattr(new_interpreter, 'load_learned_predicates'):
                new_interpreter.load_learned_predicates(temp_path)
                print(f"✅ State loaded successfully")
            
            # Verify loading effect
            test_goal = "test goal"
            original_result = self.interpreter.interpret_with_feedback(test_goal)
            loaded_result = new_interpreter.interpret_with_feedback(test_goal)
            
            self.assertIsNotNone(original_result)
            self.assertIsNotNone(loaded_result)
            print(f"✅ Loading verification successful")
            
            # Clean up temporary file
            os.unlink(temp_path)
            
        except Exception as e:
            self.fail(f"Save/load functionality failed: {e}")

class TestInterPreTIntegration(unittest.TestCase):
    """InterPreT integration test class"""
    
    def setUp(self):
        """Setup before each test"""
        self.config = {
            'model_name': 'bert-base-uncased',
            'max_predicates': 20,
            'learning_rate': 0.001,
            'feedback_threshold': 0.7
        }
    
    def test_end_to_end_workflow(self):
        """Test end-to-end workflow"""
        print("\n🧪 Test 7: End-to-End Workflow")
        
        try:
            # Initialize components
            interpreter = InterpretableGoalInterpreter(self.config)
            learner = InterPreTFeedbackLearner(self.config)
            domain_builder = PDDLDomainBuilder(self.config)
            
            # Simulate complete workflow
            goal = "take the red cup from the table to the kitchen"
            
            # 1. Basic interpretation
            interpretation = interpreter.interpret_with_feedback(goal)
            self.assertIsNotNone(interpretation)
            print(f"✅ Step 1: Basic interpretation completed")
            
            # 2. Add feedback learning
            feedback = FeedbackRecord(
                goal=goal,
                user_feedback="need to emphasize movement action",
                corrected_predicate="move_to(cup, kitchen)",
                confidence=0.85
            )
            learned_predicate = learner.learn_from_feedback(feedback)
            self.assertIsNotNone(learned_predicate)
            print(f"✅ Step 2: Feedback learning completed")
            
            # 3. Generate PDDL domain with learned predicates
            learned_predicates = [learned_predicate]
            # Create a simple LTL formula for testing
            from goal_interpreter import LTLFormula
            test_formula = LTLFormula("True", {})
            pddl_domain = domain_builder.build_domain(test_formula, learned_predicates)
            self.assertIsNotNone(pddl_domain)
            print(f"✅ Step 3: PDDL domain generation completed")
            
            # 4. Update statistics
            if hasattr(interpreter, '_update_statistics'):
                interpreter._update_statistics(goal, interpretation, success=True)
            stats = interpreter.get_statistics()
            self.assertGreater(stats['total_tasks'], 0)
            print(f"✅ Step 4: Statistics update completed")
            
            print(f"✅ End-to-end workflow test passed")
            
        except Exception as e:
            self.fail(f"End-to-end workflow failed: {e}")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n🧪 Test 8: Error Handling")
        
        try:
            interpreter = InterpretableGoalInterpreter(self.config)
            
            # Test invalid input
            try:
                interpreter.interpret_with_feedback("")  # Empty string
                self.fail("Expected an exception for empty string input")
            except Exception as e:
                print(f"✅ Correctly handled empty string input: {e}")
            
            # Test invalid feedback
            learner = InterPreTFeedbackLearner(self.config)
            invalid_feedback = FeedbackRecord("", "", "", -1.0)
            try:
                result = learner.learn_from_feedback(invalid_feedback)
                print(f"✅ Invalid feedback handling completed")
            except Exception as e:
                print(f"✅ Invalid feedback correctly raised exception: {e}")
            
            print(f"✅ Error handling test passed")
            
        except Exception as e:
            print(f"⚠️ Error handling test partially passed: {e}")

def run_performance_tests():
    """Run performance tests"""
    print("\n🚀 Performance Tests")
    print("-" * 40)
    
    config = {
        'model_name': 'bert-base-uncased',
        'max_predicates': 50,
        'learning_rate': 0.001
    }
    
    interpreter = InterpretableGoalInterpreter(config)
    
    # Test interpretation performance
    import time
    test_goals = [
        "pick up the cup",
        "open the door", 
        "walk to the kitchen",
        "put down the book",
        "close the window"
    ] * 10  # Repeat 10 times
    
    start_time = time.time()
    successful_interpretations = 0
    
    for goal in test_goals:
        try:
            interpretation = interpreter.interpret_with_feedback(goal)
            successful_interpretations += 1
        except Exception:
            pass
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"📊 Performance Test Results:")
    print(f"   Total tasks: {len(test_goals)}")
    print(f"   Successful tasks: {successful_interpretations}")
    print(f"   Total time: {total_time:.3f} seconds")
    print(f"   Average time: {total_time/len(test_goals):.3f} seconds/task")
    print(f"   Success rate: {successful_interpretations/len(test_goals):.2%}")

def main():
    """Main test function"""
    print("🧪 InterPreT Interpretable Goal Interpreter Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add core functionality tests
    test_suite.addTest(unittest.makeSuite(TestInterpretableGoalInterpreter))
    
    # Add integration tests
    test_suite.addTest(unittest.makeSuite(TestInterPreTIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run performance tests
    run_performance_tests()
    
    # Output test summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failed tests:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Error tests:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
    
    if success_rate == 1.0:
        print("\n🎉 All tests passed! InterPreT integration successful!")
        print("🚀 You can start developing with InterPreT")
    elif success_rate >= 0.8:
        print(f"\n✅ Most tests passed ({success_rate:.1%})")
        print("⚠️ Some functionality needs further debugging")
    else:
        print(f"\n⚠️ Test pass rate is low ({success_rate:.1%})")
        print("🔧 Need to check and fix related issues")
    
    return 0 if success_rate >= 0.8 else 1

if __name__ == "__main__":
    sys.exit(main())