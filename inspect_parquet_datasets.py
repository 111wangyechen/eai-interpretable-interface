#!/usr/bin/env python3
# This script inspects parquet datasets structure and content for the EAI project
"""
Dataset Inspection Script
This script inspects the structure and content of Parquet datasets used by the InterPreT system.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

def inspect_parquet_file(file_path: str) -> Dict[str, Any]:
    """
    Inspect a single Parquet file and return detailed information.
    
    Args:
        file_path: Path to the Parquet file
        
    Returns:
        Dictionary with file inspection results
    """
    print(f"\n🔍 Inspecting file: {file_path}")
    results = {
        'file_path': file_path,
        'file_size_mb': 0,
        'shape': (0, 0),
        'columns': [],
        'dtypes': {},
        'sample_rows': 0,
        'null_counts': {},
        'column_stats': {},
        'unique_values': {}
    }
    
    try:
        # Check file size
        if os.path.exists(file_path):
            results['file_size_mb'] = round(os.path.getsize(file_path) / (1024 * 1024), 2)
            print(f"📏 File size: {results['file_size_mb']} MB")
        else:
            print(f"❌ File not found: {file_path}")
            return results
        
        # Read the Parquet file
        print("📖 Reading Parquet file...")
        df = pd.read_parquet(file_path)
        
        # Basic information
        results['shape'] = df.shape
        results['columns'] = list(df.columns)
        results['dtypes'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
        results['sample_rows'] = min(10, len(df))
        
        print(f"📊 Shape: {results['shape']} (rows × columns)")
        print(f"📋 Columns: {', '.join(results['columns'])}")
        print(f"🔢 Data types: {', '.join([f'{col}: {dtype}' for col, dtype in results['dtypes'].items()])}")
        
        # Null value counts
        null_counts = df.isnull().sum()
        results['null_counts'] = null_counts.to_dict()
        
        # Column statistics
        print("\n📈 Column statistics:")
        for col in df.columns:
            col_info = {}
            
            # Count nulls
            null_count = null_counts[col]
            null_percent = (null_count / len(df) * 100) if len(df) > 0 else 0
            col_info['null_count'] = int(null_count)
            col_info['null_percent'] = round(null_percent, 2)
            
            # Get unique values count
            try:
                unique_count = df[col].nunique()
                col_info['unique_count'] = unique_count
                
                # Get sample unique values if not too many
                if unique_count <= 10:
                    unique_vals = df[col].dropna().unique()
                    # Convert to string for JSON serialization
                    results['unique_values'][col] = [str(val)[:50] if len(str(val)) > 50 else str(val) for val in unique_vals[:5]]
            except Exception as e:
                col_info['unique_count'] = -1
                print(f"  ❌ Error getting unique values for {col}: {e}")
            
            # Get statistics for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info['min'] = float(df[col].min())
                col_info['max'] = float(df[col].max())
                col_info['mean'] = float(df[col].mean())
                col_info['std'] = float(df[col].std())
            
            results['column_stats'][col] = col_info
            
            # Print column info
            print(f"  🔹 {col}:")
            print(f"     - Non-null: {len(df) - null_count}/{len(df)} ({100 - null_percent:.1f}%)")
            print(f"     - Unique values: {col_info.get('unique_count', 'N/A')}")
            if pd.api.types.is_numeric_dtype(df[col]):
                print(f"     - Min/Max: {col_info.get('min', 'N/A')}/{col_info.get('max', 'N/A')}")
                print(f"     - Mean: {col_info.get('mean', 'N/A'):.2f}")
        
        # Show sample data
        print("\n🔍 Sample data preview:")
        sample_df = df.head(min(5, len(df)))
        # Format sample data for better readability
        for _, row in sample_df.iterrows():
            row_str = []
            for col in df.columns[:3]:  # Show first 3 columns
                val = row[col]
                val_str = str(val)[:30] + '...' if len(str(val)) > 30 else str(val)
                row_str.append(f"{col}: {val_str}")
            print(f"  {' | '.join(row_str)}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error inspecting file: {e}")
        results['error'] = str(e)
        return results

def compare_parquet_files(file1_path: str, file2_path: str) -> Dict[str, Any]:
    """
    Compare two Parquet files to identify differences and similarities.
    
    Args:
        file1_path: Path to the first Parquet file
        file2_path: Path to the second Parquet file
        
    Returns:
        Dictionary with comparison results
    """
    print(f"\n🔄 Comparing files: {os.path.basename(file1_path)} vs {os.path.basename(file2_path)}")
    
    # Inspect both files
    file1_info = inspect_parquet_file(file1_path)
    file2_info = inspect_parquet_file(file2_path)
    
    comparison = {
        'file1': file1_info['file_path'],
        'file2': file2_info['file_path'],
        'file_sizes': {
            'file1_mb': file1_info['file_size_mb'],
            'file2_mb': file2_info['file_size_mb'],
            'ratio': file1_info['file_size_mb'] / file2_info['file_size_mb'] if file2_info['file_size_mb'] > 0 else 0
        },
        'row_counts': {
            'file1': file1_info['shape'][0],
            'file2': file2_info['shape'][0],
            'difference': abs(file1_info['shape'][0] - file2_info['shape'][0])
        },
        'column_comparison': {
            'common_columns': list(set(file1_info['columns']) & set(file2_info['columns'])),
            'file1_only_columns': list(set(file1_info['columns']) - set(file2_info['columns'])),
            'file2_only_columns': list(set(file2_info['columns']) - set(file1_info['columns'])),
            'total_columns_in_common': len(set(file1_info['columns']) & set(file2_info['columns'])),
            'total_columns_difference': abs(len(file1_info['columns']) - len(file2_info['columns']))
        }
    }
    
    print("\n📊 Comparison Results:")
    print(f"🔢 Row count difference: {comparison['row_counts']['difference']} rows")
    print(f"📋 Common columns: {len(comparison['column_comparison']['common_columns'])}")
    print(f"📋 Columns only in first file: {len(comparison['column_comparison']['file1_only_columns'])}")
    print(f"📋 Columns only in second file: {len(comparison['column_comparison']['file2_only_columns'])}")
    
    if comparison['column_comparison']['common_columns']:
        print("\n🔍 Common columns:")
        for col in comparison['column_comparison']['common_columns'][:10]:  # Show first 10
            print(f"  - {col}")
        if len(comparison['column_comparison']['common_columns']) > 10:
            print(f"  ... and {len(comparison['column_comparison']['common_columns']) - 10} more")
    
    return comparison

def main():
    """
    Main function to inspect Parquet datasets.
    """
    print("🚀 Parquet Dataset Inspection Tool")
    print("=" * 50)
    
    # Default Parquet files to inspect
    default_files = [
        'behavior-00000-of-00001.parquet',
        'virtualhome-00000-of-00001.parquet'
    ]
    
    # Get absolute paths and check data directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # First try to find files in the data subdirectory
    data_dir = os.path.join(base_dir, 'data')
    parquet_files = [os.path.join(data_dir, fname) for fname in default_files]
    # If files not found in data directory, fall back to base directory
    if not any(os.path.exists(f) for f in parquet_files):
        print("⚠️ Files not found in data directory, trying base directory...")
        parquet_files = [os.path.join(base_dir, fname) for fname in default_files]
    
    # Check if files exist
    existing_files = []
    for file_path in parquet_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            print(f"⚠️ File not found: {file_path}")
    
    # Inspect each file individually
    all_results = {}
    for file_path in existing_files:
        print(f"\n{'-' * 70}")
        file_results = inspect_parquet_file(file_path)
        all_results[os.path.basename(file_path)] = file_results
    
    # Compare files if we have at least two
    if len(existing_files) >= 2:
        print(f"\n{'=' * 70}")
        comparison = compare_parquet_files(existing_files[0], existing_files[1])
        all_results['comparison'] = comparison
    
    # Save results to JSON file
    output_file = os.path.join(base_dir, 'parquet_inspection_results.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n💾 Results saved to: {output_file}")
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
    
    print(f"\n{'-' * 50}")
    print("✅ Dataset inspection completed")
    print("📋 Summary:")
    for file_name, results in all_results.items():
        if file_name != 'comparison':
            print(f"  - {file_name}: {results['shape'][0]} rows, {results['shape'][1]} columns")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n❌ Inspection interrupted by user")
        sys.exit(1)
    except ImportError as e:
        print(f"\n❌ Missing required package: {e}")
        print("💡 Please install pandas and pyarrow: pip install pandas pyarrow")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)