#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新器 (Auto Updater)
自动添加特征到库、更新版本、生成changelog
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from version_control import VersionController


class AutoUpdater:
    """自动库更新器"""

    def __init__(self, library_path: str = "extracted_results/facial_features_library.json"):
        self.library_path = library_path
        self.version_controller = VersionController(library_path)
        self.changelog_path = "extracted_results/CHANGELOG.md"

    def load_library(self) -> Dict:
        """加载库"""
        with open(self.library_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_library(self, library: Dict) -> None:
        """保存库"""
        with open(self.library_path, 'w', encoding='utf-8') as f:
            json.dump(library, f, ensure_ascii=False, indent=2)

    def add_feature_to_library(self, feature: Dict, library: Dict) -> Tuple[bool, str]:
        """添加特征到库

        Args:
            feature: 特征数据
            library: 库数据

        Returns:
            (成功/失败, 消息)
        """
        category = feature.get('category', '')
        raw_text = feature.get('raw_text', '')

        # 生成分类码
        classification_code = self._generate_classification_code(raw_text)

        # 检查类别是否存在
        if category not in library:
            # 创建新类别
            library[category] = {}
            print(f"  ✨ 创建新类别: {category}")

        # 检查是否已存在相同分类
        if classification_code in library[category]:
            return False, f"分类码 '{classification_code}' 已存在"

        # 创建特征条目
        feature_entry = self._create_feature_entry(feature)

        # 添加到库
        library[category][classification_code] = feature_entry

        # 更新metadata
        self._update_metadata(library, category, is_new_category=(category not in library))

        return True, f"成功添加: {category}/{classification_code}"

    def _generate_classification_code(self, raw_text: str) -> str:
        """生成分类码"""
        import re

        # 转换为小写
        code = raw_text.lower()

        # 移除特殊字符
        code = re.sub(r'[^\w\s-]', '', code)

        # 空格和连字符转下划线
        code = re.sub(r'[-\s]+', '_', code)

        # 移除前后下划线
        code = code.strip('_')

        # 限制长度
        if len(code) > 30:
            code = code[:30]

        return code

    def _create_feature_entry(self, feature: Dict) -> Dict:
        """创建特征条目"""
        raw_text = feature.get('raw_text', '')
        category = feature.get('category', '')

        # 基础条目
        entry = {
            "chinese_name": self._generate_chinese_name(raw_text, category),
            "classification_code": self._generate_classification_code(raw_text),
            "keywords": self._extract_keywords(raw_text),
            "source": "auto_learned",
            "added_date": datetime.now().strftime('%Y-%m-%d'),
            "confidence": feature.get('confidence', 0.8),
            "reusability_score": self._estimate_reusability(category)
        }

        # 根据类别添加特定字段
        if category in ['hair_styles', 'hair_colors']:
            entry["visual_features"] = {
                "description": raw_text
            }

        return entry

    def _generate_chinese_name(self, raw_text: str, category: str) -> str:
        """生成中文名称（简单版本，可以后续手动优化）"""
        # 简单映射
        mappings = {
            'long': '长',
            'short': '短',
            'flowing': '飘逸',
            'straight': '直',
            'curly': '卷',
            'wavy': '波浪',
            'red': '红色',
            'black': '黑色',
            'blonde': '金色',
            'brown': '棕色',
            'hair': '发',
            'skin': '肤色',
            'pale': '苍白',
            'fair': '白皙',
            'dark': '深色',
            'elegant': '优雅',
            'casual': '休闲'
        }

        chinese_parts = []
        for word in raw_text.lower().split():
            if word in mappings:
                chinese_parts.append(mappings[word])

        if chinese_parts:
            return ''.join(chinese_parts)
        else:
            return raw_text  # 如果无法翻译，保留原文

    def _extract_keywords(self, raw_text: str) -> List[str]:
        """提取关键词"""
        # 简单分词
        words = raw_text.lower().split()

        # 过滤停用词
        stopwords = ['a', 'an', 'the', 'with', 'and', 'or']
        keywords = [w for w in words if w not in stopwords and len(w) > 2]

        return keywords[:5]  # 最多5个关键词

    def _estimate_reusability(self, category: str) -> float:
        """估算复用性评分"""
        high_reuse = ['hair_styles', 'hair_colors', 'skin_tones', 'makeup_styles']
        medium_reuse = ['clothing_styles', 'accessories', 'poses']

        if category in high_reuse:
            return 8.5
        elif category in medium_reuse:
            return 7.0
        else:
            return 6.0

    def _update_metadata(self, library: Dict, new_category: str = None,
                        is_new_category: bool = False) -> None:
        """更新库的metadata"""
        metadata = library.get('library_metadata', {})

        # 更新总分类数
        total_classifications = sum(
            len(items) for cat, items in library.items()
            if cat != 'library_metadata' and isinstance(items, dict)
        )

        # 更新总类别数
        total_categories = len([
            cat for cat in library.keys()
            if cat != 'library_metadata' and isinstance(library[cat], dict)
        ])

        # 更新最后修改时间
        metadata['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        metadata['total_classifications'] = total_classifications
        metadata['total_categories'] = total_categories

        library['library_metadata'] = metadata

    def batch_add_features(self, features: List[Dict], create_backup: bool = True) -> Dict:
        """批量添加特征

        Args:
            features: 特征列表
            create_backup: 是否创建备份

        Returns:
            添加结果统计
        """
        # 创建备份
        if create_backup:
            backup_path = self.version_controller.create_backup(reason="before_auto_update")
            print(f"📦 备份已创建: {os.path.basename(backup_path)}\n")

        # 加载库
        library = self.load_library()
        old_version = library['library_metadata']['version']

        # 添加特征
        results = {
            'success': [],
            'failed': [],
            'skipped': []
        }

        print("🔄 开始批量添加特征...\n")

        for idx, feature in enumerate(features, 1):
            category = feature.get('category', '')
            raw_text = feature.get('raw_text', '')

            print(f"[{idx}/{len(features)}] 添加: [{category}] {raw_text}")

            success, message = self.add_feature_to_library(feature, library)

            if success:
                results['success'].append(feature)
                print(f"  ✅ {message}")
            else:
                results['failed'].append(feature)
                print(f"  ❌ {message}")

        # 增加版本号
        new_version = self.version_controller.increment_version()
        library['library_metadata']['version'] = new_version

        # 更新描述
        old_desc = library['library_metadata'].get('description', '')
        new_desc = old_desc + f" v{new_version}更新：自动添加{len(results['success'])}个新特征。"
        library['library_metadata']['description'] = new_desc

        # 保存库
        self.save_library(library)

        print(f"\n✅ 库已更新！版本: v{old_version} → v{new_version}")

        # 生成changelog
        self._append_to_changelog(old_version, new_version, results)

        return results

    def _append_to_changelog(self, old_version: str, new_version: str, results: Dict) -> None:
        """追加到changelog"""
        changelog_entry = f"""
## v{new_version} - {datetime.now().strftime('%Y-%m-%d')}

### 自动更新

**变更统计**:
- 新增特征: {len(results['success'])} 个
- 失败: {len(results['failed'])} 个

**新增特征列表**:
"""

        # 按类别分组
        by_category = {}
        for feature in results['success']:
            category = feature['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(feature['raw_text'])

        for category, features in sorted(by_category.items()):
            changelog_entry += f"\n#### {category}\n"
            for feature_text in features:
                changelog_entry += f"- {feature_text}\n"

        changelog_entry += "\n---\n"

        # 追加到文件
        if os.path.exists(self.changelog_path):
            with open(self.changelog_path, 'r', encoding='utf-8') as f:
                existing = f.read()
            changelog_entry = changelog_entry + "\n" + existing

        with open(self.changelog_path, 'w', encoding='utf-8') as f:
            f.write(changelog_entry)

        print(f"\n📝 Changelog 已更新: {self.changelog_path}")


if __name__ == "__main__":
    # 测试
    updater = AutoUpdater()

    # 测试添加单个特征
    test_feature = {
        'category': 'hair_styles',
        'raw_text': 'long flowing red hair',
        'confidence': 0.9
    }

    print("🧪 自动更新器测试\n")

    library = updater.load_library()
    print(f"当前版本: v{library['library_metadata']['version']}")
    print(f"当前分类数: {library['library_metadata']['total_classifications']}\n")

    # 不实际添加，只显示会如何处理
    print(f"测试特征: {test_feature['raw_text']}")
    print(f"生成分类码: {updater._generate_classification_code(test_feature['raw_text'])}")
    print(f"生成中文名: {updater._generate_chinese_name(test_feature['raw_text'], test_feature['category'])}")
    print(f"提取关键词: {updater._extract_keywords(test_feature['raw_text'])}")
