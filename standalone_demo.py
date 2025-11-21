#!/usr/bin/env python3
"""
InterPreT独立演示脚本
解决所有导入问题的版本
"""

import sys
import os

# 添加goal_interpretation目录到Python路径
goal_interpretation_dir = "/home/yeah/eai-interpretable-interface/goal_interpretation"
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
    print(f"❌ 缺少必要文件: {missing_files}")
    sys.exit(1)

print("✅ 所有必要文件存在")

# 创建简化版本的演示
class SimpleInterPreTDemo:
    """简化版InterPreT演示"""
    
    def __init__(self):
        print("🚀 初始化简化版InterPreT演示...")
        
    def demo_basic_functionality(self):
        """演示基础功能"""
        print("\n🎯 演示: 基础目标解释功能")
        print("-" * 40)
        
        goals = [
            "把杯子放到桌子上",
            "从冰箱里拿苹果", 
            "打开房间的灯",
            "整理书桌上的书籍"
        ]
        
        for i, goal in enumerate(goals, 1):
            print(f"\n📝 目标{i}: {goal}")
            
            # 简单的关键词提取
            keywords = self._extract_keywords(goal)
            print(f"🔍 提取关键词: {keywords}")
            
            # 生成简单的LTL表示
            ltl_rep = self._generate_simple_ltl(goal, keywords)
            print(f"📋 LTL表示: {ltl_rep}")
    
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
            return f"◇({" ".join(keywords)})"
        elif "总是" in goal:
            return f"□({" ".join(keywords)})"
        else:
            return f"({" ".join(keywords)})"

def main():
    """主函数"""
    print("🛠️ InterPreT简化演示")
    print("=" * 50)
    
    try:
        # 创建演示实例
        demo = SimpleInterPreTDemo()
        
        # 运行演示
        demo.demo_basic_functionality()
        
        print("\n" + "=" * 50)
        print("✅ 演示完成！")
        print("注意: 这是简化版本，完整功能需要解决依赖问题")
        
        return 0
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
