#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能优化模块
提供缓存机制、并行处理、资源限制和性能监控功能，
用于优化AuDeRe和LogicGuard模块的性能。
"""

import os
import sys
import time
import functools
import threading
import multiprocessing
import logging
from typing import Dict, List, Any, Optional, Callable, Union
from collections import OrderedDict
import tracemalloc

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('performance_optimization')


class LRUCache:
    """
    最近最少使用(LRU)缓存实现
    用于缓存频繁计算的结果，避免重复计算
    """
    
    def __init__(self, capacity: int = 100, expiration: int = 3600):
        """
        初始化LRU缓存
        
        Args:
            capacity: 缓存容量
            expiration: 缓存项过期时间（秒），默认1小时
        """
        self.capacity = capacity
        self.expiration = expiration
        self.cache = OrderedDict()  # 用于LRU功能
        self.timestamps = {}
        self.lock = threading.RLock()  # 可重入锁，支持并发访问
    
    def get(self, key: Any) -> Optional[Any]:
        """
        获取缓存项
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的值，如果不存在或已过期则返回None
        """
        with self.lock:
            if key not in self.cache:
                return None
            
            # 检查是否过期
            current_time = time.time()
            if current_time - self.timestamps[key] > self.expiration:
                self._remove_key(key)
                return None
            
            # 移动到最近使用
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def put(self, key: Any, value: Any) -> None:
        """
        添加缓存项
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        with self.lock:
            # 如果键已存在，先移除
            if key in self.cache:
                self._remove_key(key)
            
            # 如果缓存已满，移除最少使用的项
            elif len(self.cache) >= self.capacity:
                oldest_key = next(iter(self.cache))
                self._remove_key(oldest_key)
            
            # 添加新项
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def _remove_key(self, key: Any) -> None:
        """移除缓存项"""
        del self.cache[key]
        del self.timestamps[key]
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        with self.lock:
            return len(self.cache)


# 创建全局缓存实例
action_suggestion_cache = LRUCache(capacity=500, expiration=1800)
ltl_validation_cache = LRUCache(capacity=300, expiration=1200)
state_transition_cache = LRUCache(capacity=1000, expiration=2400)


