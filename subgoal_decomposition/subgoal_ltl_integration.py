#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子目标分解与LTL公式集成接口
负责将子目标分解结果与现有的LTL生成和验证系统集成
"""

from typing import Dict, List, Optional, Tuple, Union
import logging
from dataclasses import dataclass

# 修改导入路径
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from goal_interpretation import GoalInterpreter, LTLFormula, EnhancedLTLGenerator
from .subgoal_decomposer import SubgoalDecomposer, DecompositionResult, Subgoal, SubgoalType
from .subgoal_validator import SubgoalValidator, SubgoalOptimizer, SubgoalAnalyzer


@dataclass
class IntegrationResult:
    """集成结果数据类"""
    original_goal: str
    ltl_formula: LTLFormula
    decomposition_result: DecompositionResult
    validation_issues: List
    optimization_result: Optional[object] = None
    analysis_result: Optional[Dict] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SubgoalLTLIntegration:
    """
    子目标分解与LTL集成类
    提供从自然语言目标到子目标分解的完整流程
    """
    
    def __init__(self, 
                 goal_interpreter: GoalInterpreter = None,
                 ltl_generator: EnhancedLTLGenerator = None,
                 subgoal_decomposer: SubgoalDecomposer = None,
                 validator: SubgoalValidator = None,
                 optimizer: SubgoalOptimizer = None,
                 analyzer: SubgoalAnalyzer = None):
        """
        初始化集成接口
        
        Args:
            goal_interpreter: 目标解释器
            ltl_generator: LTL生成器
            subgoal_decomposer: 子目标分解器
            validator: 验证器
            optimizer: 优化器
            analyzer: 分析器
        """
        self.goal_interpreter = goal_interpreter or GoalInterpreter()
        self.ltl_generator = ltl_generator or EnhancedLTLGenerator()
        self.subgoal_decomposer = subgoal_decomposer or SubgoalDecomposer()
        self.validator = validator or SubgoalValidator()
        self.optimizer = optimizer or SubgoalOptimizer()
        self.analyzer = analyzer or SubgoalAnalyzer()
        
        self.logger = logging.getLogger(__name__)
    
    def process_goal(self, 
                    natural_goal: str, 
                    validate: bool = True,
                    optimize: bool = True,
                    analyze: bool = True,
                    max_depth: int = 5,
                    max_subgoals: int = 20) -> IntegrationResult:
        """
        处理自然语言目标的完整流程
        
        Args:
            natural_goal: 自然语言目标
            validate: 是否进行验证
            optimize: 是否进行优化
            analyze: 是否进行分析
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            
        Returns:
            IntegrationResult: 集成结果
        """
        self.logger.info(f"开始处理目标: {natural_goal}")
        
        try:
            # 第一步：解释自然语言目标为LTL公式
            ltl_formula = self.goal_interpreter.interpret(natural_goal)
            self.logger.info(f"生成的LTL公式: {ltl_formula.formula}")
            
            # 第二步：分解LTL公式为子目标
            decomposition_result = self.subgoal_decomposer.decompose(
                ltl_formula, max_depth=max_depth, max_subgoals=max_subgoals
            )
            self.logger.info(f"分解得到 {len(decomposition_result.subgoals)} 个子目标")
            
            # 第三步：验证分解结果
            validation_issues = []
            optimization_result = None
            analysis_result = None
            
            if validate:
                validation_issues = self.validator.validate_decomposition(decomposition_result)
                self.logger.info(f"验证发现 {len(validation_issues)} 个问题")
                
                # 第四步：优化分解结果
                if optimize and validation_issues:
                    optimization_result = self.optimizer.optimize_decomposition(
                        decomposition_result, validation_issues
                    )
                    decomposition_result = optimization_result.optimized_result
                    self.logger.info(f"优化完成，性能提升: {optimization_result.performance_gain}%")
            
            # 第五步：分析复杂度
            if analyze:
                analysis_result = self.analyzer.analyze_complexity(decomposition_result)
                self.logger.info(f"复杂度分析完成: {analysis_result['overall_complexity']}")
            
            # 创建集成结果
            result = IntegrationResult(
                original_goal=natural_goal,
                ltl_formula=ltl_formula,
                decomposition_result=decomposition_result,
                validation_issues=validation_issues,
                optimization_result=optimization_result,
                analysis_result=analysis_result,
                metadata={
                    'processed_at': 'unknown',
                    'validation_enabled': validate,
                    'optimization_enabled': optimize,
                    'analysis_enabled': analyze,
                    'max_depth': max_depth,
                    'max_subgoals': max_subgoals
                }
            )
            
            self.logger.info("目标处理完成")
            return result
            
        except Exception as e:
            self.logger.error(f"处理目标时发生错误: {str(e)}")
            raise
    
    def process_ltl_formula(self,
                           ltl_formula: Union[str, LTLFormula],
                           validate: bool = True,
                           optimize: bool = True,
                           analyze: bool = True,
                           max_depth: int = 5,
                           max_subgoals: int = 20) -> IntegrationResult:
        """
        直接处理LTL公式
        
        Args:
            ltl_formula: LTL公式或LTLFormula对象
            validate: 是否进行验证
            optimize: 是否进行优化
            analyze: 是否进行分析
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            
        Returns:
            IntegrationResult: 集成结果
        """
        self.logger.info(f"开始处理LTL公式: {ltl_formula}")
        
        try:
            # 确保是LTLFormula对象
            if isinstance(ltl_formula, str):
                ltl_formula = LTLFormula(
                    formula=ltl_formula,
                    description="Direct LTL input",
                    confidence=0.9
                )
            
            # 分解LTL公式为子目标
            decomposition_result = self.subgoal_decomposer.decompose(
                ltl_formula, max_depth=max_depth, max_subgoals=max_subgoals
            )
            self.logger.info(f"分解得到 {len(decomposition_result.subgoals)} 个子目标")
            
            # 验证分解结果
            validation_issues = []
            optimization_result = None
            analysis_result = None
            
            if validate:
                validation_issues = self.validator.validate_decomposition(decomposition_result)
                self.logger.info(f"验证发现 {len(validation_issues)} 个问题")
                
                # 优化分解结果
                if optimize and validation_issues:
                    optimization_result = self.optimizer.optimize_decomposition(
                        decomposition_result, validation_issues
                    )
                    decomposition_result = optimization_result.optimized_result
                    self.logger.info(f"优化完成，性能提升: {optimization_result.performance_gain}%")
            
            # 分析复杂度
            if analyze:
                analysis_result = self.analyzer.analyze_complexity(decomposition_result)
                self.logger.info(f"复杂度分析完成: {analysis_result['overall_complexity']}")
            
            # 创建集成结果
            result = IntegrationResult(
                original_goal="",
                ltl_formula=ltl_formula,
                decomposition_result=decomposition_result,
                validation_issues=validation_issues,
                optimization_result=optimization_result,
                analysis_result=analysis_result,
                metadata={
                    'processed_at': 'unknown',
                    'validation_enabled': validate,
                    'optimization_enabled': optimize,
                    'analysis_enabled': analyze,
                    'max_depth': max_depth,
                    'max_subgoals': max_subgoals,
                    'direct_ltl_input': True
                }
            )
            
            self.logger.info("LTL公式处理完成")
            return result
            
        except Exception as e:
            self.logger.error(f"处理LTL公式时发生错误: {str(e)}")
            raise
    
    def batch_process_goals(self,
                          goals: List[str],
                          validate: bool = True,
                          optimize: bool = True,
                          analyze: bool = True,
                          max_depth: int = 5,
                          max_subgoals: int = 20) -> List[IntegrationResult]:
        """
        批量处理目标
        
        Args:
            goals: 自然语言目标列表
            validate: 是否进行验证
            optimize: 是否进行优化
            analyze: 是否进行分析
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            
        Returns:
            List[IntegrationResult]: 集成结果列表
        """
        results = []
        
        for i, goal in enumerate(goals):
            self.logger.info(f"处理第 {i+1}/{len(goals)} 个目标")
            try:
                result = self.process_goal(
                    goal, validate, optimize, analyze, max_depth, max_subgoals
                )
                results.append(result)
            except Exception as e:
                self.logger.error(f"处理目标 '{goal}' 时发生错误: {str(e)}")
                # 创建错误结果
                error_result = IntegrationResult(
                    original_goal=goal,
                    ltl_formula=LTLFormula(formula="", description="Error", confidence=0.0),
                    decomposition_result=DecompositionResult(
                        subgoals=[], root_subgoal="", execution_order=[], 
                        total_cost=0.0, 
                        decomposition_strategy=self.subgoal_decomposer.strategy,
                        metadata={'error': str(e)}
                    ),
                    validation_issues=[],
                    metadata={'error': str(e)}
                )
                results.append(error_result)
        
        return results
    
    def compare_strategies(self,
                          ltl_formula: Union[str, LTLFormula],
                          strategies: List = None,
                          max_depth: int = 5,
                          max_subgoals: int = 20) -> Dict[str, IntegrationResult]:
        """
        比较不同分解策略的效果
        
        Args:
            ltl_formula: LTL公式
            strategies: 要比较的策略列表
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            
        Returns:
            Dict[str, IntegrationResult]: 不同策略的分解结果
        """
        if strategies is None:
            strategies = ['default', 'hierarchical', 'sequential']
        
        results = {}
        
        for strategy in strategies:
            # 保存原始策略
            original_strategy = self.subgoal_decomposer.strategy
            
            try:
                # 设置当前策略
                self.subgoal_decomposer.strategy = strategy
                
                # 处理LTL公式
                result = self.process_ltl_formula(
                    ltl_formula, max_depth=max_depth, max_subgoals=max_subgoals
                )
                results[strategy] = result
            except Exception as e:
                self.logger.error(f"使用策略 '{strategy}' 时发生错误: {str(e)}")
            finally:
                # 恢复原始策略
                self.subgoal_decomposer.strategy = original_strategy
        
        return results
    
    def generate_subgoal_plan(self, goal_text: str, **kwargs) -> IntegrationResult:
        """
        生成子目标计划，兼容旧版接口
        
        Args:
            goal_text: 目标文本
            **kwargs: 其他参数
            
        Returns:
            IntegrationResult: 子目标计划结果
        """
        self.logger.info(f"生成子目标计划: {goal_text}")
        
        # 调用现有的process_goal方法实现相同功能
        return self.process_goal(
            natural_goal=goal_text,
            validate=kwargs.get('validate', True),
            optimize=kwargs.get('optimize', True),
            analyze=kwargs.get('analyze', True),
            max_depth=kwargs.get('max_depth', 5),
            max_subgoals=kwargs.get('max_subgoals', 20)
        )
    
    def test_all_strategies(self, ltl_formula: str, max_depth: int = 5, max_subgoals: int = 20, strategies: list = None) -> Dict[str, IntegrationResult]:
        """
        测试所有可用策略
        
        Args:
            ltl_formula: LTL公式
            max_depth: 最大分解深度
            max_subgoals: 最大子目标数量
            strategies: 要测试的策略列表，None表示测试所有策略
            
        Returns:
            Dict[str, IntegrationResult]: 各策略的结果
        """
        if strategies is None:
            from subgoal_decomposer import DecompositionStrategy
            strategies = list(DecompositionStrategy)
        
        results = {}
        
        for strategy in strategies:
            self.logger.info(f"测试策略: {strategy.value}")
            
            # 设置分解器策略
            original_strategy = self.subgoal_decomposer.strategy
            self.subgoal_decomposer.set_strategy(strategy)
            
            try:
                result = self.process_ltl_formula(
                    ltl_formula, validate=True, optimize=True, analyze=True,
                    max_depth=max_depth, max_subgoals=max_subgoals
                )
                results[strategy.value] = result
                
                self.logger.info(f"策略 {strategy.value} 生成 {len(result.decomposition_result.subgoals)} 个子目标")
                
            except Exception as e:
                self.logger.error(f"策略 {strategy.value} 执行失败: {str(e)}")
            
            # 恢复原始策略
            self.subgoal_decomposer.set_strategy(original_strategy)
        
        return results
    
    def generate_execution_plan(self, result: IntegrationResult) -> Dict:
        """
        生成执行计划
        
        Args:
            result: 集成结果
            
        Returns:
            Dict: 执行计划
        """
        plan = {
            'goal': result.original_goal,
            'ltl_formula': result.ltl_formula.formula,
            'total_cost': result.decomposition_result.total_cost,
            'estimated_duration': result.decomposition_result.total_cost * 10,  # 假设每个成本单位10分钟
            'phases': [],
            'dependencies': {},
            'risks': [],
            'recommendations': []
        }
        
        # 生成执行阶段
        current_phase = []
        current_cost = 0
        max_phase_cost = 5.0  # 每个阶段最大成本
        
        for subgoal_id in result.decomposition_result.execution_order:
            subgoal = next((sg for sg in result.decomposition_result.subgoals if sg.id == subgoal_id), None)
            if subgoal:
                if current_cost + subgoal.estimated_cost > max_phase_cost and current_phase:
                    # 完成当前阶段
                    plan['phases'].append({
                        'name': f"Phase {len(plan['phases']) + 1}",
                        'subgoals': current_phase.copy(),
                        'cost': current_cost,
                        'estimated_duration': current_cost * 10
                    })
                    current_phase = []
                    current_cost = 0
                
                current_phase.append({
                    'id': subgoal.id,
                    'description': subgoal.description,
                    'ltl_formula': subgoal.ltl_formula,
                    'type': subgoal.subgoal_type.value,
                    'cost': subgoal.estimated_cost,
                    'dependencies': subgoal.dependencies
                })
                current_cost += subgoal.estimated_cost
        
        # 添加最后一个阶段
        if current_phase:
            plan['phases'].append({
                'name': f"Phase {len(plan['phases']) + 1}",
                'subgoals': current_phase,
                'cost': current_cost,
                'estimated_duration': current_cost * 10
            })
        
        # 生成依赖关系图
        for subgoal in result.decomposition_result.subgoals:
            plan['dependencies'][subgoal.id] = subgoal.dependencies
        
        # 识别风险
        if result.validation_issues:
            error_count = len([i for i in result.validation_issues if i.severity == 'error'])
            warning_count = len([i for i in result.validation_issues if i.severity == 'warning'])
            
            if error_count > 0:
                plan['risks'].append(f"发现 {error_count} 个严重错误")
            if warning_count > 0:
                plan['risks'].append(f"发现 {warning_count} 个警告")
        
        # 生成建议
        if result.analysis_result:
            plan['recommendations'].extend(result.analysis_result.get('recommendations', []))
        
        if result.optimization_result:
            plan['recommendations'].append(f"优化后性能提升 {result.optimization_result.performance_gain}%")
        
        return plan
    
    def export_result(self, result: IntegrationResult, format: str = 'json') -> str:
        """
        导出结果
        
        Args:
            result: 集成结果
            format: 导出格式 ('json', 'text', 'html')
            
        Returns:
            str: 导出的字符串
        """
        if format == 'json':
            return self._export_json(result)
        elif format == 'text':
            return self._export_text(result)
        elif format == 'html':
            return self._export_html(result)
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    def _export_json(self, result: IntegrationResult) -> str:
        """导出为JSON格式"""
        import json
        
        data = {
            'original_goal': result.original_goal,
            'ltl_formula': {
                'formula': result.ltl_formula.formula,
                'is_valid': result.ltl_formula.is_valid()
            },
            'decomposition': {
                'subgoals': [
                    {
                        'id': sg.id,
                        'description': sg.description,
                        'ltl_formula': sg.ltl_formula,
                        'type': sg.subgoal_type.value,
                        'dependencies': sg.dependencies,
                        'priority': sg.priority,
                        'estimated_cost': sg.estimated_cost,
                        'preconditions': sg.preconditions,
                        'effects': sg.effects,
                        'metadata': sg.metadata
                    }
                    for sg in result.decomposition_result.subgoals
                ],
                'root_subgoal': result.decomposition_result.root_subgoal,
                'execution_order': result.decomposition_result.execution_order,
                'total_cost': result.decomposition_result.total_cost,
                'strategy': result.decomposition_result.decomposition_strategy.value
            },
            'validation_issues': [
                {
                    'severity': issue.severity,
                    'message': issue.message,
                    'subgoal_id': issue.subgoal_id,
                    'suggestion': issue.suggestion
                }
                for issue in result.validation_issues
            ],
            'metadata': result.metadata
        }
        
        if result.optimization_result:
            data['optimization'] = {
                'improvements': result.optimization_result.improvements,
                'performance_gain': result.optimization_result.performance_gain,
                'issues_resolved': result.optimization_result.validation_issues_resolved
            }
        
        if result.analysis_result:
            data['analysis'] = result.analysis_result
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _export_text(self, result: IntegrationResult) -> str:
        """导出为文本格式"""
        lines = []
        lines.append("=" * 80)
        lines.append("子目标分解集成结果")
        lines.append("=" * 80)
        lines.append(f"原始目标: {result.original_goal}")
        lines.append(f"LTL公式: {result.ltl_formula.formula}")
        lines.append(f"置信度: {result.ltl_formula.confidence}")
        lines.append("")
        
        lines.append("分解结果:")
        lines.append(f"  子目标数量: {len(result.decomposition_result.subgoals)}")
        lines.append(f"  总成本: {result.decomposition_result.total_cost}")
        lines.append(f"  分解策略: {result.decomposition_result.decomposition_strategy.value}")
        lines.append("")
        
        lines.append("执行顺序:")
        for i, subgoal_id in enumerate(result.decomposition_result.execution_order):
            subgoal = next((sg for sg in result.decomposition_result.subgoals if sg.id == subgoal_id), None)
            if subgoal:
                lines.append(f"  {i+1}. {subgoal.id}: {subgoal.description}")
                lines.append(f"     LTL: {subgoal.ltl_formula}")
                lines.append(f"     类型: {subgoal.subgoal_type.value}")
                lines.append(f"     成本: {subgoal.estimated_cost}")
                if subgoal.dependencies:
                    lines.append(f"     依赖: {', '.join(subgoal.dependencies)}")
                lines.append("")
        
        if result.validation_issues:
            lines.append("验证问题:")
            for issue in result.validation_issues:
                lines.append(f"  [{issue.severity.upper()}] {issue.message}")
                if issue.suggestion:
                    lines.append(f"    建议: {issue.suggestion}")
            lines.append("")
        
        if result.optimization_result:
            lines.append("优化结果:")
            lines.append(f"  性能提升: {result.optimization_result.performance_gain}%")
            lines.append(f"  解决问题: {result.optimization_result.validation_issues_resolved}")
            for improvement in result.optimization_result.improvements:
                lines.append(f"  - {improvement}")
            lines.append("")
        
        if result.analysis_result:
            lines.append("复杂度分析:")
            lines.append(f"  整体复杂度: {result.analysis_result['overall_complexity']}")
            lines.append(f"  子目标数量: {result.analysis_result['subgoal_count']}")
            lines.append(f"  最大深度: {result.analysis_result['max_depth']}")
            lines.append(f"  依赖复杂度: {result.analysis_result['dependency_complexity']:.2f}")
            
            if result.analysis_result['recommendations']:
                lines.append("  建议:")
                for rec in result.analysis_result['recommendations']:
                    lines.append(f"    - {rec}")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _export_html(self, result: IntegrationResult) -> str:
        """导出为HTML格式"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>子目标分解结果</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .subgoal {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-left: 4px solid #007cba; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .info {{ color: blue; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>子目标分解集成结果</h1>
        <p><strong>原始目标:</strong> {result.original_goal}</p>
        <p><strong>LTL公式:</strong> {result.ltl_formula.formula}</p>
        <p><strong>置信度:</strong> {result.ltl_formula.confidence}</p>
    </div>
    
    <div class="section">
        <h2>分解结果</h2>
        <p><strong>子目标数量:</strong> {len(result.decomposition_result.subgoals)}</p>
        <p><strong>总成本:</strong> {result.decomposition_result.total_cost}</p>
        <p><strong>分解策略:</strong> {result.decomposition_result.decomposition_strategy.value}</p>
        
        <h3>执行顺序</h3>
        <table>
            <tr><th>序号</th><th>ID</th><th>描述</th><th>LTL公式</th><th>类型</th><th>成本</th><th>依赖</th></tr>
"""
        
        for i, subgoal_id in enumerate(result.decomposition_result.execution_order):
            subgoal = next((sg for sg in result.decomposition_result.subgoals if sg.id == subgoal_id), None)
            if subgoal:
                dependencies = ', '.join(subgoal.dependencies) if subgoal.dependencies else '无'
                html += f"""
            <tr>
                <td>{i+1}</td>
                <td>{subgoal.id}</td>
                <td>{subgoal.description}</td>
                <td>{subgoal.ltl_formula}</td>
                <td>{subgoal.subgoal_type.value}</td>
                <td>{subgoal.estimated_cost}</td>
                <td>{dependencies}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
"""
        
        if result.validation_issues:
            html += """
    <div class="section">
        <h2>验证问题</h2>
"""
            for issue in result.validation_issues:
                css_class = issue.severity
                html += f"""
        <div class="{css_class}">
            <strong>[{issue.severity.upper()}]</strong> {issue.message}
            {f'<br><em>建议: {issue.suggestion}</em>' if issue.suggestion else ''}
        </div>
"""
            html += """
    </div>
"""
        
        html += """
</body>
</html>
"""
        
        return html