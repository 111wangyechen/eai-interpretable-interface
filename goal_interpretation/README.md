# 目标解释模块 (Goal Interpretation Module)

本模块提供了将自然语言目标描述转换为线性时序逻辑（LTL）公式的功能，用于指导智能体执行复杂任务。

## 功能特点

- 将中文自然语言目标描述转换为LTL公式
- 支持多种任务类型：简单任务、顺序任务、条件任务、并行任务等
- 支持时间操作符：总是、最终、暂时、立即等
- 内置LTL公式验证功能
- 不依赖外部NLP库，使用轻量级的正则表达式分词和模式匹配

## 模块结构

```
goal_interpretation/
├── __init__.py         # 模块初始化，导出主要类
├── goal_interpreter.py # 核心解释器类
├── nlp_parser.py       # 自然语言解析器
├── ltl_generator.py    # LTL公式生成器
├── ltl_validator.py    # LTL公式验证器
├── test_goal_interpretation.py # 测试用例
├── example_usage.py    # 使用示例
└── README.md           # 文档
```

## 安装说明

### 前提条件

- Python 3.6 或更高版本
- 无需外部依赖库

### 安装步骤

1. 将 `goal_interpretation` 文件夹复制到您的项目目录中

```bash
cp -r goal_interpretation /path/to/your/project/
```

2. 导入模块即可使用

## 使用方法

### 基本用法

```python
from goal_interpretation import GoalInterpreter

# 创建解释器实例
interpreter = GoalInterpreter()

# 解释自然语言目标
ltl_formula = interpreter.interpret("先打开门，然后进入房间")

# 获取LTL公式和语义结构
print(ltl_formula.formula)  # 输出LTL公式
print(ltl_formula.semantics)  # 输出语义结构
```

### 支持的任务类型

1. **简单任务**："到达厨房"
2. **顺序任务**："先打开门，然后进入房间"
3. **条件任务**："如果看到红灯，就停止前进"
4. **并行任务**："同时打开窗户和关闭门"
5. **时间任务**：
   - "最终到达目的地"（最终）
   - "总是保持安全"（总是）
6. **复杂任务**：组合多种任务类型的复杂目标

## 类和方法说明

### GoalInterpreter

主要的解释器类，用于将自然语言转换为LTL公式。

#### 方法

- `interpret(text: str) -> LTLFormula`: 解释自然语言文本，返回LTLFormula对象

### LTLFormula

表示LTL公式的类。

#### 属性

- `formula: str`: LTL公式字符串
- `semantics: Dict`: 语义解析结果

#### 方法

- `__str__() -> str`: 返回公式字符串
- `__repr__() -> str`: 返回公式的正式表示

## 示例

运行示例程序查看更多使用方法：

```bash
python goal_interpretation/example_usage.py
```

## 测试

运行测试用例验证功能正确性：

```bash
python goal_interpretation/test_goal_interpretation.py
```

## 在Ubuntu环境中运行

本模块经过特别优化，不依赖外部NLP库（如jieba），可以直接在Ubuntu环境中运行。安装步骤：

1. 复制文件夹到项目目录：

```bash
mkdir -p /home/yeah/embodied-agent-interface/goal_interpretation
cp -r goal_interpretation/* /home/yeah/embodied-agent-interface/goal_interpretation/
```

2. 验证模块导入：

```bash
python -c "from goal_interpretation import GoalInterpreter; print('模块导入成功')"
```

3. 运行测试：

```bash
cd /home/yeah/embodied-agent-interface
python -m goal_interpretation.test_goal_interpretation
```

## 扩展和定制

可以通过修改以下文件来扩展或定制模块功能：

- `nlp_parser.py`: 添加新的动作词、对象词和模式
- `ltl_generator.py`: 修改LTL公式生成的规则
- `ltl_validator.py`: 调整LTL公式验证的逻辑

## 注意事项

- 本模块主要针对中文自然语言进行了优化
- 对于复杂的自然语言描述，可能需要调整解析规则
- 生成的LTL公式遵循标准LTL语法

## 故障排除

如果遇到模块导入问题，请确保：
1. Python版本≥3.6
2. 模块路径正确
3. 所有必要的文件都已复制到正确位置

## 许可证

本模块为项目内部使用。