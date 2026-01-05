#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加古装相关元素：传统发型、武侠风格等
"""

import sqlite3
import json

def add_period_costume_elements():
    """添加缺失的古装元素"""
    conn = sqlite3.connect("extracted_results/elements.db")
    cursor = conn.cursor()

    # 定义新元素
    new_elements = [
        # 1. 传统发型 - 古代发髻（Hair Styles）
        {
            'element_id': 'hair_traditional_chinese_updo',
            'name': 'traditional_chinese_updo',
            'chinese_name': '传统中式发髻',
            'ai_prompt_template': 'traditional Chinese updo hairstyle with elegant hair ornaments, classical hair bun adorned with hairpins and flowers, intricate traditional styling',
            'keywords': json.dumps([
                'traditional hairstyle',
                'classical Chinese updo',
                'hair ornaments',
                'elegant hairpins',
                'hair bun with decorative accessories',
                'traditional hair styling',
                'ornate hair decoration',
                'classical Chinese coiffure'
            ]),
            'domain_id': 'portrait',
            'category_id': 'hair_styles',
            'reusability_score': 8.5,
            'learned_from': 'manual_period_costume'
        },

        # 2. 武侠风格 - 氛围/风格（Atmosphere/Style）
        {
            'element_id': 'style_wuxia',
            'name': 'wuxia_style',
            'chinese_name': '武侠风格',
            'ai_prompt_template': 'wuxia martial arts aesthetic, flowing dynamic movement, traditional Chinese martial arts atmosphere, heroic and graceful poses',
            'keywords': json.dumps([
                'wuxia',
                'martial arts style',
                'flowing movement',
                'dynamic action',
                'traditional Chinese martial arts',
                'heroic pose',
                'graceful combat stance',
                'period martial arts'
            ]),
            'domain_id': 'portrait',
            'category_id': 'atmosphere_themes',
            'reusability_score': 8.0,
            'learned_from': 'manual_tsui_hark_style'
        },

        # 3. 古装服饰 - 更具体的传统中式服装（Clothing）
        {
            'element_id': 'clothing_hanfu_traditional',
            'name': 'hanfu_traditional',
            'chinese_name': '汉服传统服饰',
            'ai_prompt_template': 'wearing traditional Chinese Hanfu costume, flowing period dress with intricate embroidery, authentic ancient Chinese attire with layered silk robes',
            'keywords': json.dumps([
                'traditional Chinese costume',
                'Hanfu',
                'period dress',
                'ancient Chinese attire',
                'flowing silk robes',
                'traditional embroidered costume',
                'classical Chinese clothing',
                'layered traditional dress'
            ]),
            'domain_id': 'portrait',
            'category_id': 'clothing_styles',
            'reusability_score': 9.0,
            'learned_from': 'manual_period_costume'
        },

        # 4. 古装场景 - 传统建筑背景（Background）
        {
            'element_id': 'background_traditional_chinese',
            'name': 'traditional_chinese_architecture',
            'chinese_name': '传统中式建筑背景',
            'ai_prompt_template': 'traditional Chinese architectural elements in background, classical pavilion and courtyard setting, period drama atmosphere with ancient architecture',
            'keywords': json.dumps([
                'traditional Chinese architecture',
                'classical pavilion',
                'period setting',
                'ancient courtyard',
                'traditional building elements',
                'historical Chinese background',
                'classical architectural details'
            ]),
            'domain_id': 'portrait',
            'category_id': 'backgrounds',
            'reusability_score': 7.5,
            'learned_from': 'manual_period_costume'
        },

        # 5. 徐克风格 - 飘逸动感（Movement/Pose）
        {
            'element_id': 'pose_flowing_dynamic',
            'name': 'flowing_dynamic_pose',
            'chinese_name': '飘逸动感姿态',
            'ai_prompt_template': 'flowing dynamic pose with graceful movement, fabric and hair flowing in motion, elegant kinetic energy',
            'keywords': json.dumps([
                'flowing pose',
                'dynamic movement',
                'graceful motion',
                'fabric flowing',
                'hair flowing in wind',
                'elegant kinetic pose',
                'dynamic grace'
            ]),
            'domain_id': 'portrait',
            'category_id': 'poses',
            'reusability_score': 8.0,
            'learned_from': 'manual_tsui_hark_style'
        }
    ]

    # 插入元素
    insert_query = """
        INSERT OR REPLACE INTO elements
        (element_id, name, chinese_name, ai_prompt_template, keywords,
         domain_id, category_id, reusability_score, learned_from)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    print("="*80)
    print("添加古装相关元素")
    print("="*80)

    for elem in new_elements:
        cursor.execute(insert_query, (
            elem['element_id'],
            elem['name'],
            elem['chinese_name'],
            elem['ai_prompt_template'],
            elem['keywords'],
            elem['domain_id'],
            elem['category_id'],
            elem['reusability_score'],
            elem['learned_from']
        ))
        print(f"✓ 添加: {elem['chinese_name']} ({elem['category_id']})")

    conn.commit()
    conn.close()

    print(f"\n✅ 成功添加 {len(new_elements)} 个元素")
    print("="*80)


if __name__ == '__main__':
    add_period_costume_elements()
