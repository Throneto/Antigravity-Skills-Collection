#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Learner V2 - 真正的自动化提取器
深入解析modules中的所有数据，不遗漏任何有价值的元素
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from element_db import ElementDB


class DomainClassifier:
    """领域分类器（保持不变）"""

    def __init__(self):
        self.keywords = {
            'portrait': {
                'face': 3, 'woman': 3, 'man': 3, 'person': 3, '人物': 3,
                'eyes': 2, 'skin': 2, 'makeup': 2, 'hair': 2, '面部': 3,
                'beauty': 2, 'facial': 2, 'portrait': 3, 'cosplay': 2,
                '肖像': 3, '美女': 3, '人像': 3, '角色': 2, 'character': 2,
                'pose': 2, 'kpop': 2, 'k-pop': 2
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
                'lighting': 2, 'iso': 1, 'aperture': 1, '光照': 2,
                'angle': 2, 'perspective': 2, 'focus': 2
            },

            # 新增领域
            'utility': {
                # 格式转换
                '转': 3, '翻译': 3, '汉化': 3, '生成': 2, '制作': 2,
                '变成': 2, '创建': 2, 'convert': 3, 'generate': 2,
                # 图像增强
                '提高': 3, '修图': 3, '智能': 3, '消除': 3, '恢复': 3,
                '扩图': 3, '优化': 2, 'enhance': 3, 'remove': 2,
                '分辨率': 3, 'resolution': 3, '清晰': 2, '提取': 2,
                # 智能分析
                '解题': 3, '分析': 2, '评分': 3, '标注': 3, '检测': 2,
                # 虚拟应用
                '虚拟': 2, '试': 2, '预览': 2, '警示': 2, 'virtual': 2
            },
            'creative': {
                # 头像生成
                '头像': 3, 'Q版': 3, '盲盒': 3, '手办': 3, '公仔': 3,
                'avatar': 3, 'funko': 3, '娃娃': 2, '玩偶': 2,
                # 3D渲染
                '3D': 3, '3d': 3, '立体': 3, '水晶球': 3, '微型': 2,
                '乐高': 3, 'lego': 3, '等距': 2, 'isometric': 2,
                # 插画漫画
                '插画': 3, '漫画': 3, '卡通': 3, '表情包': 3, 'emoji': 2,
                'comic': 3, 'illustration': 2, '手绘': 2, '涂鸦': 2,
                '科普': 2, '风格': 2, '拼贴': 2, 'collage': 2,
                # 特殊效果
                '特效': 2, '滤镜': 2, '复古': 2, '胶片': 2, 'vintage': 2,
                '光影': 2, '打光': 2,
                # 梗图
                '梗': 3, '吐槽': 3, '伪造': 3, '截图': 2, 'meme': 3
            },
            'lifestyle': {
                # 日常拍摄
                '旅行': 2, '手账': 3, '自拍': 2, '穿搭': 3, 'OOTD': 3,
                '日记': 2, '合照': 2, 'selfie': 2,
                # 电商购物
                '电商': 3, '试穿': 3, '换装': 3, '商品': 2, '购物': 2,
                # 美食烹饪
                '食材': 3, '烹饪': 3, '餐饮': 2, '菜': 2, '料理': 2,
                # 家居空间
                '家具': 2, '软装': 3, '预览': 2, '房': 2, '装饰': 2
            },
            'scenario': {
                # 摄影拍摄
                '照片': 2, '拍摄': 2, '摄影': 2, '写真': 2, 'photo': 2,
                # 地点场景
                '东京': 2, '迪拜': 2, '海滩': 2, '沙漠': 2, '山': 1,
                '城市': 2, '街头': 2, '宫殿': 2, '卧室': 2, '房间': 2,
                # 动作姿势
                '站立': 2, '坐': 2, '跪': 2, '骑': 2, '跑': 2,
                '登山': 2, '游泳': 2, '漂流': 2,
                # 虚拟角色
                '马里奥': 3, '宇航员': 3, '外星人': 3, '哈利波特': 3,
                # 故事场景
                '场景': 2, '故事': 2, '叙事': 2, '氛围': 2
            },
            'misc': {
                # 杂项（低权重，兜底用）
                '其他': 1, '道具': 1, '服装': 1, '动物': 1,
                '图标': 1, '模板': 1, '证': 1, '许可证': 2,
                '标本': 2, '展示': 1, '包裹': 2, '快递': 2,
                '年龄': 2, '参考': 1, '贴合': 2, '猫': 1,
                '狗': 1, '宝宝': 1, '钞票': 2
            }
        }

    def classify(self, prompt_text: str, theme: str = "") -> Dict:
        text_lower = (prompt_text + " " + theme).lower()
        domain_scores = {domain: 0 for domain in self.keywords.keys()}

        for domain, kw_dict in self.keywords.items():
            for keyword, weight in kw_dict.items():
                if keyword in text_lower:
                    domain_scores[domain] += weight

        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)

        primary = None
        secondary = []

        # 降低阈值以便新领域也能被识别
        # 原有领域保持高标准(>5)，新领域降低标准(>3)
        top_domain = sorted_domains[0][0]
        top_score = sorted_domains[0][1]

        if top_score > 5:
            primary = top_domain
        elif top_score > 3 and top_domain in ['utility', 'creative', 'lifestyle', 'scenario', 'misc']:
            primary = top_domain
        elif top_score > 3:  # 其他情况，分数>3也可以
            primary = top_domain

        for domain, score in sorted_domains[1:]:
            if score > 3:
                secondary.append(domain)

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


