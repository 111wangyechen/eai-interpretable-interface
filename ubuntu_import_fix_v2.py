#!/usr/bin/env python3
"""
Ubuntu导入路径修复脚本 v2
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
    
    # 创建__init__.py文件使目录成为Python包
    init_file = os.path.join(goal_interpretation_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""InterPreT目标解释模块"""\n')
        print(f"✅ 创建__init__.py文件")
    
    print("✅ 导入路径修复完成")
    return True

def create_standalone_demo():
    """创建独立的演示脚本"""
    print("📝 创建独立演示脚本...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    goal_interpretation_dir = os.path.join(current_dir, "goal_interpretation")
    
    # 创建独立演示脚本
    standalone_demo = f'''#!/usr/bin/env python3
"""
InterPreT独立演示脚本
解决所有导入问题的版本
"""

import sys
import os

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "{goal_interpretation_dir}"
if goal_interpretation_dir not in sys.path:
    sys.path.insert(0, goal_interpretation_dir)

# 切换到goal_interpretation目录
os.chdir(goal_interpretation_dir)

print("🔧 检查环境...")

# 检查必要文件是否存在
required_files = [
    "interpretable_goal_interpreter.py",
    "goal_interpreter.py", 
    "nlp_parser.py",
    "ltl_generator.py",
    "ltl_validator.py"
]

missing_files = []
for file in required_files:
    if not os.path.exists(file):
        missing_files.append(file)

if missing_files:
    print(f"❌ 缺少必要文件: {{missing_files}}")
    sys.exit(1)

print("✅ 所有必要文件存在")

# 创建简化版本的演示
class SimpleInterPreTDemo:
    """简化版InterPreT演示"""
    
    def __init__(self):
        print("🚀 初始化简化版InterPreT演示...")
        
    def demo_basic_functionality(self):
        """演示基础功能"""
        print("\\n🎯 演示: 基础目标解释功能")
        print("-" * 40)
        
        goals = [
            "把杯子放到桌子上",
            "从冰箱里拿苹果", 
            "打开房间的灯",
            "整理书桌上的书籍"
        ]
        
        for i, goal in enumerate(goals, 1):
            print(f"\\n📝 目标{{i}}: {{goal}}")
            
            # 简单的关键词提取
            keywords = self._extract_keywords(goal)
            print(f"🔍 提取关键词: {{keywords}}")
            
            # 生成简单的LTL表示
            ltl_rep = self._generate_simple_ltl(goal, keywords)
            print(f"📋 LTL表示: {{ltl_rep}}")
    
    def _extract_keywords(self, text):
        """提取关键词"""
        # 简单的关键词提取
        action_words = ["把", "从", "打开", "整理", "拿", "放"]
        objects = ["杯子", "桌子", "冰箱", "苹果", "灯", "书", "书籍"]
        
        keywords = []
        words = text.split()
        for word in words:
            if word in action_words or word in objects:
                keywords.append(word)
        
        return keywords
    
    def _generate_simple_ltl(self, goal, keywords):
        """生成简单的LTL表示"""
        # 简化的LTL生成
        if "最终" in goal or "要" in goal:
            return f"◇({{" ".join(keywords)}})"
        elif "总是" in goal:
            return f"□({{" ".join(keywords)}})"
        else:
            return f"({{" ".join(keywords)}})"

def main():
    """主函数"""
    print("🛠️ InterPreT简化演示")
    print("=" * 50)
    
    try:
        # 创建演示实例
        demo = SimpleInterPreTDemo()
        
        # 运行演示
        demo.demo_basic_functionality()
        
        print("\\n" + "=" * 50)
        print("✅ 演示完成！")
        print("注意: 这是简化版本，完整功能需要解决依赖问题")
        
        return 0
        
    except Exception as e:
        print(f"❌ 演示失败: {{e}}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    standalone_demo_path = os.path.join(current_dir, "standalone_demo.py")
    with open(standalone_demo_path, 'w') as f:
        f.write(standalone_demo)
    
    # 设置执行权限
    os.chmod(standalone_demo_path, 0o755)
    
    print(f"✅ 创建独立演示脚本: {standalone_demo_path}")
    return standalone_demo_path

def create_dependency_checker():
    """创建依赖检查脚本"""
    print("🔍 创建依赖检查脚本...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    goal_interpretation_dir = os.path.join(current_dir, "goal_interpretation")
    
    dependency_checker = f'''#!/usr/bin/env python3
"""
InterPreT依赖检查脚本
"""

import sys
import os
import importlib

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "{goal_interpretation_dir}"
sys.path.insert(0, goal_interpretation_dir)

# 切换到goal_interpretation目录
os.chdir(goal_interpretation_dir)

def check_dependencies():
    """检查依赖"""
    print("🔍 检查InterPreT依赖...")
    
    # 检查Python标准库
    standard_libs = ["os", "sys", "re", "json", "typing", "dataclasses", "logging"]
    print("\\n📚 检查Python标准库:")
    for lib in standard_libs:
        try:
            importlib.import_module(lib)
            print(f"   ✅ {{lib}}")
        except ImportError:
            print(f"   ❌ {{lib}}")
    
    # 检查第三方库
    third_party_libs = ["numpy", "torch", "transformers", "gym", "matplotlib"]
    print("\\n📦 检查第三方库:")
    for lib in third_party_libs:
        try:
            importlib.import_module(lib)
            print(f"   ✅ {{lib}}")
        except ImportError:
            print(f"   ❌ {{lib}}")
    
    # 检查本地模块
    local_modules = [
        "goal_interpreter",
        "nlp_parser", 
        "ltl_generator",
        "ltl_validator",
        "data_loader"
    ]
    print("\\n📁 检查本地模块:")
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {{module}}")
        except ImportError as e:
            print(f"   ❌ {{module}}: {{e}}")
    
    # 检查核心模块
    print("\\n🎯 检查核心模块:")
    try:
        from interpretable_goal_interpreter import InterpretableGoalInterpreter
        print("   ✅ InterpretableGoalInterpreter")
    except ImportError as e:
        print(f"   ❌ InterpretableGoalInterpreter: {{e}}")
    
    print("\\n" + "=" * 50)

def main():
    """主函数"""
    check_dependencies()

if __name__ == "__main__":
    main()
'''
    
    dependency_checker_path = os.path.join(current_dir, "check_dependencies.py")
    with open(dependency_checker_path, 'w') as f:
        f.write(dependency_checker)
    
    # 设置执行权限
    os.chmod(dependency_checker_path, 0o755)
    
    print(f"✅ 创建依赖检查脚本: {dependency_checker_path}")
    return dependency_checker_path

def main():
    """主函数"""
    print("🛠️ Ubuntu InterPreT导入修复工具 v2")
    print("=" * 50)
    
    # 修复导入路径
    if not fix_import_paths():
        print("❌ 导入路径修复失败")
        return 1
    
    # 创建独立演示脚本
    standalone_demo = create_standalone_demo()
    
    # 创建依赖检查脚本
    dependency_checker = create_dependency_checker()
    
    print("\n" + "=" * 50)
    print("✅ 修复完成！")
    print("=" * 50)
    print("\n📋 使用说明:")
    print(f"1. 检查依赖: python {dependency_checker}")
    print(f"2. 运行简化演示: python {standalone_demo}")
    print("\n🔍 故障排除:")
    print("- 如果依赖检查失败，请安装缺少的包")
    print("- 如果简化演示成功，说明基础环境正常")
    print("- 完整功能需要解决所有依赖问题")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())