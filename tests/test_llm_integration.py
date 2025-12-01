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
        测试错误处理机制
        """
        self.logger.info("测试：错误处理机制")
        
        predictor = TransitionPredictor(config={'enable_pddl_semantics': True})
        
        # 测试无效状态
        invalid_state = "invalid-state"
        goal_state = {"location": "kitchen"}
        
        try:
            result = predictor.predict_transitions(current_state=invalid_state, goal_state=goal_state, available_transitions=[])
            assert isinstance(result, list)
            self.logger.info("✓ 无效状态错误处理测试通过")
        except Exception as e:
            self.logger.error(f"✗ 无效状态错误处理测试失败: {str(e)}")
            raise
        
        # 测试无效转换
        valid_state = {"location": "kitchen"}
        invalid_transition = "invalid-transition"
        
        try:
            result = predictor.predict_transitions(current_state=valid_state, goal_state=goal_state, available_transitions=[invalid_transition])
            assert isinstance(result, list)
            self.logger.info("✓ 无效转换错误处理测试通过")
        except Exception as e:
            self.logger.error(f"✗ 无效转换错误处理测试失败: {str(e)}")
            raise
        
        # 测试缺少参数
        valid_state = {"location": "kitchen"}
        
        try:
            # 缺少goal_state参数
            result = predictor.predict_transitions(current_state=valid_state, available_transitions=[])
            assert isinstance(result, list)
            self.logger.info("✓ 缺少参数错误处理测试通过")
        except TypeError:
            # 预期会抛出TypeError，因为goal_state是必需参数
            self.logger.info("✓ 缺少参数错误处理测试通过")
        except Exception as e:
            self.logger.error(f"✗ 缺少参数错误处理测试失败: {str(e)}")
            raise
    
    def test_confidence_threshold_filtering(self):
        """
        测试置信度阈值过滤
        """
        logger.info("测试：置信度阈值过滤")
        
        # 创建测试转换
        test_transitions = [
            MagicMock(name="action1", preconditions=[], effects=[]),
            MagicMock(name="action2", preconditions=[], effects=[]),
            MagicMock(name="action3", preconditions=[], effects=[])
        ]
        
        # 使用不同的置信度阈值创建预测器
        high_threshold_predictor = TransitionPredictor(config={'confidence_threshold': 0.9})
        low_threshold_predictor = TransitionPredictor(config={'confidence_threshold': 0.1})
        
        # 定义状态
        current_state = {'location': 'kitchen'}
        goal_state = {'location': 'living_room'}
        
        # 测试高阈值过滤
        high_threshold_results = high_threshold_predictor.predict_transitions(
            current_state, goal_state, test_transitions
        )
        
        # 测试低阈值过滤
        low_threshold_results = low_threshold_predictor.predict_transitions(
            current_state, goal_state, test_transitions
        )
        
        # 验证结果类型和范围
        assert isinstance(high_threshold_results, list)
        assert isinstance(low_threshold_results, list)
        assert 0 <= len(high_threshold_results) <= len(test_transitions)
        assert 0 <= len(low_threshold_results) <= len(test_transitions)
        
        logger.info("✓ 置信度阈值过滤测试通过")
    
    def test_integration_with_transition_validator(self):
        """
        测试与转换验证器的集成
        """
        self.logger.info("测试：与转换验证器的集成")
        
        from transition_modeling.transition_validator import TransitionValidator
        
        # 创建预测器和验证器
        predictor = TransitionPredictor()
        validator = TransitionValidator()
        
        # 模拟当前状态和目标状态
        current_state = {
            "location": "kitchen",
            "holding": "apple",
            "objects": ["fridge", "counter", "apple"]
        }
        
        goal_state = {
            "location": "kitchen",
            "holding": "none",
            "objects": ["fridge", "counter"]
        }
        
        # 模拟更真实的转换对象，包含前置条件和效果
        mock_transition = MagicMock()
        mock_transition.id = "test-eat-apple"
        mock_transition.name = "eat-apple"
        mock_transition.transition_type = MagicMock(value="atomic")
        mock_transition.duration = 5
        mock_transition.cost = 1.0
        
        # 模拟更真实的前置条件
        mock_precondition = MagicMock()
        mock_precondition.evaluate = MagicMock(return_value=True)
        mock_transition.preconditions = [mock_precondition]
        
        # 模拟更真实的效果
        mock_effect = MagicMock()
        mock_transition.effects = [mock_effect]
        
        # 模拟apply_effects方法，返回新的状态
        new_state = current_state.copy()
        new_state["holding"] = "none"
        new_state["objects"].remove("apple")
        mock_transition.apply_effects = MagicMock(return_value=new_state)
        
        # 直接调用predict_transitions方法，传入必需的参数
        predictions = predictor.predict_transitions(
            current_state=current_state, 
            goal_state=goal_state,
            available_transitions=[mock_transition]
        )
        
        # 验证预测结果
        assert isinstance(predictions, list)
        
        # 使用验证器验证预测结果
        for pred in predictions:
            # 注意：validate_transition方法接受的参数是(transition, state)
            # 但predictions返回的是元组(transition, confidence)
            validation_result = validator.validate_transition(pred[0], current_state)
            assert hasattr(validation_result, 'is_valid')
        
        self.logger.info("✓ 与转换验证器的集成测试通过")

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
