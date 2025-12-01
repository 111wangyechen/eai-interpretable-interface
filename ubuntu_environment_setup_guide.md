# Ubuntu 环境配置指导

## 1. 基础环境准备

### 1.1 更新系统包
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 安装Python和pip
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 1.3 安装Git
```bash
sudo apt install git -y
```

## 2. 项目克隆与设置

### 2.1 克隆项目仓库
```bash
git clone <your-github-repository-url>
cd eai-interpretable-interface
```

### 2.2 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. 依赖安装

### 3.1 安装核心依赖
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.2 安装LiteLLM与通义千问3-Max依赖
```bash
pip install litellm>=1.37.0 dashscope>=1.14.0 anthropic>=0.20.0 openai>=1.0.0
```

## 4. 配置文件设置

### 4.1 创建配置目录
```bash
mkdir -p config
```

### 4.2 创建secret.py文件
```bash
touch config/secret.py
```

编辑secret.py文件，添加以下内容：
```python
# 配置文件示例

# LiteLLM配置
LITELLM_CONFIG = {
    "timeout": 30,
    "max_retries": 3
}

# 通义千问API密钥
DASHSCOPE_API_KEY = "your-dashscope-api-key"

# OpenAI API密钥（可选）
OPENAI_API_KEY = "your-openai-api-key"

# Anthropic API密钥（可选）
ANTHROPIC_API_KEY = "your-anthropic-api-key"
```

### 4.3 创建scenarios.yaml文件
```bash
touch config/scenarios.yaml
```

编辑scenarios.yaml文件，添加以下内容：
```yaml
# 场景配置
scenarios:
  - id: "default"
    name: "默认场景"
    description: "基础测试场景"
    initial_state:
      - "(at robot location1)"
      - "(holding robot nothing)"
    goal_state:
      - "(at robot location2)"
    available_actions:
      - "move"
      - "pick"
      - "place"

  - id: "kitchen"
    name: "厨房场景"
    description: "厨房环境测试场景"
    initial_state:
      - "(at robot kitchen)"
      - "(holding robot nothing)"
      - "(on cup counter)"
    goal_state:
      - "(on cup table)"
    available_actions:
      - "move"
      - "pick"
      - "place"
      - "grasp"
```

## 5. 环境验证

### 5.1 运行依赖检查脚本
```bash
python check_dependencies.py
```

### 5.2 运行测试用例
```bash
python -m pytest tests/test_imports.py -v
```

## 6. 常见问题解决

### 6.1 权限问题
如果遇到权限错误，可以尝试：
```bash
sudo chown -R $USER:$USER eai-interpretable-interface
```

### 6.2 依赖冲突
如果遇到依赖冲突，可以尝试：
```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### 6.3 Python版本问题
确保使用Python 3.8或更高版本：
```bash
python3 --version
```

## 7. 启动项目

### 7.1 运行演示
```bash
python run_demo.py
```

### 7.2 运行完整测试
```bash
python run_tests.py
```

---

**注意**：请将上述命令中的占位符（如`<your-github-repository-url>`、`your-dashscope-api-key`等）替换为实际值。
