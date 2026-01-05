#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加案例342高优先级特征到库（v1.8 → v1.9）
来源：日本街头摄影风格小酒吧场景
"""

import json
from pathlib import Path
from version_control import VersionController
from datetime import datetime

# 高优先级特征（复用性≥8.5）
case_342_high_priority = {
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
    }
}

print("\n" + "="*80)
print("  📦 添加案例342高优先级特征到库（v1.8 → v1.9）")
print("="*80 + "\n")

print("🎯 添加的5个高优先级特征（亚洲美学补充）:")
print("-" * 80)
for category, features in case_342_high_priority.items():
    print(f"\n【{category}】:")
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  ✓ {code}")
        print(f"    中文名: {cn_name}")
        print(f"    复用性: {score}/10")
        keywords = data.get('keywords', [])
        print(f"    关键词: {', '.join(keywords[:3])}")

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

for category, items in case_342_high_priority.items():
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

# 更新版本
old_version = metadata.get("version", "1.8")
new_version = "1.9"
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

print(f"\n版本: v{old_version} → v{new_version}")
print(f"分类数: {version_info['total_classifications']} → {total_classifications}\n")

# 更新CHANGELOG
changelog_path = SCRIPT_DIR / "extracted_results" / "CHANGELOG.md"

changelog_entry = f"""
## v{new_version} - {datetime.now().strftime('%Y-%m-%d')}

### 亚洲美学扩展 - 新增日本街头摄影风格支持

**变更统计**:
- 新增类别: {len(new_categories)} 个 ({', '.join(new_categories) if new_categories else 'N/A'})
- 新增分类: {added_count} 个
- 总类别数: {total_categories}
- 总分类数: {total_classifications}

**新增特征详情**:

#### hair_styles (发型)
- ponytail_with_bangs: 齐刘海马尾辫 (复用性: 9.0/10)

#### makeup_styles (妆容)
- oxygen_fresh_natural: 氧气妆（清新自然妆） (复用性: 8.5/10)
  - 亚洲美妆流行趋势
  - 半透明露珠底妆、内眼角高光、干净红唇

#### gaze_directions (视线方向)
- direct_gaze_chin_lowered: 低头直视 (复用性: 8.5/10)
  - 创造脆弱又自信的连接感

#### hair_colors (发色)
- chestnut_brown: 栗色/栗棕色 (复用性: 8.5/10)

#### visual_styles (视觉风格) - 新类别 🆕
- 1980s_japanese_street_photography: 1980年代日本街头摄影风格 (复用性: 8.5/10)
  - 荒木经惟、森山大道风格
  - 琥珀色调、胶片质感、低饱和度

**说明**:
此次更新首次引入亚洲美学特征：
- ✅ 亚洲流行妆容（氧气妆）
- ✅ 常见亚洲发型（齐刘海马尾）
- ✅ 日本街头摄影风格
- ✅ 丰富了gaze_directions和hair_colors类别

特征来源：案例342 - 日本街头摄影风格小酒吧场景

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
print("\n🎉 恭喜！库已升级到 v1.9")
print("\n🌏 新能力解锁（亚洲美学）:")
print("  ✅ 氧气妆（亚洲流行妆容）")
print("  ✅ 齐刘海马尾（常见亚洲发型）")
print("  ✅ 栗色发色")
print("  ✅ 低头直视姿势（增强gaze_directions）")
print("  ✅ 1980年代日本街头摄影风格（vintage aesthetic）")
print("\n💡 这是库中第一批亚洲美学特征！")
print("="*80 + "\n")
