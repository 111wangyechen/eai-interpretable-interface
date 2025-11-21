#!/usr/bin/env python3
"""
Ubuntu导入路径修复脚本
解决InterPreT模块导入问题
"""

import os
import sys
import shutil

def fix_import_paths():
    """修复导入路径问题"""
    print("🔧 修复InterPreT模块导入路径...")
    
    # 当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    goal_interpretation_dir = os.path.join(current_dir, "goal_interpretation")
    
    if not os.path.exists(goal_interpretation_dir):
        print(f"❌ 目录不存在: {goal_interpretation_dir}")
        return False
    
    # 需要修复的文件
    files_to_fix = [
        "demo_interpretable_interpreter.py",
        "test_interpretable_interpreter.py"
    ]
    
    for filename in files_to_fix:
        filepath = os.path.join(goal_interpretation_dir, filename)
        if os.path.exists(filepath):
            print(f"✅ 文件已存在: {filename}")
        else:
            print(f"❌ 文件不存在: {filename}")
    
    # 创建__init__.py文件使目录成为Python包
    init_file = os.path.join(goal_interpretation_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""InterPreT目标解释模块"""\n')
        print(f"✅ 创建__init__.py文件")
    
    print("✅ 导入路径修复完成")
    return True

def create_run_script():
    """创建运行脚本"""
    print("📝 创建运行脚本...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    goal_interpretation_dir = os.path.join(current_dir, "goal_interpretation")
    
    # 创建演示运行脚本
    demo_script = f"""#!/usr/bin/env python3
import sys
import os

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "{goal_interpretation_dir}"
sys.path.insert(0, goal_interpretation_dir)

# 切换到goal_interpretation目录
os.chdir(goal_interpretation_dir)

# 导入并运行演示
try:
    from demo_interpretable_interpreter import main
    print("🚀 启动InterPreT演示...")
    sys.exit(main())
except ImportError as e:
    print(f"❌ 导入错误: {{e}}")
    sys.exit(1)
"""
    
    demo_script_path = os.path.join(current_dir, "run_demo.py")
    with open(demo_script_path, 'w') as f:
        f.write(demo_script)
    
    # 创建测试运行脚本
    test_script = f"""#!/usr/bin/env python3
import sys
import os

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "{goal_interpretation_dir}"
sys.path.insert(0, goal_interpretation_dir)

# 切换到goal_interpretation目录
os.chdir(goal_interpretation_dir)

# 导入并运行测试
try:
    from test_interpretable_interpreter import main
    print("🧪 启动InterPreT测试...")
    sys.exit(main())
except ImportError as e:
    print(f"❌ 导入错误: {{e}}")
    sys.exit(1)
"""
    
    test_script_path = os.path.join(current_dir, "run_test.py")
    with open(test_script_path, 'w') as f:
        f.write(test_script)
    
    # 设置执行权限
    os.chmod(demo_script_path, 0o755)
    os.chmod(test_script_path, 0o755)
    
    print(f"✅ 创建演示脚本: {demo_script_path}")
    print(f"✅ 创建测试脚本: {test_script_path}")
    
    return demo_script_path, test_script_path

def main():
    """主函数"""
    print("🛠️ Ubuntu InterPreT导入修复工具")
    print("=" * 50)
    
    # 修复导入路径
    if not fix_import_paths():
        print("❌ 导入路径修复失败")
        return 1
    
    # 创建运行脚本
    demo_script, test_script = create_run_script()
    
    print("\n" + "=" * 50)
    print("✅ 修复完成！")
    print("=" * 50)
    print("\n📋 使用说明:")
    print(f"运行演示: python {demo_script}")
    print(f"运行测试: python {test_script}")
    print("\n或者在Ubuntu环境中直接运行:")
    print("cd ~/eai-interpretable-interface")
    print("python run_demo.py")
    print("python run_test.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())