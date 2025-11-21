"""
EAI兼容层 - 为InterPreT集成提供EAI接口
当官方EAI包不可用时的替代实现
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import gym
import json

class MockEAIAgent:
    """模拟EAI Agent类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.action_space = None
        self.observation_space = None
        
    def reset(self):
        """重置agent状态"""
        return np.zeros(10)  # 模拟观察空间
        
    def step(self, action):
        """执行动作"""
        observation = np.random.rand(10)
        reward = np.random.rand()
        done = False
        info = {}
        return observation, reward, done, info
        
    def get_action(self, observation):
        """根据观察获取动作"""
        return np.random.randint(0, 10)

class MockEnvironment:
    """模拟EAI Environment类"""
    
    def __init__(self, env_id: str, config: Dict[str, Any] = None):
        self.env_id = env_id
        self.config = config or {}
        self.agent = MockEAIAgent(config)
        
    def reset(self):
        """重置环境"""
        return self.agent.reset()
        
    def step(self, action):
        """环境步进"""
        return self.agent.step(action)
        
    def render(self, mode='human'):
        """渲染环境"""
        pass

# 创建模拟的eai模块
class EAIModule:
    """EAI模块的兼容实现"""
    
    __version__ = "1.0.0-compat"
    
    @staticmethod
    def make(env_id: str, **kwargs):
        """创建环境"""
        return MockEnvironment(env_id, kwargs)
        
    @staticmethod
    def Agent(config: Dict[str, Any] = None):
        """创建Agent"""
        return MockEAIAgent(config)

# 导出接口
agent = EAIModule.Agent
make = EAIModule.make
Agent = MockEAIAgent
Environment = MockEnvironment

# 版本信息
__version__ = "1.0.0-compat"
