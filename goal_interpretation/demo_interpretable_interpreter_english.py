#!/usr/bin/env python3
"""
InterPreT Integration Demo Script
Demonstrates core functionality of the interpretable goal interpreter
"""

import sys
import os
from typing import Dict, Any, List

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
        LTLFormula
    )
    print("✅ Successfully imported InterPreT modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure interpretable_goal_interpreter.py is in the same directory")
    sys.exit(1)

class InterPreTDemo:
    """InterPreT Demo Class"""
    
    def __init__(self):
        """Initialize demo environment"""
        self.interpreter = None
        self.learner = None
        self.domain_builder = None
        
    def setup_demo(self):
        """Set up demo environment"""
        print("🔧 Initializing InterPreT demo environment...")
        
        # Create configuration
        config = {
            'interpretable': {
                'enabled': True,
                'max_feedback_iterations': 3,
                'interactive_learning': {
                    'enabled': True
                },
                'pddl_domain': {
                    'auto_generate': True,
                    'use_llm': False
                }
            }
        }
        
        try:
            # Initialize core components
            self.interpreter = InterpretableGoalInterpreter(config)
            self.learner = InterPreTFeedbackLearner(config.get('interpretable', {}))
            self.domain_builder = PDDLDomainBuilder(config.get('interpretable', {}).get('pddl_domain', {}))
            
            print("✅ InterPreT components initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def demo_basic_interpretation(self):
        """Demonstrate basic goal interpretation functionality"""
        print("\n🎯 Demo 1: Basic Goal Interpretation")
        print("-" * 40)
        
        goals = [
            "Pick up the cup",
            "Open the door",
            "Walk to the kitchen",
            "Clean the table"
        ]
        
        for i, goal in enumerate(goals, 1):
            print(f"\n📝 Goal {i}: {goal}")
            
            try:
                # Create feedback history (even empty for now)
                feedback_history = []
                
                # Interpret goal with feedback method
                ltl_formula, pddl_domain = self.interpreter.interpret_with_feedback(goal, feedback_history)
                print(f"🔍 LTL Formula: {ltl_formula.formula}")
                print(f"📋 Valid: {ltl_formula.is_valid()}")
                
            except Exception as e:
                print(f"❌ Interpretation failed: {e}")
    
    def demo_feedback_learning(self):
        """Demonstrate feedback learning functionality"""
        print("\n🔄 Demo 2: Feedback Learning Mechanism")
        print("-" * 40)
        
        goal = "Put the red book on the bookshelf"
        print(f"📝 Goal: {goal}")
        
        # Create feedback history
        try:
            # Simulate user feedback
            feedback_history = [
                {
                    'text': goal,
                    'type': 'positive',
                    'content': 'The interpretation correctly identified the object',
                    'confidence': 0.9
                },
                {
                    'text': goal,
                    'type': 'correction',
                    'content': 'Add color attribute and specify action as place',
                    'confidence': 0.85
                }
            ]
            
            # Initial interpretation
            initial_formula, _ = self.interpreter.interpret_with_feedback(goal, [])
            print(f"🔍 Initial formula: {initial_formula.formula}")
            
            # Learn from feedback
            for feedback in feedback_history:
                feedback_record = FeedbackRecord(
                    text=feedback['text'],
                    initial_formula=initial_formula.formula,
                    refined_formula=initial_formula.formula,
                    feedback_type=feedback['type'],
                    feedback_content=feedback['content'],
                    timestamp=0.0,
                    confidence=feedback['confidence']
                )
                self.learner.add_feedback(feedback_record)
                print(f"📚 Added feedback: {feedback['type']} - {feedback['content']}")
            
            # Updated interpretation
            updated_formula, _ = self.interpreter.interpret_with_feedback(goal, feedback_history)
            print(f"✨ Updated formula: {updated_formula.formula}")
            
        except Exception as e:
            print(f"❌ Feedback learning failed: {e}")
    
    def demo_predicate_evolution(self):
        """Demonstrate predicate evolution functionality"""
        print("\n🧬 Demo 3: Predicate Evolution")
        print("-" * 40)
        
        try:
            # Create initial predicates with correct parameters
            initial_predicates = [
                SymbolicPredicate(
                    name="on", 
                    parameters=["obj1", "obj2"],
                    arity=2,
                    description="obj1 is on obj2",
                    confidence=1.0,
                    examples=["book on table", "cup on desk"]
                ),
                SymbolicPredicate(
                    name="holding", 
                    parameters=["agent", "obj"],
                    arity=2,
                    description="agent is holding obj",
                    confidence=1.0,
                    examples=["robot holding book", "human holding cup"]
                )
            ]
            
            print("📋 Initial predicate set:")
            for pred in initial_predicates:
                print(f"   - {pred.name}({', '.join(pred.parameters)}) - {pred.description}")
            
            # Simulate evolution process
            evolution_steps = [
                ("Add color attribute", "is_red", ["obj"], "obj is red", 1.0, ["red book", "red cup"]),
                ("Add container relation", "inside", ["obj", "container"], "obj is inside container", 1.0, ["book inside box", "apple inside fridge"]),
            ]
            
            evolved_predicates = initial_predicates.copy()
            
            for step_name, name, args, description, confidence, examples in evolution_steps:
                print(f"\n🔄 {step_name}:")
                new_predicate = SymbolicPredicate(
                    name=name,
                    parameters=args,
                    arity=len(args),
                    description=description,
                    confidence=confidence,
                    examples=examples
                )
                evolved_predicates.append(new_predicate)
                print(f"   + {new_predicate.name}({', '.join(new_predicate.parameters)}) - {new_predicate.description}")
            
            print(f"\n📊 Final predicate count: {len(evolved_predicates)}")
            
        except Exception as e:
            print(f"❌ Predicate evolution failed: {e}")
    
    def demo_pddl_domain_generation(self):
        """Demonstrate PDDL domain generation functionality"""
        print("\n🏗️  Demo 4: PDDL Domain Generation")
        print("-" * 40)
        
        try:
            # Create a simple LTL formula
            ltl_formula = LTLFormula("F (at robot kitchen)", {"action": "move"})
            
            # Create some learned predicates
            learned_predicates = [
                SymbolicPredicate(
                    name="at",
                    parameters=["agent", "location"],
                    arity=2,
                    description="Agent is at location",
                    confidence=1.0,
                    examples=["robot at kitchen"]
                ),
                SymbolicPredicate(
                    name="holding",
                    parameters=["agent", "object"],
                    arity=2,
                    description="Agent is holding object",
                    confidence=1.0,
                    examples=["holding cup"]
                )
            ]
            
            # Build PDDL domain with correct parameters
            pddl_domain = self.domain_builder.build_domain(ltl_formula, learned_predicates)
            
            # Print domain information
            print("📋 Generated PDDL Domain:")
            print(f"Domain Name: {pddl_domain.name}")
            print(f"Predicates: {len(pddl_domain.predicates)}")
            print(f"Actions: {len(pddl_domain.actions)}")
            
        except Exception as e:
            print(f"❌ PDDL domain generation failed: {e}")
    
    def demo_statistics_tracking(self):
        """Demonstrate statistics tracking functionality"""
        print("\n📊 Demo 5: Statistics Tracking")
        print("-" * 40)
        
        try:
            # Simulate a series of interpretation tasks
            test_goals = [
                "Pick up the cup",
                "Open the door", 
                "Walk to the kitchen",
                "Clean the table",
                "Close the window"
            ]
            
            print("🔄 Executing interpretation tasks and collecting statistics...")
            
            for goal in test_goals:
                try:
                    formula, _ = self.interpreter.interpret_with_feedback(goal, [])
                    print(f"✅ {goal}: Interpretation successful")
                except Exception as e:
                    print(f"❌ {goal}: Interpretation failed - {e}")
            
            # Get statistics using the correct method
            stats = self.interpreter.get_statistics()
            print(f"\n📊 Statistics:")
            print(f"   Total interpretations: {stats.get('interpretation_stats', {}).get('total_interpretations', 0)}")
            print(f"   Successful interpretations: {stats.get('interpretation_stats', {}).get('successful_interpretations', 0)}")
            print(f"   Domains generated: {stats.get('interpretation_stats', {}).get('domains_generated', 0)}")
            print(f"   Learned predicates: {stats.get('learned_predicates_count', 0)}")
            
        except Exception as e:
            print(f"❌ Statistics tracking failed: {e}")
    
    def demo_save_load_functionality(self):
        """Demonstrate save and load functionality"""
        print("\n💾 Demo 6: Save and Load Functionality")
        print("-" * 40)
        
        try:
            # Create some test predicates to save
            test_predicates = [
                SymbolicPredicate(
                    name="test_predicate",
                    parameters=["obj"],
                    arity=1,
                    description="Test predicate",
                    confidence=0.9,
                    examples=["test example"]
                )
            ]
            
            # Add predicates to the learner
            for pred in test_predicates:
                self.learner.predicate_patterns[pred.name] = pred.examples
                self.learner.predicate_confidence[pred.name] = pred.confidence
            
            # Save learned predicates
            save_path = "interpretable_predicates.json"
            self.interpreter.save_learned_predicates(save_path)
            print(f"💾 Predicates saved to: {save_path}")
            
            # Create new interpreter and load predicates
            new_interpreter = InterpretableGoalInterpreter()
            new_interpreter.load_learned_predicates(save_path)
            print("✅ Predicates loaded successfully")
            
            # Clean up temporary file
            if os.path.exists(save_path):
                os.remove(save_path)
                print(f"🗑️  Temporary file cleaned up: {save_path}")
            
        except Exception as e:
            print(f"❌ Save/load functionality failed: {e}")
    
    def run_all_demos(self):
        """Run all demonstrations"""
        print("🚀 Starting InterPreT Complete Demo")
        print("=" * 60)
        
        if not self.setup_demo():
            print("❌ Demo environment initialization failed")
            return False
        
        demos = [
            self.demo_basic_interpretation,
            self.demo_feedback_learning,
            self.demo_predicate_evolution,
            self.demo_pddl_domain_generation,
            self.demo_statistics_tracking,
            self.demo_save_load_functionality
        ]
        
        successful_demos = 0
        
        for demo_func in demos:
            try:
                demo_func()
                successful_demos += 1
            except Exception as e:
                print(f"❌ Demo failed: {e}")
        
        print("\n" + "=" * 60)
        print(f"🎉 Demo complete! Successfully ran {successful_demos}/{len(demos)} demos")
        
        if successful_demos == len(demos):
            print("🌟 All InterPreT functionality demos successful!")
        else:
            print("⚠️  Some demos failed, please check error messages")
        
        return successful_demos == len(demos)

def main():
    """Main function"""
    print("🎯 InterPreT Interpretable Goal Interpreter Demo")
    print("=" * 50)
    
    demo = InterPreTDemo()
    success = demo.run_all_demos()
    
    if success:
        print("\n🎊 All InterPreT demos successful!")
        print("🚀 You can start using InterPreT for goal interpretation development")
    else:
        print("\n⚠️  Some demos failed")
        print("🔧 Please check error messages and fix related issues")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())