#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单导入测试脚本
用于验证模块导入是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("Testing imports from project root:", project_root)

# 测试各个模块的导入
try:
    print("\n1. Testing action_sequencing module...")
    from action_sequencing import ActionSequencer, Action, ActionType, SequencingRequest
    print("   ✓ ActionSequencer imported successfully")
    print("   ✓ Action imported successfully")
    print("   ✓ ActionType imported successfully")
    print("   ✓ SequencingRequest imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import from action_sequencing: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n2. Testing direct import of action_data...")
    from action_sequencing.action_data import Action, ActionSequence
    print("   ✓ Direct import of action_data works")
except ImportError as e:
    print(f"   ✗ Failed direct import of action_data: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n3. Testing goal_interpretation module...")
    from goal_interpretation import EnhancedGoalInterpreter as GoalInterpreter
    print("   ✓ GoalInterpreter imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import from goal_interpretation: {e}")

try:
    print("\n4. Testing subgoal_decomposition module...")
    from subgoal_decomposition import SubgoalDecomposer
    print("   ✓ SubgoalDecomposer imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import from subgoal_decomposition: {e}")

try:
    print("\n5. Testing transition_modeling module...")
    from transition_modeling import TransitionModeler
    print("   ✓ TransitionModeler imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import from transition_modeling: {e}")

print("\nImport test completed.")