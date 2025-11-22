#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Sequencing核心类
整合动作规划、状态管理和数据加载功能，提供完整的动作序列生成服务
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict, field
import json
import time
import logging
from pathlib import Path

# 导入缓存管理器
try:
    # 尝试绝对导入
    from eai_interpretable_interface.utils.cache_manager import CacheManager, cache_result
except ImportError:
    # 如果绝对导入失败，尝试相对导入
    try:
        from utils.cache_manager import CacheManager, cache_result
    except ImportError:
        # 如果都失败，创建一个简单的回退实现
        class CacheManager:
            def __init__(self, cache_size=1000, ttl=3600, name="cache"):
                self.cache = {}
                self.name = name
            def get(self, key):
                return self.cache.get(key)
            def set(self, key, value):
                self.cache[key] = value
            def clear(self):
                self.cache.clear()
            def __len__(self):
                return len(self.cache)
        
        def cache_result(func):
            return func

from .action_data import Action, ActionSequence, ActionType, ActionStatus
from .state_manager import EnvironmentState, StateManager
from .action_planner import ActionPlanner, PlanningAlgorithm, PlanningResult, HeuristicType
from .aude_re import AuDeRe, AudereConfig, create_aude_re


@dataclass
class SequencingConfig:
    """动作序列配置类"""
    planning_algorithm: PlanningAlgorithm = PlanningAlgorithm.ASTAR
    heuristic_type: HeuristicType = HeuristicType.GOAL_DISTANCE
    max_depth: int = 50
    max_time: float = 30.0
    enable_logging: bool = True
    log_level: str = "INFO"
    cache_results: bool = True
    validate_sequences: bool = True
    
    # AuDeRe配置
    enable_aude_re: bool = True
    aude_re_config: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'SequencingConfig':
        """从字典创建配置"""
        # 处理枚举类型
        if 'planning_algorithm' in config_dict:
            config_dict['planning_algorithm'] = PlanningAlgorithm(config_dict['planning_algorithm'])
        if 'heuristic_type' in config_dict:
            config_dict['heuristic_type'] = HeuristicType(config_dict['heuristic_type'])
        
        return cls(**config_dict)


@dataclass
class SequencingRequest:
    """动作序列请求类"""
    initial_state: Dict[str, Any]
    goal_state: Dict[str, Any]
    available_actions: List[Action]
    state_transitions: Optional[List[Dict[str, Any]]] = None
    constraints: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    subgoals: Optional[List[Any]] = None  # 子目标信息
    transition_modeling_result: Optional[Any] = None  # 转换建模结果
    
    def validate(self) -> bool:
        """验证请求的有效性"""
        if not self.initial_state:
            return False
        if not self.goal_state:
            return False
        if not self.available_actions:
            return False
        return True


@dataclass
class SequencingResponse:
    """动作序列响应类"""
    success: bool
    action_sequence: Optional[ActionSequence]
    planning_result: Optional[PlanningResult]
    execution_time: float
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """后处理初始化"""
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'success': self.success,
            'action_sequence': self.action_sequence.to_dict() if self.action_sequence else None,
            'planning_result': asdict(self.planning_result) if self.planning_result else None,
            'execution_time': self.execution_time,
            'error_message': self.error_message,
            'metadata': self.metadata
        }
        return result


