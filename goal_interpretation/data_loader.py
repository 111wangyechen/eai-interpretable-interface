#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载器
负责加载和处理parquet格式的真实数据集
"""

import pandas as pd
import json
from typing import Dict, List, Optional, Union, Tuple
import os


class ParquetDataLoader:
    """
    Parquet数据加载器类
    负责从parquet文件中加载和处理数据
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化数据加载器
        
        Args:
            data_dir: 数据文件所在目录，默认为None（会自动搜索）
        """
        # 如果未指定数据目录，尝试多个可能的路径
        self.data_dir = self._find_data_directory(data_dir)
        self.behavior_file = os.path.join(self.data_dir, "behavior-00000-of-00001.parquet")
        self.virtualhome_file = os.path.join(self.data_dir, "virtualhome-00000-of-00001.parquet")
        self.behavior_data = None
        self.virtualhome_data = None
        
        # 验证文件是否存在
        self._validate_files()
    
    def _find_data_directory(self, data_dir: str = None) -> str:
        """
        自动查找包含parquet文件的数据目录
        
        Args:
            data_dir: 用户提供的数据目录
            
        Returns:
            str: 有效的数据目录路径
        """
        if data_dir and os.path.exists(data_dir):
            return data_dir
            
        # 尝试多个可能的路径
        possible_paths = [
            os.getcwd(),                           # 当前目录
            os.path.dirname(os.getcwd()),          # 上级目录
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),  # 模块的上级目录
            "../..",                               # 上上级目录
            "~",                                   # 用户主目录
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data"),  # 项目的data目录
            os.path.abspath("../data")            # 相对路径指向data目录
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expanduser(path)  # 展开~用户主目录
            if os.path.exists(os.path.join(expanded_path, "behavior-00000-of-00001.parquet")):
                print(f"自动定位到数据目录: {expanded_path}")
                return expanded_path
                
        # 如果都找不到，使用当前目录作为默认值
        print("警告: 未找到包含parquet文件的目录，使用当前目录")
        return os.getcwd()
        
    def _validate_files(self):
        """
        验证数据文件是否存在
        """
        behavior_exists = os.path.exists(self.behavior_file)
        virtualhome_exists = os.path.exists(self.virtualhome_file)
        
        if not behavior_exists:
            print(f"警告: 未找到behavior文件: {self.behavior_file}")
        if not virtualhome_exists:
            print(f"警告: 未找到virtualhome文件: {self.virtualhome_file}")
            
        if not behavior_exists and not virtualhome_exists:
            print("警告: 未找到任何数据文件，请确保parquet文件在正确的位置")
        
    def load_data(self, dataset: str = "all") -> None:
        """
        加载指定数据集
        
        Args:
            dataset: 数据集名称，可以是'behavior', 'virtualhome'或'all'
        """
        try:
            if dataset in ['behavior', 'all'] and os.path.exists(self.behavior_file):
                self.behavior_data = pd.read_parquet(self.behavior_file)
                print(f"成功加载Behavior数据集，共{len(self.behavior_data)}条记录")
            elif dataset in ['behavior', 'all']:
                print(f"跳过加载Behavior数据集: 文件不存在 {self.behavior_file}")
            
            if dataset in ['virtualhome', 'all'] and os.path.exists(self.virtualhome_file):
                self.virtualhome_data = pd.read_parquet(self.virtualhome_file)
                print(f"成功加载Virtualhome数据集，共{len(self.virtualhome_data)}条记录")
            elif dataset in ['virtualhome', 'all']:
                print(f"跳过加载Virtualhome数据集: 文件不存在 {self.virtualhome_file}")
                
            # 验证至少加载了一个数据集
            if ((dataset == 'behavior' and self.behavior_data is None) or
                (dataset == 'virtualhome' and self.virtualhome_data is None) or
                (dataset == 'all' and self.behavior_data is None and self.virtualhome_data is None)):
                print("警告: 没有成功加载任何数据集")
                
        except Exception as e:
            print(f"加载数据失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_sample_data(self, dataset: str = "behavior", sample_size: int = 10) -> pd.DataFrame:
        """
        获取数据集的样本
        
        Args:
            dataset: 数据集名称
            sample_size: 样本大小
            
        Returns:
            样本数据DataFrame
        """
        if dataset == "behavior":
            if self.behavior_data is None:
                self.load_data("behavior")
            return self.behavior_data.sample(min(sample_size, len(self.behavior_data)))
        elif dataset == "virtualhome":
            if self.virtualhome_data is None:
                self.load_data("virtualhome")
            return self.virtualhome_data.sample(min(sample_size, len(self.virtualhome_data)))
        else:
            raise ValueError(f"未知的数据集: {dataset}")
    
    def get_task_data(self, task_name: str, dataset: str = "all") -> List[Dict]:
        """
        根据任务名称获取相关数据
        
        Args:
            task_name: 任务名称
            dataset: 数据集名称
            
        Returns:
            任务相关数据列表
        """
        results = []
        
        if dataset in ['behavior', 'all'] and self.behavior_data is not None:
            behavior_tasks = self.behavior_data[self.behavior_data['task_name'].str.contains(task_name, case=False, na=False)]
            for _, row in behavior_tasks.iterrows():
                results.append({
                    'dataset': 'behavior',
                    'scene_id': row['scene_id'],
                    'task_id': row['task_id'],
                    'task_name': row['task_name'],
                    'description': row['natural_language_description'],
                    'original_goal': row['original_goal'],
                    'tl_goal': row['tl_goal'],
                    'action_trajectory': row['action_trajectory']
                })
        
        if dataset in ['virtualhome', 'all'] and self.virtualhome_data is not None:
            virtualhome_tasks = self.virtualhome_data[self.virtualhome_data['task_name'].str.contains(task_name, case=False, na=False)]
            for _, row in virtualhome_tasks.iterrows():
                results.append({
                    'dataset': 'virtualhome',
                    'scene_id': row['scene_id'],
                    'task_id': row['task_id'],
                    'task_name': row['task_name'],
                    'description': row['natural_language_description'],
                    'original_goal': row['original_goal'],
                    'tl_goal': row['tl_goal'],
                    'action_trajectory': row['action_trajectory']
                })
        
        return results
    
    def get_nl_tl_pairs(self, dataset: str = "all", limit: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        获取自然语言描述和TL目标的配对
        
        Args:
            dataset: 数据集名称
            limit: 返回的最大配对数量
            
        Returns:
            (自然语言描述, TL目标)配对列表
        """
        pairs = []
        
        if dataset in ['behavior', 'all'] and self.behavior_data is not None:
            for _, row in self.behavior_data.iterrows():
                pairs.append((row['natural_language_description'], row['tl_goal']))
                if limit and len(pairs) >= limit:
                    return pairs
        
        if dataset in ['virtualhome', 'all'] and self.virtualhome_data is not None:
            for _, row in self.virtualhome_data.iterrows():
                pairs.append((row['natural_language_description'], row['tl_goal']))
                if limit and len(pairs) >= limit:
                    return pairs
        
        return pairs
    
    def preprocess_tl_goal(self, tl_goal: str) -> str:
        """
        预处理TL目标，转换为LTL格式
        
        Args:
            tl_goal: 原始TL目标字符串
            
        Returns:
            处理后的LTL格式字符串
        """
        # 这里可以添加更复杂的预处理逻辑
        # 例如，将特定领域的操作符转换为标准LTL操作符
        processed = tl_goal.strip()
        
        # 替换一些常见的非标准符号
        replacements = {
            '□': 'G',  # 全局操作符
            '◇': 'F',  # 最终操作符
            '→': '->'  # 蕴含操作符
        }
        
        for old, new in replacements.items():
            processed = processed.replace(old, new)
        
        return processed
    
    def export_to_jsonl(self, output_file: str, dataset: str = "all") -> None:
        """
        将数据导出为JSONL格式，便于训练和评估
        
        Args:
            output_file: 输出文件路径
            dataset: 数据集名称
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            if dataset in ['behavior', 'all'] and self.behavior_data is not None:
                for _, row in self.behavior_data.iterrows():
                    data = {
                        'dataset': 'behavior',
                        'scene_id': row['scene_id'],
                        'task_id': row['task_id'],
                        'task_name': row['task_name'],
                        'natural_language': row['natural_language_description'],
                        'tl_goal': self.preprocess_tl_goal(row['tl_goal']),
                        'original_goal': row['original_goal'],
                        'action_trajectory': row['action_trajectory']
                    }
                    f.write(json.dumps(data, ensure_ascii=False) + '\n')
            
            if dataset in ['virtualhome', 'all'] and self.virtualhome_data is not None:
                for _, row in self.virtualhome_data.iterrows():
                    data = {
                        'dataset': 'virtualhome',
                        'scene_id': row['scene_id'],
                        'task_id': row['task_id'],
                        'task_name': row['task_name'],
                        'natural_language': row['natural_language_description'],
                        'tl_goal': self.preprocess_tl_goal(row['tl_goal']),
                        'original_goal': row['original_goal'],
                        'action_trajectory': row['action_trajectory']
                    }
                    f.write(json.dumps(data, ensure_ascii=False) + '\n')
        
        print(f"数据已导出到 {output_file}")


def main():
    """
    示例使用
    """
    loader = ParquetDataLoader()
    loader.load_data()
    
    # 获取样本数据
    behavior_sample = loader.get_sample_data("behavior", 5)
    print("\nBehavior数据集样本:")
    print(behavior_sample[['task_name', 'natural_language_description', 'tl_goal']])
    
    virtualhome_sample = loader.get_sample_data("virtualhome", 5)
    print("\nVirtualhome数据集样本:")
    print(virtualhome_sample[['task_name', 'natural_language_description', 'tl_goal']])
    
    # 导出数据为JSONL格式
    loader.export_to_jsonl("goal_interpretation/dataset.jsonl")


if __name__ == "__main__":
    main()