#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成：仙剑奇侠传真人电影风格的年轻古装女子提示词（包含makeup字段）
"""

from intelligent_generator import IntelligentGenerator


def generate_xianjian_with_makeup():
    """生成仙剑奇侠传风格提示词（正确的makeup）"""
    gen = IntelligentGenerator()

    print("="*80)
    print("🎬 仙剑奇侠传真人电影风格 - 年轻古装女子")
    print("="*80)

    # 步骤1：构造完整intent（SKILL决策）
    print("\n📋 步骤1：Intent解析（SKILL决策层）")
    print("-"*80)

    intent = {
        'subject': {
            'gender': 'female',
            'ethnicity': 'East_Asian',
            'age_range': 'young_adult',
            'reasoning': '年轻古装女子 → 东亚女性'
        },
        'clothing': 'traditional_chinese',    # ← SKILL决定：古装 → 中国传统服装
        'hairstyle': 'ancient_chinese',       # ← SKILL决定：古装 → 古代发型
        'makeup': 'traditional_chinese',      # ← SKILL决定：古装+中国 → 传统中式妆容（不是k_beauty！）
        'era': 'ancient',                     # ← SKILL决定：古装 → 古代背景
        'lighting': 'cinematic',              # ← SKILL决定：电影级别 → 电影灯光
        'atmosphere': {
            'theme': 'fantasy',               # ← SKILL决定：仙剑奇侠传 → 仙侠奇幻
        },
        'visual_style': {
            'art_style': 'cinematic'          # ← SKILL决定：真人电影风格 → 电影级写实
        }
    }

    print("✅ SKILL完成Intent构造：")
    print(f"   - 主体：年轻东亚女性")
    print(f"   - 服装：{intent['clothing']} (古装)")
    print(f"   - 发型：{intent['hairstyle']} (古代发型)")
    print(f"   - 妆容：{intent['makeup']} (传统中式妆容) ← 不是k_beauty！")
    print(f"   - 时代：{intent['era']} (古代背景)")
    print(f"   - 光影：{intent['lighting']} (电影级灯光)")
    print(f"   - 氛围：{intent['atmosphere']['theme']} (仙侠奇幻)")
    print(f"   - 风格：{intent['visual_style']['art_style']} (真人电影)")

    # 步骤2：选择元素（代码执行层）
    print("\n🔍 步骤2：选择元素（代码执行层 - 根据SKILL指令查询）")
    print("-"*80)

    elements = gen.select_elements_by_intent(intent)
    print(f"✅ 选择了 {len(elements)} 个元素")

    # 显示评分
    style_elements = [e for e in elements if e.get('relevance') is not None]
    if style_elements:
        print(f"\n   前5个风格元素的评分：")
        for elem in style_elements[:5]:
            print(f"   - {elem['chinese_name']}: 相关性={elem.get('relevance', 0):.2f}, "
                  f"质量={elem.get('reusability', 0):.1f}, "
                  f"综合={elem.get('final_score', 0):.2f}")

    # 步骤3：检查一致性
    print("\n✓ 步骤3：检查一致性")
    print("-"*80)

    issues = gen.check_consistency(elements)
    if issues:
        print(f"⚠️ 发现 {len(issues)} 个一致性问题")
        fixed_elements, fixes = gen.resolve_conflicts(elements, issues)
        for fix in fixes:
            print(f"   {fix}")
    else:
        print("✓ 没有发现一致性问题")
        fixed_elements = elements

    # 步骤4：生成提示词
    print("\n✨ 步骤4：生成最终提示词")
    print("-"*80)

    prompt = gen.compose_prompt(fixed_elements, mode='auto', keywords_limit=3)

    # 步骤5：检查完整性
    print("\n🎯 步骤5：检查完整性")
    print("-"*80)

    missing = gen.check_completeness(intent, prompt)

    if missing:
        print(f"⚠️ 发现 {len(missing)} 个缺失的需求：")
        for item in missing:
            print(f"   - {item['description']}")
            print(f"     {item['suggestion']}")
    else:
        print("✅ 提示词满足所有用户要求！")

    # 检查妆容是否正确
    print("\n🔍 步骤6：验证妆容正确性")
    print("-"*80)

    if 'k-beauty' in prompt.lower() or 'korean' in prompt.lower():
        print("❌ 错误：提示词中包含韩系妆容（K-beauty），这不符合古装要求！")
    elif 'traditional chinese' in prompt.lower() and 'makeup' in prompt.lower():
        print("✅ 正确：提示词包含传统中式妆容（traditional Chinese makeup）")
    else:
        print("⚠️ 警告：提示词中可能缺少妆容描述")

    # 输出最终提示词
    print("\n" + "="*80)
    print("✨ 最终提示词")
    print("="*80)
    print()
    print(prompt)
    print()
    print("="*80)

    # 统计信息
    word_count = len(prompt.split(','))
    print(f"\n📊 统计：{word_count} 个元素 | 来源：{len(fixed_elements)} 个数据库元素")

    gen.close()


if __name__ == '__main__':
    generate_xianjian_with_makeup()
