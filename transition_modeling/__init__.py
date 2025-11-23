#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transition Modeling Module
状态转换建模模块，负责建模环境状态转换和动作效果
"""

from .transition_modeler import TransitionModeler, ModelingRequest, ModelingResponse
from .state_transition import StateTransition, TransitionType, StateCondition, StateEffect
from .transition_predictor import TransitionPredictor
from .transition_validator import TransitionValidator

# 尝试导入LogicGuard模块
try:
    from .logic_guard import LogicGuard, create_logic_guard
    __all__ = [
        'TransitionModeler',
        'ModelingRequest',
        'ModelingResponse',
        'StateTransition', 
        'TransitionType',
        'StateCondition',
        'StateEffect',
        'TransitionPredictor',
        'TransitionValidator',
        'LogicGuard',
        'create_logic_guard'
    ]
except ImportError:
    # 如果导入失败，不包含LogicGuard在__all__中
    __all__ = [
        'TransitionModeler',
        'ModelingRequest',
        'ModelingResponse',
        'StateTransition', 
        'TransitionType',
        'StateCondition',
        'StateEffect',
        'TransitionPredictor',
        'TransitionValidator'
    ]
    import logging
    logging.warning("LogicGuard module could not be imported")

__version__ = '1.0.0'
__author__ = 'EAI Team'