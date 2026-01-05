#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.5 妆容风格完整测试
验证makeup_styles类别的10个全球主要妆容风格
"""

import json

def load_library():
    """加载特征库"""
    with open('extracted_results/facial_features_library.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_makeup_styles(library):
    """测试makeup_styles类别"""
    print("="*80)
    print("  🎨 facial_features_library.json v1.5 - Makeup Styles 测试")
    print("="*80)

    metadata = library['library_metadata']
    print(f"\n📚 库版本: v{metadata['version']}")
    print(f"📂 总类别数: {metadata['total_categories']} 个")
    print(f"📊 总分类数: {metadata['total_classifications']} 个")
    print()

    # 验证makeup_styles类别存在
    if 'makeup_styles' not in library:
        print("❌ 错误: makeup_styles类别未找到！")
        return False

    makeup_styles = library['makeup_styles']
    print(f"🎨 makeup_styles 类别包含 {len(makeup_styles)} 个妆容风格\n")

    # 预期的10个核心妆容风格
    expected_styles = [
        'k_beauty',
        'j_beauty',
        'c_beauty',
        'traditional_chinese',
        'western_glam',
        'french_elegant',
        'indian_traditional',
        'arabic_glam',
        'latina_vibrant',
        'thai_delicate'
    ]

    print("="*80)
    print("  📋 妆容风格详细信息")
    print("="*80)

    all_passed = True
    for i, style_code in enumerate(expected_styles, 1):
        if style_code not in makeup_styles:
            print(f"\n❌ 错误: 缺少妆容风格 '{style_code}'")
            all_passed = False
            continue

        style = makeup_styles[style_code]
        chinese_name = style.get('chinese_name', 'N/A')
        associated_ethnicity = style.get('associated_ethnicity', 'N/A')
        core_concept = style.get('core_concept', [])
        overall_feeling = style.get('overall_feeling', 'N/A')
        representative_figures = style.get('representative_figures', [])
        reusability_score = style.get('reusability_score', 0)

        print(f"\n{i}. {style_code}")
        print(f"   中文名称: {chinese_name}")
        print(f"   核心概念: {', '.join(core_concept)}")
        print(f"   关联人种: {associated_ethnicity}")
        print(f"   整体感觉: {overall_feeling}")
        print(f"   代表人物: {', '.join(representative_figures)}")
        print(f"   复用评分: {reusability_score}/10")

        # 验证必需字段
        required_sections = ['base_makeup', 'brows', 'eyes', 'cheeks', 'lips']
        for section in required_sections:
            if section not in style:
                print(f"   ⚠️  缺少 '{section}' 部分")
                all_passed = False
            else:
                section_data = style[section]
                keywords_count = len(section_data.get('keywords', []))
                print(f"   ✓ {section}: {keywords_count} 个关键词")

        # 验证AI提示词模板
        if 'complete_prompt_template' not in style:
            print(f"   ⚠️  缺少 'complete_prompt_template'")
            all_passed = False
        else:
            template_length = len(style['complete_prompt_template'])
            print(f"   ✓ complete_prompt_template: {template_length} 字符")

        # 验证usage_recommendations
        if 'usage_recommendations' in style:
            usage = style['usage_recommendations']
            print(f"   ✓ usage_recommendations: {len(usage)} 个建议项")

    # 统计人种-妆容关联
    print(f"\n\n{'='*80}")
    print("  🌍 人种-妆容风格关联统计")
    print(f"{'='*80}\n")

    ethnicity_makeup_map = {}
    for style_code, style_data in makeup_styles.items():
        ethnicity = style_data.get('associated_ethnicity', 'unknown')
        if ethnicity not in ethnicity_makeup_map:
            ethnicity_makeup_map[ethnicity] = []
        ethnicity_makeup_map[ethnicity].append(style_code)

    for ethnicity in sorted(ethnicity_makeup_map.keys()):
        styles = ethnicity_makeup_map[ethnicity]
        ethnicity_name = library['ethnicity'].get(ethnicity, {}).get('chinese_name', ethnicity)
        print(f"🌍 {ethnicity} ({ethnicity_name}): {len(styles)} 个妆容风格")
        for style in styles:
            style_name = makeup_styles[style]['chinese_name']
            print(f"  • {style} ({style_name})")
        print()

    # 验证总数
    print(f"{'='*80}")
    print("  ✅ v1.5 完整性验证")
    print(f"{'='*80}\n")

    print(f"✓ 预期妆容风格数: {len(expected_styles)}")
    print(f"✓ 实际妆容风格数: {len(makeup_styles)}")
    print(f"✓ 总类别数: {metadata['total_categories']} (预期 11)")
    print(f"✓ 总分类数: {metadata['total_classifications']} (预期 67)")
    print()

    if len(makeup_styles) != len(expected_styles):
        print(f"❌ 妆容风格数量不匹配！")
        all_passed = False

    if metadata['total_categories'] != 11:
        print(f"❌ 总类别数不正确！")
        all_passed = False

    if metadata['total_classifications'] != 67:
        print(f"❌ 总分类数不正确！")
        all_passed = False

    return all_passed

def main():
    library = load_library()
    success = test_makeup_styles(library)

    if success:
        print("="*80)
        print("  🎉🎉🎉 v1.5 Makeup Styles 集成成功！ 🎉🎉🎉")
        print("="*80)
        print("\n✅ 新增 makeup_styles 类别")
        print("✅ 包含 10 个全球主要妆容风格")
        print("✅ 每个风格包含完整的 base_makeup, brows, eyes, cheeks, lips")
        print("✅ 提供 complete_prompt_template 可直接用于AI生成")
        print("✅ 所有妆容风格都关联到对应人种")
        print()
        print("📊 版本变化:")
        print("  • v1.4 → v1.5")
        print("  • total_categories: 10 → 11")
        print("  • total_classifications: 57 → 67 (+17.5%)")
        print()
        print("🌍 文化覆盖:")
        print("  • 东亚: K-beauty, J-beauty, C-beauty, 传统古风中式")
        print("  • 欧美: Western Glam, French Elegant")
        print("  • 南亚: Indian Traditional")
        print("  • 中东: Arabic Glam")
        print("  • 拉丁美洲: Latina Vibrant")
        print("  • 东南亚: Thai Delicate")
        print()
        print("🚀 系统状态: v1.5 已完全就绪！")
        print("📁 数据文件: facial_features_library.json v1.5")
        print()
    else:
        print("\n❌ 测试失败，请检查数据")

if __name__ == "__main__":
    main()
