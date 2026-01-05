#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加高优先级特征到库（Batch 2部分内容提前实现）
来源：new_training_prompt.txt（Wes Anderson风格）
"""

import json
from pathlib import Path
from auto_updater import AutoUpdater
from version_control import VersionController

# 加载手动提取的特征定义
manual_features_def = {
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
    }
}

print("\n" + "="*80)
print("  📦 添加高优先级特征到库（v1.7 → v1.8）")
print("="*80 + "\n")

print("🎯 添加的特征类别:")
print("-" * 80)
for category, features in manual_features_def.items():
    print(f"\n【{category}】:")
    for code, data in features.items():
        cn_name = data.get("chinese_name", "")
        score = data.get("reusability_score", 0)
        print(f"  ✓ {code}")
        print(f"    中文名: {cn_name}")
        print(f"    复用性: {score}/10")
        print(f"    关键词: {', '.join(data.get('keywords', [])[:3])}")

print("\n" + "="*80)

# 获取当前版本
version_controller = VersionController()
version_info = version_controller.get_version_info()
print(f"\n当前版本: v{version_info['version']}")
print(f"当前分类数: {version_info['total_classifications']}\n")

# 准备添加的特征（转换为AutoUpdater格式）
features_to_add = []

for category, items in manual_features_def.items():
    for code, data in items.items():
        # 构造完整的特征数据
        feature = {
            "category": category,
            "raw_text": code,
            "confidence": 0.95,  # 手动提取的高质量特征
            "method": "manual-extraction",
            "feature_data": data  # 完整的特征定义
        }
        features_to_add.append(feature)

print("🔄 开始添加特征...\n")

# 添加特征
updater = AutoUpdater()

# 手动逐个添加以确保完整数据
SCRIPT_DIR = Path(__file__).parent
LIBRARY_PATH = SCRIPT_DIR / "extracted_results" / "facial_features_library.json"

# 创建备份
backup_path = version_controller.create_backup()
print(f"✅ 备份已创建: {backup_path}\n")

# 加载库
with open(LIBRARY_PATH, 'r', encoding='utf-8') as f:
    library = json.load(f)

# 添加特征
added_count = 0
new_categories = []

for feature in features_to_add:
    category = feature["category"]
    code = feature["raw_text"]
    data = feature["feature_data"]

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
old_version = metadata.get("version", "1.7")
new_version = "1.8"
metadata["version"] = new_version
metadata["total_categories"] = total_categories
metadata["total_classifications"] = total_classifications
from datetime import datetime
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

### Batch 2 部分实现 - 新增手势和视线类别

**变更统计**:
- 新增类别: {len(new_categories)} 个 ({', '.join(new_categories) if new_categories else 'N/A'})
- 新增分类: {added_count} 个
- 总类别数: {total_categories}
- 总分类数: {total_classifications}

**新增特征详情**:

#### gestures (手势) - 新类别 🆕
- praying_hands_interlocked: 祈祷手势（手指交叉）

#### gaze_directions (视线方向) - 新类别 🆕
- looking_up_pleading: 仰视恳求目光

#### hair_styles (发型)
- twin_buns_space_buns: 双丸子头（太空发髻）

#### expressions (表情)
- playful_shy_smile: 俏皮害羞微笑

**说明**:
此次更新提前实现了COMPLETE_CATEGORY_PLAN.md中Batch 2的部分内容：
- ✅ gestures（手势）- 来自真实用户prompt
- ✅ gaze_directions（视线方向）- 来自真实用户prompt
- ✅ 增强了hair_styles和expressions类别

特征来源：Wes Anderson风格少女肖像prompt（高度具体化的专业描述）

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
print("\n🎉 恭喜！库已升级到 v1.8")
print("\n新能力解锁:")
print("  ✅ 手势控制（gestures）")
print("  ✅ 视线方向控制（gaze_directions）")
print("  ✅ 更丰富的发型和表情选择")
print("\n这些是COMPLETE_CATEGORY_PLAN.md Batch 2中的核心类别！")
print("="*80 + "\n")
