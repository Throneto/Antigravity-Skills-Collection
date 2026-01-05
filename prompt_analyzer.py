#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Analyzer - 执行层
只负责查询数据，不做任何决策
"""

import sqlite3
from typing import Dict, List, Optional
from datetime import datetime

DB_PATH = 'extracted_results/elements.db'


def analyze_prompt_detail(prompt_id: int, db_path: str = DB_PATH) -> dict:
    """
    【执行层】查询Prompt完整信息

    返回原始数据，由SKILL层决定如何展示

    参数：
    - prompt_id: Prompt ID
    - db_path: 数据库路径

    返回：
    dict包含：prompt基本信息 + 使用的元素列表
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 查询Prompt基本信息
        cursor.execute('''
            SELECT prompt_text, user_intent, generation_date, quality_score, style_tag
            FROM generated_prompts
            WHERE prompt_id = ?
        ''', (prompt_id,))

        prompt_info = cursor.fetchone()

        if not prompt_info:
            return {'error': f'Prompt #{prompt_id} not found'}

        # 查询使用的所有元素
        cursor.execute('''
            SELECT pe.category, pe.field_name, e.element_id, e.name, e.chinese_name,
                   e.ai_prompt_template, e.reusability_score
            FROM prompt_elements pe
            JOIN elements e ON pe.element_id = e.element_id
            WHERE pe.prompt_id = ?
        ''', (prompt_id,))

        elements = cursor.fetchall()

        return {
            'prompt_id': prompt_id,
            'prompt_text': prompt_info[0],
            'user_intent': prompt_info[1],
            'generation_date': prompt_info[2],
            'quality_score': prompt_info[3],
            'style_tag': prompt_info[4],
            'elements': [
                {
                    'category': e[0],
                    'field_name': e[1],
                    'element_id': e[2],
                    'name': e[3],
                    'chinese_name': e[4],
                    'template': e[5],
                    'reusability': e[6]
                }
                for e in elements
            ]
        }

    finally:
        conn.close()


def compare_prompts(prompt_id1: int, prompt_id2: int, db_path: str = DB_PATH) -> dict:
    """
    【执行层】对比两个Prompt

    返回原始对比数据，由SKILL层分析差异

    参数：
    - prompt_id1: 第一个Prompt ID
    - prompt_id2: 第二个Prompt ID
    - db_path: 数据库路径

    返回：
    dict包含：两个Prompt的详情 + 共同元素 + 独有元素 + 相似度
    """
    # 获取两个Prompt的详情
    p1 = analyze_prompt_detail(prompt_id1, db_path)
    p2 = analyze_prompt_detail(prompt_id2, db_path)

    if 'error' in p1 or 'error' in p2:
        return {'error': 'One or both prompts not found'}

    # 提取元素ID集合
    p1_element_ids = {e['element_id'] for e in p1['elements']}
    p2_element_ids = {e['element_id'] for e in p2['elements']}

    # 计算共同和独有元素
    common_ids = p1_element_ids & p2_element_ids
    unique_to_p1_ids = p1_element_ids - p2_element_ids
    unique_to_p2_ids = p2_element_ids - p1_element_ids

    # 获取元素详情
    common_elements = [e for e in p1['elements'] if e['element_id'] in common_ids]
    unique_to_p1 = [e for e in p1['elements'] if e['element_id'] in unique_to_p1_ids]
    unique_to_p2 = [e for e in p2['elements'] if e['element_id'] in unique_to_p2_ids]

    # 计算相似度
    total_unique_elements = len(p1_element_ids | p2_element_ids)
    similarity_score = len(common_ids) / total_unique_elements if total_unique_elements > 0 else 0.0

    return {
        'prompt1': p1,
        'prompt2': p2,
        'common_elements': common_elements,
        'unique_to_p1': unique_to_p1,
        'unique_to_p2': unique_to_p2,
        'similarity_score': similarity_score,
        'common_count': len(common_ids),
        'total_elements_p1': len(p1_element_ids),
        'total_elements_p2': len(p2_element_ids)
    }


