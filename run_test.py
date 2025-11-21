#!/usr/bin/env python3
import sys
import os

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "/home/yeah/eai-interpretable-interface/goal_interpretation"
sys.path.insert(0, goal_interpretation_dir)

# 切换到goal_interpretation目录
os.chdir(goal_interpretation_dir)

# 导入并运行测试
try:
    from test_interpretable_interpreter import main
    print("🧪 启动InterPreT测试...")
    sys.exit(main())
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)
