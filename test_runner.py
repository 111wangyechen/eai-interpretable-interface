#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统一测试运行器脚本

此脚本用于统一管理和运行BEHAVIOR和VirtualHome环境的测试，包括：
- 支持运行单个或多个环境的测试
- 并行或顺序执行测试任务
- 收集和整合测试结果
- 生成综合测试报告
- 提供命令行接口进行配置
"""

import os
import sys
import json
import yaml
import time
import logging
import argparse
import datetime
import subprocess
import traceback
import importlib.util
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_runner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('test_runner')


class TestRunner:
    """统一测试运行器类"""
    
    # 支持的环境类型
    SUPPORTED_ENVIRONMENTS = {
        'behavior': {
            'script_path': 'simulation_behavior/scripts/behavior_test_evaluator.py',
            'config_path': 'simulation_behavior/config/behavior_test_config.yaml',
            'result_dir': 'simulation_behavior/results'
        },
        'virtualhome': {
            'script_path': 'simulation_virtualhome/scripts/virtualhome_test_evaluator.py',
            'config_path': 'simulation_virtualhome/config/virtualhome_test_config.yaml',
            'result_dir': 'simulation_virtualhome/results'
        }
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化测试运行器
        
        Args:
            config: 配置字典
        """
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 默认配置
        self.config = {
            'environments': ['behavior', 'virtualhome'],
            'parallel': False,
            'max_workers': 2,
            'output_dir': os.path.join(self.base_dir, 'test_results'),
            'report_format': 'both',  # 'json', 'markdown', or 'both'
            'log_level': 'INFO'
        }
        
        # 更新配置
        if config:
            self.config.update(config)
        
        # 设置日志级别
        if 'log_level' in self.config:
            logger.setLevel(getattr(logging, self.config['log_level'], logging.INFO))
        
        # 确保输出目录存在
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # 初始化结果存储
        self.overall_results = {
            'test_run_id': datetime.datetime.now().strftime('%Y%m%d_%H%M%S'),
            'start_time': None,
            'end_time': None,
            'environments': {},
            'summary': {}
        }
    
    def validate_environments(self, environments: List[str]) -> List[str]:
        """
        验证环境列表
        
        Args:
            environments: 要验证的环境列表
            
        Returns:
            有效环境列表
        """
        valid_environments = []
        for env in environments:
            if env in self.SUPPORTED_ENVIRONMENTS:
                script_path = os.path.join(self.base_dir, self.SUPPORTED_ENVIRONMENTS[env]['script_path'])
                if os.path.exists(script_path):
                    valid_environments.append(env)
                    logger.info(f"验证通过环境: {env}")
                else:
                    logger.warning(f"环境 {env} 的测试脚本不存在: {script_path}")
            else:
                logger.warning(f"不支持的环境类型: {env}")
        
        return valid_environments
    
    def run_environment_test(self, environment: str, args: List[str] = None) -> Dict[str, Any]:
        """
        运行指定环境的测试
        
        Args:
            environment: 环境名称
            args: 命令行参数
            
        Returns:
            测试结果
        """
        if environment not in self.SUPPORTED_ENVIRONMENTS:
            logger.error(f"不支持的环境: {environment}")
            return {
                'status': 'failed',
                'error': f'不支持的环境: {environment}',
                'environment': environment
            }
        
        env_config = self.SUPPORTED_ENVIRONMENTS[environment]
        script_path = os.path.join(self.base_dir, env_config['script_path'])
        
        if not os.path.exists(script_path):
            logger.error(f"测试脚本不存在: {script_path}")
            return {
                'status': 'failed',
                'error': f'测试脚本不存在: {script_path}',
                'environment': environment
            }
        
        logger.info(f"开始运行 {environment} 环境测试")
        
        # 构建命令
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)
        
        # 添加日志输出重定向
        log_file = os.path.join(self.config['output_dir'], f'{environment}_test_{self.overall_results["test_run_id"]}.log')
        
        try:
            # 运行测试脚本
            start_time = time.time()
            
            with open(log_file, 'w', encoding='utf-8') as log_f:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=self.base_dir
                )
                
                # 实时输出日志
                for line in process.stdout:
                    log_f.write(line)
                    log_f.flush()
                    print(line.strip())
                
                process.wait()
            
            duration = time.time() - start_time
            
            # 尝试查找最新的结果文件
            result_files = self._find_latest_result_files(environment)
            
            result = {
                'environment': environment,
                'status': 'success' if process.returncode == 0 else 'failed',
                'exit_code': process.returncode,
                'duration': duration,
                'log_file': log_file,
                'result_files': result_files,
                'start_time': datetime.datetime.fromtimestamp(start_time).isoformat(),
                'end_time': datetime.datetime.fromtimestamp(start_time + duration).isoformat()
            }
            
            # 加载结果文件内容
            if result_files:
                result['results'] = self._load_result_files(result_files)
            
            logger.info(f"{environment} 环境测试完成，状态: {'成功' if process.returncode == 0 else '失败'}")
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"运行 {environment} 环境测试时出错: {error_msg}")
            traceback.print_exc()
            
            return {
                'environment': environment,
                'status': 'failed',
                'error': error_msg,
                'log_file': log_file
            }
    
    def _find_latest_result_files(self, environment: str) -> List[str]:
        """
        查找最新的结果文件
        
        Args:
            environment: 环境名称
            
        Returns:
            最新结果文件路径列表
        """
        if environment not in self.SUPPORTED_ENVIRONMENTS:
            return []
        
        result_dir = os.path.join(self.base_dir, self.SUPPORTED_ENVIRONMENTS[environment]['result_dir'])
        if not os.path.exists(result_dir):
            return []
        
        # 查找所有结果文件
        result_files = []
        for root, _, files in os.walk(result_dir):
            for file in files:
                if file.endswith('.json') and ('result' in file or 'summary' in file):
                    result_files.append(os.path.join(root, file))
        
        # 按修改时间排序，返回最新的几个
        result_files.sort(key=os.path.getmtime, reverse=True)
        return result_files[:5]  # 返回最新的5个文件
    
    def _load_result_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        加载结果文件内容
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            结果字典
        """
        results = {}
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 尝试解析为JSON
                    if file_path.endswith('.json'):
                        content = json.load(f)
                        file_name = os.path.basename(file_path)
                        results[file_name] = content
            except Exception as e:
                logger.warning(f"加载结果文件失败 {file_path}: {e}")
        
        return results
    
    def run_sequential(self, environments: List[str], args: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """
        顺序执行测试
        
        Args:
            environments: 环境列表
            args: 各环境的命令行参数
            
        Returns:
            测试结果
        """
        logger.info(f"开始顺序执行测试: {', '.join(environments)}")
        
        for environment in environments:
            env_args = args.get(environment, []) if args else []
            result = self.run_environment_test(environment, env_args)
            self.overall_results['environments'][environment] = result
        
        return self.overall_results
    
    def run_parallel(self, environments: List[str], args: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """
        并行执行测试
        
        Args:
            environments: 环境列表
            args: 各环境的命令行参数
            
        Returns:
            测试结果
        """
        logger.info(f"开始并行执行测试: {', '.join(environments)}")
        max_workers = min(self.config.get('max_workers', 2), len(environments))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_env = {}
            for environment in environments:
                env_args = args.get(environment, []) if args else []
                future = executor.submit(self.run_environment_test, environment, env_args)
                future_to_env[future] = environment
            
            # 收集结果
            for future in as_completed(future_to_env):
                environment = future_to_env[future]
                try:
                    result = future.result()
                    self.overall_results['environments'][environment] = result
                except Exception as e:
                    logger.error(f"获取 {environment} 结果时出错: {e}")
                    self.overall_results['environments'][environment] = {
                        'environment': environment,
                        'status': 'failed',
                        'error': str(e)
                    }
        
        return self.overall_results
    
    def run_all_tests(self):
        """
        运行所有测试
        
        Returns:
            测试结果
        """
        self.overall_results['start_time'] = datetime.datetime.now().isoformat()
        logger.info("开始运行所有测试")
        
        # 验证环境
        environments = self.validate_environments(self.config['environments'])
        if not environments:
            logger.error("没有有效的环境可以测试")
            return self.overall_results
        
        # 准备参数
        args = self.config.get('environment_args', {})
        
        # 执行测试
        if self.config.get('parallel', False):
            self.run_parallel(environments, args)
        else:
            self.run_sequential(environments, args)
        
        # 计算汇总信息
        self._calculate_summary()
        
        self.overall_results['end_time'] = datetime.datetime.now().isoformat()
        logger.info("所有测试完成")
        
        # 保存结果
        self.save_results()
        
        return self.overall_results
    
    def _calculate_summary(self):
        """计算汇总信息"""
        environments = self.overall_results.get('environments', {})
        
        summary = {
            'total_environments': len(environments),
            'successful_environments': 0,
            'failed_environments': 0,
            'metrics': {}
        }
        
        # 统计成功失败情况
        for env_name, env_result in environments.items():
            if env_result.get('status') == 'success':
                summary['successful_environments'] += 1
            else:
                summary['failed_environments'] += 1
            
            # 汇总指标
            if 'results' in env_result:
                for file_name, file_content in env_result['results'].items():
                    if isinstance(file_content, dict) and 'summary' in file_content:
                        env_summary = file_content['summary']
                        for metric_name, metric_value in env_summary.items():
                            if metric_name not in summary['metrics']:
                                summary['metrics'][metric_name] = {}
                            summary['metrics'][metric_name][env_name] = metric_value
        
        # 计算整体成功率
        if summary['total_environments'] > 0:
            summary['success_rate'] = summary['successful_environments'] / summary['total_environments']
        else:
            summary['success_rate'] = 0
        
        self.overall_results['summary'] = summary
    
    def save_results(self):
        """保存测试结果"""
        # 保存JSON格式
        if self.config.get('report_format') in ['json', 'both']:
            json_file = os.path.join(self.config['output_dir'], f'test_summary_{self.overall_results["test_run_id"]}.json')
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(self.overall_results, f, indent=2, ensure_ascii=False)
                logger.info(f"JSON报告已保存至: {json_file}")
            except Exception as e:
                logger.error(f"保存JSON报告失败: {e}")
        
        # 保存Markdown格式
        if self.config.get('report_format') in ['markdown', 'both']:
            md_file = os.path.join(self.config['output_dir'], f'test_summary_{self.overall_results["test_run_id"]}.md')
            try:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(self._generate_markdown_report())
                logger.info(f"Markdown报告已保存至: {md_file}")
            except Exception as e:
                logger.error(f"保存Markdown报告失败: {e}")
    
    def _generate_markdown_report(self) -> str:
        """
        生成Markdown格式报告
        
        Returns:
            Markdown格式的报告内容
        """
        summary = self.overall_results.get('summary', {})
        environments = self.overall_results.get('environments', {})
        
        report = f"""# 综合测试报告

