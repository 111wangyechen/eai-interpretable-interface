#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载器模块
用于加载和处理virtualhome和behavior数据集
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import pandas as pd
import json
import logging
from pathlib import Path
import numpy as np
from collections import defaultdict

from .action_data import Action, ActionType, ActionStatus
from .state_manager import StateTransition


@dataclass
class DatasetConfig:
    """数据集配置类"""
    virtualhome_path: str
    behavior_path: str
    max_samples: int = 10
    sample_randomly: bool = True
    cache_data: bool = True
    validate_data: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'virtualhome_path': self.virtualhome_path,
            'behavior_path': self.behavior_path,
            'max_samples': self.max_samples,
            'sample_randomly': self.sample_randomly,
            'cache_data': self.cache_data,
            'validate_data': self.validate_data
        }


@dataclass
class VirtualHomeRecord:
    """VirtualHome数据记录"""
    task_id: str
    task_description: str
    actions: List[Dict[str, Any]]
    initial_state: Dict[str, Any]
    goal_state: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'task_id': self.task_id,
            'task_description': self.task_description,
            'actions': self.actions,
            'initial_state': self.initial_state,
            'goal_state': self.goal_state,
            'metadata': self.metadata
        }


@dataclass
class BehaviorRecord:
    """Behavior数据记录"""
    behavior_id: str
    behavior_type: str
    context: Dict[str, Any]
    actions: List[Dict[str, Any]]
    outcomes: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'behavior_id': self.behavior_id,
            'behavior_type': self.behavior_type,
            'context': self.context,
            'actions': self.actions,
            'outcomes': self.outcomes,
            'metadata': self.metadata
        }


