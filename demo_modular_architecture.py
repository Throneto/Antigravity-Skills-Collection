#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块化架构演示
Demonstration of Modular Architecture

展示如何使用新的模块化库系统生成各类摄影prompt
"""

import json
from pathlib import Path

def load_library(filename):
    """加载库文件"""
    lib_path = Path(__file__).parent / "extracted_results" / filename
    with open(lib_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_index():
    """加载库索引"""
    return load_library("library_index.json")

def get_feature(library, category, code):
    """从库中获取特征"""
    if category in library and code in library[category]:
        return library[category][code]
    return None

print("\n" + "="*80)
print("  📚 模块化架构演示 - Modular Architecture Demo")
print("="*80 + "\n")

# 加载库
print("🔄 加载库文件...\n")
portrait_lib = load_library("facial_features_library.json")
common_lib = load_library("photography_common.json")
index = load_index()

print(f"✅ portrait_features_library v{portrait_lib['library_metadata']['version']}")
print(f"   - {portrait_lib['library_metadata']['total_classifications']} 个分类")
print(f"   - 专注：{portrait_lib['library_metadata'].get('focus', '人像摄影')}\n")

print(f"✅ photography_common v{common_lib['library_metadata']['version']}")
print(f"   - {common_lib['library_metadata']['total_classifications']} 个分类")
print(f"   - 专注：{common_lib['library_metadata']['focus']}\n")

print("="*80)

# 示例1: 人像摄影 - 使用两个库
print("\n📸 示例1：高端人像摄影（使用双库）")
print("-" * 80)

portrait_features = {
    "face_shape": portrait_lib["face_shapes"]["oval_asian_refined"],
    "eyes": portrait_lib["eye_types"]["large_expressive_almond"],
    "makeup": portrait_lib["makeup_styles"]["oxygen_fresh_natural"],
    "hair": portrait_lib["hair_styles"]["ponytail_with_bangs"],
    "expression": portrait_lib["expressions"]["gentle_smile"],
    "pose": portrait_lib["poses"]["relaxed_standing"]
}

common_features = {
    "camera_angle": common_lib["camera_angles"]["eye_level_close_up"],
    "lighting": common_lib["lighting_techniques"]["natural_window_light"],
    "effect": common_lib["technical_effects"]["bokeh_creamy_cinematic"]
}

print("\n来自 portrait_features_library:")
for key, feature in portrait_features.items():
    template = feature.get('ai_prompt_template') or ', '.join(feature.get('keywords', [])[:2])
    print(f"  • {feature['chinese_name']}: {template}")

print("\n来自 photography_common:")
for key, feature in common_features.items():
    print(f"  • {feature['chinese_name']}: {feature['ai_prompt_template']}")

# 组合prompt
prompt_parts = []
prompt_parts.append("A young Asian woman")
prompt_parts.append(portrait_features["face_shape"].get("ai_prompt_template") or ", ".join(portrait_features["face_shape"]["keywords"][:2]))
prompt_parts.append(", ".join(portrait_features["eyes"]["keywords"][:2]))
prompt_parts.append(portrait_features["hair"].get("ai_prompt_template") or ", ".join(portrait_features["hair"]["keywords"][:2]))
prompt_parts.append(portrait_features["makeup"]["visual_features"]["base"])
prompt_parts.append(portrait_features["expression"].get("ai_prompt_template") or ", ".join(portrait_features["expression"]["keywords"][:2]))
prompt_parts.append(portrait_features["pose"].get("ai_prompt_template") or ", ".join(portrait_features["pose"]["keywords"][:2]))
prompt_parts.append(common_features["camera_angle"]["ai_prompt_template"])
prompt_parts.append(common_features["lighting"]["ai_prompt_template"])
prompt_parts.append(common_features["effect"]["ai_prompt_template"])

combined_prompt = ", ".join(prompt_parts)
print(f"\n生成的Prompt:\n{combined_prompt}")

# 示例2: 产品摄影 - 主要使用通用库
print("\n\n" + "="*80)
print("📦 示例2：产品微距摄影（主要使用 photography_common）")
print("-" * 80)

product_features = {
    "technique": common_lib["photography_techniques"]["macro_photography"],
    "lighting1": common_lib["lighting_techniques"]["rim_lighting"],
    "lighting2": common_lib["lighting_techniques"]["natural_window_light"],
    "material": common_lib["material_textures"]["glossy_surfaces"],
    "effect": common_lib["technical_effects"]["bokeh_creamy_cinematic"],
    "angle": common_lib["camera_angles"]["high_angle_birds_eye"]
}

print("\n来自 photography_common:")
for key, feature in product_features.items():
    reuse_score = feature.get("reusability_score", "N/A")
    print(f"  • {feature['chinese_name']} (复用性: {reuse_score}/10)")
    print(f"    {feature['ai_prompt_template']}")

# 组合产品摄影prompt
product_prompt_parts = []
product_prompt_parts.append("A luxury watch on a marble surface")
product_prompt_parts.append(product_features["technique"]["ai_prompt_template"])
product_prompt_parts.append(product_features["angle"]["ai_prompt_template"])
product_prompt_parts.append(product_features["lighting1"]["ai_prompt_template"])
product_prompt_parts.append(product_features["lighting2"]["ai_prompt_template"])
product_prompt_parts.append(product_features["material"]["ai_prompt_template"])
product_prompt_parts.append(product_features["effect"]["ai_prompt_template"])
product_prompt_parts.append("professional product photography, 8K resolution")

product_prompt = ", ".join(product_prompt_parts)
print(f"\n生成的产品摄影Prompt:\n{product_prompt}")

# 示例3: 美食摄影 - 使用通用库
print("\n\n" + "="*80)
print("🍰 示例3：美食摄影（使用 photography_common）")
print("-" * 80)

food_features = {
    "lighting": common_lib["lighting_techniques"]["natural_window_light"],
    "effect1": common_lib["technical_effects"]["subsurface_scattering"],
    "effect2": common_lib["technical_effects"]["bokeh_creamy_cinematic"],
    "material": common_lib["material_textures"]["translucent_materials"],
    "angle": common_lib["camera_angles"]["eye_level_close_up"]
}

print("\n来自 photography_common:")
for key, feature in food_features.items():
    print(f"  • {feature['chinese_name']}: {feature['ai_prompt_template']}")

# 组合美食摄影prompt
food_prompt_parts = []
food_prompt_parts.append("A slice of layered cake with fresh strawberries")
food_prompt_parts.append(food_features["angle"]["ai_prompt_template"])
food_prompt_parts.append(food_features["lighting"]["ai_prompt_template"])
food_prompt_parts.append(food_features["effect1"]["ai_prompt_template"])
food_prompt_parts.append(food_features["material"]["ai_prompt_template"])
food_prompt_parts.append(food_features["effect2"]["ai_prompt_template"])
food_prompt_parts.append("professional food photography, mouthwatering, appetizing")

food_prompt = ", ".join(food_prompt_parts)
print(f"\n生成的美食摄影Prompt:\n{food_prompt}")

# 库统计
print("\n\n" + "="*80)
print("📊 库统计信息")
print("="*80 + "\n")

print(f"总库数: {index['statistics']['total_libraries']}")
print(f"总类别数: {index['statistics']['total_categories']}")
print(f"总分类数: {index['statistics']['total_classifications']}")
print(f"架构版本: v{index['statistics']['architecture_version']}")

print("\n类别归属:")
unique_to_portrait = sum(1 for cat, info in index['category_ownership'].items()
                         if info.get('exclusive') and info['primary_library'] == 'portrait_features_library')
unique_to_common = sum(1 for cat, info in index['category_ownership'].items()
                       if info.get('exclusive') and info['primary_library'] == 'photography_common')
shared = sum(1 for cat, info in index['category_ownership'].items() if not info.get('exclusive'))

print(f"  • portrait_features_library 独有: {unique_to_portrait} 个类别")
print(f"  • photography_common 独有: {unique_to_common} 个类别")
print(f"  • 共享类别: {shared} 个")

print("\n未来计划:")
for lib_name, lib_info in index['future_libraries'].items():
    print(f"  • {lib_name}: {lib_info['description']}")
    print(f"    状态: {lib_info['status']}, 优先级: {lib_info['priority']}")

print("\n" + "="*80)
print("\n✨ 模块化架构优势:")
print("  1. ✅ 清晰的职责划分 - 人像专注人像，通用技术跨领域")
print("  2. ✅ 高复用性 - 光影和相机角度可用于所有摄影类型")
print("  3. ✅ 易于扩展 - 可轻松添加新的专业库")
print("  4. ✅ 避免冗余 - 通用特征只维护一份")
print("\n💡 当前可支持:")
print("  • 人像摄影（完整支持）")
print("  • 产品摄影（基础支持，使用通用库）")
print("  • 美食摄影（基础支持，使用通用库）")
print("  • 微距摄影（支持）")
print("  • 艺术摄影（支持）")
print("\n" + "="*80 + "\n")
