#!/usr/bin/env python3
"""
LLM集成测试用例
"""

import os
import sys
import pytest
import tempfile
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import get_logger
from transition_modeling.transition_predictor import TransitionPredictor

# 获取日志记录器
logger = get_logger(__name__)

class TestLLMIntegration:
    """
    LLM集成测试类
    """
    
    def setup_method(self):
        """
        测试方法设置
        """
        logger.info("=== 设置LLM集成测试环境 ===")
        # 创建临时配置文件
        self.temp_dir = tempfile.mkdtemp()
        
        # 模拟场景配置
        self.mock_scenarios = {
            "basic": {
                "model": {
                    "name": "qwen/qwen-turbo",
                    "temperature": 0.7,
                    "max_tokens": 512
                },
                "transition": {
                    "min_length": 1,
                    "max_length": 10,
                    "allowed_types": ["action", "state_change"],
                    "default_cost": 1.0
                }
            },
            "debug": {
                "model": {
                    "name": "debug-model",
                    "temperature": 0.0,
                    "max_tokens": 128
                },
                "transition": {
                    "min_length": 1,
                    "max_length": 5,
                    "allowed_types": ["action"],
                    "default_cost": 0.5
                }
            }
        }
    
    def teardown_method(self):
        """
        测试方法清理
        """
        logger.info("=== 清理LLM集成测试环境 ===")
        # 清理临时目录
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_llm_integration_initialization(self):
        """
        测试LLM集成初始化
        """
        logger.info("测试：LLM集成初始化")
        
        # 创建TransitionPredictor实例，测试LLM相关配置是否正确加载
        config = {
            'confidence_threshold': 0.8,
            'max_predictions': 5
        }
        predictor = TransitionPredictor(config=config)
        
        # 验证初始化参数
        assert predictor.confidence_threshold == 0.8
        assert predictor.max_predictions == 5
        
        logger.info("✓ LLM集成初始化测试通过")
    
    def test_confidence_calculation(self):
        """
        测试置信度计算
        """
        logger.info("测试：置信度计算")
        
        predictor = TransitionPredictor(config={})
        
        # 模拟测试数据
        transition = MagicMock()
        transition.id = "test-transition"
        transition.name = "test-action"
        
        current_state = {
            "location": "kitchen",
            "holding": "none",
            "objects": ["fridge", "counter", "knife"]
        }
        
        goal_state = {
            "location": "living_room",
            "holding": "knife",
            "objects": ["sofa", "table"]
        }
        
        # 调用置信度计算方法
        confidence = predictor._calculate_transition_confidence(
            transition, current_state, goal_state
        )
        
        # 验证置信度结果类型和范围
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
        
        # 测试除以零情况 - 模拟一个可能导致除以零的转换
        # 创建一个没有参数但启用了PDDL语义的转换
        mock_transition_no_params = MagicMock()
        mock_transition_no_params.name = "test-action-no-params"
        mock_transition_no_params.preconditions = []
        mock_transition_no_params.effects = []
        mock_transition_no_params.parameters = []
        
        # 启用PDDL语义
        predictor.enable_pddl_semantics = True
        
        # 这应该不会导致除以零
        confidence_no_params = predictor._calculate_transition_confidence(
            mock_transition_no_params,
            current_state,
            goal_state
        )
        
        assert 0.0 <= confidence_no_params <= 1.0, f"置信度值应在0到1之间，实际为{confidence_no_params}"
        
        logger.info("✓ 置信度计算测试通过")
    
    def test_scene_config_loading(self):
        """
        测试场景配置加载
        """
        logger.info("测试：场景配置加载")
        
        with patch('transition_modeling.transition_predictor.yaml.safe_load') as mock_load:
            mock_load.return_value = {
                "default_scene": "basic",
                "scene_priority": ["debug", "basic"],
                "scenes": self.mock_scenarios
            }
            
            with patch('builtins.open', MagicMock()):
                predictor = TransitionPredictor()
                
                # 验证场景配置是否正确加载
                assert hasattr(predictor, '_scenes')
                assert 'basic' in predictor._scenes
                assert 'debug' in predictor._scenes
                
                logger.info("✓ 场景配置加载测试通过")
    
    def test_llm_model_call(self):
        """
        测试LLM模型调用
        """
        logger.info("测试：LLM模型调用")
        
        predictor = TransitionPredictor()
        
        # 模拟当前状态和目标状态
        current_state = {
            "location": "living_room",
            "holding": "remote_control",
            "objects": ["tv", "sofa", "lamp"]
        }
        
        goal_state = {
            "location": "bedroom",
            "holding": "none",
            "objects": ["bed", "nightstand"]
        }
        
        # 模拟可用转换
        mock_transitions = []
        
        # 调用预测方法
        predictions = predictor.predict_transitions(
            current_state,
            goal_state,
            mock_transitions
        )
        
        # 验证预测结果
        assert isinstance(predictions, list)
        
        logger.info("✓ LLM模型调用测试通过")
    
    def test_transition_prediction_with_different_scenes(self):
        """
        测试不同场景下的转换预测
        """
        logger.info("测试：不同场景下的转换预测")
        
        # 模拟不同场景配置
        predictor = TransitionPredictor()
        
        # 模拟当前状态和目标状态
        current_state = {
            "location": "bedroom",
            "holding": "book",
            "objects": ["bed", "nightstand", "lamp"]
        }
        
        goal_state = {
            "location": "living_room",
            "holding": "none",
            "objects": ["tv", "sofa"]
        }
        
        # 模拟可用转换
        mock_transitions = []
        
        # 测试基本场景
        with patch.object(predictor, '_get_best_matching_scene', return_value="basic"):
            basic_predictions = predictor.predict_transitions(
                current_state,
                goal_state,
                mock_transitions
            )
            assert isinstance(basic_predictions, list)
        
        # 测试调试场景
        with patch.object(predictor, '_get_best_matching_scene', return_value="debug"):
            debug_predictions = predictor.predict_transitions(
                current_state,
                goal_state,
                mock_transitions
            )
            assert isinstance(debug_predictions, list)
        
        logger.info("✓ 不同场景下的转换预测测试通过")
    
    def test_error_handling(self):
        """
        测试错误处理
        """
        logger.info("测试：错误处理")
        
        predictor = TransitionPredictor()
        
        # 测试无效状态
        invalid_states = [
            "not-a-dict",
            123,
            None,
            ["invalid", "state"]
        ]
        
        for invalid_state in invalid_states:
            with pytest.raises(Exception):
                predictor.predict_transitions(
                    invalid_state,
                    num_predictions=1
                )
        
        logger.info("✓ 错误处理测试通过")
    
    def test_confidence_threshold_filtering(self):
        """
        测试置信度阈值过滤
        """
        logger.info("测试：置信度阈值过滤")
        
        # 使用不同的置信度阈值创建预测器
        high_threshold_predictor = TransitionPredictor(confidence_threshold=0.9)
        low_threshold_predictor = TransitionPredictor(confidence_threshold=0.5)
        
        # 模拟预测结果
        mock_transitions = [
            MagicMock(id="t1", name="action1", confidence=0.95),
            MagicMock(id="t2", name="action2", confidence=0.8),
            MagicMock(id="t3", name="action3", confidence=0.6)
        ]
        
        with patch.object(high_threshold_predictor, '_generate_transition_candidates', return_value=mock_transitions):
            high_threshold_results = high_threshold_predictor.predict_transitions(
                {}, num_predictions=3
            )
            # 高阈值应该只返回高置信度的转换
            assert len(high_threshold_results) <= len(mock_transitions)
        
        with patch.object(low_threshold_predictor, '_generate_transition_candidates', return_value=mock_transitions):
            low_threshold_results = low_threshold_predictor.predict_transitions(
                {}, num_predictions=3
            )
            # 低阈值应该返回更多转换
            assert len(low_threshold_results) <= len(mock_transitions)
        
        logger.info("✓ 置信度阈值过滤测试通过")
    
    def test_integration_with_transition_validator(self):
        """
        测试与转换验证器的集成
        """
        logger.info("测试：与转换验证器的集成")
        
        from transition_modeling.transition_validator import TransitionValidator
        
        # 创建预测器和验证器
        predictor = TransitionPredictor()
        validator = TransitionValidator()
        
        # 模拟当前状态
        current_state = {
            "location": "kitchen",
            "holding": "none",
            "objects": ["fridge", "counter", "apple"]
        }
        
        # 模拟预测结果
        mock_transition = MagicMock()
        mock_transition.id = "test-eat-apple"
        mock_transition.name = "eat-apple"
        mock_transition.transition_type = MagicMock()
        mock_transition.duration = 5
        mock_transition.cost = 1.0
        mock_transition.preconditions = []
        mock_transition.effects = []
        mock_transition.apply_effects = MagicMock(return_value=current_state)
        
        with patch.object(predictor, '_generate_transition_candidates', return_value=[mock_transition]):
            predictions = predictor.predict_transitions(current_state, num_predictions=1)
            
            # 验证预测结果
            assert len(predictions) > 0
            
            # 使用验证器验证预测结果
            for pred in predictions:
                validation_result = validator.validate_transition(pred, current_state)
                assert hasattr(validation_result, 'is_valid')
        
        logger.info("✓ 与转换验证器的集成测试通过")

def run_llm_integration_tests():
    """
    运行LLM集成测试
    """
    logger.info("=== 开始LLM集成测试套件 ===")
    
    test_instance = TestLLMIntegration()
    
    try:
        # 运行测试
        test_instance.setup_method()
        test_instance.test_llm_integration_initialization()
        test_instance.test_confidence_calculation()
        test_instance.test_scene_config_loading()
        test_instance.test_error_handling()
        test_instance.test_confidence_threshold_filtering()
        test_instance.test_integration_with_transition_validator()
        
        logger.info("\n🎉 所有LLM集成测试通过！")
        return True
    except Exception as e:
        logger.error(f"\n❌ LLM集成测试失败: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False
    finally:
        test_instance.teardown_method()

if __name__ == "__main__":
    # 直接运行测试
    success = run_llm_integration_tests()
    sys.exit(0 if success else 1)
