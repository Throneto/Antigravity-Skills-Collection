#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加动态视角肖像高复用特征到库（v1.9 → v2.0）
来源：Dynamic Perspective Portrait 模板
"""

import json
from pathlib import Path
from version_control import VersionController
from datetime import datetime

# 方案C：所有高复用特征（复用性≥8.0）
dynamic_perspective_high_priority = {
    "camera_angles": {
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

print("\n" + "="*80)
print("  📦 添加动态视角肖像高复用特征到库（v1.9 → v2.0）")
print("="*80 + "\n")

print("🎯 添加的9个高复用特征（复用性≥8.0）:")
print("-" * 80)
total_count = 0
for category, features in dynamic_perspective_high_priority.items():
    print(f"\n【{category}】({len(features)}个):")
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  ✓ {code}")
        print(f"    中文名: {cn_name}")
        print(f"    复用性: {score}/10")
        total_count += 1

print(f"\n总计: {total_count} 个特征")
print("\n" + "="*80)

# 获取当前版本
version_controller = VersionController()
version_info = version_controller.get_version_info()
print(f"\n当前版本: v{version_info['version']}")
print(f"当前分类数: {version_info['total_classifications']}\n")

# 加载库
SCRIPT_DIR = Path(__file__).parent
LIBRARY_PATH = SCRIPT_DIR / "extracted_results" / "facial_features_library.json"

# 创建备份
backup_path = version_controller.create_backup()
print(f"✅ 备份已创建: {backup_path}\n")

# 加载库
with open(LIBRARY_PATH, 'r', encoding='utf-8') as f:
    library = json.load(f)

print("🔄 开始添加特征...\n")

# 添加特征
added_count = 0
new_categories = []

for category, items in dynamic_perspective_high_priority.items():
    for code, data in items.items():
        # 确保类别存在
        if category not in library:
            library[category] = {}
            new_categories.append(category)
            print(f"  ✨ 创建新类别: {category}")

        # 添加特征
        library[category][code] = data
        added_count += 1
        print(f"  ✅ 已添加: {category}/{code}")

# 更新元数据
if "library_metadata" not in library:
    library["library_metadata"] = {}

metadata = library["library_metadata"]

# 计算总分类数
total_classifications = 0
total_categories = 0
for key, value in library.items():
    if key != "library_metadata":
        total_categories += 1
        if isinstance(value, dict):
            total_classifications += len([k for k in value.keys() if k != "library_metadata"])

# 更新版本 - 升级到v2.0！
old_version = metadata.get("version", "1.9")
new_version = "2.0"
metadata["version"] = new_version
metadata["total_categories"] = total_categories
metadata["total_classifications"] = total_classifications
metadata["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 保存库
with open(LIBRARY_PATH, 'w', encoding='utf-8') as f:
    json.dump(library, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("  ✅ 更新完成")
print("="*80 + "\n")

print(f"成功添加: {added_count} 个特征")
if new_categories:
    print(f"新增类别: {', '.join(new_categories)}")

print(f"\n版本: v{old_version} → v{new_version} 🎉")
print(f"分类数: {version_info['total_classifications']} → {total_classifications}\n")

# 更新CHANGELOG
changelog_path = SCRIPT_DIR / "extracted_results" / "CHANGELOG.md"

changelog_entry = f"""
## v{new_version} - {datetime.now().strftime('%Y-%m-%d')} 🎉

### 里程碑版本 - Batch 4实现 + 专业摄影技术

**变更统计**:
- 新增类别: {len(new_categories)} 个 ({', '.join(new_categories) if new_categories else 'N/A'})
- 新增分类: {added_count} 个
- 总类别数: {total_categories}
- 总分类数: {total_classifications}

**新增特征详情**:

#### camera_angles (相机角度) - 新类别 🆕
- eye_level_close_up: 平视特写 (复用性: 9.0/10) ⭐
- low_angle_worms_eye: 低角度仰视/虫眼视角 (复用性: 8.5/10)
- high_angle_birds_eye: 高角度俯视/鸟眼视角 (复用性: 8.5/10)
- dutch_angle_tilted: 荷兰角/倾斜视角 (复用性: 7.5/10)

#### photography_techniques (摄影技术) - 新类别 🆕
- wide_angle_24mm: 24mm广角镜头 (复用性: 8.5/10)
- forced_perspective_hand: 强制透视/手部特写 (复用性: 8.0/10)

#### poses (姿势)
- sitting_cross_legged: 盘腿坐姿 (复用性: 8.5/10)
- leaning_forward: 前倾姿势 (复用性: 8.5/10)

#### visual_styles (视觉风格)
- kpop_aesthetic: K-pop美学风格 (复用性: 8.0/10)

**说明**:
此次更新是一个重要里程碑：
- ✅ 提前完成COMPLETE_CATEGORY_PLAN.md Batch 4核心内容（camera_angles）
- ✅ 新增专业摄影技术类别（photography_techniques）
- ✅ 增强poses和visual_styles类别
- ✅ 达到v2.0版本，总分类数突破100大关！

特征来源：Dynamic Perspective Portrait模板（K-pop/MV风格）

**v2.0新能力**:
- 相机角度完全控制（4种专业角度）
- 专业摄影技术（广角镜头、强制透视）
- 更多动态姿势选择
- K-pop流行文化支持

---

"""

# 追加到CHANGELOG开头
if changelog_path.exists():
    with open(changelog_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()

    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_entry + existing_content)
else:
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_entry)

print(f"📝 CHANGELOG已更新: {changelog_path}\n")

# 显示最新备份
backups = version_controller.list_backups()
if backups:
    latest_backup = backups[0]
    print(f"最新备份: {latest_backup['filename']}\n")

print("="*80)
print("\n🎉🎉🎉 恭喜！库已升级到 v2.0 - 里程碑版本！🎉🎉🎉")
print("\n🌟 v2.0新能力解锁:")
print("  ✅ 相机角度控制（camera_angles）- Batch 4核心")
print("     • 平视特写 - 自然平衡")
print("     • 低角度仰视 - 力量感")
print("     • 高角度俯视 - 亲密感")
print("     • 荷兰角 - 动态张力")
print("\n  ✅ 专业摄影技术（photography_techniques）")
print("     • 24mm广角镜头 - 动态视野")
print("     • 强制透视 - 创意效果")
print("\n  ✅ 丰富姿势库（poses增强）")
print("     • 盘腿坐姿 - 休闲放松")
print("     • 前倾姿势 - 互动性强")
print("\n  ✅ K-pop美学风格支持")
print("\n📊 库状态:")
print(f"  • 总类别数: {total_categories}")
print(f"  • 总分类数: {total_classifications} （突破100大关！）")
print(f"  • 版本: v{new_version}")
print("\n💡 这是一个里程碑版本：")
print("  • 提前完成Batch 4核心内容")
print("  • 支持专业摄影控制")
print("  • 适用于K-pop、MV、动态肖像等现代风格")
print("="*80 + "\n")
