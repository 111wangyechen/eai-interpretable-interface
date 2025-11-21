#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Sequencing Module
动作序列生成模块

该模块提供从目标描述到具体动作序列的完整解决方案，
支持多种规划算法、状态管理和数据加载功能。

主要组件:
- ActionSequencer: 核心序列生成器
- ActionPlanner: 动作规划算法实现
- StateManager: 环境状态管理
- DataLoader: 数据集加载和处理
- Action, ActionSequence: 动作和序列数据结构

作者: EAI Challenge Team
版本: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "EAI Challenge Team"
__email__ = "eai-challenge@example.com"

# 导入核心数据类
from .action_data import (
    ActionType,
    ActionStatus,
    Action,
    ActionSequence
)

# 导入状态管理相关类
from .state_manager import (
    StateType,
    StateVariable,
    StateTransition,
    EnvironmentState,
    StateManager
)

# 导入规划相关类
from .action_planner import (
    PlanningAlgorithm,
    HeuristicType,
    PlanningNode,
    PlanningResult,
    HeuristicCalculator,
    ActionPlanner
)

# 导入序列生成器相关类
from .action_sequencer import (
    SequencingConfig,
    SequencingRequest,
    SequencingResponse,
    ActionSequencer
)

# 导入数据加载相关类
from .data_loader import (
    DatasetConfig,
    VirtualHomeRecord,
    BehaviorRecord,
    DataLoader
)

# 定义模块公共接口
__all__ = [
    # 版本信息
    '__version__',
    '__author__',
    
    # 核心数据类
    'ActionType',
    'ActionStatus', 
    'Action',
    'ActionSequence',
    
    # 状态管理
    'StateType',
    'StateVariable',
    'StateTransition',
    'EnvironmentState',
    'StateManager',
    
    # 规划算法
    'PlanningAlgorithm',
    'HeuristicType',
    'PlanningNode',
    'PlanningResult',
    'HeuristicCalculator',
    'ActionPlanner',
    
    # 序列生成器
    'SequencingConfig',
    'SequencingRequest',
    'SequencingResponse',
    'ActionSequencer',
    
    # 数据加载
    'DatasetConfig',
    'VirtualHomeRecord',
    'BehaviorRecord',
    'DataLoader'
]

# 模块级别的便捷函数
def create_action_sequencer(
    algorithm: PlanningAlgorithm = PlanningAlgorithm.ASTAR,
    heuristic_type: HeuristicType = HeuristicType.GOAL_DISTANCE,
    max_depth: int = 50,
    max_time: float = 30.0,
    enable_cache: bool = True
) -> ActionSequencer:
    """
    创建配置好的ActionSequencer实例
    
    Args:
        algorithm: 规划算法类型
        heuristic_type: 启发式函数类型
        max_depth: 最大搜索深度
        max_time: 最大规划时间(秒)
        enable_cache: 是否启用缓存
        
    Returns:
        配置好的ActionSequencer实例
    """
    config = SequencingConfig(
        planning_algorithm=algorithm,
        heuristic_type=heuristic_type,
        max_depth=max_depth,
        max_time=max_time,
        enable_cache=enable_cache
    )
    
    return ActionSequencer(config)


def create_data_loader(
    virtualhome_path: str,
    behavior_path: str,
    max_samples: int = 1000,
    cache_data: bool = True
) -> DataLoader:
    """
    创建配置好的DataLoader实例
    
    Args:
        virtualhome_path: VirtualHome数据集路径
        behavior_path: Behavior数据集路径
        max_samples: 最大样本数量
        cache_data: 是否缓存数据
        
    Returns:
        配置好的DataLoader实例
    """
    config = DatasetConfig(
        virtualhome_path=virtualhome_path,
        behavior_path=behavior_path,
        max_samples=max_samples,
        cache_data=cache_data
    )
    
    return DataLoader(config)


def quick_sequence_generation(
    initial_state: dict,
    goal_state: dict,
    available_actions: list,
    algorithm: PlanningAlgorithm = PlanningAlgorithm.ASTAR
) -> SequencingResponse:
    """
    快速生成动作序列的便捷函数
    
    Args:
        initial_state: 初始状态
        goal_state: 目标状态
        available_actions: 可用动作列表
        algorithm: 规划算法
        
    Returns:
        序列生成响应
    """
    # 创建动作对象
    actions = []
    for action_dict in available_actions:
        if isinstance(action_dict, dict):
            action = Action(
                id=action_dict.get('id', f'action_{len(actions)}'),
                name=action_dict.get('name', 'UnnamedAction'),
                action_type=ActionType(action_dict.get('type', 'navigation')),
                parameters=action_dict.get('parameters', {}),
                preconditions=action_dict.get('preconditions', []),
                effects=action_dict.get('effects', []),
                duration=action_dict.get('duration', 1.0),
                success_probability=action_dict.get('success_probability', 1.0)
            )
            actions.append(action)
        else:
            actions.append(action_dict)
    
    # 创建请求
    request = SequencingRequest(
        initial_state=initial_state,
        goal_state=goal_state,
        available_actions=actions
    )
    
    # 创建序列生成器并生成序列
    sequencer = create_action_sequencer(algorithm=algorithm)
    return sequencer.generate_sequence(request)


# 模块初始化日志
import logging
logger = logging.getLogger(__name__)
logger.info(f"Action Sequencing Module v{__version__} loaded successfully")

# 检查依赖项
def check_dependencies():
    """检查模块依赖项"""
    required_packages = ['numpy', 'pandas', 'typing']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"Missing dependencies: {missing_packages}")
        return False
    
    return True


# 模块信息
def get_module_info():
    """获取模块信息"""
    return {
        'name': 'action_sequencing',
        'version': __version__,
        'author': __author__,
        'description': 'Action Sequencing Module for EAI Challenge',
        'components': [
            'ActionSequencer',
            'ActionPlanner', 
            'StateManager',
            'DataLoader'
        ],
        'algorithms': [
            'BFS', 'DFS', 'A*', 'Greedy', 'RRT'
        ],
        'supported_datasets': [
            'VirtualHome',
            'Behavior'
        ]
    }


# 在模块导入时检查依赖项
if not check_dependencies():
    logger.warning("Some dependencies are missing. Please install required packages.")

# 导出便捷函数
__all__.extend([
    'create_action_sequencer',
    'create_data_loader', 
    'quick_sequence_generation',
    'check_dependencies',
    'get_module_info'
])