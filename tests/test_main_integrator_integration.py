#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Integration Test Suite for Main Integrator Interface
Tests the integration of all four modules through the MainIntegrator interface
"""

import pytest
import sys
import os
import time
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the MainIntegrator
from integration.main_integrator import MainIntegrator, IntegrationResult


class TestMainIntegratorInterface:
    """
    Test class for the MainIntegrator interface
    """
    
    @pytest.fixture(scope="class")
    def integrator(self):
        """
        Fixture to create a MainIntegrator instance
        """
        config = {
            'enable_module_feedback': True,
            'enable_error_handling': True,
            'enable_recovery': True,
            'timeout_seconds': 60,
            'goal_interpretation': {
                'enable_debugging': False,
                'max_interpretation_depth': 5
            },
            'subgoal_decomposition': {
                'enable_debugging': False,
                'max_subgoals': 10
            },
            'transition_modeling': {
                'enable_debugging': False,
                'enable_module_feedback': True
            },
            'action_sequencing': {
                'enable_debugging': False,
                'max_sequence_length': 20
            }
        }
        
        return MainIntegrator(config)
    
    def test_integrator_initialization(self, integrator):
        """
        Test that the MainIntegrator initializes correctly
        """
        assert integrator is not None, "MainIntegrator initialization failed"
        
        # Verify integration status
        status = integrator.validate_integration()
        assert isinstance(status, Dict), "Integration status should be a dictionary"
        assert 'all_modules_available' in status, "Integration status missing 'all_modules_available' key"
    
    def test_simple_goal_processing(self, integrator):
        """
        Test processing of a simple natural language goal
        """
        goal_text = "Move the red box to the table"
        context = {
            'environment': 'kitchen',
            'available_objects': ['red_box', 'table', 'chair'],
            'robot_position': 'start_position'
        }
        
        result = integrator.process_goal(goal_text, context)
        assert isinstance(result, IntegrationResult), "Result should be an IntegrationResult object"
        assert result.success is not None, "Result success status should be set"
        assert result.execution_time is not None, "Result should include execution time"
        
    def test_complex_goal_processing(self, integrator):
        """
        Test processing of a complex natural language goal
        """
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
        
        result = integrator.process_goal(goal_text, context)
        
        assert isinstance(result, IntegrationResult), "Result should be an IntegrationResult object"
        assert result.success is not None, "Result success status should be set"
    
    def test_empty_goal_input(self, integrator):
        """
        Test handling of empty goal input
        """
        goal_text = ""
        context = {
            'environment': 'kitchen',
            'available_objects': ['red_box', 'table'],
            'robot_position': 'start_position'
        }
        
        result = integrator.process_goal(goal_text, context)
        
        assert isinstance(result, IntegrationResult), "Result should be an IntegrationResult object"
    
    def test_invalid_context(self, integrator):
        """
        Test handling of invalid context input
        """
        goal_text = "Move the red box to the table"
        context = None
        
        result = integrator.process_goal(goal_text, context)
        
        assert isinstance(result, IntegrationResult)
        "Result should be an IntegrationResult object"
    
    def test_multi_goal_processing(self, integrator):
        """
        Test processing multiple goals sequentially
        """
        goals = [
            "Move the red box to the table",
            "Clean the window",
            "Turn off the lights"
        ]
        
        context = {
            'environment': 'living_room',
            'available_objects': ['red_box', 'table', 'window', 'light_switch'],
            'robot_position': 'start_position'
        }
        
        for goal_text in goals:
            result = integrator.process_goal(goal_text, context)
            assert isinstance(result, IntegrationResult), f"Result for goal '{goal_text}' should be an IntegrationResult object"
    
    def test_integration_performance(self, integrator):
        """
        Test performance of the integration interface
        """
        goal_text = "Move the red box to the table"
        context = {
            'environment': 'kitchen',
            'available_objects': ['red_box', 'table', 'chair'],
            'robot_position': 'start_position'
        }
        
        start_time = time.time()
        result = integrator.process_goal(goal_text, context)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert isinstance(result, IntegrationResult), "Result should be an IntegrationResult object"
        assert execution_time < 10.0, f"Integration should complete in under 10 seconds, took {execution_time:.2f} seconds"


class TestIntegrationEdgeCases:
    """
    Test edge cases for the integration interface
    """
    
    @pytest.fixture(scope="class")
    def integrator(self):
        """
        Fixture to create a MainIntegrator instance for edge case testing
        """
        config = {
            'enable_module_feedback': True,
            'enable_error_handling': True,
            'enable_recovery': True,
            'timeout_seconds': 30,
            'goal_interpretation': {
                'enable_debugging': False,
                'max_interpretation_depth': 3
            },
            'subgoal_decomposition': {
                'enable_debugging': False,
                'max_subgoals': 5
            },
            'transition_modeling': {
                'enable_debugging': False,
                'enable_module_feedback': False
            },
            'action_sequencing': {
                'enable_debugging': False,
                'max_sequence_length': 10
            }
        }
        
        return MainIntegrator(config)
    
    def test_long_goal_text(self, integrator):
        """
        Test processing of extremely long goal text
        """
        long_goal = "Move the " + "very " * 50 + "heavy " + "red " * 20 + "box to the " + "large " * 30 + "wooden table in the " + "bright " * 40 + "living room"
        context = {
            'environment': 'living_room',
            'available_objects': ['box', 'table'],
            'robot_position': 'start_position'
        }
        
        result = integrator.process_goal(long_goal, context)
        assert isinstance(result, IntegrationResult), "Result should be an IntegrationResult object"
    
    def test_unsupported_goal(self, integrator):
        """
        Test processing of an unsupported goal type
        """
        goal_text = "Fly to the moon and collect samples"
        context = {
            'environment': 'earth',
            'available_objects': [],
            'robot_position': 'launch_pad'
        }
        
        result = integrator.process_goal(goal_text, context)
        assert isinstance(result, IntegrationResult), "Result should be an IntegrationResult object"


def run_integration_tests():
    """
    Run all integration tests manually
    """
    import unittest
    
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestMainIntegratorInterface))
    test_suite.addTest(unittest.makeSuite(TestIntegrationEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
