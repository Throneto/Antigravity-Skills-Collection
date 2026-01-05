#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态视角肖像提示词分析
Dynamic Perspective Portrait - 强制透视效果
"""

# 从提示词模板中提取的高价值特征
dynamic_perspective_features = {
    "camera_angles": {
        "low_angle_worms_eye": {
            "chinese_name": "低角度仰视（虫眼视角）",
            "keywords": [
                "low angle",
                "worm's-eye view",
                "from below",
                "looking up at subject"
            ],
            "visual_features": {
                "angle": "camera positioned low, looking upward",
                "effect": "subject appears powerful, dominant, heroic",
                "distortion": "slight wide-angle distortion, dramatic perspective"
            },
            "ai_prompt_template": "shot from a low angle worm's-eye view using 24mm wide-angle lens",
            "reusability_score": 8.5,
            "suitable_for": ["power poses", "heroic shots", "dramatic portraits"]
        },

        "high_angle_birds_eye": {
            "chinese_name": "高角度俯视（鸟眼视角）",
            "keywords": [
                "high angle",
                "bird's-eye view",
                "from above",
                "looking down at subject"
            ],
            "visual_features": {
                "angle": "camera positioned high, looking downward",
                "effect": "subject appears vulnerable, intimate, smaller",
                "composition": "top-down perspective"
            },
            "ai_prompt_template": "shot from a high angle bird's-eye view using 24mm wide-angle lens",
            "reusability_score": 8.5,
            "suitable_for": ["intimate portraits", "vulnerable expressions", "creative angles"]
        },

        "eye_level_close_up": {
            "chinese_name": "平视特写",
            "keywords": [
                "eye-level",
                "close up",
                "face level",
                "direct view"
            ],
            "visual_features": {
                "angle": "camera at same height as subject's eyes",
                "effect": "natural, balanced, intimate connection",
                "framing": "close-up framing"
            },
            "ai_prompt_template": "shot from eye-level close up using 24mm wide-angle lens",
            "reusability_score": 9.0,
            "suitable_for": ["portraits", "natural connection", "standard shots"]
        },

        "dutch_angle_tilted": {
            "chinese_name": "荷兰角（倾斜视角）",
            "keywords": [
                "dutch angle",
                "tilted angle",
                "canted angle",
                "diagonal composition"
            ],
            "visual_features": {
                "angle": "camera tilted at diagonal angle",
                "effect": "dynamic, tension, unease or energy",
                "composition": "horizon line at angle"
            },
            "ai_prompt_template": "shot from a dutch angle (tilted) using 24mm wide-angle lens",
            "reusability_score": 7.5,
            "suitable_for": ["dynamic shots", "music videos", "energetic portraits"]
        }
    },

    "poses": {
        "deep_squatting": {
            "chinese_name": "深蹲姿势",
            "keywords": [
                "deep squatting",
                "crouching",
                "squatting pose",
                "low stance"
            ],
            "visual_features": {
                "legs": "bent deeply, squatting low",
                "balance": "weight centered, low to ground",
                "arms": "can be reaching forward or resting on knees"
            },
            "ai_prompt_template": "character in deep squatting pose, crouching low",
            "reusability_score": 7.5,
            "suitable_styles": ["street fashion", "hip-hop", "dynamic portraits"]
        },

        "standing_power_pose": {
            "chinese_name": "站立力量姿势",
            "keywords": [
                "standing power pose",
                "confident standing",
                "strong stance",
                "power stance"
            ],
            "visual_features": {
                "posture": "upright, chest out, shoulders back",
                "stance": "feet apart, grounded",
                "energy": "confident, powerful, commanding"
            },
            "ai_prompt_template": "character in standing power pose, confident and strong",
            "reusability_score": 9.0,
            "suitable_styles": ["fashion", "professional", "editorial"]
        },

        "sitting_cross_legged": {
            "chinese_name": "盘腿坐姿",
            "keywords": [
                "sitting cross-legged",
                "crossed legs sitting",
                "lotus position",
                "casual sitting"
            ],
            "visual_features": {
                "legs": "crossed in front, casual or lotus style",
                "posture": "relaxed or meditative",
                "placement": "on floor, bed, or low surface"
            },
            "ai_prompt_template": "character sitting cross-legged, casual relaxed pose",
            "reusability_score": 8.5,
            "suitable_styles": ["casual", "lifestyle", "relaxed portraits"]
        },

        "dynamic_running": {
            "chinese_name": "动态跑步姿势",
            "keywords": [
                "dynamic running",
                "running pose",
                "motion running",
                "active movement"
            ],
            "visual_features": {
                "motion": "mid-stride, one leg forward one back",
                "energy": "dynamic, active, energetic",
                "arms": "pumping in running motion"
            },
            "ai_prompt_template": "character in dynamic running pose, full of energy and movement",
            "reusability_score": 7.0,
            "suitable_styles": ["sports", "energetic", "action shots"]
        },

        "leaning_forward": {
            "chinese_name": "前倾姿势",
            "keywords": [
                "leaning forward",
                "body leaning",
                "forward lean",
                "bending towards camera"
            ],
            "visual_features": {
                "torso": "leaning forward from hips",
                "effect": "creates depth, engagement with viewer",
                "balance": "weight shifted forward"
            },
            "ai_prompt_template": "character leaning forward towards camera, engaging pose",
            "reusability_score": 8.5,
            "suitable_styles": ["interactive", "playful", "engaging portraits"]
        }
    },

    "photography_techniques": {
        "forced_perspective_hand": {
            "chinese_name": "强制透视（手部特写）",
            "keywords": [
                "forced perspective",
                "hand reaching to camera",
                "exaggerated depth",
                "foreshortening effect"
            ],
            "visual_features": {
                "composition": "hand or foot reaching towards lens",
                "scale": "limb appears larger due to proximity",
                "depth": "creates dramatic depth and playfulness",
                "focus": "sharp on face, hand in foreground"
            },
            "ai_prompt_template": "one hand reaching towards camera lens, creating playful forced perspective effect where the limb appears larger and close-up",
            "technical_specs": {
                "lens": "24mm wide-angle lens",
                "dof": "shallow depth of field",
                "focus": "sharp on eyes, soft background"
            },
            "reusability_score": 8.0,
            "suitable_styles": ["K-pop", "music video", "dynamic portraits", "social media"]
        },

        "wide_angle_24mm": {
            "chinese_name": "24mm广角镜头",
            "keywords": [
                "24mm lens",
                "wide-angle lens",
                "wide field of view",
                "slight distortion"
            ],
            "visual_features": {
                "field_of_view": "wide, captures more of scene",
                "distortion": "slight barrel distortion at edges",
                "depth": "exaggerated depth perception",
                "perspective": "dramatic perspective lines"
            },
            "ai_prompt_template": "shot using 24mm wide-angle lens",
            "reusability_score": 8.5,
            "technical_note": "Creates dynamic, immersive feel"
        }
    },

    "visual_styles": {
        "kpop_aesthetic": {
            "chinese_name": "K-pop美学风格",
            "keywords": [
                "K-pop aesthetic",
                "Korean pop style",
                "vibrant colors",
                "modern trendy",
                "idol photography"
            ],
            "visual_features": {
                "colors": "vibrant, saturated, bold",
                "lighting": "soft studio lighting, clean highlights",
                "style": "modern, trendy, polished",
                "texture": "realistic texture, high detail",
                "mood": "energetic, youthful, stylish"
            },
            "ai_prompt_template": "K-pop aesthetic, vibrant colors, realistic texture, 8k resolution, raw photography",
            "technical_specs": {
                "resolution": "8k",
                "style": "raw photography",
                "color_treatment": "vibrant, punchy"
            },
            "reusability_score": 8.0,
            "cultural_context": "Korean pop music industry visual style",
            "suitable_for": ["idol portraits", "music industry", "youth culture"]
        }
    }
}

# 统计和分析
print("\n" + "="*80)
print("📋 动态视角肖像（Dynamic Perspective Portrait）特征提取")
print("="*80 + "\n")

total_features = 0
for category, features in dynamic_perspective_features.items():
    print(f"【{category}】: {len(features)} 个")
    total_features += len(features)
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  - {code}: {cn_name} (复用性: {score}/10)")

print(f"\n总计: {total_features} 个特征")
print("\n" + "="*80)

# 按优先级分组
print("\n📊 按优先级和价值分组:")
print("="*80 + "\n")

print("🔴 高优先级 - 摄影技术核心（复用性≥8.5）:")
print("  • camera_angles/eye_level_close_up (9.0/10) - 平视特写")
print("  • camera_angles/low_angle_worms_eye (8.5/10) - 低角度仰视")
print("  • camera_angles/high_angle_birds_eye (8.5/10) - 高角度俯视")
print("  • poses/standing_power_pose (9.0/10) - 站立力量姿势（已有power_stance）")
print("  • poses/sitting_cross_legged (8.5/10) - 盘腿坐姿")
print("  • poses/leaning_forward (8.5/10) - 前倾姿势")
print("  • photography_techniques/wide_angle_24mm (8.5/10) - 24mm广角")

print("\n🟡 中高优先级 - 特色技术（复用性8.0-8.4）:")
print("  • photography_techniques/forced_perspective_hand (8.0/10) - 强制透视")
print("  • visual_styles/kpop_aesthetic (8.0/10) - K-pop美学")

print("\n🟢 中优先级 - 特定风格（复用性7.0-7.9）:")
print("  • camera_angles/dutch_angle_tilted (7.5/10) - 荷兰角")
print("  • poses/deep_squatting (7.5/10) - 深蹲姿势")
print("  • poses/dynamic_running (7.0/10) - 动态跑步")

print("\n" + "="*80)

print("\n💡 核心价值分析:")
print("  1. 【camera_angles】- 全新类别！")
print("     填补了相机角度控制的空白")
print("     提供4种专业摄影角度选择")
print("     这是COMPLETE_CATEGORY_PLAN.md Batch 4的内容！")
print("\n  2. 【poses】- 增强现有类别")
print("     新增5个动态姿势")
print("     覆盖从静态到动态的完整范围")
print("\n  3. 【photography_techniques】- 全新类别！")
print("     专业摄影技术（强制透视、广角镜头）")
print("     技术性强，专业度高")
print("\n  4. 【visual_styles】- 增强现有类别")
print("     K-pop美学（现代流行文化）")
print("     补充亚洲流行文化维度")

print("\n🎯 推荐添加策略:")
print("="*80)
print("\n方案A：添加camera_angles类别（4个特征）⭐ 强烈推荐")
print("  - 填补重要空白，提前完成Batch 4内容")
print("  - 高复用性（8.5-9.0）")
print("  - 专业摄影必备")
print("\n方案B：添加camera_angles + 高优先级poses（3个）")
print("  - 7个特征，全面增强")
print("  - 覆盖相机角度和姿势")
print("\n方案C：完整添加所有高优先级特征（7个）")
print("  - camera_angles (4个) + poses (3个)")
print("\n方案D：添加所有特征（14个）")
print("  - 最全面，但包含一些低复用特征")

print("\n⚠️  注意事项:")
print("  • standing_power_pose 与现有的 power_stance 类似，可能重复")
print("  • photography_techniques 是新概念，需要评估是否符合库定位")
print("  • K-pop aesthetic 可能过于具体（但符合亚洲美学主题）")

print("\n" + "="*80)
print("\n✨ 推荐选择：方案A（camera_angles类别）")
print("  理由：")
print("  1. 填补重要空白（相机角度控制）")
print("  2. 提前完成COMPLETE_CATEGORY_PLAN.md Batch 4")
print("  3. 高复用性，适用于所有肖像摄影")
print("  4. 4个特征，适中的数量")
print("="*80 + "\n")
