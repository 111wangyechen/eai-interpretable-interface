基于提供的代码库内容，以下是针对动作序列和转移建模模块的问题排查及具体修改建议：


### 一、状态转换（`state_manager.py`）核心问题及修改
#### 问题1：条件解析逻辑脆弱
`StateTransition`的`_evaluate_condition`方法使用简单字符串分割处理条件（如`=`、`!=`），存在以下问题：
- 无法处理包含多个运算符的条件（如`count>5 and name="test"`）
- 布尔值比较错误（如状态中是`True`（布尔型），条件是`key=True`（字符串解析）会判定为不匹配）
- 数值比较未处理类型转换（如状态值为`10`（int），条件`key>5`会因字符串比较出错）

#### 修改方案：
```python
# state_manager.py 中 _evaluate_condition 方法重构
import re

def _evaluate_condition(self, condition: str, state: Dict[str, Any]) -> bool:
    """使用正则表达式解析条件，支持多种类型比较"""
    # 匹配运算符：==, !=, >, <, >=, <=
    pattern = r'(\w+)\s*(==|!=|>|<|>=|<=)\s*(.+)'
    match = re.match(pattern, condition.strip())
    if not match:
        # 处理简单存在性判断（如 "has_key"）
        return state.get(condition.strip(), False)
    
    key, op, value_str = match.groups()
    current_value = state.get(key)
    
    # 尝试转换值类型（保持与状态中值的类型一致）
    try:
        # 若状态值是数值，转换条件值为相同类型
        if isinstance(current_value, (int, float)):
            value = float(value_str)
        # 若状态值是布尔，解析条件值为布尔
        elif isinstance(current_value, bool):
            value = value_str.lower() == "true"
        else:
            # 字符串比较
            value = value_str.strip('"\'')  # 移除引号
    except (ValueError, TypeError):
        value = value_str
    
    # 执行比较
    try:
        if op == '==':
            return current_value == value
        elif op == '!=':
            return current_value != value
        elif op == '>':
            return current_value > value
        elif op == '<':
            return current_value < value
        elif op == '>=':
            return current_value >= value
        elif op == '<=':
            return current_value <= value
    except (TypeError, ValueError):
        return False
```


### 二、数据加载（`data_loader.py`）参数不匹配问题
#### 问题1：`StateTransition`初始化参数错误
`data_loader.py`的`create_state_transitions`方法中，创建`StateTransition`时传入了`id`和`action_id`参数，但`state_manager.py`中`StateTransition`类的定义不含这两个字段（仅含`action_name`），导致实例化失败。

#### 修改方案：
```python
# data_loader.py 中 create_state_transitions 方法调整
def create_state_transitions(self, actions: List[Action], initial_state: Dict[str, Any]) -> List[StateTransition]:
    transitions = []
    current_state = initial_state.copy()
    
    for i, action in enumerate(actions):
        try:
            next_state = action.execute(current_state)
            # 匹配 StateTransition 类的字段定义（使用 action_name 而非 action_id）
            transition = StateTransition(
                from_state=current_state.copy(),
                to_state=next_state.copy(),
                action_name=action.name,  # 修正：使用 action.name 对应 action_name 字段
                probability=action.success_probability,  # 补充概率信息
                cost=action.cost,
                duration=action.duration,
                preconditions=action.preconditions,
                effects=action.effects
            )
            transitions.append(transition)
            current_state = next_state
        except Exception as e:
            self.logger.warning(f"Failed to create transition for action {action.id}: {str(e)}")
            continue
    return transitions
```


### 三、动作序列优化（`aude_re.py`）缓存与迭代问题
#### 问题1：缓存键生成不稳定
`optimize_action_sequence`方法使用`hash(str(sequence.actions))`作为缓存键，而`str(sequence.actions)`的结果依赖于`Action`类的`__str__`实现，可能因内存地址等因素变化，导致缓存失效。

#### 问题2：优化迭代未收敛判断
固定迭代次数（`self.config.optimization_iterations`），未检查序列是否已稳定，造成无效计算。

