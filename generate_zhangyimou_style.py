#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成张艺谋电影风格的传统中国女子prompt
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
print("🎬 张艺谋电影风格 - 传统中国女子 Prompt生成器")
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
gender_term = "beautiful young Chinese woman"
print(f"✓ 性别: {gender.get('chinese_name', '女性')}")

# 年龄
age_range = library.get("age_range", {}).get("young_adult", {})
print(f"✓ 年龄: {age_range.get('chinese_name', '青年')} ({age_range.get('age_range', '18-25')})")

# 人种
ethnicity = library.get("ethnicity", {}).get("east_asian", {})
ethnicity_keywords = ethnicity.get("keywords", ["Chinese"])
print(f"✓ 人种: {ethnicity.get('chinese_name', '东亚人')}")

# ====================
# 2. 面部特征
# ====================
print("\n【2/7】面部特征（传统东方美）")
print("-" * 80)

# 眼睛 - 选择凤眼（传统东方美）
eye_type = library.get("eye_types", {}).get("phoenix_elegant", {})
if not eye_type:
    eye_type = list(library.get("eye_types", {}).values())[0] if library.get("eye_types") else {}
eye_keywords = eye_type.get("keywords", ["expressive almond eyes"])
print(f"✓ 眼型: {eye_type.get('chinese_name', '凤眼')}")

# 脸型 - 精致鹅蛋脸
face_shape = library.get("face_shapes", {}).get("refined_oval", {})
if not face_shape:
    face_shape = list(library.get("face_shapes", {}).values())[0] if library.get("face_shapes") else {}
face_keywords = face_shape.get("keywords", ["delicate oval face"])
print(f"✓ 脸型: {face_shape.get('chinese_name', '鹅蛋脸')}")

# 皮肤 - 使用我们新添加的porcelain skin
skin_tones = library.get("skin_tones", {})
skin_tone = skin_tones.get("porcelain_skin", {})
if not skin_tone:
    # 备选
    skin_textures = library.get("skin_textures", {})
    skin_tone = skin_textures.get("photorealistic_texture", {})
skin_keywords = skin_tone.get("keywords", ["fair porcelain skin"])
print(f"✓ 肤色: {skin_tone.get('chinese_name', '瓷白肌肤')}")

# ====================
# 3. 表情（新增的expressions类别）
# ====================
print("\n【3/7】表情（v1.7新增）")
print("-" * 80)

expressions = library.get("expressions", {})
# 选择宁静平和的表情（符合张艺谋电影风格）
expression = expressions.get("serene_calm", {})
if not expression:
    # 使用我们新添加的gentle_smile
    expression = expressions.get("gentle_smile", {})
if not expression and expressions:
    expression = list(expressions.values())[0]

expr_keywords = expression.get("keywords", ["serene expression"])
print(f"✓ 表情: {expression.get('chinese_name', '宁静平和')}")
print(f"  情感: {expression.get('emotional_tone', 'peaceful')}")

# ====================
# 4. 姿势（新增的poses类别）
# ====================
print("\n【4/7】姿势（v1.7新增）")
print("-" * 80)

poses = library.get("poses", {})
# 选择优雅站姿
pose = poses.get("relaxed_standing", {})
if not pose:
    pose = poses.get("chin_raised", {})
if not pose and poses:
    pose = list(poses.values())[0]

pose_keywords = pose.get("keywords", ["standing gracefully"]) if pose else []
if pose:
    print(f"✓ 姿势: {pose.get('chinese_name', '优雅站姿')}")
    pose_template = pose.get("ai_prompt_template", "standing gracefully")
else:
    pose_template = "standing elegantly"
    print(f"✓ 姿势: 优雅站立")

# ====================
# 5. 服装风格（新增的clothing_styles类别）
# ====================
print("\n【5/7】服装风格（v1.7新增）")
print("-" * 80)

clothing_styles = library.get("clothing_styles", {})
# 选择传统文化装
clothing = clothing_styles.get("traditional_cultural", {})
if not clothing and clothing_styles:
    clothing = list(clothing_styles.values())[0]

if clothing:
    print(f"✓ 服装: {clothing.get('chinese_name', '传统服装')}")
    clothing_template = clothing.get("ai_prompt_template", "wearing traditional attire")
    # 添加具体的传统中国服装描述
    clothing_desc = "wearing exquisite traditional Chinese hanfu, deep red silk with gold embroidery, flowing sleeves"
else:
    clothing_desc = "wearing traditional Chinese red silk hanfu with intricate gold patterns"
    print(f"✓ 服装: 传统中国汉服")

# ====================
# 6. 张艺谋电影风格元素
# ====================
print("\n【6/7】张艺谋电影风格元素")
print("-" * 80)

zhangyimou_elements = {
    "color_palette": "rich saturated colors, deep crimson red, golden accents",
    "lighting": "dramatic cinematic lighting, soft rim light, atmospheric haze",
    "composition": "symmetric composition, rule of thirds, negative space",
    "mood": "poetic, contemplative, classical Chinese aesthetic",
    "cinematography": "shot on Arri Alexa, anamorphic lens, shallow depth of field",
    "quality": "8K resolution, HDR, film grain, cinematic color grading"
}

print("✓ 色彩: 浓郁饱和色彩，深红与金色")
print("✓ 光线: 戏剧性电影光线，柔和轮廓光")
print("✓ 构图: 对称构图，三分法则")
print("✓ 氛围: 诗意、沉思、古典中国美学")
print("✓ 摄影: Arri Alexa, 变形镜头")

# ====================
# 7. 组装最终Prompt
# ====================
print("\n【7/7】组装最终Prompt")
print("-" * 80 + "\n")

# 构建prompt各部分
parts = []

# Part 1: 主体描述
subject = f"A {gender_term}"
parts.append(subject)

# Part 2: 面部特征
facial_features = ", ".join([
    ", ".join(face_keywords[:2]),
    ", ".join(eye_keywords[:2]),
    ", ".join(skin_keywords[:2])
])
parts.append(facial_features)

# Part 3: 表情
if expr_keywords:
    parts.append(", ".join(expr_keywords[:2]))

# Part 4: 姿势
parts.append(pose_template)

# Part 5: 服装
parts.append(clothing_desc)

# Part 6: 张艺谋风格元素
parts.append(zhangyimou_elements["color_palette"])
parts.append(zhangyimou_elements["lighting"])
parts.append(zhangyimou_elements["composition"])
parts.append(zhangyimou_elements["mood"])

# Part 7: 技术参数
parts.append(zhangyimou_elements["cinematography"])
parts.append(zhangyimou_elements["quality"])

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
print("3. 根据需要调整：")
print("   - 修改服装颜色（深红 → 蓝色、绿色等张艺谋经典色调）")
print("   - 添加场景（bamboo forest, ancient palace, courtyard等）")
print("   - 调整表情（serene → determined, melancholic等）")
print("\n4. 张艺谋风格关键词参考：")
print("   《英雄》风格: + 'Hero movie style, martial arts aesthetic'")
print("   《大红灯笼高高挂》: + 'Raise the Red Lantern aesthetic, courtyard setting'")
print("   《满城尽带黄金甲》: + 'Curse of the Golden Flower style, imperial palace'")
print("\n" + "="*80 + "\n")

# 保存到文件
output_file = SCRIPT_DIR / "generated_zhangyimou_prompt.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_prompt)

print(f"📁 Prompt已保存到: {output_file}\n")
