# Action Sequencing Module

## 概述

Action Sequencing模块是EAI Challenge项目中的核心组件之一，负责将高级目标描述转换为具体的、可执行的动作序列。该模块集成了多种规划算法、状态管理功能和数据加载器，为智能体提供完整的动作规划解决方案。

## 功能特性

### 🎯 核心功能
- **动作序列生成**: 从目标状态到动作序列的自动规划
- **多种规划算法**: 支持BFS、DFS、A*、贪心、RRT等算法
- **状态管理**: 完整的环境状态跟踪和转换
- **数据集成**: 支持VirtualHome和Behavior数据集
- **性能优化**: 内置缓存和启发式优化

### 🛠 技术特点
- **模块化设计**: 清晰的组件分离和接口定义
- **类型安全**: 完整的类型注解和数据验证
- **可扩展性**: 易于添加新的算法和数据类型
- **测试覆盖**: 全面的单元测试和集成测试
- **文档完整**: 详细的使用示例和API文档

## 安装和配置

### 系统要求
- Python 3.8+
- Ubuntu 18.04+ (推荐)
- 内存: 至少4GB
- 存储: 至少2GB可用空间

### 依赖安装

```bash
# 安装基础依赖
pip install numpy pandas typing-extensions

# 安装可选依赖 (用于高级功能)
pip install matplotlib seaborn  # 可视化
pip install pytest pytest-cov  # 测试覆盖率
```

### 文件结构

```
action_sequencing/
├── __init__.py              # 模块初始化和公共接口
├── action_data.py           # 动作和序列数据结构
├── state_manager.py        # 环境状态管理
├── action_planner.py        # 规划算法实现
├── action_sequencer.py      # 核心序列生成器
├── data_loader.py           # 数据集加载器
├── test_action_sequencing.py # 测试文件
├── example_usage.py         # 使用示例
└── README.md               # 本文档
```

## 快速开始

### 基础使用

```python
from action_sequencing import (
    Action, ActionType, SequencingRequest, 
    create_action_sequencer
)

# 定义动作
actions = [
    Action(
        id="walk_to_kitchen",
        name="WalkToKitchen",
        action_type=ActionType.NAVIGATION,
        parameters={"target": "kitchen"},
        preconditions=["agent_in_living_room"],
        effects=["agent_in_kitchen"],
        duration=3.0
    )
]

# 创建请求
request = SequencingRequest(
    initial_state={"agent_in_living_room": True, "agent_in_kitchen": False},
    goal_state={"agent_in_kitchen": True},
    available_actions=actions
)

# 生成序列
sequencer = create_action_sequencer()
response = sequencer.generate_sequence(request)

if response.success:
    print(f"生成动作序列: {len(response.action_sequence.actions)} 个动作")
    for action in response.action_sequence.actions:
        print(f"- {action.name}")
```

### 快速API

```python
from action_sequencing import quick_sequence_generation, PlanningAlgorithm

# 使用快速API
response = quick_sequence_generation(
    initial_state={"at_start": True, "at_goal": False},
    goal_state={"at_goal": True},
    available_actions=[{
        'id': 'move',
        'name': 'MoveToGoal',
        'type': 'navigation',
        'preconditions': ['at_start'],
        'effects': ['at_goal'],
        'duration': 2.0
    }],
    algorithm=PlanningAlgorithm.ASTAR
)
```

## 核心组件

### 1. ActionSequencer (核心序列生成器)

负责协调整个规划过程的主要组件。

```python
from action_sequencing import ActionSequencer, SequencingConfig, PlanningAlgorithm

config = SequencingConfig(
    planning_algorithm=PlanningAlgorithm.ASTAR,
    max_depth=50,
    max_time=30.0,
    enable_cache=True
)

sequencer = ActionSequencer(config)
response = sequencer.generate_sequence(request)
```

### 2. ActionPlanner (规划算法)

实现多种搜索和规划算法。

**支持的算法:**
- `BFS`: 广度优先搜索
- `DFS`: 深度优先搜索  
- `ASTAR`: A*搜索算法
- `GREEDY`: 贪心最佳优先搜索
- `RRT`: 快速随机探索树

```python
from action_sequencing import ActionPlanner, PlanningAlgorithm, HeuristicType

planner = ActionPlanner(
    algorithm=PlanningAlgorithm.ASTAR,
    heuristic_type=HeuristicType.GOAL_DISTANCE
)

result = planner.plan(
    initial_state=initial_state,
    goal_state=goal_state,
    available_actions=actions
)
```

### 3. StateManager (状态管理)

管理环境状态和状态转换。

```python
from action_sequencing import StateManager, StateTransition

state_manager = StateManager()
state_manager.update_state(new_state)

# 添加状态转换
transition = StateTransition(
    id="move_transition",
    from_state={"location": "A"},
    to_state={"location": "B"},
    action_id="move_action"
)
state_manager.add_transition(transition)
```

### 4. DataLoader (数据加载)

加载和处理VirtualHome和Behavior数据集。

```python
from action_sequencing import DataLoader, DatasetConfig

config = DatasetConfig(
    virtualhome_path="virtualhome-00000-of-00001.parquet",
    behavior_path="behavior-00000-of-00001.parquet",
    max_samples=1000
)

loader = DataLoader(config)
virtualhome_records = loader.load_virtualhome_data()
behavior_records = loader.load_behavior_data()
```

## 数据格式

### Action数据结构

