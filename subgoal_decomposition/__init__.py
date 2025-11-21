#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子目标分解模块
提供LTL公式分解为子目标的完整解决方案
"""

from .subgoal_decomposer import (
    SubgoalType,
    DecompositionStrategy,
    Subgoal,
    DecompositionResult,
    SubgoalDecomposer
)

from .subgoal_validator import (
    ValidationIssue,
    OptimizationResult,
    SubgoalValidator,
    SubgoalOptimizer,
    SubgoalAnalyzer
)

from .subgoal_ltl_integration import (
    IntegrationResult,
    SubgoalLTLIntegration
)

__version__ = "1.0.0"
__author__ = "EAI Team"

__all__ = [
    # 核心枚举和数据类
    'SubgoalType',
    'DecompositionStrategy',
    'Subgoal',
    'DecompositionResult',
    'ValidationIssue',
    'OptimizationResult',
    'IntegrationResult',
    
    # 核心类
    'SubgoalDecomposer',
    'SubgoalValidator',
    'SubgoalOptimizer',
    'SubgoalAnalyzer',
    'SubgoalLTLIntegration',
]