class DataLoader:
    """数据加载器类"""
    
    def __init__(self, config: DatasetConfig):
        """
        初始化数据加载器
        
        Args:
            config: 数据集配置
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 数据缓存
        self._virtualhome_cache = None
        self._behavior_cache = None
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
    
    def load_virtualhome_data(self, num_samples: Optional[int] = None) -> List[VirtualHomeRecord]:
        """
        加载VirtualHome数据集
        
        Args:
            num_samples: 要加载的样本数量，如果为None则使用配置中的值
            
        Returns:
            List[VirtualHomeRecord]: VirtualHome记录列表
        """
        try:
            num_samples = num_samples or self.config.max_samples
            
            # 检查缓存
            if self.config.cache_data and self._virtualhome_cache is not None:
                self.logger.info("Returning cached VirtualHome data")
                return self._virtualhome_cache[:num_samples]
            
            # 检查文件是否存在
            if not Path(self.config.virtualhome_path).exists():
                raise FileNotFoundError(f"VirtualHome data file not found: {self.config.virtualhome_path}")
            
            # 加载Parquet文件
            self.logger.info(f"Loading VirtualHome data from {self.config.virtualhome_path}")
            df = pd.read_parquet(self.config.virtualhome_path)
            
            # 采样数据
            if len(df) > num_samples:
                if self.config.sample_randomly:
                    df = df.sample(n=num_samples, random_state=42)
                else:
                    df = df.head(num_samples)
            
            # 转换为VirtualHomeRecord对象
            records = []
            for idx, row in df.iterrows():
                try:
                    record = self._parse_virtualhome_row(row)
                    if self.config.validate_data and self._validate_virtualhome_record(record):
                        records.append(record)
                    elif not self.config.validate_data:
                        records.append(record)
                except Exception as e:
                    self.logger.warning(f"Failed to parse VirtualHome row {idx}: {str(e)}")
                    continue
            
            # 缓存数据
            if self.config.cache_data:
                self._virtualhome_cache = records
            
            self.logger.info(f"Successfully loaded {len(records)} VirtualHome records")
            return records
            
        except Exception as e:
            self.logger.error(f"Failed to load VirtualHome data: {str(e)}")
            raise
    
    def load_behavior_data(self, num_samples: Optional[int] = None) -> List[BehaviorRecord]:
        """
        加载Behavior数据集
        
        Args:
            num_samples: 要加载的样本数量，如果为None则使用配置中的值
            
        Returns:
            List[BehaviorRecord]: Behavior记录列表
        """
        try:
            num_samples = num_samples or self.config.max_samples
            
            # 检查缓存
            if self.config.cache_data and self._behavior_cache is not None:
                self.logger.info("Returning cached Behavior data")
                return self._behavior_cache[:num_samples]
            
            # 检查文件是否存在
            if not Path(self.config.behavior_path).exists():
                raise FileNotFoundError(f"Behavior data file not found: {self.config.behavior_path}")
            
            # 加载Parquet文件
            self.logger.info(f"Loading Behavior data from {self.config.behavior_path}")
            df = pd.read_parquet(self.config.behavior_path)
            
            # 采样数据
            if len(df) > num_samples:
                if self.config.sample_randomly:
                    df = df.sample(n=num_samples, random_state=42)
                else:
                    df = df.head(num_samples)
            
            # 转换为BehaviorRecord对象
            records = []
            for idx, row in df.iterrows():
                try:
                    record = self._parse_behavior_row(row)
                    if self.config.validate_data and self._validate_behavior_record(record):
                        records.append(record)
                    elif not self.config.validate_data:
                        records.append(record)
                except Exception as e:
                    self.logger.warning(f"Failed to parse Behavior row {idx}: {str(e)}")
                    continue
            
            # 缓存数据
            if self.config.cache_data:
                self._behavior_cache = records
            
            self.logger.info(f"Successfully loaded {len(records)} Behavior records")
            return records
            
        except Exception as e:
            self.logger.error(f"Failed to load Behavior data: {str(e)}")
            raise
    
    def _parse_virtualhome_row(self, row: pd.Series) -> VirtualHomeRecord:
        """
        解析VirtualHome数据行
        
        Args:
            row: pandas Series对象
            
        Returns:
            VirtualHomeRecord: 解析后的记录
        """
        # 提取基本信息
        task_id = str(row.get('task_id', f'unknown_{row.name}'))
        task_description = str(row.get('task_description', ''))
        
        # 解析动作列表
        actions = []
        if 'actions' in row and pd.notna(row['actions']):
            try:
                if isinstance(row['actions'], str):
                    actions_data = json.loads(row['actions'])
                else:
                    actions_data = row['actions']
                
                if isinstance(actions_data, list):
                    actions = actions_data
                elif isinstance(actions_data, dict):
                    actions = [actions_data]
            except json.JSONDecodeError:
                actions = []
        
        # 解析状态信息
        initial_state = {}
        if 'initial_state' in row and pd.notna(row['initial_state']):
            try:
                if isinstance(row['initial_state'], str):
                    initial_state = json.loads(row['initial_state'])
                else:
                    initial_state = row['initial_state']
            except json.JSONDecodeError:
                initial_state = {}
        
        goal_state = {}
        if 'goal_state' in row and pd.notna(row['goal_state']):
            try:
                if isinstance(row['goal_state'], str):
                    goal_state = json.loads(row['goal_state'])
                else:
                    goal_state = row['goal_state']
            except json.JSONDecodeError:
                goal_state = {}
        
        # 提取元数据
        metadata = {}
        for col in row.index:
            if col not in ['task_id', 'task_description', 'actions', 'initial_state', 'goal_state']:
                value = row[col]
                if pd.notna(value):
                    metadata[col] = value
        
        return VirtualHomeRecord(
            task_id=task_id,
            task_description=task_description,
            actions=actions,
            initial_state=initial_state,
            goal_state=goal_state,
            metadata=metadata
        )
    
    def _parse_behavior_row(self, row: pd.Series) -> BehaviorRecord:
        """
        解析Behavior数据行
        
        Args:
            row: pandas Series对象
            
        Returns:
            BehaviorRecord: 解析后的记录
        """
        # 提取基本信息
        behavior_id = str(row.get('behavior_id', f'unknown_{row.name}'))
        behavior_type = str(row.get('behavior_type', ''))
        
        # 解析上下文信息
        context = {}
        if 'context' in row and pd.notna(row['context']):
            try:
                if isinstance(row['context'], str):
                    context = json.loads(row['context'])
                else:
                    context = row['context']
            except json.JSONDecodeError:
                context = {}
        
        # 解析动作列表
        actions = []
        if 'actions' in row and pd.notna(row['actions']):
            try:
                if isinstance(row['actions'], str):
                    actions_data = json.loads(row['actions'])
                else:
                    actions_data = row['actions']
                
                if isinstance(actions_data, list):
                    actions = actions_data
                elif isinstance(actions_data, dict):
                    actions = [actions_data]
            except json.JSONDecodeError:
                actions = []
        
        # 解析结果信息
        outcomes = {}
        if 'outcomes' in row and pd.notna(row['outcomes']):
            try:
                if isinstance(row['outcomes'], str):
                    outcomes = json.loads(row['outcomes'])
                else:
                    outcomes = row['outcomes']
            except json.JSONDecodeError:
                outcomes = {}
        
        # 提取元数据
        metadata = {}
        for col in row.index:
            if col not in ['behavior_id', 'behavior_type', 'context', 'actions', 'outcomes']:
                value = row[col]
                if pd.notna(value):
                    metadata[col] = value
        
        return BehaviorRecord(
            behavior_id=behavior_id,
            behavior_type=behavior_type,
            context=context,
            actions=actions,
            outcomes=outcomes,
            metadata=metadata
        )
    
    def _validate_virtualhome_record(self, record: VirtualHomeRecord) -> bool:
        """
        验证VirtualHome记录的有效性
        
        Args:
            record: VirtualHome记录
            
        Returns:
            bool: 是否有效
        """
        if not record.task_id:
            return False
        
        if not record.actions:
            return False
        
        if not isinstance(record.actions, list):
            return False
        
        return True
    
    def _validate_behavior_record(self, record: BehaviorRecord) -> bool:
        """
        验证Behavior记录的有效性
        
        Args:
            record: Behavior记录
            
        Returns:
            bool: 是否有效
        """
        if not record.behavior_id:
            return False
        
        if not record.behavior_type:
            return False
        
        if not record.actions:
            return False
        
        if not isinstance(record.actions, list):
            return False
        
        return True
    
    def convert_to_actions(self, action_dicts: List[Dict[str, Any]]) -> List[Action]:
        """
        将动作字典转换为Action对象
        
        Args:
            action_dicts: 动作字典列表
            
        Returns:
            List[Action]: Action对象列表
        """
        actions = []
        
        for i, action_dict in enumerate(action_dicts):
            try:
                # 提取动作信息
                action_id = action_dict.get('id', f'action_{i}')
                action_name = action_dict.get('name', f'action_{i}')
                
                # 映射动作类型
                action_type_str = action_dict.get('type', 'navigation')
                action_type = self._map_action_type(action_type_str)
                
                # 提取参数
                parameters = action_dict.get('parameters', {})
                
                # 提取前置条件和效果
                preconditions = action_dict.get('preconditions', [])
                effects = action_dict.get('effects', [])
                
                # 提取其他属性
                duration = float(action_dict.get('duration', 1.0))
                success_probability = float(action_dict.get('success_probability', 1.0))
                
                action = Action(
                    id=action_id,
                    name=action_name,
                    action_type=action_type,
                    parameters=parameters,
                    preconditions=preconditions,
                    effects=effects,
                    duration=duration,
                    success_probability=success_probability
                )
                
                actions.append(action)
                
            except Exception as e:
                self.logger.warning(f"Failed to convert action {i}: {str(e)}")
                continue
        
        return actions
    
    def _map_action_type(self, type_str: str) -> ActionType:
        """
        映射动作类型字符串到枚举
        
        Args:
            type_str: 动作类型字符串
            
        Returns:
            ActionType: 动作类型枚举
        """
        type_mapping = {
            'navigation': ActionType.NAVIGATION,
            'manipulation': ActionType.MANIPULATION,
            'perception': ActionType.PERCEPTION,
            'communication': ActionType.COMMUNICATION,
            'observation': ActionType.OBSERVATION,
            'wait': ActionType.WAIT,
            'conditional': ActionType.CONDITIONAL
        }
        
        return type_mapping.get(type_str.lower(), ActionType.NAVIGATION)
    
    def create_state_transitions(self, actions: List[Action], 
                                 initial_state: Dict[str, Any]) -> List[StateTransition]:
        """
        创建状态转换列表
        
        Args:
            actions: 动作列表
            initial_state: 初始状态
            
        Returns:
            List[StateTransition]: 状态转换列表
        """
        transitions = []
        current_state = initial_state.copy()
        
        for i, action in enumerate(actions):
            try:
                # 模拟执行动作
                next_state = action.execute(current_state)
                
                # 创建状态转换
                transition = StateTransition(
                    id=f'transition_{i}',
                    from_state=current_state.copy(),
                    to_state=next_state.copy(),
                    action_id=action.id,
                    conditions=action.preconditions,
                    effects=action.effects
                )
                
                transitions.append(transition)
                current_state = next_state
                
            except Exception as e:
                self.logger.warning(f"Failed to create transition for action {action.id}: {str(e)}")
                continue
        
        return transitions
    
    def get_data_statistics(self) -> Dict[str, Any]:
        """
        获取数据统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        stats = {}
        
        try:
            # VirtualHome统计
            if self._virtualhome_cache is not None:
                vh_records = self._virtualhome_cache
                stats['virtualhome'] = {
                    'total_records': len(vh_records),
                    'avg_actions_per_record': np.mean([len(r.actions) for r in vh_records]),
                    'unique_task_types': len(set(r.task_description for r in vh_records)),
                    'records_with_initial_state': len([r for r in vh_records if r.initial_state]),
                    'records_with_goal_state': len([r for r in vh_records if r.goal_state])
                }
            
            # Behavior统计
            if self._behavior_cache is not None:
                bh_records = self._behavior_cache
                stats['behavior'] = {
                    'total_records': len(bh_records),
                    'avg_actions_per_record': np.mean([len(r.actions) for r in bh_records]),
                    'unique_behavior_types': len(set(r.behavior_type for r in bh_records)),
                    'records_with_context': len([r for r in bh_records if r.context]),
                    'records_with_outcomes': len([r for r in bh_records if r.outcomes])
                }
            
        except Exception as e:
            self.logger.error(f"Failed to compute statistics: {str(e)}")
        
        return stats
    
    def clear_cache(self):
        """清空数据缓存"""
        self._virtualhome_cache = None
        self._behavior_cache = None
        self.logger.info("Data cache cleared")
    
    def save_processed_data(self, output_dir: str):
        """
        保存处理后的数据
        
        Args:
            output_dir: 输出目录
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 保存VirtualHome数据
            if self._virtualhome_cache is not None:
                vh_data = [record.to_dict() for record in self._virtualhome_cache]
                with open(output_path / 'virtualhome_processed.json', 'w', encoding='utf-8') as f:
                    json.dump(vh_data, f, indent=2, ensure_ascii=False)
            
            # 保存Behavior数据
            if self._behavior_cache is not None:
                bh_data = [record.to_dict() for record in self._behavior_cache]
                with open(output_path / 'behavior_processed.json', 'w', encoding='utf-8') as f:
                    json.dump(bh_data, f, indent=2, ensure_ascii=False)
            
            # 保存统计信息
            stats = self.get_data_statistics()
            with open(output_path / 'data_statistics.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Processed data saved to {output_dir}")
            
        except Exception as e:
            self.logger.error(f"Failed to save processed data: {str(e)}")
            raise