#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动提取的高质量特征 - Wes Anderson风格少女肖像
基于new_training_prompt.txt
"""

# 这些是从prompt中手动识别的高价值特征
# 可以直接添加到库中

manual_features = {
    "gestures": {
        "praying_hands_interlocked": {
            "chinese_name": "祈祷手势（手指交叉）",
            "keywords": [
                "praying hands",
                "prayer hands",
                "fingers interlocked",
                "fingers crossed",
                "clasped hands",
                "hands clasped into fists"
            ],
            "visual_features": {
                "hand_position": "fingers tightly interlocked and crossed",
                "fist_formation": "clasped into fists",
                "placement": "in front of chest, partially covering mouth",
                "key_detail": "ten fingers visibly crossed and gripping"
            },
            "ai_prompt_template": "praying hands with fingers tightly interlocked and crossed, clasped into fists",
            "reusability_score": 7.5,
            "usage_notes": "区别于简单的合掌：这是手指交叉紧握成拳的祈祷姿势"
        }
    },

    "hair_styles": {
        "twin_buns_space_buns": {
            "chinese_name": "双丸子头（太空发髻）",
            "keywords": [
                "twin buns",
                "space buns",
                "high twin buns",
                "double buns",
                "symmetrical high buns"
            ],
            "visual_features": {
                "count": "two buns",
                "position": "high on head, symmetrical",
                "shape": "vertical neat buns pointing upward",
                "style": "space buns hairstyle"
            },
            "ai_prompt_template": "symmetrical high twin buns hairstyle, space buns, two high vertical neat buns",
            "reusability_score": 8.5,
            "suitable_styles": ["cute", "playful", "youthful", "anime-inspired"]
        }
    },

    "hair_colors": {
        "platinum_blonde": {
            "chinese_name": "铂金色金发",
            "keywords": [
                "platinum blonde",
                "platinum-blonde hair",
                "shimmering platinum",
                "very light blonde"
            ],
            "visual_features": {
                "tone": "very light, almost white-blonde",
                "quality": "shimmering, lustrous",
                "undertones": "cool, silvery"
            },
            "ai_prompt_template": "shimmering platinum-blonde hair",
            "reusability_score": 8.0,
            "color_codes": ["#F0EAD6", "#FAFAD2", "#E8D5C4"]
        },

        "blonde_hair": {
            "chinese_name": "金发",
            "keywords": [
                "blonde hair",
                "blonde",
                "golden hair",
                "fair hair"
            ],
            "visual_features": {
                "tone": "light to medium blonde",
                "quality": "natural blonde tones"
            },
            "ai_prompt_template": "blonde hair",
            "reusability_score": 9.5
        }
    },

    "expressions": {
        "playful_shy_smile": {
            "chinese_name": "俏皮害羞微笑",
            "keywords": [
                "playful shy smile",
                "coy smile",
                "shy giggling",
                "adorable smile",
                "playful shy coy"
            ],
            "visual_features": {
                "mouth": "playful shy coy smile",
                "eyes": "sparkling, slightly pleading",
                "overall_mood": "playful, shy, charming, adorable"
            },
            "ai_prompt_template": "playful shy coy smile with adorable giggling expression",
            "emotional_tone": "positive, playful, innocent",
            "reusability_score": 8.5
        }
    },

    "gaze_directions": {
        "looking_up_pleading": {
            "chinese_name": "仰视恳求目光",
            "keywords": [
                "looking up",
                "gazing up",
                "upward gaze",
                "pleading eyes",
                "begging look"
            ],
            "visual_features": {
                "direction": "looking upward at viewer",
                "emotion": "pleading, begging, innocent",
                "eyes": "big sparkling eyes looking up"
            },
            "ai_prompt_template": "looking up with pleading eyes, upward gaze",
            "reusability_score": 8.0,
            "impact": "creates innocent, vulnerable, charming mood"
        }
    },

    "accessories": {
        "oversized_round_glasses_pink": {
            "chinese_name": "大号圆形粉色渐变眼镜",
            "keywords": [
                "oversized round glasses",
                "pink gradient glasses",
                "tinted glasses",
                "large round glasses",
                "pink-gradient acetate glasses"
            ],
            "visual_features": {
                "size": "large oversized",
                "shape": "round",
                "color": "transparent pink-gradient tinted",
                "material": "acetate with soft pink sheen frame"
            },
            "ai_prompt_template": "large oversized round transparent pink-gradient tinted acetate glasses with soft pink sheen frame",
            "reusability_score": 7.0,
            "style": "trendy, kawaii, fashion-forward"
        },

        "glasses": {
            "chinese_name": "眼镜",
            "keywords": [
                "glasses",
                "eyeglasses",
                "spectacles"
            ],
            "visual_features": {
                "type": "eyewear accessory"
            },
            "ai_prompt_template": "wearing glasses",
            "reusability_score": 9.0
        }
    },

    "body_types": {
        "petite_hourglass": {
            "chinese_name": "娇小沙漏身材",
            "keywords": [
                "petite",
                "hourglass figure",
                "very short stature",
                "tiny frame",
                "wide hips",
                "full bust"
            ],
            "visual_features": {
                "height": "very short stature, petite",
                "proportions": "hourglass with wide hips and full bust",
                "overall": "dramatically exaggerated voluptuous curves on tiny frame"
            },
            "ai_prompt_template": "very petite short stature with hourglass figure, dramatically exaggerated voluptuous wide hips and full bust",
            "reusability_score": 7.5
        }
    },

    "skin_tones": {
        "fair_skin": {
            "chinese_name": "白皙肤色",
            "keywords": [
                "fair skin",
                "fair complexion",
                "light skin",
                "pale skin"
            ],
            "visual_features": {
                "tone": "fair, light",
                "quality": "smooth, youthful"
            },
            "ai_prompt_template": "fair skin",
            "reusability_score": 9.0
        }
    },

    "clothing_styles": {
        "layered_casual_cute": {
            "chinese_name": "分层休闲可爱装",
            "keywords": [
                "layered outfit",
                "inner shirt outer sweater",
                "cute casual layers",
                "striped shirt and sweater"
            ],
            "visual_features": {
                "layers": "inner white shirt with light gray vertical stripes + outer pink round-neck wool sweater",
                "details": "collar featuring small cute cartoon patterns",
                "fit": "tight-fitting, hugging curves"
            },
            "ai_prompt_template": "wearing inner white shirt with light gray vertical stripes (collar featuring small cute cartoon patterns), outer pink round-neck fine vertical stripe wool sweater",
            "occasion": "casual, everyday, cute",
            "reusability_score": 7.0
        }
    },

    "visual_styles": {
        "wes_anderson_aesthetic": {
            "chinese_name": "韦斯·安德森美学",
            "keywords": [
                "Wes Anderson style",
                "Wes Anderson aesthetic",
                "Wes Anderson inspired",
                "flat aesthetic",
                "symmetrical composition"
            ],
            "visual_features": {
                "composition": "perfect symmetrical centered",
                "color_palette": "low saturation soft pastels, pinks blues yellows",
                "mood": "dreamy, vintage analog, sweet nostalgic",
                "framing": "flat aesthetic, rule of thirds"
            },
            "ai_prompt_template": "dreamy Wes Anderson inspired flat aesthetic, low saturation soft pastel color palette dominant pinks blues yellows, vintage analog sweet nostalgic mood, perfect symmetrical centered composition",
            "reusability_score": 8.0,
            "reference_films": ["The Grand Budapest Hotel", "Moonrise Kingdom"]
        }
    }
}

# 统计
print("\n" + "="*80)
print("📋 手动提取的高质量特征")
print("="*80 + "\n")

total_features = 0
for category, features in manual_features.items():
    print(f"【{category}】: {len(features)} 个")
    total_features += len(features)
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  - {code}: {cn_name} (复用性: {score}/10)")

print(f"\n总计: {total_features} 个高质量特征")
print("\n" + "="*80)

# 按重要性分组
print("\n📊 按重要性分组:")
print("="*80 + "\n")

high_priority = ["gestures", "hair_styles", "gaze_directions", "expressions"]
medium_priority = ["hair_colors", "body_types", "visual_styles", "clothing_styles"]
low_priority = ["accessories", "skin_tones"]

print("🔴 高优先级（核心新类别/特征）:")
for cat in high_priority:
    if cat in manual_features:
        features = manual_features[cat]
        print(f"  • {cat}: {', '.join(features.keys())}")

print("\n🟡 中优先级（增强类别）:")
for cat in medium_priority:
    if cat in manual_features:
        features = manual_features[cat]
        print(f"  • {cat}: {', '.join(features.keys())}")

print("\n🟢 低优先级（已有类别的扩充）:")
for cat in low_priority:
    if cat in manual_features:
        features = manual_features[cat]
        print(f"  • {cat}: {', '.join(features.keys())}")

print("\n" + "="*80)
print("\n💡 建议:")
print("  1. 高优先级特征建议全部添加（填补类别空白）")
print("  2. 中优先级特征根据需求选择")
print("  3. 低优先级特征可选（已有相似特征）")
print("\n  如果要添加这些特征，可以：")
print("  • 全部添加: python3 add_manual_features.py --all")
print("  • 只添加高优先级: python3 add_manual_features.py --high")
print("  • 交互式选择: python3 add_manual_features.py --interactive")
print()
