#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Learner V3 - AI驱动版本
使用Claude AI进行领域分类和元素提取，完全消除硬编码
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from element_db import ElementDB

try:
    import anthropic
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  anthropic package not installed. Run: pip install anthropic")


class AIBasedLearner:
    """AI驱动的学习器 - 通过Claude进行智能分类和提取"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.db = ElementDB(db_path)
        self.stats = {
            'total_prompts': 0,
            'total_extracted': 0,
            'total_added': 0,
            'total_skipped': 0,
            'by_domain': {}
        }

        # 初始化AI客户端
        if AI_AVAILABLE:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.ai_enabled = True
                print("✅ AI classifier/extractor enabled")
            else:
                self.client = None
                self.ai_enabled = False
                print("⚠️  ANTHROPIC_API_KEY not found, using fallback")
        else:
            self.client = None
            self.ai_enabled = False

    def learn_from_prompt(self, prompt_data: Dict) -> Dict:
        """
        从单个Prompt学习（V3 - AI驱动）

        Args:
            prompt_data: {
                'prompt_id': int,
                'theme': str,
                'original_prompt': str,
                'modules': dict
            }

        Returns:
            {'added': int, 'skipped': int}
        """
        prompt_id = prompt_data['prompt_id']
        theme = prompt_data.get('theme', '')
        original_prompt = prompt_data['original_prompt']

        print(f"\n{'='*80}")
        print(f"Learning from Prompt #{prompt_id}")
        print(f"Theme: {theme}")
        print(f"{'='*80}")

        # 步骤1: AI领域分类
        print("\n🤖 Step 1: AI Domain Classification...")
        domain_info = self._ai_classify(prompt_data)

        if not domain_info or not domain_info.get('primary'):
            print("⚠️  AI无法确定领域，跳过")
            return {'added': 0, 'skipped': 0}

        primary = domain_info['primary']
        print(f"✅ Domain: {primary} (confidence: {domain_info['confidence']:.0%})")
        if domain_info.get('reasoning'):
            print(f"   Reasoning: {domain_info['reasoning']}")

        # 步骤2: AI元素提取
        print("\n🤖 Step 2: AI Element Extraction...")
        elements = self._ai_extract(prompt_data, domain_info)
        print(f"✅ Extracted {len(elements)} elements")

        # 步骤3: 存入数据库（工具层）
        added = 0
        skipped = 0

        for element in elements:
            # 生成tags
            tags = self._generate_tags(element, primary)

            # 添加中文名（如果没有）
            if 'chinese_name' not in element:
                element['chinese_name'] = element['name'].replace('_', ' ').title()

            success, element_id = self._add_to_db(element, primary, tags, prompt_id)

            if success:
                added += 1
                print(f"   ✅ {element_id}: {element.get('chinese_name', element['name'])}")
            else:
                skipped += 1

        # 保存学习记录
        self._save_learning_record(
            prompt_id, original_prompt, theme,
            domain_info, elements, added
        )

        print(f"\n✅ Summary: Added {added}, Skipped {skipped}")

        return {'added': added, 'skipped': skipped}

    def _ai_classify(self, prompt_data: Dict) -> Optional[Dict]:
        """
        AI领域分类 - 调用Claude进行智能分类
        """
        if not self.ai_enabled:
            print("   ⚠️  AI未启用，使用fallback...")
            return self._fallback_classify(prompt_data)

        try:
            # 构建AI分类提示
            theme = prompt_data.get('theme', '')
            original_prompt = prompt_data['original_prompt']
            modules_summary = self._summarize_modules(prompt_data.get('modules', {}))

            classification_prompt = f"""请分析以下图像提示词，将其分类到最合适的领域中。

提示词主题: {theme}
提示词内容: {original_prompt}
提示词模块: {modules_summary}

可选领域及其定义：
- portrait: 人物肖像、角色、人像摄影
- product: 产品摄影、商品展示
- creative: 创意作品（3D模型、盲盒、头像、插画、卡通、表情包）
- utility: 工具类功能（图像转换、翻译、修图、提高质量）
- lifestyle: 生活方式、日常场景
- scenario: 特定场景（婚礼、节日、活动）
- design: 设计相关（UI、平面、品牌）
- art: 艺术创作（油画、水彩、数字艺术）
- video: 视频相关（电影、动画、视频效果）
- interior: 室内设计、空间设计
- common: 通用场景
- misc: 无法明确分类的杂项