def recommend_similar_prompts(prompt_id: int, top_n: int = 3, db_path: str = DB_PATH) -> list:
    """
    【执行层】推荐相似Prompts

    算法：计算元素重叠度，返回Top N

    参数：
    - prompt_id: 目标Prompt ID
    - top_n: 返回前N个相似Prompt（默认3个）
    - db_path: 数据库路径

    返回：
    list，每项包含：prompt_id, similarity, common_count, prompt_info
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 获取目标Prompt使用的元素
        cursor.execute('''
            SELECT element_id FROM prompt_elements
            WHERE prompt_id = ?
        ''', (prompt_id,))

        target_elements = {row[0] for row in cursor.fetchall()}

        if not target_elements:
            return {'error': f'Prompt #{prompt_id} not found or has no elements'}

        # 查询所有其他Prompts
        cursor.execute('''
            SELECT prompt_id, user_intent, style_tag, quality_score
            FROM generated_prompts
            WHERE prompt_id != ?
        ''', (prompt_id,))

        all_prompts = cursor.fetchall()

        # 计算相似度
        similarities = []
        for other_id, user_intent, style_tag, quality_score in all_prompts:
            cursor.execute('''
                SELECT element_id FROM prompt_elements
                WHERE prompt_id = ?
            ''', (other_id,))

            other_elements = {row[0] for row in cursor.fetchall()}

            common = target_elements & other_elements
            total_unique = len(target_elements | other_elements)
            similarity = len(common) / total_unique if total_unique > 0 else 0.0

            similarities.append({
                'prompt_id': other_id,
                'user_intent': user_intent,
                'style_tag': style_tag,
                'quality_score': quality_score,
                'similarity': similarity,
                'common_count': len(common),
                'common_element_ids': list(common)
            })

        # 排序并返回Top N
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_n]

    finally:
        conn.close()


def get_library_statistics(category: str = None, db_path: str = DB_PATH) -> dict:
    """
    【执行层】查询元素库统计

    参数：
    - category: 可选，指定类别查询详情（如makeup_styles）
    - db_path: 数据库路径

    返回：
    dict包含：总元素数 + 按类别分布 + （可选）类别详情
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 总元素数
        cursor.execute('SELECT COUNT(*) FROM elements')
        total = cursor.fetchone()[0]

        # 按类别统计
        cursor.execute('''
            SELECT category_id, COUNT(*)
            FROM elements
            GROUP BY category_id
        ''')
        by_category = {row[0]: row[1] for row in cursor.fetchall()}

        result = {
            'total_elements': total,
            'by_category': by_category
        }

        # 如果指定类别，查询详情
        if category:
            cursor.execute('''
                SELECT e.element_id, e.name, e.chinese_name, e.reusability_score,
                       COALESCE(s.usage_count, 0) as usage_count,
                       COALESCE(s.avg_quality, 0) as avg_quality
                FROM elements e
                LEFT JOIN element_usage_stats s ON e.element_id = s.element_id
                WHERE e.category_id = ?
                ORDER BY usage_count DESC, reusability_score DESC
            ''', (category,))

            elements = cursor.fetchall()
            result['category_details'] = {
                'category': category,
                'total_count': len(elements),
                'elements': [
                    {
                        'element_id': e[0],
                        'name': e[1],
                        'chinese_name': e[2],
                        'reusability': e[3],
                        'usage_count': e[4],
                        'avg_quality': e[5]
                    }
                    for e in elements
                ]
            }

        return result

    finally:
        conn.close()


def recommend_elements_by_style(style: str, db_path: str = DB_PATH) -> dict:
    """
    【执行层】按风格推荐元素组合

    算法：
    1. 查询该风格的所有历史Prompts
    2. 统计每个元素的使用频率
    3. 返回高频元素

    参数：
    - style: 风格标签（如ancient_chinese, modern_sci_fi）
    - db_path: 数据库路径

    返回：
    dict包含：风格信息 + 推荐元素列表（按使用频率排序）
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 查询该风格的所有Prompts
        cursor.execute('''
            SELECT prompt_id FROM generated_prompts
            WHERE style_tag = ?
        ''', (style,))

        style_prompts = [row[0] for row in cursor.fetchall()]
        total_prompts = len(style_prompts)

        if total_prompts == 0:
            return {'error': f'No prompts found for style: {style}'}

        # 统计元素使用频率
        element_stats = {}

        for pid in style_prompts:
            cursor.execute('''
                SELECT pe.element_id, pe.category, pe.field_name,
                       e.name, e.chinese_name, e.ai_prompt_template, e.reusability_score
                FROM prompt_elements pe
                JOIN elements e ON pe.element_id = e.element_id
                WHERE pe.prompt_id = ?
            ''', (pid,))

            for row in cursor.fetchall():
                element_id = row[0]
                if element_id not in element_stats:
                    element_stats[element_id] = {
                        'element_id': element_id,
                        'category': row[1],
                        'field_name': row[2],
                        'name': row[3],
                        'chinese_name': row[4],
                        'template': row[5],
                        'reusability': row[6],
                        'usage_count': 0
                    }
                element_stats[element_id]['usage_count'] += 1

        # 计算使用频率
        for element in element_stats.values():
            element['usage_frequency'] = element['usage_count'] / total_prompts

        # 按使用频率排序
        sorted_elements = sorted(element_stats.values(),
                                key=lambda x: (x['usage_frequency'], x['reusability']),
                                reverse=True)

        return {
            'style': style,
            'total_prompts': total_prompts,
            'recommended_elements': sorted_elements
        }

    finally:
        conn.close()


if __name__ == '__main__':
    """测试执行层函数"""

    print("="*80)
    print("Prompt Analyzer - 执行层函数测试")
    print("="*80)

    # 测试获取库统计
    print("\n📊 测试：get_library_statistics()")
    stats = get_library_statistics()
    print(f"  总元素数: {stats['total_elements']}")
    print(f"  类别数: {len(stats['by_category'])}")

    # 测试获取makeup类别详情
    print("\n📊 测试：get_library_statistics('makeup_styles')")
    makeup_stats = get_library_statistics('makeup_styles')
    if 'category_details' in makeup_stats:
        details = makeup_stats['category_details']
        print(f"  makeup_styles 类别: {details['total_count']} 个元素")
        if details['elements']:
            top3 = details['elements'][:3]
            print("  Top 3最常用元素:")
            for e in top3:
                print(f"    - {e['chinese_name']} (使用{e['usage_count']}次)")

    print("\n✅ 执行层函数测试完成")
