#!/usr/bin/env python3
"""
环境验证脚本 - 验证所有依赖是否正确安装
"""

import sys
import os

def check_dependency(name, import_name=None):
    """检查依赖是否可用"""
    try:
        module = __import__(import_name or name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {name}: {e}")
        return False

def main():
    print("🔍 EAI Interpretable Interface - 环境验证")
    print("=" * 50)
    
    # 检查Python版本
    print(f"🐍 Python版本: {sys.version}")
    print()
    
    # 检查核心依赖
    core_deps = [
        ('numpy', 'numpy'),
        ('torch', 'torch'),
        ('gym', 'gym'),
        ('pyyaml', 'yaml'),
        ('matplotlib', 'matplotlib'),
        ('scipy', 'scipy'),
        ('networkx', 'networkx'),
    ]
    
    print("📦 核心依赖检查:")
    for name, import_name in core_deps:
        check_dependency(name, import_name)
    
    print()
    
    # 检查仿真环境
    print("🎮 仿真环境检查:")
    
    # 检查iGibson
    if check_dependency('iGibson', 'igibson'):
        try:
            import igibson
            from igibson.envs.igibson_env import iGibsonEnv
            print("   ✅ iGibson环境类可用")
        except ImportError as e:
            print(f"   ❌ iGibson环境类不可用: {e}")
    
    # 检查EAI
    try:
        import eai
        print(f"✅ EAI: {eai.__version__}")
    except ImportError:
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from eai_compat import agent, make
            print("✅ EAI兼容层: 可用")
        except ImportError:
            print("❌ EAI: 不可用")
    
    print()
    
    # 检查GPU支持
    print("🎮 GPU支持检查:")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA可用: {torch.version.cuda}")
            print(f"🎮 GPU数量: {torch.cuda.device_count()}")
        else:
            print("⚠️  CUDA不可用，使用CPU模式")
    except ImportError:
        print("❌ 无法检查GPU支持")
    
    print()
    print("✅ 环境验证完成！")

if __name__ == "__main__":
    main()
