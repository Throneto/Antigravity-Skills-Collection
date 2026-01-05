#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
室内设计客厅生成演示 v4.0
展示如何使用 interior_design_library + photography_common 生成客厅设计
"""

import json
from pathlib import Path

def load_library(filename):
    """加载库文件"""
    lib_path = Path(__file__).parent / "extracted_results" / filename
    with open(lib_path, 'r', encoding='utf-8') as f:
        return json.load(f)

print("\n" + "="*80)
print("  🏠 室内设计客厅生成演示 - v4.0 Interior Design Demo")
print("="*80 + "\n")

# 加载库
print("📚 加载库...")
interior_lib = load_library("interior_design_library.json")
common_lib = load_library("photography_common.json")
print(f"✅ interior_design_library v{interior_lib['library_metadata']['version']} ({interior_lib['library_metadata']['total_classifications']} 分类)")
print(f"✅ photography_common v{common_lib['library_metadata']['version']} ({common_lib['library_metadata']['total_classifications']} 分类)")

print("\n" + "="*80)
print("  🎨 场景1: 北欧温馨风格客厅")
print("="*80 + "\n")

# 从库中选择特征
style = common_lib["interior_styles"]["nordic_cozy"]
space = interior_lib["space_types"]["living_room"]
layout = interior_lib["furniture_layouts"]["l_shape_sofa"]
lighting = common_lib["interior_lighting_scenarios"]["afternoon_warm"]
atmosphere = interior_lib["spatial_atmospheres"]["cozy_warm"]
wood_finish = common_lib["wood_finishes"]["light_oak"]
material_combo = interior_lib["material_combinations"]["textile_wood"]
camera_angle = common_lib["camera_angles"]["eye_level_close_up"]
bokeh = common_lib["technical_effects"]["bokeh_creamy_cinematic"]

print("选择的特征:")
print(f"  🏷️  风格: {style['chinese_name']}")
print(f"  🏠 空间: {space['chinese_name']}")
print(f"  🛋️  布局: {layout['chinese_name']}")
print(f"  💡 光照: {lighting['chinese_name']}")
print(f"  🌟 氛围: {atmosphere['chinese_name']}")
print(f"  🪵 木质: {wood_finish['chinese_name']}")
print(f"  🎨 材质组合: {material_combo['chinese_name']}")

# 组合生成prompt
print("\n" + "-"*80)
print("生成Prompt:\n")

prompt_parts = []

# 1. 风格和空间
prompt_parts.append(style['ai_prompt_template'])
prompt_parts.append(space['ai_prompt_template'])

# 2. 布局和家具
prompt_parts.append(layout['ai_prompt_template'])

# 3. 材质
prompt_parts.append(f"{wood_finish['ai_prompt_template']}")
prompt_parts.append(material_combo['ai_prompt_template'])

# 4. 氛围
prompt_parts.append(atmosphere['ai_prompt_template'])

# 5. 光照
prompt_parts.append(lighting['ai_prompt_template'])

# 6. 摄影技术
prompt_parts.append(camera_angle['ai_prompt_template'])
prompt_parts.append(bokeh['ai_prompt_template'])

# 7. 质量标签
prompt_parts.append("8K interior photography, architectural digest quality, professional lighting")

combined_prompt = ", ".join(prompt_parts)
print(combined_prompt)

print("\n" + "="*80)
print("  💎 场景2: 轻奢雅致风格客厅")
print("="*80 + "\n")

# 场景2：轻奢风格
style2 = common_lib["interior_styles"]["light_luxury"]
layout2 = interior_lib["furniture_layouts"]["linear_sofa"]
lighting2 = common_lib["interior_lighting_scenarios"]["evening_ambient"]
atmosphere2 = interior_lib["spatial_atmospheres"]["luxury_elegant"]
wood_finish2 = common_lib["wood_finishes"]["walnut_dark"]
material_combo2 = interior_lib["material_combinations"]["marble_brass"]
window_light = common_lib["lighting_techniques"]["natural_window_light"]

print("选择的特征:")
print(f"  🏷️  风格: {style2['chinese_name']}")
print(f"  🛋️  布局: {layout2['chinese_name']}")
print(f"  💡 光照: {lighting2['chinese_name']}")
print(f"  🌟 氛围: {atmosphere2['chinese_name']}")
print(f"  🪵 木质: {wood_finish2['chinese_name']}")
print(f"  🎨 材质组合: {material_combo2['chinese_name']}")

print("\n" + "-"*80)
print("生成Prompt:\n")

prompt_parts2 = []
prompt_parts2.append(style2['ai_prompt_template'])
prompt_parts2.append(space['ai_prompt_template'])
prompt_parts2.append(layout2['ai_prompt_template'])
prompt_parts2.append(f"{wood_finish2['ai_prompt_template']}")
prompt_parts2.append(material_combo2['ai_prompt_template'])
prompt_parts2.append(atmosphere2['ai_prompt_template'])
prompt_parts2.append(lighting2['ai_prompt_template'])
prompt_parts2.append(window_light['ai_prompt_template'])
prompt_parts2.append(camera_angle['ai_prompt_template'])
prompt_parts2.append("8K interior photography, luxury lifestyle, premium materials")

combined_prompt2 = ", ".join(prompt_parts2)
print(combined_prompt2)

print("\n" + "="*80)
print("  🌿 场景3: 现代简约开放式客厅")
print("="*80 + "\n")

# 场景3：现代简约
style3 = common_lib["interior_styles"]["modern_minimal"]
layout3 = interior_lib["furniture_layouts"]["open_plan_kitchen"]
lighting3 = common_lib["interior_lighting_scenarios"]["morning_light"]
atmosphere3 = interior_lib["spatial_atmospheres"]["modern_minimalist"]
stone_finish = common_lib["stone_finishes"]["large_format_tiles"]
material_combo3 = interior_lib["material_combinations"]["concrete_wood"]
design_element = interior_lib["design_elements"]["floor_to_ceiling_windows"]

print("选择的特征:")
print(f"  🏷️  风格: {style3['chinese_name']}")
print(f"  📐 布局: {layout3['chinese_name']}")
print(f"  💡 光照: {lighting3['chinese_name']}")
print(f"  🌟 氛围: {atmosphere3['chinese_name']}")
print(f"  🪨 石材: {stone_finish['chinese_name']}")
print(f"  🎨 材质组合: {material_combo3['chinese_name']}")
print(f"  ✨ 设计元素: {design_element['chinese_name']}")

print("\n" + "-"*80)
print("生成Prompt:\n")

prompt_parts3 = []
prompt_parts3.append(style3['ai_prompt_template'])
prompt_parts3.append(space['ai_prompt_template'])
prompt_parts3.append(layout3['ai_prompt_template'])
prompt_parts3.append(design_element['ai_prompt_template'])
prompt_parts3.append(f"{stone_finish['ai_prompt_template']}")
prompt_parts3.append(material_combo3['ai_prompt_template'])
prompt_parts3.append(atmosphere3['ai_prompt_template'])
prompt_parts3.append(lighting3['ai_prompt_template'])
prompt_parts3.append(common_lib["photography_techniques"]["wide_angle_24mm"]['ai_prompt_template'])
prompt_parts3.append("8K interior photography, architectural minimalism, clean modern design")

combined_prompt3 = ", ".join(prompt_parts3)
print(combined_prompt3)

# 保存结果
output_file = Path(__file__).parent / "generated_interior_living_rooms.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# 室内设计客厅生成结果 v4.0\n\n")

    f.write("## 场景1: 北欧温馨风格客厅\n")
    f.write(f"风格: {style['chinese_name']}\n")
    f.write(f"氛围: {atmosphere['chinese_name']}\n")
    f.write(f"Prompt:\n{combined_prompt}\n\n")
    f.write("-"*80 + "\n\n")

    f.write("## 场景2: 轻奢雅致风格客厅\n")
    f.write(f"风格: {style2['chinese_name']}\n")
    f.write(f"氛围: {atmosphere2['chinese_name']}\n")
    f.write(f"Prompt:\n{combined_prompt2}\n\n")
    f.write("-"*80 + "\n\n")

    f.write("## 场景3: 现代简约开放式客厅\n")
    f.write(f"风格: {style3['chinese_name']}\n")
    f.write(f"氛围: {atmosphere3['chinese_name']}\n")
    f.write(f"Prompt:\n{combined_prompt3}\n\n")

print("\n" + "="*80)
print("  📝 结果已保存")
print("="*80 + "\n")
print(f"文件: {output_file}")

print("\n" + "="*80)
print("  📊 库统计")
print("="*80 + "\n")
print(f"总库数: 3")
print(f"总分类数: 184")
print(f"  • portrait_features_library: 104")
print(f"  • photography_common: 30 (v2.0)")
print(f"  • interior_design_library: 50 (v1.0)")
print(f"\n架构版本: v4.0")

print("\n" + "="*80)
print("  ✨ 新增功能")
print("="*80 + "\n")
print("✅ 5种室内风格预设 (现代/轻奢/北欧/新中式/日式)")
print("✅ 9种空间类型 (客厅/主卧/厨房/餐厅等)")
print("✅ 12种家具布局 (L型沙发/开放式厨房等)")
print("✅ 15种设计元素 (背景墙/落地窗/氛围灯等)")
print("✅ 4种木质饰面 + 3种石材饰面")
print("✅ 4种光照场景 (晨光/午后/傍晚/无主灯)")
print("✅ 8种空间氛围 (温馨/简约/奢华/清新等)")
print("✅ 6种材质组合 (木石/金属玻璃/大理石黄铜等)")

print("\n" + "="*80)
print("  💡 使用建议")
print("="*80 + "\n")
print("1. 先选择整体风格 (interior_styles)")
print("2. 选择空间类型 (space_types)")
print("3. 选择布局和家具 (furniture_layouts)")
print("4. 选择材质 (wood_finishes, stone_finishes, material_combinations)")
print("5. 选择光照和氛围 (interior_lighting_scenarios, spatial_atmospheres)")
print("6. 添加设计元素 (design_elements)")
print("7. 添加摄影技术 (photography_common)")

print("\n" + "="*80 + "\n")