def cache_result(cache_instance: LRUCache):
    """
    缓存函数结果的装饰器
    
    Args:
        cache_instance: 要使用的缓存实例
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            # 将不可哈希的参数转换为字符串表示
            def make_hashable(obj):
                if isinstance(obj, (str, int, float, bool, type(None))):
                    return obj
                elif isinstance(obj, (list, tuple)):
                    return tuple(make_hashable(item) for item in obj)
                elif isinstance(obj, dict):
                    return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
                else:
                    return str(obj)
            
            # 排除self参数
            key_args = args[1:] if args and hasattr(args[0], func.__name__) else args
            cache_key = (
                func.__module__, 
                func.__name__, 
                make_hashable(key_args), 
                make_hashable(sorted(kwargs.items()))
            )
            
            # 尝试从缓存获取结果
            result = cache_instance.get(cache_key)
            if result is not None:
                logger.debug(f"缓存命中: {func.__name__}")
                return result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 缓存结果（如果结果不是None）
            if result is not None:
                cache_instance.put(cache_key, result)
                logger.debug(f"缓存结果: {func.__name__}")
            
            return result
        
        return wrapper
    
    return decorator


def memoize_action_suggestions(func):
    """AuDeRe动作建议缓存装饰器"""
    return cache_result(action_suggestion_cache)(func)


def memoize_ltl_validation(func):
    """LogicGuard LTL验证缓存装饰器"""
    return cache_result(ltl_validation_cache)(func)


def memoize_state_transitions(func):
    """状态转换缓存装饰器"""
    return cache_result(state_transition_cache)(func)


class ParallelProcessor:
    """
    并行处理器
    用于将耗时操作并行执行，提高性能
    """
    
    def __init__(self, max_workers: Optional[int] = None):
        """
        初始化并行处理器
        
        Args:
            max_workers: 最大工作线程数，默认使用CPU核心数
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
        logger.info(f"并行处理器初始化，最大工作线程数: {self.max_workers}")
    
    def process_parallel(self, items: List[Any], processor_func: Callable, 
                        chunk_size: int = 10, timeout: float = 30.0) -> List[Any]:
        """
        并行处理多个项目
        
        Args:
            items: 待处理的项目列表
            processor_func: 处理单个项目的函数
            chunk_size: 每个批次的大小
            timeout: 处理超时时间（秒）
            
        Returns:
            处理结果列表
        """
        # 如果项目很少，直接串行处理
        if len(items) <= 1:
            return [processor_func(item) for item in items]
        
        results = []
        
        # 根据可用工作线程调整块大小
        adjusted_chunk_size = max(1, min(chunk_size, len(items) // self.max_workers))
        
        # 创建线程池
        with multiprocessing.Pool(processes=self.max_workers) as pool:
            try:
                # 并行处理
                results = pool.map(
                    processor_func, 
                    items, 
                    chunksize=adjusted_chunk_size
                )
            except Exception as e:
                logger.error(f"并行处理失败: {str(e)}")
                # 失败时回退到串行处理
                results = [processor_func(item) for item in items]
            
        return results


# 创建全局并行处理器实例
parallel_processor = ParallelProcessor()


def resource_limiter(max_memory_mb: int = 512):
    """
    资源限制装饰器
    监控函数的内存使用，防止过度消耗资源
    
    Args:
        max_memory_mb: 最大允许内存使用量（MB）
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 开始监控内存
            tracemalloc.start()
            
            try:
                # 执行函数
                result = func(*args, **kwargs)
                
                # 检查内存使用
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                current_mb = current / 1024 / 1024
                peak_mb = peak / 1024 / 1024
                
                logger.debug(
                    f"函数 {func.__name__} 内存使用: "
                    f"当前={current_mb:.2f}MB, 峰值={peak_mb:.2f}MB"
                )
                
                # 如果超过内存限制，发出警告
                if peak_mb > max_memory_mb:
                    logger.warning(
                        f"函数 {func.__name__} 内存使用超过限制: "
                        f"{peak_mb:.2f}MB > {max_memory_mb}MB"
                    )
                
                return result
                
            except Exception as e:
                tracemalloc.stop()
                logger.error(f"资源限制装饰器捕获异常: {str(e)}")
                raise
        
        return wrapper
    
    return decorator


class PerformanceMonitor:
    """
    性能监控器
    用于跟踪和记录函数执行时间和资源使用情况
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """单例模式实现"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.metrics = {}
                cls._instance.enable_metrics = True
        return cls._instance
    
    def enable(self):
        """启用性能监控"""
        self.enable_metrics = True
    
    def disable(self):
        """禁用性能监控"""
        self.enable_metrics = False
    
    def reset_metrics(self):
        """重置所有性能指标"""
        with self._lock:
            self.metrics.clear()
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        with self._lock:
            return self.metrics.copy()
    
    def monitor(self, category: str = "default"):
        """
        性能监控装饰器
        
        Args:
            category: 监控类别，用于分类统计
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enable_metrics:
                    return func(*args, **kwargs)
                
                # 初始化该函数的指标
                func_key = f"{category}.{func.__module__}.{func.__name__}"
                with self._lock:
                    if func_key not in self.metrics:
                        self.metrics[func_key] = {
                            'calls': 0,
                            'total_time': 0.0,
                            'min_time': float('inf'),
                            'max_time': 0.0,
                            'avg_time': 0.0
                        }
                
                # 开始计时
                start_time = time.time()
                
                try:
                    # 执行函数
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # 结束计时
                    elapsed_time = time.time() - start_time
                    
                    # 更新指标
                    with self._lock:
                        metrics = self.metrics[func_key]
                        metrics['calls'] += 1
                        metrics['total_time'] += elapsed_time
                        metrics['min_time'] = min(metrics['min_time'], elapsed_time)
                        metrics['max_time'] = max(metrics['max_time'], elapsed_time)
                        metrics['avg_time'] = metrics['total_time'] / metrics['calls']
                    
                    # 记录慢函数
                    if elapsed_time > 1.0:  # 超过1秒的函数被认为是慢函数
                        logger.warning(
                            f"慢函数检测: {func_key} 执行时间={elapsed_time:.4f}秒"
                        )
            
            return wrapper
        
        return decorator


# 创建全局性能监控实例
performance_monitor = PerformanceMonitor()

# 便捷装饰器
def monitor_performance(category: str = "default"):
    """性能监控装饰器"""
    return performance_monitor.monitor(category)


def optimize_memory_usage(obj):
    """
    优化对象的内存使用
    对于大型数据结构，提供一些优化建议
    
    Args:
        obj: 要优化的对象
        
    Returns:
        优化后的对象或优化建议
    """
    # 对于字典列表，尝试转换为元组列表（更节省内存）
    if isinstance(obj, list) and all(isinstance(item, dict) for item in obj):
        if len(obj) > 1000:  # 只对大型列表进行优化
            logger.info("优化大型字典列表内存使用")
            # 假设所有字典有相同的键
            if obj:
                keys = tuple(obj[0].keys())
                # 转换为元组列表
                return [(tuple(item.get(k) for k in keys)) for item in obj], keys
    
    # 对于大型字符串，检查是否可以压缩
    elif isinstance(obj, str) and len(obj) > 10000:
        logger.info("检测到大型字符串，建议考虑压缩")
    
    return obj


def adaptive_computation(threshold: int):
    """
    自适应计算装饰器
    根据输入数据大小自动选择计算策略
    
    Args:
        threshold: 小型数据集的阈值
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 判断输入规模
            data_size = 0
            
            # 检查参数中的列表/字典大小
            for arg in args:
                if isinstance(arg, (list, tuple)):
                    data_size += len(arg)
                elif isinstance(arg, dict):
                    data_size += len(arg)
            
            for arg in kwargs.values():
                if isinstance(arg, (list, tuple)):
                    data_size += len(arg)
                elif isinstance(arg, dict):
                    data_size += len(arg)
            
            logger.debug(f"函数 {func.__name__} 输入数据大小: {data_size}")
            
            # 根据数据大小选择处理策略
            if data_size < threshold:
                # 小型数据，直接执行
                return func(*args, **kwargs)
            else:
                # 大型数据，考虑分批处理
                logger.info(f"检测到大型数据，函数 {func.__name__} 可能需要优化")
                return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def generate_performance_report(output_file: str = "performance_report.json"):
    """
    生成性能报告
    
    Args:
        output_file: 报告输出文件路径
    """
    import json
    
    metrics = performance_monitor.get_metrics()
    
    # 按平均执行时间排序
    sorted_metrics = sorted(
        metrics.items(), 
        key=lambda x: x[1]['avg_time'], 
        reverse=True
    )
    
    report = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'top_10_slowest_functions': [],
        'summary': {
            'total_functions': len(metrics),
            'total_calls': sum(m['calls'] for m in metrics.values()),
            'total_execution_time': sum(m['total_time'] for m in metrics.values())
        },
        'detailed_metrics': metrics
    }
    
    # 添加最慢的10个函数
    for func_key, func_metrics in sorted_metrics[:10]:
        report['top_10_slowest_functions'].append({
            'function': func_key,
            'calls': func_metrics['calls'],
            'avg_time': func_metrics['avg_time'],
            'max_time': func_metrics['max_time'],
            'total_time': func_metrics['total_time']
        })
    
    # 输出报告
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"性能报告已保存到: {output_file}")
        return report
    except Exception as e:
        logger.error(f"保存性能报告失败: {str(e)}")
        return None


# 优化配置类
class OptimizationConfig:
    """性能优化配置"""
    
    def __init__(self):
        # 默认配置
        self.config = {
            'enable_caching': True,
            'enable_parallel_processing': True,
            'enable_resource_limiting': False,
            'enable_performance_monitoring': True,
            'max_workers': multiprocessing.cpu_count(),
            'max_memory_mb': 1024,
            'cache_capacity': {
                'action_suggestions': 500,
                'ltl_validation': 300,
                'state_transitions': 1000
            },
            'cache_expiration': {
                'action_suggestions': 1800,
                'ltl_validation': 1200,
                'state_transitions': 2400
            }
        }
    
    def update(self, new_config: Dict[str, Any]):
        """更新配置"""
        def recursive_update(d, u):
            for k, v in u.items():
                if k in d and isinstance(d[k], dict) and isinstance(v, dict):
                    recursive_update(d[k], v)
                else:
                    d[k] = v
        
        recursive_update(self.config, new_config)
        self._apply_config()
    
    def _apply_config(self):
        """应用配置"""
        # 应用缓存配置
        if self.config['enable_caching']:
            global action_suggestion_cache, ltl_validation_cache, state_transition_cache
            action_suggestion_cache = LRUCache(
                capacity=self.config['cache_capacity']['action_suggestions'],
                expiration=self.config['cache_expiration']['action_suggestions']
            )
            ltl_validation_cache = LRUCache(
                capacity=self.config['cache_capacity']['ltl_validation'],
                expiration=self.config['cache_expiration']['ltl_validation']
            )
            state_transition_cache = LRUCache(
                capacity=self.config['cache_capacity']['state_transitions'],
                expiration=self.config['cache_expiration']['state_transitions']
            )
        
        # 应用并行处理配置
        if self.config['enable_parallel_processing']:
            global parallel_processor
            parallel_processor = ParallelProcessor(
                max_workers=self.config['max_workers']
            )
        
        # 应用性能监控配置
        if self.config['enable_performance_monitoring']:
            performance_monitor.enable()
        else:
            performance_monitor.disable()
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config.copy()


# 创建全局优化配置实例
optimization_config = OptimizationConfig()


def apply_optimizations(module_obj: Any, category: str = "default"):
    """
    为模块应用所有优化
    
    Args:
        module_obj: 要优化的模块对象
        category: 性能监控类别
    """
    import inspect
    
    config = optimization_config.get_config()
    
    # 获取模块中所有可调用函数
    for name, func in inspect.getmembers(module_obj, inspect.isfunction):
        # 跳过私有函数
        if name.startswith('_'):
            continue
        
        # 应用性能监控
        if config['enable_performance_monitoring']:
            setattr(module_obj, name, monitor_performance(category)(func))
        
        # 应用缓存（根据函数名判断）
        if config['enable_caching']:
            if 'suggest' in name.lower():
                setattr(module_obj, name, memoize_action_suggestions(func))
            elif 'validate' in name.lower():
                setattr(module_obj, name, memoize_ltl_validation(func))
            elif 'transition' in name.lower():
                setattr(module_obj, name, memoize_state_transitions(func))
        
        # 应用资源限制
        if config['enable_resource_limiting']:
            setattr(module_obj, name, resource_limiter(config['max_memory_mb'])(func))
    
    logger.info(f"已为模块 {module_obj.__name__} 应用优化")


# 主函数示例
if __name__ == "__main__":
    # 演示性能优化功能
    print("性能优化模块演示")
    
    # 启用性能监控
    performance_monitor.enable()
    
    # 示例函数
    @monitor_performance("example")
    def example_function(n: int) -> int:
        """示例函数"""
        time.sleep(0.1)
        return sum(i for i in range(n))
    
    # 运行示例
    print("运行示例函数...")
    for i in range(3):
        example_function(1000000)
    
    # 生成性能报告
    report = generate_performance_report()
    if report:
        print(f"\n总执行时间: {report['summary']['total_execution_time']:.2f}秒")
        print("最慢函数:")
        for func in report['top_10_slowest_functions']:
            print(f"  - {func['function']}: 平均 {func['avg_time']*1000:.2f}ms")