class ActionSequencer:
    """动作序列生成器核心类"""
    
    def __init__(self, config: Optional[SequencingConfig] = None):
        """
        初始化动作序列生成器
        
        Args:
            config: 配置对象
        """
        self.config = config or SequencingConfig()
        self.state_manager = StateManager()
        # 将字符串算法名称转换为枚举
        algorithm_enum = self.config.planning_algorithm
        if isinstance(self.config.planning_algorithm, str):
            try:
                algorithm_enum = PlanningAlgorithm(self.config.planning_algorithm)
            except ValueError:
                # 如果字符串不匹配任何枚举值，使用默认算法
                algorithm_enum = PlanningAlgorithm.ASTAR
                if self.config.enable_logging:
                    self.logger.warning(f"Unknown planning algorithm '{self.config.planning_algorithm}', using ASTAR instead")
        
        self.action_planner = ActionPlanner(
            algorithm=algorithm_enum,
            heuristic_type=self.config.heuristic_type,
            max_depth=self.config.max_depth,
            max_time=self.config.max_time
        )
        
        # 设置日志
        if self.config.enable_logging:
            self._setup_logging()
        
        # 初始化AuDeRe模块
        self.aude_re = None
        if self.config.enable_aude_re:
            try:
                self.aude_re = create_aude_re(self.config.aude_re_config)
                if self.config.enable_logging:
                    self.logger.info("AuDeRe module initialized successfully")
            except Exception as e:
                if self.config.enable_logging:
                    self.logger.error(f"Failed to initialize AuDeRe module: {str(e)}")
        
        # 结果缓存 - 使用CacheManager替代简单字典
        self._cache_manager = CacheManager(
            cache_size=1000,  # 设置合理的缓存大小
            ttl=3600,         # 缓存过期时间（秒）
            name="action_sequencer_cache"
        ) if self.config.cache_results else None
        
        # 统计信息
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_planning_time': 0.0,
            'cache_hits': 0,
            'aude_re_enhanced_sequences': 0,
            'aude_re_pattern_recognitions': 0,
            'aude_re_action_derivations': 0
        }
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    @cache_result
    def generate_sequence(self, request: SequencingRequest) -> SequencingResponse:
        """
        生成动作序列
        
        Args:
            request: 动作序列请求
            
        Returns:
            SequencingResponse: 动作序列响应
        """
        start_time = time.time()
        
        try:
            # 验证请求
            if not request.validate():
                return SequencingResponse(
                    success=False,
                    action_sequence=None,
                    planning_result=None,
                    execution_time=time.time() - start_time,
                    error_message="Invalid request"
                )
            
            # 检查缓存
            if self._cache_manager is not None:
                cache_key = self._generate_cache_key(request)
                cached_result = self._cache_manager.get(cache_key)
                if cached_result is not None:
                    self.stats['cache_hits'] += 1
                    if self.config.enable_logging:
                        self.logger.info(f"Cache hit for request: {cache_key}")
                    
                    action_sequence = cached_result['action_sequence']
                    
                    # 对缓存的结果也进行AuDeRe增强（如果启用）
                    if self.config.enable_aude_re and self.aude_re:
                        try:
                            action_sequence = self._enhance_actions_with_aude_re(
                                action_sequence, request.initial_state, request.goal_state
                            )
                            self.stats['aude_re_enhanced_sequences'] += 1
                        except Exception as e:
                            if self.config.enable_logging:
                                self.logger.warning(f"Failed to enhance cached sequence with AuDeRe: {str(e)}")
                    
                    return SequencingResponse(
                        success=True,
                        action_sequence=action_sequence,
                        planning_result=cached_result['planning_result'],
                        execution_time=time.time() - start_time,
                        metadata={'from_cache': True}
                    )
            
            # 如果需要，使用AuDeRe增强请求
            enhanced_request = request
            if self.config.enable_aude_re and self.aude_re:
                try:
                    enhanced_request = self._enhance_request_with_aude_re(request)
                except Exception as e:
                    if self.config.enable_logging:
                        self.logger.warning(f"Failed to enhance request with AuDeRe: {str(e)}")
            
            # 准备状态转换
            state_transitions = None
            if enhanced_request.state_transitions:
                # 添加类型检查和错误处理，确保state_transitions是正确的类型
                try:
                    # 检查是否为列表类型
                    if isinstance(enhanced_request.state_transitions, list):
                        state_transitions = enhanced_request.state_transitions
                    else:
                        # 如果不是列表，尝试转换或者使用空列表
                        if self.config.enable_logging:
                            self.logger.warning(f"state_transitions is not a list, type: {type(enhanced_request.state_transitions).__name__}")
                        state_transitions = []
                except Exception as e:
                    if self.config.enable_logging:
                        self.logger.error(f"Error processing state_transitions: {str(e)}")
                    state_transitions = []
            
            # 执行规划
            planning_result = self.action_planner.plan(
                initial_state=enhanced_request.initial_state,
                goal_state=enhanced_request.goal_state,
                available_actions=request.available_actions,
                state_transitions=state_transitions
            )
            
            # 更新统计信息
            self.stats['total_requests'] += 1
            if planning_result.success:
                self.stats['successful_requests'] += 1
            else:
                self.stats['failed_requests'] += 1
            
            # 更新平均规划时间
            self.stats['average_planning_time'] = (
                (self.stats['average_planning_time'] * (self.stats['total_requests'] - 1) + 
                 planning_result.planning_time) / self.stats['total_requests']
            )
            
            # 验证生成的序列
            action_sequence = None
            if planning_result.success and planning_result.action_sequence:
                action_sequence = planning_result.action_sequence
                
                # 如果需要，使用AuDeRe增强动作序列
                if self.config.enable_aude_re and self.aude_re:
                    try:
                        action_sequence = self._enhance_actions_with_aude_re(
                            action_sequence, enhanced_request.initial_state, enhanced_request.goal_state
                        )
                        self.stats['aude_re_enhanced_sequences'] += 1
                    except Exception as e:
                        if self.config.enable_logging:
                            self.logger.warning(f"Failed to enhance sequence with AuDeRe: {str(e)}")
                
                if self.config.validate_sequences:
                    validation_result = self._validate_sequence(
                        action_sequence, enhanced_request.initial_state, enhanced_request.goal_state
                    )
                    if not validation_result['valid']:
                        if self.config.enable_logging:
                            self.logger.warning(f"Generated sequence failed validation: {validation_result['errors']}")
                        
                        return SequencingResponse(
                            success=False,
                            action_sequence=None,
                            planning_result=planning_result,
                            execution_time=time.time() - start_time,
                            error_message=f"Generated sequence failed validation: {validation_result['errors']}"
                        )
            
            # 缓存结果
            if self._cache_manager is not None and planning_result.success:
                cache_key = self._generate_cache_key(request)
                self._cache_manager.set(cache_key, {
                    'action_sequence': action_sequence,
                    'planning_result': planning_result,
                    'timestamp': time.time()
                })
            
            # 记录日志
            if self.config.enable_logging:
                if planning_result.success:
                    self.logger.info(f"Successfully generated action sequence with {len(action_sequence.actions) if action_sequence else 0} actions")
                else:
                    self.logger.warning(f"Failed to generate action sequence: {planning_result.metadata.get('reason', 'Unknown reason')}")
            
            return SequencingResponse(
                success=planning_result.success,
                action_sequence=action_sequence,
                planning_result=planning_result,
                execution_time=time.time() - start_time,
                metadata={'cache_key': cache_key if self._cache_manager is not None else None}
            )
            
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Error generating action sequence: {str(e)}")
            
            self.stats['total_requests'] += 1
            self.stats['failed_requests'] += 1
            
            return SequencingResponse(
                success=False,
                action_sequence=None,
                planning_result=None,
                execution_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def _generate_cache_key(self, request: SequencingRequest) -> str:
        """生成缓存键"""
        import hashlib
        
        # 创建请求的字符串表示
        request_str = json.dumps({
            'initial_state': request.initial_state,
            'goal_state': request.goal_state,
            'available_actions': [action.to_dict() for action in request.available_actions],
            'state_transitions': request.state_transitions,
            'constraints': request.constraints,
            'preferences': request.preferences
        }, sort_keys=True, default=str)
        
        # 生成哈希
        return hashlib.md5(request_str.encode()).hexdigest()
    
    def _validate_sequence(self, sequence: ActionSequence, initial_state: Dict[str, Any], 
                          goal_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证动作序列的有效性
        
        Args:
            sequence: 动作序列
            initial_state: 初始状态
            goal_state: 目标状态
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        errors = []
        warnings = []
        
        try:
            # 检查序列是否为空
            if not sequence.actions:
                errors.append("Action sequence is empty")
                return {'valid': False, 'errors': errors, 'warnings': warnings}
            
            # 模拟执行序列
            current_state = initial_state.copy()
            
            for i, action in enumerate(sequence.actions):
                # 检查前置条件
                if not action.can_execute(current_state):
                    errors.append(f"Action {i+1} ({action.name}) preconditions not satisfied")
                    continue
                
                try:
                    # 执行动作
                    current_state = action.execute(current_state)
                except Exception as e:
                    errors.append(f"Action {i+1} ({action.name}) execution failed: {str(e)}")
            
            # 检查是否达到目标状态
            goal_achieved = True
            # 添加类型检查确保 goal_state 是字典类型
            if isinstance(goal_state, dict):
                for key, goal_value in goal_state.items():
                    if current_state.get(key) != goal_value:
                        goal_achieved = False
                        warnings.append(f"Goal state not achieved for variable: {key}")
            else:
                # 如果 goal_state 不是字典，记录警告并设置目标未达成
                warnings.append(f"Warning: goal_state is not a dictionary but a {type(goal_state).__name__}")
                goal_achieved = False
            
            # 如果启用了AuDeRe，使用它进行额外的序列验证
            aude_re_validation = True
            if self.config.enable_aude_re and self.aude_re:
                try:
                    # 使用AuDeRe的动作建议功能验证序列质量
                    action_suggestions = self.aude_re.generate_action_suggestions(
                        initial_state, goal_state, sequence.actions
                    )
                    # 检查生成的序列中的动作是否在建议列表中
                    if action_suggestions:
                        suggested_action_names = {action.name for action, _ in action_suggestions}
                        for i, action in enumerate(sequence.actions):
                            if action.name not in suggested_action_names and i < len(action_suggestions):
                                warnings.append(f"Action {i+1} ({action.name}) is not in the top suggestions")
                except Exception as e:
                    if self.config.enable_logging:
                        self.logger.warning(f"AuDeRe validation failed: {str(e)}")
            
            if goal_achieved and not errors and aude_re_validation:
                return {'valid': True, 'errors': [], 'warnings': warnings}
            else:
                return {'valid': False, 'errors': errors, 'warnings': warnings}
                
        except Exception as e:
            errors.append(f"Validation failed with exception: {str(e)}")
            return {'valid': False, 'errors': errors, 'warnings': warnings}
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            'stats': self.stats.copy(),
            'config': self.config.to_dict(),
            'cache_size': len(self._cache_manager) if self._cache_manager is not None else 0
        }
        
        # 如果启用了AuDeRe，添加其统计信息
        if self.config.enable_aude_re and self.aude_re:
            try:
                aude_re_stats = self.aude_re.get_statistics()
                stats['aude_re_stats'] = aude_re_stats
            except Exception as e:
                if self.config.enable_logging:
                    self.logger.warning(f"Failed to get AuDeRe statistics: {str(e)}")
        
        return stats
    
    def clear_cache(self):
        """清空缓存"""
        if self._cache_manager is not None:
            self._cache_manager.clear()
            if self.config.enable_logging:
                self.logger.info("Cache cleared")
    
    def update_config(self, new_config: SequencingConfig):
        """更新配置"""
        self.config = new_config
        
        # 重新初始化组件
        self.action_planner = ActionPlanner(
            algorithm=self.config.planning_algorithm,
            heuristic_type=self.config.heuristic_type,
            max_depth=self.config.max_depth,
            max_time=self.config.max_time
        )
        
        # 重新初始化AuDeRe
        if self.config.enable_aude_re:
            if self.aude_re is None:
                try:
                    self.aude_re = create_aude_re(self.config.aude_re_config)
                    if self.config.enable_logging:
                        self.logger.info("AuDeRe module initialized successfully")
                except Exception as e:
                    if self.config.enable_logging:
                        self.logger.error(f"Failed to initialize AuDeRe module: {str(e)}")
            else:
                # 更新现有AuDeRe配置
                try:
                    aude_re_config = AudereConfig.from_dict(self.config.aude_re_config)
                    if hasattr(self.aude_re, 'update_config'):
                        self.aude_re.update_config(aude_re_config)
                    else:
                        # 如果AuDeRe没有update_config方法，重新创建实例
                        self.aude_re = create_aude_re(self.config.aude_re_config)
                except Exception as e:
                    if self.config.enable_logging:
                        self.logger.error(f"Failed to update AuDeRe configuration: {str(e)}")
        else:
            # 禁用AuDeRe
            self.aude_re = None
            if self.config.enable_logging:
                self.logger.info("AuDeRe module disabled")
        
        # 重新设置日志
        if self.config.enable_logging:
            self._setup_logging()
        
        # 清空缓存
        if self.config.cache_results:
            self._cache_manager = CacheManager(
                cache_size=1000,
                ttl=3600,
                name="action_sequencer_cache"
            )
        else:
            self._cache_manager = None
        
        if self.config.enable_logging:
            self.logger.info("Configuration updated")
    
    def save_results(self, response: SequencingResponse, file_path: str):
        """
        保存结果到文件
        
        Args:
            response: 响应对象
            file_path: 文件路径
        """
        try:
            result_data = response.to_dict()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            if self.config.enable_logging:
                self.logger.info(f"Results saved to {file_path}")
                
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Failed to save results: {str(e)}")
            raise
    
    def load_results(self, file_path: str) -> SequencingResponse:
        """
        从文件加载结果
        
        Args:
            file_path: 文件路径
            
        Returns:
            SequencingResponse: 响应对象
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                result_data = json.load(f)
            
            # 重建ActionSequence对象
            action_sequence = None
            if result_data.get('action_sequence'):
                sequence_data = result_data['action_sequence']
                actions = [Action(**action_data) for action_data in sequence_data['actions']]
                action_sequence = ActionSequence(
                    id=sequence_data['id'],
                    actions=actions,
                    initial_state=sequence_data['initial_state'],
                    goal_state=sequence_data['goal_state']
                )
            
            # 重建PlanningResult对象
            planning_result = None
            if result_data.get('planning_result'):
                planning_data = result_data['planning_result']
                planning_result = PlanningResult(**planning_data)
            
            response = SequencingResponse(
                success=result_data['success'],
                action_sequence=action_sequence,
                planning_result=planning_result,
                execution_time=result_data['execution_time'],
                error_message=result_data.get('error_message'),
                metadata=result_data.get('metadata')
            )
            
            if self.config.enable_logging:
                self.logger.info(f"Results loaded from {file_path}")
            
            return response
            
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Failed to load results: {str(e)}")
            raise
    
    def export_sequence_to_json(self, sequence: ActionSequence, file_path: str):
        """
        导出动作序列到JSON文件
        
        Args:
            sequence: 动作序列
            file_path: 文件路径
        """
        try:
            sequence_data = sequence.to_dict()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(sequence_data, f, indent=2, ensure_ascii=False)
            
            if self.config.enable_logging:
                self.logger.info(f"Action sequence exported to {file_path}")
                
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Failed to export sequence: {str(e)}")
            raise
    
    def import_sequence_from_json(self, file_path: str) -> ActionSequence:
        """
        从JSON文件导入动作序列
        
        Args:
            file_path: 文件路径
            
        Returns:
            ActionSequence: 动作序列
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sequence_data = json.load(f)
            
            actions = [Action(**action_data) for action_data in sequence_data['actions']]
            sequence = ActionSequence(
                id=sequence_data['id'],
                actions=actions,
                initial_state=sequence_data['initial_state'],
                goal_state=sequence_data['goal_state']
            )
            
            if self.config.enable_logging:
                self.logger.info(f"Action sequence imported from {file_path}")
            
            return sequence
            
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Failed to import sequence: {str(e)}")
            raise
    
    def _enhance_request_with_aude_re(self, request: SequencingRequest) -> SequencingRequest:
        """
        使用AuDeRe增强请求
        
        Args:
            request: 原始请求
            
        Returns:
            SequencingRequest: 增强后的请求
        """
        if not self.aude_re:
            return request
        
        try:
            # 复制原始请求以避免修改
            enhanced_actions = request.available_actions.copy()
            
            # 尝试从自然语言目标中提取更多信息
            if hasattr(request, 'goal_description') and request.goal_description:
                interpreted_goal = self.aude_re.interpret_natural_language_goal(request.goal_description)
                if interpreted_goal:
                    # 更新目标状态
                    enhanced_goal_state = request.goal_state.copy()
                    enhanced_goal_state.update(interpreted_goal)
                    request.goal_state = enhanced_goal_state
                    
                    if self.config.enable_logging:
                        self.logger.info(f"Enhanced goal state with {len(interpreted_goal)} additional conditions")
            
            # 使用AuDeRe生成动作建议，可能会发现新的动作
            action_suggestions = self.aude_re.generate_action_suggestions(
                request.initial_state, request.goal_state, enhanced_actions
            )
            
            if action_suggestions:
                self.stats['aude_re_action_derivations'] += len(action_suggestions)
                
            return request
            
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Failed to enhance request with AuDeRe: {str(e)}")
            return request
    
    def _enhance_actions_with_aude_re(self, action_sequence: ActionSequence, 
                                     initial_state: Dict[str, Any],
                                     goal_state: Dict[str, Any]) -> ActionSequence:
        """
        Enhance action sequence using AuDeRe
        
        Args:
            action_sequence: Original action sequence
            initial_state: Initial state
            goal_state: Goal state
            
        Returns:
            ActionSequence: Enhanced action sequence
        """
        if not self.aude_re:
            return action_sequence
        
        try:
            # 识别动作模式 - 对每个动作单独识别模式，而不是将整个列表转换为字符串
            for action in action_sequence.actions:
                # 为每个动作创建自然语言描述
                action_desc = f"{action.name} "
                if action.parameters:
                    if 'target' in action.parameters:
                        action_desc += f"{action.parameters['target']}"
                
                recognized_patterns = self.aude_re.recognize_action_patterns(action_desc)
                if recognized_patterns:
                    self.stats['aude_re_pattern_recognitions'] += len(recognized_patterns)
                    if self.config.enable_logging:
                        self.logger.info(f"Recognized {len(recognized_patterns)} action patterns for {action.name}")
            
            # 优化动作序列
            if hasattr(self.aude_re, 'optimize_action_sequence'):
                # 定义优化目标
                optimization_goals = {
                    'minimize_duration': True,
                    'maximize_success_rate': True
                }
                
                optimized_sequence = self.aude_re.optimize_action_sequence(
                    action_sequence, optimization_goals
                )
                
                # 更新序列ID以表示已优化
                optimized_sequence.id = f"{action_sequence.id}_aude_re_optimized"
                
                return optimized_sequence
            
            return action_sequence
            
        except Exception as e:
            if self.config.enable_logging:
                self.logger.error(f"Failed to enhance actions with AuDeRe: {str(e)}")
            return action_sequence