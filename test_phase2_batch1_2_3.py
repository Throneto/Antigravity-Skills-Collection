#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 综合测试 (Batch 1-3)
验证 eye_types, nose_types, face_shapes 的扩展和人种关联
"""

import json

def load_library():
    """加载特征库"""
    with open('extracted_results/facial_features_library.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_phase2_progress(library):
    """测试Phase 2进度"""
    print("="*70)
    print("  Phase 2 进度测试 (Batch 1-3)")
    print("="*70)

    metadata = library['library_metadata']
    print(f"\n📚 库版本: v{metadata['version']}")
    print(f"📊 总分类数: {metadata['total_classifications']} 个")
    print()

    # 统计各类别数量
    categories = {
        'eye_types': len(library['eye_types']),
        'nose_types': len(library['nose_types']),
        'face_shapes': len(library['face_shapes']),
        'lip_types': len(library['lip_types']),
        'skin_textures': len(library['skin_textures']),
        'ethnicity': len(library['ethnicity'])
    }

    print("📊 各类别统计:")
    print(f"  👁️  eye_types: {categories['eye_types']} 个 (v1.2: 4个 → v1.4: 10个) ✅ Batch 1完成")
    print(f"  👃 nose_types: {categories['nose_types']} 个 (v1.2: 2个 → v1.4: 7个) ✅ Batch 2完成")
    print(f"  👤 face_shapes: {categories['face_shapes']} 个 (v1.2: 2个 → v1.4: 6个) ✅ Batch 3完成")
    print(f"  💋 lip_types: {categories['lip_types']} 个 (待扩展: +3个) ⏭️ Batch 4")
    print(f"  🎨 skin_textures: {categories['skin_textures']} 个 (待添加skin_tones: +6个) ⏭️ Batch 5")
    print(f"  🌍 ethnicity: {categories['ethnicity']} 个")
    print()

    # 统计人种关联
    print("="*70)
    print("  🌍 人种-五官关联统计")
    print("="*70)

    ethnicity_features = {}
    for ethnicity_code in library['ethnicity'].keys():
        ethnicity_features[ethnicity_code] = {
            'eyes': [],
            'noses': [],
            'faces': []
        }

    # 统计眼型关联
    for eye_code, eye_data in library['eye_types'].items():
        associated = eye_data.get('associated_ethnicities', [])
        for ethnicity in associated:
            if ethnicity in ethnicity_features:
                ethnicity_features[ethnicity]['eyes'].append(eye_code)

    # 统计鼻型关联
    for nose_code, nose_data in library['nose_types'].items():
        associated = nose_data.get('associated_ethnicities', [])
        for ethnicity in associated:
            if ethnicity in ethnicity_features:
                ethnicity_features[ethnicity]['noses'].append(nose_code)

    # 统计脸型关联
    for face_code, face_data in library['face_shapes'].items():
        associated = face_data.get('associated_ethnicities', [])
        for ethnicity in associated:
            if ethnicity in ethnicity_features:
                ethnicity_features[ethnicity]['faces'].append(face_code)

    # 打印汇总
    for ethnicity_code in sorted(ethnicity_features.keys()):
        ethnicity_data = library['ethnicity'][ethnicity_code]
        chinese_name = ethnicity_data.get('chinese_name', ethnicity_code)
        features = ethnicity_features[ethnicity_code]

        total_features = len(features['eyes']) + len(features['noses']) + len(features['faces'])
        print(f"\n{ethnicity_code} ({chinese_name}): {total_features} 个五官特征")

        if features['eyes']:
            print(f"  👁️  眼型 ({len(features['eyes'])}个):")
            for eye in features['eyes']:
                eye_name = library['eye_types'][eye]['chinese_name']
                print(f"     ✓ {eye} ({eye_name})")

        if features['noses']:
            print(f"  👃 鼻型 ({len(features['noses'])}个):")
            for nose in features['noses']:
                nose_name = library['nose_types'][nose]['chinese_name']
                print(f"     ✓ {nose} ({nose_name})")

        if features['faces']:
            print(f"  👤 脸型 ({len(features['faces'])}个):")
            for face in features['faces']:
                face_name = library['face_shapes'][face]['chinese_name']
                print(f"     ✓ {face} ({face_name})")

    # 验证总数
    print(f"\n\n{'='*70}")
    print("  ✅ Phase 2 进度验证")
    print(f"{'='*70}\n")

    expected_counts = {
        'eye_types': 10,
        'nose_types': 7,
        'face_shapes': 6
    }

    all_passed = True
    for category, expected in expected_counts.items():
        actual = categories[category]
        status = "✅" if actual == expected else "❌"
        print(f"{status} {category}: {actual} (预期 {expected})")
        if actual != expected:
            all_passed = False

    return all_passed

def main():
    library = load_library()
    success = test_phase2_progress(library)

    if success:
        print("\n" + "="*70)
        print("  🎉 Phase 2 Batch 1-3 全部完成！")
        print("="*70)
        print("\n✅ Batch 1: eye_types 扩展完成 (4 → 10个)")
        print("✅ Batch 2: nose_types 扩展完成 (2 → 7个)")
        print("✅ Batch 3: face_shapes 扩展完成 (2 → 6个)")
        print("\n📊 已新增: 15个人种特异性五官特征")
        print("📊 总分类数: 48个")
        print("\n⏭️  下一步: Batch 4 - 添加lip_types (3个新增)")
        print("⏭️  后续: Batch 5 - 添加skin_tones (6个新增)\n")
    else:
        print("\n❌ 测试失败，请检查数据")

if __name__ == "__main__":
    main()
