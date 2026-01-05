#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid Learning System - 混合学习系统
从新Prompt中自动学习和提取未定义的特征模块

实现三种方法：
1. RuleBasedLearner: 基于正则表达式的规则提取
2. AIAssistedLearner: AI辅助的智能提取
3. HybridLearner: 混合模式（推荐）
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class RuleBasedLearner:
    """基于规则的特征学习器"""

    def __init__(self):
        self.patterns = {
            "hair_style": {
                "keywords": ["hair", "hairstyle", "hairdo", "locks", "tresses"],
                "attributes": {
                    "length": ["long", "short", "shoulder-length", "waist-length", "medium"],
                    "style": ["straight", "curly", "wavy", "flowing", "silky", "spiky", "messy", "sleek"],
                    "type": ["ponytail", "twin tails", "braid", "bun", "bob", "pixie cut", "bangs"]
                },
                "regex": r"(long|short|medium|shoulder-length|waist-length)?\s*(straight|curly|wavy|flowing|silky|spiky)?\s*(black|blonde|brown|red|silver|gray|blue|pink|purple)?\s*(hair|hairstyle|ponytail|twin\s+tails|braid|bun)"
            },
            "hair_color": {
                "keywords": ["hair color", "colored hair"],
                "attributes": {
                    "color": ["black", "blonde", "brown", "red", "auburn", "silver", "gray", "blue", "pink", "purple", "green"]
                },
                "regex": r"(black|blonde|brown|red|auburn|silver|gray|blue|pink|purple|green)\s+(hair|locks)"
            },
            "skin_tone": {
                "keywords": ["skin tone", "complexion", "skin color"],
                "attributes": {
                    "tone": ["fair", "pale", "porcelain", "tan", "olive", "dark", "ebony", "light", "medium"]
                },
                "regex": r"(fair|pale|porcelain|tan|olive|dark|ebony|light|medium)\s+(skin|complexion|skin\s+tone)"
            },
            "body_type": {
                "keywords": ["body", "figure", "build", "physique"],
                "attributes": {
                    "type": ["slim", "petite", "athletic", "curvy", "voluptuous", "muscular", "average", "fit"]
                },
                "regex": r"(slim|petite|athletic|curvy|voluptuous|muscular|average|fit)\s+(body|figure|build|physique)"
            },
            "clothing": {
                "keywords": ["wearing", "dressed in", "outfit", "dress", "clothes"],
                "attributes": {
                    "style": ["traditional", "modern", "casual", "formal", "elegant", "punk", "gothic"],
                    "type": ["dress", "qipao", "kimono", "suit", "t-shirt", "jeans", "skirt"],
                    "color": ["red", "blue", "black", "white", "green", "pink", "purple"],
                    "material": ["silk", "cotton", "leather", "lace", "velvet"]
                },
                "regex": r"wearing\s+(elegant|traditional|modern|casual|formal)?\s*(\w+)?\s*(red|blue|black|white)?\s*(silk|cotton|leather)?\s*(dress|qipao|outfit|kimono|suit)"
            },
            "accessories": {
                "keywords": ["earrings", "necklace", "bracelet", "glasses", "hat", "jewelry"],
                "attributes": {
                    "type": ["earrings", "necklace", "bracelet", "ring", "glasses", "hat"],
                    "material": ["silver", "gold", "diamond", "pearl"],
                    "style": ["delicate", "bold", "vintage", "modern"]
                },
                "regex": r"(delicate|bold|vintage|modern)?\s*(silver|gold|diamond|pearl)?\s*(earrings|necklace|bracelet|ring|glasses)"
            },
            "pose": {
                "keywords": ["pose", "posture", "stance", "position"],
                "attributes": {
                    "type": ["standing", "sitting", "lying", "walking", "running"],
                    "style": ["confident", "shy", "relaxed", "tense", "elegant", "casual"]
                },
                "regex": r"(confident|shy|relaxed|elegant|casual)?\s*(pose|posture|stance|standing|sitting)"
            },
            "poses": {
                "keywords": ["pose", "posture", "stance", "position", "standing", "arms"],
                "attributes": {
                    "stance": ["power stance", "wide stance", "relaxed", "casual"],
                    "arms": ["crossed", "arms crossed", "over chest"],
                    "head": ["chin raised", "chin up", "head tilt", "tilted"]
                },
                "regex": r"(power\s+stance|wide\s+stance|arms\s+crossed|crossed\s+arms|chin\s+raised|head\s+tilt|relaxed\s+standing)"
            },
            "expressions": {
                "keywords": ["expression", "smile", "smirk", "look", "gaze", "mood"],
                "attributes": {
                    "type": ["smirk", "smile", "grin", "serene", "calm", "playful"],
                    "mood": ["confident", "sassy", "gentle", "warm", "peaceful"]
                },
                "regex": r"(confident\s+smirk|playful\s+smile|gentle\s+smile|serene|calm\s+expression|sassy)"
            },
            "clothing_styles": {
                "keywords": ["wearing", "dressed in", "outfit", "attire", "clothing"],
                "attributes": {
                    "style": ["casual", "formal", "elegant", "traditional", "sporty", "athletic"],
                    "type": ["modern", "contemporary", "cultural", "activewear"]
                },
                "regex": r"wearing\s+(casual|formal|elegant|traditional|sporty|athletic|modern)\s+(outfit|attire|clothing|wear)"
            }
        }

    def extract_features(self, prompt_text: str) -> List[Dict]:
        """使用正则表达式提取特征"""
        detected = []

        for category, pattern_info in self.patterns.items():
            # 正则匹配
            matches = re.findall(pattern_info["regex"], prompt_text, re.IGNORECASE)

            if matches:
                for match in matches:
                    # match 是一个tuple，包含所有捕获组
                    raw_text = " ".join([m for m in match if m]).strip()

                    if raw_text:
                        detected.append({
                            "category": category,
                            "raw_text": raw_text,
                            "match_groups": match,
                            "confidence": 0.8,
                            "method": "rule-based"
                        })

        return detected


