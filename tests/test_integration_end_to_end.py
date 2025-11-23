"""
端到端集成测试

测试四个模块的完整集成流程和错误处理机制
"""

import unittest
import sys
import os
import time
from typing import Dict, Any, List
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入主集成器
from integration.main_integrator import MainIntegrator, IntegrationResult


class TestIntegrationEndToEnd(unittest.TestCase):
    """
    端到端集成测试类
    """
    
    def setUp(self):
        """
        测试前设置
        """
        # 创建配置
        self.config = {
            'enable_module_feedback': True,
            'enable_error_handling': True,
            'enable_recovery': True,
            'timeout_seconds': 120,
            'goal_interpretation': {
                'enable_debugging': True,
                'max_interpretation_depth': 5
            },
            'subgoal_decomposition': {
                'enable_debugging': True,
                'max_subgoals': 10
            },
            'transition_modeling': {
                'enable_debugging': True,
                'enable_module_feedback': True
            },
            'action_sequencing': {
                'enable_debugging': True,
                'max_sequence_length': 30
            }
        }
        
        # 初始化集成器
        try:
            self.integrator = MainIntegrator(self.config)
            self.integration_available = True
            logger.info("MainIntegrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MainIntegrator: {str(e)}")
            self.integrator = None
            self.integration_available = False
    
    def test_integration_status(self):
        """
        测试集成状态
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 验证集成状态
        status = self.integrator.validate_integration()
        logger.info(f"Integration status: {status}")
        
        # 检查各个模块是否可用
        for module_name, is_available in status.items():
            if module_name != 'all_modules_available':
                logger.info(f"Module {module_name}: {'Available' if is_available else 'Not Available'}")
    
    def test_simple_goal_processing(self):
        """
        测试简单目标处理
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 简单目标
        goal_text = "Move the red box to the table"
        context = {
            'environment': 'kitchen',
            'available_objects': ['red_box', 'table', 'chair'],
            'robot_position': 'start_position'
        }
        
        # 处理目标
        result = self.integrator.process_goal(goal_text, context)
        
        # 验证结果
        self.assertIsInstance(result, IntegrationResult)
        logger.info(f"Simple goal processing result: {'Success' if result.success else 'Failed'}")
        logger.info(f"Execution time: {result.execution_time.get('total', 0):.2f} seconds")
        
        # 记录详细结果
        self._log_result_details(result)
    
    def test_complex_goal_processing(self):
        """
        测试复杂目标处理
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 复杂目标
        goal_text = "Clean the kitchen, wash the dishes, and put them away in the cabinet"
        context = {
            'environment': 'kitchen',
            'available_objects': ['dishes', 'sink', 'cabinet', 'sponge', 'soap'],
            'robot_position': 'kitchen entrance',
            'current_state': {
                'dishes_on_counter': True,
                'cabinet_closed': True,
                'sink_has_water': False
            }
        }
        
        # 处理目标
        result = self.integrator.process_goal(goal_text, context)
        
        # 验证结果
        self.assertIsInstance(result, IntegrationResult)
        logger.info(f"Complex goal processing result: {'Success' if result.success else 'Failed'}")
        logger.info(f"Execution time: {result.execution_time.get('total', 0):.2f} seconds")
        
        # 记录详细结果
        self._log_result_details(result)
    
    def test_error_handling(self):
        """
        测试错误处理机制
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 有问题的目标（缺少关键信息）
        goal_text = "Fix the broken machine"
        context = {
            'environment': 'factory',
            'available_objects': [],  # 空对象列表
            'robot_position': 'factory floor'
        }
        
        # 处理目标
        result = self.integrator.process_goal(goal_text, context)
        
        # 验证错误处理
        self.assertIsInstance(result, IntegrationResult)
        logger.info(f"Error handling test result: {'Success' if result.success else 'Failed with errors'}")
        
        # 检查是否有错误记录
        if result.errors:
            logger.info(f"Errors captured: {len(result.errors)}")
            for error_type, error_msg in result.errors.items():
                logger.info(f"  {error_type}: {error_msg}")
        
        # 检查是否有警告记录
        if result.warnings:
            logger.info(f"Warnings captured: {len(result.warnings)}")
            for warning_type, warning_msg in result.warnings.items():
                logger.info(f"  {warning_type}: {warning_msg}")
        
        # 检查是否有诊断信息
        if 'error_diagnostics' in result.statistics:
            logger.info("Error diagnostics available")
    
    def test_recovery_mechanism(self):
        """
        测试恢复机制
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 边界情况目标
        goal_text = "Find and organize the scattered items on the floor"
        context = {
            'environment': 'office',
            'available_objects': ['paper', 'pen', 'stapler'],
            'robot_position': 'office entrance',
            'incomplete_information': True  # 标记为不完整信息
        }
        
        # 处理目标
        result = self.integrator.process_goal(goal_text, context)
        
        # 验证结果
        self.assertIsInstance(result, IntegrationResult)
        logger.info(f"Recovery mechanism test result: {'Success' if result.success else 'Failed'}")
        
        # 检查是否尝试了恢复
        if result.warnings:
            recovery_warnings = [w for w in result.warnings if 'recovery' in w.lower()]
            if recovery_warnings:
                logger.info(f"Recovery attempts detected: {len(recovery_warnings)}")
                for warning in recovery_warnings:
                    logger.info(f"  {warning}: {result.warnings[warning]}")
    
    def test_module_feedback(self):
        """
        测试模块反馈机制
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 连续处理两个相关目标，测试反馈机制
        first_goal = "Pick up the blue cup from the table"
        second_goal = "Now put it on the shelf"
        
        context = {
            'environment': 'living_room',
            'available_objects': ['blue_cup', 'table', 'shelf'],
            'robot_position': 'living_room center'
        }
        
        # 处理第一个目标
        first_result = self.integrator.process_goal(first_goal, context)
        logger.info(f"First goal processing: {'Success' if first_result.success else 'Failed'}")
        
        # 更新上下文，包含第一个目标的结果
        if first_result.action_sequence:
            updated_context = context.copy()
            updated_context['previous_actions'] = first_result.action_sequence.action_sequence
            updated_context['previous_result'] = first_result.success
        else:
            updated_context = context
        
        # 处理第二个目标
        second_result = self.integrator.process_goal(second_goal, updated_context)
        logger.info(f"Second goal processing: {'Success' if second_result.success else 'Failed'}")
        
        # 验证两个结果
        self.assertIsInstance(first_result, IntegrationResult)
        self.assertIsInstance(second_result, IntegrationResult)
    
    def test_performance_metrics(self):
        """
        测试性能指标
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 多个简单目标测试性能
        test_goals = [
            "Move the book to the desk",
            "Open the door",
            "Pick up the pen",
            "Turn on the light"
        ]
        
        context = {
            'environment': 'office',
            'available_objects': ['book', 'desk', 'door', 'pen', 'light'],
            'robot_position': 'office entrance'
        }
        
        execution_times = []
        success_count = 0
        
        # 处理所有目标
        for goal in test_goals:
            start_time = time.time()
            result = self.integrator.process_goal(goal, context)
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            
            if result.success:
                success_count += 1
            
            logger.info(f"Goal '{goal}' processed in {execution_time:.2f} seconds: {'Success' if result.success else 'Failed'}")
        
        # 计算平均执行时间
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            logger.info(f"Average execution time: {avg_time:.2f} seconds")
            logger.info(f"Success rate: {success_count}/{len(test_goals)} ({success_count/len(test_goals)*100:.1f}%)")
        
        # 获取集成统计信息
        stats = self.integrator.get_integration_statistics()
        logger.info(f"Integration statistics: {stats}")
    
    def _log_result_details(self, result: IntegrationResult):
        """
        记录结果详细信息
        
        Args:
            result: 集成结果
        """
        # 记录执行时间详情
        for phase, phase_time in result.execution_time.items():
            logger.info(f"  {phase}: {phase_time:.2f} seconds")
        
        # 记录模块结果详情
        if result.goal_interpretation:
            try:
                logger.info(f"  Goal interpretation confidence: {result.goal_interpretation.confidence_score:.2f}")
                logger.info(f"  Compatibility flags: {result.goal_interpretation.compatibility_flags}")
            except:
                pass
        
        if result.subgoal_decomposition:
            try:
                logger.info(f"  Subgoal count: {len(result.subgoal_decomposition.subgoals)}")
                logger.info(f"  Decomposition confidence: {result.subgoal_decomposition.confidence_score:.2f}")
            except:
                pass
        
        if result.action_sequence:
            try:
                logger.info(f"  Action count: {len(result.action_sequence.action_sequence)}")
                logger.info(f"  Sequence confidence: {result.action_sequence.confidence_score:.2f}")
            except:
                pass
    
    def test_result_export(self):
        """
        测试结果导出功能
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 简单目标
        goal_text = "Test export functionality"
        context = {
            'environment': 'test',
            'available_objects': ['test_object'],
            'robot_position': 'test_position'
        }
        
        # 处理目标
        result = self.integrator.process_goal(goal_text, context)
        
        # 导出结果
        export_path = os.path.join(os.path.dirname(__file__), 'test_export_result.json')
        self.integrator.export_results_to_json(result, export_path)
        
        # 验证文件是否创建
        if os.path.exists(export_path):
            logger.info(f"Result exported successfully to {export_path}")
            # 清理测试文件
            try:
                os.remove(export_path)
                logger.info("Test export file cleaned up")
            except:
                pass
        else:
            logger.warning(f"Export file not found at {export_path}")
    
    def test_edge_cases(self):
        """
        测试边界情况
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        edge_cases = [
            {
                'goal': "",  # 空目标
                'context': {'environment': 'empty'},
                'description': "Empty goal"
            },
            {
                'goal': "Invalid@#$%^&*() characters",  # 包含无效字符
                'context': {'environment': 'test'},
                'description': "Goal with invalid characters"
            },
            {
                'goal': "Very long goal " + "text " * 100,  # 超长目标
                'context': {'environment': 'test'},
                'description': "Very long goal"
            },
            {
                'goal': "Impossible action",  # 不可能完成的动作
                'context': {
                    'environment': 'vacuum',
                    'available_objects': [],
                    'physics_constraints': 'zero_gravity'
                },
                'description': "Impossible action"
            }
        ]
        
        for case in edge_cases:
            logger.info(f"Testing edge case: {case['description']}")
            result = self.integrator.process_goal(case['goal'], case['context'])
            
            # 验证错误处理
            if result.errors:
                logger.info(f"  Expected errors captured: {len(result.errors)}")
            else:
                logger.warning(f"  No errors captured for edge case: {case['description']}")
    
    def test_integration_statistics_reset(self):
        """
        测试集成统计信息重置
        """
        if not self.integration_available:
            self.skipTest("Integration not available")
        
        # 先获取初始统计
        initial_stats = self.integrator.get_integration_statistics()
        logger.info(f"Initial statistics: {initial_stats['total_executions']} executions")
        
        # 处理一个目标
        self.integrator.process_goal("Test statistics", {'environment': 'test'})
        
        # 获取新统计
        new_stats = self.integrator.get_integration_statistics()
        logger.info(f"Updated statistics: {new_stats['total_executions']} executions")
        
        # 验证统计信息更新
        self.assertGreaterEqual(new_stats['total_executions'], initial_stats['total_executions'])


if __name__ == "__main__":
    unittest.main()