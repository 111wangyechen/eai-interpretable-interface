#!/usr/bin/env python3
"""
InterPreT主运行脚本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = "/home/yeah/eai-interpretable-interface"
sys.path.insert(0, project_root)

# 添加各模块目录
modules = ["goal_interpretation", "action_sequencing", "transition_modeling", "subgoal_decomposition"]
for module in modules:
    module_path = os.path.join(project_root, module)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

def main():
    """主函数"""
    print("🚀 InterPreT项目启动")
    print("=" * 50)
    
    # 检查模块
    print("🔍 检查模块状态...")
    for module in modules:
        module_path = os.path.join(project_root, module)
        if os.path.exists(module_path):
            print(f"✅ {module} 模块存在")
        else:
            print(f"❌ {module} 模块缺失")
    
    print("\n📋 可用功能:")
    print("1. 目标解释演示")
    print("2. 动作序列演示") 
    print("3. 状态转换演示")
    print("4. 子目标分解演示")
    print("5. 集成测试")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
