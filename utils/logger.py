#!/usr/bin/env python3
"""
统一日志配置模块
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# 日志级别映射
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# 日志格式
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 日志目录
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件名
LOG_FILE = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d")}_interpretr.log')

def get_logger(name: str, log_level: str = 'info') -> logging.Logger:
    """
    获取配置好的日志记录器
    
    Args:
        name: 日志记录器名称，通常使用__name__
        log_level: 日志级别，默认为info
        
    Returns:
        配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(log_level.lower(), logging.INFO))
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVELS.get(log_level.lower(), logging.INFO))
        
        # 创建文件处理器（按大小切割，保留5个备份）
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(LOG_LEVELS.get(log_level.lower(), logging.INFO))
        
        # 创建格式化器
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        
        # 为处理器设置格式化器
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# 暴露常用日志级别方法
def debug(msg: str, *args, **kwargs):
    """调试日志"""
    get_logger('interpretr').debug(msg, *args, **kwargs)

def info(msg: str, *args, **kwargs):
    """信息日志"""
    get_logger('interpretr').info(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs):
    """警告日志"""
    get_logger('interpretr').warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    """错误日志"""
    get_logger('interpretr').error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs):
    """严重错误日志"""
    get_logger('interpretr').critical(msg, *args, **kwargs)
