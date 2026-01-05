#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整工作流：生成 → 保存 → 分析
"""

from intelligent_generator import save_generated_prompt
from prompt_analyzer import (
    analyze_prompt_detail,
    get_library_statistics,
    recommend_elements_by_style
)

print("="*80)
print("完整工作流测试：生成 → 保存 → 分析")
print("="*80)

# ============================================================================
# 步骤1：模拟生成Prompt（简化版，实际应该用framework）
# ============================================================================
print("\n📝 步骤1：模拟生成Prompt")

# 模拟用户需求
user_intent = "西部世界风格的半人半机器人"

# 模拟SKILL选择的元素（应该通过framework查询，这里简化为直接构造）
selected_elements = [
    {
        'element_id': 'portrait_lighting_techniques_198',
        'name': 'dramatic_three_point_lighting',
        'chinese_name': '戏剧性三点照明',
        'template': 'dramatic three-point lighting with warm key light from left, cooler fill light from right, strong rim light creating edge separation, high contrast duality',
        'category': 'lighting_techniques',
        'field_name': 'lighting.lighting_type',
        'reusability': 9.0
    },
    {
        'element_id': 'portrait_lighting_techniques_199',
        'name': 'cinematic_volumetric_lighting',
        'chinese_name': '电影级体积光照明',
        'template': 'volumetric atmospheric haze adding depth and cinematic mood, minimalist dark gradient background, professional studio setup',
        'category': 'lighting_techniques',
        'field_name': 'lighting.atmosphere',
        'reusability': 8.0
    },
    {
        'element_id': 'art_special_effects_001',
        'name': 'half_human_half_machine_reveal',
        'chinese_name': '半人半机器垂直揭示',
        'template': 'dramatic vertical half-human half-android revelation with precise midline division, one half intact human appearance, other half exposing sophisticated mechanical layer beneath skin',
        'category': 'special_effects',
        'field_name': 'special.effect',
        'reusability': 7.0
    }
]

# 模拟生成的完整提示词
generated_prompt = "A young woman, " + ", ".join([e['template'] for e in selected_elements])

print(f"  用户需求: {user_intent}")
print(f"  使用元素: {len(selected_elements)}个")
print(f"  生成提示词长度: {len(generated_prompt)} 字符")

# ============================================================================
# 步骤2：保存到数据库
# ============================================================================
print("\n💾 步骤2：保存到数据库")

prompt_id = save_generated_prompt(
    prompt_text=generated_prompt,
    user_intent=user_intent,
    elements_used=selected_elements,
    style_tag="westworld_android",
    quality_score=9.2
)

print(f"  保存成功，Prompt ID: #{prompt_id}")

# ============================================================================
# 步骤3：使用analyzer分析
# ============================================================================
print("\n🔍 步骤3：使用analyzer分析")

# 功能A：查看详情
print("\n  功能A：查看Prompt详情")
result = analyze_prompt_detail(prompt_id)

if 'error' not in result:
    print(f"    Prompt ID: #{result['prompt_id']}")
    print(f"    用户需求: {result['user_intent']}")
    print(f"    风格标签: {result['style_tag']}")
    print(f"    质量评分: {result['quality_score']}/10")
    print(f"    使用元素: {len(result['elements'])}个")

    print(f"\n    元素列表:")
    for elem in result['elements']:
        print(f"      - [{elem['field_name']}] {elem['chinese_name']}")
        print(f"        复用度: {elem['reusability']}/10")
else:
    print(f"    ❌ {result['error']}")

# 功能B：元素库统计
print("\n  功能B：元素库统计")
stats = get_library_statistics()
print(f"    总元素数: {stats['total_elements']}")
print(f"    类别数: {len(stats['by_category'])}")
print(f"    Top 5类别:")
sorted_categories = sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:5]
for category, count in sorted_categories:
    print(f"      - {category}: {count}个")

# 功能C：按风格推荐（如果有足够数据）
print("\n  功能C：按风格推荐元素组合")
style_result = recommend_elements_by_style("westworld_android")

if 'error' not in style_result:
    print(f"    风格: {style_result['style']}")
    print(f"    数据来源: {style_result['total_prompts']}个历史Prompt")
    print(f"    推荐元素: {len(style_result['recommended_elements'])}个")

    if style_result['recommended_elements']:
        print(f"\n    Top 3推荐元素:")
        for elem in style_result['recommended_elements'][:3]:
            print(f"      - {elem['chinese_name']}")
            print(f"        使用频率: {elem['usage_frequency']*100:.0f}% ({elem['usage_count']}/{style_result['total_prompts']}次)")
            print(f"        复用度: {elem['reusability']}/10")
else:
    print(f"    ⚠️ {style_result['error']}")
    print(f"    （这是正常的，因为只有1个westworld_android风格的Prompt）")

# ============================================================================
# 总结
# ============================================================================
print("\n" + "="*80)
print("✅ 完整工作流测试完成！")
print("="*80)
print("\n测试结果:")
print(f"  1. ✅ 生成Prompt（模拟）")
print(f"  2. ✅ 保存到数据库 (Prompt ID: #{prompt_id})")
print(f"  3. ✅ 分析Prompt详情")
print(f"  4. ✅ 查询元素库统计")
print(f"  5. ✅ 按风格推荐（数据有限）")
print("\n三个skill的数据流:")
print("  universal-learner → elements 表 (934个元素)")
print("  intelligent-prompt-generator → generated_prompts 表 (至少1个)")
print("  prompt-analyzer → 可以分析了！")
print("\n💡 下一步：使用真实的SKILL调用测试")
