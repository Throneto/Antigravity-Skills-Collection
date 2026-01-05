#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例342手动特征提取
日本街头摄影风格 - 小酒吧场景
"""

# 从中文prompt中手动识别的高价值特征
case_342_features = {
    "hair_styles": {
        "ponytail_with_bangs": {
            "chinese_name": "齐刘海马尾辫",
            "keywords": [
                "ponytail with bangs",
                "straight bangs ponytail",
                "ponytail and fringe",
                "bangs with tied hair"
            ],
            "visual_features": {
                "main_style": "straight hair tied in ponytail",
                "bangs": "straight bangs (齐刘海) framing the face",
                "hair_color": "chestnut brown"
            },
            "ai_prompt_template": "chestnut brown straight hair in ponytail with straight bangs framing face",
            "reusability_score": 9.0,
            "suitable_styles": ["neat", "professional", "youthful", "Asian aesthetic"]
        }
    },

    "makeup_styles": {
        "oxygen_fresh_natural": {
            "chinese_name": "氧气妆（清新自然妆）",
            "keywords": [
                "oxygen fresh makeup",
                "natural dewy makeup",
                "fresh clean makeup",
                "barely-there makeup",
                "translucent base"
            ],
            "visual_features": {
                "base": "translucent dewy foundation (半透明露珠底妆)",
                "eyes": "barely visible eyeliner, soft straight brows",
                "cheeks": "subtle rose blush",
                "highlight": "inner corner highlight for bright transparent eyes",
                "lips": "clean bright red, non-greasy"
            },
            "ai_prompt_template": "oxygen fresh natural makeup with translucent dewy base, barely visible eyeliner, soft straight brows, subtle rose blush, inner eye corner highlight, clean bright red lips",
            "makeup_details": {
                "coverage": "light to medium",
                "finish": "dewy, fresh",
                "emphasis": "natural skin texture with subtle glow",
                "mood": "fresh, clean, youthful"
            },
            "reusability_score": 8.5,
            "cultural_note": "Popular in Asian beauty trends, emphasizes natural fresh look"
        }
    },

    "poses": {
        "seated_knees_together_hands_crossed": {
            "chinese_name": "端坐姿（双膝并拢，手交叉）",
            "keywords": [
                "seated with knees together",
                "sitting primly",
                "hands crossed on lap",
                "proper sitting posture",
                "elegant seated pose"
            ],
            "visual_features": {
                "legs": "knees together, ankles slightly bent back",
                "torso": "slightly leaning forward from hips",
                "arms": "forearms relaxed",
                "hands": "gloved hands gently overlapping on small glass between knees",
                "head": "chin slightly lowered, looking straight at camera"
            },
            "ai_prompt_template": "sitting on narrow wooden bench with knees together, torso slightly forward from hips, gloved hands gently crossed holding glass between knees, chin slightly lowered, direct gaze",
            "posture_qualities": ["poised", "refined", "calm", "elegant"],
            "reusability_score": 8.0,
            "suitable_contexts": ["formal portraits", "vintage photography", "character studies"]
        }
    },

    "visual_styles": {
        "1980s_japanese_street_photography": {
            "chinese_name": "1980年代日本街头摄影风格",
            "keywords": [
                "1980s Japanese street photography",
                "Nobuyoshi Araki style",
                "Daido Moriyama aesthetic",
                "vintage analog snapshot",
                "retro Japanese photography"
            ],
            "visual_features": {
                "lighting": "warm incandescent with nostalgic amber tones",
                "colors": "low saturation, desaturated palette",
                "texture": "fine 35mm film grain",
                "exposure": "slightly overexposed highlights",
                "composition": "candid framing, intimate eye-level perspective",
                "mood": "nostalgic, intimate, documentary"
            },
            "technical_specs": {
                "focal_length": "classic 35mm feeling",
                "aspect_ratio": "3:4 vertical portrait",
                "depth_of_field": "shallow",
                "color_grading": "cinematic, amber-toned"
            },
            "ai_prompt_template": "1980s analog snapshot aesthetic, warm incandescent nostalgic amber tones, low saturation colors, fine 35mm film grain texture, slightly overexposed highlights, vintage Japanese street photography style, Nobuyoshi Araki and Daido Moriyama inspired, candid composition, shallow depth of field, cinematic color grading",
            "reference_photographers": ["Nobuyoshi Araki (荒木経惟)", "Daido Moriyama (森山大道)"],
            "reusability_score": 8.5,
            "cultural_context": "Classic Japanese documentary photography aesthetic"
        }
    },

    "clothing_styles": {
        "japanese_police_uniform_female": {
            "chinese_name": "日本女警制服",
            "keywords": [
                "Japanese police uniform",
                "female officer uniform",
                "light blue police shirt",
                "navy skirt uniform"
            ],
            "visual_features": {
                "top": "fitted light blue police uniform shirt with gold buttons and badges",
                "tie": "deep green flat ribbon tie knotted at collar with short tails like gift bow",
                "bottom": "navy blue skirt with dark belt and brass buckle",
                "accessories": "white gloves, black shoes"
            },
            "ai_prompt_template": "wearing fitted light blue police uniform shirt with gold buttons and badges, deep green flat ribbon tie knotted at collar with short tails hanging like gift bow, navy blue skirt, dark belt with brass buckle, white gloves, black shoes",
            "occasion": "formal, professional, uniform",
            "reusability_score": 6.5,
            "cultural_specific": True,
            "note": "Very specific to Japanese police aesthetic"
        }
    },

    "gaze_directions": {
        "direct_gaze_chin_lowered": {
            "chinese_name": "低头直视（下巴微垂直视镜头）",
            "keywords": [
                "chin slightly lowered",
                "looking straight at camera",
                "direct gaze with lowered chin",
                "eyes up while chin down"
            ],
            "visual_features": {
                "head": "chin slightly lowered",
                "eyes": "looking directly at camera/viewer",
                "effect": "creates intimate, engaging connection"
            },
            "ai_prompt_template": "chin slightly lowered, direct gaze at camera",
            "reusability_score": 8.5,
            "impact": "Creates vulnerable yet confident connection with viewer"
        }
    },

    "accessories": {
        "white_gloves": {
            "chinese_name": "白手套",
            "keywords": [
                "white gloves",
                "gloved hands",
                "formal white gloves"
            ],
            "visual_features": {
                "color": "white",
                "material": "formal dress gloves",
                "style": "classic, elegant"
            },
            "ai_prompt_template": "wearing white gloves",
            "reusability_score": 7.5,
            "suitable_contexts": ["formal wear", "uniforms", "vintage fashion", "elegant portraits"]
        }
    },

    "hair_colors": {
        "chestnut_brown": {
            "chinese_name": "栗色（栗棕色）",
            "keywords": [
                "chestnut brown",
                "chestnut hair",
                "warm brown hair",
                "brown hair"
            ],
            "visual_features": {
                "tone": "warm brown with reddish undertones",
                "quality": "natural, rich"
            },
            "ai_prompt_template": "chestnut brown hair",
            "reusability_score": 8.5,
            "color_codes": ["#8B4513", "#A0522D", "#CD853F"]
        }
    }
}

# 统计
print("\n" + "="*80)
print("📋 案例342手动提取的特征")
print("="*80 + "\n")

total_features = 0
for category, features in case_342_features.items():
    print(f"【{category}】: {len(features)} 个")
    total_features += len(features)
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  - {code}: {cn_name} (复用性: {score}/10)")

print(f"\n总计: {total_features} 个特征")
print("\n" + "="*80)

# 按优先级分组
print("\n📊 按优先级和新颖性分组:")
print("="*80 + "\n")

print("🔴 高优先级 - 高复用性通用特征:")
print("  • hair_styles/ponytail_with_bangs (9.0/10) - 齐刘海马尾")
print("  • makeup_styles/oxygen_fresh_natural (8.5/10) - 氧气妆")
print("  • gaze_directions/direct_gaze_chin_lowered (8.5/10) - 低头直视")
print("  • hair_colors/chestnut_brown (8.5/10) - 栗色")
print("  • visual_styles/1980s_japanese_street_photography (8.5/10) - 日本街拍风格")

print("\n🟡 中优先级 - 实用特征:")
print("  • poses/seated_knees_together_hands_crossed (8.0/10) - 端坐姿")
print("  • accessories/white_gloves (7.5/10) - 白手套")

print("\n🟢 低优先级 - 特定场景:")
print("  • clothing_styles/japanese_police_uniform_female (6.5/10) - 日本女警制服（文化特定）")

print("\n" + "="*80)

print("\n💡 推荐添加:")
print("  建议添加高优先级的5个特征（复用性≥8.5）：")
print("  1. ponytail_with_bangs - 常见发型，亚洲风格")
print("  2. oxygen_fresh_natural - 流行妆容，亚洲美妆趋势")
print("  3. direct_gaze_chin_lowered - 经典摄影姿势")
print("  4. chestnut_brown - 常见发色")
print("  5. 1980s_japanese_street_photography - 独特视觉风格")

print("\n❓ 可选添加:")
print("  • seated_knees_together_hands_crossed - 正式坐姿")
print("  • white_gloves - 正式配饰")

print("\n❌ 不建议添加:")
print("  • japanese_police_uniform_female - 过于特定，复用性低")

print("\n" + "="*80)
print("\n✨ 这些特征的价值:")
print("  • 填补了亚洲美学gap（氧气妆、齐刘海等）")
print("  • 增加了vintage摄影风格支持")
print("  • 丰富了gaze_directions类别")
print("  • 提供了更多发型和妆容选择")
print()
