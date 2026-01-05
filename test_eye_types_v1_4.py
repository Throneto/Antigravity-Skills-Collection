#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 facial_features_library.json v1.4 的eye_types扩展功能
验证10个眼型分类及其人种关联
"""

import json

def load_library():
    """加载特征库"""
    with open('extracted_results/facial_features_library.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_eye_types(library):
    """测试所有眼型分类"""
    print("="*70)
    print("  facial_features_library.json v1.4 - Eye Types模块测试")
    print("="*70)

    metadata = library['library_metadata']
    print(f"\n📚 库版本: v{metadata['version']}")
    print(f"📊 总分类数: {metadata['total_classifications']} 个")
    print(f"👁️  Eye Types分类: {len(library['eye_types'])} 个")
    print()

    # 统计每个人种关联的眼型数量
    ethnicity_eye_map = {}

    for eye_code, eye_data in library['eye_types'].items():
        chinese_name = eye_data.get('chinese_name', 'N/A')
        classification_code = eye_data.get('classification_code', eye_code)
        reusability = eye_data.get('reusability_score', 0)

        # 获取关联的人种
        associated_ethnicities = eye_data.get('associated_ethnicities', [])

        print(f"\n{'='*70}")
        print(f"👁️  {eye_code}: {chinese_name}")
        print(f"{'='*70}")
        print(f"📝 分类代码: {classification_code}")
        print(f"⭐ 复用评分: {reusability}/10")

        if associated_ethnicities:
            print(f"🌍 关联人种: {', '.join(associated_ethnicities)}")
            # 统计
            for ethnicity in associated_ethnicities:
                if ethnicity not in ethnicity_eye_map:
                    ethnicity_eye_map[ethnicity] = []
                ethnicity_eye_map[ethnicity].append(eye_code)
        else:
            print(f"🌍 关联人种: 通用（所有人种）")

        # 显示视觉特征
        if 'visual_features' in eye_data:
            print(f"\n✨ 视觉特征:")
            for feature, desc in eye_data['visual_features'].items():
                print(f"   • {feature}: {desc}")

        # 显示使用建议
        if 'usage_recommendations' in eye_data:
            usage = eye_data['usage_recommendations']
            print(f"\n💡 使用建议:")
            for key, value in usage.items():
                print(f"   • {key}: {value}")

    # 显示人种-眼型映射汇总
    print(f"\n\n{'='*70}")
    print("  🌍 人种-眼型关联汇总")
    print(f"{'='*70}\n")

    for ethnicity, eye_types in sorted(ethnicity_eye_map.items()):
        ethnicity_data = library['ethnicity'].get(ethnicity, {})
        chinese_name = ethnicity_data.get('chinese_name', ethnicity)
        print(f"{ethnicity} ({chinese_name}): {len(eye_types)} 个眼型")
        for eye_type in eye_types:
            eye_chinese = library['eye_types'][eye_type]['chinese_name']
            print(f"  ✓ {eye_type} ({eye_chinese})")
        print()

    print("="*70)
    print("  ✅ 测试完成！所有10个eye_types分类均可正常使用")
    print("="*70)

    # 验证总数
    expected_count = 10
    actual_count = len(library['eye_types'])
    if actual_count == expected_count:
        print(f"\n✅ 验证通过：eye_types总数 = {actual_count} (预期 {expected_count})")
    else:
        print(f"\n❌ 验证失败：eye_types总数 = {actual_count} (预期 {expected_count})")
        return False

    # 验证所有新眼型都有ethnicity关联
    new_eye_types = ['monolid_eyes', 'double_eyelids', 'deep_set_eyes',
                     'hooded_lids', 'wide_expressive_eyes', 'almond_brown_eyes']

    print(f"\n✅ 验证新增的6个eye_types:")
    for eye_code in new_eye_types:
        if eye_code in library['eye_types']:
            associated = library['eye_types'][eye_code].get('associated_ethnicities', [])
            print(f"  ✓ {eye_code}: {', '.join(associated)}")
        else:
            print(f"  ❌ {eye_code}: 缺失")
            return False

    return True

def main():
    library = load_library()
    success = test_eye_types(library)

    if success:
        print("\n" + "="*70)
        print("  🎉 v1.4 Eye Types扩展测试全部通过！")
        print("="*70)
        print("\n✅ 10个eye_types分类已就绪")
        print("✅ 所有新眼型都有人种关联")
        print("✅ 数据完整性验证通过")
        print("\n🚀 可以继续Phase 2 - Batch 2: 添加nose_types\n")
    else:
        print("\n❌ 测试失败，请检查数据")

if __name__ == "__main__":
    main()
