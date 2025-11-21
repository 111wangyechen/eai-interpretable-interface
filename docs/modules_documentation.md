# AuDeRe和LogicGuard模块文档

本文档详细介绍了系统中新增的两个关键模块：AuDeRe（智能动作规划和建议）和LogicGuard（状态转换建模和验证）模块的功能、配置选项和使用方法。

## 目录
- [AuDeRe模块](#audere模块)
  - [功能概述](#功能概述)
  - [配置选项](#配置选项)
  - [使用示例](#使用示例)
  - [API参考](#api参考)
- [LogicGuard模块](#logicguard模块)
  - [功能概述](#功能概述-1)
  - [配置选项](#配置选项-1)
  - [使用示例](#使用示例-1)
  - [API参考](#api参考-1)
- [模块集成](#模块集成)
  - [与现有系统的集成](#与现有系统的集成)
  - [集成测试](#集成测试)
- [最佳实践](#最佳实践)

## AuDeRe模块

### 功能概述

AuDeRe（智能动作决策与建议）模块是一个高级动作规划增强组件，提供以下核心功能：

- **自然语言目标解释**：将自然语言描述的目标转换为结构化的状态表示
- **智能动作建议**：基于当前状态和目标状态，提供最适合的动作序列建议
- **意图理解**：分析用户意图，识别隐含的目标和约束
- **置信度评估**：为生成的动作建议提供置信度评分

### 配置选项

AuDeRe模块支持以下配置选项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_natural_language_goal_interpretation` | Boolean | `True` | 是否启用自然语言目标解释功能 |
| `enable_action_suggestions` | Boolean | `True` | 是否启用动作建议功能 |
| `confidence_threshold` | Float | `0.7` | 动作建议的置信度阈值（0.0-1.0） |
| `max_suggestions` | Integer | `5` | 最大动作建议数量 |
| `context_awareness` | Boolean | `True` | 是否启用上下文感知功能 |
| `model_path` | String | `"models/aude_re/default_model"` | 模型文件路径 |

示例配置：

```python
aude_re_config = {
    'enable_natural_language_goal_interpretation': True,
    'enable_action_suggestions': True,
    'confidence_threshold': 0.75,
    'max_suggestions': 3,
    'context_awareness': True
}
```

### 使用示例

#### 基本用法

```python
from action_sequencing.aude_re import create_aude_re

# 创建AuDeRe实例
aude_re = create_aude_re(aude_re_config)

# 示例1：自然语言目标解释
natural_language_goal = "我需要从冰箱拿一瓶水"
interpreted_goal = aude_re.interpret_natural_language_goal(natural_language_goal)
print(f"解释后的目标状态: {interpreted_goal}")

# 示例2：生成动作建议
initial_state = {
    "agent_at_location": "kitchen",
    "fridge_open": "False",
    "holding_water": "False"
}
goal_state = {
    "holding_water": "True"
}

available_actions = [
    # 这里应该是您系统中的可用动作列表
    # 例如：Move, Open, PickUp等动作
]

action_suggestions = aude_re.generate_action_suggestions(
    initial_state=initial_state,
    goal_state=goal_state,
    available_actions=available_actions
)

print("动作建议:")
for suggestion in action_suggestions:
    print(f"- {suggestion['action_name']} (置信度: {suggestion['confidence']})")
```

#### 与ActionSequencer集成

```python
from action_sequencing.action_sequencer import ActionSequencer

# 配置ActionSequencer以启用AuDeRe
sequencer_config = {
    'enable_aude_re': True,
    'aude_re': aude_re_config
}

# 创建ActionSequencer实例
sequencer = ActionSequencer(config=sequencer_config)

# 使用配置了AuDeRe的ActionSequencer生成动作序列
request = SequencingRequest(
    request_id="test_request",
    initial_state=initial_state,
    goal_state=goal_state,
    natural_language_goal="我需要从冰箱拿一瓶水"
)

response = sequencer.generate_sequence(request)
```

### API参考

#### create_aude_re(config)

创建并返回AuDeRe实例的工厂函数。

**参数：**
- `config` (Dict): 配置字典，包含AuDeRe的配置选项

**返回值：**
- `AuDeRe` 实例

#### AuDeRe.interpret_natural_language_goal(natural_language_goal)

将自然语言描述的目标转换为结构化状态表示。

**参数：**
- `natural_language_goal` (String): 自然语言描述的目标

**返回值：**
- `Dict`: 结构化的目标状态表示

#### AuDeRe.generate_action_suggestions(initial_state, goal_state, available_actions)

基于当前状态和目标状态生成动作建议。

**参数：**
- `initial_state` (Dict): 初始状态
- `goal_state` (Dict): 目标状态
- `available_actions` (List): 可用动作列表

**返回值：**
- `List[Dict]`: 动作建议列表，每项包含动作信息和置信度

#### AuDeRe.evaluate_plan_confidence(plan, initial_state, goal_state)

评估一个动作序列的置信度。

**参数：**
- `plan` (List): 动作序列
- `initial_state` (Dict): 初始状态
- `goal_state` (Dict): 目标状态

**返回值：**
- `Float`: 置信度评分（0.0-1.0）

## LogicGuard模块

### 功能概述

LogicGuard模块是一个高级状态转换验证和保护组件，提供以下核心功能：

- **时序逻辑验证**：使用LTL（线性时序逻辑）公式验证状态转换序列的正确性
- **运行时错误检测**：检测状态不一致、无效转换、前置条件缺失等错误
- **自动错误纠正**：自动修正检测到的错误，确保系统稳定性
- **安全保障**：强制执行安全属性，防止危险状态转换

### 配置选项

LogicGuard模块支持以下配置选项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_ltl_validation` | Boolean | `True` | 是否启用LTL验证 |
| `enable_runtime_error_detection` | Boolean | `True` | 是否启用运行时错误检测 |
| `enable_auto_correction` | Boolean | `True` | 是否启用自动纠正功能 |
| `ltl_specifications` | List[Dict] | `[]` | LTL规范列表 |
| `error_detection_rules` | List[String] | `["inconsistent_state", "invalid_transition_order", "missing_precondition"]` | 错误检测规则列表 |
| `correction_strategies` | List[String] | `["state_recovery", "action_replanning"]` | 纠正策略列表 |
| `model_path` | String | `"models/logic_guard/default_model"` | 模型文件路径 |

LTL规范格式：
```python
{
    'name': '安全属性名称',
    'formula': 'LTL公式',
    'priority': 'high/medium/low'
}
```

示例配置：

```python
logic_guard_config = {
    'enable_ltl_validation': True,
    'enable_runtime_error_detection': True,
    'enable_auto_correction': True,
    'ltl_specifications': [
        {
            'name': '安全区域约束',
            'formula': 'G (at_location != "danger_zone")',
            'priority': 'high'
        },
        {
            'name': '对象操作约束',
            'formula': 'G (holding_object -> can_hold_object)',
            'priority': 'high'
        }
    ],
    'error_detection_rules': [
        'inconsistent_state',
        'invalid_transition_order',
        'missing_precondition',
        'postcondition_violation'
    ],
    'correction_strategies': ['state_recovery', 'action_replanning']
}
```

### 使用示例

#### 基本用法

```python
from transition_modeling.logic_guard import create_logic_guard

# 创建LogicGuard实例
logic_guard = create_logic_guard(logic_guard_config)

# 示例1：LTL规范验证
initial_state = {"at_location": "start", "holding_object": "False"}
transitions = [
    # 这里是状态转换列表
    # 例如：MoveTo, PickUp等转换
]
goal_state = {"at_location": "target", "holding_object": "True"}

validation_result = logic_guard.validate_ltl_specifications(
    initial_state=initial_state,
    transitions=transitions,
    goal_state=goal_state
)

print(f"LTL验证结果: {validation_result['valid']}")

# 示例2：运行时错误检测
errors = logic_guard.detect_runtime_errors(initial_state, transitions)

if errors:
    print("检测到错误:")
    for error in errors:
        print(f"- {error['type']}: {error['message']}")
    
    # 自动纠正错误
    corrected_transitions = logic_guard.correct_sequence(
        initial_state=initial_state,
        transitions=transitions,
        errors=errors,
        goal_state=goal_state
    )
    print("已尝试纠正错误")
```

#### 与TransitionModeler集成

```python
from transition_modeling.transition_modeler import TransitionModeler

# 配置TransitionModeler以启用LogicGuard
modeler_config = {
    'enable_logic_guard': True,
    'logic_guard': logic_guard_config
}

# 创建TransitionModeler实例
modeler = TransitionModeler(config=modeler_config)

# 使用配置了LogicGuard的TransitionModeler进行状态转换建模
request = ModelingRequest(
    initial_state=initial_state,
    goal_state=goal_state
)

response = modeler.model_transitions(request)

# 检查是否有逻辑验证警告
if response.logic_warnings:
    print("LogicGuard警告:")
    for warning in response.logic_warnings:
        print(f"- {warning}")
```

### API参考

#### create_logic_guard(config)

创建并返回LogicGuard实例的工厂函数。

**参数：**
- `config` (Dict): 配置字典，包含LogicGuard的配置选项

**返回值：**
- `LogicGuard` 实例

#### LogicGuard.validate_ltl_specifications(initial_state, transitions, goal_state)

使用LTL规范验证状态转换序列。

**参数：**
- `initial_state` (Dict): 初始状态
- `transitions` (List): 状态转换序列
- `goal_state` (Dict): 目标状态

**返回值：**
- `Dict`: 包含验证结果和详细信息

#### LogicGuard.detect_runtime_errors(initial_state, transitions)

检测运行时错误。

**参数：**
- `initial_state` (Dict): 初始状态
- `transitions` (List): 状态转换序列

**返回值：**
- `List[Dict]`: 检测到的错误列表

#### LogicGuard.correct_sequence(initial_state, transitions, errors, goal_state)

自动纠正检测到的错误。

**参数：**
- `initial_state` (Dict): 初始状态
- `transitions` (List): 状态转换序列
- `errors` (List[Dict]): 检测到的错误列表
- `goal_state` (Dict): 目标状态

**返回值：**
- `List`: 修正后的状态转换序列

#### LogicGuard.get_validation_statistics()

获取验证统计信息。

**返回值：**
- `Dict`: 包含验证统计信息的字典

## 模块集成

### 与现有系统的集成

AuDeRe和LogicGuard模块都设计为可插拔组件，可以无缝集成到现有的动作规划和状态转换建模系统中。

#### 集成架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Goal Parser    │────▶│  AuDeRe         │────▶│  Action         │
│                 │     │  (智能建议)     │     │  Sequencer      │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Execution      │◀────│  Transition     │◀────│  LogicGuard     │
│  Engine         │     │  Modeler        │     │  (验证保护)     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### 配置文件示例

在`enhanced_config.yaml`中配置这两个模块：

```yaml
# AuDeRe配置
aude_re:
  enable_natural_language_goal_interpretation: true
  enable_action_suggestions: true
  confidence_threshold: 0.7
  max_suggestions: 5
  context_awareness: true

# LogicGuard配置
logic_guard:
  enable_ltl_validation: true
  enable_runtime_error_detection: true
  enable_auto_correction: true
  ltl_specifications:
    - name: "安全属性"
      formula: "G (at_location != \"danger_zone\")"
      priority: "high"
    - name: "操作约束"
      formula: "G (holding_object -> can_hold_object)"
      priority: "high"
    - name: "任务完成约束"
      formula: "F (task_completed = true)"
      priority: "medium"
  error_detection_rules:
    - "inconsistent_state"
    - "invalid_transition_order"
    - "missing_precondition"
    - "postcondition_violation"
  correction_strategies:
    - "state_recovery"
    - "action_replanning"
    - "constraint_relaxation"
```

### 集成测试

系统提供了专门的集成测试脚本来验证两个模块的功能和与现有系统的集成：

```bash
python test_aude_re_logic_guard_integration.py
```

测试报告将生成在当前目录，文件名为`aude_re_logic_guard_test_report.json`。

## 最佳实践

### AuDeRe模块最佳实践

1. **置信度阈值调整**：
   - 对于安全关键型应用，建议将置信度阈值设置得更高（如0.8-0.9）
   - 对于探索性任务，可以使用较低的阈值（如0.6-0.7）

2. **上下文信息**：
   - 尽可能提供丰富的上下文信息，以提高建议的准确性
   - 包括历史动作、环境描述和用户偏好

3. **错误处理**：
   - 实现适当的错误处理机制，处理AuDeRe可能返回的低置信度建议
   - 在关键任务中，考虑在执行前进行人工确认

### LogicGuard模块最佳实践

1. **LTL规范设计**：
   - 从关键安全属性开始设计LTL规范
   - 使用分层方法：先确保安全，再优化性能
   - 避免过于复杂的LTL公式，可能导致验证困难

2. **错误检测与纠正**：
   - 优先启用错误检测功能，即使不启用自动纠正
   - 记录所有检测到的错误，用于系统改进
   - 在生产环境中，考虑先监控一段时间再启用自动纠正

3. **性能优化**：
   - 对于大型系统，考虑对LTL验证进行分批处理
   - 根据系统负载动态调整验证频率

### 综合使用建议

1. **渐进式部署**：
   - 从非关键任务开始部署这两个模块
   - 收集使用数据，逐步扩展到更复杂的任务

2. **监控与反馈**：
   - 实现详细的日志记录，捕获模块的决策过程
   - 定期审查验证结果和错误报告
   - 建立反馈机制，持续改进模块性能

3. **模块协同**：
   - AuDeRe生成的动作建议可以作为LogicGuard验证的输入
   - LogicGuard检测到的错误可以反馈给AuDeRe进行改进
   - 两个模块协同工作，实现更智能、更安全的系统行为

---

本文档将随着模块的更新而不断完善。如有任何问题或建议，请联系开发团队。