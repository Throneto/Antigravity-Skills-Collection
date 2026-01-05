#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复空template的基础人物属性元素
将name（英文描述）转换为ai_prompt_template
"""

import sqlite3

def fix_empty_templates():
    conn = sqlite3.connect("extracted_results/elements.db")
    cursor = conn.cursor()

    # 1. 获取所有空template的基础属性元素
    cursor.execute("""
        SELECT element_id, name, chinese_name, category_id
        FROM elements
        WHERE domain_id = 'portrait'
        AND (ai_prompt_template = '' OR ai_prompt_template IS NULL)
        AND category_id IN ('age_range', 'ethnicity', 'skin_tones', 'eye_types',
                           'nose_types', 'lip_types', 'face_shapes', 'hair_colors', 'gender')
    """)

    elements = cursor.fetchall()

    print(f"找到 {len(elements)} 个需要修复的元素\n")

    updated_count = 0

    for element_id, name, chinese_name, category_id in elements:
        # 将name（下划线分隔）转换为自然语言
        # 例如: "large_expressive_almond" -> "large expressive almond-shaped eyes"

        template = None

        if category_id == 'eye_types':
            # 眼型：将name转为描述 + "eyes"
            template = name.replace('_', ' ') + " eyes"

        elif category_id == 'face_shapes':
            # 脸型：将name转为描述 + "face shape"
            template = name.replace('_', ' ') + " face shape"

        elif category_id == 'nose_types':
            # 鼻型：将name转为描述 + "nose"
            template = name.replace('_', ' ') + " nose"

        elif category_id == 'lip_types':
            # 唇型：将name转为描述 + "lips"
            template = name.replace('_', ' ') + " lips"

        elif category_id == 'age_range':
            # 年龄：直接用中文名的英文翻译
            age_map = {
                'young_adult': 'young adult (18-25 years old)',
                'adult': 'adult (25-35 years old)',
                'teenager': 'teenager (13-17 years old)',
                'child': 'child (5-12 years old)',
                'middle_aged': 'middle-aged (35-50 years old)'
            }
            template = age_map.get(name, name.replace('_', ' '))

        elif category_id == 'ethnicity':
            # 国籍/族裔：直接用name
            ethnicity_map = {
                'east_asian': 'East Asian',
                'south_asian': 'South Asian',
                'southeast_asian': 'Southeast Asian',
                'caucasian': 'Caucasian',
                'african': 'African',
                'latin_american': 'Latin American',
                'middle_eastern': 'Middle Eastern',
                'mixed_ethnicity': 'Mixed ethnicity'
            }
            template = ethnicity_map.get(name, name.replace('_', ' '))

        elif category_id == 'skin_tones':
            # 肤色：描述 + "skin tone"
            template = name.replace('_', ' ') + " skin tone"

        elif category_id == 'hair_colors':
            # 发色：描述 + "hair"
            template = name.replace('_', ' ') + " hair"

        elif category_id == 'gender':
            # 性别
            template = name.replace('_', ' ')

        else:
            # 默认：直接用name替换下划线
            template = name.replace('_', ' ')

        if template:
            # 更新数据库
            cursor.execute("""
                UPDATE elements
                SET ai_prompt_template = ?
                WHERE element_id = ?
            """, (template, element_id))

            updated_count += 1
            print(f"✓ {element_id}")
            print(f"  [{category_id}] {chinese_name}")
            print(f"  template: {template}\n")

    conn.commit()
    conn.close()

    print(f"\n{'='*80}")
    print(f"✅ 成功修复 {updated_count} 个元素的ai_prompt_template")
    print(f"{'='*80}")

    return updated_count


if __name__ == "__main__":
    fix_empty_templates()
