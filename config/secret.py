# Configuration file for API keys and sensitive information
# Please keep this file secure and do not commit to version control

# Import LiteLLM to configure API keys
import litellm

# LLM Provider API Keys
API_KEYS = {
    # Example: OpenAI API key
    # "openai": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    
    # Example: Anthropic API key  
    # "anthropic": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    
    # Tongyi Qianwen 3-Max API key (DashScope)
    # Get from: https://dashscope.aliyun.com/
    "dashscope": "your-dashscope-api-key-here",
    
    # Add other API keys as needed
}

# Configure LiteLLM with the API keys dictionary
# This allows LiteLLM to automatically use the correct key for each model
litellm.api_key = API_KEYS

# Model configurations
MODEL_CONFIGS = {
    # Primary LLM model for transition modeling
    "primary_model": "qwen/qwen-turbo",  # Tongyi Qianwen Turbo
    
    # Fallback models in case primary fails
    "fallback_models": [
        "qwen/qwen-plus",  # Tongyi Qianwen Plus
        "gpt-3.5-turbo",   # OpenAI GPT-3.5 Turbo
    ],
    
    # Model parameters
    "default_params": {
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95,
    }
}

# Security settings
SECURITY = {
    # Enable/disable API key validation
    "validate_api_keys": True,
    
    # Rate limiting settings (requests per minute)
    "rate_limit": {
        "enabled": True,
        "requests_per_minute": 60,
    }
}

# Logging settings
LOGGING = {
    "level": "INFO",
    "file": "logs/app.log",
    "rotate": True,
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
}

# Export the configuration
export = {
    "API_KEYS": API_KEYS,
    "MODEL_CONFIGS": MODEL_CONFIGS,
    "SECURITY": SECURITY,
    "LOGGING": LOGGING,
}