请返回JSON格式：
{{
  "primary": "领域ID",
  "secondary": "次要领域ID或null",
  "confidence": 0.0-1.0的置信度,
  "reasoning": "简短的分类理由"
}}"""

            # 调用Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": classification_prompt
                }]
            )

            # 解析响应
            response_text = message.content[0].text
            # 提取JSON（可能在markdown代码块中）
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_text = response_text.strip()

            result = json.loads(json_text)
            return result

        except Exception as e:
            print(f"   ⚠️  AI分类出错: {e}, 使用fallback...")
            return self._fallback_classify(prompt_data)

    def _ai_extract(self, prompt_data: Dict, domain_info: Dict) -> List[Dict]:
        """
        AI元素提取 - 调用Claude进行智能提取
        """
        if not self.ai_enabled:
            print("   ⚠️  AI未启用，使用fallback...")
            return self._fallback_extract(prompt_data, domain_info)

        try:
            domain = domain_info['primary']
            original_prompt = prompt_data['original_prompt']
            modules = prompt_data.get('modules', {})

            extraction_prompt = f"""从以下图像提示词中提取可复用的元素。

领域: {domain}
提示词内容: {original_prompt}
提示词模块: {json.dumps(modules, ensure_ascii=False, indent=2)}

请提取以下类型的可复用元素（根据领域选择合适的类型）：
- lighting_techniques: 光照技术
- camera_angles: 摄像机角度
- visual_effects: 视觉效果
- styles: 风格
- moods: 氛围/情绪
- colors: 色彩方案
- compositions: 构图方式
- materials: 材质
- poses: 姿势（人物类）
- expressions: 表情（人物类）
- environments: 环境
- technical_parameters: 技术参数

提取原则：
1. 只提取真正可复用的元素（可以应用到其他类似提示词）
2. 每个元素应该是独立的、明确的
3. 提供清晰的ai_prompt_template（可直接用于生成图像的提示词片段）
4. 至少提取3-10个元素（如果提示词足够丰富）
5. 优先提取最有价值、最特色的元素

