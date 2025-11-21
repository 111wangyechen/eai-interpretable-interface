#!/usr/bin/env python3
"""
InterPreT依赖检查脚本
"""

import sys
import os
import importlib

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "/home/yeah/eai-interpretable-interface/goal_interpretation"
sys.path.insert(0, goal_interpretation_dir)

# 切换到goal_interpretation目录
os.chdir(goal_interpretation_dir)

def check_dependencies():
    """检查依赖"""
    print("🔍 检查InterPreT依赖...")
    
    # 检查Python标准库
    standard_libs = ["os", "sys", "re", "json", "typing", "dataclasses", "logging"]
    print("\n📚 检查Python标准库:")
    for lib in standard_libs:
        try:
            importlib.import_module(lib)
            print(f"   ✅ {lib}")
        except ImportError:
            print(f"   ❌ {lib}")
    
    # 检查第三方库
    third_party_libs = ["numpy", "torch", "transformers", "gym", "matplotlib"]
    print("\n📦 检查第三方库:")
    for lib in third_party_libs:
        try:
            importlib.import_module(lib)
            print(f"   ✅ {lib}")
        except ImportError:
            print(f"   ❌ {lib}")
    
    # 检查本地模块
    local_modules = [
        "goal_interpreter",
        "nlp_parser", 
        "ltl_generator",
        "ltl_validator",
        "data_loader"
    ]
    print("\n📁 检查本地模块:")
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
    
    # 检查核心模块
    print("\n🎯 检查核心模块:")
    try:
        from interpretable_goal_interpreter import InterpretableGoalInterpreter
        print("   ✅ InterpretableGoalInterpreter")
    except ImportError as e:
        print(f"   ❌ InterpretableGoalInterpreter: {e}")
    
    print("\n" + "=" * 50)

def main():
    """主函数"""
    check_dependencies()

if __name__ == "__main__":
    main()
