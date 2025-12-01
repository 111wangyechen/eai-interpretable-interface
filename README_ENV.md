# 环境依赖配置指南

## 1. 依赖安装

确保已安装以下依赖包：

```bash
pip install litellm dashscope anthropic openai
```

## 2. 通义千问API配置

### 2.1 环境变量设置

在使用通义千问API之前，需要设置以下环境变量：

```bash
# Windows
set DASHSCOPE_API_KEY=your-dashscope-api-key

# Linux/Mac
export DASHSCOPE_API_KEY=your-dashscope-api-key
```

### 2.2 API密钥获取

1. 访问 [阿里云灵积平台](https://dashscope.aliyun.com/)
2. 注册并登录账号
3. 进入控制台，创建API密钥
4. 将获取的API密钥设置为环境变量

## 3. 代码结构说明

项目中与LLM集成相关的主要文件：

- `embodied-agent-interface/src/behavior_eval/evaluation/action_sequencing/scripts/replanning.py` - 行为评估的LLM调用
- `embodied-agent-interface/src/virtualhome_eval/simulation/evolving_graph/eval_utils.py` - 虚拟家庭评估的LLM调用
- `config/secret.py` - API密钥配置
- `tests/test_llm_integration.py` - LLM集成测试

## 4. 测试说明

### 4.1 运行LLM集成测试

```bash
cd d:\Tare_projects\eai-interface\eai-interpretable-interface
pytest tests/test_llm_integration.py -v
```

### 4.2 测试通义千问API连接

可以使用以下代码测试API连接：

```python
import os
from dashscope import Generation
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]

response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-max",
    messages=messages,
    result_format="message",
)

print(response.output.choices[0].message.content)
```

## 5. 常见问题

### 5.1 API调用失败

- 检查环境变量 `DASHSCOPE_API_KEY` 是否已正确设置
- 检查网络连接是否正常
- 检查API密钥是否有效

### 5.2 模型响应格式问题

- 确保在调用API时设置了正确的 `result_format` 参数
- 通义千问API默认返回消息格式，可通过 `result_format="message"` 指定

### 5.3 依赖版本冲突

- 建议使用最新版本的依赖包
- 可以通过 `pip list` 查看已安装的包版本
- 如有冲突，可使用 `pip install --upgrade package-name` 更新包

## 6. 最佳实践

1. 不要将API密钥硬编码到代码中，始终使用环境变量
2. 为不同的环境（开发、测试、生产）使用不同的API密钥
3. 合理设置API调用的重试机制，处理网络波动等异常情况
4. 定期更新依赖包，确保使用最新的API功能和安全补丁
5. 监控API调用频率，避免超过配额限制
