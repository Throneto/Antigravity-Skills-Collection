#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Learner - 通用学习器实现
从18个源Prompts中提取可复用元素，存入Universal Elements Database
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from element_db import ElementDB


class DomainClassifier:
    """领域分类器"""

    def __init__(self):
        # 领域关键词权重表
        self.keywords = {
            'portrait': {
                'face': 3, 'woman': 3, 'man': 3, 'person': 3, '人物': 3,
                'eyes': 2, 'skin': 2, 'makeup': 2, 'hair': 2, '面部': 3,
                'beauty': 2, 'facial': 2, 'portrait': 3, 'cosplay': 2,
                '肖像': 3, '美女': 3, '人像': 3, '角色': 2
            },
            'product': {
                'product': 3, 'book': 2, 'bottle': 2, 'watch': 2,
                'packaging': 2, 'item': 2, 'object': 1, '产品': 3,
                'collector': 2, 'premium': 1, '周边': 2, '自行车': 2,
                '物品': 2, 'bike': 2, 'edition': 1
            },
            'design': {
                'poster': 3, 'layout': 3, 'bento': 3, 'ui': 3, '海报': 3,
                'typography': 2, 'graphic': 2, 'card': 1, '设计': 2,
                'grid': 2, 'design': 1, '网格': 2, '布局': 3,
                'infographic': 2, '信息图': 2, '指南': 2
            },
            'art': {
                'painting': 3, 'artistic': 2, 'surreal': 3, '绘画': 3,
                'illustration': 2, 'art': 1, 'canvas': 2, '艺术': 2,
                'brushstroke': 2, 'effect': 1, '水墨': 3, '插画': 3,
                '卷轴': 2, '拟人': 2, '超现实': 3
            },
            'video': {
                'video': 3, 'scene': 2, 'cinematic': 3, '视频': 3,
                'motion': 2, 'camera movement': 3, 'sequence': 2,
                '分镜': 3, '武侠': 2, '动作': 2, 'action': 2
            },
            'interior': {
                'interior': 3, 'room': 2, 'living room': 3, '室内': 3,
                'bedroom': 3, 'furniture': 2, 'space': 1, '空间': 2,
                'kitchen': 3, 'home': 1
            },
            'common': {
                'photography': 2, 'camera': 2, 'lens': 2, '摄影': 2,
                'lighting': 2, 'iso': 1, 'aperture': 1, '光照': 2
            }
        }

    def classify(self, prompt_text: str, theme: str = "") -> Dict:
        """
        分类Prompt到领域

        Returns:
            {
                'primary': 'product',
                'secondary': ['common'],
                'confidence': 0.75,
                'scores': {...}
            }
        """
        # 合并prompt和theme
        text_lower = (prompt_text + " " + theme).lower()

        # 计算各领域得分
        domain_scores = {domain: 0 for domain in self.keywords.keys()}

        for domain, kw_dict in self.keywords.items():
            for keyword, weight in kw_dict.items():
                if keyword in text_lower:
                    domain_scores[domain] += weight

        # 排序
        sorted_domains = sorted(
            domain_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # 确定主次领域
        primary = None
        secondary = []

        if sorted_domains[0][1] > 5:
            primary = sorted_domains[0][0]

        # 次领域：得分 > 3 但不是主领域
        for domain, score in sorted_domains[1:]:
            if score > 3:
                secondary.append(domain)

        # common通常作为次领域
        if domain_scores['common'] > 2 and primary != 'common':
            if 'common' not in secondary:
                secondary.append('common')

        confidence = sorted_domains[0][1] / 20 if sorted_domains[0][1] > 0 else 0

        return {
            'primary': primary,
            'secondary': secondary,
            'confidence': min(1.0, confidence),
            'scores': dict(sorted_domains[:5])
        }


class ElementExtractor:
    """元素提取器"""

    def __init__(self):
        pass

    def extract(self, prompt_data: Dict, domain_info: Dict) -> List[Dict]:
        """从Prompt中提取元素"""
        elements = []
        primary = domain_info['primary']

        if not primary:
            return elements

        # 根据领域调用不同的提取策略
        if primary == 'product':
            elements.extend(self._extract_product_elements(prompt_data))
        elif primary == 'design':
            elements.extend(self._extract_design_elements(prompt_data))
        elif primary == 'art':
            elements.extend(self._extract_art_elements(prompt_data))
        elif primary == 'video':
            elements.extend(self._extract_video_elements(prompt_data))
        elif primary == 'portrait':
            elements.extend(self._extract_portrait_elements(prompt_data))

        # 通用摄影技术（所有领域）
        elements.extend(self._extract_common_elements(prompt_data))

        return elements

    def _extract_product_elements(self, prompt_data: Dict) -> List[Dict]:
        """提取产品摄影元素"""
        elements = []
        modules = prompt_data.get('modules', {})
        original = prompt_data.get('original_prompt', '')

        # 1. 产品类型
        subject = modules.get('subject_variables', {})
        main_subject = subject.get('main', '')

        if main_subject:
            # 简化产品名称
            product_name = self._simplify_name(main_subject)
            if product_name:
                elements.append({
                    'category': 'product_types',
                    'name': product_name,
                    'ai_prompt_template': main_subject[:100],
                    'keywords': self._extract_keywords(main_subject),
                    'reusability': self._estimate_reusability(main_subject, 'product_types')
                })

        # 2. 摄影技术
        tech = modules.get('technical_parameters', {})
        if tech.get('camera'):
            elements.append({
                'category': 'photography_techniques',
                'name': self._simplify_name(tech['camera']),
                'ai_prompt_template': tech['camera'],
                'keywords': self._extract_keywords(tech['camera']),
                'reusability': 9.0
            })

        # 3. 光照设置
        if tech.get('lighting'):
            elements.append({
                'category': 'lighting_techniques',
                'name': self._simplify_name(tech['lighting']),
                'ai_prompt_template': tech['lighting'],
                'keywords': self._extract_keywords(tech['lighting']),
                'reusability': 8.5
            })

        # 4. 材质纹理
        materials = self._find_materials(original)
        for material in materials:
            elements.append({
                'category': 'material_textures',
                'name': self._simplify_name(material),
                'ai_prompt_template': material,
                'keywords': self._extract_keywords(material),
                'reusability': 8.0
            })

        return elements

    def _extract_design_elements(self, prompt_data: Dict) -> List[Dict]:
        """提取设计元素"""
        elements = []
        modules = prompt_data.get('modules', {})
        original = prompt_data.get('original_prompt', '')

        # 1. 布局系统
        comp = modules.get('composition', {})
        layout_desc = comp.get('layout', '')
        if layout_desc:
            elements.append({
                'category': 'layout_systems',
                'name': self._simplify_name(layout_desc),
                'ai_prompt_template': layout_desc,
                'keywords': self._extract_keywords(layout_desc),
                'reusability': 8.5
            })

        # 2. 视觉效果
        visual = modules.get('visual_style', {})
        art_style = visual.get('art_style', '')
        if 'glass' in art_style.lower() or '玻璃' in original or '透明' in original:
            elements.append({
                'category': 'visual_effects',
                'name': 'glassmorphism',
                'ai_prompt_template': 'frosted glass effect, translucent backdrop, blur filter',
                'keywords': ['glassmorphism', 'frosted glass', 'translucent', 'blur'],
                'reusability': 8.0
            })

        # 3. 色彩方案
        colors = modules.get('color_scheme', {})
        if colors:
            palette = colors.get('palette', [])
            if palette:
                elements.append({
                    'category': 'color_schemes',
                    'name': self._simplify_name(colors.get('tone', 'custom_palette')),
                    'ai_prompt_template': f"{colors.get('tone', '')}, colors: {', '.join(palette[:5])}",
                    'keywords': self._extract_keywords(colors.get('tone', '')) + palette[:3],
                    'reusability': 7.0
                })

        return elements

    def _extract_art_elements(self, prompt_data: Dict) -> List[Dict]:
        """提取艺术风格元素"""
        elements = []
        modules = prompt_data.get('modules', {})
        original = prompt_data.get('original_prompt', '')

        # 1. 艺术风格
        visual = modules.get('visual_style', {})
        art_style = visual.get('art_style', '')
        if art_style:
            elements.append({
                'category': 'art_styles',
                'name': self._simplify_name(art_style),
                'ai_prompt_template': art_style,
                'keywords': self._extract_keywords(art_style),
                'reusability': 7.5
            })

        # 2. 特殊效果
        if '玻璃' in original and '爆炸' in original:
            elements.append({
                'category': 'special_effects',
                'name': 'glass_shatter_explosion',
                'ai_prompt_template': 'dynamic glass shatter explosion, flying fragments, motion blur',
                'keywords': ['glass', 'shatter', 'explosion', 'fragments'],
                'reusability': 7.0
            })

        if '水墨' in original or 'ink' in original.lower():
            elements.append({
                'category': 'art_styles',
                'name': 'chinese_ink_painting',
                'ai_prompt_template': 'traditional Chinese ink painting, flowing brush strokes, minimalist',
                'keywords': ['Chinese ink', 'painting', 'brush', 'traditional'],
                'reusability': 7.5
            })

        return elements

    def _extract_video_elements(self, prompt_data: Dict) -> List[Dict]:
        """提取视频生成元素"""
        elements = []
        modules = prompt_data.get('modules', {})

        # 1. 场景类型
        subject = modules.get('subject_variables', {})
        scene_type = subject.get('main', '')
        if scene_type:
            elements.append({
                'category': 'scene_types',
                'name': self._simplify_name(scene_type),
                'ai_prompt_template': scene_type[:100],
                'keywords': self._extract_keywords(scene_type),
                'reusability': 6.5
            })

        # 2. 相机运动
        tech = modules.get('technical_parameters', {})
        camera_movement = tech.get('camera_movement', tech.get('camera', ''))
        if camera_movement:
            elements.append({
                'category': 'camera_movements',
                'name': self._simplify_name(camera_movement),
                'ai_prompt_template': camera_movement,
                'keywords': self._extract_keywords(camera_movement),
                'reusability': 8.0
            })

        return elements

    def _extract_portrait_elements(self, prompt_data: Dict) -> List[Dict]:
        """提取人像元素（已有库，主要补充）"""
        elements = []
        original = prompt_data.get('original_prompt', '')

        # 只提取特殊的、库中没有的元素
        if 'cosplay' in original.lower():
            elements.append({
                'category': 'photography_styles',
                'name': 'cosplay_photography',
                'ai_prompt_template': 'cosplay photography, character costume, detailed props',
                'keywords': ['cosplay', 'costume', 'character', 'props'],
                'reusability': 7.0
            })

        return elements

    def _extract_common_elements(self, prompt_data: Dict) -> List[Dict]:
        """提取通用摄影元素"""
        elements = []
        modules = prompt_data.get('modules', {})

        tech = modules.get('technical_parameters', {})

        # 分辨率
        resolution = tech.get('resolution', '')
        if resolution and ('4k' in resolution.lower() or '8k' in resolution.lower()):
            elements.append({
                'category': 'technical_effects',
                'name': self._simplify_name(resolution),
                'ai_prompt_template': resolution,
                'keywords': self._extract_keywords(resolution),
                'reusability': 9.5
            })

        return elements

    def _simplify_name(self, text: str) -> str:
        """简化名称为element name格式"""
        # 移除特殊字符
        name = re.sub(r'[^\w\s-]', '', text.lower())
        # 转为snake_case
        name = re.sub(r'[-\s]+', '_', name)
        # 限制长度
        name = '_'.join(name.split('_')[:6])
        return name[:50] if name else 'unnamed'

    def _extract_keywords(self, text: str) -> List[str]:
        """从文本提取关键词"""
        # 简单分词
        words = re.findall(r'\b[\w]+\b', text.lower())
        # 过滤停用词
        stopwords = {'a', 'an', 'the', 'with', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        return keywords[:10]

    def _estimate_reusability(self, text: str, category: str) -> float:
        """估计复用性评分"""
        # 基础评分
        base_scores = {
            'photography_techniques': 9.0,
            'lighting_techniques': 8.5,
            'technical_effects': 9.5,
            'layout_systems': 8.5,
            'art_styles': 7.5,
            'product_types': 6.5,
            'scene_types': 6.5
        }

        base = base_scores.get(category, 7.0)

        # 长度惩罚（太具体）
        word_count = len(text.split())
        if word_count > 15:
            base -= 1.0
        elif word_count > 25:
            base -= 2.0

        # 通用词汇加分
        generic_words = ['modern', 'professional', 'high', 'quality', 'premium']
        if any(w in text.lower() for w in generic_words):
            base += 0.5

        return min(10.0, max(1.0, base))

    def _find_materials(self, text: str) -> List[str]:
        """查找材质描述"""
        materials = []
        material_patterns = [
            r'([\w\s]+?(?:leather|calfskin|wood|metal|glass|fabric|silk|cotton))',
            r'([\w\s]+?(?:material|texture|finish|surface))'
        ]

        for pattern in material_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if len(match.strip()) > 5:
                    materials.append(match.strip())

        return materials[:3]


class Tagger:
    """标签生成器"""

    def generate_tags(self, element: Dict, domain_id: str) -> List[str]:
        """生成标签"""
        tags = []

        # 1. 领域标签
        domain_tag_map = {
            'portrait': 'portrait',
            'product': 'product',
            'design': 'design',
            'art': 'art',
            'video': 'video',
            'interior': 'interior',
            'common': 'photography'
        }
        tags.append(domain_tag_map.get(domain_id, domain_id))

        # 2. 类别标签
        category_tag = element['category'].replace('_', '-')
        tags.append(category_tag)

        # 3. 从关键词提取
        keywords = element.get('keywords', [])
        for kw in keywords[:5]:
            tag = kw.lower().replace(' ', '-').replace('_', '-')
            if 2 < len(tag) < 30:
                tags.append(tag)

        # 4. 智能特征标签
        template = element['ai_prompt_template'].lower()

        # 材质
        if any(m in template for m in ['wood', 'wooden', 'walnut', 'oak']):
            tags.append('wood')
        if any(m in template for m in ['metal', 'brass', 'gold', 'steel']):
            tags.append('metal')
        if any(m in template for m in ['glass', 'translucent', 'transparent']):
            tags.append('glass')
        if any(m in template for m in ['leather', 'calfskin']):
            tags.append('leather')

        # 风格
        if any(s in template for s in ['modern', 'contemporary']):
            tags.append('modern')
        if any(s in template for s in ['vintage', 'retro', 'classic']):
            tags.append('vintage')
        if any(s in template for s in ['luxury', 'premium', 'high-end']):
            tags.append('luxury')

        # 去重
        tags = list(dict.fromkeys(tags))  # 保持顺序的去重
        return tags[:15]


class UniversalLearner:
    """通用学习器主类"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.db = ElementDB(db_path)
        self.classifier = DomainClassifier()
        self.extractor = ElementExtractor()
        self.tagger = Tagger()

        self.stats = {
            'total_prompts': 0,
            'total_extracted': 0,
            'total_added': 0,
            'total_skipped': 0,
            'by_domain': {}
        }

    def learn_from_prompt(self, prompt_data: Dict) -> Dict:
        """从单个Prompt学习"""
        prompt_id = prompt_data['prompt_id']
        original_prompt = prompt_data['original_prompt']
        theme = prompt_data.get('theme', '')

        print(f"\n{'='*80}")
        print(f"Learning from Prompt #{prompt_id}")
        print(f"Theme: {theme}")
        print(f"{'='*80}")

        # Step 1: 领域分类
        domain_info = self.classifier.classify(original_prompt, theme)
        primary = domain_info['primary']

        print(f"\n🎯 Domain: {primary} (confidence: {domain_info['confidence']:.0%})")
        if domain_info['secondary']:
            print(f"   Secondary: {', '.join(domain_info['secondary'])}")

        if not primary:
            print("⚠️  无法确定领域，跳过")
            return {'added': 0, 'skipped': 0}

        # Step 2: 元素提取
        elements = self.extractor.extract(prompt_data, domain_info)
        print(f"\n📦 Extracted {len(elements)} elements")

        if not elements:
            print("   No elements extracted")
            return {'added': 0, 'skipped': 0}

        # Step 3: 处理每个元素
        added = 0
        skipped = 0

        for element in elements:
            # 生成标签
            tags = self.tagger.generate_tags(element, primary)

            # 添加中文名（如果没有）
            if 'chinese_name' not in element:
                element['chinese_name'] = element['name'].replace('_', ' ').title()

            # 尝试添加到数据库
            success, element_id = self._add_to_db(
                element,
                primary,
                tags,
                prompt_id
            )

            if success:
                added += 1
                print(f"   ✅ {element_id}: {element.get('chinese_name', element['name'])}")
            else:
                skipped += 1

        # 更新统计
        self.stats['total_prompts'] += 1
        self.stats['total_extracted'] += len(elements)
        self.stats['total_added'] += added
        self.stats['total_skipped'] += skipped

        if primary not in self.stats['by_domain']:
            self.stats['by_domain'][primary] = {'added': 0, 'skipped': 0}
        self.stats['by_domain'][primary]['added'] += added
        self.stats['by_domain'][primary]['skipped'] += skipped

        print(f"\n✅ Summary: Added {added}, Skipped {skipped}")

        return {'added': added, 'skipped': skipped}

    def _add_to_db(self, element: Dict, domain_id: str, tags: List[str], prompt_id: int) -> Tuple[bool, Optional[str]]:
        """添加元素到数据库"""
        # 检查是否已存在
        exists = self._check_exists(element['name'], domain_id, element['category'])
        if exists:
            return False, None

        # 生成element_id
        element_id = self._generate_id(domain_id, element['category'])

        # 添加
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
            learned_from='universal_learner',
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
        """生成element_id"""
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

    def batch_learn(self, prompts_file: str = "extracted_results/extracted_modules.json"):
        """批量学习所有Prompts"""
        print("=" * 80)
        print("Universal Learner - Batch Learning Mode")
        print("=" * 80)

        with open(prompts_file, 'r', encoding='utf-8') as f:
            prompts = json.load(f)

        print(f"\nTotal Prompts: {len(prompts)}\n")

        for prompt_data in prompts:
            try:
                self.learn_from_prompt(prompt_data)
            except Exception as e:
                print(f"❌ Error learning Prompt #{prompt_data['prompt_id']}: {e}")
                import traceback
                traceback.print_exc()

        # 最终统计
        self._print_final_stats()

        # 导出JSON
        print("\n\nExporting to JSON...")
        self.db.export_to_json('extracted_results/universal_elements_library.json')

    def _print_final_stats(self):
        """打印最终统计"""
        print("\n" + "=" * 80)
        print("📊 Final Learning Statistics")
        print("=" * 80)

        print(f"\nTotal Prompts Processed: {self.stats['total_prompts']}")
        print(f"Total Elements Extracted: {self.stats['total_extracted']}")
        print(f"Total Elements Added: {self.stats['total_added']}")
        print(f"Total Elements Skipped: {self.stats['total_skipped']}")

        print(f"\n📦 By Domain:")
        for domain, counts in self.stats['by_domain'].items():
            print(f"   {domain:15s}: +{counts['added']:3d} elements (skipped {counts['skipped']})")

        # 数据库总统计
        db_stats = self.db.get_stats()
        print(f"\n📊 Database Status:")
        print(f"   Total Elements: {db_stats['total_elements']}")
        print(f"   Total Tags: {db_stats['total_tags']}")

        print(f"\n   By Domain:")
        for domain in db_stats['domains']:
            if domain['total_elements'] > 0:
                print(f"   - {domain['name']:15s}: {domain['total_elements']:3d} elements")

    def close(self):
        """关闭数据库"""
        self.db.close()


def main():
    """主函数"""
    learner = UniversalLearner()

    try:
        learner.batch_learn()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        learner.close()


if __name__ == "__main__":
    main()
