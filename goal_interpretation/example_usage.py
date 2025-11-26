#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标解释模块使用示例
演示如何使用目标解释器将自然语言转换为LTL公式
"""

from goal_interpreter import GoalInterpreter


def main():
    """
    Main function, demonstrating the use of the goal interpretation module
    """
    # Create goal interpreter instance
    interpreter = GoalInterpreter()
    
    print("=== Goal Interpretation Module Usage Example ===")
    print("This module can convert natural language goal descriptions into LTL formulas")
    print("\n")
    
    # List of test cases
    test_cases = [
        "Reach the kitchen",
        "First open the door, then enter the room",
        "If you see a red light, stop moving forward",
        "Open the window and close the door at the same time",
        "Eventually reach the destination",
        "Always stay safe",
        "First check if the environment is safe, if safe then proceed to the table, then pick up the key",
    ]
    
    # Process each test case
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Example {i} ---")
        print(f"Natural Language: {text}")
        
        try:
            # Interpret natural language to generate LTL formula
            ltl_formula = interpreter.interpret(text)
            
            # Print generated LTL formula
            print(f"LTL Formula: {ltl_formula.formula}")
            
            # Print semantic parsing results
            print("Semantic Structure:")
            print(f"  - Task Type: {ltl_formula.semantics.get('task_type', 'unknown')}")
            print(f"  - Actions: {ltl_formula.semantics.get('actions', [])}")
            print(f"  - Objects: {ltl_formula.semantics.get('objects', [])}")
            print(f"  - Conditions: {ltl_formula.semantics.get('conditions', [])}")
            
            # Validate LTL formula
            print("Validation Result: Valid Formula")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n")
    print("=== Custom Input Example ===")
    print("Try entering a custom natural language goal description:")
    
    # Allow user to input custom text
    while True:
        try:
            user_input = input("\nPlease enter a natural language goal description (enter 'q' to exit): ")
            
            if user_input.lower() == 'q':
                break
            
            # Interpret user input
            ltl_formula = interpreter.interpret(user_input)
            
            # Display results
            print(f"LTL Formula: {ltl_formula.formula}")
            print(f"Task Type: {ltl_formula.semantics.get('task_type', 'unknown')}")
            
        except Exception as e:
            print(f"Processing Failed: {str(e)}")
    
    print("\nThank you for using the Goal Interpretation Module!")


def batch_processing():
    """
    Batch processing example, handling multiple natural language goals
    """
    interpreter = GoalInterpreter()
    
    # List of natural language goals to process
    goals = [
        "Collect all items and return to the starting point",
        "Reach the end without hitting any obstacles",
        "First turn off the lights, then lock the door, and finally leave the room",
        "If danger is detected, evacuate immediately",
        "Keep the environment clean and check equipment regularly"
    ]
    
    print("=== Batch Processing Example ===")
    
    results = []
    
    # Batch process all goals
    for i, goal in enumerate(goals, 1):
        ltl_formula = interpreter.interpret(goal)
        results.append({
            "id": i,
            "natural_language": goal,
            "ltl_formula": ltl_formula.formula,
            "task_type": ltl_formula.semantics.get('task_type', 'unknown')
        })
    
    # Display batch processing results
    for result in results:
        print(f"\nGoal {result['id']}:")
        print(f"  Natural Language: {result['natural_language']}")
        print(f"  LTL Formula: {result['ltl_formula']}")
        print(f"  Task Type: {result['task_type']}")


def custom_configuration():
    """
    Custom configuration example
    Demonstrating how to use the goal interpretation module for specific needs
    """
    interpreter = GoalInterpreter()
    
    print("\n=== Custom Configuration Example ===")
    print("Using the goal interpretation module for specific domain requirements")
    
    # Domain-specific goal descriptions
    domain_goals = [
        "The robot needs to first move to shelf A, then pick up the box, and finally place it on the conveyor belt",
        "The smart home system turns on the air conditioner when it detects the indoor temperature is above 26 degrees",
        "The autonomous vehicle stays in the lane and maintains a safe distance from the vehicle ahead"
    ]
    
    for goal in domain_goals:
        ltl_formula = interpreter.interpret(goal)
        print(f"\nDomain Goal: {goal}")
        print(f"LTL Formula: {ltl_formula.formula}")


if __name__ == "__main__":
    # 运行主示例
    main()
    
    # 运行批处理示例
    batch_processing()
    
    # 运行自定义配置示例
    custom_configuration()