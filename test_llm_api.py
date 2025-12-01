#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试LLM API连接的脚本
用于验证通义千问API密钥配置是否正确
"""

import os
import sys

# 添加项目根目录到Python路径，以便导入配置
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入必要的库
import litellm
from config.secret import API_KEYS

def test_llm_connection():
    """
    测试LLM API连接是否正常
    """
    print("开始测试LLM API连接...")
    print(f"已加载的API密钥提供方: {list(API_KEYS.keys())}")
    
    # 确保LiteLLM已正确配置
    if hasattr(litellm, 'api_key'):
        print("LiteLLM API密钥配置已加载")
    else:
        print("警告: LiteLLM API密钥配置未加载")
        # 手动配置LiteLLM
        litellm.api_key = API_KEYS
    
    # 测试通义千问3-Max模型
    try:
        print("\n测试通义千问3-Max模型...")
        response = litellm.completion(
            model="qwen3-max",
            messages=[{"role": "user", "content": "测试API连接，请返回'连接成功'"}],
            max_tokens=50
        )
        
        # 检查响应
        if response and hasattr(response, 'choices') and response.choices:
            content = response.choices[0].message.content
            print(f"✓ 通义千问3-Max调用成功!")
            print(f"响应内容: {content}")
        else:
            print("⚠ 收到响应但格式异常")
            print(f"完整响应: {response}")
            
    except Exception as e:
        print(f"✗ 通义千问3-Max调用失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {str(e)}")
        
        # 根据错误类型提供建议
        if "AuthenticationError" in str(type(e).__name__):
            print("\n建议: 请检查API密钥是否正确。请从https://dashscope.aliyun.com/获取正确的密钥。")
        elif "ConnectionError" in str(type(e).__name__):
            print("\n建议: 请检查网络连接是否正常。")
        else:
            print("\n建议: 请检查secret.py中的API_KEYS配置是否正确。")
    
    print("\n测试完成！")

if __name__ == "__main__":
    # 显示使用说明
    print("=" * 60)
    print("LLM API连接测试工具")
    print("=" * 60)
    print("此工具用于验证通义千问API密钥配置是否正确")
    print("请确保:")
    print("1. config/secret.py中的API_KEYS字典包含正确的'dashscope'密钥")
    print("2. 已安装必要的依赖: pip install litellm dashscope")
    print("3. 网络连接正常")
    print("=" * 60)
    
    # 运行测试
    test_llm_connection()
