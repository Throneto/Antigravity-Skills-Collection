#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中古风客厅生成演示
Mid-century Modern Living Room with Herringbone Flooring
"""

import json
from pathlib import Path

def load_library(filename):
    """加载库文件"""
    lib_path = Path(__file__).parent / "extracted_results" / filename
    with open(lib_path, 'r', encoding='utf-8') as f:
        return json.load(f)

print("\n" + "="*80)
print("  🏠 中古风客厅生成 - Mid-century Modern Living Room")
print("="*80 + "\n")

# 加载库
interior_lib = load_library("interior_design_library.json")
common_lib = load_library("photography_common.json")

print("📚 加载特征库...\n")

# 中古风特征组合
space = interior_lib["space_types"]["living_room"]
layout = interior_lib["furniture_layouts"]["linear_sofa"]  # 中古风常用简洁线性布局
atmosphere = interior_lib["spatial_atmospheres"]["cozy_warm"]  # 温馨舒适
material_combo = interior_lib["material_combinations"]["wood_stone_mix"]  # 木石结合
design_element = interior_lib["design_elements"]["statement_lighting"]  # 特色灯具（中古风标志）

# 光照
lighting = common_lib["interior_lighting_scenarios"]["afternoon_warm"]

# 摄影技术
camera_angle = common_lib["camera_angles"]["eye_level_close_up"]
wide_lens = common_lib["photography_techniques"]["wide_angle_24mm"]

print("🎨 中古风特征选择:")
print(f"  • 空间: {space['chinese_name']}")
print(f"  • 布局: {layout['chinese_name']} (简洁线性)")
print(f"  • 氛围: {atmosphere['chinese_name']}")
print(f"  • 材质: {material_combo['chinese_name']}")
print(f"  • 灯具: {design_element['chinese_name']} (中古风标志性设计)")
print(f"  • 光照: {lighting['chinese_name']}")
print(f"  • 地板: 人字纹木地板 (herringbone pattern)")

print("\n" + "-"*80)
print("生成的完整提示词:\n")

# 组合提示词
prompt_parts = []

# 1. 核心风格描述（手动添加中古风）
prompt_parts.append("mid-century modern interior design")
prompt_parts.append("1950s-1960s aesthetic")
prompt_parts.append("retro-modern fusion")

# 2. 空间和布局
prompt_parts.append(space['ai_prompt_template'])
prompt_parts.append(layout['ai_prompt_template'])

# 3. 地板特征（人字纹木地板 - 手动添加）
prompt_parts.append("warm walnut herringbone wood flooring")
prompt_parts.append("chevron pattern wooden floor")
prompt_parts.append("natural wood grain in geometric arrangement")

# 4. 家具特征（中古风特点）
prompt_parts.append("tapered wooden legs furniture")
prompt_parts.append("low-profile sleek sofa")
prompt_parts.append("iconic mid-century armchair")

# 5. 材质和颜色
prompt_parts.append(material_combo['ai_prompt_template'])
prompt_parts.append("warm wood tones with neutral palette")
prompt_parts.append("teak and walnut wood accents")

# 6. 设计元素
prompt_parts.append(design_element['ai_prompt_template'])
prompt_parts.append("sputnik chandelier or arc floor lamp")
prompt_parts.append("geometric patterns and organic shapes")

# 7. 氛围
prompt_parts.append(atmosphere['ai_prompt_template'])
prompt_parts.append("nostalgic yet timeless atmosphere")

# 8. 光照
prompt_parts.append(lighting['ai_prompt_template'])
prompt_parts.append("natural_window_light")

# 9. 摄影技术
prompt_parts.append(wide_lens['ai_prompt_template'])
prompt_parts.append("clean architectural photography")

# 10. 质量标签
prompt_parts.append("8K interior photography")
prompt_parts.append("architectural digest quality")
prompt_parts.append("professional real estate photography")
prompt_parts.append("mid-century modern showcase")

combined_prompt = ", ".join(prompt_parts)
print(combined_prompt)

# 保存结果
output_file = Path(__file__).parent / "generated_midcentury_living_room.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# 中古风客厅生成结果\n")
    f.write("# Mid-century Modern Living Room with Herringbone Flooring\n\n")
    f.write("## 风格特点\n")
    f.write("- 1950-1960年代美学\n")
    f.write("- 人字纹木地板（胡桃木色调）\n")
    f.write("- 锥形木腿家具\n")
    f.write("- 标志性中古风灯具（卫星吊灯或弧形落地灯）\n")
    f.write("- 温暖木色 + 中性色调\n")
    f.write("- 几何图案与有机形状结合\n\n")
    f.write("## AI提示词\n\n")
    f.write(combined_prompt + "\n\n")
    f.write("-"*80 + "\n\n")
    f.write("## 使用建议\n")
    f.write("- 适用于 Midjourney, Stable Diffusion, DALL-E 等AI图像生成工具\n")
    f.write("- 可根据需要调整提示词权重\n")
    f.write("- 建议配合参考图使用以获得更精准的效果\n")

print("\n" + "="*80)
print("  ✅ 提示词已生成并保存")
print("="*80 + "\n")
print(f"📁 文件位置: {output_file}")

print("\n" + "="*80)
print("  💡 中古风设计要点")
print("="*80 + "\n")
print("✨ 家具特征:")
print("  • 细锥形木腿（tapered legs）")
print("  • 低矮线性设计")
print("  • Eames、Saarinen等经典设计")
print("\n✨ 色彩搭配:")
print("  • 木色：胡桃木、柚木")
print("  • 主色：米白、灰绿、芥末黄、橘红")
print("  • 中性背景 + 活力点缀色")
print("\n✨ 标志性元素:")
print("  • 人字纹木地板")
print("  • 卫星吊灯/弧形落地灯")
print("  • 几何图案地毯")
print("  • 有机形状装饰")
print("  • 开放式书架")

print("\n" + "="*80 + "\n")
