#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可配置提示词生成引擎
支持从模板配置动态生成提示词
"""

import sqlite3
import json
from typing import List, Dict, Optional
from pathlib import Path


class PromptGeneratorEngine:
    def __init__(self, db_path: str = "extracted_results/elements.db",
                 template_path: str = "templates.json"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # 加载模板配置
        with open(template_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.templates = self.config['templates']
        self.style_keywords = self.config['style_keywords']

    def get_template(self, template_name: str) -> Optional[Dict]:
        """获取模板配置"""
        return self.templates.get(template_name)

    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        return list(self.templates.keys())

    def get_elements_by_category(self, domain: str, category: str, limit: int = 3) -> List[Dict]:
        """按领域和类别获取元素"""
        query = """
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   domain_id, category_id, reusability_score, keywords
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
                template = row[2] if row[2] else row[1]

            # 解析keywords JSON
            keywords = None
            if row[7]:
                try:
                    keywords = json.loads(row[7])
                except:
                    keywords = None

            elements.append({
                'element_id': row[0],
                'name': row[1],
                'chinese_name': row[2],
                'template': template,
                'domain': row[4],
                'category': row[5],
                'reusability': row[6],
                'keywords': keywords
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

    def get_element_text(self, element: Dict, mode: str = 'auto', keywords_limit: int = 3) -> str:
        """
        智能选择使用单字符串还是keywords

        参数:
            element: 元素字典（包含template和keywords）
            mode: 'simple' - 只用template
                  'detailed' - 优先用keywords
                  'auto' - 自动判断
            keywords_limit: 使用keywords时取前N个

        返回:
            提示词文本
        """
        template = element.get('template', '')
        keywords = element.get('keywords')

        # 简单模式：只用template
        if mode == 'simple':
            return template

        # 详细模式：优先用keywords
        if mode == 'detailed':
            if keywords and len(keywords) > 0:
                return ", ".join(keywords[:keywords_limit])
            else:
                return template

        # 自动模式：根据keywords数量决定
        if mode == 'auto':
            # 如果有丰富的keywords（>2个），使用前几个
            if keywords and len(keywords) > 2:
                return ", ".join(keywords[:keywords_limit])
            # 如果keywords少或没有，直接用template
            else:
                return template

        return template

    def generate_from_template(self,
                               template_name: str,
                               theme: str,
                               style_keywords: List[str] = None,
                               attribute_overrides: Dict = None,
                               mode: str = 'auto',
                               keywords_limit: int = 3,
                               verbose: bool = True) -> Dict:
        """
        从模板生成提示词

        参数:
            template_name: 模板名称 (如 'portrait_full', 'product_photography')
            theme: 主题描述
            style_keywords: 额外的风格关键词列表
            attribute_overrides: 覆盖特定属性的配置
            mode: 'simple' - 只用template, 'detailed' - 优先keywords, 'auto' - 自动
            keywords_limit: keywords模式下取前N个
            verbose: 是否显示详细信息
        """
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"模板 '{template_name}' 不存在")

        if verbose:
            print(f"\n{'='*80}")
            print(f"🎨 主题: {theme}")
            print(f"📋 模板: {template['name']} ({template['description']})")
            print(f"{'='*80}\n")

        all_elements = {}

        # 处理模板定义的属性
        for attr_name, attr_config in template['attributes'].items():
            # 应用覆盖配置
            if attribute_overrides and attr_name in attribute_overrides:
                attr_config = {**attr_config, **attribute_overrides[attr_name]}

            if verbose:
                print(f"🔍 搜索 {attr_name}...")

            # 判断是关键词搜索还是类别搜索
            if 'keywords' in attr_config:
                elements = self.search_by_keywords(
                    attr_config['keywords'],
                    attr_config.get('domain'),
                    attr_config.get('limit', 3)
                )
            else:
                elements = self.get_elements_by_category(
                    attr_config['domain'],
                    attr_config['category'],
                    attr_config.get('limit', 3)
                )

            all_elements[attr_name] = elements

            if verbose:
                print(f"   ✓ 找到 {len(elements)} 个元素")

        # 添加额外的风格关键词
        if style_keywords:
            if verbose:
                print(f"🎨 搜索风格关键词: {', '.join(style_keywords)}...")

            # 收集已定义的类别，避免重复
            excluded_categories = set()
            for attr_config in template['attributes'].values():
                if 'category' in attr_config:
                    excluded_categories.add(attr_config['category'])

            if verbose and excluded_categories:
                print(f"   ⚠️  排除已定义的类别: {', '.join(excluded_categories)}")

            # 搜索风格元素，排除人物属性类别
            style_elements = self.search_by_keywords(style_keywords, limit=10)

            # 过滤掉已定义类别的元素
            filtered_style_elements = [
                elem for elem in style_elements
                if elem['category'] not in excluded_categories
            ]

            all_elements['_style_keywords'] = filtered_style_elements

            if verbose:
                print(f"   ✓ 找到 {len(style_elements)} 个元素，过滤后 {len(filtered_style_elements)} 个风格元素")

        # 组合提示词
        if verbose:
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
                    # 使用智能选择方法
                    element_text = self.get_element_text(elem, mode=mode, keywords_limit=keywords_limit)
                    prompt_parts.append(element_text)
                    element_details.append({
                        'category': category_name,
                        'name': elem['chinese_name'] or elem['name'],
                        'template': elem['template'],
                        'keywords': elem.get('keywords'),
                        'used_text': element_text,  # 记录实际使用的文本
                        'reusability': elem['reusability'],
                        'domain': elem['domain']
                    })

        final_prompt = ', '.join(prompt_parts)

        if verbose:
            print(final_prompt)
            print(f"\n{'─'*80}")
            print(f"使用元素 ({len(element_details)}个):")
            for idx, elem in enumerate(element_details, 1):
                print(f"  {idx}. [{elem['category']}] {elem['name']} ({elem['reusability']}/10)")

        return {
            'theme': theme,
            'template': template_name,
            'prompt': final_prompt,
            'elements_used': element_details,
            'total_elements': len(element_details)
        }

    def generate_with_auto_template(self,
                                    theme: str,
                                    theme_type: str = "portrait",
                                    style: str = None,
                                    **kwargs) -> Dict:
        """
        智能选择模板并生成

        参数:
            theme: 主题描述
            theme_type: 主题类型 (portrait/product/art/cinematic)
            style: 风格名称 (cyberpunk/anime/realistic等)
            **kwargs: 传递给 generate_from_template 的其他参数
        """
        # 根据主题类型选择默认模板
        template_map = {
            'portrait': 'portrait_full',
            'product': 'product_photography',
            'art': 'art_style',
            'cinematic': 'cinematic'
        }

        template_name = template_map.get(theme_type, 'portrait_full')

        # 获取风格关键词
        style_kw = []
        if style and style in self.style_keywords:
            style_kw = self.style_keywords[style]

        return self.generate_from_template(
            template_name,
            theme,
            style_keywords=style_kw,
            **kwargs
        )

    def close(self):
        self.conn.close()


def main():
    """测试生成器引擎"""
    engine = PromptGeneratorEngine()

    print("🎯 可用模板:")
    for template_name in engine.list_templates():
        template = engine.get_template(template_name)
        print(f"  - {template_name}: {template['name']} - {template['description']}")

    # 测试1: 使用完整人物模板
    print("\n" + "="*80)
    print("测试1: 使用 portrait_full 模板生成赛博朋克动漫少女")
    print("="*80)

    result1 = engine.generate_from_template(
        'portrait_full',
        '赛博朋克风格的动漫少女',
        style_keywords=['neon', 'cyberpunk', 'futuristic', 'glow']
    )

    # 测试2: 使用产品摄影模板
    print("\n" + "="*80)
    print("测试2: 使用 product_photography 模板")
    print("="*80)

    result2 = engine.generate_from_template(
        'product_photography',
        '高端化妆品产品摄影',
        style_keywords=['luxury', 'elegant', 'premium']
    )

    # 测试3: 使用电影级模板
    print("\n" + "="*80)
    print("测试3: 使用 cinematic 模板")
    print("="*80)

    result3 = engine.generate_from_template(
        'cinematic',
        '电影级人物特写镜头',
        style_keywords=['dramatic', 'moody', 'atmospheric']
    )

    # 测试4: 智能生成（自动选择模板）
    print("\n" + "="*80)
    print("测试4: 智能生成 - 中国风水墨画")
    print("="*80)

    result4 = engine.generate_with_auto_template(
        '中国风水墨画插画',
        theme_type='art',
        style='chinese_traditional'
    )

    print(f"\n{'='*80}")
    print(f"📊 生成总结")
    print(f"{'='*80}")
    print(f"✅ 成功生成 4 个主题的提示词")
    print(f"✅ 测试1使用元素: {result1['total_elements']} 个")
    print(f"✅ 测试2使用元素: {result2['total_elements']} 个")
    print(f"✅ 测试3使用元素: {result3['total_elements']} 个")
    print(f"✅ 测试4使用元素: {result4['total_elements']} 个")
    print(f"{'='*80}")

    engine.close()


if __name__ == "__main__":
    main()