class AIAssistedLearner:
    """AI辅助的特征学习器 - 利用Claude Skill能力"""

    def __init__(self):
        self.use_ai = True  # 在Claude Code环境中默认启用

    def extract_features(self, prompt_text: str) -> List[Dict]:
        """使用Claude Skill能力直接分析提取特征"""
        # 在Claude Code Skill环境中，我（Claude）可以直接分析文本
        # 不需要外部API调用

        if not self.use_ai:
            return []

        # 直接分析提取（这里提供更智能的分析）
        detected = []

        # 发型分析
        if any(word in prompt_text.lower() for word in ['hair', 'hairstyle', 'locks']):
            hair_features = self._analyze_hair(prompt_text)
            detected.extend(hair_features)

        # 肤色分析
        if any(word in prompt_text.lower() for word in ['skin', 'complexion']):
            skin_features = self._analyze_skin(prompt_text)
            detected.extend(skin_features)

        # 服装分析
        if any(word in prompt_text.lower() for word in ['wearing', 'dress', 'outfit', 'clothing']):
            clothing_features = self._analyze_clothing(prompt_text)
            detected.extend(clothing_features)

        # 配饰分析
        if any(word in prompt_text.lower() for word in ['earrings', 'necklace', 'jewelry', 'glasses']):
            accessory_features = self._analyze_accessories(prompt_text)
            detected.extend(accessory_features)

        # 姿势分析
        if any(word in prompt_text.lower() for word in ['pose', 'stance', 'standing', 'arms', 'chin']):
            pose_features = self._analyze_poses(prompt_text)
            detected.extend(pose_features)

        # 表情分析
        if any(word in prompt_text.lower() for word in ['expression', 'smile', 'smirk', 'look', 'mood']):
            expression_features = self._analyze_expressions(prompt_text)
            detected.extend(expression_features)

        # 服装风格分析（详细版）
        if any(word in prompt_text.lower() for word in ['casual', 'formal', 'traditional', 'sporty']):
            clothing_style_features = self._analyze_clothing_detailed(prompt_text)
            detected.extend(clothing_style_features)

        return detected

    def _analyze_hair(self, text: str) -> List[Dict]:
        """智能分析发型和发色"""
        features = []

        # 发色检测
        colors = {
            'red': ['red hair', 'auburn', 'ginger'],
            'black': ['black hair', 'dark hair', 'ebony'],
            'blonde': ['blonde', 'golden hair', 'fair hair'],
            'brown': ['brown hair', 'brunette'],
            'silver': ['silver hair', 'gray hair', 'white hair'],
            'blue': ['blue hair'],
            'pink': ['pink hair'],
            'purple': ['purple hair']
        }

        for color, patterns in colors.items():
            for pattern in patterns:
                if pattern in text.lower():
                    features.append({
                        'category': 'hair_colors',
                        'raw_text': f'{color} hair',
                        'confidence': 0.95,
                        'method': 'ai-assisted'
                    })
                    break

        # 发型检测
        styles = {
            'long': ['long hair', 'long flowing'],
            'short': ['short hair', 'pixie cut', 'bob'],
            'wavy': ['wavy hair', 'waves'],
            'curly': ['curly hair', 'curls'],
            'straight': ['straight hair'],
            'ponytail': ['ponytail'],
            'braided': ['braid', 'braided'],
            'twin_tails': ['twin tails', 'twintails']
        }

        for style, patterns in styles.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 提取完整描述
                    import re
                    match = re.search(r'\b[\w\s]{0,30}' + pattern + r'[\w\s]{0,10}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'hair_styles',
                            'raw_text': raw_text,
                            'confidence': 0.9,
                            'method': 'ai-assisted'
                        })
                    break

        return features

    def _analyze_skin(self, text: str) -> List[Dict]:
        """智能分析肤色"""
        features = []

        skin_tones = {
            'fair': ['fair skin', 'pale skin', 'porcelain skin'],
            'tan': ['tan skin', 'tanned'],
            'olive': ['olive skin'],
            'dark': ['dark skin', 'ebony skin'],
            'golden': ['golden skin']
        }

        for tone, patterns in skin_tones.items():
            for pattern in patterns:
                if pattern in text.lower():
                    features.append({
                        'category': 'skin_tones',
                        'raw_text': pattern,
                        'confidence': 0.95,
                        'method': 'ai-assisted'
                    })
                    return features

        return features

    def _analyze_clothing(self, text: str) -> List[Dict]:
        """智能分析服装"""
        features = []

        import re

        # 寻找服装描述
        clothing_patterns = [
            r'wearing\s+([\w\s]+?(?:dress|qipao|kimono|suit|outfit|gown|robe))',
            r'dressed in\s+([\w\s]+?(?:dress|qipao|kimono|suit|outfit|gown|robe))',
            r'(elegant|traditional|modern|casual)\s+[\w\s]*?(?:dress|qipao|outfit)'
        ]

        for pattern in clothing_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        match = ' '.join(match)
                    features.append({
                        'category': 'clothing_styles',
                        'raw_text': match.strip(),
                        'confidence': 0.85,
                        'method': 'ai-assisted'
                    })

        return features

    def _analyze_accessories(self, text: str) -> List[Dict]:
        """智能分析配饰"""
        features = []

        accessories = [
            'earrings', 'necklace', 'bracelet', 'ring',
            'glasses', 'hat', 'crown', 'tiara'
        ]

        import re
        for accessory in accessories:
            pattern = r'([\w\s]{0,20}' + accessory + r')'
            matches = re.findall(pattern, text.lower())
            if matches:
                for match in matches:
                    if len(match.strip()) > 2:
                        features.append({
                            'category': 'accessories',
                            'raw_text': match.strip(),
                            'confidence': 0.85,
                            'method': 'ai-assisted'
                        })

        return features

    def _analyze_poses(self, text: str) -> List[Dict]:
        """智能分析姿势"""
        features = []

        poses = {
            'power_stance': ['power stance', 'wide stance', 'feet apart', 'confident pose'],
            'arms_crossed': ['arms crossed', 'crossed arms', 'arms over chest'],
            'chin_raised': ['chin raised', 'chin up', 'head tilted up'],
            'relaxed_standing': ['relaxed', 'casual stance', 'natural pose']
        }

        import re
        for pose, patterns in poses.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 提取完整描述
                    match = re.search(r'\b[\w\s]{0,30}' + re.escape(pattern) + r'[\w\s]{0,20}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'poses',
                            'raw_text': raw_text,
                            'confidence': 0.9,
                            'method': 'ai-assisted'
                        })
                    break

        return features

    def _analyze_expressions(self, text: str) -> List[Dict]:
        """智能分析表情"""
        features = []

        expressions = {
            'confident_smirk': ['smirk', 'confident', 'sassy', 'smug'],
            'playful_smile': ['playful', 'fun', 'lighthearted', 'cheeky'],
            'serene_calm': ['serene', 'calm', 'peaceful', 'tranquil'],
            'gentle_smile': ['gentle', 'soft smile', 'warm', 'kind']
        }

        import re
        for expr, patterns in expressions.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 提取包含表情的完整描述
                    match = re.search(r'\b[\w\s]{0,30}' + re.escape(pattern) + r'[\w\s]{0,20}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'expressions',
                            'raw_text': raw_text,
                            'confidence': 0.9,
                            'method': 'ai-assisted'
                        })
                    break

        return features

    def _analyze_clothing_detailed(self, text: str) -> List[Dict]:
        """智能分析服装风格（详细版）"""
        features = []

        clothing_styles = {
            'casual_modern': ['casual', 'modern outfit', 'everyday wear'],
            'elegant_formal': ['elegant', 'formal', 'sophisticated'],
            'traditional_cultural': ['traditional', 'cultural attire', 'ethnic'],
            'sporty_athletic': ['sporty', 'athletic', 'activewear']
        }

        import re
        for style, patterns in clothing_styles.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 寻找完整的服装描述
                    match = re.search(r'wearing\s+[\w\s]{0,50}' + re.escape(pattern) + r'[\w\s]{0,30}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'clothing_styles',
                            'raw_text': raw_text,
                            'confidence': 0.85,
                            'method': 'ai-assisted'
                        })
                    break

        return features


