#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词生成器 V2 - 按类别精确选择元素
"""

import sqlite3
from typing import List, Dict

class PromptGeneratorV2:
    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_elements_by_category(self, domain: str, category: str, limit: int = 3) -> List[Dict]:
        """按领域和类别获取元素"""
        query = """
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   domain_id, category_id, reusability_score
            FROM elements
            WHERE domain_id = ?
              AND category_id = ?
            ORDER BY reusability_score DESC
            LIMIT ?
        """

        self.cursor.execute(query, (domain, category, limit))

        elements = []
        for row in self.cursor.fetchall():
            # 如果template为空，用chinese_name或name作为fallback
            template = row[3]
            if not template or len(template) < 3:
                template = row[2] if row[2] else row[1]  # chinese_name优先，否则用name

            elements.append({
                'element_id': row[0],
                'name': row[1],
                'chinese_name': row[2],
                'template': template,
                'domain': row[4],
                'category': row[5],
                'reusability': row[6]
            })

        return elements

    def search_by_keywords(self, keywords: List[str], domain: str = None, limit: int = 5) -> List[Dict]:
        """按关键词搜索元素"""
        keyword_conditions = " OR ".join([f"ai_prompt_template LIKE ?" for _ in keywords])

        query = f"""
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   domain_id, category_id, reusability_score
            FROM elements
            WHERE ({keyword_conditions})
              AND ai_prompt_template != ''
              AND LENGTH(ai_prompt_template) > 5
        """

        params = [f"%{kw}%" for kw in keywords]

        if domain:
            query += " AND domain_id = ?"
            params.append(domain)

        query += " ORDER BY reusability_score DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)

        elements = []
        for row in self.cursor.fetchall():
            elements.append({
                'element_id': row[0],
                'name': row[1],
                'chinese_name': row[2],
                'template': row[3],
                'domain': row[4],
                'category': row[5],
                'reusability': row[6]
            })

        return elements

    def generate_prompt(self, theme: str, element_config: Dict) -> Dict:
        """
        生成提示词

        element_config格式:
        {
            'category_name': {
                'domain': 'portrait',
                'category': 'poses',
                'limit': 2
            },
            或
            'category_name': {
                'keywords': ['cyberpunk', 'neon'],
                'domain': 'art',
                'limit': 3
            }
        }
        """
        print(f"\n{'='*80}")
        print(f"🎨 主题: {theme}")
        print(f"{'='*80}\n")

        all_elements = {}

        for category_name, config in element_config.items():
            print(f"🔍 搜索 {category_name}...")

            if 'keywords' in config:
                # 关键词搜索
                elements = self.search_by_keywords(
                    config['keywords'],
                    config.get('domain'),
                    config.get('limit', 3)
                )
            else:
                # 类别搜索
                elements = self.get_elements_by_category(
                    config['domain'],
                    config['category'],
                    config.get('limit', 3)
                )

            all_elements[category_name] = elements
            print(f"   ✓ 找到 {len(elements)} 个元素")

        # 组合提示词
        print(f"\n{'─'*80}")
        print(f"📝 生成的提示词:")
        print(f"{'─'*80}\n")

        prompt_parts = []
        element_details = []

        for category_name, elements in all_elements.items():
            if not elements:
                continue

            for elem in elements:
                if elem['template']:
                    prompt_parts.append(elem['template'])
                    element_details.append({
                        'category': category_name,
                        'name': elem['chinese_name'] or elem['name'],
                        'template': elem['template'],
                        'reusability': elem['reusability'],
                        'domain': elem['domain']
                    })

        final_prompt = ', '.join(prompt_parts)

        print(final_prompt)
        print(f"\n{'─'*80}")
        print(f"使用元素 ({len(element_details)}个):")
        for idx, elem in enumerate(element_details, 1):
            print(f"  {idx}. [{elem['category']}] {elem['name']} ({elem['reusability']}/10)")

        return {
            'theme': theme,
            'prompt': final_prompt,
            'elements_used': element_details,
            'total_elements': len(element_details)
        }

    def close(self):
        self.conn.close()


def main():
    gen = PromptGeneratorV2()

    # 主题1: 赛博朋克风格的动漫少女
    print("\n" + "="*80)
    print("测试1: 赛博朋克风格的动漫少女")
    print("="*80)

    result1 = gen.generate_prompt(
        "赛博朋克风格的动漫少女",
        {
            # === 基础人物属性（必须） ===
            # 性别
            'gender': {
                'domain': 'portrait',
                'category': 'gender',
                'limit': 1
            },
            # 年龄
            'age': {
                'domain': 'portrait',
                'category': 'age_range',
                'limit': 1
            },
            # 国籍/区域
            'ethnicity': {
                'domain': 'portrait',
                'category': 'ethnicity',
                'limit': 1
            },
            # 肤色
            'skin_tone': {
                'domain': 'portrait',
                'category': 'skin_tones',
                'limit': 1
            },
            # 皮肤质感
            'skin_texture': {
                'domain': 'portrait',
                'category': 'skin_textures',
                'limit': 1
            },
            # 脸型
            'face_shape': {
                'domain': 'portrait',
                'category': 'face_shapes',
                'limit': 1
            },
            # 眼型
            'eyes': {
                'domain': 'portrait',
                'category': 'eye_types',
                'limit': 1
            },
            # 发型
            'hair': {
                'domain': 'portrait',
                'category': 'hair_styles',
                'limit': 1
            },
            # 妆容
            'makeup': {
                'domain': 'portrait',
                'category': 'makeup_styles',
                'limit': 1
            },
            # === 人物状态 ===
            # 表情
            'expression': {
                'domain': 'portrait',
                'category': 'expressions',
                'limit': 1
            },
            # 姿势
            'pose': {
                'domain': 'portrait',
                'category': 'poses',
                'limit': 1
            },
            # 服装
            'clothing': {
                'domain': 'portrait',
                'category': 'clothing_styles',
                'limit': 1
            },
            # === 风格和环境 ===
            # 灯光（赛博朋克风格）
            'lighting': {
                'keywords': ['dramatic', 'glow', 'rim light'],
                'limit': 2
            },
            # 相机设置
            'camera': {
                'domain': 'portrait',
                'category': 'technical_effects',
                'limit': 1
            }
        }
    )

    # 主题2: 高端化妆品产品摄影
    print("\n" + "="*80)
    print("测试2: 高端化妆品产品摄影")
    print("="*80)

    result2 = gen.generate_prompt(
        "高端化妆品产品摄影",
        {
            # 产品摄影技术
            'product_tech': {
                'keywords': ['product', 'macro', 'commercial'],
                'domain': 'product',
                'limit': 2
            },
            # 柔光照明
            'lighting': {
                'keywords': ['soft', 'diffused', 'studio', 'softbox'],
                'limit': 3
            },
            # 技术参数
            'technical': {
                'domain': 'product',
                'category': 'technical_effects',
                'limit': 1
            }
        }
    )

    # 主题3: 电影级人物特写镜头
    print("\n" + "="*80)
    print("测试3: 电影级人物特写镜头")
    print("="*80)

    result3 = gen.generate_prompt(
        "电影级人物特写镜头",
        {
            # === 基础人物属性 ===
            'gender': {
                'domain': 'portrait',
                'category': 'gender',
                'limit': 1
            },
            'age': {
                'domain': 'portrait',
                'category': 'age_range',
                'limit': 1
            },
            'ethnicity': {
                'domain': 'portrait',
                'category': 'ethnicity',
                'limit': 1
            },
            'skin_tone': {
                'domain': 'portrait',
                'category': 'skin_tones',
                'limit': 1
            },
            'skin_texture': {
                'domain': 'portrait',
                'category': 'skin_textures',
                'limit': 1
            },
            'face_shape': {
                'domain': 'portrait',
                'category': 'face_shapes',
                'limit': 1
            },
            'eyes': {
                'domain': 'portrait',
                'category': 'eye_types',
                'limit': 1
            },
            'makeup': {
                'domain': 'portrait',
                'category': 'makeup_styles',
                'limit': 1
            },
            # === 人物状态 ===
            'expression': {
                'domain': 'portrait',
                'category': 'expressions',
                'limit': 1
            },
            'pose': {
                'domain': 'portrait',
                'category': 'poses',
                'limit': 1
            },
            # === 风格 ===
            # 电影级灯光
            'lighting': {
                'keywords': ['cinematic', 'dramatic', 'warm'],
                'limit': 2
            },
            # 相机技术
            'camera': {
                'keywords': ['8K', 'film camera', 'cinema'],
                'limit': 2
            }
        }
    )

    # 主题4: 中国风水墨画插画
    print("\n" + "="*80)
    print("测试4: 中国风水墨画插画")
    print("="*80)

    result4 = gen.generate_prompt(
        "中国风水墨画插画",
        {
            # 水墨画风格
            'art_style': {
                'keywords': ['ink', 'watercolor', 'painting', 'traditional', 'chinese'],
                'domain': 'art',
                'limit': 5
            },
            # 艺术技法
            'technique': {
                'keywords': ['brush', 'stroke', 'artistic', 'illustration'],
                'domain': 'art',
                'limit': 3
            }
        }
    )

    print(f"\n{'='*80}")
    print(f"📊 生成总结")
    print(f"{'='*80}")
    print(f"✅ 成功生成 4 个主题的提示词")
    print(f"✅ 主题1使用元素: {result1['total_elements']} 个")
    print(f"✅ 主题2使用元素: {result2['total_elements']} 个")
    print(f"✅ 主题3使用元素: {result3['total_elements']} 个")
    print(f"✅ 主题4使用元素: {result4['total_elements']} 个")
    print(f"{'='*80}")

    gen.close()


if __name__ == "__main__":
    main()
