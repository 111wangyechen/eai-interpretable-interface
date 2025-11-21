# InterPreT集成 - 可解释目标理解模块

## 概述

本项目实现了InterPreT（Interpretable Predicate Transformer）方法在目标理解模块中的集成。InterPreT是一种从语言反馈中学习符号谓词的创新方法，能够将自然语言目标转换为LTL公式和PDDL域定义，并通过用户反馈不断改进解释质量。

## 核心特性

### 🧠 智能目标解释
- **自然语言到LTL转换**: 将用户指令转换为线性时序逻辑公式
- **PDDL域自动生成**: 基于目标自动生成规划域定义
- **多模态理解**: 支持文本、图像等多种输入模态

### 🎓 反馈学习机制
- **交互式学习**: 从用户反馈中学习改进解释
- **谓词演化**: 动态学习和优化符号谓词
- **置信度评估**: 提供解释结果的可信度评分

### 🔧 系统集成
- **模块化设计**: 易于与其他系统集成
- **配置灵活**: 支持多种配置选项
- **性能优化**: 内置缓存和批处理机制

## 文件结构

```
goal_interpretation/
├── interpretable_goal_interpreter.py    # 核心实现文件
├── test_interpretable_interpreter.py    # 测试脚本
├── demo_interpretable_interpreter.py    # 演示脚本
├── README.md                            # 说明文档
└── enhanced_config.yaml                 # 配置文件
```

## 快速开始

### 1. 环境要求

```bash
Python >= 3.8
pip install numpy pyyaml typing-extensions
```

### 2. 基础使用

```python
from interpretable_goal_interpreter import InterpretableGoalInterpreter

# 创建解释器
config = {
    'interpretable': {
        'enabled': True,
        'max_feedback_iterations': 3
    }
}
interpreter = InterpretableGoalInterpreter(config)

# 解释目标
goal = "Pick up the red cup from the table"
ltl_formula, pddl_domain = interpreter.interpret_with_feedback(goal)

print(f"LTL公式: {ltl_formula.formula}")
print(f"置信度: {ltl_formula.confidence}")
print(f"PDDL域: {pddl_domain.name}")
```

### 3. 添加反馈学习

```python
# 添加正面反馈
interpreter.add_feedback(
    text=goal,
    ltl_formula=ltl_formula,
    feedback_type="positive",
    content="Good interpretation of the action",
    confidence=0.9
)

# 添加纠正反馈
interpreter.add_feedback(
    text=goal,
    ltl_formula=ltl_formula,
    feedback_type="correction",
    content="Add temporal constraint for the final state",
    confidence=0.8
)
```

## 核心组件

### 1. InterpretableGoalInterpreter

主要的目标解释器类，提供以下功能：

- `interpret_with_feedback()`: 执行带反馈的目标解释
- `add_feedback()`: 添加用户反馈
- `get_statistics()`: 获取系统统计信息
- `save_learned_predicates()`: 保存学习到的谓词
- `load_learned_predicates()`: 加载学习到的谓词

### 2. InterPreTFeedbackLearner

反馈学习器，负责：

- 从反馈中提取谓词模式
- 更新谓词置信度
- 管理反馈历史

### 3. PDDLDomainBuilder

PDDL域构建器，提供：

- 自动生成PDDL域定义
- 支持自定义谓词和动作
- 生成标准PDDL格式输出

### 4. 数据结构

#### FeedbackRecord
```python
@dataclass
class FeedbackRecord:
    text: str                    # 原始文本
    ltl_formula: str             # LTL公式
    feedback_type: str           # 反馈类型
    content: str                 # 反馈内容
    confidence: float            # 置信度
    timestamp: float             # 时间戳
```

#### SymbolicPredicate
```python
@dataclass
class SymbolicPredicate:
    name: str                   # 谓词名称
    arity: int                  # 参数数量
    confidence: float           # 置信度
    usage_history: List[str]    # 使用历史
```

## 配置选项

### 全局配置
```yaml
interpretable:
  enabled: true                          # 启用InterPreT
  max_feedback_iterations: 3              # 最大反馈迭代次数
```

### LLM配置
```yaml
llm:
  provider: "openai"                      # LLM提供商
  model: "gpt-4"                          # 模型名称
  api_key: "your-api-key"                 # API密钥
  temperature: 0.7                        # 温度参数
  max_tokens: 1000                        # 最大令牌数
```

### PDDL域配置
```yaml
pddl_domain:
  auto_generate: true                     # 自动生成PDDL域
  use_llm: true                          # 使用LLM生成
  default_types:                          # 默认类型
    - "location"
    - "object" 
    - "robot"
  default_predicates:                     # 默认谓词
    - "at(?r - robot, ?l - location)"
    - "holding(?r - robot, ?o - object)"
```

### 反馈学习配置
```yaml
feedback:
  confidence_threshold: 0.7              # 置信度阈值
  learning_rate: 0.1                     # 学习率
  feedback_buffer_size: 100              # 反馈缓冲区大小
```

## 使用示例

### 示例1: 基础目标解释