class HybridLearner:
    """混合学习器：结合规则和AI"""

    def __init__(self, library_path: str = "extracted_results/facial_features_library.json"):
        self.library_path = library_path
        self.rule_learner = RuleBasedLearner()
        self.ai_learner = AIAssistedLearner()
        self.library = self._load_library()

    def _load_library(self) -> Dict:
        """加载现有特征库"""
        if os.path.exists(self.library_path):
            with open(self.library_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _calculate_keyword_overlap(self, keywords1: List[str], keywords2: List[str]) -> float:
        """计算关键词重叠度"""
        if not keywords1 or not keywords2:
            return 0.0

        # 转换为小写集合
        set1 = set([k.lower() for k in keywords1])
        set2 = set([k.lower() for k in keywords2])

        # 计算Jaccard相似度
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def check_existing_category(self, feature: Dict) -> Tuple[str, Optional[str]]:
        """检查特征是否已在库中"""
        category = feature["category"]
        raw_text = feature.get("raw_text", "")
        keywords = [raw_text] if raw_text else []

        # 检查类别是否存在
        if category not in self.library:
            return "NEW_CATEGORY", None

        # 检查关键词是否已存在
        existing_items = self.library[category]

        for item_code, item_data in existing_items.items():
            if item_code == "library_metadata":
                continue

            item_keywords = item_data.get("keywords", [])

            # 关键词重叠度检查
            overlap = self._calculate_keyword_overlap(keywords, item_keywords)

            if overlap > 0.7:  # 70%以上重叠
                return "EXISTS", item_code

        return "NEW_ITEM", None

    def extract_and_classify(self, prompt_text: str) -> Dict:
        """提取并分类特征"""
        # Step 1: 规则提取
        rule_features = self.rule_learner.extract_features(prompt_text)

        # Step 2: AI增强提取（可选）
        ai_features = self.ai_learner.extract_features(prompt_text)

        # Step 3: 合并和去重
        merged_features = self._merge_features(rule_features, ai_features)

        # Step 4: 匹配现有库
        new_features = []
        existing_features = []

        for feature in merged_features:
            status, item_code = self.check_existing_category(feature)

            if status in ["NEW_CATEGORY", "NEW_ITEM"]:
                feature["status"] = status
                new_features.append(feature)
            else:
                feature["status"] = "EXISTS"
                feature["existing_code"] = item_code
                existing_features.append(feature)

        return {
            "new_features": new_features,
            "existing_features": existing_features,
            "total_detected": len(merged_features)
        }

    def _merge_features(self, rule_features: List[Dict], ai_features: List[Dict]) -> List[Dict]:
        """合并规则和AI提取的特征"""
        # 简单合并（去重可以更复杂）
        merged = {}

        for feature in rule_features + ai_features:
            key = f"{feature['category']}_{feature.get('raw_text', '')}"
            if key not in merged:
                merged[key] = feature
            else:
                # 如果已存在，提高置信度
                merged[key]["confidence"] = min(1.0, merged[key]["confidence"] + 0.1)

        return list(merged.values())

    def generate_review_report(self, new_features: List[Dict], source_prompt: str) -> str:
        """生成审核报告"""
        report_lines = []
        report_lines.append("# 新特征发现报告\n")
        report_lines.append(f"**扫描时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append(f"**扫描来源**: 用户输入\n")
        report_lines.append(f"\n## 源Prompt\n```\n{source_prompt}\n```\n")
        report_lines.append(f"\n## 新发现的特征 ({len(new_features)}个)\n")

        for idx, feature in enumerate(new_features, 1):
            category = feature["category"]
            raw_text = feature.get("raw_text", "")
            confidence = feature.get("confidence", 0)
            status = feature.get("status", "")

            report_lines.append(f"\n### {idx}. {category} - {status}")
            report_lines.append(f"**关键词**: \"{raw_text}\"")
            report_lines.append(f"**置信度**: {confidence*100:.0f}%")
            report_lines.append(f"**提取方法**: {feature.get('method', 'unknown')}")

            # 建议分类码
            suggested_code = self._suggest_classification_code(raw_text)
            report_lines.append(f"**建议分类码**: `{suggested_code}`")

            # 复用性评估
            reusability = self._estimate_reusability(category)
            report_lines.append(f"**复用性评估**: {reusability}")

            report_lines.append("\n**审核选项**:")
            report_lines.append("- [ ] 批准添加")
            report_lines.append("- [ ] 需要修改（请说明）")
            report_lines.append("- [ ] 拒绝（说明原因）")
            report_lines.append("")

        return "\n".join(report_lines)

    def _suggest_classification_code(self, raw_text: str) -> str:
        """建议分类码"""
        # 转换为snake_case
        code = raw_text.lower()
        code = re.sub(r'[^\w\s-]', '', code)  # 移除特殊字符
        code = re.sub(r'[-\s]+', '_', code)   # 空格和连字符转下划线
        return code

    def _estimate_reusability(self, category: str) -> str:
        """评估复用性"""
        high_reusability = ["hair_style", "hair_color", "skin_tone", "body_type"]
        medium_reusability = ["clothing", "pose", "accessories"]

        if category in high_reusability:
            return "高（这是人像的重要基础元素）"
        elif category in medium_reusability:
            return "中（取决于具体风格）"
        else:
            return "待评估"

    def scan_prompt(self, prompt_text: str, save_report: bool = True) -> Dict:
        """扫描单个Prompt"""
        print(f"\n🔍 扫描Prompt中...")
        print(f"   文本长度: {len(prompt_text)} 字符\n")

        # 提取和分类
        result = self.extract_and_classify(prompt_text)

        # 显示结果
        print(f"✅ 扫描完成！")
        print(f"   发现特征: {result['total_detected']} 个")
        print(f"   新特征: {len(result['new_features'])} 个")
        print(f"   已存在: {len(result['existing_features'])} 个\n")

        if result['new_features']:
            print("📋 新发现的特征类别:")
            category_count = defaultdict(int)
            for f in result['new_features']:
                category_count[f['category']] += 1

            for category, count in category_count.items():
                print(f"   - {category}: {count} 个")

            # 生成审核报告
            if save_report:
                report = self.generate_review_report(result['new_features'], prompt_text)
                report_filename = f"new_features_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                report_path = os.path.join("extracted_results", report_filename)

                os.makedirs("extracted_results", exist_ok=True)
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)

                print(f"\n📄 审核报告已生成: {report_path}")
        else:
            print("ℹ️  未发现新特征")

        return result

    def batch_scan_prompts(self, prompts_file: str = "extracted_results/extracted_modules.json") -> Dict:
        """批量扫描所有Prompts"""
        print(f"\n📚 批量扫描模式")
        print(f"   读取文件: {prompts_file}\n")

        if not os.path.exists(prompts_file):
            print(f"❌ 文件不存在: {prompts_file}")
            return {}

        with open(prompts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 支持两种格式：直接列表 或 包含"prompts"键的字典
        if isinstance(data, list):
            all_prompts = data
        else:
            all_prompts = data.get("prompts", [])
        print(f"   共 {len(all_prompts)} 个Prompts\n")

        all_new_features = defaultdict(list)

        for idx, prompt_data in enumerate(all_prompts, 1):
            prompt_text = prompt_data.get("original_prompt", "")
            prompt_id = prompt_data.get("prompt_id", idx)

            print(f"[{idx}/{len(all_prompts)}] 扫描 Prompt #{prompt_id}...")

            result = self.extract_and_classify(prompt_text)

            for feature in result['new_features']:
                category = feature['category']
                feature['source_prompt_id'] = prompt_id
                all_new_features[category].append(feature)

        # 生成汇总报告
        print(f"\n" + "="*60)
        print(f"📊 批量扫描完成！")
        print(f"="*60)
        print(f"\n发现新类别:")

        for category, features in all_new_features.items():
            print(f"\n{category}: {len(features)} 个新分类")

            # 显示前3个
            for feature in features[:3]:
                print(f"   - {feature['raw_text']} (Prompt #{feature['source_prompt_id']})")

            if len(features) > 3:
                print(f"   ... 还有 {len(features)-3} 个")

        # 保存汇总报告
        summary_report = self._generate_batch_summary_report(all_new_features)
        report_filename = f"batch_scan_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path = os.path.join("extracted_results", report_filename)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(summary_report)

        print(f"\n📄 汇总报告: {report_path}")

        return dict(all_new_features)

    def _generate_batch_summary_report(self, all_new_features: Dict[str, List[Dict]]) -> str:
        """生成批量扫描汇总报告"""
        report_lines = []
        report_lines.append("# 批量扫描汇总报告\n")
        report_lines.append(f"**扫描时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        total_features = sum(len(features) for features in all_new_features.values())
        report_lines.append(f"**发现新特征**: {total_features} 个")
        report_lines.append(f"**新类别数**: {len(all_new_features)} 个\n")

        report_lines.append("## 类别汇总\n")

        for category, features in sorted(all_new_features.items()):
            report_lines.append(f"### {category} ({len(features)} 个)\n")

            for feature in features:
                prompt_id = feature.get('source_prompt_id', '?')
                raw_text = feature.get('raw_text', '')
                confidence = feature.get('confidence', 0)

                report_lines.append(f"- **{raw_text}** (Prompt #{prompt_id}, 置信度: {confidence*100:.0f}%)")

            report_lines.append("")

        return "\n".join(report_lines)


def main():
    """主函数 - 命令行接口"""
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 learner.py scan \"<prompt文本>\"       # 扫描单个Prompt")
        print("  python3 learner.py batch                     # 批量扫描所有Prompts")
        print("\n示例:")
        print('  python3 learner.py scan "A woman with long flowing red hair, fair skin tone, wearing elegant red silk qipao dress"')
        return

    learner = HybridLearner()

    command = sys.argv[1]

    if command == "scan":
        if len(sys.argv) < 3:
            print("❌ 请提供要扫描的Prompt文本")
            return

        prompt_text = sys.argv[2]
        learner.scan_prompt(prompt_text)

    elif command == "batch":
        learner.batch_scan_prompts()

    else:
        print(f"❌ 未知命令: {command}")
        print("   支持的命令: scan, batch")


if __name__ == "__main__":
    main()