```python
Action(
    id="unique_action_id",
    name="HumanReadableName", 
    action_type=ActionType.NAVIGATION,  # NAVIGATION, MANIPULATION, OBSERVATION, COMMUNICATION
    parameters={"target": "kitchen", "speed": 1.0},
    preconditions=["agent_at_living_room"],
    effects=["agent_at_kitchen"],
    duration=2.0,
    success_probability=0.95
)
```

### 状态表示

状态使用字典格式表示，键为状态变量名，值为布尔值或其他数据类型：

```python
state = {
    "agent_location": "kitchen",
    "holding_object": "cup",
    "door_open": True,
    "light_on": False
}
```

### 数据集格式

#### VirtualHome记录
```python
VirtualHomeRecord(
    task_id="task_001",
    task_description="Make coffee",
    actions='[{"name": "walk", "type": "navigation", ...}]',
    initial_state='{"agent_location": "bedroom"}',
    goal_state='{"agent_location": "kitchen"}',
    difficulty="easy"
)
```

#### Behavior记录
```python
BehaviorRecord(
    behavior_id="behavior_001", 
    behavior_type="social",
    actions='[{"name": "greet", "type": "communication", ...}]',
    context='{"location": "living_room"}',
    outcomes='{"response": "positive"}'
)
```

## 规划算法详解

### A*算法
最常用的规划算法，结合了路径成本和启发式估计。

**适用场景:** 
- 状态空间较大但结构清晰
- 需要最优解
- 有良好的启发式函数

### BFS算法
保证找到最短路径（按动作数量计算）。

**适用场景:**
- 状态空间较小
- 需要最少动作数
- 所有动作成本相同

### 贪心算法
只考虑启发式函数，速度快但不保证最优。

**适用场景:**
- 需要快速解
- 最优性不重要
- 启发式函数质量高

## 性能优化

### 启发式函数
- `GOAL_DISTANCE`: 基于目标状态的距离估计
- `ACTION_COUNT`: 基于剩余动作数量
- `STATE_DIFFERENCE`: 基于状态差异

### 缓存策略
```python
config = SequencingConfig(
    enable_cache=True,
    cache_size=1000,
    cache_ttl=3600  # 1小时
)
```

### 并行处理
对于大规模问题，可以考虑并行规划：

```python
# 多算法并行规划
algorithms = [PlanningAlgorithm.ASTAR, PlanningAlgorithm.GREEDY, PlanningAlgorithm.BFS]
responses = []

for algorithm in algorithms:
    sequencer = create_action_sequencer(algorithm=algorithm)
    response = sequencer.generate_sequence(request)
    responses.append(response)

# 选择最佳结果
best_response = min(responses, key=lambda r: r.execution_time if r.success else float('inf'))
```

## 测试

### 运行单元测试

```bash
# 在Ubuntu系统中
cd /path/to/action_sequencing
python3 -m pytest test_action_sequencing.py -v

# 或者直接运行
python3 test_action_sequencing.py
```

### 测试覆盖率

```bash
pip install pytest-cov
python3 -m pytest test_action_sequencing.py --cov=. --cov-report=html
```

### 运行示例

```bash
python3 example_usage.py
```

## 常见问题

### Q: 规划失败怎么办？
A: 检查以下几点：
1. 动作的前置条件和效果是否正确定义
2. 目标状态是否可达
3. 增加max_depth或max_time限制
4. 尝试不同的规划算法

### Q: 如何处理大型数据集？
A: 使用以下策略：
1. 设置max_samples限制样本数量
2. 启用数据缓存
3. 使用数据采样
4. 分批处理数据

### Q: 如何自定义启发式函数？
A: 继承HeuristicCalculator类：

```python
class CustomHeuristic(HeuristicCalculator):
    def calculate(self, current_state, goal_state):
        # 自定义启发式逻辑
        return custom_score
```

### Q: 如何添加新的动作类型？
A: 扩展ActionType枚举：

```python
from enum import Enum

class ActionType(Enum):
    NAVIGATION = "navigation"
    MANIPULATION = "manipulation"
    OBSERVATION = "observation"
    COMMUNICATION = "communication"
    CUSTOM_TYPE = "custom"  # 新增类型
```

## API参考

### 主要类和方法

#### ActionSequencer
- `generate_sequence(request: SequencingRequest) -> SequencingResponse`
- `get_statistics() -> dict`
- `clear_cache() -> None`

#### ActionPlanner  
- `plan(initial_state, goal_state, available_actions) -> PlanningResult`
- `set_algorithm(algorithm: PlanningAlgorithm) -> None`

#### StateManager
- `update_state(new_state: dict) -> None`
- `get_current_state() -> dict`
- `add_transition(transition: StateTransition) -> None`

#### DataLoader
- `load_virtualhome_data() -> List[VirtualHomeRecord]`
- `load_behavior_data() -> List[BehaviorRecord]`
- `get_dataset_statistics() -> dict`

## 贡献指南

### 开发环境设置

```bash
# 克隆项目
git clone <repository_url>
cd action_sequencing

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python3 -m pytest
```

### 代码规范
- 使用类型注解
- 遵循PEP 8规范
- 添加文档字符串
- 编写单元测试

### 提交流程
1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 联系方式

- 项目主页: [EAI Challenge](https://neurips25-eai.github.io/)
- 问题反馈: 通过GitHub Issues
- 邮箱: eai-challenge@example.com

## 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 实现基础规划算法
- 支持VirtualHome和Behavior数据集
- 完整的测试覆盖

---

**注意**: 本文档会随项目更新而持续完善。如有疑问或建议，请及时反馈。