class ElementExtractorV2:
    """V2版本 - 深入解析modules的所有数据"""

    def __init__(self):
        pass

    def extract(self, prompt_data: Dict, domain_info: Dict) -> List[Dict]:
        """从Prompt中提取元素（全自动）"""
        elements = []
        primary = domain_info['primary']
        modules = prompt_data.get('modules', {})

        print(f"\n🔍 深入解析modules...")

        # 1. 提取相机角度（所有领域通用）
        elements.extend(self._extract_camera_angles(modules))

        # 2. 提取技术参数（所有领域通用）
        elements.extend(self._extract_technical_params(modules))

        # 3. 提取构图技术（所有领域通用）
        elements.extend(self._extract_composition_techniques(modules))

        # 4. 根据主领域提取特定元素
        if primary == 'portrait':
            elements.extend(self._extract_portrait_specific(modules, prompt_data.get('original_prompt', '')))
        elif primary == 'product':
            elements.extend(self._extract_product_specific(modules, prompt_data.get('original_prompt', '')))
        elif primary == 'design':
            elements.extend(self._extract_design_specific(modules, prompt_data.get('original_prompt', '')))
        elif primary == 'art':
            elements.extend(self._extract_art_specific(modules, prompt_data.get('original_prompt', '')))
        elif primary == 'video':
            elements.extend(self._extract_video_specific(modules, prompt_data.get('original_prompt', '')))
        elif primary == 'common':
            # common作为主领域时，也提取portrait相关（因为可能是摄影技术为主）
            elements.extend(self._extract_portrait_specific(modules, prompt_data.get('original_prompt', '')))

        # 5. 提取光照技术数组（所有领域）
        elements.extend(self._extract_lighting_techniques_array(modules))

        # 6. 提取特殊效果数组（所有领域）
        elements.extend(self._extract_special_effects_array(modules))

        # 7. 提取材质纹理数组（所有领域）
        elements.extend(self._extract_material_textures_array(modules))

        # 8. 提取视觉风格（所有领域）
        elements.extend(self._extract_visual_styles(modules))

        print(f"   提取到 {len(elements)} 个潜在元素")
        return elements

    def _extract_camera_angles(self, modules: Dict) -> List[Dict]:
        """提取相机角度（关键改进！）"""
        elements = []

        # 检查modules中的camera_angles数组
        camera_angles = modules.get('camera_angles', [])
        if camera_angles and isinstance(camera_angles, list):
            print(f"   ✓ 发现camera_angles数组: {len(camera_angles)}个")
            for angle in camera_angles:
                if isinstance(angle, str) and len(angle) > 3:
                    elements.append({
                        'category': 'camera_angles',
                        'name': self._simplify_name(angle),
                        'ai_prompt_template': angle,
                        'keywords': self._extract_keywords(angle),
                        'reusability': 8.0
                    })

        # 也检查technical_parameters中的camera
        tech = modules.get('technical_parameters', {})
        if tech.get('camera'):
            camera_desc = tech['camera']
            if 'angle' not in camera_desc.lower():  # 避免重复
                elements.append({
                    'category': 'photography_techniques',
                    'name': self._simplify_name(camera_desc),
                    'ai_prompt_template': camera_desc,
                    'keywords': self._extract_keywords(camera_desc),
                    'reusability': 9.0
                })

        return elements

    def _extract_technical_params(self, modules: Dict) -> List[Dict]:
        """提取技术参数"""
        elements = []
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

        # 光照
        lighting = tech.get('lighting', '')
        if lighting:
            elements.append({
                'category': 'lighting_techniques',
                'name': self._simplify_name(lighting),
                'ai_prompt_template': lighting,
                'keywords': self._extract_keywords(lighting),
                'reusability': 8.5
            })

        # 对焦（关键改进！）
        focus = tech.get('focus', '')
        if focus:
            print(f"   ✓ 发现focus参数: {focus[:50]}...")
            elements.append({
                'category': 'photography_techniques',
                'name': self._simplify_name(focus),
                'ai_prompt_template': focus,
                'keywords': self._extract_keywords(focus),
                'reusability': 9.0
            })

        # 光圈
        aperture = tech.get('aperture', '')
        if aperture:
            elements.append({
                'category': 'photography_techniques',
                'name': self._simplify_name(aperture),
                'ai_prompt_template': aperture,
                'keywords': self._extract_keywords(aperture),
                'reusability': 8.5
            })

        return elements

    def _extract_composition_techniques(self, modules: Dict) -> List[Dict]:
        """提取构图技术（关键改进！）"""
        elements = []
        comp = modules.get('composition', {})

        # 透视技术
        perspective = comp.get('perspective_technique', '')
        if perspective:
            print(f"   ✓ 发现perspective_technique: {perspective}")
            elements.append({
                'category': 'photography_techniques',
                'name': self._simplify_name(perspective),
                'ai_prompt_template': perspective,
                'keywords': self._extract_keywords(perspective),
                'reusability': 8.5
            })

        # 焦点元素
        focal_element = comp.get('focal_element', '')
        if focal_element:
            elements.append({
                'category': 'photography_techniques',
                'name': self._simplify_name(focal_element),
                'ai_prompt_template': focal_element,
                'keywords': self._extract_keywords(focal_element),
                'reusability': 7.5
            })

        # 景深
        dof = comp.get('depth_of_field', '')
        if dof:
            elements.append({
                'category': 'photography_techniques',
                'name': self._simplify_name(dof),
                'ai_prompt_template': dof,
                'keywords': self._extract_keywords(dof),
                'reusability': 8.5
            })

        return elements

    def _extract_portrait_specific(self, modules: Dict, original: str) -> List[Dict]:
        """提取人像特定元素（关键改进！）"""
        elements = []

        # 1. 姿势数组（关键改进！）
        poses = modules.get('character_poses', [])
        if poses and isinstance(poses, list):
            print(f"   ✓ 发现character_poses数组: {len(poses)}个")
            for pose in poses:
                if isinstance(pose, str) and len(pose) > 3:
                    elements.append({
                        'category': 'poses',
                        'name': self._simplify_name(pose),
                        'ai_prompt_template': pose,
                        'keywords': self._extract_keywords(pose),
                        'reusability': 7.5
                    })

        # 2. 摄影风格/美学（关键改进！）
        visual = modules.get('visual_style', {})

        # aesthetic字段
        aesthetic = visual.get('aesthetic', '')
        if aesthetic:
            print(f"   ✓ 发现aesthetic: {aesthetic}")
            elements.append({
                'category': 'photography_styles',
                'name': self._simplify_name(aesthetic),
                'ai_prompt_template': aesthetic,
                'keywords': self._extract_keywords(aesthetic),
                'reusability': 7.5
            })

        # art_style字段（如果是摄影风格）
        art_style = visual.get('art_style', '')
        if 'photography' in art_style.lower() or 'photo' in art_style.lower():
            elements.append({
                'category': 'photography_styles',
                'name': self._simplify_name(art_style),
                'ai_prompt_template': art_style,
                'keywords': self._extract_keywords(art_style),
                'reusability': 7.5
            })

        return elements

    def _extract_product_specific(self, modules: Dict, original: str) -> List[Dict]:
        """提取产品特定元素"""
        elements = []

        # 产品类型
        subject = modules.get('subject_variables', {})
        main_subject = subject.get('main', '')
        if main_subject:
            elements.append({
                'category': 'product_types',
                'name': self._simplify_name(main_subject),
                'ai_prompt_template': main_subject[:100],
                'keywords': self._extract_keywords(main_subject),
                'reusability': 6.5
            })

        # 材质
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

    def _extract_design_specific(self, modules: Dict, original: str) -> List[Dict]:
        """提取设计特定元素"""
        elements = []

        # 布局
        comp = modules.get('composition', {})
        layout = comp.get('layout', '')
        if layout:
            elements.append({
                'category': 'layout_systems',
                'name': self._simplify_name(layout),
                'ai_prompt_template': layout,
                'keywords': self._extract_keywords(layout),
                'reusability': 8.5
            })

        # 玻璃态效果检测
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

        return elements

    def _extract_art_specific(self, modules: Dict, original: str) -> List[Dict]:
        """提取艺术特定元素"""
        elements = []

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

        return elements

    def _extract_video_specific(self, modules: Dict, original: str) -> List[Dict]:
        """提取视频特定元素"""
        elements = []

        subject = modules.get('subject_variables', {})
        scene = subject.get('main', '')
        if scene:
            elements.append({
                'category': 'scene_types',
                'name': self._simplify_name(scene),
                'ai_prompt_template': scene[:100],
                'keywords': self._extract_keywords(scene),
                'reusability': 6.5
            })

        return elements

    def _extract_lighting_techniques_array(self, modules: Dict) -> List[Dict]:
        """提取光照技术数组（V2.1新增）"""
        elements = []

        # 检查modules中的lighting_techniques数组
        lighting_array = modules.get('lighting_techniques', [])
        if lighting_array and isinstance(lighting_array, list):
            print(f"   ✓ 发现lighting_techniques数组: {len(lighting_array)}个")
            for lighting in lighting_array:
                if isinstance(lighting, str) and len(lighting) > 5:
                    elements.append({
                        'category': 'lighting_techniques',
                        'name': self._simplify_name(lighting),
                        'ai_prompt_template': lighting,
                        'keywords': self._extract_keywords(lighting),
                        'reusability': 8.5
                    })

        return elements

    def _extract_special_effects_array(self, modules: Dict) -> List[Dict]:
        """提取特殊效果数组（V2.1新增）"""
        elements = []

        # 检查modules中的special_effects数组
        effects_array = modules.get('special_effects', [])
        if effects_array and isinstance(effects_array, list):
            print(f"   ✓ 发现special_effects数组: {len(effects_array)}个")
            for effect in effects_array:
                if isinstance(effect, str) and len(effect) > 5:
                    elements.append({
                        'category': 'visual_effects',
                        'name': self._simplify_name(effect),
                        'ai_prompt_template': effect,
                        'keywords': self._extract_keywords(effect),
                        'reusability': 8.0
                    })

        return elements

    def _extract_material_textures_array(self, modules: Dict) -> List[Dict]:
        """提取材质纹理数组（V2.1新增）"""
        elements = []

        # 检查modules中的material_textures数组
        materials_array = modules.get('material_textures', [])
        if materials_array and isinstance(materials_array, list):
            print(f"   ✓ 发现material_textures数组: {len(materials_array)}个")
            for material in materials_array:
                if isinstance(material, str) and len(material) > 3:
                    elements.append({
                        'category': 'material_textures',
                        'name': self._simplify_name(material),
                        'ai_prompt_template': material,
                        'keywords': self._extract_keywords(material),
                        'reusability': 8.0
                    })

        return elements

    def _extract_visual_styles(self, modules: Dict) -> List[Dict]:
        """提取视觉风格"""
        elements = []
        visual = modules.get('visual_style', {})

        # era（时代风格）
        era = visual.get('era', '')
        if era and len(era) > 5:
            elements.append({
                'category': 'visual_styles',
                'name': self._simplify_name(era),
                'ai_prompt_template': era,
                'keywords': self._extract_keywords(era),
                'reusability': 7.0
            })

        return elements

    # 辅助方法（保持不变）
    def _simplify_name(self, text: str) -> str:
        name = re.sub(r'[^\w\s-]', '', text.lower())
        name = re.sub(r'[-\s]+', '_', name)
        name = '_'.join(name.split('_')[:6])
        return name[:50] if name else 'unnamed'

    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[\w]+\b', text.lower())
        stopwords = {'a', 'an', 'the', 'with', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        return keywords[:10]

    def _find_materials(self, text: str) -> List[str]:
        materials = []
        material_patterns = [
            r'([\w\s]+?(?:leather|calfskin|wood|metal|glass|fabric|silk|cotton))',
        ]
        for pattern in material_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if len(match.strip()) > 5:
                    materials.append(match.strip())
        return materials[:3]


class Tagger:
    """标签生成器（保持不变）"""

    def generate_tags(self, element: Dict, domain_id: str) -> List[str]:
        tags = []

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

        category_tag = element['category'].replace('_', '-')
        tags.append(category_tag)

        keywords = element.get('keywords', [])
        for kw in keywords[:5]:
            tag = kw.lower().replace(' ', '-').replace('_', '-')
            if 2 < len(tag) < 30:
                tags.append(tag)

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

        tags = list(dict.fromkeys(tags))
        return tags[:15]


class UniversalLearnerV2:
    """V2版本 - 真正的自动化"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.db = ElementDB(db_path)
        self.classifier = DomainClassifier()
        self.extractor = ElementExtractorV2()  # 使用V2提取器
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

        # Step 2: 元素提取（V2深度提取）
        elements = self.extractor.extract(prompt_data, domain_info)
        print(f"\n📦 Extracted {len(elements)} elements")

        # Step 3: 处理每个元素
        added = 0
        skipped = 0

        if not elements:
            print("   No elements extracted")
            # 即使没有提取到元素，也要保存学习记录
            self._save_learning_record(prompt_id, original_prompt, theme, domain_info, elements, 0)
            return {'added': 0, 'skipped': 0}

        for element in elements:
            tags = self.tagger.generate_tags(element, primary)

            if 'chinese_name' not in element:
                element['chinese_name'] = element['name'].replace('_', ' ').title()

            success, element_id = self._add_to_db(element, primary, tags, prompt_id)

            if success:
                added += 1
                print(f"   ✅ {element_id}: {element.get('chinese_name', element['name'])}")
            else:
                skipped += 1

        self.stats['total_prompts'] += 1
        self.stats['total_extracted'] += len(elements)
        self.stats['total_added'] += added
        self.stats['total_skipped'] += skipped

        if primary not in self.stats['by_domain']:
            self.stats['by_domain'][primary] = {'added': 0, 'skipped': 0}
        self.stats['by_domain'][primary]['added'] += added
        self.stats['by_domain'][primary]['skipped'] += skipped

        # 保存学习记录
        self._save_learning_record(prompt_id, original_prompt, theme, domain_info, elements, added)

        print(f"\n✅ Summary: Added {added}, Skipped {skipped}")

        return {'added': added, 'skipped': skipped}

    def _add_to_db(self, element: Dict, domain_id: str, tags: List[str], prompt_id: int) -> Tuple[bool, Optional[str]]:
        """添加元素到数据库"""
        exists = self._check_exists(element['name'], domain_id, element['category'])
        if exists:
            return False, None

        element_id = self._generate_id(domain_id, element['category'])

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
            learned_from='universal_learner_v2',
            metadata={}
        )

        return success, element_id if success else None

    def _check_exists(self, name: str, domain_id: str, category_id: str) -> bool:
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT element_id FROM elements
            WHERE domain_id = ? AND category_id = ? AND name = ?
        """, (domain_id, category_id, name))
        return cursor.fetchone() is not None

    def _generate_id(self, domain_id: str, category_id: str) -> str:
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
        """
        保存学习记录到source_prompts表

        Args:
            prompt_id: Prompt ID
            original_prompt: 原始提示词文本
            theme: 主题
            domain_info: 领域分类信息
            elements: 提取的元素列表
            added_count: 成功添加的元素数量
        """
        try:
            # 计算质量评分（基于提取的元素数量）
            quality_score = min(10.0, 5.0 + len(elements) * 0.5)

            # 判断复杂度
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
                extracted_elements_count=added_count  # 只统计成功添加的元素
            )
            print(f"   💾 学习记录已保存 (ID: {prompt_id}, 质量: {quality_score:.1f}/10, 复杂度: {complexity})")
        except Exception as e:
            print(f"   ⚠️  保存学习记录失败: {e}")

    def close(self):
        """关闭数据库"""
        self.db.close()


# 测试用
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 universal_learner_v2.py <prompt_json_file>")
        sys.exit(1)

    learner = UniversalLearnerV2()

    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)

        result = learner.learn_from_prompt(prompt_data)

        print(f"\n✅ Learning Complete!")
        print(f"   Added: {result['added']} elements")
        print(f"   Skipped: {result['skipped']} elements")

        stats = learner.db.get_stats()
        print(f"\n📊 Database Status:")
        print(f"   Total Elements: {stats['total_elements']}")

        learner.db.export_to_json('extracted_results/universal_elements_library.json')

    finally:
        learner.close()
