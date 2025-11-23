#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集分析脚本
用于检查和分析eai-interpretable-interface/data目录下的.parquet文件
"""

import os
import sys
import pandas as pd
import json
from typing import Dict, Any, List

# 设置中文显示
pd.set_option('display.unicode.east_asian_width', True)

# 数据集路径
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def print_header(title: str) -> None:
    """
    打印标题头
    """
    print("\n" + "=" * 80)
    print(f"{title}".center(80))
    print("=" * 80)


def print_subheader(title: str) -> None:
    """
    打印子标题
    """
    print("\n" + "-" * 80)
    print(f"{title}".center(80))
    print("-" * 80)


def check_directory_structure() -> None:
    """
    检查数据目录结构
    """
    print_header("数据目录结构分析")
    
    # 检查data目录是否存在
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在: {data_dir}")
        return
    
    print(f"✓ 找到数据目录: {data_dir}")
    
    # 列出目录内容
    try:
        files = os.listdir(data_dir)
        print(f"✓ 目录中的文件数量: {len(files)}")
        print("\n文件列表:")
        for i, file in enumerate(sorted(files), 1):
            file_path = os.path.join(data_dir, file)
            file_size = os.path.getsize(file_path) / 1024 / 1024  # 转换为MB
            print(f"  {i}. {file} ({file_size:.2f} MB)")
    except Exception as e:
        print(f"❌ 读取目录内容失败: {e}")


def analyze_parquet_file(file_path: str) -> None:
    """
    分析parquet文件内容
    """
    print_subheader(f"分析文件: {os.path.basename(file_path)}")
    
    try:
        # 读取parquet文件
        df = pd.read_parquet(file_path)
        
        # 基本信息
        print(f"✓ 成功读取文件: {os.path.basename(file_path)}")
        print(f"✓ 数据行数: {len(df)}")
        print(f"✓ 数据列数: {len(df.columns)}")
        print(f"✓ 文件大小: {os.path.getsize(file_path) / 1024 / 1024:.2f} MB")
        
        # 显示列信息
        print("\n列信息:")
        for i, column in enumerate(df.columns, 1):
            col_type = str(df[column].dtype)
            print(f"  {i}. {column} ({col_type})")
        
        # 显示列统计信息
        print("\n列统计信息:")
        for column in df.columns:
            # 计算非空值数量
            non_null_count = df[column].count()
            # 对于分类列，显示唯一值数量
            if df[column].dtype == 'object':
                unique_count = df[column].nunique()
                print(f"  {column}: 非空值={non_null_count}, 唯一值={unique_count}")
                # 显示前5个唯一值示例
                if unique_count <= 10:
                    unique_values = df[column].dropna().unique()
                    print(f"    示例值: {', '.join(map(str, unique_values[:5]))}")
                else:
                    unique_values = df[column].dropna().unique()
                    print(f"    示例值: {', '.join(map(str, unique_values[:3]))}, ...")
            else:
                # 对于数值列，显示范围
                min_val = df[column].min()
                max_val = df[column].max()
                print(f"  {column}: 非空值={non_null_count}, 范围={min_val} - {max_val}")
        
        # 显示前5行数据（限制显示列数）
        print("\n前5行数据:")
        if len(df.columns) > 10:
            # 如果列太多，只显示前10列
            print(df.head().iloc[:, :10])
        else:
            print(df.head())
        
        # 检查是否有嵌套JSON数据
        print("\n检查嵌套JSON数据:")
        has_json_columns = False
        for column in df.columns:
            if df[column].dtype == 'object':
                # 尝试解析为JSON
                try:
                    # 只检查前几个非空值
                    sample_values = df[column].dropna().head(3)
                    for val in sample_values:
                        if isinstance(val, str) and (val.startswith('{') or val.startswith('[')):
                            try:
                                json_obj = json.loads(val)
                                has_json_columns = True
                                print(f"✓ 在列 '{column}' 中发现JSON格式数据")
                                print(f"  示例JSON结构: {type(json_obj).__name__}")
                                if isinstance(json_obj, dict):
                                    print(f"  JSON键: {', '.join(json_obj.keys())[:100]}...")
                                elif isinstance(json_obj, list) and json_obj:
                                    print(f"  列表长度: {len(json_obj)}, 第一个元素类型: {type(json_obj[0]).__name__}")
                                break
                            except:
                                pass
                except Exception as e:
                    print(f"  检查列 '{column}' 时出错: {e}")
        
        if not has_json_columns:
            print("  未发现嵌套JSON格式数据")
        
    except Exception as e:
        print(f"❌ 分析文件失败: {e}")


def analyze_all_parquet_files() -> None:
    """
    分析所有parquet文件
    """
    print_header("PARQUET文件分析")
    
    # 查找所有.parquet文件
    parquet_files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
    
    if not parquet_files:
        print("❌ 未找到.parquet文件")
        return
    
    print(f"✓ 找到 {len(parquet_files)} 个.parquet文件")
    
    # 逐个分析文件
    for parquet_file in sorted(parquet_files):
        file_path = os.path.join(data_dir, parquet_file)
        analyze_parquet_file(file_path)


def generate_dataset_summary() -> Dict[str, Any]:
    """
    生成数据集摘要
    """
    print_header("生成数据集摘要")
    
    summary = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'data_directory': data_dir,
        'files': [],
        'summary_stats': {}
    }
    
    # 分析所有parquet文件
    parquet_files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
    
    # 计算总文件数和总大小
    total_size = 0
    total_rows = 0
    
    for parquet_file in sorted(parquet_files):
        file_path = os.path.join(data_dir, parquet_file)
        file_size = os.path.getsize(file_path) / 1024 / 1024  # MB
        total_size += file_size
        
        try:
            df = pd.read_parquet(file_path)
            file_rows = len(df)
            total_rows += file_rows
            
            file_info = {
                'filename': parquet_file,
                'size_mb': round(file_size, 2),
                'rows': file_rows,
                'columns': df.columns.tolist(),
                'column_types': {col: str(df[col].dtype) for col in df.columns},
                'sample_data': df.head(2).to_dict('records')
            }
            
            summary['files'].append(file_info)
            print(f"✓ 已处理文件: {parquet_file} ({file_rows} 行)")
            
        except Exception as e:
            print(f"❌ 处理文件失败: {parquet_file} - {e}")
            summary['files'].append({
                'filename': parquet_file,
                'error': str(e)
            })
    
    # 更新摘要统计
    summary['summary_stats'] = {
        'total_files': len(parquet_files),
        'total_size_mb': round(total_size, 2),
        'total_rows': total_rows,
        'average_rows_per_file': round(total_rows / len(parquet_files), 2) if parquet_files else 0
    }
    
    # 保存摘要到JSON文件
    summary_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_summary.json')
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        print(f"✓ 数据集摘要已保存到: {summary_file}")
    except Exception as e:
        print(f"❌ 保存摘要失败: {e}")
    
    return summary

def check_readme_file() -> None:
    """
    检查README.md文件
    """
    print_header("README文件分析")
    
    readme_path = os.path.join(data_dir, 'README.md')
    
    if not os.path.exists(readme_path):
        print("❌ 未找到README.md文件")
        return
    
    print(f"✓ 找到README.md文件: {readme_path}")
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\nREADME内容:")
        print("---")
        print(content)
        print("---")
        
        # 检查README内容是否有有用信息
        if len(content.strip()) == 0:
            print("❌ README内容为空")
        elif len(content) < 100:
            print("⚠️ README内容较少，可能缺少详细说明")
        else:
            print("✓ README内容似乎完整")
            
    except Exception as e:
        print(f"❌ 读取README.md失败: {e}")

def main():
    """
    主函数
    """
    print("EAI Challenge 数据集分析工具")
    print("用于分析behavior和virtualhome数据集")
    print("=" * 80)
    
    # 检查目录结构
    check_directory_structure()
    
    # 检查README文件
    check_readme_file()
    
    # 分析所有parquet文件
    analyze_all_parquet_files()
    
    # 生成摘要
    generate_dataset_summary()
    
    print("\n" + "=" * 80)
    print("数据集分析完成".center(80))
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ 脚本被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 脚本执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)