#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通义千问3-Max 原生API测试脚本（无LiteLLM依赖）
"""
import os
import sys
from http import HTTPStatus
# 导入Dashscope官方SDK
import dashscope
from dashscope import Generation

# ===================== 核心配置 =====================
# 方式1：从环境变量读取密钥（推荐，和curl一致）
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 方式2：手动硬编码（仅测试用，不要提交到仓库）
# DASHSCOPE_API_KEY = "sk-4eb2cc33545742999a0570f40e680f40"

# 国内端点（和curl成功的端点一致）
dashscope.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# 配置密钥
dashscope.api_key = DASHSCOPE_API_KEY

# ===================== 测试函数 =====================
def test_qwen3_max():
    print("=" * 60)
    print("通义千问3-Max 原生API测试工具")
    print("=" * 60)
    
    # 1. 前置校验
    if not DASHSCOPE_API_KEY:
        print("❌ 错误：未读取到DASHSCOPE_API_KEY环境变量！")
        print("请先执行：export DASHSCOPE_API_KEY='你的密钥'")
        sys.exit(1)
    print(f"✅ 已加载密钥（前8位）：{DASHSCOPE_API_KEY[:8]}...")
    print(f"✅ 已配置国内端点：{dashscope.api_base}")

    # 2. 测试参数（和curl一致）
    test_messages = [{"role": "user", "content": "测试：请返回\"开通成功\""}]
    
    try:
        print("\n开始调用通义千问3-Max...")
        # 原生SDK调用（兼容OpenAI格式）
        response = Generation.call(
            model="qwen3-max",          # 模型名（无需前缀）
            messages=test_messages,     # 对话消息
            result_format="message",    # 返回OpenAI兼容格式
            max_tokens=50,              # 最大生成token
            temperature=0.1,            # 低随机性
            timeout=10                  # 超时时间
        )

        # 3. 响应校验
        if response.status_code == HTTPStatus.OK:
            content = response.output.choices[0].message.content.strip()
            print("✅ 调用成功！")
            print(f"响应内容：{content}")
            # 可选：打印完整响应（调试用）
            # print(f"完整响应：{response}")
        else:
            print(f"❌ 调用失败：{response.code} - {response.message}")

    except Exception as e:
        print(f"❌ 调用异常！")
        print(f"错误类型：{type(e).__name__}")
        print(f"错误详情：{str(e)}")

    print("=" * 60)
    print("测试完成！")

# ===================== 运行测试 =====================
if __name__ == "__main__":
    test_qwen3_max()