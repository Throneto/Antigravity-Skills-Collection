#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nano Banana糖果雕塑Prompt分析
探讨库的扩展方向：从人像到全领域摄影
"""

# 从Nano Banana prompt中提取的特征
nano_banana_features = {
    "photography_types": {
        "macro_photography": {
            "chinese_name": "微距摄影",
            "keywords": [
                "macro photography",
                "macro lens",
                "100mm macro",
                "extreme close-up",
                "detailed texture"
            ],
            "technical_specs": {
                "lens": "100mm macro lens or similar",
                "focus": "extreme detail on surface textures",
                "magnification": "high magnification ratio"
            },
            "ai_prompt_template": "hyper-realistic ultra-detailed 8K macro photography, extreme detail on every surface",
            "reusability_score": 9.0,
            "suitable_for": ["product", "food", "nature", "jewelry", "texture studies"]
        },

        "product_photography": {
            "chinese_name": "产品摄影",
            "keywords": [
                "product photography",
                "commercial photography",
                "studio photography",
                "professional product shot"
            ],
            "visual_features": {
                "focus": "product as hero subject",
                "lighting": "clean, professional, highlights product",
                "background": "minimal, non-distracting",
                "style": "commercial, polished"
            },
            "ai_prompt_template": "professional product photography, commercial style, studio lighting",
            "reusability_score": 9.5,
            "suitable_for": ["e-commerce", "advertising", "catalogs", "marketing"]
        },

        "food_photography": {
            "chinese_name": "美食摄影",
            "keywords": [
                "food photography",
                "culinary photography",
                "mouthwatering",
                "appetizing",
                "food styling"
            ],
            "visual_features": {
                "appeal": "mouthwatering, appetizing appearance",
                "styling": "professional food styling",
                "colors": "vibrant, fresh, rich",
                "textures": "realistic food textures"
            },
            "ai_prompt_template": "professional food photography, mouthwatering appearance, vibrant colors",
            "reusability_score": 8.5,
            "suitable_for": ["restaurants", "cookbooks", "food brands", "social media"]
        }
    },

    "lighting_techniques": {
        "volumetric_god_rays": {
            "chinese_name": "体积光/上帝之光",
            "keywords": [
                "volumetric light",
                "god rays",
                "light rays",
                "atmospheric lighting",
                "light beams"
            ],
            "visual_features": {
                "effect": "visible light beams through particles",
                "atmosphere": "dramatic, ethereal, divine",
                "particles": "dust, mist, or particles visible in light"
            },
            "ai_prompt_template": "subtle volumetric god rays through particles, dramatic atmospheric lighting",
            "reusability_score": 8.0,
            "suitable_for": ["dramatic scenes", "atmospheric shots", "artistic photography"]
        },

        "rim_lighting": {
            "chinese_name": "轮廓光/边缘光",
            "keywords": [
                "rim light",
                "edge lighting",
                "backlight",
                "contour lighting",
                "separation light"
            ],
            "visual_features": {
                "placement": "light from behind/side creating edge glow",
                "effect": "separates subject from background",
                "quality": "dramatic, dimensional"
            },
            "ai_prompt_template": "dramatic rim light creating edge glow and separation",
            "reusability_score": 9.0,
            "suitable_for": ["portraits", "product", "dramatic shots", "silhouettes"]
        },

        "natural_window_light": {
            "chinese_name": "自然窗光",
            "keywords": [
                "natural window light",
                "soft window lighting",
                "diffused daylight",
                "natural light"
            ],
            "visual_features": {
                "quality": "soft, diffused, natural",
                "direction": "from window, directional but soft",
                "mood": "warm, inviting, organic"
            },
            "ai_prompt_template": "soft natural window light, diffused daylight",
            "reusability_score": 9.5,
            "suitable_for": ["portraits", "lifestyle", "product", "interiors"]
        }
    },

    "technical_effects": {
        "subsurface_scattering": {
            "chinese_name": "次表面散射",
            "keywords": [
                "subsurface scattering",
                "SSS",
                "translucent glow",
                "light transmission",
                "internal glow"
            ],
            "visual_features": {
                "materials": "translucent materials (skin, wax, marble, candy)",
                "effect": "light passing through and scattering inside material",
                "appearance": "soft glow, realistic translucency"
            },
            "ai_prompt_template": "realistic subsurface scattering in translucent parts, soft internal glow",
            "reusability_score": 7.5,
            "technical_note": "Important for realistic rendering of translucent materials",
            "suitable_for": ["skin", "candles", "marble", "jade", "candy", "certain foods"]
        },

        "caustics": {
            "chinese_name": "焦散效果",
            "keywords": [
                "caustics",
                "light caustics",
                "refraction patterns",
                "focused light patterns"
            ],
            "visual_features": {
                "source": "light refracted through transparent/translucent materials",
                "appearance": "concentrated light patterns, dancing light",
                "materials": "glass, water, crystals, transparent objects"
            },
            "ai_prompt_template": "realistic caustics and light refraction patterns",
            "reusability_score": 7.0,
            "suitable_for": ["glass", "water", "crystals", "jewelry", "transparent materials"]
        },

        "bokeh_creamy_cinematic": {
            "chinese_name": "奶油般散景",
            "keywords": [
                "creamy bokeh",
                "cinematic bokeh",
                "smooth bokeh",
                "beautiful blur"
            ],
            "visual_features": {
                "quality": "smooth, creamy, pleasing blur",
                "appearance": "soft circular or shaped blur spots",
                "effect": "separates subject, artistic depth"
            },
            "ai_prompt_template": "creamy cinematic bokeh, smooth beautiful background blur",
            "reusability_score": 9.0,
            "suitable_for": ["portraits", "product", "artistic shots"]
        }
    },

    "material_textures": {
        "glossy_surfaces": {
            "chinese_name": "光泽表面",
            "keywords": [
                "glossy surface",
                "shiny finish",
                "reflective surface",
                "polished",
                "lustrous"
            ],
            "visual_features": {
                "appearance": "high reflectivity, mirror-like",
                "highlights": "bright specular highlights",
                "materials": "polished metal, glass, plastic, glazed ceramics"
            },
            "ai_prompt_template": "glossy surface with realistic reflections and highlights",
            "reusability_score": 8.5
        },

        "translucent_materials": {
            "chinese_name": "半透明材质",
            "keywords": [
                "translucent",
                "semi-transparent",
                "light-transmitting",
                "glow effect"
            ],
            "visual_features": {
                "light_behavior": "allows light to pass through partially",
                "appearance": "soft glow, internal luminosity",
                "materials": "frosted glass, wax, certain plastics, candy"
            },
            "ai_prompt_template": "translucent materials with soft glow and light transmission",
            "reusability_score": 8.0
        },

        "sugar_crystal_sparkle": {
            "chinese_name": "糖晶闪光",
            "keywords": [
                "sugar crystals",
                "crystalline sparkle",
                "sugar sparkle",
                "crystal glitter"
            ],
            "visual_features": {
                "appearance": "tiny bright sparkle points",
                "effect": "crystalline, jewel-like glints",
                "context": "sugar, salt, frost, crystals"
            },
            "ai_prompt_template": "sugar crystal sparkle, fine crystalline glitter",
            "reusability_score": 7.0,
            "specific_use": "Food, candy, decorative crystals"
        }
    },

    "subject_types": {
        "sculptural_art": {
            "chinese_name": "雕塑艺术",
            "keywords": [
                "sculpture",
                "sculptural art",
                "three-dimensional art",
                "constructed sculpture"
            ],
            "visual_features": {
                "form": "three-dimensional artistic form",
                "construction": "assembled or carved structure",
                "presentation": "art object, display piece"
            },
            "ai_prompt_template": "meticulously constructed sculpture, intricate artistic form",
            "reusability_score": 7.5
        },

        "impossible_construction": {
            "chinese_name": "不可能结构",
            "keywords": [
                "impossible construction",
                "impossible precision",
                "defying gravity",
                "intricate assembly"
            ],
            "visual_features": {
                "complexity": "impossibly intricate, precise",
                "impression": "technically challenging, impressive",
                "detail": "extreme attention to assembly"
            },
            "ai_prompt_template": "impossibly intricate construction, impossible precision",
            "reusability_score": 6.5,
            "artistic_concept": "Emphasizes the impressive, surreal nature"
        }
    }
}

# 统计分析
print("\n" + "="*80)
print("📋 Nano Banana糖果雕塑Prompt分析")
print("="*80 + "\n")

print("🎯 核心发现：")
print("-" * 80)
print("这个prompt展示了当前库的局限性：")
print("  • 当前库主要聚焦：人像摄影（Portrait Photography）")
print("  • 这个prompt需要：产品摄影、微距摄影、美食摄影")
print("  • 涉及领域：商业摄影、艺术摄影、技术渲染")
print("\n" + "="*80)

total_features = 0
for category, features in nano_banana_features.items():
    print(f"\n【{category}】: {len(features)} 个")
    total_features += len(features)
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  - {code}: {cn_name} (复用性: {score}/10)")

print(f"\n总计: {total_features} 个特征")
print("\n" + "="*80)

# 按适用范围分组
print("\n📊 按适用范围分类:")
print("="*80 + "\n")

print("🌟 通用型特征（高复用，跨领域）:")
print("  • product_photography (9.5/10) - 所有产品类")
print("  • natural_window_light (9.5/10) - 人像、产品、生活方式")
print("  • rim_lighting (9.0/10) - 人像、产品、艺术")
print("  • macro_photography (9.0/10) - 产品、自然、珠宝")
print("  • bokeh_creamy_cinematic (9.0/10) - 人像、产品、艺术")

print("\n🎨 摄影类型特征（中高复用）:")
print("  • food_photography (8.5/10)")
print("  • glossy_surfaces (8.5/10)")
print("  • translucent_materials (8.0/10)")
print("  • volumetric_god_rays (8.0/10)")

print("\n🔬 技术/特定特征（中低复用）:")
print("  • subsurface_scattering (7.5/10) - 技术渲染")
print("  • sculptural_art (7.5/10) - 艺术品")
print("  • caustics (7.0/10) - 透明材质")
print("  • sugar_crystal_sparkle (7.0/10) - 食品/糖果")
print("  • impossible_construction (6.5/10) - 艺术概念")

print("\n" + "="*80)

print("\n💡 关键问题：库的定位与边界")
print("="*80)
print("\n当前状态：")
print("  • 库名称：facial_features_library.json")
print("  • 主要内容：人像摄影特征（面部、妆容、姿势、表情等）")
print("  • v2.0状态：23个类别，104个分类")

print("\n面临的选择：")
print("  【选项A】保持人像专注")
print("    优势：")
print("      + 专业化，深度挖掘人像摄影")
print("      + 库结构清晰，易于维护")
print("      + 已有良好基础（104个人像特征）")
print("    劣势：")
print("      - 无法支持产品摄影、美食摄影等")
print("      - 限制了应用范围")

print("\n  【选项B】扩展到全领域摄影")
print("    优势：")
print("      + 支持更广泛的摄影类型")
print("      + 一个库解决所有问题")
print("      + 提取的光影、技术特征可跨领域复用")
print("    劣势：")
print("      - 库可能变得庞大、复杂")
print("      - 需要重新规划架构")
print("      - 可能稀释人像摄影的专业性")

print("\n  【选项C】创建模块化架构")
print("    • 保留 facial_features_library.json（人像专用）")
print("    • 新建 photography_techniques_library.json（通用技术）")
print("    • 新建 product_photography_library.json（产品摄影）")
print("    • 共享通用类别（lighting, camera_angles, photography_techniques等）")
print("    优势：")
print("      + 各司其职，结构清晰")
print("      + 可以复用通用特征")
print("      + 易于扩展新领域")
print("    劣势：")
print("      - 需要管理多个库")
print("      - 可能有重复内容")

print("\n" + "="*80)

print("\n🎯 推荐策略：")
print("="*80)
print("\n我的建议是【选项C】- 模块化架构：\n")
print("1. 当前库重命名为 portrait_features_library.json")
print("   - 继续专注人像摄影")
print("   - 保持现有结构和内容")

print("\n2. 提取通用特征到 photography_common.json")
print("   包括：")
print("   • camera_angles（已有）")
print("   • photography_techniques（部分已有）")
print("   • lighting_techniques（新增）")
print("   • technical_effects（新增）")

print("\n3. 根据需求创建专门库：")
print("   • product_photography_library.json（产品摄影）")
print("   • food_photography_library.json（美食摄影）")
print("   • nature_photography_library.json（自然摄影）")

print("\n这样：")
print("  ✅ 保持人像摄影的专业性")
print("  ✅ 支持其他摄影类型")
print("  ✅ 通用特征可复用")
print("  ✅ 结构清晰，易于扩展")

print("\n" + "="*80)

print("\n❓ 你的选择：")
print("-" * 80)
print("A. 保持人像专注（不添加Nano Banana类特征）")
print("B. 扩展到全领域（将所有特征加入当前库）")
print("C. 模块化架构（我最推荐的方案）")
print("D. 先讨论具体需求，再决定方向")

print("\n告诉我你的想法！")
print("="*80 + "\n")
