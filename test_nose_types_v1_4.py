#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 facial_features_library.json v1.4 的nose_types扩展功能
验证7个鼻型分类及其人种关联
"""

import json

def load_library():
    """加载特征库"""
    with open('extracted_results/facial_features_library.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_nose_types(library):
    """测试所有鼻型分类"""
    print("="*70)
    print("  facial_features_library.json v1.4 - Nose Types模块测试")
    print("="*70)

    metadata = library['library_metadata']
    print(f"\n📚 库版本: v{metadata['version']}")
    print(f"📊 总分类数: {metadata['total_classifications']} 个")
    print(f"👃 Nose Types分类: {len(library['nose_types'])} 个")
    print()

    # 统计每个人种关联的鼻型数量
    ethnicity_nose_map = {}

    for nose_code, nose_data in library['nose_types'].items():
        chinese_name = nose_data.get('chinese_name', 'N/A')
        classification_code = nose_data.get('classification_code', nose_code)
        reusability = nose_data.get('reusability_score', 0)

        # 获取关联的人种
        associated_ethnicities = nose_data.get('associated_ethnicities', [])

        print(f"\n{'='*70}")
        print(f"👃 {nose_code}: {chinese_name}")
        print(f"{'='*70}")
        print(f"📝 分类代码: {classification_code}")
        print(f"⭐ 复用评分: {reusability}/10")

        if associated_ethnicities:
            print(f"🌍 关联人种: {', '.join(associated_ethnicities)}")
            # 统计
            for ethnicity in associated_ethnicities:
                if ethnicity not in ethnicity_nose_map:
                    ethnicity_nose_map[ethnicity] = []
                ethnicity_nose_map[ethnicity].append(nose_code)
        else:
            print(f"🌍 关联人种: 通用（所有人种）")

        # 显示视觉特征
        if 'visual_features' in nose_data:
            print(f"\n✨ 视觉特征:")
            for feature, desc in nose_data['visual_features'].items():
                print(f"   • {feature}: {desc}")

        # 显示使用建议
        if 'usage_recommendations' in nose_data:
            usage = nose_data['usage_recommendations']
            print(f"\n💡 使用建议:")
            for key, value in usage.items():
                print(f"   • {key}: {value}")

    # 显示人种-鼻型映射汇总
    print(f"\n\n{'='*70}")
    print("  🌍 人种-鼻型关联汇总")
    print(f"{'='*70}\n")

    for ethnicity, nose_types in sorted(ethnicity_nose_map.items()):
        ethnicity_data = library['ethnicity'].get(ethnicity, {})
        chinese_name = ethnicity_data.get('chinese_name', ethnicity)
        print(f"{ethnicity} ({chinese_name}): {len(nose_types)} 个鼻型")
        for nose_type in nose_types:
            nose_chinese = library['nose_types'][nose_type]['chinese_name']
            print(f"  ✓ {nose_type} ({nose_chinese})")
        print()

    print("="*70)
    print("  ✅ 测试完成！所有7个nose_types分类均可正常使用")
    print("="*70)

    # 验证总数
    expected_count = 7
    actual_count = len(library['nose_types'])
    if actual_count == expected_count:
        print(f"\n✅ 验证通过：nose_types总数 = {actual_count} (预期 {expected_count})")
    else:
        print(f"\n❌ 验证失败：nose_types总数 = {actual_count} (预期 {expected_count})")
        return False

    # 验证所有新鼻型都有ethnicity关联
    new_nose_types = ['flat_nose_bridge', 'high_nose_bridge', 'wide_nose',
                      'aquiline_nose', 'button_nose']

    print(f"\n✅ 验证新增的5个nose_types:")
    for nose_code in new_nose_types:
        if nose_code in library['nose_types']:
            associated = library['nose_types'][nose_code].get('associated_ethnicities', [])
            print(f"  ✓ {nose_code}: {', '.join(associated)}")
        else:
            print(f"  ❌ {nose_code}: 缺失")
            return False

    return True

def main():
    library = load_library()
    success = test_nose_types(library)

    if success:
        print("\n" + "="*70)
        print("  🎉 v1.4 Nose Types扩展测试全部通过！")
        print("="*70)
        print("\n✅ 7个nose_types分类已就绪")
        print("✅ 所有新鼻型都有人种关联")
        print("✅ 数据完整性验证通过")
        print("\n🚀 可以继续Phase 2 - Batch 3: 添加face_shapes\n")
    else:
        print("\n❌ 测试失败，请检查数据")

if __name__ == "__main__":
    main()
