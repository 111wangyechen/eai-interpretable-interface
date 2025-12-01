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
import yaml
import os
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
        self.confidence_threshold = self.config.get('confidence_threshold', 0.005)  # 降低置信度阈值
        self.max_predictions = self.config.get('max_predictions', 15)  # 增加最大预测数量
        self.use_historical_data = self.config.get('use_historical_data', True)
        
        # PDDL相关配置
        self.enable_pddl_semantics = self.config.get('enable_pddl_semantics', True)
        self.pddl_parameter_weight = self.config.get('pddl_parameter_weight', 0.2)
        
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
        
        # 场景配置
        self.scenarios_config = {}
        self.common_scenarios = {}
        
        # 加载场景配置
        self._load_scenarios_config()
        
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
                                       goal_state: Dict[str, Any],
                                       context: Optional[Dict[str, Any]] = None) -> float:
        """
        计算转换置信度，支持PDDL语义
        
        Args:
            transition: 状态转换
            current_state: 当前状态
            goal_state: 目标状态
            context: 上下文信息
            
        Returns:
            置信度分数 (0.0 - 1.0)
        """
        try:
            confidence = 0.0
            
            # 1. 前提条件满足度 (30%)
            precondition_score = self._evaluate_preconditions(transition, current_state)
            confidence += precondition_score * 0.30
            
            # 2. 目标相关性 (25%)
            relevance_score = self._calculate_goal_relevance(transition, current_state, goal_state)
            confidence += relevance_score * 0.25
            
            # 3. 历史成功率 (20%)
            historical_score = self._get_historical_success_rate(transition)
            confidence += historical_score * 0.20
            
            # 4. 转换复杂度惩罚 (10%)
            complexity_penalty = self._calculate_complexity_penalty(transition)
            confidence -= complexity_penalty * 0.10
            
            # 5. PDDL参数匹配度（如果启用）(10%)
            pddl_parameter_match = 1.0
            if self.enable_pddl_semantics and hasattr(transition, 'parameters') and transition.parameters:
                # 检查参数化谓词的匹配情况
                parameter_match_count = 0
                total_params = 0
                
                # 检查前置条件参数匹配
                for condition in transition.preconditions:
                    if hasattr(condition, 'params') and condition.params:
                        total_params += len(condition.params)
                        for param in condition.params:
                            if param in current_state:
                                parameter_match_count += 1
                
                # 检查效果参数匹配
                for effect in transition.effects:
                    if hasattr(effect, 'params') and effect.params:
                        total_params += len(effect.params)
                        for param in effect.params:
                            if param in goal_state:
                                parameter_match_count += 1
                
                if total_params > 0:
                    pddl_parameter_match = parameter_match_count / total_params
                confidence += pddl_parameter_match * 0.10
            
            # 6. 场景匹配度 (5%)
            scenario_match_score = self._calculate_scenario_match(transition, current_state, goal_state)
            confidence += scenario_match_score * 0.05
            
            # 确保最小置信度
            min_confidence = 0.01
            confidence = max(confidence, min_confidence)
            
            return max(0.0, min(1.0, confidence))
            
        except ZeroDivisionError as e:
            self.logger.error(f"Error calculating confidence for transition {transition.name}: Division by zero detected. Check all denominator values.")
            self.logger.error(f"Transition: {transition.name}, Current state: {current_state}, Goal state: {goal_state}")
            return 0.01  # 返回最小置信度而不是0
        except Exception as e:
            self.logger.error(f"Error calculating confidence for transition {transition.name}: {e}")
            self.logger.error(f"Transition: {transition.name}, Current state: {current_state}, Goal state: {goal_state}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return 0.01  # 返回最小置信度而不是0
    
    def validate_pddl_compatibility(self, transition: StateTransition) -> Dict[str, Any]:
        """
        验证转换的PDDL兼容性
        
        Args:
            transition: 转换对象
            
        Returns:
            兼容性验证报告
        """
        report = {
            'is_compatible': True,
            'issues': [],
            'missing_elements': []
        }
        
        # 检查是否有parameters属性
        if not hasattr(transition, 'parameters'):
            report['issues'].append('缺少parameters属性')
            report['is_compatible'] = False
        
        # 检查前提条件是否支持PDDL格式
        for i, condition in enumerate(transition.preconditions):
            if not hasattr(condition, 'to_pddl'):
                report['issues'].append(f'前提条件[{i}]不支持PDDL格式转换')
                report['is_compatible'] = False
            
        # 检查效果是否支持PDDL格式
        for i, effect in enumerate(transition.effects):
            if not hasattr(effect, 'to_pddl'):
                report['issues'].append(f'效果[{i}]不支持PDDL格式转换')
                report['is_compatible'] = False
        
        return report
    
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
        """计算状态相似度，增强部分匹配和语义相似性"""
        if not state1 or not state2:
            return 0.0
        
        all_keys = set(state1.keys()) | set(state2.keys())
        common_keys = set(state1.keys()) & set(state2.keys())
        
        if not all_keys:
            return 0.0
        
        # 精确匹配分数
        exact_matches = sum(1 for key in common_keys if state1[key] == state2[key])
        exact_score = exact_matches / len(common_keys) if common_keys else 0.0
        
        # 部分匹配分数 - 考虑每个状态是否包含了目标状态的关键部分
        goal_key_match = 0
        for key in state2.keys():
            if key in state1:
                # 考虑布尔值和数值的部分匹配
                if isinstance(state1[key], bool) and isinstance(state2[key], bool):
                    goal_key_match += 1 if state1[key] == state2[key] else 0
                elif isinstance(state1[key], (int, float)) and isinstance(state2[key], (int, float)):
                    # 数值相似度计算
                    diff = abs(state1[key] - state2[key])
                    max_val = max(abs(state1[key]), abs(state2[key]), 1.0)  # 避免除以0
                    similarity = 1.0 - min(1.0, diff / max_val)
                    goal_key_match += similarity
                else:
                    goal_key_match += 1 if state1[key] == state2[key] else 0.3  # 部分匹配给0.3分
        
        partial_score = goal_key_match / len(state2.keys()) if state2 else 0.0
        
        # 综合相似度分数
        similarity = (exact_score * 0.6) + (partial_score * 0.4)
        
        return similarity
    
    def _get_historical_success_rate(self, transition: StateTransition) -> float:
        """获取历史成功率，增强对常见场景的加权"""
        transition_key = f"{transition.name}_{transition.transition_type.value}"
        base_rate = self.success_rates.get(transition_key, 0.5)  # 默认0.5
        
        # 为常见场景增加权重
        for scenario, data in self.common_scenarios.items():
            if transition.name in data.get('transitions', []):
                # 常见场景的转换给予额外加权
                base_rate = max(base_rate, 0.6 + data.get('weight', 0.0))  # 至少0.6的基础成功率
                break
        
        # 基于转换类型调整基础率
        if transition.transition_type.value == 'atomic':
            base_rate = min(1.0, base_rate + 0.05)  # 原子转换更可靠
        elif transition.transition_type.value == 'conditional':
            base_rate = max(0.3, base_rate - 0.05)  # 条件转换可靠性稍低
        
        return base_rate
    
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
                             max_depth: int = 15) -> List[List[StateTransition]]:
        """
        预测状态转换序列，增强对常见场景的支持
        
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
                # 即使达到深度限制，也保存部分路径
                if self._calculate_state_similarity(current_state, goal_state) >= 0.4:
                    sequences.append(path.copy())
                return
            
            # 检查是否达到目标
            similarity = self._calculate_state_similarity(current_state, goal_state)
            if similarity >= 0.7:  # 降低目标达成的相似度阈值
                sequences.append(path.copy())
                # 继续搜索更优路径
                if similarity < 0.95:
                    pass
                else:
                    return
            
            # 获取适用的转换
            applicable_transitions = [
                t for t in available_transitions 
                if t.is_applicable(current_state)
            ]
            
            # 预测并排序转换
            predictions = self.predict_transitions(
                current_state, goal_state, applicable_transitions
            )
            
            # 探索前几个最佳预测
            for transition, confidence in predictions[:5]:  # 增加探索的转换数量
                next_state = transition.apply_effects(current_state)
                path.append(transition)
                search_path(next_state, path, depth + 1)
                path.pop()
        
        search_path(initial_state, [], 0)
        
        # 为常见场景添加预设序列
        if not sequences:
            for scenario, data in self.common_scenarios.items():
                scenario_sequences = []
                current_path = []
                current_state = initial_state.copy()
                
                # 尝试构建场景序列
                for transition_name in data['transitions']:
                    matching_transitions = [t for t in available_transitions if t.name == transition_name]
                    if matching_transitions:
                        transition = matching_transitions[0]
                        if transition.is_applicable(current_state):
                            current_path.append(transition)
                            current_state = transition.apply_effects(current_state)
                        else:
                            break
                
                if len(current_path) >= 2:  # 至少有2个有效转换
                    sequences.append(current_path)
        
        # 按路径长度和置信度排序
        if sequences:
            sequences.sort(key=lambda seq: (
                -len(seq),  # 优先更长的序列
                sum(self._calculate_transition_confidence(t, initial_state, goal_state) for t in seq)  # 然后是总置信度
            ))
        
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
    
    def _load_scenarios_config(self):
        """
        从配置文件加载场景配置
        """
        scenarios_path = os.path.join('config', 'scenarios.yaml')
        
        try:
            if os.path.exists(scenarios_path):
                with open(scenarios_path, 'r', encoding='utf-8') as f:
                    scenarios_data = yaml.safe_load(f)
                
                self.scenarios_config = scenarios_data.get('scenarios', {})
                
                # 转换为common_scenarios格式
                for scenario_name, scenario_config in self.scenarios_config.items():
                    if scenario_config.get('enabled', True):
                        # 从场景配置中提取转换规则
                        transition_config = scenario_config.get('transition', {})
                        self.common_scenarios[scenario_name] = {
                            'transitions': transition_config.get('allowed_types', []),
                            'weight': transition_config.get('default_cost', 0.5),
                            'min_length': transition_config.get('min_length', 2),
                            'max_length': transition_config.get('max_length', 5)
                        }
                
                self.logger.info(f"Loaded scenarios configuration from {scenarios_path}")
            else:
                # 使用默认场景配置
                self.common_scenarios = {
                    'open_fridge_take_milk': {
                        'transitions': ['open_fridge', 'take_milk', 'pour_cup'],
                        'weight': 0.3,
                        'min_length': 2,
                        'max_length': 5
                    },
                    'make_coffee': {
                        'transitions': ['open_cabinet', 'take_coffee', 'pour_water', 'brew_coffee'],
                        'weight': 0.25,
                        'min_length': 2,
                        'max_length': 5
                    }
                }
                self.logger.warning(f"Scenarios config file not found at {scenarios_path}, using default scenarios")
        except Exception as e:
            self.logger.error(f"Failed to load scenarios config: {e}")
            # 使用默认配置
            self.common_scenarios = {
                'open_fridge_take_milk': {
                    'transitions': ['open_fridge', 'take_milk', 'pour_cup'],
                    'weight': 0.3,
                    'min_length': 2,
                    'max_length': 5
                },
                'make_coffee': {
                    'transitions': ['open_cabinet', 'take_coffee', 'pour_water', 'brew_coffee'],
                    'weight': 0.25,
                    'min_length': 2,
                    'max_length': 5
                }
            }
    
    def _calculate_scenario_match(self, 
                                 transition: StateTransition,
                                 current_state: Dict[str, Any],
                                 goal_state: Dict[str, Any]) -> float:
        """
        计算转换与当前场景的匹配度
        
        Args:
            transition: 状态转换
            current_state: 当前状态
            goal_state: 目标状态
            
        Returns:
            场景匹配分数 (0.0 - 1.0)
        """
        match_score = 0.0
        match_count = 0
        
        # 检查转换是否属于任何常见场景
        for scenario, scenario_data in self.common_scenarios.items():
            if transition.name in scenario_data.get('transitions', []):
                match_score += 1.0
                match_count += 1
        
        # 基于状态上下文调整匹配分数
        for scenario, scenario_data in self.common_scenarios.items():
            scenario_config = self.scenarios_config.get(scenario, {})
            # 简单的状态匹配检查
            if scenario_config.get('name') in str(current_state):
                match_score += 0.5
                match_count += 1
            if scenario_config.get('name') in str(goal_state):
                match_score += 0.5
                match_count += 1
        
        if match_count == 0:
            return 0.0
        
        return min(1.0, match_score / match_count)
    
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
            
            # 重新加载场景配置，确保最新
            self._load_scenarios_config()
            
            self.logger.info(f"Model loaded from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise