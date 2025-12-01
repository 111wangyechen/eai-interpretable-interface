#!/usr/bin/env python3
"""
版本信息模块
"""

# 项目版本信息
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__build_date__ = "2025-02-29"
__build_number__ = "2025022901"

# 模块版本信息
MODULE_VERSIONS = {
    "goal_interpretation": "1.0.0",
    "action_sequencing": "1.0.0",
    "transition_modeling": "1.0.0",
    "subgoal_decomposition": "1.0.0",
    "integration": "1.0.0",
    "utils": "1.0.0"
}

# 依赖版本要求
DEPENDENCY_REQUIREMENTS = {
    "python": ">=3.8.0",
    "transformers": ">=4.30.0",
    "torch": ">=2.0.0",
    "numpy": ">=1.24.0",
    "yaml": ">=6.0",
    "pydantic": ">=2.0.0"
}

# 版本信息类
class VersionInfo:
    """版本信息类"""
    
    def __init__(self):
        self.version = __version__
        self.version_info = __version_info__
        self.build_date = __build_date__
        self.build_number = __build_number__
        self.module_versions = MODULE_VERSIONS.copy()
        self.dependency_requirements = DEPENDENCY_REQUIREMENTS.copy()
    
    def get_version_string(self) -> str:
        """获取完整版本字符串"""
        return f"{self.version} ({self.build_number}, {self.build_date})"
    
    def get_module_versions(self) -> dict:
        """获取各模块版本"""
        return self.module_versions.copy()
    
    def get_dependency_requirements(self) -> dict:
        """获取依赖要求"""
        return self.dependency_requirements.copy()
    
    def __str__(self) -> str:
        """字符串表示"""
        return self.get_version_string()

# 单例版本信息对象
version_info = VersionInfo()
