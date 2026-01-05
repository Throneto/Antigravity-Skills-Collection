#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词生成器 - 基于元素库组合生成
"""

import sqlite3
import json
from typing import List, Dict

class PromptGenerator:
    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def search_elements(self, tags: List[str], domain: str = None, limit: int = 20) -> List[Dict]:
        """搜索相关元素"""
        # 构建查询
        query = """
            SELECT DISTINCT e.element_id, e.name, e.chinese_name, e.ai_prompt_template,
                   e.domain_id, e.category_id, e.reusability_score
            FROM elements e
            JOIN element_tags et ON e.element_id = et.element_id
            JOIN tags t ON et.tag_id = t.tag_id
            WHERE t.tag_name IN ({})
        """.format(','.join(['?'] * len(tags)))

        params = tags.copy()

        if domain:
            query += " AND e.domain_id = ?"
            params.append(domain)

        query += " ORDER BY e.reusability_score DESC LIMIT ?"
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

    def get_elements_by_category(self, category: str, domain: str = None, limit: int = 5) -> List[Dict]:
        """按类别获取元素"""
        query = """
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   domain_id, category_id, reusability_score
            FROM elements
            WHERE category_id LIKE ?
        """

        params = [f"%{category}%"]

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

    def generate_prompt(self, theme: str, requirements: Dict) -> Dict:
        """生成完整提示词"""
        print(f"\n{'='*80}")
        print(f"🎨 主题: {theme}")
        print(f"{'='*80}\n")

        # 根据需求搜索元素
        all_elements = {}

        for category, config in requirements.items():
            print(f"🔍 搜索 {category}...")

            if 'tags' in config:
                elements = self.search_elements(
                    config['tags'],
                    config.get('domain'),
                    config.get('limit', 5)
                )
            else:
                elements = self.get_elements_by_category(
                    config['category'],
                    config.get('domain'),
                    config.get('limit', 5)
                )

            all_elements[category] = elements
            print(f"   ✓ 找到 {len(elements)} 个相关元素")

        # 组合生成提示词
        print(f"\n{'─'*80}")
        print(f"📝 生成提示词:")
        print(f"{'─'*80}\n")

        prompt_parts = []
        element_details = []

        for category, elements in all_elements.items():
            if not elements:
                continue

            # 选择最佳元素（可重用性最高的）
            best_elements = sorted(elements, key=lambda x: x['reusability'], reverse=True)[:3]

            category_prompts = []
            for elem in best_elements:
                category_prompts.append(elem['template'])
                element_details.append({
                    'category': category,
                    'name': elem['chinese_name'] or elem['name'],
                    'template': elem['template'],
                    'reusability': elem['reusability'],
                    'domain': elem['domain']
                })

            if category_prompts:
                prompt_parts.append(', '.join(category_prompts))

        # 组合最终提示词
        final_prompt = ', '.join(prompt_parts)

        return {
            'theme': theme,
            'prompt': final_prompt,
            'elements_used': element_details,
            'total_elements': len(element_details)
        }

    def close(self):
        self.conn.close()


def main():
    generator = PromptGenerator()

    # 主题1: 赛博朋克风格的动漫少女
    result1 = generator.generate_prompt(
        "赛博朋克风格的动漫少女",
        {
            'character_style': {
                'tags': ['portrait', 'anime', 'character', 'cyberpunk'],
                'domain': 'portrait',
                'limit': 3
            },
            'lighting': {
                'tags': ['lighting-techniques', 'neon', 'dramatic'],
                'limit': 3
            },
            'camera': {
                'tags': ['photography-techniques', 'portrait'],
                'limit': 2
            },
            'details': {
                'tags': ['anime', 'detailed', 'art'],
                'domain': 'art',
                'limit': 2
            }
        }
    )

    print(f"生成的提示词:\n{result1['prompt']}\n")
    print(f"使用元素:")
    for idx, elem in enumerate(result1['elements_used'], 1):
        print(f"  {idx}. [{elem['category']}] {elem['name']} (可重用性: {elem['reusability']}/10)")

    print(f"\n总计使用 {result1['total_elements']} 个学习到的元素")

    # 主题2: 高端化妆品产品摄影
    result2 = generator.generate_prompt(
        "高端化妆品产品摄影",
        {
            'product_style': {
                'tags': ['product', 'luxury', 'cosmetics'],
                'domain': 'product',
                'limit': 3
            },
            'lighting': {
                'tags': ['lighting-techniques', 'studio', 'soft'],
                'limit': 3
            },
            'composition': {
                'tags': ['photography-techniques', 'product'],
                'limit': 2
            },
            'background': {
                'tags': ['product', 'elegant', 'minimal'],
                'limit': 2
            }
        }
    )

    print(f"\n生成的提示词:\n{result2['prompt']}\n")
    print(f"使用元素:")
    for idx, elem in enumerate(result2['elements_used'], 1):
        print(f"  {idx}. [{elem['category']}] {elem['name']} (可重用性: {elem['reusability']}/10)")

    print(f"\n总计使用 {result2['total_elements']} 个学习到的元素")

    # 主题3: 电影级人物特写镜头
    result3 = generator.generate_prompt(
        "电影级人物特写镜头",
        {
            'cinematography': {
                'tags': ['video', 'cinematic', 'film'],
                'limit': 3
            },
            'portrait_style': {
                'tags': ['portrait', 'closeup', 'dramatic'],
                'domain': 'portrait',
                'limit': 3
            },
            'lighting': {
                'tags': ['lighting-techniques', 'cinematic', 'dramatic'],
                'limit': 3
            },
            'camera': {
                'tags': ['photography-techniques', 'professional'],
                'limit': 2
            }
        }
    )

    print(f"\n生成的提示词:\n{result3['prompt']}\n")
    print(f"使用元素:")
    for idx, elem in enumerate(result3['elements_used'], 1):
        print(f"  {idx}. [{elem['category']}] {elem['name']} (可重用性: {elem['reusability']}/10)")

    print(f"\n总计使用 {result3['total_elements']} 个学习到的元素")

    # 主题4: 中国风水墨画插画
    result4 = generator.generate_prompt(
        "中国风水墨画插画",
        {
            'art_style': {
                'tags': ['art', 'chinese', 'ink', 'painting'],
                'domain': 'art',
                'limit': 4
            },
            'composition': {
                'tags': ['art', 'traditional', 'elegant'],
                'limit': 3
            },
            'details': {
                'tags': ['art', 'detailed', 'artistic'],
                'limit': 2
            }
        }
    )

    print(f"\n生成的提示词:\n{result4['prompt']}\n")
    print(f"使用元素:")
    for idx, elem in enumerate(result4['elements_used'], 1):
        print(f"  {idx}. [{elem['category']}] {elem['name']} (可重用性: {elem['reusability']}/10)")

    print(f"\n总计使用 {result4['total_elements']} 个学习到的元素")

    # 总结
    print(f"\n{'='*80}")
    print(f"📊 生成总结")
    print(f"{'='*80}")
    print(f"✅ 成功生成 4 个不同主题的完整提示词")
    print(f"✅ 使用元素总数: {sum([r['total_elements'] for r in [result1, result2, result3, result4]])} 个")
    print(f"✅ 所有元素均来自921个学习到的元素库")
    print(f"✅ 平均可重用性: {sum([sum([e['reusability'] for e in r['elements_used']]) / len(r['elements_used']) for r in [result1, result2, result3, result4]]) / 4:.1f}/10")
    print(f"{'='*80}")

    generator.close()

if __name__ == "__main__":
    main()