```python
# 创建解释器
interpreter = InterpretableGoalInterpreter(config)

# 解释简单目标
goal = "Pick up the cup"
ltl_formula, pddl_domain = interpreter.interpret_with_feedback(goal)

print(f"LTL: {ltl_formula.formula}")
# 输出: F (holding(robot, cup) & at(robot, cup_location))
```

### 示例2: 复杂目标解释

```python
# 解释复杂目标
goal = "Move to the kitchen, pick up the red cup, and place it on the table"
ltl_formula, pddl_domain = interpreter.interpret_with_feedback(goal)

print(f"PDDL域: {pddl_domain.name}")
print(f"谓词数量: {len(pddl_domain.predicates)}")
print(f"动作数量: {len(pddl_domain.actions)}")
```

### 示例3: 反馈学习循环

```python
# 初始解释
goal = "Clean the room"
ltl_formula, pddl_domain = interpreter.interpret_with_feedback(goal)

# 用户反馈循环
for iteration in range(3):
    # 模拟用户反馈
    feedback_type = input("反馈类型 (positive/correction): ")
    feedback_content = input("反馈内容: ")
    
    # 添加反馈
    interpreter.add_feedback(
        text=goal,
        ltl_formula=ltl_formula,
        feedback_type=feedback_type,
        content=feedback_content,
        confidence=0.8
    )
    
    # 重新解释
    ltl_formula, pddl_domain = interpreter.interpret_with_feedback(
        goal, 
        interpreter.get_feedback_history()
    )
    
    print(f"迭代 {iteration + 1}: {ltl_formula.formula}")
```

## 测试和演示

### 运行测试
```bash
python test_interpretable_interpreter.py
```

测试包括：
- 基础解释功能测试
- 反馈学习机制测试
- PDDL域生成测试
- 谓词学习测试
- 统计信息跟踪测试
- 保存加载功能测试

### 运行演示
```bash
python demo_interpretable_interpreter.py
```

演示包括：
- 基础目标解释演示
- 反馈学习机制演示
- 谓词演化过程演示
- PDDL域生成演示
- 统计与分析功能演示
- 保存和加载演示

## 性能优化

### 1. 缓存机制
- 解释结果自动缓存
- 谓词模式缓存
- 反馈历史缓存

### 2. 批处理
- 支持批量目标解释
- 批量反馈处理
- 批量谓词学习

### 3. 内存管理
- 自动清理过期缓存
- 限制反馈缓冲区大小
- 优化谓词存储

## 集成指南

### 与BEHAVIOR仿真环境集成

```python
# 在BEHAVIOR环境中使用
from behavior import BEHAVIORSimulator
from interpretable_goal_interpreter import InterpretableGoalInterpreter

# 创建仿真器
sim = BEHAVIORSimulator()

# 创建解释器
interpreter = InterpretableGoalInterpreter(config)

# 解释任务目标
task_goal = "Clean the kitchen table"
ltl_formula, pddl_domain = interpreter.interpret_with_feedback(task_goal)

# 在仿真中执行
sim.execute_task(pddl_domain, ltl_formula)
```

### 与动作规划模块集成

```python
# 与动作规划器集成
from action_planner import ActionPlanner
from interpretable_goal_interpreter import InterpretableGoalInterpreter

# 创建组件
planner = ActionPlanner()
interpreter = InterpretableGoalInterpreter(config)

# 解释目标并生成计划
goal = "Pick up the cup and place it on the shelf"
ltl_formula, pddl_domain = interpreter.interpret_with_feedback(goal)

# 生成动作序列
action_sequence = planner.plan(pddl_domain, ltl_formula)
```

## 故障排除

### 常见问题

1. **导入错误**
   ```
   ImportError: cannot import name 'InterpretableGoalInterpreter'
   ```
   **解决方案**: 确保文件在同一目录下，检查Python路径设置

2. **LLM连接错误**
   ```
   ConnectionError: Failed to connect to LLM service
   ```
   **解决方案**: 检查API密钥和网络连接，或使用mock模式

3. **PDDL生成失败**
   ```
   ValueError: Invalid PDDL domain structure
   ```
   **解决方案**: 检查目标文本格式，确保包含有效的动作描述

### 调试模式

```python
# 启用调试日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 创建调试模式解释器
config['debug'] = True
interpreter = InterpretableGoalInterpreter(config)
```

## 扩展开发

### 添加新的反馈类型

```python
# 扩展反馈类型
class CustomFeedbackRecord(FeedbackRecord):
    custom_field: str = ""
    
    def process_custom_feedback(self):
        # 自定义反馈处理逻辑
        pass
```

### 自定义谓词学习器

```python
# 实现自定义学习器
class CustomPredicateLearner(InterPreTFeedbackLearner):
    def learn_from_feedback(self, feedback: FeedbackRecord):
        # 自定义学习算法
        super().learn_from_feedback(feedback)
        # 添加额外逻辑
```

## 贡献指南

1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 运行测试确保通过
5. 提交Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues]
- 邮箱: [项目邮箱]

---

**注意**: 本项目是Embodied Agent Interface方案三（通用具身推理框架）的核心组件，与其他模块（AuDeRe、LogicGuard）协同工作，提供完整的具身智能解决方案。