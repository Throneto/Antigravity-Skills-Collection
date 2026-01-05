#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加已批准的特征到库
"""

from auto_updater import AutoUpdater
from version_control import VersionController

# 用户已批准的7个特征（70-90%置信度）
approved_features = [
    {
        "category": "hair_colors",
        "raw_text": "black hair",
        "confidence": 0.87,
        "method": "ai-assisted"
    },
    {
        "category": "hair_styles",
        "raw_text": "hair with subtle classical waves",
        "confidence": 0.83,
        "method": "ai-assisted"
    },
    {
        "category": "skin_tones",
        "raw_text": "porcelain skin",
        "confidence": 0.82,
        "method": "ai-assisted"
    },
    {
        "category": "expressions",
        "raw_text": "captivating gentle yet subtly seductive",
        "confidence": 0.77,
        "method": "ai-assisted"
    },
    {
        "category": "expressions",
        "raw_text": "gentle smile",
        "confidence": 0.76,
        "method": "rule-based"
    },
    {
        "category": "clothing_styles",
        "raw_text": "wearing elegant deep emerald green classical",
        "confidence": 0.75,
        "method": "ai-assisted"
    },
    {
        "category": "hair_style",
        "raw_text": "long black hair",
        "confidence": 0.72,
        "method": "rule-based"
    }
]

print("\n" + "="*70)
print("  📦 添加已批准的特征到库")
print("="*70 + "\n")

# 获取当前版本
version_controller = VersionController()
version_info = version_controller.get_version_info()
print(f"当前版本: v{version_info['version']}")
print(f"当前分类数: {version_info['total_classifications']}\n")

# 添加特征
updater = AutoUpdater()
results = updater.batch_add_features(approved_features, create_backup=True)

print("\n" + "="*70)
print("  ✅ 更新完成")
print("="*70 + "\n")

print(f"成功添加: {len(results['success'])} 个")
print(f"失败: {len(results['failed'])} 个\n")

if results['success']:
    print("成功添加的特征:")
    for item in results['success']:
        print(f"  ✅ [{item['category']}] {item['raw_text']}")

if results['failed']:
    print("\n失败的特征:")
    for item in results['failed']:
        print(f"  ❌ [{item['category']}] {item['raw_text']}: {item['reason']}")

# 显示新版本
new_version_info = version_controller.get_version_info()
print(f"\n新版本: v{new_version_info['version']}")
print(f"新分类数: {new_version_info['total_classifications']}\n")

# 显示最新备份
backups = version_controller.list_backups()
if backups:
    latest_backup = backups[0]
    print(f"最新备份: {latest_backup['filename']}\n")
