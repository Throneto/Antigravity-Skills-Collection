#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成现代时尚杂志风格prompt
使用v1.7特征库（包括poses, expressions, clothing_styles）
"""

import json
from pathlib import Path

# 加载特征库
SCRIPT_DIR = Path(__file__).parent
FACIAL_FEATURES = SCRIPT_DIR / "extracted_results" / "facial_features_library.json"

with open(FACIAL_FEATURES, 'r', encoding='utf-8') as f:
    library = json.load(f)

print("\n" + "="*80)
print("📸 现代时尚杂志风格 - Fashion Magazine Prompt生成器")
print("="*80 + "\n")

# 版本信息
version = library.get("library_metadata", {}).get("version", "unknown")
total = library.get("library_metadata", {}).get("total_classifications", 0)
print(f"📚 使用特征库: v{version} ({total}个分类)\n")

# ====================
# 1. 基础设定
# ====================
print("【1/7】基础设定")
print("-" * 80)

# 性别
gender = library.get("gender", {}).get("female", {})
gender_term = "stunning young woman"
print(f"✓ 性别: {gender.get('chinese_name', '女性')}")

# 年龄 - 时尚杂志通常用青年模特
age_range = library.get("age_range", {}).get("young_adult", {})
print(f"✓ 年龄: {age_range.get('chinese_name', '青年')} ({age_range.get('age_range', '18-25')})")

# 人种 - 可以是任何人种，这里选东亚（符合用户之前的偏好）
ethnicity = library.get("ethnicity", {}).get("east_asian", {})
ethnicity_keywords = ethnicity.get("keywords", ["Asian"])
print(f"✓ 人种: {ethnicity.get('chinese_name', '东亚人')}")

# ====================
# 2. 面部特征（时尚高级感）
# ====================
print("\n【2/7】面部特征（时尚高级）")
print("-" * 80)

# 眼睛 - 选择大眼（时尚感强）
eye_types = library.get("eye_types", {})
eye_type = eye_types.get("large_blue_realistic", {})
if not eye_type:
    eye_type = eye_types.get("phoenix_elegant", {})
if not eye_type and eye_types:
    eye_type = list(eye_types.values())[0]
eye_keywords = eye_type.get("keywords", ["striking eyes"])
print(f"✓ 眼型: {eye_type.get('chinese_name', '迷人大眼')}")

# 脸型 - 高颧骨棱角脸（时尚模特感）
face_shapes = library.get("face_shapes", {})
face_shape = face_shapes.get("high_cheekbone_angular", {})
if not face_shape:
    face_shape = face_shapes.get("refined_oval", {})
if not face_shape and face_shapes:
    face_shape = list(face_shapes.values())[0]
face_keywords = face_shape.get("keywords", ["sculpted face"])
print(f"✓ 脸型: {face_shape.get('chinese_name', '高级脸型')}")

# 皮肤 - 光滑质感
skin_textures = library.get("skin_textures", {})
skin_tone = skin_textures.get("photorealistic_texture", {})
if not skin_tone:
    skin_tones = library.get("skin_tones", {})
    skin_tone = skin_tones.get("porcelain_skin", {})
if not skin_tone and skin_textures:
    skin_tone = list(skin_textures.values())[0]
skin_keywords = skin_tone.get("keywords", ["flawless skin"])
print(f"✓ 皮肤: {skin_tone.get('chinese_name', '完美肌肤')}")

# 妆容 - 专业时尚妆容
makeup_styles = library.get("makeup_styles", {})
makeup = makeup_styles.get("editorial_bold", {})
if not makeup:
    makeup = makeup_styles.get("commercial_polished", {})
if not makeup and makeup_styles:
    makeup = list(makeup_styles.values())[0]
if makeup:
    makeup_keywords = makeup.get("keywords", ["professional makeup"])
    print(f"✓ 妆容: {makeup.get('chinese_name', '时尚妆容')}")
else:
    makeup_keywords = ["professional editorial makeup"]
    print(f"✓ 妆容: 专业编辑妆容")

# ====================
# 3. 表情（时尚自信）
# ====================
print("\n【3/7】表情（v1.7新增 - 时尚自信）")
print("-" * 80)

expressions = library.get("expressions", {})
# 选择自信微笑（时尚杂志常用）
expression = expressions.get("confident_smirk", {})
if not expression:
    # 备选：俏皮微笑
    expression = expressions.get("playful_smile", {})
if not expression and expressions:
    expression = list(expressions.values())[0]

if expression:
    expr_keywords = expression.get("keywords", ["confident expression"])
    print(f"✓ 表情: {expression.get('chinese_name', '自信微笑')}")
    print(f"  情感: {expression.get('emotional_tone', 'confident')}")
    expr_template = expression.get("ai_prompt_template", "confident expression")
else:
    expr_keywords = ["confident", "fierce gaze"]
    expr_template = "confident fierce expression"
    print(f"✓ 表情: 自信凌厉")

# ====================
# 4. 姿势（时尚力量感）
# ====================
print("\n【4/7】姿势（v1.7新增 - 时尚power pose）")
print("-" * 80)

poses = library.get("poses", {})
# 选择力量站姿（时尚杂志封面常用）
pose = poses.get("power_stance", {})
if not pose:
    pose = poses.get("chin_raised", {})
if not pose:
    pose = poses.get("arms_crossed", {})
if not pose and poses:
    pose = list(poses.values())[0]

if pose:
    print(f"✓ 姿势: {pose.get('chinese_name', '力量站姿')}")
    pose_template = pose.get("ai_prompt_template", "confident power pose")
else:
    pose_template = "standing tall, confident power stance"
    print(f"✓ 姿势: 自信力量站姿")

# ====================
# 5. 服装风格（现代时尚）
# ====================
print("\n【5/7】服装风格（v1.7新增 - 现代时尚）")
print("-" * 80)

clothing_styles = library.get("clothing_styles", {})
# 优先选择优雅正装或现代休闲
clothing = clothing_styles.get("elegant_formal", {})
if not clothing:
    clothing = clothing_styles.get("casual_modern", {})
if not clothing and clothing_styles:
    clothing = list(clothing_styles.values())[0]

if clothing:
    print(f"✓ 服装: {clothing.get('chinese_name', '时尚服装')}")
    clothing_template = clothing.get("ai_prompt_template", "wearing elegant modern outfit")
    # 具体化为时尚单品
    clothing_desc = "wearing haute couture designer outfit, tailored blazer, minimalist elegant design"
else:
    clothing_desc = "wearing high-fashion designer clothing, elegant tailored fit"
    print(f"✓ 服装: 高级定制时装")

# ====================
# 6. 时尚杂志风格元素
# ====================
print("\n【6/7】时尚杂志风格元素")
print("-" * 80)

fashion_magazine_elements = {
    "color_palette": "clean color palette, high contrast, monochromatic tones",
    "lighting": "professional studio lighting, crisp clean light, soft fill, beauty dish",
    "composition": "vertical magazine cover composition, negative space, rule of thirds",
    "mood": "sophisticated, confident, modern elegance, high-fashion",
    "background": "seamless backdrop, minimal clean background, pure white or grey",
    "photography": "shot on Hasselblad H6D-100c, 80mm f/2.8 lens, medium format",
    "quality": "ultra-high resolution, sharp focus, professional retouching, Vogue style",
    "style": "editorial fashion photography, commercial beauty shot"
}

print("✓ 色彩: 干净配色，高对比度，单色调")
print("✓ 光线: 专业影棚灯光，清晰干净")
print("✓ 构图: 垂直杂志封面构图，留白")
print("✓ 氛围: 精致、自信、现代优雅")
print("✓ 背景: 无缝背景，极简干净")
print("✓ 摄影: Hasselblad中画幅相机")
print("✓ 风格: Vogue/Harper's Bazaar编辑摄影")

# ====================
# 7. 组装最终Prompt
# ====================
print("\n【7/7】组装最终Prompt")
print("-" * 80 + "\n")

# 构建prompt各部分
parts = []

# Part 1: 主体描述
subject = f"A {gender_term}, professional fashion model"
parts.append(subject)

# Part 2: 人种（时尚杂志风格）
if ethnicity_keywords:
    parts.append(ethnicity_keywords[0])

# Part 3: 面部特征
facial_features = ", ".join([
    ", ".join(face_keywords[:2]),
    ", ".join(eye_keywords[:2]),
    ", ".join(skin_keywords[:2])
])
parts.append(facial_features)

# Part 4: 妆容
if makeup_keywords:
    parts.append(", ".join(makeup_keywords[:2]))

# Part 5: 表情
parts.append(expr_template)

# Part 6: 姿势
parts.append(pose_template)

# Part 7: 服装
parts.append(clothing_desc)

# Part 8: 时尚杂志元素
parts.append(fashion_magazine_elements["background"])
parts.append(fashion_magazine_elements["lighting"])
parts.append(fashion_magazine_elements["composition"])
parts.append(fashion_magazine_elements["color_palette"])
parts.append(fashion_magazine_elements["mood"])
parts.append(fashion_magazine_elements["style"])

# Part 9: 技术参数
parts.append(fashion_magazine_elements["photography"])
parts.append(fashion_magazine_elements["quality"])

# 组合
final_prompt = ", ".join(parts)

# ====================
# 输出结果
# ====================
print("✨ 最终生成的Prompt:")
print("="*80)
print("\033[92m")  # 绿色
print(final_prompt)
print("\033[0m")   # 重置颜色
print("="*80)

# 输出使用建议
print("\n💡 使用建议:")
print("-" * 80)
print("1. 复制上面的绿色prompt文本")
print("2. 粘贴到图像生成工具（Midjourney, Stable Diffusion, DALL-E等）")
print("\n3. 根据杂志类型调整风格：")
print("   【Vogue】: + 'Vogue magazine cover, high fashion editorial'")
print("   【Harper's Bazaar】: + 'sophisticated elegance, timeless beauty'")
print("   【Elle】: + 'modern chic, contemporary style'")
print("   【Marie Claire】: + 'accessible elegance, confident femininity'")
print("\n4. 调整背景颜色：")
print("   - 纯白背景: 'pure white seamless backdrop' (当前)")
print("   - 灰色背景: 'soft grey studio backdrop'")
print("   - 彩色背景: 'bold red backdrop' / 'pastel pink background'")
print("\n5. 调整服装风格：")
print("   - 正装: 'tailored power suit, minimalist' (专业)")
print("   - 高定: 'haute couture evening gown' (奢华)")
print("   - 街头: 'designer streetwear, urban chic' (现代)")
print("\n6. 添加配饰（可选）：")
print("   + 'statement jewelry, designer accessories'")
print("   + 'luxury handbag, high-end fashion accessories'")
print("\n" + "="*80 + "\n")

# 保存到文件
output_file = SCRIPT_DIR / "generated_fashion_magazine_prompt.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_prompt)

print(f"📁 Prompt已保存到: {output_file}\n")

# 额外：生成3个变体
print("🎨 生成3个快速变体供选择:")
print("="*80 + "\n")

variants = [
    {
        "name": "【变体1】Vogue封面风格",
        "additions": "Vogue magazine cover style, iconic fashion photography, bold typography space"
    },
    {
        "name": "【变体2】黑白经典风格",
        "additions": "black and white editorial, timeless classic photography, dramatic contrast"
    },
    {
        "name": "【变体3】色彩时尚风格",
        "additions": "vibrant color blocking, bold fashion statement, contemporary pop aesthetics"
    }
]

for i, variant in enumerate(variants, 1):
    print(f"{variant['name']}:")
    print(f"{final_prompt}, {variant['additions']}")
    print()

print("="*80 + "\n")
