#!/usr/bin/env python3
"""
基础集成测试 - 验证InterPreT集成的基本功能
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

def test_basic_imports():
    """测试基础导入"""
    print("🧪 测试基础导入...")
    
    try:
        import numpy as np
        print("✅ numpy导入成功")
    except ImportError as e:
        print(f"❌ numpy导入失败: {e}")
        return False
    
    try:
        import torch
        print("✅ torch导入成功")
    except ImportError as e:
        print(f"❌ torch导入失败: {e}")
        return False
    
    try:
        import yaml
        print("✅ yaml导入成功")
    except ImportError as e:
        print(f"❌ yaml导入失败: {e}")
        return False
    
    return True

def test_igibson_import():
    """测试iGibson导入"""
    print("🧪 测试iGibson导入...")
    
    try:
        import igibson
        print(f"✅ iGibson {igibson.__version__} 导入成功")
        return True
    except ImportError as e:
        print(f"❌ iGibson导入失败: {e}")
        return False

def test_eai_compatibility():
    """测试EAI兼容性"""
    print("🧪 测试EAI兼容性...")
    
    try:
        import eai
        print(f"✅ EAI {eai.__version__} 导入成功")
        return True
    except ImportError:
        try:
            from eai_compat import agent, make
            print("✅ EAI兼容层导入成功")
            return True
        except ImportError as e:
            print(f"❌ EAI兼容层导入失败: {e}")
            return False

def test_interpret_module():
    """测试目标解释模块"""
    print("🧪 测试目标解释模块...")
    
    try:
        from goal_interpretation import EAI_AVAILABLE
        print(f"✅ 目标解释模块导入成功，EAI可用: {EAI_AVAILABLE}")
        return True
    except ImportError as e:
        print(f"❌ 目标解释模块导入失败: {e}")
        return False

def main():
    print("🚀 EAI Interpretable Interface - 基础集成测试")
    print("=" * 60)
    
    tests = [
        ("基础导入", test_basic_imports),
        ("iGibson导入", test_igibson_import),
        ("EAI兼容性", test_eai_compatibility),
        ("目标解释模块", test_interpret_module),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 执行测试: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(tests)} 测试通过")
    
    if passed == len(tests):
        print("🎉 所有测试通过！环境配置成功！")
        return True
    else:
        print("⚠️  部分测试失败，请检查环境配置")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
