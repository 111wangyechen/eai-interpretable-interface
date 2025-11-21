#!/bin/bash
# 项目初始化脚本

echo "🔄 初始化EAI Interpretable Interface项目..."

# 激活conda环境
source ~/anaconda3/etc/profile.d/conda.sh
conda activate eai-eval

# 设置Python路径
export PYTHONPATH="$PWD:$PYTHONPATH"

# 创建必要的目录
mkdir -p logs
mkdir -p data
mkdir -p results
mkdir -p checkpoints

echo "✅ 项目初始化完成！"
echo "📁 当前目录: $PWD"
echo "🐍 Python路径: $(which python)"
echo "🌍 PYTHONPATH: $PYTHONPATH"
