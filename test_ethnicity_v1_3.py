#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 facial_features_library.json v1.3 的ethnicity扩展功能
演示8个人种分类的提示词生成
"""

import json

def load_library():
    """加载特征库"""
    with open('extracted_results/facial_features_library.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_prompt_for_ethnicity(ethnicity_code, library):
    """为指定人种生成示例提示词"""
    ethnicity_data = library['ethnicity'][ethnicity_code]

    # 基本信息
    chinese_name = ethnicity_data['chinese_name']
    regions = ', '.join(ethnicity_data['regions'])
    example_prompt = ethnicity_data['example_prompt']

    # 典型特征
    visual_features = ethnicity_data['visual_features']

    print(f"\n{'='*70}")
    print(f"🌍 {ethnicity_code.upper()}: {chinese_name}")
    print(f"{'='*70}")
    print(f"📍 覆盖地区: {regions}")
    print()
    print(f"👁️  典型五官特征:")
    for feature_type, description in visual_features.items():
        print(f"   {feature_type}: {description}")
    print()
    print(f"✨ 示例提示词:")
    print(f"   {example_prompt}")
    print()

def main():
    print("="*70)
    print("  facial_features_library.json v1.3 - Ethnicity模块测试")
    print("="*70)

    library = load_library()

    # 显示库信息
    metadata = library['library_metadata']
    print(f"\n📚 库版本: v{metadata['version']}")
    print(f"📊 总分类数: {metadata['total_classifications']} 个")
    print(f"🌍 Ethnicity分类: {len(library['ethnicity'])} 个")
    print()

    # 遍历所有ethnicity
    ethnicity_order = [
        'east_asian',
        'south_asian',
        'southeast_asian',
        'caucasian',
        'african',
        'latin_american',
        'middle_eastern',
        'mixed_ethnicity'
    ]

    for ethnicity_code in ethnicity_order:
        generate_prompt_for_ethnicity(ethnicity_code, library)

    print("="*70)
    print("  测试完成！所有8个ethnicity分类均可正常使用")
    print("="*70)

if __name__ == "__main__":
    main()