返回JSON数组格式：
[
  {{
    "category": "元素类别（如lighting_techniques）",
    "name": "元素英文标识名（小写下划线）",
    "chinese_name": "元素中文名称",
    "ai_prompt_template": "可直接用于AI生成的提示词片段",
    "keywords": ["关键词1", "关键词2", "关键词3"],
    "reusability": 7.0  // 1-10的可复用性评分
  }}
]"""

            # 调用Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.5,
                messages=[{
                    "role": "user",
                    "content": extraction_prompt
                }]
            )

            # 解析响应
            response_text = message.content[0].text
            # 提取JSON（可能在markdown代码块中）
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_text = response_text.strip()

            elements = json.loads(json_text)
            return elements if isinstance(elements, list) else []

        except Exception as e:
            print(f"   ⚠️  AI提取出错: {e}, 使用fallback...")
            return self._fallback_extract(prompt_data, domain_info)

    def _fallback_classify(self, prompt_data: Dict) -> Dict:
        """临时fallback分类器（等待AI实现）"""
        text = (prompt_data.get('theme', '') + ' ' +
                prompt_data['original_prompt']).lower()

        # 非常简单的规则
        if any(k in text for k in ['3d', '盲盒', '头像', '插画', '漫画']):
            return {'primary': 'creative', 'confidence': 0.5, 'reasoning': 'fallback rule'}
        elif any(k in text for k in ['转', '生成', '提高', '修图']):
            return {'primary': 'utility', 'confidence': 0.5, 'reasoning': 'fallback rule'}
        else:
            return {'primary': 'portrait', 'confidence': 0.3, 'reasoning': 'fallback default'}

    def _fallback_extract(self, prompt_data: Dict, domain_info: Dict) -> List[Dict]:
        """临时fallback提取器（等待AI实现）"""
        elements = []
        modules = prompt_data.get('modules', {})

        # 基础提取：只提取数组字段
        for key, value in modules.items():
            if isinstance(value, list) and len(value) > 0:
                for item in value[:3]:  # 最多3个
                    if isinstance(item, str) and len(item) > 5:
                        elements.append({
                            'category': key,
                            'name': self._simplify_name(item),
                            'ai_prompt_template': item,
                            'keywords': item.split()[:5],
                            'reusability': 7.0
                        })

        return elements

    def _summarize_modules(self, modules: Dict) -> str:
        """总结模块信息，用于AI分类"""
        if not modules:
            return "无模块信息"

        summary_parts = []
        for key, value in modules.items():
            if isinstance(value, list):
                summary_parts.append(f"{key}: {len(value)}项")
            elif isinstance(value, dict):
                summary_parts.append(f"{key}: {len(value)}个字段")
            else:
                summary_parts.append(f"{key}: {str(value)[:50]}")

        return ", ".join(summary_parts[:5])  # 最多5项

    def _generate_tags(self, element: Dict, domain_id: str) -> List[str]:
        """生成标签（简化版）"""
        tags = [domain_id, element['category']]
        tags.extend(element.get('keywords', [])[:3])
        return list(set(tags))[:10]

    def _simplify_name(self, text: str) -> str:
        """简化名称"""
        import re
        name = re.sub(r'[^\w\s-]', '', text.lower())
        name = re.sub(r'[-\s]+', '_', name)
        return name[:50] if name else 'unnamed'

    def _add_to_db(self, element: Dict, domain_id: str, tags: List[str],
                   prompt_id: int) -> tuple:
        """添加元素到数据库"""
        # 检查是否已存在
        if self._check_exists(element['name'], domain_id, element['category']):
            return False, None

        # 生成ID
        element_id = self._generate_id(domain_id, element['category'])

        # 添加到数据库
        success = self.db.add_element(
            element_id=element_id,
            domain_id=domain_id,
            category_id=element['category'],
            name=element['name'],
            chinese_name=element.get('chinese_name'),
            ai_prompt_template=element['ai_prompt_template'],
            keywords=element.get('keywords', []),
            tags=tags,
            reusability_score=element.get('reusability', 7.0),
            source_prompts=[prompt_id],
            learned_from='universal_learner_v3_ai',
            metadata={}
        )

        return success, element_id if success else None

    def _check_exists(self, name: str, domain_id: str, category_id: str) -> bool:
        """检查元素是否已存在"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT element_id FROM elements
            WHERE domain_id = ? AND category_id = ? AND name = ?
        """, (domain_id, category_id, name))
        return cursor.fetchone() is not None

    def _generate_id(self, domain_id: str, category_id: str) -> str:
        """生成元素ID"""
        import re
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT element_id FROM elements
            WHERE domain_id = ? AND category_id = ?
            ORDER BY element_id DESC
            LIMIT 1
        """, (domain_id, category_id))

        last = cursor.fetchone()
        if last:
            match = re.search(r'_(\d+)$', last[0])
            num = int(match.group(1)) + 1 if match else 1
        else:
            num = 1

        return f"{domain_id}_{category_id}_{num:03d}"

    def _save_learning_record(self, prompt_id: int, original_prompt: str,
                              theme: str, domain_info: Dict,
                              elements: List, added_count: int):
        """保存学习记录"""
        quality_score = min(10.0, 5.0 + len(elements) * 0.5)

        if len(elements) >= 10:
            complexity = 'complex'
        elif len(elements) >= 5:
            complexity = 'medium'
        else:
            complexity = 'simple'

        self.db.save_source_prompt(
            prompt_id=prompt_id,
            original_prompt=original_prompt,
            theme=theme,
            domain_classification=json.dumps(domain_info, ensure_ascii=False),
            quality_score=quality_score,
            complexity=complexity,
            extracted_elements_count=added_count
        )

    def close(self):
        """关闭数据库"""
        self.db.close()


# 测试用
if __name__ == "__main__":
    print("Universal Learner V3 - AI驱动版本")
    print("注意：当前使用fallback实现，等待AI集成")
