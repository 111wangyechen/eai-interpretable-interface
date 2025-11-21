#!/usr/bin/env python3
"""
InterPreT项目Ubuntu迁移脚本
专门用于从embodied-agent-interface迁移到eai-interpretable-interface
"""

import os
import sys
import shutil
import json
from pathlib import Path

def create_project_structure(target_dir):
    """创建完整的项目结构"""
    print(f"🏗️ 在 {target_dir} 创建InterPreT项目结构...")
    
    # 定义项目结构
    project_structure = {
        "goal_interpretation": {
            "description": "目标解释模块",
            "files": [
                "interpretable_goal_interpreter.py",
                "goal_interpreter.py",
                "nlp_parser.py", 
                "ltl_generator.py",
                "ltl_validator.py",
                "data_loader.py",
                "demo_interpretable_interpreter.py",
                "test_interpretable_interpreter.py",
                "enhanced_goal_interpreter.py",
                "enhanced_nlp_parser.py",
                "enhanced_ltl_generator.py",
                "compound_task_processor.py",
                "subgoal_decomposer.py",
                "example_usage.py",
                "README.md",
                "__init__.py"
            ]
        },
        "action_sequencing": {
            "description": "动作序列模块", 
            "files": [
                "action_sequencer.py",
                "action_planner.py",
                "state_manager.py",
                "data_loader.py",
                "action_data.py",
                "test_action_sequencing.py",
                "example_usage.py",
                "debug_test.py",
                "README.md",
                "__init__.py"
            ]
        },
        "transition_modeling": {
            "description": "状态转换模块",
            "files": [
                "transition_modeler.py",
                "transition_predictor.py", 
                "state_transition.py",
                "transition_validator.py",
                "README.md",
                "__init__.py"
            ]
        },
        "subgoal_decomposition": {
            "description": "子目标分解模块",
            "files": [
                "subgoal_decomposer.py",
                "subgoal_validator.py",
                "subgoal_ltl_integration.py",
                "demo_subgoal_decomposition.py",
                "test_subgoal_decomposition.py",
                "quick_test.py",
                "README.md",
                "__init__.py"
            ]
        },
        "config": {
            "description": "配置文件",
            "files": [
                "enhanced_config.yaml",
                "example_config.yaml"
            ]
        },
        "data": {
            "description": "数据文件",
            "files": [
                "behavior-00000-of-00001.parquet",
                "virtualhome-00000-of-00001.parquet"
            ]
        },
        "docs": {
            "description": "文档",
            "files": [
                "技术指导文档.md",
                "双人团队任务规划.md", 
                "四人团队任务规划.md"
            ]
        },
        "tests": {
            "description": "集成测试",
            "files": [
                "test_comprehensive_integration.py",
                "test_cross_module_integration.py",
                "test_four_module_integration.py",
                "test_integration.py",
                "complete_test.py",
                "final_test.py"
            ]
        }
    }
    
    # 创建目录结构
    for module_name, module_info in project_structure.items():
        module_dir = os.path.join(target_dir, module_name)
        os.makedirs(module_dir, exist_ok=True)
        print(f"✅ 创建目录: {module_name}/")
        
        # 创建模块说明文件
        readme_path = os.path.join(module_dir, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {module_info['description']}\n\n")
                f.write(f"## 模块说明\n{module_info['description']}\n\n")
                f.write("## 文件列表\n")
                for file in module_info['files']:
                    f.write(f"- {file}\n")
    
    return project_structure

def copy_module_files(source_dir, target_dir, project_structure):
    """复制模块文件"""
    print("📁 复制模块文件...")
    
    # 源目录映射
    source_mappings = {
        "goal_interpretation": "goal_interpretation",
        "action_sequencing": "action_sequencing", 
        "transition_modeling": "transition_modeling",
        "subgoal_decomposition": "subgoal_decomposition",
        "config": "",  # 配置文件在根目录
        "data": "",     # 数据文件在根目录
        "docs": "docs", # 文档在docs目录
        "tests": ""     # 测试文件在根目录
    }
    
    copied_files = []
    failed_files = []
    
    for module_name, module_info in project_structure.items():
        # 确定源目录
        source_subdir = source_mappings[module_name]
        if source_subdir:
            source_module_dir = os.path.join(source_dir, source_subdir)
        else:
            source_module_dir = source_dir
        
        target_module_dir = os.path.join(target_dir, module_name)
        
        for filename in module_info['files']:
            source_file = os.path.join(source_module_dir, filename)
            target_file = os.path.join(target_module_dir, filename)
            
            if os.path.exists(source_file):
                try:
                    shutil.copy2(source_file, target_file)
                    copied_files.append(filename)
                    print(f"✅ 复制: {module_name}/{filename}")
                except Exception as e:
                    failed_files.append((filename, str(e)))
                    print(f"❌ 复制失败: {module_name}/{filename} - {e}")
            else:
                print(f"⚠️  文件不存在: {source_file}")
    
    return copied_files, failed_files

def create_project_scripts(target_dir):
    """创建项目运行脚本"""
    print("📝 创建项目运行脚本...")
    
    # 创建主运行脚本
    main_script = '''#!/usr/bin/env python3
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
    
    print("\\n📋 可用功能:")
    print("1. 目标解释演示")
    print("2. 动作序列演示") 
    print("3. 状态转换演示")
    print("4. 子目标分解演示")
    print("5. 集成测试")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    main_script_path = os.path.join(target_dir, "main.py")
    with open(main_script_path, 'w') as f:
        f.write(main_script)
    
    os.chmod(main_script_path, 0o755)
    print(f"✅ 创建主脚本: main.py")
    
    # 创建测试脚本
    test_script = '''#!/usr/bin/env python3
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
            print(f"\\n🔍 运行 {module} 测试...")
            try:
                exec(open(test_path).read())
                print(f"✅ {module} 测试完成")
            except Exception as e:
                print(f"❌ {module} 测试失败: {e}")
        else:
            print(f"⚠️  测试文件不存在: {test_path}")

if __name__ == "__main__":
    run_tests()
'''
    
    test_script_path = os.path.join(target_dir, "run_tests.py")
    with open(test_script_path, 'w') as f:
        f.write(test_script)
    
    os.chmod(test_script_path, 0o755)
    print(f"✅ 创建测试脚本: run_tests.py")

def create_requirements(target_dir):
    """创建requirements.txt"""
    print("📦 创建requirements.txt...")
    
    requirements = """# InterPreT项目依赖

# 核心依赖
numpy>=1.21.0
torch>=1.9.0
transformers>=4.20.0
gym>=0.21.0

# 数据处理
pandas>=1.3.0
pyarrow>=6.0.0

# 可视化
matplotlib>=3.5.0
seaborn>=0.11.0

# 配置和工具
pyyaml>=6.0
tqdm>=4.62.0

# 仿真环境
igibson>=2.2.0

# 测试框架
pytest>=6.2.0

# 开发工具
black>=22.0.0
flake8>=4.0.0
"""
    
    requirements_path = os.path.join(target_dir, "requirements.txt")
    with open(requirements_path, 'w') as f:
        f.write(requirements)
    
    print(f"✅ 创建requirements.txt")

def create_project_readme(target_dir):
    """创建项目README"""
    print("📖 创建项目README...")
    
    readme_content = """# InterPreT - 可解释具身推理框架

## 项目概述

InterPreT是一个用于具身智能的可解释推理框架，支持自然语言目标解释、动作序列生成、状态转换建模和子目标分解。

## 模块结构

### 🎯 goal_interpretation - 目标解释模块
- `interpretable_goal_interpreter.py` - 核心解释器
- `goal_interpreter.py` - 基础目标解释
- `nlp_parser.py` - 自然语言处理
- `ltl_generator.py` - LTL公式生成
- `demo_interpretable_interpreter.py` - 演示脚本

### 🔄 action_sequencing - 动作序列模块  
- `action_sequencer.py` - 动作序列生成
- `action_planner.py` - 动作规划
- `state_manager.py` - 状态管理
- `test_action_sequencing.py` - 测试脚本

### 🔄 transition_modeling - 状态转换模块
- `transition_modeler.py` - 状态转换建模
- `transition_predictor.py` - 状态预测
- `state_transition.py` - 状态转换逻辑

### 🧩 subgoal_decomposition - 子目标分解模块
- `subgoal_decomposer.py` - 子目标分解
- `subgoal_validator.py` - 子目标验证
- `demo_subgoal_decomposition.py` - 演示脚本

## 快速开始

### 1. 环境配置
```bash
# 安装依赖
pip install -r requirements.txt

# 激活conda环境
conda activate eai-eval
```

### 2. 运行演示
```bash
# 运行主程序
python main.py

# 运行测试
python run_tests.py

# 运行目标解释演示
cd goal_interpretation
python demo_interpretable_interpreter.py
```

### 3. 集成测试
```bash
# 运行完整集成测试
cd tests
python test_comprehensive_integration.py
```

## 配置文件

- `config/enhanced_config.yaml` - 增强配置
- `config/example_config.yaml` - 示例配置

## 数据文件

- `data/behavior-00000-of-00001.parquet` - BEHAVIOR数据集
- `data/virtualhome-00000-of-00001.parquet` - VirtualHome数据集

## 技术特性

- 🧠 智能目标解释
- 🔄 反馈学习机制
- 🏗️ PDDL域生成
- 📊 统计跟踪
- 💾 模型保存/加载
- 🧬 谓词演化

## 开发指南

详细的开发指南请参考各模块的README.md文件。

## 许可证

MIT License
"""
    
    readme_path = os.path.join(target_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ 创建README.md")

def main():
    """主函数"""
    print("🚀 InterPreT项目Ubuntu迁移工具")
    print("=" * 60)
    
    # 获取源目录和目标目录
    source_dir = "/home/yeah/embodied-agent-interface"  # 原项目路径
    target_dir = "/home/yeah/eai-interpretable-interface"  # 新建项目路径
    
    print(f"📁 源目录: {source_dir}")
    print(f"🎯 目标目录: {target_dir}")
    
    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"❌ 源目录不存在: {source_dir}")
        print("请确认原项目路径是否正确")
        return 1
    
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. 创建项目结构
    project_structure = create_project_structure(target_dir)
    
    # 2. 复制模块文件
    copied_files, failed_files = copy_module_files(source_dir, target_dir, project_structure)
    
    # 3. 创建项目脚本
    create_project_scripts(target_dir)
    
    # 4. 创建requirements.txt
    create_requirements(target_dir)
    
    # 5. 创建项目README
    create_project_readme(target_dir)
    
    # 输出总结
    print("\n" + "=" * 60)
    print("✅ 项目迁移完成！")
    print("=" * 60)
    print(f"📊 复制文件数: {len(copied_files)}")
    print(f"❌ 失败文件数: {len(failed_files)}")
    
    if failed_files:
        print("\n❌ 失败文件列表:")
        for filename, error in failed_files:
            print(f"   - {filename}: {error}")
    
    print(f"\n🎯 目标目录: {target_dir}")
    print("\n📋 下一步操作:")
    print("1. cd /home/yeah/eai-interpretable-interface")
    print("2. pip install -r requirements.txt")
    print("3. python main.py")
    print("4. python run_tests.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())