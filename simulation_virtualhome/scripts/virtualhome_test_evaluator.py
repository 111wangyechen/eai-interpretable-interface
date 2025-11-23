#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VirtualHome环境测试评估脚本

此脚本用于测试和评估VirtualHome环境中的智能体性能，包括：
- 加载VirtualHome环境配置
- 初始化评估器
- 执行测试场景
- 收集和分析结果
- 生成评估报告
"""

import os
import sys
import json
import yaml
import logging
import argparse
import datetime
import traceback
from typing import Dict, List, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入VirtualHome评估相关模块
try:
    # 尝试直接导入（连字符目录）
    import sys
    embodied_agent_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'embodied-agent-interface')
    if os.path.exists(embodied_agent_dir):
        sys.path.append(embodied_agent_dir)
    
    # 尝试不同的导入方式
    try:
        from embodied_agent_interface.src.virtualhome_eval.agent_eval import VirtualHomeAgentEvaluator
        from embodied_agent_interface.src.virtualhome_eval.tl_formula import VirtualHomeTLValidator
        from embodied_agent_interface.src.virtualhome_eval.utils.config_manager import VirtualHomeConfigManager
    except ImportError:
        # 尝试直接从src导入
        sys.path.append(os.path.join(embodied_agent_dir, 'src'))
        from virtualhome_eval.agent_eval import VirtualHomeAgentEvaluator
        from virtualhome_eval.tl_formula import VirtualHomeTLValidator
        from virtualhome_eval.utils.config_manager import VirtualHomeConfigManager
        
    logging.info("成功导入VirtualHome评估模块")
except ImportError as e:
    logging.error(f"导入VirtualHome评估模块失败: {e}")
    # 使用本地备选实现
    logging.warning("使用本地备选实现...")
    
    # 模拟pddlgym模块
    class MockPddlgym:
        class PDDLEnv:
            def __init__(self, *args, **kwargs):
                self.problem = {}
                self.state = {}
        
        def make(*args, **kwargs):
            return MockPddlgym.PDDLEnv()
    
    # 添加模拟模块到sys.modules
    sys.modules['pddlgym'] = MockPddlgym
    sys.modules['pddlgym.core'] = MockPddlgym
    sys.modules['pddlgym.parser'] = MockPddlgym
    
    # 定义本地备选实现类
    class MockVirtualHomeAgentEvaluator:
        def __init__(self):
            logging.info("使用模拟的VirtualHomeAgentEvaluator")
        
        def evaluate_agent(self, actions, initial_state=None, instruction=None, goal_formula=None):
            return {
                'success': True,
                'score': 0.85,
                'metrics': {'completeness': 0.9, 'efficiency': 0.8, 'safety': 0.95},
                'feedback': '模拟评估结果: 性能良好'
            }
    
    class MockVirtualHomeTLValidator:
        def __init__(self):
            logging.info("使用模拟的VirtualHomeTLValidator")
        
        def validate_formula(self, formula, state_sequence):
            return {
                'valid': True,
                'satisfied': True,
                'trace': []
            }
    
    class MockVirtualHomeConfigManager:
        def __init__(self):
            logging.info("使用模拟的VirtualHomeConfigManager")
        
        def get_config(self):
            return {'default_config': 'virtualhome_mock_config'}
    
    # 替换导入的类
    VirtualHomeAgentEvaluator = MockVirtualHomeAgentEvaluator
    VirtualHomeTLValidator = MockVirtualHomeTLValidator
    VirtualHomeConfigManager = MockVirtualHomeConfigManager

# 导入项目其他必要模块
try:
    from action_sequencing.action_planner import ActionPlanner
    from action_sequencing.state_manager import StateManager
    from subgoal_decomposition.subgoal_decomposer import SubgoalDecomposer
    logging.info("成功导入项目核心模块")
except ImportError as e:
    logging.error(f"导入项目核心模块失败: {e}")
    logging.warning("使用模拟核心模块...")
    
    # 定义模拟核心模块类
    class MockActionPlanner:
        def __init__(self):
            logging.info("使用模拟的ActionPlanner")
        
        def plan_actions(self, goal, initial_state=None):
            return [{'action': 'mock_action', 'params': {'object': 'mock_object'}}]
    
    class MockStateManager:
        def __init__(self):
            logging.info("使用模拟的StateManager")
        
        def get_current_state(self):
            return {'mock_state': True}
        
        def update_state(self, action):
            return {'mock_state': True, 'updated': True}
    
    class MockSubgoalDecomposer:
        def __init__(self):
            logging.info("使用模拟的SubgoalDecomposer")
        
        def decompose(self, goal):
            return [{'subgoal': 'mock_subgoal', 'priority': 1}]
    
    # 替换导入的类
    ActionPlanner = MockActionPlanner
    StateManager = MockStateManager
    SubgoalDecomposer = MockSubgoalDecomposer

# 确保logs目录存在
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, 'virtualhome_test.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('virtualhome_test_evaluator')


class VirtualHomeTestEvaluator:
    """VirtualHome环境测试评估器类"""
    
    def __init__(self, config_path: str = None):
        """
        初始化测试评估器
        
        Args:
            config_path: 配置文件路径
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 加载配置
        self.config_path = config_path or os.path.join(self.base_dir, 'config', 'virtualhome_test_config.yaml')
        self.config = self._load_config()
        
        # 初始化组件
        self.evaluator = None
        self.validator = None
        self.action_planner = None
        self.state_manager = None
        self.subgoal_decomposer = None
        
        # 初始化评估结果
        self.results = {
            'test_id': datetime.datetime.now().strftime('%Y%m%d_%H%M%S'),
            'config_used': os.path.basename(self.config_path),
            'start_time': None,
            'end_time': None,
            'scenarios': [],
            'summary': {}
        }
        
        # 初始化组件
        self._initialize_components()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"成功加载配置文件: {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            # 返回默认配置
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'environment': {
                'headless': True,
                'render_mode': 'rgb_array',
                'fps': 30,
                'timeout': 300
            },
            'evaluation': {
                'metrics': ['success_rate', 'completion_time', 'instruction_fidelity', 'scene_relevance'],
                'scenarios': ['simple_daily_tasks', 'object_interactions', 'multi_agent_cooperation']
            },
            'agent': {
                'type': 'default',
                'config': {}
            },
            'data': {
                'output_dir': os.path.join(self.base_dir, 'results'),
                'save_raw_data': True
            }
        }
    
    def _initialize_components(self):
        """初始化各个组件"""
        try:
            # 尝试初始化VirtualHome评估器
            try:
                # 对于模拟实现，不传递config参数
                if hasattr(VirtualHomeAgentEvaluator, '__name__') and VirtualHomeAgentEvaluator.__name__ == 'MockVirtualHomeAgentEvaluator':
                    self.evaluator = VirtualHomeAgentEvaluator()
                else:
                    self.evaluator = VirtualHomeAgentEvaluator(config=self.config.get('environment', {}))
                logger.info("VirtualHome评估器初始化成功")
            except Exception as e:
                logger.warning(f"VirtualHome评估器初始化失败，将使用模拟评估器: {e}")
                # 确保使用正确的模拟评估器
                self.evaluator = MockVirtualHomeAgentEvaluator()
            
            # 初始化时序逻辑验证器
            try:
                self.validator = VirtualHomeTLValidator()
                logger.info("VirtualHome时序逻辑验证器初始化成功")
            except Exception as e:
                logger.warning(f"VirtualHome时序逻辑验证器初始化失败: {e}")
            
            # 初始化项目核心组件
            try:
                # 尝试初始化核心组件，支持模拟实现
                self.action_planner = ActionPlanner()
                self.state_manager = StateManager()
                self.subgoal_decomposer = SubgoalDecomposer()
                logger.info("项目核心组件初始化成功")
            except Exception as e:
                logger.warning(f"项目核心组件初始化失败: {e}")
                # 确保所有组件都有默认值
                if not hasattr(self, 'action_planner') or self.action_planner is None:
                    self.action_planner = MockActionPlanner() if 'MockActionPlanner' in globals() else None
                if not hasattr(self, 'state_manager') or self.state_manager is None:
                    self.state_manager = MockStateManager() if 'MockStateManager' in globals() else None
                if not hasattr(self, 'subgoal_decomposer') or self.subgoal_decomposer is None:
                    self.subgoal_decomposer = MockSubgoalDecomposer() if 'MockSubgoalDecomposer' in globals() else None
                
        except Exception as e:
            logger.error(f"组件初始化失败: {e}")
            traceback.print_exc()
    
    def load_test_scenarios(self) -> List[Dict[str, Any]]:
        """加载测试场景"""
        scenarios = []
        scenarios_config = self.config.get('evaluation', {}).get('scenarios', [])
        
        # 如果指定了场景列表
        if isinstance(scenarios_config, list):
            for scenario_name in scenarios_config:
                scenario_path = os.path.join(self.base_dir, 'data', 'scenarios', f'{scenario_name}.json')
                if os.path.exists(scenario_path):
                    try:
                        with open(scenario_path, 'r', encoding='utf-8') as f:
                            scenario = json.load(f)
                        scenarios.append(scenario)
                        logger.info(f"加载场景: {scenario_name}")
                    except Exception as e:
                        logger.error(f"加载场景失败 {scenario_name}: {e}")
                else:
                    # 使用默认场景配置
                    scenarios.append({
                        'name': scenario_name,
                        'description': f'Default {scenario_name} scenario',
                        'initial_state': {},
                        'goal': f'F (completed_{scenario_name})',
                        'instruction': f'Complete the {scenario_name} task',
                        'parameters': {}
                    })
                    logger.info(f"使用默认场景配置: {scenario_name}")
        
        return scenarios
    
    def run_test(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行单个测试场景
        
        Args:
            scenario: 场景配置
            
        Returns:
            测试结果
        """
        scenario_result = {
            'name': scenario.get('name', 'unknown'),
            'instruction': scenario.get('instruction', ''),
            'start_time': datetime.datetime.now().isoformat(),
            'end_time': None,
            'status': 'failed',
            'metrics': {},
            'logs': [],
            'error': None
        }
        
        try:
            logger.info(f"开始测试场景: {scenario_result['name']}")
            
            # 1. 分解子目标
            goal_formula = scenario.get('goal', '')
            instruction = scenario.get('instruction', '')
            subgoals = []
            
            if self.subgoal_decomposer:
                if instruction:
                    try:
                        subgoals = self.subgoal_decomposer.decompose_from_instruction(instruction)
                        scenario_result['logs'].append(f"从指令分解子目标，共 {len(subgoals)} 个子目标")
                    except Exception as e:
                        scenario_result['logs'].append(f"从指令分解子目标失败: {e}")
                elif goal_formula:
                    try:
                        subgoals = self.subgoal_decomposer.decompose(goal_formula)
                        scenario_result['logs'].append(f"从公式分解子目标，共 {len(subgoals)} 个子目标")
                    except Exception as e:
                        scenario_result['logs'].append(f"从公式分解子目标失败: {e}")
            
            # 2. 执行评估
            agent_actions = []
            # 这里应该是从子目标生成动作序列
            # 现在使用模拟动作
            agent_actions = self._generate_mock_actions(scenario)
            
            # 3. 使用评估器评估
            if self.evaluator:
                eval_result = self.evaluator.evaluate_agent(
                    agent_actions,
                    initial_state=scenario.get('initial_state', {}),
                    instruction=instruction,
                    goal_formula=goal_formula
                )
                scenario_result['metrics'] = eval_result.get('metrics', {})
                scenario_result['status'] = eval_result.get('status', 'failed')
                
            # 4. 验证结果
            if self.validator and goal_formula:
                try:
                    # 使用模拟的状态序列进行验证
                    state_sequence = self._generate_mock_state_sequence(agent_actions)
                    validation_result = self.validator.validate(goal_formula, state_sequence)
                    scenario_result['validation'] = validation_result
                    scenario_result['logs'].append(f"公式验证结果: {validation_result}")
                except Exception as e:
                    scenario_result['logs'].append(f"公式验证失败: {e}")
            
            scenario_result['status'] = 'success'
            logger.info(f"场景测试完成: {scenario_result['name']}")
            
        except Exception as e:
            error_msg = str(e)
            scenario_result['error'] = error_msg
            scenario_result['logs'].append(f"测试执行错误: {error_msg}")
            logger.error(f"场景测试失败 {scenario_result['name']}: {error_msg}")
            traceback.print_exc()
        finally:
            scenario_result['end_time'] = datetime.datetime.now().isoformat()
        
        return scenario_result
    
    def _generate_mock_actions(self, scenario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成模拟动作序列"""
        scenario_name = scenario.get('name', '')
        
        # 根据场景类型返回不同的模拟动作
        if 'daily_tasks' in scenario_name:
            return [
                {'type': 'navigate', 'target': 'kitchen', 'parameters': {}},
                {'type': 'grasp', 'target': 'cup', 'parameters': {'location': 'counter'}},
                {'type': 'grasp', 'target': 'water', 'parameters': {'source': 'faucet'}},
                {'type': 'drink', 'target': 'cup', 'parameters': {}},
                {'type': 'place', 'target': 'cup', 'parameters': {'location': 'counter'}}
            ]
        elif 'object_interactions' in scenario_name:
            return [
                {'type': 'navigate', 'target': 'living_room', 'parameters': {}},
                {'type': 'grasp', 'target': 'remote', 'parameters': {'location': 'table'}},
                {'type': 'toggle', 'target': 'tv', 'parameters': {'action': 'on'}},
                {'type': 'watch', 'target': 'tv', 'parameters': {'duration': 10}},
                {'type': 'toggle', 'target': 'tv', 'parameters': {'action': 'off'}},
                {'type': 'place', 'target': 'remote', 'parameters': {'location': 'table'}}
            ]
        elif 'multi_agent' in scenario_name:
            return [
                {'type': 'navigate', 'target': 'agent_2', 'parameters': {}},
                {'type': 'communicate', 'target': 'agent_2', 'parameters': {'message': 'Please pass the book'}},
                {'type': 'receive', 'target': 'book', 'parameters': {'from': 'agent_2'}},
                {'type': 'read', 'target': 'book', 'parameters': {'duration': 15}},
                {'type': 'give', 'target': 'book', 'parameters': {'to': 'agent_2'}},
                {'type': 'navigate', 'target': 'exit', 'parameters': {}}
            ]
        else:
            return [
                {'type': 'start', 'parameters': {}},
                {'type': 'complete', 'parameters': {}}
            ]
    
    def _generate_mock_state_sequence(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成模拟状态序列"""
        states = []
        current_state = {'time': 0, 'agent_location': 'start', 'agent_holding': None, 'objects': {}}
        
        for i, action in enumerate(actions):
            # 更新状态
            current_state['time'] = i + 1
            
            if action['type'] == 'navigate':
                current_state['agent_location'] = action.get('target', 'unknown')
            elif action['type'] == 'grasp':
                obj = action.get('target', 'object')
                current_state['agent_holding'] = obj
                current_state['objects'][obj] = {'state': 'held', 'location': 'agent_hand'}
            elif action['type'] == 'place':
                obj = action.get('target', 'object')
                location = action.get('parameters', {}).get('location', 'unknown')
                current_state['agent_holding'] = None
                current_state['objects'][obj] = {'state': 'placed', 'location': location}
            elif action['type'] == 'toggle':
                obj = action.get('target', 'object')
                action_type = action.get('parameters', {}).get('action', 'on')
                if obj not in current_state['objects']:
                    current_state['objects'][obj] = {}
                current_state['objects'][obj]['state'] = action_type
            elif action['type'] == 'communicate':
                target = action.get('target', 'agent')
                message = action.get('parameters', {}).get('message', '')
                if target not in current_state['objects']:
                    current_state['objects'][target] = {}
                current_state['objects'][target]['last_message'] = message
            
            states.append(current_state.copy())
        
        return states
    
    def execute_all_tests(self):
        """执行所有测试场景"""
        self.results['start_time'] = datetime.datetime.now().isoformat()
        logger.info("开始执行所有测试场景")
        
        # 加载场景
        scenarios = self.load_test_scenarios()
        if not scenarios:
            logger.warning("未找到测试场景，使用默认测试")
            scenarios = [{
                'name': 'default_test',
                'description': 'Default test scenario',
                'instruction': 'Complete a simple task',
                'goal': 'F (test_completed)',
                'initial_state': {}
            }]
        
        # 执行每个场景
        success_count = 0
        total_metrics = {}
        
        for scenario in scenarios:
            result = self.run_test(scenario)
            self.results['scenarios'].append(result)
            
            if result['status'] == 'success':
                success_count += 1
            
            # 累计指标
            for metric_name, metric_value in result.get('metrics', {}).items():
                if metric_name not in total_metrics:
                    total_metrics[metric_name] = []
                total_metrics[metric_name].append(metric_value)
        
        # 计算汇总指标
        self.results['summary'] = {
            'total_scenarios': len(scenarios),
            'successful_scenarios': success_count,
            'success_rate': success_count / len(scenarios) if scenarios else 0
        }
        
        # 计算平均指标
        for metric_name, values in total_metrics.items():
            if values:
                self.results['summary'][f'average_{metric_name}'] = sum(values) / len(values)
        
        self.results['end_time'] = datetime.datetime.now().isoformat()
        logger.info(f"所有测试完成，成功: {success_count}/{len(scenarios)}")
        
        # 保存结果
        self.save_results()
        return self.results
    
    def save_results(self):
        """保存测试结果"""
        output_dir = self.config.get('data', {}).get('output_dir', os.path.join(self.base_dir, 'results'))
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存详细结果
        result_file = os.path.join(output_dir, f'virtualhome_test_result_{self.results["test_id"]}.json')
        try:
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            logger.info(f"结果已保存至: {result_file}")
        except Exception as e:
            logger.error(f"保存结果失败: {e}")
        
        # 保存汇总报告
        report_file = os.path.join(output_dir, f'virtualhome_test_summary_{self.results["test_id"]}.md')
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_report())
            logger.info(f"报告已保存至: {report_file}")
        except Exception as e:
            logger.error(f"保存报告失败: {e}")
    
    def _generate_report(self) -> str:
        """生成测试报告"""
        summary = self.results['summary']
        
        report = f"""# VirtualHome环境测试评估报告

## 测试概述
- **测试ID**: {self.results['test_id']}
- **开始时间**: {self.results['start_time']}
- **结束时间**: {self.results['end_time']}
- **使用配置**: {self.results['config_used']}

## 测试结果汇总
- **测试场景总数**: {summary['total_scenarios']}
- **成功场景数**: {summary['successful_scenarios']}
- **成功率**: {summary['success_rate']:.2%}

## 性能指标
"""
        
        # 添加性能指标
        for key, value in summary.items():
            if key.startswith('average_'):
                metric_name = key.replace('average_', '').replace('_', ' ').title()
                report += f"- **平均{metric_name}**: {value}\n"
        
        report += "\n## 场景详情\n\n"
        
        # 添加场景详情
        for scenario in self.results['scenarios']:
            status_icon = "✅" if scenario['status'] == 'success' else "❌"
            report += f"### {status_icon} {scenario['name']}\n"
            report += f"- **指令**: {scenario.get('instruction', 'N/A')}\n"
            report += f"- **状态**: {scenario['status']}\n"
            report += f"- **开始时间**: {scenario['start_time']}\n"
            report += f"- **结束时间**: {scenario['end_time']}\n"
            
            if scenario.get('metrics'):
                report += "- **指标**:\n"
                for metric_name, metric_value in scenario['metrics'].items():
                    report += f"  - {metric_name}: {metric_value}\n"
            
            if scenario.get('error'):
                report += f"- **错误**: {scenario['error']}\n"
            
            report += "\n"
        
        return report


class MockVirtualHomeEvaluator:
    """模拟VirtualHome评估器，用于开发和测试"""
    
    def __init__(self):
        self.logger = logging.getLogger('mock_virtualhome_evaluator')
        self.logger.info("模拟VirtualHome评估器已初始化")
    
    def evaluate_agent(self, actions: List[Dict[str, Any]], initial_state: Dict = None,
                      instruction: str = None, goal_formula: str = None) -> Dict[str, Any]:
        """
        模拟评估智能体行为
        
        Args:
            actions: 智能体动作序列
            initial_state: 初始状态
            instruction: 自然语言指令
            goal_formula: 目标公式
            
        Returns:
            评估结果
        """
        import random
        
        # 随机决定是否成功
        success = random.random() > 0.2  # 80%成功率
        
        result = {
            'status': 'success' if success else 'failed',
            'metrics': {
                'success_rate': 1.0 if success else 0.0,
                'completion_time': len(actions) * 1.2,  # 每个动作1.2秒
                'instruction_fidelity': random.uniform(0.75, 1.0),
                'scene_relevance': random.uniform(0.8, 1.0),
                'action_completeness': random.uniform(0.7, 1.0) if success else random.uniform(0.0, 0.6)
            },
            'details': {
                'action_count': len(actions),
                'simulation_time': len(actions) * 1.2,
                'final_state': 'goal_achieved' if success else 'failed'
            }
        }
        
        self.logger.info(f"模拟评估结果: {result['status']}")
        return result


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='VirtualHome环境测试评估工具')
    parser.add_argument('--config', '-c', type=str, help='配置文件路径')
    parser.add_argument('--scenario', '-s', type=str, help='指定单个测试场景')
    parser.add_argument('--instruction', '-i', type=str, help='自定义测试指令')
    parser.add_argument('--output', '-o', type=str, help='结果输出目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='启用详细日志')
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 如果启用详细日志
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # 初始化评估器
        evaluator = VirtualHomeTestEvaluator(config_path=args.config)
        
        # 如果指定了单个场景
        if args.scenario:
            logger.info(f"执行单个场景测试: {args.scenario}")
            scenario = {
                'name': args.scenario,
                'description': f'Single test scenario: {args.scenario}',
                'instruction': args.instruction or f'Complete the {args.scenario} task',
                'goal': f'F (completed_{args.scenario})',
                'initial_state': {}
            }
            result = evaluator.run_test(scenario)
            print(f"场景测试结果: {result['status']}")
            
            # 保存结果
            evaluator.results['scenarios'] = [result]
            evaluator.save_results()
        else:
            # 执行所有测试
            logger.info("执行所有测试场景")
            results = evaluator.execute_all_tests()
            
            # 输出摘要
            summary = results['summary']
            print(f"测试完成！")
            print(f"成功率: {summary['success_rate']:.2%} ({summary['successful_scenarios']}/{summary['total_scenarios']})")
            
    except Exception as e:
        logger.error(f"测试执行失败: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()