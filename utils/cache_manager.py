"""缓存管理器 - 用于优化系统性能的高效缓存实现"""

import time
import hashlib
from typing import Any, Dict, Optional, Callable, Tuple
from collections import OrderedDict


class CacheEntry:
    """缓存条目，包含值、创建时间、最后访问时间和过期时间"""
    
    def __init__(self, value: Any, ttl: Optional[int] = None):
        self.value = value
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.ttl = ttl  # 过期时间（秒）
    
    def is_expired(self) -> bool:
        """检查缓存是否过期"""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    def access(self) -> Any:
        """访问缓存值并更新最后访问时间"""
        self.last_accessed = time.time()
        return self.value
    
    def get_age(self) -> float:
        """获取缓存年龄（秒）"""
        return time.time() - self.created_at


class LRUCache:
    """LRU (Least Recently Used) 缓存实现，支持最大容量和过期时间"""
    
    def __init__(self, max_size: int = 100, default_ttl: Optional[int] = None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def _generate_key(self, *args, **kwargs) -> str:
        """生成缓存键"""
        key_parts = [str(arg) for arg in args]
        key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        key_str = ":".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # 检查是否过期
        if entry.is_expired():
            self.remove(key)
            self.misses += 1
            return None
        
        # 更新访问时间和位置
        value = entry.access()
        self.cache.move_to_end(key)
        self.hits += 1
        return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """设置缓存值"""
        # 如果缓存已满，移除最久未使用的项
        if len(self.cache) >= self.max_size and key not in self.cache:
            self.cache.popitem(last=False)
            self.evictions += 1
        
        # 使用指定的TTL或默认TTL
        effective_ttl = ttl if ttl is not None else self.default_ttl
        self.cache[key] = CacheEntry(value, effective_ttl)
        self.cache.move_to_end(key)
    
    def remove(self, key: str) -> None:
        """移除缓存项"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total) * 100 if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'evictions': self.evictions,
            'size': len(self.cache),
            'max_size': self.max_size,
            'default_ttl': self.default_ttl
        }
    
    def memoize(self, ttl: Optional[int] = None) -> Callable:
        """装饰器，用于缓存函数结果"""
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                # 为方法生成缓存键（排除self参数）
                if args and hasattr(args[0], func.__name__):
                    cache_key = self._generate_key(*args[1:], **kwargs)
                else:
                    cache_key = self._generate_key(*args, **kwargs)
                
                # 尝试从缓存获取结果
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator


class CacheManager:
    """缓存管理器，为系统各模块提供缓存功能"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._init_caches()
        return cls._instance
    
    def _init_caches(self):
        """初始化各模块的缓存"""
        # 为不同模块创建专用缓存
        self.caches = {
            'goal_interpretation': LRUCache(max_size=1000, default_ttl=3600),  # 目标解释缓存，1小时过期
            'subgoal_decomposition': LRUCache(max_size=500, default_ttl=1800),   # 子目标分解缓存，30分钟过期
            'transition_modeling': LRUCache(max_size=300, default_ttl=1200),     # 转换建模缓存，20分钟过期
            'action_sequencing': LRUCache(max_size=500, default_ttl=900),        # 动作序列缓存，15分钟过期
            'common': LRUCache(max_size=2000, default_ttl=7200)                  # 通用缓存，2小时过期
        }
        
        # 全局统计
        self.global_stats = {
            'total_hits': 0,
            'total_misses': 0,
            'total_evictions': 0,
            'start_time': time.time()
        }
    
    def get_cache(self, cache_name: str = 'common') -> LRUCache:
        """获取指定名称的缓存实例"""
        if cache_name not in self.caches:
            # 动态创建不存在的缓存
            self.caches[cache_name] = LRUCache()
        return self.caches[cache_name]
    
    def cache_result(self, module_name: str, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """缓存模块的处理结果"""
        cache = self.get_cache(module_name)
        cache.set(key, value, ttl)
    
    def get_cached_result(self, module_name: str, key: str) -> Optional[Any]:
        """获取缓存的模块处理结果"""
        cache = self.get_cache(module_name)
        return cache.get(key)
    
    def clear_cache(self, module_name: Optional[str] = None) -> None:
        """清除指定模块缓存或所有缓存"""
        if module_name:
            if module_name in self.caches:
                self.caches[module_name].clear()
        else:
            # 清除所有缓存
            for cache in self.caches.values():
                cache.clear()
    
    def get_cache_stats(self, module_name: Optional[str] = None) -> Dict[str, Any]:
        """获取缓存统计信息"""
        if module_name:
            if module_name not in self.caches:
                return None
            return self.caches[module_name].get_stats()
        
        # 获取所有缓存的统计
        stats = {}
        total_hits = 0
        total_misses = 0
        total_evictions = 0
        
        for name, cache in self.caches.items():
            cache_stats = cache.get_stats()
            stats[name] = cache_stats
            total_hits += cache_stats['hits']
            total_misses += cache_stats['misses']
            total_evictions += cache_stats['evictions']
        
        # 更新全局统计
        self.global_stats['total_hits'] = total_hits
        self.global_stats['total_misses'] = total_misses
        self.global_stats['total_evictions'] = total_evictions
        
        total_ops = total_hits + total_misses
        overall_hit_rate = (total_hits / total_ops) * 100 if total_ops > 0 else 0
        
        return {
            'overall': {
                'hit_rate': overall_hit_rate,
                'total_hits': total_hits,
                'total_misses': total_misses,
                'total_evictions': total_evictions,
                'total_operations': total_ops,
                'uptime_seconds': time.time() - self.global_stats['start_time']
            },
            'module_stats': stats
        }
    
    def optimize_caches(self) -> None:
        """优化缓存配置（基于使用模式）"""
        # 这个方法可以根据实际使用情况动态调整缓存大小和TTL
        # 目前只是一个占位符实现
        print("Cache optimization not yet implemented")
    
    def decorators(self):
        """提供缓存装饰器"""
        class ModuleDecorators:
            def __init__(self, cache_manager):
                self.cache_manager = cache_manager
            
            def goal_interpretation(self, ttl: Optional[int] = None):
                cache = self.cache_manager.get_cache('goal_interpretation')
                return cache.memoize(ttl)
            
            def subgoal_decomposition(self, ttl: Optional[int] = None):
                cache = self.cache_manager.get_cache('subgoal_decomposition')
                return cache.memoize(ttl)
            
            def transition_modeling(self, ttl: Optional[int] = None):
                cache = self.cache_manager.get_cache('transition_modeling')
                return cache.memoize(ttl)
            
            def action_sequencing(self, ttl: Optional[int] = None):
                cache = self.cache_manager.get_cache('action_sequencing')
                return cache.memoize(ttl)
            
            def common(self, ttl: Optional[int] = None):
                cache = self.cache_manager.get_cache('common')
                return cache.memoize(ttl)
        
        return ModuleDecorators(self)


# 创建全局缓存管理器实例
cache_manager = CacheManager()


def get_cache_manager() -> CacheManager:
    """获取缓存管理器实例"""
    return cache_manager


def memoize_goal_interpretation(func: Callable) -> Callable:
    """目标解释缓存装饰器"""
    return cache_manager.decorators().goal_interpretation()(func)


def memoize_subgoal_decomposition(func: Callable) -> Callable:
    """子目标分解缓存装饰器"""
    return cache_manager.decorators().subgoal_decomposition()(func)


def memoize_transition_modeling(func: Callable) -> Callable:
    """转换建模缓存装饰器"""
    return cache_manager.decorators().transition_modeling()(func)


def memoize_action_sequencing(func: Callable) -> Callable:
    """动作序列缓存装饰器"""
    return cache_manager.decorators().action_sequencing()(func)