## 测试概述
- **测试运行ID**: {self.overall_results.get('test_run_id', 'N/A')}
- **开始时间**: {self.overall_results.get('start_time', 'N/A')}
- **结束时间**: {self.overall_results.get('end_time', 'N/A')}
- **并行执行**: {self.config.get('parallel', False)}

## 整体结果
- **测试环境总数**: {summary.get('total_environments', 0)}
- **成功环境数**: {summary.get('successful_environments', 0)}
- **失败环境数**: {summary.get('failed_environments', 0)}
- **整体成功率**: {summary.get('success_rate', 0):.2%}

## 详细指标汇总
"""
        
        # 添加指标表格
        if summary.get('metrics'):
            for metric_name, env_values in summary['metrics'].items():
                report += f"### {metric_name}\n\n"
                report += "| 环境 | 值 |\n"
                report += "|------|-----|\n"
                for env_name, value in env_values.items():
                    report += f"| {env_name} | {value} |\n"
                report += "\n"
        
        report += "## 各环境测试详情\n\n"
        
        # 添加各环境详情
        for env_name, env_result in environments.items():
            status_icon = "✅" if env_result.get('status') == 'success' else "❌"
            report += f"### {status_icon} {env_name}\n\n"
            report += f"- **状态**: {env_result.get('status', 'N/A')}\n"
            report += f"- **开始时间**: {env_result.get('start_time', 'N/A')}\n"
            report += f"- **结束时间**: {env_result.get('end_time', 'N/A')}\n"
            report += f"- **持续时间**: {env_result.get('duration', 'N/A'):.2f}秒\n"
            
            if 'exit_code' in env_result:
                report += f"- **退出代码**: {env_result['exit_code']}\n"
            
            if 'error' in env_result:
                report += f"- **错误信息**: {env_result['error']}\n"
            
            if 'log_file' in env_result:
                report += f"- **日志文件**: {env_result['log_file']}\n"
            
            if 'result_files' in env_result:
                report += f"- **结果文件**:\n"
                for file_path in env_result['result_files']:
                    report += f"  - {file_path}\n"
            
            report += "\n"
        
        return report


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='统一测试运行器')
    
    # 环境选择
    parser.add_argument('--environments', '-e', nargs='+', 
                      choices=['behavior', 'virtualhome'],
                      default=['behavior', 'virtualhome'],
                      help='要测试的环境列表')
    
    # 执行模式
    parser.add_argument('--parallel', '-p', action='store_true',
                      help='并行执行测试')
    
    # 工作线程数
    parser.add_argument('--max-workers', type=int, default=2,
                      help='并行执行的最大工作线程数')
    
    # 输出配置
    parser.add_argument('--output-dir', '-o', type=str,
                      help='结果输出目录')
    
    # 报告格式
    parser.add_argument('--report-format', choices=['json', 'markdown', 'both'],
                      default='both',
                      help='报告格式')
    
    # 日志级别
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      default='INFO',
                      help='日志级别')
    
    # 特定环境参数
    parser.add_argument('--behavior-args', nargs=argparse.REMAINDER,
                      help='传递给BEHAVIOR测试的参数')
    
    # 调试模式
    parser.add_argument('--debug', action='store_true',
                      help='启用调试模式')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 构建配置
    config = {
        'environments': args.environments,
        'parallel': args.parallel,
        'max_workers': args.max_workers,
        'log_level': args.log_level,
        'report_format': args.report_format
    }
    
    if args.output_dir:
        config['output_dir'] = args.output_dir
    
    # 添加特定环境参数
    if args.behavior_args and '--behavior-args' in sys.argv:
        # 提取--behavior-args之后的参数
        behavior_args_index = sys.argv.index('--behavior-args')
        behavior_args = sys.argv[behavior_args_index + 1:]
        config['environment_args'] = {'behavior': behavior_args}
    
    # 启用调试模式
    if args.debug:
        config['log_level'] = 'DEBUG'
    
    try:
        # 初始化并运行测试
        runner = TestRunner(config)
        results = runner.run_all_tests()
        
        # 输出结果摘要
        summary = results.get('summary', {})
        print("\n测试完成！")
        print(f"整体成功率: {summary.get('success_rate', 0):.2%}")
        print(f"成功环境数: {summary.get('successful_environments', 0)}")
        print(f"失败环境数: {summary.get('failed_environments', 0)}")
        
        # 输出报告位置
        output_dir = config.get('output_dir', runner.config['output_dir'])
        print(f"\n报告已保存至: {output_dir}")
        
    except KeyboardInterrupt:
        logger.info("用户中断测试")
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"测试运行器出错: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()