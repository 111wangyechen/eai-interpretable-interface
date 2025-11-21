#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Natural Language Parser for English Environment
Optimized for English-only task interpretation
"""

import re
from typing import Dict, List, Optional, Tuple, Union


class EnhancedNLPParser:
    """
    Enhanced Natural Language Parser Class
    Optimized for English-only complex semantic structure parsing
    """
    
    def __init__(self):
        """
        Initialize Enhanced NLP Parser
        """
        self._init_enhanced_patterns()
        self._init_english_vocab()
        self._init_semantic_roles()
        self._init_complex_structures()
    
    def _init_enhanced_patterns(self):
        """
        Initialize enhanced English-only patterns
        """
        # Complex task patterns - improved for better English recognition
        self.complex_task_patterns = {
            # Multi-step sequential tasks - enhanced patterns
            "multi_step_sequential": [
                r"\bfirst\b.*?\bthen\b.*?\bfinally\b",
                r"\bfirst\b.*?\bthen\b",
                r"\bthen\b.*?\bfinally\b",
                r"\bstep\s*\d+\b.*?\bstep\s*\d+\b.*?\bstep\s*\d+\b",
                r"\bstep\s*\d+\b.*?\bstep\s*\d+\b",
                r"\b(\w+)\s*,\s*then\s+(\w+)\b",
                r"\b(\w+)\s+then\s+(\w+)\b",
                r"\b(\w+)\s*,\s*then\s+(\w+)\s*,\s*finally\s+(\w+)\b"
            ],
            # Conditional branch tasks - enhanced patterns
            "conditional_branch": [
                r"\bif\s+[^,]+?\s+then\s+[^,]+?(?:\s+else\s+[^,]+)?",
                r"\bwhen\s+[^,]+?\s+then\s+[^,]+?(?:\s+otherwise\s+[^,]+)?",
                r"\bif\s+[^,]+?\s*,\s*[^,]+?\s+then\s+[^,]+",
                r"\bprovided\s+that\s+[^,]+?\s+then\s+[^,]+",
                r"\bunless\s+[^,]+?\s+then\s+[^,]+"
            ],
            # Iterative tasks - enhanced patterns
            "iterative_task": [
                r"\brepeat\b[^,]*?\b(times|until|while)\b",
                r"\bkeep\b[^,]*?\b(until|while)\b",
                r"\bcontinue\b[^,]*?\b(until|while)\b",
                r"\bagain\b[^,]*?\b(times|until|while)\b",
                r"\bmultiple\b[^,]*?\btimes\b",
                r"\bwhile\b[^,]*?\b(?:do|perform|execute)\b",
                r"\buntil\b[^,]*?\b(?:stop|finish|complete)\b"
            ],
            # Parallel tasks - enhanced patterns
            "parallel_task": [
                r"\b\w+\s+and\s+\w+\b.*?\bsimultaneously\b",
                r"\bsimultaneously\b",
                r"\bat the same time\b",
                r"\bboth\s+\w+\s+and\s+\w+\b",
                r"\b\w+\s+and\s+\w+\b.*?\bat the same time\b",
                r"\bwhile\s+\w+\b.*?\b\w+\s+and\s+\w+\b"
            ],
            # Temporal constraint tasks - enhanced patterns
            "temporal_constraint": [
                r"\b(within|before|after|during|by)\b[^,]*?\b\w+\b",
                r"\b(no later than|earlier than)\b[^,]*?\b\w+\b",
                r"\bbefore\s+\w+\b.*?\bafter\s+\w+\b",
                r"\bafter\s+\w+\b.*?\bbefore\s+\w+\b"
            ]
        }
        
        # Enhanced time expression patterns
        self.enhanced_time_patterns = {
            # Relative time
            "relative_time": [
                r"\b(immediately|right away|as soon as|instantly)\b",
                r"\b(eventually|finally|ultimately|in the end)\b",
                r"\b(soon|later|earlier|now|then)\b"
            ],
            # Duration
            "duration": [
                r"\b(for\s+\d+\s*(seconds|minutes|hours|days|weeks|months))\b",
                r"\b(while\s+[^,]*?\buntil\b[^,]*?)\b",
                r"\b(from\s+[^,]*?\bto\b[^,]*?)\b"
            ],
            # Frequency
            "frequency": [
                r"\b(always|never|sometimes|often|rarely|occasionally)\b",
                r"\b(every|each|all|some|most)\b",
                r"\b(daily|weekly|monthly|yearly)\b"
            ]
        }
    
    def _init_english_vocab(self):
        """
        Initialize comprehensive English vocabulary
        """
        # English action verbs - expanded
        self.english_actions = {
            "movement": ["go", "move", "walk", "travel", "approach", "reach", "enter", "leave", "return", "run", "drive", "fly", "climb", "jump", "swim"],
            "operation": ["open", "close", "press", "pull", "push", "turn", "adjust", "set", "activate", "deactivate", "start", "stop", "switch", "toggle", "lock", "unlock"],
            "take": ["take", "get", "grab", "pick", "fetch", "obtain", "collect", "receive", "acquire", "retrieve"],
            "place": ["put", "place", "set", "lay", "store", "put down", "position", "arrange", "organize"],
            "use": ["use", "utilize", "apply", "operate", "start", "run", "execute", "perform", "handle", "manage"],
            "observe": ["look", "see", "watch", "observe", "check", "monitor", "notice", "examine", "inspect", "verify", "detect"],
            "wait": ["wait", "stay", "remain", "keep", "pause", "hold", "rest"],
            "complete": ["complete", "finish", "end", "accomplish", "achieve", "done", "finalize", "conclude"],
            "clean": ["clean", "wash", "wipe", "sweep", "mop", "dust", "vacuum", "scrub", "polish"],
            "prepare": ["prepare", "make", "cook", "get", "ready", "setup", "arrange", "organize"],
            "communicate": ["talk", "speak", "tell", "say", "ask", "answer", "call", "message", "email", "contact"],
            "read": ["read", "browse", "scan", "review", "study", "examine", "peruse"],
            "write": ["write", "type", "compose", "create", "draft", "record", "document"],
            "eat": ["eat", "drink", "consume", "have", "taste", "enjoy"],
            "sleep": ["sleep", "rest", "nap", "relax"],
            "work": ["work", "study", "learn", "practice", "train", "exercise"]
        }
        
        # English object categories - expanded
        self.english_objects = {
            "furniture": ["table", "chair", "sofa", "bed", "cabinet", "bookshelf", "desk", "dresser", "nightstand", "stool"],
            "appliances": ["tv", "television", "computer", "fridge", "refrigerator", "ac", "air conditioner", "light", "lamp", "switch", "outlet", "microwave", "oven", "toaster", "coffee maker"],
            "containers": ["cup", "glass", "bowl", "plate", "bottle", "box", "bag", "container", "jar", "can", "basket"],
            "food": ["apple", "banana", "bread", "milk", "water", "rice", "food", "fruit", "vegetable", "meat", "fish", "chicken", "egg", "cheese"],
            "locations": ["room", "living room", "kitchen", "bedroom", "bathroom", "balcony", "door", "entrance", "house", "office", "garage", "garden", "yard", "park", "store"],
            "tools": ["vacuum cleaner", "mop", "cloth", "broom", "key", "phone", "computer", "pen", "pencil", "paper", "scissors", "hammer", "screwdriver"],
            "vehicles": ["car", "truck", "bus", "train", "plane", "bicycle", "motorcycle", "boat"],
            "electronics": ["phone", "computer", "laptop", "tablet", "camera", "speaker", "headphones", "watch"]
        }
    
    def _init_semantic_roles(self):
        """
        Initialize semantic role labeling for English
        """
        self.semantic_roles = {
            # Action-related roles
            "agent": ["by", "with", "using"],  # Executor
            "patient": ["take", "get", "grab"],  # Patient
            "instrument": ["with", "using", "by means of"],  # Tool
            "location": ["in", "on", "at", "to", "from"],  # Location
            "destination": ["to", "towards", "into"],  # Destination
            "source": ["from", "out of", "away from"],  # Source
            "time": ["at", "on", "in", "during", "before", "after"],  # Time
            "purpose": ["for", "to", "in order to"],  # Purpose
            "condition": ["if", "when", "unless", "provided that"],  # Condition
        }
    
    def _init_complex_structures(self):
        """
        Initialize complex structure patterns for English
        """
        self.complex_structures = {
            # Nested conditions
            "nested_condition": [
                r"\bif\s+[^,]+?\s+and\s+[^,]+?\s+then\s+[^,]+",
                r"\bwhen\s+[^,]+?\s+and\s+[^,]+?\s+then\s+[^,]+",
                r"\bif\s+[^,]+?\s+or\s+[^,]+?\s+then\s+[^,]+"
            ],
            # Multiple constraints
            "multiple_constraints": [
                r"\b(must|should|need to)\s+[^,]+?\s+and\s+(?:must|should|need to)\s+[^,]+",
                r"\b(not|never)\s+[^,]+?\s+and\s+(?:not|never)\s+[^,]+"
            ],
            # Temporal chain
            "temporal_chain": [
                r"\bbefore\s+[^,]+?\s+after\s+[^,]+?\s+then\s+[^,]+",
                r"\bfirst\s+[^,]+?\s+then\s+[^,]+?\s+finally\s+[^,]+",
                r"\bstep\s*\d+\s+[^,]*?\bstep\s*\d+\s+[^,]*?\bstep\s*\d+"
            ]
        }
    
    def parse(self, text: str) -> Dict:
        """
        Parse natural language text (Enhanced English)
        
        Args:
            text: Input natural language text
            
        Returns:
            Dict: Enhanced parsing result
        """
        # Preprocess
        text = self._enhanced_preprocess(text)
        
        # Initialize enhanced result
        result = {
            "original_text": text,
            "language": "en",
            "task_complexity": "simple",
            "semantic_structure": {},
            "actions": [],
            "objects": [],
            "temporal_info": [],
            "conditions": [],
            "constraints": [],
            "propositions": [],
            "structure": "simple",
            "semantic_roles": {},
            "dependencies": [],
            "modifiers": []
        }
        
        # Identify task complexity
        result["task_complexity"] = self._identify_task_complexity(text)
        
        # Parse semantic structure
        result["semantic_structure"] = self._parse_semantic_structure(text)
        
        # Extract enhanced action information
        result["actions"] = self._extract_enhanced_actions(text)
        
        # Extract enhanced object information
        result["objects"] = self._extract_enhanced_objects(text)
        
        # Extract enhanced temporal information
        result["temporal_info"] = self._extract_enhanced_temporal_info(text)
        
        # Extract enhanced condition information
        result["conditions"] = self._extract_enhanced_conditions(text)
        
        # Extract enhanced constraint information
        result["constraints"] = self._extract_enhanced_constraints(text)
        
        # Extract semantic roles
        result["semantic_roles"] = self._extract_semantic_roles(text)
        
        # Analyze dependencies
        result["dependencies"] = self._analyze_dependencies(text)
        
        # Extract modifiers
        result["modifiers"] = self._extract_modifiers(text)
        
        # Generate enhanced propositions
        result["propositions"] = self._generate_enhanced_propositions(result)
        
        # Determine enhanced structure
        result["structure"] = self._determine_enhanced_structure(result)
        
        return result
    
    def _enhanced_preprocess(self, text: str) -> str:
        """
        Enhanced text preprocessing for English
        """
        # Handle empty input
        if not text or not text.strip():
            return ""
        
        # Standardize quotes and brackets
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('(', ' ( ').replace(')', ' ) ')
        
        # Handle contractions
        text = re.sub(r"can't", "cannot", text, flags=re.IGNORECASE)
        text = re.sub(r"won't", "will not", text, flags=re.IGNORECASE)
        text = re.sub(r"n't", " not", text, flags=re.IGNORECASE)
        text = re.sub(r"'ll", " will", text, flags=re.IGNORECASE)
        text = re.sub(r"'re", " are", text, flags=re.IGNORECASE)
        text = re.sub(r"'ve", " have", text, flags=re.IGNORECASE)
        text = re.sub(r"'m", " am", text, flags=re.IGNORECASE)
        
        # Standardize spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Preserve important punctuation
        important_punct = r'[,.!?;:]'
        text = re.sub(f'({important_punct})', r' \1 ', text)
        
        return text.strip().lower()
    
    def _identify_task_complexity(self, text: str) -> str:
        """
        Identify task complexity for English
        """
        if not text:
            return "simple"
            
        complexity_score = 0
        
        # Check complex patterns
        for pattern_type, patterns in self.complex_task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    complexity_score += 2
                    break
        
        # Check connector count
        connectors = len(re.findall(r'\b(and|or|but|if|when|then|because|so|while|until|before|after|first|finally)\b', text, re.IGNORECASE))
        complexity_score += connectors
        
        # Check clause count
        clauses = len(re.findall(r'\b(that|which|who|where|when|why|how|if|when|while|because|since|unless)\b', text, re.IGNORECASE))
        complexity_score += clauses
        
        if complexity_score >= 4:
            return "complex"
        elif complexity_score >= 2:
            return "medium"
        else:
            return "simple"
    
    def _parse_semantic_structure(self, text: str) -> Dict:
        """
        Parse semantic structure for English
        """
        structure = {
            "main_clause": "",
            "subordinate_clauses": [],
            "connectors": [],
            "modifiers": []
        }
        
        if not text:
            return structure
        
        # Identify main clause and subordinate clauses
        clause_markers = [
            r'(.*?)(?:\b(if|when|while|because|although|since|unless|before|after)\b)(.*?)(?:\b(then|so)\b)?(.*)'
        ]
        
        for pattern in clause_markers:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structure["main_clause"] = match.group(1).strip()
                structure["subordinate_clauses"].append(match.group(2).strip())
                if len(match.groups()) > 3:
                    structure["main_clause"] += " " + (match.group(4) or "").strip()
                break
        
        return structure
    
    def _extract_enhanced_actions(self, text: str) -> List[Dict]:
        """
        Extract enhanced action information for English
        """
        actions = []
        
        if not text:
            return actions
        
        # First identify sequential structure actions with improved patterns
        sequential_patterns = [
            r'\bfirst\s+(\w+)(?:\s+then\s+(\w+))?(?:\s+finally\s+(\w+))?',
            r'\b(\w+)\s+then\s+(\w+)(?:\s+finally\s+(\w+))?',
            r'\b(\w+)\s*,\s*then\s+(\w+)(?:\s*,\s*finally\s+(\w+))?',
            r'\bstep\s*\d+\s*[:\-]?\s*(\w+)(?:\s*,\s*step\s*\d+\s*[:\-]?\s*(\w+))?(?:\s*,\s*step\s*\d+\s*[:\-]?\s*(\w+))?'
        ]
        
        for pattern in sequential_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                for i in range(1, len(match.groups()) + 1):
                    if match.group(i):
                        verb = match.group(i)
                        # Verify if it's an action word
                        if self._is_action_word(verb):
                            action = {
                                "type": self._get_action_type(verb),
                                "verb": verb,
                                "object": self._extract_object_for_verb(text, verb, match.start(i)),
                                "position": match.start(i),
                                "context": text[max(0, match.start()-10):match.end()+10],
                                "sequential_order": i,
                                "sequential_pattern": True
                            }
                            actions.append(action)
        
        # If no sequential actions found, use regular action extraction
        if not actions:
            for action_type, action_words in self.english_actions.items():
                for word in action_words:
                    # More relaxed action word matching pattern
                    pattern = rf'\b({word})\b'
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    
                    for match in matches:
                        # Find object for action word
                        object_pattern = rf'\b{word}\b\s+(?:\w+\s+)?(\w+)'
                        object_match = re.search(object_pattern, text[match.start():match.start()+30], re.IGNORECASE)
                        
                        action = {
                            "type": action_type,
                            "verb": match.group(1),
                            "object": object_match.group(1) if object_match else None,
                            "position": match.start(),
                            "context": text[max(0, match.start()-10):match.end()+10]
                        }
                        actions.append(action)
        
        # Special handling: identify parallel actions
        conjunction_patterns = [
            r'\b(\w+)\s+and\s+(\w+)\b',
            r'\bboth\s+(\w+)\s+and\s+(\w+)\b'
        ]
        
        for pattern in conjunction_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                verb1, verb2 = match.group(1), match.group(2)
                
                # Check if both words are action words
                if self._is_action_word(verb1) and self._is_action_word(verb2):
                    for i, verb in enumerate([verb1, verb2], 1):
                        actions.append({
                            "type": self._get_action_type(verb),
                            "verb": verb,
                            "object": self._extract_object_for_verb(text, verb, match.start(i)),
                            "position": match.start(i),
                            "context": text[max(0, match.start()-10):match.end()+10],
                            "conjunction": "and"
                        })
        
        # Sort by position and deduplicate
        actions.sort(key=lambda x: x["position"])
        unique_actions = []
        seen_positions = set()
        
        for action in actions:
            pos_key = (action["position"], action["verb"])
            if pos_key not in seen_positions:
                seen_positions.add(pos_key)
                unique_actions.append(action)
        
        return unique_actions
    
    def _is_action_word(self, word: str) -> bool:
        """Check if word is an action word"""
        if not word:
            return False
        word_lower = word.lower()
        for action_type, action_words in self.english_actions.items():
            if word_lower in [w.lower() for w in action_words]:
                return True
        return False
    
    def _get_action_type(self, word: str) -> str:
        """Get action word type"""
        if not word:
            return "unknown"
        word_lower = word.lower()
        for action_type, action_words in self.english_actions.items():
            if word_lower in [w.lower() for w in action_words]:
                return action_type
        return "unknown"
    
    def _extract_object_for_verb(self, text: str, verb: str, verb_position: int) -> str:
        """Extract object for verb"""
        if not text or not verb:
            return None
        # Find object after verb
        after_verb = text[verb_position + len(verb):verb_position + len(verb) + 20]
        object_pattern = r'\s+(\w+)'
        match = re.search(object_pattern, after_verb)
        return match.group(1) if match else None
    
    def _extract_enhanced_objects(self, text: str) -> List[Dict]:
        """
        Extract enhanced object information for English
        """
        objects = []
        
        if not text:
            return objects
        
        for obj_type, obj_words in self.english_objects.items():
            for word in obj_words:
                # Find object words and their modifiers
                pattern = rf'(\b\w+\b\s+)?\b({re.escape(word)})\b'
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    obj = {
                        "name": match.group(2),
                        "category": obj_type,
                        "modifier": match.group(1) if match.group(1) else None,
                        "position": match.start(),
                        "context": text[max(0, match.start()-10):match.end()+10]
                    }
                    objects.append(obj)
        
        # Sort by position
        objects.sort(key=lambda x: x["position"])
        return objects
    
    def _extract_enhanced_temporal_info(self, text: str) -> List[Dict]:
        """
        Extract enhanced temporal information for English
        """
        temporal_info = []
        
        if not text:
            return temporal_info
        
        for time_type, patterns in self.enhanced_time_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    temporal_info.append({
                        "type": time_type,
                        "expression": match.group(0),
                        "position": match.start(),
                        "end_position": match.end()
                    })
        
        # Sort by position
        temporal_info.sort(key=lambda x: x["position"])
        return temporal_info
    
    def _extract_enhanced_conditions(self, text: str) -> List[Dict]:
        """
        Extract enhanced condition information for English
        """
        conditions = []
        
        if not text:
            return conditions
        
        # Enhanced condition patterns
        condition_patterns = [
            (r"\bif\s+([^,]+?)\s+then\s+([^,]+)", "if_then"),
            (r"\bwhen\s+([^,]+?)\s+then\s+([^,]+)", "when_then"),
            (r"\bprovided\s+that\s+([^,]+)", "provided"),
            (r"\bunless\s+([^,]+)", "unless"),
            (r"\bif\s+([^,]+?),\s*([^,]+?)\s+then\s+([^,]+)", "complex_if_then"),
            (r"\bwhen\s+([^,]+?),\s*([^,]+?)\s+then\s+([^,]+)", "complex_when_then")
        ]
        
        for pattern, cond_type in condition_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                condition = {
                    "type": cond_type,
                    "condition": match.group(1).strip(),
                    "consequence": match.group(2).strip() if len(match.groups()) > 1 else None,
                    "position": match.start()
                }
                conditions.append(condition)
        
        # Sort by position
        conditions.sort(key=lambda x: x["position"])
        return conditions
    
    def _extract_enhanced_constraints(self, text: str) -> List[Dict]:
        """
        Extract enhanced constraint information for English
        """
        constraints = []
        
        if not text:
            return constraints
        
        # Constraint type patterns
        constraint_patterns = [
            (r"\b(must|should|need to|have to)\b", "obligation"),
            (r"\b(must not|should not|cannot|can't)\b", "prohibition"),
            (r"\b(can|may|allowed to)\b", "permission"),
            (r"\b(before|after|during|while|until)\b", "temporal_constraint"),
        ]
        
        for pattern, constraint_type in constraint_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                constraint = {
                    "type": constraint_type,
                    "content": match.group(1),
                    "operator": match.group(1),
                    "position": match.start()
                }
                constraints.append(constraint)
        
        # Sort by position
        constraints.sort(key=lambda x: x["position"])
        return constraints
    
    def _extract_semantic_roles(self, text: str) -> Dict:
        """
        Extract semantic roles for English
        """
        roles = {}
        
        if not text:
            return roles
        
        for role_type, markers in self.semantic_roles.items():
            roles[role_type] = []
            
            for marker in markers:
                pattern = rf'\b{re.escape(marker)}\s+(\w+(?:\s+\w+)*)'
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    roles[role_type].append({
                        "marker": marker,
                        "filler": match.group(1),
                        "position": match.start()
                    })
        
        return roles
    
    def _analyze_dependencies(self, text: str) -> List[Dict]:
        """
        Analyze dependencies for English
        """
        dependencies = []
        
        if not text:
            return dependencies
        
        # Causal relationships
        causal_patterns = [
            (r"\bbecause\s+([^,]+?),?\s*([^,]+)", "cause"),
            (r"\bso\s+([^,]+?),?\s*([^,]+)", "effect"),
            (r"\btherefore\s+([^,]+)", "consequence"),
            (r"\bthus\s+([^,]+)", "consequence")
        ]
        
        for pattern, dep_type in causal_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                dependencies.append({
                    "type": dep_type,
                    "source": match.group(1),
                    "target": match.group(2) if len(match.groups()) > 1 else None,
                    "position": match.start()
                })
        
        return dependencies
    
    def _extract_modifiers(self, text: str) -> List[Dict]:
        """
        Extract modifiers for English
        """
        modifiers = []
        
        if not text:
            return modifiers
        
        # Adjective modifiers
        adj_pattern = r'\b(\w+)\s+(\w+)\s+(?:\w+)'
        matches = re.finditer(adj_pattern, text)
        
        for match in matches:
            potential_adj = match.group(1)
            if len(potential_adj) > 2:  # Simple heuristic for adjectives
                modifiers.append({
                    "type": "adjective",
                    "modifier": potential_adj,
                    "modified": match.group(2),
                    "position": match.start()
                })
        
        return modifiers
    
    def _generate_enhanced_propositions(self, parse_result: Dict) -> List[str]:
        """
        Generate enhanced propositions for English
        """
        propositions = []
        
        # Generate action-object propositions with improved format
        for action in parse_result["actions"]:
            verb = action.get("verb", "").lower()
            obj = action.get("object", "").lower()
            action_type = action.get("type", "unknown").lower()
            
            # Clean and normalize the components
            verb = verb.strip().replace(" ", "_")
            obj = obj.strip().replace(" ", "_")
            
            if verb and obj and verb != "the" and obj != "the":
                # Create meaningful proposition: verb_object or object_verb
                if verb in ["walk", "go", "move"]:
                    # For movement actions, use destination_verb format
                    propositions.append(f"{obj}_{verb}")
                elif verb in ["wash", "clean", "put", "take", "get"]:
                    # For manipulation actions, use object_verb format
                    propositions.append(f"{obj}_{verb}")
                else:
                    # Default format
                    propositions.append(f"{verb}_{obj}")
            elif verb and verb not in ["the", "a", "an"]:
                # Create verb proposition if meaningful
                propositions.append(f"{verb}")
            elif obj and obj not in ["the", "a", "an"]:
                # Create object proposition if meaningful
                propositions.append(f"{obj}")
        
        # Generate propositions from objects and their relationships
        objects = parse_result.get("objects", [])
        if objects:
            for i, obj in enumerate(objects):
                obj_name = obj.get("name", "").lower().strip()
                obj_category = obj.get("category", "").lower().strip()
                
                if obj_name and obj_name not in ["the", "a", "an"]:
                    # Create object-based propositions
                    if obj_category and obj_category not in ["the", "a", "an"]:
                        propositions.append(f"{obj_category}_{obj_name}")
                    else:
                        propositions.append(f"object_{obj_name}")
        
        # Generate location-based propositions
        for obj_info in parse_result.get("objects", []):
            if "location" in obj_info:
                location = obj_info["location"].lower().strip().replace(" ", "_")
                obj_name = obj_info.get("name", "").lower().strip().replace(" ", "_")
                if location and obj_name:
                    propositions.append(f"{location}_{obj_name}")
        
        # Generate condition propositions with improved format
        for condition in parse_result["conditions"]:
            condition_text = condition.get("condition", "").strip()
            if condition_text and condition_text.lower() not in ["the", "a", "an"]:
                # Clean and normalize condition text
                clean_condition = condition_text.replace(" ", "_").lower()
                # Remove common articles
                clean_condition = clean_condition.replace("_the_", "_").replace("_a_", "_").replace("_an_", "_")
                if clean_condition:
                    propositions.append(f"condition_{clean_condition}")
        
        # Generate constraint propositions with improved format
        for constraint in parse_result["constraints"]:
            content = constraint.get("content", "").strip()
            constraint_type = constraint.get("type", "").strip()
            if content and content.lower() not in ["the", "a", "an"]:
                # Clean and normalize constraint content
                clean_content = content.replace(" ", "_").lower()
                # Remove common articles
                clean_content = clean_content.replace("_the_", "_").replace("_a_", "_").replace("_an_", "_")
                if clean_content:
                    if constraint_type:
                        propositions.append(f"{constraint_type}_{clean_content}")
                    else:
                        propositions.append(f"constraint_{clean_content}")
        
        # Generate temporal propositions
        for temp_info in parse_result["temporal_info"]:
            temp_expr = temp_info.get("expression", "").strip()
            temp_type = temp_info.get("type", "").strip()
            if temp_expr and temp_expr.lower() not in ["the", "a", "an"]:
                clean_temp = temp_expr.replace(" ", "_").lower()
                # Remove common articles
                clean_temp = clean_temp.replace("_the_", "_").replace("_a_", "_").replace("_an_", "_")
                if clean_temp:
                    if temp_type:
                        propositions.append(f"{temp_type}_{clean_temp}")
                    else:
                        propositions.append(f"temporal_{clean_temp}")
        
        # Remove duplicates and empty propositions
        clean_propositions = []
        seen = set()
        for prop in propositions:
            if prop and prop not in seen and len(prop) > 1:  # Ensure meaningful length
                # Further clean the proposition
                prop = prop.replace("__", "_").strip("_")
                if prop:
                    clean_propositions.append(prop)
                    seen.add(prop)
        
        # If still no propositions, create a default one from the original text
        if not clean_propositions:
            original_text = parse_result.get("original_text", "").strip()
            if original_text:
                # Extract meaningful words (excluding common stop words)
                stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by"}
                words = [w.lower() for w in original_text.split() if w.lower() not in stop_words and len(w) > 2]
                if words:
                    default_prop = "_".join(words[:3])  # Use first 3 meaningful words
                    clean_propositions.append(f"task_{default_prop}")
                else:
                    clean_propositions.append("task_complete")
            else:
                clean_propositions.append("task_complete")
        
        return clean_propositions
    
    def _determine_enhanced_structure(self, parse_result: Dict) -> str:
        """
        Determine enhanced structure type for English
        """
        text = parse_result["original_text"]
        actions = parse_result["actions"]
        conditions = parse_result["conditions"]
        constraints = parse_result["constraints"]
        temporal_info = parse_result["temporal_info"]
        
        if not text:
            return "simple"
        
        # Priority 1: Conditional tasks - check first with improved patterns
        conditional_patterns = [
            r'\bif\s+[^,]+?\s+then\s+[^,]+',
            r'\bwhen\s+[^,]+?\s+then\s+[^,]+',
            r'\bif\s+[^,]+?\s*,\s*[^,]+?\s+then\s+[^,]+',
            r'\bprovided\s+that\s+[^,]+?\s+then\s+[^,]+',
            r'\bunless\s+[^,]+?\s+then\s+[^,]+',
            r'\bif\s+[^,]+?\s+otherwise\s+[^,]+',
            r'\bwhen\s+[^,]+?\s*,\s*[^,]+',
            r'\bif\s+[^,]+?\s+,\s*[^,]+',
            r'\bif\s+then\b'
        ]
        
        for pattern in conditional_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "conditional"
        
        # Priority 2: Sequential tasks - check with improved patterns
        sequential_patterns = [
            r'\bfirst\b.*?\bthen\b',
            r'\bfirst\b.*?\bthen\b.*?\bfinally\b',
            r'\bthen\b.*?\bfinally\b',
            r'\bstep\s*\d+\b.*?\bstep\s*\d+\b',
            r'\b\w+\s*,\s*then\s+\w+\b',
            r'\b\w+\s+then\s+\w+\b',
            r'\bstep\s*\d+\s*[:\-]?\s*\w+\b.*?\bstep\s*\d+\s*[:\-]?\s*\w+\b',
            r'\bbefore\s+[^,]+?\s+(?:then|and)\b',
            r'\bafter\s+[^,]+?\s+(?:then|and)\b',
            r'\b\w+\s*,\s*\w+\s*,\s*\w+\b',
            r'\bstart\s+the\s+\w+\s*,\s*\w+\s+to\s+\w+\s*,\s*\w+\s+the\s+\w+\b',
            r'\b\w+\s+the\s+\w+\s*,\s*\w+\s+to\s+\w+\s*,\s*\w+\s+the\s+\w+\b',
            r'\bbefore\s+\w+ing\b\s+[^,]*?\b(?:and|,)\s+\w+\b',
            r'\bbefore\s+[^,]+,\s*\w+.*?\band\s+\w+',
            r'\bafter\s+[^,]+,\s*\w+.*?\band\s+\w+',
            r'\bbefore\s+\w+ing\s+[^,]*,\s*\w+.*?\band\s+\w+'
        ]
        
        for pattern in sequential_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "sequential"
        
        # Priority 3: Parallel tasks - improved patterns
        parallel_patterns = [
            r'\b\w+\s+and\s+\w+\b.*?\bsimultaneously\b',
            r'\bsimultaneously\b',
            r'\bat the same time\b',
            r'\bboth\s+\w+\s+and\s+\w+\b',
            r'\b\w+\s+and\s+\w+\b.*?\bat the same time\b',
            r'\bwhile\s+\w+ing\b.*?\b(?:and|,)\s+\w+\b.*?\bsimultaneously\b',
            r'\b\w+\s+while\s+\w+ing\b',
            r'\b\w+\s+and\s+\w+\s+while\s+\w+ing\b',
            r'\bwhile\s+\w+ing,\s+\w+\b',
            r'\bwhile\s+\w+ing\b.*?\b(?:listen|watch|read|play|work|study|exercise|cook|clean)\b',
            r'\b\w+\s+while\s+\w+ing\b.*?\b(?:listen|watch|read|play|work|study|exercise|cook|clean)\b'
        ]
        
        # Check for iterative indicators first to avoid conflicts
        iterative_indicators = [
            r'\boccasionally\b',
            r'\brepeat\b',
            r'\bkeep\s+\w+ing\b',
            r'\bcontinue\s+\w+ing\b',
            r'\bagain\s+and\s+again\b',
            r'\bmultiple\s+times\b'
        ]
        
        for indicator in iterative_indicators:
            if re.search(indicator, text, re.IGNORECASE):
                # Skip parallel patterns if iterative indicators are found
                break
        else:
            # Only check parallel patterns if no iterative indicators found
            for pattern in parallel_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return "parallel"
        
        # Priority 4: Iterative tasks - improved patterns
        iterative_patterns = [
            r'\brepeat\b[^,]*?\b(times|until|while)\b',
            r'\brepeat\s+the\s+following\s+process\b',
            r'\bkeep\b[^,]*?\b(until|while)\b',
            r'\bcontinue\b[^,]*?\b(until|while)\b',
            r'\bagain\b[^,]*?\b(times|until|while)\b',
            r'\bmultiple\b[^,]*?\btimes\b',
            r'\bwhile\s+[^,]*?\b(?:do|perform|execute)\b',
            r'\bwhile\s+[^,]*?\b\w+ing\b.*?\b(?:stir|mix|cook|monitor|check|watch|observe)\b',
            r'\bwhile\s+\w+ing\b.*?\b(?:monitor|check|watch|observe|stir|mix|cook|wait|measure|track)\b',
            r'\boccasionally\b.*?\b(?:check|monitor|watch|observe|look|see|verify)\b',
            r'\boccasionally\b.*?\b\w+\b',
            r'\bwhile\s+\w+ing\b.*?\boccasionally\b',
            r'\buntil\s+[^,]*?\b(?:stop|finish|complete)\b',
            r'\brepeat\s+\d+\s+times\b',
            r'\bkeep\s+\w+ing\b',
            r'\bcontinue\s+\w+ing\b',
            r'\bdo\s+\w+\s+again\s+and\s+again\b',
            r'\bmultiple\s+\w+\s+times\b',
            r'\bover\s+and\s+over\b',
            r'\bagain\s+and\s+again\b',
            r'\bkeep\s+trying\b',
            r'\bcontinue\s+monitoring\b',
            r'\bpractice\s+\w+\s+multiple\s+times\b',
            r'\bstir\s+\w+\s+while\s+\w+\b',
            r'\bexercise\s+\d+\s+times\b'
        ]
        
        for pattern in iterative_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "iterative"
        
        # Priority 5: Priority-based tasks - improved patterns
        priority_patterns = [
            r'\burgent\b.*?\bhigh\b.*?\blow\b',
            r'\bpriority\b',
            r'\bprimary\b.*?\bsecondary\b',
            r'\burgent\b',
            r'\bhigh\s+priority\b',
            r'\blow\s+priority\b',
            r'\bfirst\s+priority\b',
            r'\bsecondary\s+priority\b',
            r'\btertiary\s+priority\b'
        ]
        
        for pattern in priority_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "priority_based"
        
        # Priority 6: Hierarchical tasks
        hierarchical_patterns = [
            r'\bmain\s+task\b',
            r'\bsub\s+task\b',
            r'\bprimary\b.*?\bsecondary\b.*?\btertiary\b'
        ]
        
        for pattern in hierarchical_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "hierarchical"
        
        # Priority 7: Resource-constrained tasks
        resource_patterns = [
            r'\buse\s+\w+\s+to\b',
            r'\bwith\s+\w+\b',
            r'\busing\s+\w+\b',
            r'\bby\s+means\s+of\s+\w+\b'
        ]
        
        for pattern in resource_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "resource_constrained"
        
        # Priority 9: Temporal chain tasks
        temporal_chain_patterns = [
            r'\bbefore\s+[^,]*?\bafter\s+[^,]*?\bthen\b',
            r'\bfirst\s+[^,]*?\bthen\s+[^,]*?\bfinally\b',
            r'\bstep\s*\d+\s+[^,]*?\bstep\s*\d+\s+[^,]*?\bstep\s*\d+',
            r'\bbefore\s+\w+ing\b.*?\bafter\s+\w+ing\b.*?\b(?:then|and)\b',
            r'\b\w+\s+before\s+\w+ing\b.*?\b\w+\s+after\s+\w+ing\b',
            r'\bbefore\s+\w+ing.*?\b\w+ing.*?\bafter\s+\w+ing\b'
        ]
        
        for pattern in temporal_chain_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "temporal_chain"
        
        # Priority 10: Complex/Composite tasks - improved patterns
        complex_indicators = [
            r'\bthen\b.*?\bif\b',
            r'\bif\b.*?\bthen\b.*?\belse\b',
            r'\bwhile\b.*?\bif\b',
            r'\bif\b.*?\bwhile\b',
            r'\bfirst\b.*?\bthen\b.*?\bif\b',
            r'\bif\b.*?\band\b.*?\bthen\b',
            r'\bwhile\b.*?\band\b.*?\bthen\b',
            r'\bif\b.*?\bor\b.*?\bthen\b',
            r'\bwhen\b.*?\bthen\b.*?\bwhile\b',
            r'\bif\b.*?\bthen\b.*?\bwhile\b'
        ]
        
        for indicator in complex_indicators:
            if re.search(indicator, text, re.IGNORECASE):
                return "complex"
        
        # Check for multiple task types
        task_types_found = 0
        if re.search(r'\bif\b.*?\bthen\b', text, re.IGNORECASE):
            task_types_found += 1
        if re.search(r'\bfirst\b.*?\bthen\b', text, re.IGNORECASE):
            task_types_found += 1
        if re.search(r'\bsimultaneously\b', text, re.IGNORECASE):
            task_types_found += 1
        if re.search(r'\brepeat\b', text, re.IGNORECASE):
            task_types_found += 1
        if re.search(r'\bwhile\b', text, re.IGNORECASE):
            task_types_found += 1
            
        if task_types_found >= 2:
            return "complex"
        
        # Priority 11: Medium complexity tasks
        if parse_result["task_complexity"] == "medium":
            return "medium_complex"
        
        # Priority 12: Simple tasks (default)
        return "simple"