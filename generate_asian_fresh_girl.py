#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成亚洲清新少女风格prompt
使用v1.9特征库（氧气妆 + 齐刘海马尾）
"""

import json
from pathlib import Path

# 加载特征库
SCRIPT_DIR = Path(__file__).parent
FACIAL_FEATURES = SCRIPT_DIR / "extracted_results" / "facial_features_library.json"

with open(FACIAL_FEATURES, 'r', encoding='utf-8') as f:
    library = json.load(f)

print("\n" + "="*80)
print("🌸 亚洲清新少女风格 - Fresh Asian Girl Prompt生成器")
print("="*80 + "\n")

# 版本信息
version = library.get("library_metadata", {}).get("version", "unknown")
total = library.get("library_metadata", {}).get("total_classifications", 0)
print(f"📚 使用特征库: v{version} ({total}个分类)\n")

# ====================
# 1. 基础设定
# ====================
print("【1/8】基础设定（亚洲清新风格）")
print("-" * 80)

# 性别
gender = library.get("gender", {}).get("female", {})
gender_term = "a fresh youthful Asian girl"
print(f"✓ 性别: {gender.get('chinese_name', '女性')}")

# 年龄 - 青年
age_range = library.get("age_range", {}).get("young_adult", {})
print(f"✓ 年龄: {age_range.get('chinese_name', '青年')} ({age_range.get('age_range', '18-25')})")

# 人种 - 东亚
ethnicity = library.get("ethnicity", {}).get("east_asian", {})
ethnicity_keywords = ethnicity.get("keywords", ["East Asian"])
print(f"✓ 人种: {ethnicity.get('chinese_name', '东亚人')}")

# ====================
# 2. 发型（v1.9新增：齐刘海马尾）
# ====================
print("\n【2/8】发型（v1.9新增特征 ⭐）")
print("-" * 80)

hair_styles = library.get("hair_styles", {})
# 使用新增的齐刘海马尾
hair_style = hair_styles.get("ponytail_with_bangs", {})
if hair_style:
    print(f"✓ 发型: {hair_style.get('chinese_name', '齐刘海马尾辫')}")
    hair_template = hair_style.get("ai_prompt_template", "ponytail with bangs")
    print(f"  模板: {hair_template}")
else:
    hair_template = "long straight hair"
    print(f"✓ 发型: 长直发")

# 发色 - 使用新增的栗色
hair_colors = library.get("hair_colors", {})
hair_color = hair_colors.get("chestnut_brown", {})
if not hair_color:
    hair_color = hair_colors.get("black_hair", {})
if hair_color:
    print(f"✓ 发色: {hair_color.get('chinese_name', '栗色')}")
    hair_color_keywords = hair_color.get("keywords", ["chestnut brown"])
else:
    hair_color_keywords = ["dark brown"]
    print(f"✓ 发色: 深棕色")

# ====================
# 3. 妆容（v1.9新增：氧气妆）
# ====================
print("\n【3/8】妆容（v1.9新增特征 ⭐）")
print("-" * 80)

makeup_styles = library.get("makeup_styles", {})
# 使用新增的氧气妆
makeup = makeup_styles.get("oxygen_fresh_natural", {})
if makeup:
    print(f"✓ 妆容: {makeup.get('chinese_name', '氧气妆')}")
    makeup_template = makeup.get("ai_prompt_template", "natural fresh makeup")
    print(f"  特点: 半透明露珠底妆、内眼角高光、干净红唇")
    makeup_note = makeup.get("cultural_note", "")
    if makeup_note:
        print(f"  备注: {makeup_note}")
else:
    makeup_template = "natural fresh makeup"
    print(f"✓ 妆容: 自然清新妆")

# ====================
# 4. 面部特征（清新可爱）
# ====================
print("\n【4/8】面部特征（清新可爱）")
print("-" * 80)

# 眼睛 - 选择大眼杏仁眼
eye_types = library.get("eye_types", {})
eye_type = eye_types.get("large_almond_realistic", {})
if not eye_type:
    eye_type = list(eye_types.values())[0] if eye_types else {}
eye_keywords = eye_type.get("keywords", ["bright eyes"])
print(f"✓ 眼型: {eye_type.get('chinese_name', '杏仁大眼')}")

# 脸型 - 精致鹅蛋脸
face_shapes = library.get("face_shapes", {})
face_shape = face_shapes.get("refined_oval", {})
if not face_shape and face_shapes:
    face_shape = list(face_shapes.values())[0]
face_keywords = face_shape.get("keywords", ["delicate face"])
print(f"✓ 脸型: {face_shape.get('chinese_name', '鹅蛋脸')}")

# 皮肤
skin_tones = library.get("skin_tones", {})
skin_tone = skin_tones.get("porcelain_skin", {})
if not skin_tone:
    skin_tone = skin_tones.get("fair_skin", {})
if skin_tone:
    skin_keywords = skin_tone.get("keywords", ["fair skin"])
    print(f"✓ 肤色: {skin_tone.get('chinese_name', '白皙肤色')}")
else:
    skin_keywords = ["smooth fair skin"]
    print(f"✓ 肤色: 白皙光滑肌肤")

# ====================
# 5. 表情（清新甜美）
# ====================
print("\n【5/8】表情（清新甜美）")
print("-" * 80)

expressions = library.get("expressions", {})
# 选择温柔微笑或俏皮害羞微笑
expression = expressions.get("gentle_smile", {})
if not expression:
    expression = expressions.get("playful_shy_smile", {})
if not expression and expressions:
    expression = list(expressions.values())[0]

if expression:
    expr_keywords = expression.get("keywords", ["gentle smile"])
    print(f"✓ 表情: {expression.get('chinese_name', '温柔微笑')}")
    expr_template = expression.get("ai_prompt_template", "gentle smile")
else:
    expr_keywords = ["sweet smile"]
    expr_template = "sweet gentle smile"
    print(f"✓ 表情: 甜美微笑")

# ====================
# 6. 视线方向（v1.9增强）
# ====================
print("\n【6/8】视线方向（v1.9增强特征）")
print("-" * 80)

gaze_directions = library.get("gaze_directions", {})
# 可以使用looking_at_camera或新增的direct_gaze_chin_lowered
gaze = gaze_directions.get("looking_at_camera", {})
if not gaze:
    gaze = gaze_directions.get("direct_gaze_chin_lowered", {})
if gaze:
    print(f"✓ 视线: {gaze.get('chinese_name', '直视镜头')}")
    gaze_template = gaze.get("ai_prompt_template", "looking at camera")
else:
    gaze_template = "looking directly at camera with friendly gaze"
    print(f"✓ 视线: 友好直视镜头")

# ====================
# 7. 姿势（轻松自然）
# ====================
print("\n【7/8】姿势（轻松自然）")
print("-" * 80)

poses = library.get("poses", {})
# 选择放松站姿
pose = poses.get("relaxed_standing", {})
if not pose and poses:
    pose = list(poses.values())[0]

if pose:
    print(f"✓ 姿势: {pose.get('chinese_name', '放松站姿')}")
    pose_template = pose.get("ai_prompt_template", "relaxed natural pose")
else:
    pose_template = "standing naturally, relaxed pose"
    print(f"✓ 姿势: 自然放松站立")

# ====================
# 8. 服装风格（清新休闲）
# ====================
print("\n【8/8】服装风格（清新休闲）")
print("-" * 80)

clothing_styles = library.get("clothing_styles", {})
# 选择现代休闲装
clothing = clothing_styles.get("casual_modern", {})
if not clothing and clothing_styles:
    clothing = list(clothing_styles.values())[0]

if clothing:
    print(f"✓ 服装: {clothing.get('chinese_name', '现代休闲装')}")
    clothing_template = clothing.get("ai_prompt_template", "casual modern outfit")
else:
    clothing_template = "casual comfortable outfit"
    print(f"✓ 服装: 休闲舒适服装")

# 具体化为清新风格
clothing_desc = "wearing light pastel blue or white casual top, soft colors, comfortable fit"

# ====================
# 9. 清新少女风格元素
# ====================
print("\n【9/9】清新少女风格元素")
print("-" * 80)

fresh_girl_elements = {
    "mood": "fresh, youthful, innocent, approachable",
    "lighting": "soft natural daylight, bright and airy",
    "colors": "light pastel tones, soft pinks, blues, whites",
    "atmosphere": "bright, clean, positive energy",
    "background": "simple clean background, minimal distractions, soft bokeh",
    "photography": "natural light portrait, soft focus, shallow depth of field",
    "quality": "high resolution, professional photography, natural colors"
}

print("✓ 氛围: 清新、年轻、纯真、亲和")
print("✓ 光线: 柔和自然日光，明亮通透")
print("✓ 色彩: 浅色系，柔和粉蓝白")
print("✓ 背景: 简洁干净，柔和虚化")

# ====================
# 10. 组装最终Prompt
# ====================
print("\n【10/10】组装最终Prompt")
print("-" * 80 + "\n")

# 构建prompt各部分
parts = []

# Part 1: 主体描述
subject = gender_term
parts.append(subject)

# Part 2: 人种
if ethnicity_keywords:
    parts.append(ethnicity_keywords[0])

# Part 3: 面部特征
facial_features = ", ".join([
    ", ".join(face_keywords[:2]),
    ", ".join(eye_keywords[:2]),
    ", ".join(skin_keywords[:2])
])
parts.append(facial_features)

# Part 4: 发型（v1.9新特征）
parts.append(hair_template)

# Part 5: 妆容（v1.9新特征）
parts.append(makeup_template)

# Part 6: 表情
parts.append(expr_template)

# Part 7: 视线
parts.append(gaze_template)

# Part 8: 姿势
parts.append(pose_template)

# Part 9: 服装
parts.append(clothing_desc)

# Part 10: 清新风格元素
parts.append(fresh_girl_elements["mood"])
parts.append(fresh_girl_elements["lighting"])
parts.append(fresh_girl_elements["colors"])
parts.append(fresh_girl_elements["background"])

# Part 11: 技术参数
parts.append(fresh_girl_elements["photography"])
parts.append(fresh_girl_elements["quality"])

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
print("\n3. 可选调整：")
print("   【场景】:")
print("   + 'in a bright cafe' (明亮咖啡厅)")
print("   + 'outdoor park with cherry blossoms' (樱花公园)")
print("   + 'cozy bedroom with soft morning light' (温馨卧室)")
print("\n   【服装细节】:")
print("   - 'light blue knit sweater' (浅蓝针织衫)")
print("   - 'white cotton dress' (白色棉质连衣裙)")
print("   - 'pastel pink cardigan' (粉色开衫)")
print("\n   【配饰】:")
print("   + 'small delicate earrings' (精致小耳环)")
print("   + 'simple necklace' (简约项链)")
print("\n4. v1.9新特征亮点：")
print("   ✨ 氧气妆 - 半透明露珠底妆，内眼角高光")
print("   ✨ 齐刘海马尾 - 经典亚洲清新发型")
print("   ✨ 栗色发色 - 温暖自然的棕红色调")
print("\n" + "="*80 + "\n")

# 保存到文件
output_file = SCRIPT_DIR / "generated_asian_fresh_girl_prompt.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_prompt)

print(f"📁 Prompt已保存到: {output_file}\n")

# 额外：生成变体
print("🎨 生成3个场景变体供选择:")
print("="*80 + "\n")

variants = [
    {
        "name": "【变体1】樱花公园场景",
        "additions": "in a cherry blossom park, pink petals falling gently, spring atmosphere, dreamy soft focus"
    },
    {
        "name": "【变体2】明亮咖啡厅",
        "additions": "in a bright modern cafe, sitting by large window, natural sunlight streaming in, warm cozy atmosphere"
    },
    {
        "name": "【变体3】校园清新风",
        "additions": "on university campus, library or study area background, youthful student vibe, afternoon golden hour light"
    }
]

for i, variant in enumerate(variants, 1):
    print(f"{variant['name']}:")
    print(f"{final_prompt}, {variant['additions']}")
    print()

print("="*80)
print("\n🌸 对比：亚洲清新 vs 西方时尚")
print("-" * 80)
print("【亚洲清新风格】（当前）")
print("  • 氧气妆 - 强调自然透明感")
print("  • 齐刘海马尾 - 可爱减龄")
print("  • 柔和色调 - 粉蓝白浅色系")
print("  • 柔光摄影 - 明亮通透")
print("  • 氛围：纯真、亲和、清新")
print("\n【西方时尚风格】（参考：之前生成的时尚杂志风格）")
print("  • 专业妆容 - 强调轮廓和立体感")
print("  • 力量站姿 - 自信凌厉")
print("  • 高对比 - 黑白单色调")
print("  • 影棚光 - 清晰锐利")
print("  • 氛围：自信、高级、专业")
print("="*80 + "\n")
