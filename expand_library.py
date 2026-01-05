#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库扩展脚本 - 添加新类别
为 facial_features_library.json 添加 poses, expressions, clothing_styles
"""

import json
import os
from datetime import datetime
from version_control import VersionController

def expand_library():
    """扩展库，添加新类别"""

    library_path = "extracted_results/facial_features_library.json"

    # 创建备份
    print("📦 创建备份...")
    vc = VersionController(library_path)
    backup_path = vc.create_backup(reason="before_expansion")
    print(f"✅ 备份已创建: {os.path.basename(backup_path)}\n")

    # 读取现有库
    with open(library_path, 'r', encoding='utf-8') as f:
        lib = json.load(f)

    old_version = lib['library_metadata']['version']
    old_categories = lib['library_metadata']['total_categories']

    print(f"当前版本: v{old_version}")
    print(f"当前类别数: {old_categories}\n")

    # 定义新类别
    new_categories = {
        "poses": {
            "power_stance": {
                "chinese_name": "力量站姿",
                "classification_code": "power_stance",
                "keywords": ["power stance", "wide stance", "feet apart", "confident pose"],
                "visual_features": {
                    "legs": "feet shoulder-width or wider apart",
                    "weight_distribution": "weight mostly on back leg",
                    "upper_body": "chest forward, shoulders back",
                    "overall_attitude": "confident, grounded"
                },
                "ai_prompt_template": "standing in a confident power stance with feet apart, weight on back leg, chest forward",
                "reusability_score": 8.5,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "arms_crossed": {
                "chinese_name": "双臂交叉",
                "classification_code": "arms_crossed",
                "keywords": ["arms crossed", "crossed arms", "arms over chest"],
                "visual_features": {
                    "arms": "firmly crossed over chest",
                    "hands": "hands tucked under opposite arms",
                    "posture": "upright, confident"
                },
                "ai_prompt_template": "arms firmly crossed over chest",
                "reusability_score": 9.0,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "chin_raised": {
                "chinese_name": "昂首姿态",
                "classification_code": "chin_raised",
                "keywords": ["chin up", "chin raised", "head tilted up"],
                "visual_features": {
                    "head": "chin slightly raised",
                    "neck": "elongated",
                    "gaze": "looking slightly upward or straight ahead",
                    "attitude": "proud, confident"
                },
                "ai_prompt_template": "chin slightly raised with a confident gaze",
                "reusability_score": 8.0,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "relaxed_standing": {
                "chinese_name": "放松站姿",
                "classification_code": "relaxed_standing",
                "keywords": ["relaxed", "casual stance", "natural pose"],
                "visual_features": {
                    "posture": "relaxed, natural",
                    "weight": "shifted to one leg",
                    "overall": "comfortable, approachable"
                },
                "ai_prompt_template": "standing in a relaxed, casual pose",
                "reusability_score": 9.5,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            }
        },

        "expressions": {
            "confident_smirk": {
                "chinese_name": "自信微笑",
                "classification_code": "confident_smirk",
                "keywords": ["smirk", "confident", "sassy", "smug expression"],
                "visual_features": {
                    "mouth": "subtle smirk, one corner slightly raised",
                    "eyes": "slightly narrowed, knowing look",
                    "eyebrows": "slightly raised or relaxed",
                    "overall_mood": "confident, sassy, self-assured"
                },
                "ai_prompt_template": "a confident, sassy expression with a subtle smirk",
                "emotional_tone": "positive, confident, playful",
                "reusability_score": 9.0,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "playful_smile": {
                "chinese_name": "俏皮笑容",
                "classification_code": "playful_smile",
                "keywords": ["playful", "fun", "lighthearted", "cheeky"],
                "visual_features": {
                    "mouth": "bright smile, playful grin",
                    "eyes": "sparkling, bright",
                    "head": "slight tilt",
                    "overall_mood": "playful, fun, approachable"
                },
                "ai_prompt_template": "playful, lighthearted smile with a fun attitude",
                "emotional_tone": "positive, energetic, friendly",
                "reusability_score": 9.5,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "serene_calm": {
                "chinese_name": "宁静平和",
                "classification_code": "serene_calm",
                "keywords": ["serene", "calm", "peaceful", "tranquil"],
                "visual_features": {
                    "mouth": "slight smile or neutral",
                    "eyes": "soft, relaxed gaze",
                    "face": "relaxed muscles, no tension",
                    "overall_mood": "peaceful, calm, centered"
                },
                "ai_prompt_template": "serene, calm expression with a peaceful demeanor",
                "emotional_tone": "neutral-positive, peaceful",
                "reusability_score": 9.0,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "gentle_smile": {
                "chinese_name": "温柔微笑",
                "classification_code": "gentle_smile",
                "keywords": ["gentle", "soft smile", "warm", "kind"],
                "visual_features": {
                    "mouth": "soft, gentle smile",
                    "eyes": "warm, kind eyes",
                    "face": "relaxed, approachable",
                    "overall_mood": "gentle, warm, friendly"
                },
                "ai_prompt_template": "gentle, warm smile with kind eyes",
                "emotional_tone": "positive, warm, approachable",
                "reusability_score": 9.5,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            }
        },

        "clothing_styles": {
            "casual_modern": {
                "chinese_name": "现代休闲装",
                "classification_code": "casual_modern",
                "keywords": ["casual", "modern", "comfortable", "everyday"],
                "visual_features": {
                    "style": "casual, comfortable, contemporary",
                    "fit": "relaxed but well-fitted",
                    "overall": "modern, clean, effortless"
                },
                "ai_prompt_template": "wearing modern casual outfit with comfortable fit",
                "occasion": "everyday, casual, street",
                "reusability_score": 9.5,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "elegant_formal": {
                "chinese_name": "优雅正装",
                "classification_code": "elegant_formal",
                "keywords": ["elegant", "formal", "sophisticated", "dressy"],
                "visual_features": {
                    "style": "elegant, formal, refined",
                    "fit": "tailored, fitted",
                    "overall": "sophisticated, polished"
                },
                "ai_prompt_template": "wearing elegant formal attire with sophisticated styling",
                "occasion": "formal, business, evening",
                "reusability_score": 8.5,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "traditional_cultural": {
                "chinese_name": "传统文化装",
                "classification_code": "traditional_cultural",
                "keywords": ["traditional", "cultural", "ethnic", "heritage"],
                "visual_features": {
                    "style": "traditional, cultural-specific",
                    "details": "authentic cultural elements",
                    "overall": "respectful, authentic representation"
                },
                "ai_prompt_template": "wearing traditional cultural attire with authentic details",
                "occasion": "cultural, ceremonial, special occasions",
                "reusability_score": 7.0,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            },
            "sporty_athletic": {
                "chinese_name": "运动休闲装",
                "classification_code": "sporty_athletic",
                "keywords": ["sporty", "athletic", "activewear", "fitness"],
                "visual_features": {
                    "style": "sporty, athletic, functional",
                    "material": "breathable, performance fabrics",
                    "overall": "dynamic, active, healthy"
                },
                "ai_prompt_template": "wearing sporty athletic outfit with modern activewear",
                "occasion": "sports, fitness, active lifestyle",
                "reusability_score": 8.0,
                "source": "manual_expansion",
                "added_date": datetime.now().strftime('%Y-%m-%d')
            }
        }
    }

    # 添加新类别
    print("🚀 添加新类别...\n")
    added_count = 0

    for category_name, category_data in new_categories.items():
        if category_name not in lib:
            lib[category_name] = category_data
            added_count += len(category_data)
            print(f"✅ 添加类别: {category_name}")
            print(f"   包含 {len(category_data)} 个分类:")
            for code, data in category_data.items():
                print(f"   - {code}: {data['chinese_name']}")
            print()
        else:
            print(f"⚠️  类别已存在: {category_name}")

    # 更新metadata
    print("📊 更新metadata...")

    # 计算总分类数
    total_classifications = 0
    for cat_name, cat_data in lib.items():
        if cat_name != 'library_metadata' and isinstance(cat_data, dict):
            total_classifications += len(cat_data)

    # 计算总类别数
    total_categories = len([k for k in lib.keys() if k != 'library_metadata'])

    # 增加版本号
    new_version = vc.increment_version()

    lib['library_metadata']['version'] = new_version
    lib['library_metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    lib['library_metadata']['total_classifications'] = total_classifications
    lib['library_metadata']['total_categories'] = total_categories

    # 更新描述
    old_desc = lib['library_metadata'].get('description', '')
    expansion_note = f" v{new_version}扩展：新增poses, expressions, clothing_styles三个类别，共{added_count}个新分类。"
    lib['library_metadata']['description'] = old_desc + expansion_note

    # 保存
    with open(library_path, 'w', encoding='utf-8') as f:
        json.dump(lib, f, ensure_ascii=False, indent=2)

    print(f"✅ 版本更新: v{old_version} → v{new_version}")
    print(f"✅ 类别数: {old_categories} → {total_categories}")
    print(f"✅ 分类数: {total_classifications}")

    # 生成CHANGELOG
    print("\n📝 生成CHANGELOG...")
    changelog_path = "extracted_results/CHANGELOG.md"

    changelog_entry = f"""
