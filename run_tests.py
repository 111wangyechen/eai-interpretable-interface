#!/usr/bin/env python3
"""
InterPreT测试脚本
"""

import sys
import os

# 添加项目路径
project_root = "/home/yeah/eai-interpretable-interface"
sys.path.insert(0, project_root)

for module in ["goal_interpretation", "action_sequencing", "transition_modeling", "subgoal_decomposition"]:
    module_path = os.path.join(project_root, module)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

def run_tests():
    """运行测试"""
    print("🧪 运行InterPreT测试套件")
    print("=" * 50)
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    # 运行各模块测试
    test_modules = [
        ("goal_interpretation", "test_interpretable_interpreter.py"),
        ("action_sequencing", "test_action_sequencing.py"),
        ("subgoal_decomposition", "test_subgoal_decomposition.py")
    ]
    
    for module, test_file in test_modules:
        test_path = os.path.join(project_root, module, test_file)
        if os.path.exists(test_path):
            print(f"\n🔍 运行 {module} 测试...")
            try:
                exec(open(test_path).read())
                print(f"✅ {module} 测试完成")
            except Exception as e:
                print(f"❌ {module} 测试失败: {e}")
        else:
            print(f"⚠️  测试文件不存在: {test_path}")

if __name__ == "__main__":
    run_tests()
