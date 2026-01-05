#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有空template元素 - 完整版
"""

import sqlite3

def fix_all_empty_templates():
    conn = sqlite3.connect("extracted_results/elements.db")
    cursor = conn.cursor()

    # 获取所有空template的元素
    cursor.execute("""
        SELECT element_id, name, chinese_name, category_id
        FROM elements
        WHERE (ai_prompt_template = '' OR ai_prompt_template IS NULL)
    """)

    elements = cursor.fetchall()

    print(f"找到 {len(elements)} 个需要修复的元素\n")

    updated_count = 0
    skipped_count = 0

    for element_id, name, chinese_name, category_id in elements:
        template = None

        # === 妆容样式 ===
        if category_id == 'makeup_styles':
            # 将name转为描述 + "makeup style"
            makeup_map = {
                'k_beauty': 'Korean K-beauty makeup style, fresh natural dewy skin, gradient lips, straight brows',
                'j_beauty': 'Japanese J-beauty makeup style, subtle natural look, minimal eye makeup, glossy lips',
                'c_beauty': 'Chinese C-beauty makeup style, porcelain skin, delicate features, red lips',
                'traditional_chinese': 'traditional Chinese ancient makeup style, red lips, delicate eyebrows, classical elegance',
                'western_glam': 'Western glam makeup style, bold eyes, contoured features, matte lips',
                'french_elegant': 'French chic elegant makeup style, natural sophistication, subtle enhancement',
                'indian_traditional': 'Indian traditional bridal makeup style, bold eyes with kohl, vibrant colors',
                'arabic_glam': 'Arabic glam makeup style, dramatic smokey eyes, winged liner, bold brows',
                'latina_vibrant': 'Latina glam makeup style, warm tones, bronzed skin, bold lips',
                'thai_delicate': 'Thai beauty makeup style, soft natural look, luminous skin'
            }
            template = makeup_map.get(name, name.replace('_', ' ') + " makeup style")

        # === 表情 ===
        elif category_id == 'expressions':
            # 直接用name，替换下划线
            template = name.replace('_', ' ')

        # === 皮肤质感 ===
        elif category_id == 'skin_textures':
            texture_map = {
                'porcelain_flawless_radiant': 'porcelain flawless radiant skin texture, glowing luminous appearance',
                'realistic_textured_pores': 'realistic textured skin with visible pores, natural detail',
                'wet_dewy_droplets': 'wet dewy skin with water droplets effect, fresh moisture',
                'warm_rich_analog_film': 'warm rich analog film grain skin texture, vintage feel'
            }
            template = texture_map.get(name, name.replace('_', ' ') + " skin texture")

        # === 服装样式 ===
        elif category_id == 'clothing_styles':
            template = name.replace('_', ' ') + " clothing style"

        # === 发型 ===
        elif category_id in ['hair_style', 'hair_styles']:
            template = name.replace('_', ' ') + " hairstyle"

        # === 元数据类别（可以跳过）===
        elif category_id in ['expansion_roadmap', 'usage_index']:
            print(f"⊘ 跳过元数据: {element_id} [{category_id}]")
            skipped_count += 1
            continue

        # === 默认处理 ===
        else:
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
    print(f"✅ 成功修复 {updated_count} 个元素")
    print(f"⊘ 跳过 {skipped_count} 个元数据元素")
    print(f"{'='*80}")

    return updated_count


if __name__ == "__main__":
    fix_all_empty_templates()
