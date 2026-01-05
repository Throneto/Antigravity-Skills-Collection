#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试：徐克风格的电影级的年轻女子古装图片提示词
验证完整性检查和相关性评分系统
"""

from intelligent_generator import IntelligentGenerator


def test_tsui_hark_period_costume():
    """
    测试用户需求："徐克风格的电影级的年轻女子古装图片提示词"

    需求分析：
    - "年轻女子" → 东亚女性，年轻成人
    - "古装" → 中国传统服装 + 古代发型 + 古代背景
    - "徐克风格" → 武侠、飘逸、动感特征
    - "电影级" → 电影灯光
    """
    gen = IntelligentGenerator()

    print("="*80)
    print("测试：徐克风格的电影级的年轻女子古装图片提示词")
    print("="*80)

    # 步骤1：构造完整intent（按照SKILL.md规则）
    print("\n📋 步骤1：构造Intent（全面提取所有用户条件）")
    print("-"*80)

    intent = {
        'subject': {
            'gender': 'female',
            'ethnicity': 'East_Asian',
            'age_range': 'young_adult',
            'reasoning': '"年轻女子" → 东亚女性'
        },
        'clothing': 'traditional_chinese',  # ← "古装" → 中国传统服装！
        'hairstyle': 'ancient_chinese',     # ← 自动匹配：古装→古代发型！
        'era': 'ancient',                   # ← "古装" → 古代背景！
        'lighting': 'cinematic',            # ← "电影级" → 电影灯光！
        'atmosphere': {
            'theme': 'period_drama',        # ← "古装" → 古装剧氛围
            'director_style': 'tsui_hark',  # ← "徐克" → 武侠、飘逸、动感！
        },
        'visual_style': {
            'art_style': 'cinematic'
        }
    }

    print("✅ Intent构造完成：")
    print(f"   - subject: 女性, 东亚人, 年轻成人")
    print(f"   - clothing: {intent['clothing']}")
    print(f"   - hairstyle: {intent['hairstyle']}")
    print(f"   - era: {intent['era']}")
    print(f"   - lighting: {intent['lighting']}")
    print(f"   - director_style: {intent['atmosphere']['director_style']}")

    # 步骤2：选择元素（使用相关性×质量评分）
    print("\n🔍 步骤2：选择元素（相关性 × 质量评分）")
    print("-"*80)

    elements = gen.select_elements_by_intent(intent)
    print(f"✅ 选择了 {len(elements)} 个元素")

    # 显示部分元素的评分（如果有）
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
        print(f"⚠️ 发现 {len(issues)} 个一致性问题:")
        for issue in issues:
            print(f"   - [{issue['severity']}] {issue['description']}")
            print(f"     {issue['suggestion']}")

        print("\n🔧 修正冲突...")
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
    print(f"\n{prompt}\n")

    # 步骤5：检查完整性（NEW！）
    print("\n🎯 步骤5：检查完整性（验证所有用户要求）")
    print("-"*80)

    missing = gen.check_completeness(intent, prompt)

    if missing:
        print(f"❌ 发现 {len(missing)} 个缺失的需求：")
        for item in missing:
            print(f"\n   类型：{item['requirement']}")
            print(f"   问题：{item['description']}")
            print(f"   建议：{item['suggestion']}")
            print(f"   期望关键词：{', '.join(item['expected'][:5])}")

        print("\n⚠️ 提示词不完整，需要补充缺失元素！")
    else:
        print("✅ 提示词满足所有用户要求！")
        print("\n验证通过的条件：")
        print("   ✓ 服装：传统中式服装")
        print("   ✓ 发型：古代发型")
        print("   ✓ 时代：古代背景")
        print("   ✓ 导演风格：徐克特征（武侠/动感）")
        print("   ✓ 光影：电影级灯光")

    # 统计信息
    print("\n📊 统计信息")
    print("-"*80)
    word_count = len(prompt.split(','))
    print(f"   - 总词数：{word_count} 个元素")
    print(f"   - 选择模式：auto（keywords优先）")
    print(f"   - 元素来源：{len(fixed_elements)} 个数据库元素")

    gen.close()

    print("\n" + "="*80)
    print("测试完成")
    print("="*80)


if __name__ == '__main__':
    test_tsui_hark_period_costume()