## v{new_version} - {datetime.now().strftime('%Y-%m-%d')}

### 库扩展 - 新增三大类别

**变更统计**:
- 新增类别: 3 个 (poses, expressions, clothing_styles)
- 新增分类: {added_count} 个
- 总类别数: {total_categories}
- 总分类数: {total_classifications}

**新增类别详情**:

#### poses (姿势)
- power_stance: 力量站姿
- arms_crossed: 双臂交叉
- chin_raised: 昂首姿态
- relaxed_standing: 放松站姿

#### expressions (表情)
- confident_smirk: 自信微笑
- playful_smile: 俏皮笑容
- serene_calm: 宁静平和
- gentle_smile: 温柔微笑

#### clothing_styles (服装风格)
- casual_modern: 现代休闲装
- elegant_formal: 优雅正装
- traditional_cultural: 传统文化装
- sporty_athletic: 运动休闲装

**说明**:
此次扩展大幅增强了人像生成的表现力，现在可以：
- ✅ 控制人物姿势（站姿、手势、头部姿态）
- ✅ 控制面部表情（自信、俏皮、平和等）
- ✅ 控制服装风格（休闲、正式、传统、运动）

---

"""

    # 追加到CHANGELOG
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing = f.read()
        changelog_entry = changelog_entry + "\n" + existing

    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_entry)

    print(f"✅ CHANGELOG已更新: {changelog_path}")

    # 总结
    print("\n" + "="*70)
    print("  🎉 库扩展完成！")
    print("="*70)
    print(f"\n📊 扩展统计:")
    print(f"   • 新增类别: 3 个")
    print(f"   • 新增分类: {added_count} 个")
    print(f"   • 新版本: v{new_version}")
    print(f"   • 备份文件: {os.path.basename(backup_path)}")

    print(f"\n✅ 现在可以使用自动学习系统扫描这些类型的特征了！")
    print(f"\n💡 下一步:")
    print(f"   1. 运行 python3 update_learner_for_expansion.py 更新学习器")
    print(f"   2. 测试扫描: python3 test_scan_new_prompt.py")
    print(f"   3. 开始使用: python3 auto_learn_workflow.py scan \"your prompt\"\n")


if __name__ == "__main__":
    expand_library()
