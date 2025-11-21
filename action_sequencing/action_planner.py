#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动作规划算法模块
实现多种动作序列规划算法，包括A*、BFS、DFS等
"""

from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass
from enum import Enum
import heapq
import time
import copy
from collections import deque

from .action_data import Action, ActionSequence, ActionType, ActionStatus
from .state_manager import EnvironmentState, StateTransition, StateManager


class PlanningAlgorithm(Enum):
    """规划算法枚举"""
    BFS = "bfs"                    # 广度优先搜索
    DFS = "dfs"                    # 深度优先搜索
    ASTAR = "astar"                # A*搜索
    GREEDY = "greedy"              # 贪心搜索
    HIERARCHICAL = "hierarchical"  # 分层规划
    SAMPLING_BASED = "sampling_based"  # 基于采样的规划


class HeuristicType(Enum):
    """启发式类型枚举"""
    ZERO = "zero"                  # 零启发式
    GOAL_DISTANCE = "goal_distance"  # 目标距离
    ACTION_COST = "action_cost"    # 动作成本
    COMBINED = "combined"          # 组合启发式


@dataclass
class PlanningNode:
    """规划节点数据类"""
    state: Dict[str, Any]
    actions: List[Action]
    cost: float
    heuristic: float
    total_cost: float
    depth: int
    parent: Optional['PlanningNode'] = None
    
    def __lt__(self, other):
        """用于优先队列比较"""
        return self.total_cost < other.total_cost
    
    def __eq__(self, other):
        """节点相等比较"""
        return self.state == other.state
    
    def __hash__(self):
        """节点哈希"""
        return hash(str(sorted(self.state.items())))


@dataclass
class PlanningResult:
    """规划结果数据类"""
    success: bool
    action_sequence: Optional[ActionSequence]
    planning_time: float
    nodes_expanded: int
    solution_cost: float
    solution_length: int
    algorithm: PlanningAlgorithm
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """后处理初始化"""
        if self.metadata is None:
            self.metadata = {}


class HeuristicCalculator:
    """启发式计算器"""
    
    def __init__(self, heuristic_type: HeuristicType = HeuristicType.GOAL_DISTANCE):
        """
        初始化启发式计算器
        
        Args:
            heuristic_type: 启发式类型
        """
        self.heuristic_type = heuristic_type
    
    def calculate(self, current_state: Dict[str, Any], goal_state: Dict[str, Any],
                  available_actions: List[Action]) -> float:
        """
        计算启发式值
        
        Args:
            current_state: 当前状态
            goal_state: 目标状态
            available_actions: 可用动作列表
            
        Returns:
            float: 启发式值
        """
        if self.heuristic_type == HeuristicType.ZERO:
            return 0.0
        elif self.heuristic_type == HeuristicType.GOAL_DISTANCE:
            return self._goal_distance_heuristic(current_state, goal_state)
        elif self.heuristic_type == HeuristicType.ACTION_COST:
            return self._action_cost_heuristic(current_state, goal_state, available_actions)
        elif self.heuristic_type == HeuristicType.COMBINED:
            return self._combined_heuristic(current_state, goal_state, available_actions)
        else:
            return 0.0
    
    def _goal_distance_heuristic(self, current_state: Dict[str, Any], 
                                goal_state: Dict[str, Any]) -> float:
        """目标距离启发式"""
        distance = 0
        for key, goal_value in goal_state.items():
            current_value = current_state.get(key)
            if current_value != goal_value:
                distance += 1
        return distance
    
    def _action_cost_heuristic(self, current_state: Dict[str, Any], 
                              goal_state: Dict[str, Any], 
                              available_actions: List[Action]) -> float:
        """动作成本启发式"""
        # 简单实现：估计达到目标所需的最小动作成本
        min_cost = float('inf')
        
        for action in available_actions:
            if action.can_execute(current_state):
                # 模拟执行动作
                simulated_state = copy.deepcopy(current_state)
                try:
                    new_state = action.execute(simulated_state)
                    # 计算新状态到目标的距离
                    distance = self._goal_distance_heuristic(new_state, goal_state)
                    total_cost = action.duration + distance
                    if total_cost < min_cost:
                        min_cost = total_cost
                except Exception:
                    continue
        
        return min_cost if min_cost != float('inf') else self._goal_distance_heuristic(current_state, goal_state)
    
    def _combined_heuristic(self, current_state: Dict[str, Any], 
                           goal_state: Dict[str, Any], 
                           available_actions: List[Action]) -> float:
        """组合启发式"""
        goal_distance = self._goal_distance_heuristic(current_state, goal_state)
        action_cost = self._action_cost_heuristic(current_state, goal_state, available_actions)
        
        # 加权组合
        return 0.7 * goal_distance + 0.3 * action_cost


class ActionPlanner:
    """动作规划器类"""
    
    def __init__(self, algorithm: PlanningAlgorithm = PlanningAlgorithm.ASTAR,
                 heuristic_type: HeuristicType = HeuristicType.GOAL_DISTANCE,
                 max_depth: int = 50, max_time: float = 30.0):
        """
        初始化动作规划器
        
        Args:
            algorithm: 规划算法
            heuristic_type: 启发式类型
            max_depth: 最大搜索深度
            max_time: 最大规划时间
        """
        self.algorithm = algorithm
        self.max_depth = max_depth
        self.max_time = max_time
        self.heuristic_calculator = HeuristicCalculator(heuristic_type)
        self.state_manager = StateManager()
        
        # 统计信息
        self.nodes_expanded = 0
        self.planning_start_time = 0
    
    def plan(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
             available_actions: List[Action], 
             state_transitions: Optional[List[StateTransition]] = None) -> PlanningResult:
        """
        规划动作序列
        
        Args:
            initial_state: 初始状态
            goal_state: 目标状态
            available_actions: 可用动作列表
            state_transitions: 状态转换列表
            
        Returns:
            PlanningResult: 规划结果
        """
        self.planning_start_time = time.time()
        self.nodes_expanded = 0
        
        # 设置状态管理器
        self.state_manager.reset_to_initial_state(initial_state)
        if state_transitions:
            for transition in state_transitions:
                self.state_manager.add_transition(transition)
        
        # 根据算法选择规划方法
        if self.algorithm == PlanningAlgorithm.BFS:
            return self._bfs_planning(initial_state, goal_state, available_actions)
        elif self.algorithm == PlanningAlgorithm.DFS:
            return self._dfs_planning(initial_state, goal_state, available_actions)
        elif self.algorithm == PlanningAlgorithm.ASTAR:
            return self._astar_planning(initial_state, goal_state, available_actions)
        elif self.algorithm == PlanningAlgorithm.GREEDY:
            return self._greedy_planning(initial_state, goal_state, available_actions)
        elif self.algorithm == PlanningAlgorithm.HIERARCHICAL:
            return self._hierarchical_planning(initial_state, goal_state, available_actions)
        elif self.algorithm == PlanningAlgorithm.SAMPLING_BASED:
            return self._sampling_based_planning(initial_state, goal_state, available_actions)
        else:
            raise ValueError(f"Unsupported planning algorithm: {self.algorithm}")
    
    def _bfs_planning(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
                      available_actions: List[Action]) -> PlanningResult:
        """广度优先搜索规划"""
        queue = deque([PlanningNode(
            state=initial_state,
            actions=[],
            cost=0.0,
            heuristic=0.0,
            total_cost=0.0,
            depth=0
        )])
        
        visited = {str(sorted(initial_state.items()))}
        
        while queue and (time.time() - self.planning_start_time) < self.max_time:
            current_node = queue.popleft()
            self.nodes_expanded += 1
            
            # 检查是否达到目标
            if self._is_goal_achieved(current_node.state, goal_state):
                return self._create_success_result(current_node, available_actions, goal_state)
            
            # 检查深度限制
            if current_node.depth >= self.max_depth:
                continue
            
            # 扩展节点
            successors = self._get_successors(current_node, available_actions, goal_state)
            for successor in successors:
                state_key = str(sorted(successor.state.items()))
                if state_key not in visited:
                    visited.add(state_key)
                    queue.append(successor)
        
        return self._create_failure_result()
    
    def _dfs_planning(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
                      available_actions: List[Action]) -> PlanningResult:
        """深度优先搜索规划"""
        stack = [PlanningNode(
            state=initial_state,
            actions=[],
            cost=0.0,
            heuristic=0.0,
            total_cost=0.0,
            depth=0
        )]
        
        visited = {str(sorted(initial_state.items()))}
        
        while stack and (time.time() - self.planning_start_time) < self.max_time:
            current_node = stack.pop()
            self.nodes_expanded += 1
            
            # 检查是否达到目标
            if self._is_goal_achieved(current_node.state, goal_state):
                return self._create_success_result(current_node, available_actions, goal_state)
            
            # 检查深度限制
            if current_node.depth >= self.max_depth:
                continue
            
            # 扩展节点
            successors = self._get_successors(current_node, available_actions, goal_state)
            for successor in reversed(successors):  # 反向添加以保持顺序
                state_key = str(sorted(successor.state.items()))
                if state_key not in visited:
                    visited.add(state_key)
                    stack.append(successor)
        
        return self._create_failure_result()
    
    def _astar_planning(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
                       available_actions: List[Action]) -> PlanningResult:
        """A*搜索规划"""
        open_list = []
        closed_set = set()
        
        # 初始节点
        initial_heuristic = self.heuristic_calculator.calculate(initial_state, goal_state, available_actions)
        initial_node = PlanningNode(
            state=initial_state,
            actions=[],
            cost=0.0,
            heuristic=initial_heuristic,
            total_cost=initial_heuristic,
            depth=0
        )
        
        heapq.heappush(open_list, initial_node)
        
        while open_list and (time.time() - self.planning_start_time) < self.max_time:
            current_node = heapq.heappop(open_list)
            self.nodes_expanded += 1
            
            # 检查是否达到目标
            if self._is_goal_achieved(current_node.state, goal_state):
                return self._create_success_result(current_node, available_actions, goal_state)
            
            # 检查是否已访问
            state_key = str(sorted(current_node.state.items()))
            if state_key in closed_set:
                continue
            
            closed_set.add(state_key)
            
            # 检查深度限制
            if current_node.depth >= self.max_depth:
                continue
            
            # 扩展节点
            successors = self._get_successors(current_node, available_actions, goal_state)
            for successor in successors:
                successor_key = str(sorted(successor.state.items()))
                if successor_key not in closed_set:
                    heapq.heappush(open_list, successor)
        
        return self._create_failure_result()
    
    def _greedy_planning(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
                        available_actions: List[Action]) -> PlanningResult:
        """贪心搜索规划"""
        current_state = initial_state
        current_actions = []
        total_cost = 0.0
        
        while (time.time() - self.planning_start_time) < self.max_time:
            self.nodes_expanded += 1
            
            # 检查是否达到目标
            if self._is_goal_achieved(current_state, goal_state):
                # 创建动作序列
                action_sequence = ActionSequence(
                    id=f"greedy_{int(time.time())}",
                    actions=current_actions,
                    initial_state=initial_state,
                    goal_state=goal_state
                )
                
                return PlanningResult(
                    success=True,
                    action_sequence=action_sequence,
                    planning_time=time.time() - self.planning_start_time,
                    nodes_expanded=self.nodes_expanded,
                    solution_cost=total_cost,
                    solution_length=len(current_actions),
                    algorithm=self.algorithm,
                    metadata={}
                )
            
            # 获取可执行动作
            executable_actions = [action for action in available_actions 
                                 if action.can_execute(current_state)]
            
            if not executable_actions:
                break
            
            # 选择最佳动作（基于启发式）
            best_action = None
            best_heuristic = float('inf')
            
            for action in executable_actions:
                try:
                    simulated_state = copy.deepcopy(current_state)
                    new_state = action.execute(simulated_state)
                    heuristic = self.heuristic_calculator.calculate(new_state, goal_state, available_actions)
                    
                    if heuristic < best_heuristic:
                        best_heuristic = heuristic
                        best_action = action
                except Exception:
                    continue
            
            if best_action is None:
                break
            
            # 执行最佳动作
            try:
                current_state = best_action.execute(current_state)
                current_actions.append(best_action)
                total_cost += best_action.duration
            except Exception:
                break
        
        return self._create_failure_result()
    
    def _hierarchical_planning(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
                              available_actions: List[Action]) -> PlanningResult:
        """分层规划"""
        # 简化的分层规划实现
        # 将复杂目标分解为子目标，然后逐个规划
        
        # 创建子目标
        subgoals = []
        
        try:
            # 如果目标状态为空，返回空列表
            if not goal_state:
                return self._create_failure_result()
            
            # 按优先级排序目标变量
            prioritized_goals = []
            
            # 首先处理位置相关的目标
            location_goals = {k: v for k, v in goal_state.items() 
                           if any(loc_key in k.lower() for loc_key in ['location', 'position', 'place', 'room', 'area'])}
            if location_goals:
                prioritized_goals.append(('location', location_goals))
            
            # 然后处理对象状态相关的目标
            object_goals = {k: v for k, v in goal_state.items() 
                          if any(obj_key in k.lower() for obj_key in ['object', 'item', 'thing', 'entity'])}
            if object_goals:
                prioritized_goals.append(('objects', object_goals))
            
            # 接着处理布尔状态相关的目标
            bool_goals = {k: v for k, v in goal_state.items() if isinstance(v, bool)}
            if bool_goals:
                prioritized_goals.append(('boolean', bool_goals))
            
            # 最后处理其他目标
            other_goals = {k: v for k, v in goal_state.items() 
                         if k not in location_goals and k not in object_goals and k not in bool_goals}
            if other_goals:
                prioritized_goals.append(('other', other_goals))
            
            # 如果没有特殊分类，按变量数量分割
            if not prioritized_goals:
                goal_items = list(goal_state.items())
                if len(goal_items) <= 3:
                    # 如果目标很少，作为一个子目标
                    subgoals.append(goal_state)
                else:
                    # 分割成多个子目标，每个子目标包含2-3个变量
                    for i in range(0, len(goal_items), 2):
                        subgoal = dict(goal_items[i:i+2])
                        subgoals.append(subgoal)
            else:
                # 按优先级创建子目标
                for category, goals in prioritized_goals:
                    if len(goals) <= 2:
                        subgoals.append(goals)
                    else:
                        # 如果某个类别的目标太多，进一步分割
                        items = list(goals.items())
                        for i in range(0, len(items), 2):
                            subgoal = dict(items[i:i+2])
                            subgoals.append(subgoal)
            
            # 确保至少有一个子目标
            if not subgoals and goal_state:
                subgoals.append(goal_state)
            
        except Exception as e:
            # 如果创建子目标失败，使用原始目标作为单个子目标
            if hasattr(self, 'logger'):
                self.logger.warning(f"Failed to create subgoals, using original goal: {str(e)}")
            subgoals = [goal_state] if goal_state else []
        
        if not subgoals:
            return self._create_failure_result()
        
        # 逐个规划子目标
        all_actions = []
        current_state = initial_state
        
        for subgoal in subgoals:
            subgoal_result = self._astar_planning(current_state, subgoal, available_actions)
            
            if not subgoal_result.success:
                return self._create_failure_result()
            
            all_actions.extend(subgoal_result.action_sequence.actions)
            current_state = subgoal_result.action_sequence.actions[-1].execute(current_state)
        
        # 创建最终动作序列
        action_sequence = ActionSequence(
            id=f"hierarchical_{int(time.time())}",
            actions=all_actions,
            initial_state=initial_state,
            goal_state=goal_state
        )
        
        return PlanningResult(
            success=True,
            action_sequence=action_sequence,
            planning_time=time.time() - self.planning_start_time,
            nodes_expanded=self.nodes_expanded,
            solution_cost=sum(action.duration for action in all_actions),
            solution_length=len(all_actions),
            algorithm=self.algorithm,
            metadata={"subgoals": subgoals}
        )
    
    def _sampling_based_planning(self, initial_state: Dict[str, Any], goal_state: Dict[str, Any],
                                available_actions: List[Action]) -> PlanningResult:
        """基于采样的规划（简化RRT）"""
        import random
        
        max_iterations = 1000
        best_sequence = None
        best_cost = float('inf')
        
        for _ in range(max_iterations):
            if (time.time() - self.planning_start_time) > self.max_time:
                break
            
            # 随机采样动作序列
            current_state = initial_state
            current_actions = []
            total_cost = 0.0
            
            for _ in range(random.randint(1, 20)):  # 随机长度
                executable_actions = [action for action in available_actions 
                                   if action.can_execute(current_state)]
                
                if not executable_actions:
                    break
                
                # 随机选择动作
                action = random.choice(executable_actions)
                
                try:
                    current_state = action.execute(current_state)
                    current_actions.append(action)
                    total_cost += action.duration
                except Exception:
                    break
                
                # 检查是否达到目标
                if self._is_goal_achieved(current_state, goal_state):
                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_sequence = current_actions.copy()
                    break
            
            self.nodes_expanded += 1
        
        if best_sequence:
            action_sequence = ActionSequence(
                id=f"sampling_{int(time.time())}",
                actions=best_sequence,
                initial_state=initial_state,
                goal_state=goal_state
            )
            
            return PlanningResult(
                success=True,
                action_sequence=action_sequence,
                planning_time=time.time() - self.planning_start_time,
                nodes_expanded=self.nodes_expanded,
                solution_cost=best_cost,
                solution_length=len(best_sequence),
                algorithm=self.algorithm,
                metadata={"iterations": max_iterations}
            )
        
        return self._create_failure_result()
    
    def _get_successors(self, node: PlanningNode, available_actions: List[Action], 
                        goal_state: Dict[str, Any]) -> List[PlanningNode]:
        """获取后继节点"""
        successors = []
        
        for action in available_actions:
            if action.can_execute(node.state):
                try:
                    # 复制状态并执行动作
                    new_state = copy.deepcopy(node.state)
                    new_state = action.execute(new_state)
                    
                    # 创建新动作对象
                    new_action = Action(
                        id=f"{action.id}_{node.depth}",
                        name=action.name,
                        action_type=action.action_type,
                        parameters=copy.deepcopy(action.parameters),
                        preconditions=copy.deepcopy(action.preconditions),
                        effects=copy.deepcopy(action.effects),
                        duration=action.duration,
                        success_probability=action.success_probability
                    )
                    
                    # 计算启发式值
                    heuristic = self.heuristic_calculator.calculate(new_state, goal_state, available_actions)
                    
                    # 创建后继节点
                    successor = PlanningNode(
                        state=new_state,
                        actions=node.actions + [new_action],
                        cost=node.cost + action.duration,
                        heuristic=heuristic,
                        total_cost=node.cost + action.duration + heuristic,
                        depth=node.depth + 1,
                        parent=node
                    )
                    
                    successors.append(successor)
                    
                except Exception:
                    continue
        
        # 如果没有找到任何后继节点，尝试创建默认动作以确保进展
        if not successors and node.depth < self.max_depth:
            try:
                # 创建一个简单的状态改变动作
                new_state = copy.deepcopy(node.state)
                new_state['_step'] = new_state.get('_step', 0) + 1
                
                # 创建虚拟动作
                default_action = Action(
                    id=f"default_{node.depth}",
                    name="default_progress",
                    action_type=ActionType.NAVIGATION,
                    parameters={},
                    preconditions={},
                    effects={"_step": new_state['_step']},
                    duration=1.0,
                    success_probability=1.0
                )
                
                heuristic = self.heuristic_calculator.calculate(new_state, goal_state, available_actions)
                
                successor = PlanningNode(
                    state=new_state,
                    actions=node.actions + [default_action],
                    cost=node.cost + 1.0,
                    heuristic=heuristic,
                    total_cost=node.cost + 1.0 + heuristic,
                    depth=node.depth + 1,
                    parent=node
                )
                
                successors.append(successor)
            except Exception:
                pass
        
        return successors
    
    def _is_goal_achieved(self, current_state: Dict[str, Any], goal_state: Dict[str, Any]) -> bool:
        """检查是否达到目标状态"""
        if not goal_state:
            return True
        
        try:
            matched_goals = 0
            total_goals = len(goal_state)
            
            for key, goal_value in goal_state.items():
                current_value = current_state.get(key)
                
                if current_value is None:
                    # 如果当前状态没有这个键，检查是否是可选目标
                    if key.startswith('_'):
                        # 以下划线开头的键是元数据，可以忽略
                        matched_goals += 1
                        continue
                    else:
                        return False
                
                # 灵活的目标匹配
                if isinstance(goal_value, (int, float)):
                    # 数值类型：允许小的误差
                    if isinstance(current_value, (int, float)):
                        if abs(current_value - goal_value) < 0.001:
                            matched_goals += 1
                        else:
                            return False
                    else:
                        return False
                elif isinstance(goal_value, str):
                    # 字符串类型：忽略大小写和空格
                    if isinstance(current_value, str):
                        if current_value.strip().lower() == goal_value.strip().lower():
                            matched_goals += 1
                        else:
                            return False
                    else:
                        return False
                elif isinstance(goal_value, bool):
                    # 布尔类型：严格匹配
                    if current_value == goal_value:
                        matched_goals += 1
                    else:
                        return False
                elif isinstance(goal_value, (list, tuple)):
                    # 列表类型：检查包含关系
                    if isinstance(current_value, (list, tuple)):
                        if set(goal_value) == set(current_value):
                            matched_goals += 1
                        else:
                            return False
                    else:
                        return False
                elif isinstance(goal_value, dict):
                    # 字典类型：递归检查
                    if isinstance(current_value, dict):
                        if self._is_goal_achieved(current_value, goal_value):
                            matched_goals += 1
                        else:
                            return False
                    else:
                        return False
                else:
                    # 其他类型：直接比较
                    if current_value == goal_value:
                        matched_goals += 1
                    else:
                        return False
            
            # 如果所有目标都匹配，返回True
            return matched_goals == total_goals
            
        except Exception as e:
            # 如果检查过程中出现异常，返回False
            if hasattr(self, 'logger'):
                self.logger.warning(f"Goal check failed with exception: {str(e)}")
            return False
    
    def _create_success_result(self, node: PlanningNode, available_actions: List[Action],
                               goal_state: Dict[str, Any]) -> PlanningResult:
        """创建成功结果"""
        # 修复：从第一个动作的参数中获取初始状态，如果失败则使用空字典
        initial_state = {}
        if node.actions and len(node.actions) > 0:
            # 从第一个动作的参数中提取初始状态
            first_action_params = node.actions[0].parameters
            if 'initial_state' in first_action_params:
                initial_state = first_action_params['initial_state']
            else:
                # 如果没有初始状态参数，尝试从节点状态中推断
                initial_state = node.state
        
        action_sequence = ActionSequence(
            id=f"{self.algorithm.value}_{int(time.time())}",
            actions=node.actions,
            initial_state=initial_state,
            goal_state=goal_state
        )
        
        return PlanningResult(
            success=True,
            action_sequence=action_sequence,
            planning_time=time.time() - self.planning_start_time,
            nodes_expanded=self.nodes_expanded,
            solution_cost=node.cost,
            solution_length=len(node.actions),
            algorithm=self.algorithm,
            metadata={"final_state": node.state}
        )
    
    def _create_failure_result(self) -> PlanningResult:
        """创建失败结果"""
        return PlanningResult(
            success=False,
            action_sequence=None,
            planning_time=time.time() - self.planning_start_time,
            nodes_expanded=self.nodes_expanded,
            solution_cost=float('inf'),
            solution_length=0,
            algorithm=self.algorithm,
            metadata={"reason": "No solution found within time/depth limits"}
        )