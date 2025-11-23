# Ubuntu环境下EAI-Eval项目环境更新指南

本文档提供了在Ubuntu环境下更新和使用`eai-eval` conda环境的详细步骤，以及如何利用项目中的BEHAVIOR和VirtualHome资源。

## 目录
- [1. 环境准备](#1-环境准备)
- [2. 环境创建与更新](#2-环境创建与更新)
- [3. BEHAVIOR和VirtualHome资源说明](#3-behavior和virtualhome资源说明)
- [4. 资源使用示例](#4-资源使用示例)
- [5. 常见问题排查](#5-常见问题排查)

## 1. 环境准备

### 1.1 检查Conda安装

```bash
# 检查conda是否已安装
conda --version

# 如果未安装，请先安装Miniconda或Anaconda
# Miniconda安装示例：
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# 按照提示完成安装后，重启终端
```

### 1.2 检查Python版本

项目使用Python 3.8，environment.yml中已指定。

## 2. 环境创建与更新

### 2.1 使用现有environment.yml创建环境

```bash
# 进入项目目录
cd d:\Tare_projects\eai-interface\eai-interpretable-interface

# 使用environment.yml创建环境
conda env create -f environment.yml

# 激活环境
conda activate eai-eval

# 如果环境已存在，更新环境
conda env update -f environment.yml --prune
```

### 2.2 验证环境安装

```bash
# 验证Python版本
python --version

# 验证关键依赖
pip list | grep -E 'torch|numpy|pandas|pyarrow'
```

### 2.3 安装embodied-agent-interface

```bash
# 安装embodied-agent-interface包
cd embodied-agent-interface
pip install -e .
```

## 3. BEHAVIOR和VirtualHome资源说明

通过检查目录结构，我们发现了以下关键资源：

### 3.1 BEHAVIOR资源

位置：`embodied-agent-interface/src/behavior_eval/`

主要组件：
- `agent_eval.py`: BEHAVIOR智能体评估模块
- `data/`: 数据集相关文件
- `evaluation/`: 评估工具和方法
- `transition_model/`: 状态转换模型
- `tl_formula/`: 时序逻辑公式相关实现

### 3.2 VirtualHome资源

位置：`embodied-agent-interface/src/virtualhome_eval/`

主要组件：
- `agent_eval.py`: VirtualHome智能体评估模块
- `dataset/`: 数据集相关文件
- `evaluation/`: 评估工具和方法
- `resources/`: 资源文件
- `simulation/`: 模拟环境
- `tl_formula/`: 时序逻辑公式相关实现

### 3.3 公共接口

位置：`embodied-agent-interface/src/eai_eval/`

提供统一的评估接口和工具。

## 4. 资源使用示例

### 4.1 使用BEHAVIOR评估

```python
from behavior_eval.agent_eval import BEHAVIORAgentEvaluator

# 初始化评估器
evaluator = BEHAVIORAgentEvaluator()

# 评估智能体行为
results = evaluator.evaluate_agent(agent_actions)
print(results)
```

### 4.2 使用VirtualHome评估

```python
from virtualhome_eval.agent_eval import VirtualHomeAgentEvaluator

# 初始化评估器
evaluator = VirtualHomeAgentEvaluator()

# 评估智能体行为
results = evaluator.evaluate_agent(agent_actions)
print(results)
```

### 4.3 使用时序逻辑验证

```python
from behavior_eval.tl_formula import TLFormulaValidator

# 验证时序逻辑公式
validator = TLFormulaValidator()
result = validator.validate(formula, state_sequence)
print(result)
```

## 5. 常见问题排查

### 5.1 依赖安装问题

**问题**：某些包安装失败

**解决方案**：
```bash
# 单独安装失败的包
pip install <package_name> --upgrade

# 或使用不同的源
pip install <package_name> -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5.2 权限问题

**问题**：文件权限不足

**解决方案**：
```bash
# 修改文件权限
chmod +x <script_file>

# 或使用sudo安装
```

### 5.3 环境变量问题

**问题**：找不到某些资源或模块

**解决方案**：
```bash
# 确保环境变量正确设置
export PYTHONPATH=$PYTHONPATH:$(pwd)/embodied-agent-interface/src
```

### 5.4 CUDA相关问题

**注意**：当前environment.yml中安装的是CPU版本的PyTorch

**如果需要GPU支持**：
```bash
# 卸载CPU版本
pip uninstall torch torchaudio torchvision

# 安装GPU版本
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
```

---

**作者**: EAI开发团队
**最后更新**: 2024年