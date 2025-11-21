#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言解析器
负责从自然语言文本中提取结构化信息
"""

import re
# 使用简单的正则表达式分词方法替代jieba，避免额外依赖
from typing import Dict, List, Optional, Tuple, Union


class NLPParser:
    """
    自然语言解析器类
    使用规则和模式识别来解析中文自然语言文本
    """
    
    def __init__(self):
        """
        初始化NLP解析器
        """
        # 初始化分词器
        self._init_patterns()
        self._init_action_verbs()
        self._init_objects()
        self._init_prepositions()
    
    def _init_patterns(self):
        """
        初始化语言模式
        """
        # 任务模式
        self.task_patterns = {
            "顺序任务": r"(先|首先|第一步).*?(然后|接着|第二步).*?(最后|完成)",
            "条件任务": r"如果.*?那么.*?",
            "禁止任务": r"(不要|避免|禁止|防止).*?",
            "必须任务": r"(必须|需要|应该|应当).*?",
            "直到任务": r"(直到|在.*?之前).*?",
        }
        
        # 时间表达式模式
        self.time_patterns = {
            "总是": r"(总是|始终|一直|永远)",
            "最终": r"(最终|终于|终将|最后)",
            "暂时": r"(暂时|临时|短期)",
            "立即": r"(立即|马上|立刻)",
        }
        
        # 动作模式
        self.action_patterns = {
            "动宾结构": r"(\w+)\s+(\w+)",
            "双宾语": r"(\w+)\s+(\w+)\s+(\w+)",
            "结果补语": r"(\w+)\s+得\s+(\w+)",
        }
    
    def _init_action_verbs(self):
        """
        初始化常用动作动词列表
        """
        self.action_verbs = {
            "移动": ["走", "去", "移动", "前往", "到达", "进入", "离开", "返回"],
            "操作": ["打开", "关闭", "按下", "拉动", "推动", "转动", "调整", "设置"],
            "拿取": ["拿", "取", "抓取", "拿起", "捡起", "拾取", "拿到", "获取"],
            "放置": ["放", "放置", "放下", "搁置", "摆放", "存入", "放入", "搁在"],
            "使用": ["使用", "利用", "应用", "操作", "启动", "运行", "激活"],
            "观察": ["看", "观察", "检查", "查看", "监视", "注意", "留意"],
            "等待": ["等待", "等候", "停留", "待在", "保持"],
            "完成": ["完成", "结束", "达成", "实现", "做完", "搞定"],
        }
    
    def _init_objects(self):
        """
        初始化常用对象类别
        """
        self.object_categories = {
            "家具": ["桌子", "椅子", "沙发", "床", "柜子", "书架", "茶几"],
            "电器": ["电视", "电脑", "冰箱", "空调", "灯", "开关", "插座"],
            "容器": ["杯子", "碗", "盘子", "瓶子", "盒子", "箱子", "袋子"],
            "食物": ["苹果", "香蕉", "面包", "牛奶", "水", "米饭", "蔬菜"],
            "位置": ["房间", "客厅", "厨房", "卧室", "浴室", "阳台", "门口"],
        }
    
    def _init_prepositions(self):
        """
        初始化常用介词和方位词
        """
        self.prepositions = {
            "位置": ["在", "于", "位于", "处于"],
            "方向": ["向", "朝", "往", "对着"],
            "目标": ["到", "至", "达", "向"],
            "方式": ["用", "使用", "通过", "借助"],
            "时间": ["在", "当", "于", "等到"],
        }
    
    def parse(self, text: str) -> Dict:
        """
        解析自然语言文本
        
        Args:
            text: 输入的自然语言文本
            
        Returns:
            Dict: 解析结果，包含任务类型、动作、对象等信息
        """
        # 预处理
        text = self._preprocess(text)
        
        # 初始化结果
        result = {
            "original_text": text,
            "task_type": None,
            "actions": [],
            "objects": [],
            "temporal_info": [],
            "conditions": [],
            "constraints": [],
            "propositions": [],
            "structure": "simple"
        }
        
        # 识别任务类型
        result["task_type"] = self._identify_task_type(text)
        
        # 分词
        words = self.tokenize(text)
        
        # 提取动作
        result["actions"] = self._extract_actions(words, text)
        
        # 提取对象
        result["objects"] = self._extract_objects(words, text)
        
        # 提取时间信息
        result["temporal_info"] = self._extract_temporal_info(text)
        
        # 提取条件
        result["conditions"] = self._extract_conditions(text)
        
        # 提取约束
        result["constraints"] = self._extract_constraints(text)
        
        # 生成命题
        result["propositions"] = self._generate_propositions(result)
        
        # 确定结构
        result["structure"] = self._determine_structure(result)
        
        return result
    
    def _preprocess(self, text: str) -> str:
        """
        预处理文本
        
        Args:
            text: 原始文本
            
        Returns:
            str: 处理后的文本
        """
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        # 去除标点符号（保留括号）
        text = re.sub(r'[，。！？；：、]', '', text)
        
        # 转换为小写
        text = text.lower()
        
        return text.strip()
    
    def _identify_task_type(self, text: str) -> Optional[str]:
        """
        识别任务类型
        
        Args:
            text: 文本
            
        Returns:
            str: 任务类型
        """
        for task_type, pattern in self.task_patterns.items():
            if re.search(pattern, text):
                return task_type
        
        # 默认任务类型
        return "简单任务"
    
    def _extract_actions(self, words: List[str], text: str) -> List[Dict]:
        """
        提取动作信息
        
        Args:
            words: 分词后的单词列表
            text: 原始文本
            
        Returns:
            List[Dict]: 动作列表，每个动作包含类型、动词等信息
        """
        actions = []
        
        # 使用动词表匹配
        for word in words:
            for action_type, verb_list in self.action_verbs.items():
                if word in verb_list:
                    action = {
                        "type": action_type,
                        "verb": word,
                        "position": text.find(word)
                    }
                    actions.append(action)
                    break
        
        # 使用模式匹配动宾结构
        for pattern_name, pattern in self.action_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                if pattern_name == "动宾结构" and len(match) == 2:
                    verb, obj = match
                    action = {
                        "type": "未知",
                        "verb": verb,
                        "object": obj,
                        "structure": pattern_name
                    }
                    # 避免重复
                    if not any(a["verb"] == verb for a in actions):
                        actions.append(action)
        
        # 按照在文本中的位置排序
        actions.sort(key=lambda x: x.get("position", 0))
        
        return actions
    
    def _extract_objects(self, words: List[str], text: str) -> List[Dict]:
        """
        提取对象信息
        
        Args:
            words: 分词后的单词列表
            text: 原始文本
            
        Returns:
            List[Dict]: 对象列表
        """
        objects = []
        
        # 使用对象类别表匹配
        for word in words:
            for category, obj_list in self.object_categories.items():
                if word in obj_list:
                    obj = {
                        "name": word,
                        "category": category,
                        "position": text.find(word)
                    }
                    objects.append(obj)
                    break
        
        # 提取动宾结构中的宾语
        for pattern in [self.action_patterns["动宾结构"]]:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) == 2:
                    verb, obj_name = match
                    # 检查是否已经添加
                    if not any(o["name"] == obj_name for o in objects):
                        obj = {
                            "name": obj_name,
                            "category": "未知",
                            "position": text.find(obj_name)
                        }
                        objects.append(obj)
        
        # 按照在文本中的位置排序
        objects.sort(key=lambda x: x.get("position", 0))
        
        return objects
    
    def _extract_temporal_info(self, text: str) -> List[Dict]:
        """
        提取时间信息
        
        Args:
            text: 文本
            
        Returns:
            List[Dict]: 时间信息列表
        """
        temporal_info = []
        
        for info_type, pattern in self.time_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                temporal_info.append({
                    "type": info_type,
                    "expression": match,
                    "position": text.find(match)
                })
        
        # 按照在文本中的位置排序
        temporal_info.sort(key=lambda x: x.get("position", 0))
        
        return temporal_info
    
    def _extract_conditions(self, text: str) -> List[Dict]:
        """
        提取条件信息
        
        Args:
            text: 文本
            
        Returns:
            List[Dict]: 条件列表
        """
        conditions = []
        
        # 查找条件句式
        condition_patterns = [
            ("if", r"如果(.*?)那么"),
            ("when", r"当(.*?)时"),
            ("while", r"在(.*?)的情况下"),
        ]
        
        for cond_type, pattern in condition_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                conditions.append({
                    "type": cond_type,
                    "content": match.strip(),
                    "position": text.find(match)
                })
        
        # 按照在文本中的位置排序
        conditions.sort(key=lambda x: x.get("position", 0))
        
        return conditions
    
    def _extract_constraints(self, text: str) -> List[Dict]:
        """
        提取约束信息
        
        Args:
            text: 文本
            
        Returns:
            List[Dict]: 约束列表
        """
        constraints = []
        
        # 查找约束句式
        constraint_patterns = [
            ("禁止", r"(不要|禁止|避免|防止)(.*?)([，。！？；：]|$)"),
            ("必须", r"(必须|需要|应该)(.*?)([，。！？；：]|$)"),
            ("直到", r"(直到|在.*?之前)(.*?)([，。！？；：]|$)"),
        ]
        
        for constraint_type, pattern in constraint_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 2:
                    content = match[1].strip()
                    if content:
                        constraints.append({
                            "type": constraint_type,
                            "content": content,
                            "position": text.find(content)
                        })
        
        # 按照在文本中的位置排序
        constraints.sort(key=lambda x: x.get("position", 0))
        
        return constraints
    
    def _generate_propositions(self, parse_result: Dict) -> List[str]:
        """
        根据解析结果生成命题列表
        
        Args:
            parse_result: 解析结果字典
            
        Returns:
            List[str]: 命题列表
        """
        propositions = []
        
        # 从动作和对象生成命题
        actions = parse_result.get("actions", [])
        objects = parse_result.get("objects", [])
        
        # 简单的命题生成：动作+对象
        for action in actions:
            if "object" in action:
                # 如果动作已经包含对象，直接生成命题
                prop = f"{action['verb']}_{action['object']}"
                propositions.append(prop)
            else:
                # 否则尝试匹配最接近的对象
                action_pos = action.get("position", 0)
                closest_obj = None
                min_distance = float('inf')
                
                for obj in objects:
                    obj_pos = obj.get("position", 0)
                    distance = abs(obj_pos - action_pos)
                    if obj_pos > action_pos and distance < min_distance:  # 只考虑动作后面的对象
                        min_distance = distance
                        closest_obj = obj
                
                if closest_obj:
                    prop = f"{action['verb']}_{closest_obj['name']}"
                    propositions.append(prop)
        
        # 如果没有命题，使用约束内容生成
        if not propositions and parse_result.get("constraints"):
            for constraint in parse_result["constraints"]:
                # 简化约束内容，生成命题
                content = constraint["content"]
                # 使用简单的分词方法替代jieba
                words = self.tokenize(content)
                # 查找动词
                for word in words:
                    for verb_list in self.action_verbs.values():
                        if word in verb_list:
                            # 查找该动词后面的名词
                            verb_index = words.index(word)
                            for i in range(verb_index + 1, len(words)):
                                prop = f"{word}_{words[i]}"
                                propositions.append(prop)
                                break
                            break
        
        # 去重
        propositions = list(dict.fromkeys(propositions))
        
        return propositions
    
    def _determine_structure(self, parse_result: Dict) -> str:
        """
        确定句子结构类型
        
        Args:
            parse_result: 解析结果
            
        Returns:
            str: 结构类型
        """
        task_type = parse_result.get("task_type", "")
        
        if "顺序" in task_type:
            return "sequential"
        elif "条件" in task_type:
            return "conditional"
        elif "禁止" in task_type or any(c["type"] == "禁止" for c in parse_result.get("constraints", [])):
            return "prohibitive"
        elif "必须" in task_type or any(c["type"] == "必须" for c in parse_result.get("constraints", [])):
            return "obligatory"
        elif "直到" in task_type or any(c["type"] == "直到" for c in parse_result.get("constraints", [])):
            return "until"
        elif parse_result.get("temporal_info"):
            # 检查时间信息类型
            for temp_info in parse_result["temporal_info"]:
                if temp_info["type"] == "总是":
                    return "always"
                elif temp_info["type"] == "最终":
                    return "eventually"
        
        # 默认结构
        return "simple"
    
    def tokenize(self, text: str) -> List[str]:
        """
        使用简单的正则表达式分词方法对文本进行分词
        替代jieba分词器，避免额外依赖
        
        Args:
            text: 输入的文本
            
        Returns:
            分词后的词汇列表
        """
        # 简单的分词方法：将文本按照常见的动作词、对象词和连接词进行匹配
        # 首先定义一些常见的词汇
        common_words = []
        
        # 添加所有支持的动作词
        for category, actions in self.action_verbs.items():
            common_words.extend(actions)
        
        # 添加所有支持的对象词
        for category, objects in self.object_categories.items():
            common_words.extend(objects)
        
        # 添加一些常见的连接词和时间词
        common_words.extend([
            '先', '首先', '第一步', '然后', '接着', '第二步', '最后', '完成',
            '如果', '那么', '不要', '避免', '禁止', '防止',
            '必须', '需要', '应该', '应当', '直到', '在', '之前',
            '总是', '始终', '一直', '永远', '最终', '终于', '终将',
            '暂时', '临时', '短期', '立即', '马上', '立刻',
            '同时', '并且', '或者', '但', '但是'
        ])
        
        # 按长度降序排列，优先匹配较长的词
        common_words.sort(key=len, reverse=True)
        
        # 构建正则表达式模式
        pattern = '|'.join(re.escape(word) for word in common_words)
        
        # 提取所有匹配的词
        tokens = re.findall(pattern, text)
        
        # 如果没有匹配到任何词，简单地按字符分割（备用方案）
        if not tokens:
            # 保留一些基本的分词逻辑
            # 将文本分割为单个汉字和英文/数字序列
            tokens = re.findall(r'[a-zA-Z0-9]+|[\u4e00-\u9fa5]', text)
        
        return tokens
    
    def get_supported_actions(self) -> Dict[str, List[str]]:
        """
        获取支持的动作列表
        
        Returns:
            Dict: 动作类型到动作列表的映射
        """
        return self.action_verbs
    
    def get_supported_objects(self) -> Dict[str, List[str]]:
        """
        获取支持的对象类别
        
        Returns:
            Dict: 类别到对象列表的映射
        """
        return self.object_categories