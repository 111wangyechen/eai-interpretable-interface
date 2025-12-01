# Configuration file for API keys and sensitive information
# Please keep this file secure and do not commit to version control

# LLM Provider API Keys
API_KEYS = {
    # Tongyi Qianwen 3-Max API key (DashScope)
    "dashscope": "sk-4eb2cc33545742999a0570f40e680f40",  # 你的真实密钥
    # 其他密钥（如OpenAI）可保留，不影响
}

# Model configurations（适配原生调用）
MODEL_CONFIGS = {
    "primary_model": "qwen3-max",  # 原生调用无需前缀
    "fallback_models": ["qwen-plus"],
    "default_params": {
        "temperature": 0.1,
        "max_tokens": 1000,
        "top_p": 0.9,
    }
}

# 其他配置（安全、日志）可保留，不影响
SECURITY = {
    "validate_api_keys": True,
    "rate_limit": {
        "enabled": True,
        "requests_per_minute": 60,
    }
}

LOGGING = {
    "level": "INFO",
    "file": "logs/app.log",
    "rotate": True,
    "max_size": 10 * 1024 * 1024,
    "backup_count": 5,
    "console_output": True,
}

# Export the configuration
export = {
    "API_KEYS": API_KEYS,
    "MODEL_CONFIGS": MODEL_CONFIGS,
    "SECURITY": SECURITY,
    "LOGGING": LOGGING,
}