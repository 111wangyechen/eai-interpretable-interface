#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transition Predictor
状态转换预测器，预测状态转换的可能性和效果
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np
import json
import time
from collections import defaultdict, Counter
import logging

try:
    from .state_transition import StateTransition, TransitionType, TransitionStatus, StateCondition, StateEffect
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from state_transition import StateTransition, TransitionType, TransitionStatus, StateCondition, StateEffect


class TransitionPredictor:
    """状态转换预测器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化转换预测器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 预测模型参数
        self.confidence_threshold = self.config.get('confidence_threshold', 0.01)
        self.max_predictions = self.config.get('max_predictions', 10)
        self.use_historical_data = self.config.get('use_historical_data', True)
        
        # 历史数据存储
        self.transition_history: List[Dict[str, Any]] = []
        self.success_rates: Dict[str, float] = {}
        self.state_patterns: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # 统计信息
        self.prediction_stats = {
            'total_predictions': 0,
            'successful_predictions': 0,
            'accuracy': 0.0
        }
        
        self.logger.info("Transition Predictor initialized")
    
    def predict_transitions(self, 
                          current_state: Dict[str, Any], 
                          goal_state: Dict[str, Any],
                          available_transitions: List[StateTransition]) -> List[Tuple[StateTransition, float]]:
        """
        预测最可能的状态转换
        
        Args:
            current_state: 当前状态
            goal_state: 目标状态
            available_transitions: 可用转换列表
            
        Returns:
            转换和置信度的排序列表
        """
        predictions = []
        
        for transition in available_transitions:
            confidence = self._calculate_transition_confidence(
                transition, current_state, goal_state
            )
            
            if confidence >= self.confidence_threshold:
                predictions.append((transition, confidence))
        
        # 按置信度排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # 限制预测数量
        predictions = predictions[:self.max_predictions]
        
        self.prediction_stats['total_predictions'] += 1
        
        self.logger.info(f"Generated {len(predictions)} transition predictions")
        return predictions
    
    def _calculate_transition_confidence(self, 
                                       transition: StateTransition,
                                       current_state: Dict[str, Any], 
                                       goal_state: Dict[str, Any]) -> float:
        """
        计算转换置信度
        
        Args:
            transition: 状态转换
            current_state: 当前状态
            goal_state: 目标状态
            
        Returns:
            置信度分数 (0.0 - 1.0)
        """
        try:
            confidence = 0.0
            
            # 1. 前提条件满足度 (40%) - 增加权重
            precondition_score = self._evaluate_preconditions(transition, current_state)
            confidence += precondition_score * 0.4
            
            # 2. 目标相关性 (40%) - 保持高权重
            relevance_score = self._calculate_goal_relevance(transition, current_state, goal_state)
            confidence += relevance_score * 0.4
            
            # 3. 历史成功率 (20%) - 保持权重
            historical_score = self._get_historical_success_rate(transition)
            confidence += historical_score * 0.2
            
            # 4. 转换复杂度惩罚 (5%) - 降低惩罚
            complexity_penalty = self._calculate_complexity_penalty(transition)
            confidence -= complexity_penalty * 0.05
            
            # 确保最小置信度 - 修复：避免完全过滤掉所有转换
            min_confidence = 0.01  # 设置最小置信度，与阈值保持一致
            confidence = max(confidence, min_confidence)
            
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence for transition {transition.name}: {e}")
            return 0.01  # 返回最小置信度而不是0
    
    def _evaluate_preconditions(self, transition: StateTransition, state: Dict[str, Any]) -> float:
        """评估前提条件满足度"""
        if not transition.preconditions:
            return 1.0
        
        satisfied_count = sum(1 for cond in transition.preconditions if cond.evaluate(state))
        return satisfied_count / len(transition.preconditions)
    
    def _calculate_goal_relevance(self, 
                                transition: StateTransition,
                                current_state: Dict[str, Any], 
                                goal_state: Dict[str, Any]) -> float:
        """计算目标相关性"""
        if not transition.effects:
            return 0.0
        
        # 模拟应用转换效果
        predicted_state = transition.apply_effects(current_state)
        
        # 计算与目标状态的相似度
        similarity = self._calculate_state_similarity(predicted_state, goal_state)
        
        return similarity
    
    def _calculate_state_similarity(self, state1: Dict[str, Any], state2: Dict[str, Any]) -> float:
        """计算状态相似度"""
        if not state1 or not state2:
            return 0.0
        
        common_keys = set(state1.keys()) & set(state2.keys())
        if not common_keys:
            return 0.0
        
        matches = sum(1 for key in common_keys if state1[key] == state2[key])
        return matches / len(common_keys)
    
    def _get_historical_success_rate(self, transition: StateTransition) -> float:
        """获取历史成功率"""
        transition_key = f"{transition.name}_{transition.transition_type.value}"
        return self.success_rates.get(transition_key, 0.5)  # 默认0.5
    
    def _calculate_complexity_penalty(self, transition: StateTransition) -> float:
        """计算复杂度惩罚"""
        penalty = 0.0
        
        # 前提条件复杂度
        penalty += len(transition.preconditions) * 0.05
        
        # 效果复杂度
        penalty += len(transition.effects) * 0.03
        
        # 时间成本
        penalty += transition.duration * 0.02
        
        # 资源成本
        penalty += transition.cost * 0.01
        
        return min(0.5, penalty)  # 最大惩罚0.5
    
    def predict_state_sequence(self, 
                             initial_state: Dict[str, Any],
                             goal_state: Dict[str, Any],
                             available_transitions: List[StateTransition],
                             max_depth: int = 10) -> List[List[StateTransition]]:
        """
        预测状态转换序列
        
        Args:
            initial_state: 初始状态
            goal_state: 目标状态
            available_transitions: 可用转换列表
            max_depth: 最大搜索深度
            
        Returns:
            可能的转换序列列表
        """
        sequences = []
        
        def search_path(current_state: Dict[str, Any], 
                       path: List[StateTransition], 
                       depth: int):
            """递归搜索路径"""
            if depth >= max_depth:
                return
            
            # 检查是否达到目标
            if self._calculate_state_similarity(current_state, goal_state) >= 0.8:
                sequences.append(path.copy())
                return
            
            # 获取适用的转换
            applicable_transitions = [
                t for t in available_transitions 
                if t.is_applicable(current_state) and t not in path
            ]
            
            # 预测并排序转换
            predictions = self.predict_transitions(
                current_state, goal_state, applicable_transitions
            )
            
            # 探索前几个最佳预测
            for transition, confidence in predictions[:3]:
                next_state = transition.apply_effects(current_state)
                path.append(transition)
                search_path(next_state, path, depth + 1)
                path.pop()
        
        search_path(initial_state, [], 0)
        
        # 按路径长度和置信度排序
        sequences.sort(key=lambda seq: (len(seq), sum(
            self._calculate_transition_confidence(t, initial_state, goal_state) 
            for t in seq
        )))
        
        self.logger.info(f"Generated {len(sequences)} possible sequences")
        return sequences
    
    def update_historical_data(self, 
                             transition: StateTransition, 
                             success: bool,
                             execution_time: float):
        """
        更新历史数据
        
        Args:
            transition: 执行的转换
            success: 是否成功
            execution_time: 执行时间
        """
        transition_key = f"{transition.name}_{transition.transition_type.value}"
        
        # 更新成功率
        if transition_key not in self.success_rates:
            self.success_rates[transition_key] = 0.5
        
        # 指数移动平均更新
        alpha = 0.1  # 学习率
        current_rate = self.success_rates[transition_key]
        new_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * current_rate
        self.success_rates[transition_key] = new_rate
        
        # 记录历史
        self.transition_history.append({
            'transition_key': transition_key,
            'success': success,
            'execution_time': execution_time,
            'timestamp': time.time()
        })
        
        self.logger.info(f"Updated historical data for {transition_key}: {new_rate:.3f}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取预测器统计信息"""
        return {
            'prediction_stats': self.prediction_stats,
            'success_rates': self.success_rates,
            'transition_history_size': len(self.transition_history),
            'state_patterns_count': len(self.state_patterns)
        }
    
    def save_model(self, filepath: str):
        """保存预测器模型"""
        model_data = {
            'config': self.config,
            'success_rates': self.success_rates,
            'prediction_stats': self.prediction_stats,
            'transition_history': self.transition_history[-1000:],  # 保存最近1000条记录
            'state_patterns': dict(self.state_patterns)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """加载预测器模型"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                model_data = json.load(f)
            
            self.config = model_data.get('config', {})
            self.success_rates = model_data.get('success_rates', {})
            self.prediction_stats = model_data.get('prediction_stats', {
                'total_predictions': 0,
                'successful_predictions': 0,
                'accuracy': 0.0
            })
            self.transition_history = model_data.get('transition_history', [])
            self.state_patterns = defaultdict(list, model_data.get('state_patterns', {}))
            
            self.logger.info(f"Model loaded from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise