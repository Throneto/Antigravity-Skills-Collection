#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试框架系统：仙剑奇侠传案例
"""

from framework_loader import FrameworkDrivenGenerator


def test_framework_xianjian():
    """测试：仙剑奇侠传真人电影风格的年轻古装女子"""

    print("="*80)
    print("🎬 测试框架系统：仙剑奇侠传真人电影风格的年轻古装女子")
    print("="*80)

    # 创建框架驱动生成器
    gen = FrameworkDrivenGenerator()

    # 用户请求："仙剑奇侠传真人电影风格的，电影级别的年轻古装女子图片"
    #
    # SKILL根据框架解析后的Intent（关键：包含makeup字段）
    intent = {
        'subject': {
            'gender': 'female',
            'ethnicity': 'East_Asian',
            'age_range': 'young_adult'
        },
        'styling': {
            'clothing': 'traditional_chinese',     # SKILL决定
            'hairstyle': 'ancient_chinese',        # SKILL决定
            'makeup': 'traditional_chinese',       # ← SKILL决定（不是k_beauty！）
        },
        'lighting': {
            'lighting_type': 'cinematic'           # SKILL决定
        },
        'scene': {
            'era': 'ancient',                      # SKILL决定
            'atmosphere': 'fantasy',               # SKILL决定
        },
        'technical': {
            'art_style': 'cinematic'               # SKILL决定
        }
    }

    print("\n📝 原始Intent（SKILL提供）：")
    print("-"*80)
    import json
    print(json.dumps(intent, indent=2, ensure_ascii=False))

    # 框架驱动生成
    result = gen.generate_by_framework(intent)

    # 输出结果
    print("\n" + "="*80)
    print("✨ 生成结果")
    print("="*80)

    print("\n【最终提示词】")
    print("-"*80)
    print(result['prompt'])
    print("-"*80)

    # 验证妆容
    print("\n🔍 妆容验证")
    print("-"*80)

    prompt_lower = result['prompt'].lower()

    if 'k-beauty' in prompt_lower or 'korean' in prompt_lower:
        print("❌ 错误：提示词包含韩系妆容（K-beauty）")
    elif 'traditional' in prompt_lower and ('chinese' in prompt_lower or 'ancient' in prompt_lower):
        print("✅ 正确：提示词包含传统中式妆容")
        print(f"   验证关键词：traditional, chinese, ancient")
    else:
        print("⚠️ 警告：无法确定妆容类型")

    # 统计
    word_count = len(result['prompt'].split(','))
    print(f"\n📊 统计：{word_count} 个元素 | 来源：{len(result['elements'])} 个数据库元素")

    print("\n" + "="*80)
    print("测试完成")
    print("="*80)

    gen.close()


if __name__ == '__main__':
    test_framework_xianjian()
