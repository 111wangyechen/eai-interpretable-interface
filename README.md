# InterPreT - 可解释具身推理框架

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
