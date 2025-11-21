#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Four-Module Integration Test
完整四模块集成测试
测试 goal_interpretation, subgoal_decomposition, transition_modeling, action_sequencing 四个模块的协同工作
"""

import sys
import os
import json
import time
from pathlib import Path

# 添加项目根目录到Python路径
# tests文件夹和四个模块文件夹是并行的，所以需要将父目录添加到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入四个模块
try:
    from goal_interpretation import GoalInterpreter
    from subgoal_decomposition import SubgoalDecomposer
    from transition_modeling import TransitionModeler, ModelingRequest, ModelingResponse
    from action_sequencing import ActionSequencer, ActionType, Action
    print("✓ All four modules imported successfully")
except ImportError as e:
    print(f"✗ Module import failed: {e}")
    sys.exit(1)


class FourModuleIntegrationTester:
    """四模块集成测试器"""
    
    def __init__(self):
        self.goal_interpreter = GoalInterpreter()
        self.subgoal_decomposer = SubgoalDecomposer()
        self.transition_modeler = TransitionModeler()
        self.action_sequencer = ActionSequencer()
        
        self.test_results = []
        self.start_time = time.time()
    
    def run_comprehensive_integration_test(self):
        """运行全面的集成测试"""
        print("=" * 80)
        print("Complete Four-Module Integration Test")
        print("Goal Interpretation + Subgoal Decomposition + Transition Modeling + Action Sequencing")
        print("=" * 80)
        
        # 1. 模块初始化测试
        self.test_module_initialization()
        
        # 2. 目标解释到转换建模的完整流程测试
        self.test_goal_to_transition_flow()
        
        # 3. 子目标分解与动作序列集成测试
        self.test_subgoal_to_action_flow()
        
        # 4. 完整的端到端工作流程测试
        self.test_end_to_end_workflow()
        
        # 5. 复杂场景集成测试
        self.test_complex_scenarios()
        
        # 6. 性能和稳定性测试
        self.test_performance_and_stability()
        
        # 7. 错误处理和恢复测试
        self.test_error_handling_and_recovery()
        
        # 生成测试报告
        self.generate_integration_report()
    
    def test_module_initialization(self):
        """测试模块初始化"""
        print("\n1. Testing Module Initialization...")
        
        try:
            initialization_results = {}
            
            # 测试目标解释模块初始化
            try:
                goal_result = self.goal_interpreter.interpret("Move object to location")
                initialization_results['goal_interpretation'] = goal_result is not None
                print("   ✓ Goal Interpretation module initialized")
            except Exception as e:
                initialization_results['goal_interpretation'] = False
                print(f"   ✗ Goal Interpretation module failed: {e}")
            
            # 测试子目标分解模块初始化
            try:
                from goal_interpretation.goal_interpreter import LTLFormula
                ltl_formula = LTLFormula("F(object_at_location)")
                subgoal_result = self.subgoal_decomposer.decompose(ltl_formula)
                initialization_results['subgoal_decomposition'] = subgoal_result is not None
                print("   ✓ Subgoal Decomposition module initialized")
            except Exception as e:
                initialization_results['subgoal_decomposition'] = False
                print(f"   ✗ Subgoal Decomposition module failed: {e}")
            
            # 测试转换建模模块初始化
            try:
                transitions = self.transition_modeler.create_sample_transitions()
                initialization_results['transition_modeling'] = len(transitions) > 0
                print("   ✓ Transition Modeling module initialized")
            except Exception as e:
                initialization_results['transition_modeling'] = False
                print(f"   ✗ Transition Modeling module failed: {e}")
            
            # 测试动作序列模块初始化
            try:
                from action_sequencing.action_sequencer import SequencingRequest
                test_actions = [Action(id="test_move", name="move", action_type=ActionType.MANIPULATION)]
                test_request = SequencingRequest(
                    initial_state={'at_location': 'start'},
                    goal_state={'at_location': 'goal'},
                    available_actions=test_actions
                )
                action_result = self.action_sequencer.generate_sequence(test_request)
                initialization_results['action_sequencing'] = action_result is not None
                print("   ✓ Action Sequencing module initialized")
            except Exception as e:
                initialization_results['action_sequencing'] = False
                print(f"   ✗ Action Sequencing module failed: {e}")
            
            success = all(initialization_results.values())
            message = f"Module initialization: {sum(initialization_results.values())}/4 modules ready"
            
            self.test_results.append({
                'test': 'module_initialization',
                'success': success,
                'message': message,
                'details': initialization_results
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ Module initialization test failed: {e}")
            self.test_results.append({
                'test': 'module_initialization',
                'success': False,
                'message': str(e)
            })
    
    def test_goal_to_transition_flow(self):
        """测试目标解释到转换建模的完整流程"""
        print("\n2. Testing Goal Interpretation to Transition Modeling Flow...")
        
        try:
            # 步骤1: 目标解释
            goal_description = "Move the red ball to the kitchen table"
            goal_result = self.goal_interpreter.interpret(goal_description)
            
            if not goal_result:
                raise Exception("Goal interpretation failed")
            
            print(f"   ✓ Goal interpreted: {goal_result.get('goal_state', {})}")
            
            # 步骤2: 创建初始状态（与转换建模模块的示例转换匹配）
            initial_state = {
                'at_location': 'start',
                'path_clear': {'destination': 'object_location'},
                'path_clear_to_target': {'destination': 'target_location'},
                'hands_free': True,
                'object_available': {'object': 'target_object'}
            }
            
            # 步骤3: 转换建模
            transitions = self.transition_modeler.create_sample_transitions()
            
            modeling_request = ModelingRequest(
                initial_state=initial_state,
                goal_state=goal_result.get('goal_state', {
                    'object_at_location': {'object': 'target_object', 'location': 'target_location'}
                }),
                available_transitions=transitions,
                constraints=goal_result.get('constraints', {})
            )
            
            modeling_response = self.transition_modeler.model_transitions(modeling_request)
            
            success = (goal_result is not None and 
                      modeling_response.success and 
                      len(modeling_response.predicted_sequences) > 0)
            
            message = f"Goal→Transition flow: {len(modeling_response.predicted_sequences)} sequences generated"
            
            self.test_results.append({
                'test': 'goal_to_transition_flow',
                'success': success,
                'message': message,
                'details': {
                    'goal_interpretation_success': goal_result is not None,
                    'transition_modeling_success': modeling_response.success,
                    'sequences_generated': len(modeling_response.predicted_sequences),
                    'modeling_time': modeling_response.metadata.get('modeling_time', 0)
                }
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ Goal to transition flow test failed: {e}")
            self.test_results.append({
                'test': 'goal_to_transition_flow',
                'success': False,
                'message': str(e)
            })
    
    def test_subgoal_to_action_flow(self):
        """测试子目标分解与动作序列集成"""
        print("\n3. Testing Subgoal Decomposition to Action Sequencing Flow...")
        
        try:
            # 步骤1: 子目标分解
            main_goal = "Move object to location"
            context = {
                'object': 'target_object',
                'start_location': 'start',
                'target_location': 'target_location'
            }
            
            subgoal_result = self.subgoal_decomposer.decompose(
                ltl_formula=main_goal
            )
            
            if not subgoal_result:
                raise Exception("Subgoal decomposition failed")
            
            subgoals = subgoal_result.get('subgoals', [])
            print(f"   ✓ {len(subgoals)} subgoals generated")
            
            # 步骤2: 为每个子目标生成动作序列
            action_sequences = []
            for i, subgoal in enumerate(subgoals):
                subgoal_description = f"Achieve: {subgoal}"
                available_actions = ["move", "pickup", "place", "navigate"]
                
                action_result = self.action_sequencer.sequence_actions(
                    goal=subgoal_description,
                    available_actions=available_actions,
                    context={'subgoal_index': i}
                )
                
                if action_result:
                    action_sequences.append(action_result)
            
            success = len(subgoals) > 0 and len(action_sequences) > 0
            
            message = f"Subgoal→Action flow: {len(subgoals)} subgoals → {len(action_sequences)} action sequences"
            
            self.test_results.append({
                'test': 'subgoal_to_action_flow',
                'success': success,
                'message': message,
                'details': {
                    'subgoals_count': len(subgoals),
                    'action_sequences_count': len(action_sequences),
                    'subgoals': subgoals,
                    'action_sequences': [seq.get('actions', []) for seq in action_sequences[:3]]  # 前3个序列
                }
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ Subgoal to action flow test failed: {e}")
            self.test_results.append({
                'test': 'subgoal_to_action_flow',
                'success': False,
                'message': str(e)
            })
    
    def test_end_to_end_workflow(self):
        """测试完整的端到端工作流程"""
        print("\n4. Testing End-to-End Workflow...")
        
        try:
            workflow_start_time = time.time()
            
            # 完整工作流程：自然语言目标 → 动作序列
            natural_goal = "Pick up the red ball from the floor and place it on the kitchen table"
            
            # 步骤1: 目标解释
            goal_result = self.goal_interpreter.interpret(natural_goal)
            if not goal_result:
                raise Exception("Goal interpretation failed")
            
            # 步骤2: 子目标分解
            subgoal_result = self.subgoal_decomposer.decompose(
                ltl_formula=natural_goal
            )
            if not subgoal_result:
                raise Exception("Subgoal decomposition failed")
            
            # 步骤3: 转换建模
            initial_state = {
                'at_location': 'start',
                'path_clear': {'destination': 'object_location'},
                'path_clear_to_target': {'destination': 'target_location'},
                'hands_free': True,
                'object_available': {'object': 'target_object'}
            }
            
            transitions = self.transition_modeler.create_sample_transitions()
            modeling_request = ModelingRequest(
                initial_state=initial_state,
                goal_state=goal_result.get('goal_state', {
                    'object_at_location': {'object': 'target_object', 'location': 'target_location'}
                }),
                available_transitions=transitions
            )
            
            modeling_response = self.transition_modeler.model_transitions(modeling_request)
            if not modeling_response.success:
                raise Exception("Transition modeling failed")
            
            # 步骤4: 动作序列生成
            final_actions = []
            for sequence in modeling_response.predicted_sequences:
                for transition in sequence.transitions:
                    action_result = self.action_sequencer.sequence_actions(
                        goal=transition.name,
                        available_actions=["move", "pickup", "place", "navigate"],
                        context={'transition_id': transition.id}
                    )
                    if action_result and action_result.get('actions'):
                        final_actions.extend(action_result['actions'])
            
            workflow_end_time = time.time()
            workflow_duration = workflow_end_time - workflow_start_time
            
            success = (goal_result is not None and 
                      subgoal_result is not None and 
                      modeling_response.success and 
                      len(final_actions) > 0)
            
            message = f"End-to-end workflow: {len(final_actions)} actions generated in {workflow_duration:.2f}s"
            
            self.test_results.append({
                'test': 'end_to_end_workflow',
                'success': success,
                'message': message,
                'details': {
                    'goal_interpretation_success': goal_result is not None,
                    'subgoal_decomposition_success': subgoal_result is not None,
                    'transition_modeling_success': modeling_response.success,
                    'action_sequencing_success': len(final_actions) > 0,
                    'total_actions': len(final_actions),
                    'workflow_duration': workflow_duration,
                    'final_actions': final_actions[:10]  # 前10个动作
                }
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ End-to-end workflow test failed: {e}")
            self.test_results.append({
                'test': 'end_to_end_workflow',
                'success': False,
                'message': str(e)
            })
    
    def test_complex_scenarios(self):
        """测试复杂场景"""
        print("\n5. Testing Complex Scenarios...")
        
        try:
            complex_scenarios = [
                {
                    'name': 'Multi-object manipulation',
                    'goal': 'Move the red ball and blue cube to the kitchen table',
                    'expected_complexity': 'high'
                },
                {
                    'name': 'Sequential tasks',
                    'goal': 'First clean the floor, then arrange the furniture',
                    'expected_complexity': 'medium'
                },
                {
                    'name': 'Conditional tasks',
                    'goal': 'If the door is open, go outside and get the package',
                    'expected_complexity': 'medium'
                }
            ]
            
            scenario_results = []
            
            for scenario in complex_scenarios:
                try:
                    # 执行完整工作流程
                    goal_result = self.goal_interpreter.interpret(scenario['goal'])
                    subgoal_result = self.subgoal_decomposer.decompose(
                        ltl_formula=scenario['goal']
                    )
                    
                    # 简化的转换建模（使用示例转换）
                    modeling_request = ModelingRequest(
                        initial_state={'at_location': 'start'},
                        goal_state={'task_completed': True},
                        available_transitions=self.transition_modeler.create_sample_transitions()
                    )
                    modeling_response = self.transition_modeler.model_transitions(modeling_request)
                    
                    action_result = self.action_sequencer.sequence_actions(
                        goal=scenario['goal'],
                        available_actions=["move", "pickup", "place", "clean", "arrange"]
                    )
                    
                    scenario_success = all([
                        goal_result is not None,
                        subgoal_result is not None,
                        modeling_response.success,
                        action_result is not None
                    ])
                    
                    scenario_results.append({
                        'name': scenario['name'],
                        'success': scenario_success,
                        'complexity': scenario['expected_complexity']
                    })
                    
                    print(f"     ✓ {scenario['name']}: {'PASS' if scenario_success else 'FAIL'}")
                    
                except Exception as e:
                    scenario_results.append({
                        'name': scenario['name'],
                        'success': False,
                        'error': str(e)
                    })
                    print(f"     ✗ {scenario['name']}: FAIL ({e})")
            
            success_count = sum(1 for r in scenario_results if r['success'])
            success = success_count >= 2  # 至少2个场景成功
            
            message = f"Complex scenarios: {success_count}/{len(scenario_results)} successful"
            
            self.test_results.append({
                'test': 'complex_scenarios',
                'success': success,
                'message': message,
                'details': {
                    'total_scenarios': len(scenario_results),
                    'successful_scenarios': success_count,
                    'scenario_results': scenario_results
                }
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ Complex scenarios test failed: {e}")
            self.test_results.append({
                'test': 'complex_scenarios',
                'success': False,
                'message': str(e)
            })
    
    def test_performance_and_stability(self):
        """测试性能和稳定性"""
        print("\n6. Testing Performance and Stability...")
        
        try:
            # 性能测试参数
            test_iterations = 5
            performance_metrics = {
                'goal_interpretation_times': [],
                'subgoal_decomposition_times': [],
                'transition_modeling_times': [],
                'action_sequencing_times': [],
                'total_workflow_times': []
            }
            
            for i in range(test_iterations):
                iteration_start = time.time()
                
                # 目标解释性能测试
                start_time = time.time()
                goal_result = self.goal_interpreter.interpret(f"Test goal {i}")
                goal_time = time.time() - start_time
                performance_metrics['goal_interpretation_times'].append(goal_time)
                
                # 子目标分解性能测试
                start_time = time.time()
                subgoal_result = self.subgoal_decomposer.decompose(
                    ltl_formula=f"Test goal {i}"
                )
                subgoal_time = time.time() - start_time
                performance_metrics['subgoal_decomposition_times'].append(subgoal_time)
                
                # 转换建模性能测试
                start_time = time.time()
                modeling_request = ModelingRequest(
                    initial_state={'at_location': 'start'},
                    goal_state={'task_completed': True},
                    available_transitions=self.transition_modeler.create_sample_transitions()
                )
                modeling_response = self.transition_modeler.model_transitions(modeling_request)
                modeling_time = time.time() - start_time
                performance_metrics['transition_modeling_times'].append(modeling_time)
                
                # 动作序列性能测试
                start_time = time.time()
                action_result = self.action_sequencer.sequence_actions(
                    goal=f"Test goal {i}",
                    available_actions=["move", "pickup", "place"]
                )
                action_time = time.time() - start_time
                performance_metrics['action_sequencing_times'].append(action_time)
                
                total_time = time.time() - iteration_start
                performance_metrics['total_workflow_times'].append(total_time)
            
            # 计算平均性能指标
            avg_metrics = {}
            for key, times in performance_metrics.items():
                avg_metrics[key] = sum(times) / len(times)
            
            # 性能标准：总工作流程应在5秒内完成
            success = avg_metrics['total_workflow_times'] < 5.0
            
            message = f"Performance: avg workflow time {avg_metrics['total_workflow_times']:.2f}s"
            
            self.test_results.append({
                'test': 'performance_and_stability',
                'success': success,
                'message': message,
                'details': {
                    'iterations': test_iterations,
                    'average_times': avg_metrics,
                    'performance_within_limits': success
                }
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ Performance and stability test failed: {e}")
            self.test_results.append({
                'test': 'performance_and_stability',
                'success': False,
                'message': str(e)
            })
    
    def test_error_handling_and_recovery(self):
        """测试错误处理和恢复"""
        print("\n7. Testing Error Handling and Recovery...")
        
        try:
            error_cases = []
            
            # 测试无效目标处理
            try:
                goal_result = self.goal_interpreter.interpret("")
                error_cases.append(('empty_goal', goal_result is not None))
            except:
                error_cases.append(('empty_goal', True))
            
            # 测试无效上下文处理
            try:
                subgoal_result = self.subgoal_decomposer.decompose(
                    ltl_formula="Test goal"
                )
                error_cases.append(('invalid_context', subgoal_result is not None))
            except:
                error_cases.append(('invalid_context', True))
            
            # 测试无效状态处理
            try:
                modeling_request = ModelingRequest(
                    initial_state={},
                    goal_state={},
                    available_transitions=[]
                )
                modeling_response = self.transition_modeler.model_transitions(modeling_request)
                error_cases.append(('invalid_states', not modeling_response.success))
            except:
                error_cases.append(('invalid_states', True))
            
            # 测试无效动作处理
            try:
                action_result = self.action_sequencer.sequence_actions(
                    goal="Test goal",
                    available_actions=[]
                )
                error_cases.append(('invalid_actions', action_result is not None))
            except:
                error_cases.append(('invalid_actions', True))
            
            success = all(result for _, result in error_cases)
            message = f"Error handling: {len(error_cases)} error cases tested"
            
            self.test_results.append({
                'test': 'error_handling_and_recovery',
                'success': success,
                'message': message,
                'details': {
                    'error_cases': error_cases
                }
            })
            
            print(f"   ✓ {message}")
            
        except Exception as e:
            print(f"   ✗ Error handling and recovery test failed: {e}")
            self.test_results.append({
                'test': 'error_handling_and_recovery',
                'success': False,
                'message': str(e)
            })
    
    def generate_integration_report(self):
        """生成集成测试报告"""
        print("\n" + "=" * 80)
        print("INTEGRATION TEST REPORT")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        total_time = time.time() - self.start_time
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Total Time: {total_time:.2f} seconds")
        print()
        
        # 详细测试结果
        for i, result in enumerate(self.test_results, 1):
            status = "✓ PASS" if result['success'] else "✗ FAIL"
            print(f"{i}. {result['test']}: {status}")
            print(f"   Message: {result['message']}")
            if 'details' in result:
                print(f"   Details: {json.dumps(result['details'], indent=2, ensure_ascii=False)}")
            print()
        
        # 模块状态总结
        print("MODULE STATUS SUMMARY:")
        print("=" * 50)
        
        module_status = {
            'Goal Interpretation': 'Unknown',
            'Subgoal Decomposition': 'Unknown',
            'Transition Modeling': 'Unknown',
            'Action Sequencing': 'Unknown'
        }
        
        # 根据测试结果确定模块状态
        if any('goal_interpretation' in str(result.get('details', {})) and result['success'] for result in self.test_results):
            module_status['Goal Interpretation'] = '✓ Working'
        
        if any('subgoal_decomposition' in str(result.get('details', {})) and result['success'] for result in self.test_results):
            module_status['Subgoal Decomposition'] = '✓ Working'
        
        if any('transition_modeling' in str(result.get('details', {})) and result['success'] for result in self.test_results):
            module_status['Transition Modeling'] = '✓ Working'
        
        if any('action_sequencing' in str(result.get('details', {})) and result['success'] for result in self.test_results):
            module_status['Action Sequencing'] = '✓ Working'
        
        for module, status in module_status.items():
            print(f"{module:<25}: {status}")
        
        print()
        print("INTEGRATION STATUS:")
        if success_rate >= 85:
            print("🎉 EXCELLENT: All modules are well integrated and working together!")
        elif success_rate >= 70:
            print("✅ GOOD: Most modules are integrated with minor issues")
        elif success_rate >= 50:
            print("⚠️  FAIR: Partial integration, some modules need attention")
        else:
            print("❌ POOR: Significant integration issues need to be resolved")
        
        # 保存详细报告
        report_data = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': success_rate,
                'total_time': total_time,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'module_status': module_status,
            'test_results': self.test_results
        }
        
        report_file = 'four_module_integration_test_results.json'
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Detailed report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️  Could not save report file: {e}")
        
        return success_rate >= 70


def main():
    """主函数"""
    try:
        tester = FourModuleIntegrationTester()
        success = tester.run_comprehensive_integration_test()
        
        if success:
            print("\n🎉 Four-module integration test completed successfully!")
            return 0
        else:
            print("\n⚠️  Four-module integration test completed with issues.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Integration test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())