#### 修改方案：
```python
# aude_re.py 中 optimize_action_sequence 方法优化
def optimize_action_sequence(self, sequence: ActionSequence, optimization_goals: Dict[str, Any]) -> ActionSequence:
    # 生成稳定的缓存键（基于动作的可哈希属性）
    def get_stable_hash(actions):
        return hash(tuple(
            (a.id, a.name, tuple(sorted(a.preconditions)), tuple(sorted(a.effects))) 
            for a in actions
        ))
    
    # 检查缓存
    if self._cache is not None:
        cache_key = f"optimize_sequence:{get_stable_hash(sequence.actions)}:{hash(frozenset(optimization_goals.items()))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
    
    optimized_actions = sequence.actions.copy()
    prev_actions_hash = None
    iterations = 0
    
    # 迭代优化直到收敛或达到最大次数
    while iterations < self.config.optimization_iterations:
        # 1. 消除冗余动作
        optimized_actions = self._remove_redundant_actions(optimized_actions)
        
        # 2. 根据目标调整顺序
        if optimization_goals.get('minimize_duration', False):
            optimized_actions = self._sort_by_duration(optimized_actions)
        # ... 其他优化目标
        
        # 检查是否收敛（动作序列未变化）
        current_hash = get_stable_hash(optimized_actions)
        if current_hash == prev_actions_hash:
            break  # 已收敛，停止迭代
        prev_actions_hash = current_hash
        iterations += 1
    
    # 后续创建优化序列和缓存逻辑不变...
    optimized_sequence = ActionSequence(
        id=f"{sequence.id}_optimized",
        actions=optimized_actions,
        initial_state=sequence.initial_state,
        goal_state=sequence.goal_state
    )
    
    if self._cache is not None:
        self._cache[cache_key] = optimized_sequence
    
    return optimized_sequence
```


### 四、规划算法（`action_planner.py`）启发式计算问题
#### 问题1：启发式缓存键生成低效
`HeuristicCalculator`的`_combined_heuristic`方法中，缓存键使用`str(sorted(hashable_current.items()))`，对复杂状态会生成冗长字符串，影响性能。

#### 修改方案：
```python
# action_planner.py 中 HeuristicCalculator 优化
def _combined_heuristic(self, current_state: Dict[str, Any], goal_state: Dict[str, Any], available_actions: List[Action]) -> float:
    # 生成紧凑的哈希键（使用 tuple 而非 str）
    def make_hashable(value):
        if isinstance(value, dict):
            return tuple(sorted((k, make_hashable(v)) for k, v in value.items()))
        elif isinstance(value, list):
            return tuple(make_hashable(v) for v in value)
        return value
    
    # 直接使用可哈希的 tuple 作为缓存键
    hashable_current = make_hashable(current_state)
    hashable_goal = make_hashable(goal_state)
    cache_key = (hashable_current, hashable_goal)
    
    if cache_key in self.heuristic_cache:
        return self.heuristic_cache[cache_key]
    
    # 后续启发式计算逻辑不变...
    # ...
    
    self.heuristic_cache[cache_key] = final_heuristic
    return final_heuristic
```


### 五、测试用例（`test_action_sequencing.py`）覆盖不足
#### 问题1：未测试布尔值类型状态
测试用例中状态值使用字符串`"True"`，但实际场景可能用布尔`True`，导致条件判断漏洞未被发现。

#### 修改方案：
```python
# test_action_sequencing.py 中补充测试用例
def test_state_transition_boolean_values(self):
    """测试布尔值状态的转换判断"""
    # 初始状态使用布尔值（而非字符串）
    self.state_manager.update_state({"agent_location": "start", "agent_at_start": True})
    
    transition = StateTransition(
        from_state={"agent_location": "start"},
        to_state={"agent_location": "kitchen"},
        action_name="move_action",
        preconditions=["agent_at_start==True"],  # 使用 == 运算符
        effects=["agent_at_kitchen=True"]
    )
    
    self.state_manager.add_transition(transition)
    result = self.state_manager.apply_action("move_action")
    self.assertTrue(result)  # 确保布尔值状态能被正确识别
    self.assertEqual(self.state_manager.get_current_state().get_value("agent_location"), "kitchen")
```


### 六、总结：关键改进点
1. **状态转换稳健性**：通过正则解析条件，支持多类型比较，修复布尔/数值判断错误。
2. **参数一致性**：对齐`StateTransition`的定义与使用，解决实例化失败问题。
3. **优化效率**：改进缓存键生成方式，增加收敛判断，减少无效迭代。
4. **性能与准确性**：优化启发式计算的缓存机制，提升复杂状态下的处理效率。
5. **测试覆盖**：补充布尔值等边缘场景测试，避免潜在逻辑漏洞。

这些修改可显著提升模块的稳定性、效率和兼容性，尤其适合处理复杂环境下的动作序列规划。