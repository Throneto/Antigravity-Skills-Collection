#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script - 迁移现有库到Universal Elements Database
将现有的3个JSON库迁移到SQLite数据库中
"""

import json
from pathlib import Path
from element_db import ElementDB


class LibraryMigrator:
    """库迁移器"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.db = ElementDB(db_path)
        self.lib_dir = Path("extracted_results")

        self.element_counter = {
            'portrait': 0,
            'interior': 0,
            'common': 0
        }

    def migrate_all(self):
        """迁移所有库"""
        print("=" * 80)
        print("开始迁移现有库到Universal Elements Database")
        print("=" * 80)

        # 1. 迁移人像特征库
        print("\n[1/3] 迁移 facial_features_library.json → portrait domain")
        facial_path = self.lib_dir / "facial_features_library.json"
        if facial_path.exists():
            self.migrate_facial_features(facial_path)
        else:
            print(f"   ⚠️  文件不存在: {facial_path}")

        # 2. 迁移室内设计库
        print("\n[2/3] 迁移 interior_design_library.json → interior domain")
        interior_path = self.lib_dir / "interior_design_library.json"
        if interior_path.exists():
            self.migrate_interior_design(interior_path)
        else:
            print(f"   ⚠️  文件不存在: {interior_path}")

        # 3. 迁移通用摄影库
        print("\n[3/3] 迁移 photography_common.json → common domain")
        common_path = self.lib_dir / "photography_common.json"
        if common_path.exists():
            self.migrate_photography_common(common_path)
        else:
            print(f"   ⚠️  文件不存在: {common_path}")

        # 4. 显示迁移统计
        print("\n" + "=" * 80)
        print("迁移完成！")
        print("=" * 80)
        self.show_migration_stats()

        # 5. 导出JSON备份
        print("\n导出JSON备份...")
        self.db.export_to_json('extracted_results/universal_elements_library.json')

        print("\n✅ 所有迁移任务完成！")

    def migrate_facial_features(self, json_path: Path):
        """迁移人像特征库"""
        with open(json_path, 'r', encoding='utf-8') as f:
            lib = json.load(f)

        print(f"   读取文件: {json_path}")

        migrated = 0

        # facial_features_library.json 的结构：
        # {
        #   "facial_features": { "feature_name": {...}, ... },
        #   "makeup_styles": { ... },
        #   ...
        # }

        for category_id, category_items in lib.items():
            if category_id == "library_metadata":
                continue

            if not isinstance(category_items, dict):
                continue

            print(f"   迁移类别: {category_id} ({len(category_items)} 个元素)")

            for item_name, item_data in category_items.items():
                if item_name == "library_metadata":
                    continue

                # 生成element_id
                self.element_counter['portrait'] += 1
                element_id = f"portrait_{category_id}_{self.element_counter['portrait']:03d}"

                # 提取标签
                tags = self._extract_tags_from_keywords(
                    item_data.get('keywords', [])
                ) + ['portrait', category_id.replace('_', '-')]

                # 添加到数据库
                success = self.db.add_element(
                    element_id=element_id,
                    domain_id='portrait',
                    category_id=category_id,
                    name=item_name,
                    chinese_name=item_data.get('chinese_name'),
                    ai_prompt_template=item_data.get('ai_prompt_template', ''),
                    keywords=item_data.get('keywords', []),
                    tags=tags,
                    reusability_score=item_data.get('reusability_score'),
                    source_prompts=item_data.get('source_prompts', []),
                    learned_from='migrated_from_v2',
                    metadata={
                        'original_category': category_id,
                        'suitable_for': item_data.get('suitable_for', [])
                    }
                )

                if success:
                    migrated += 1

        print(f"   ✅ 迁移完成: {migrated} 个元素")

    def migrate_interior_design(self, json_path: Path):
        """迁移室内设计库"""
        with open(json_path, 'r', encoding='utf-8') as f:
            lib = json.load(f)

        print(f"   读取文件: {json_path}")

        migrated = 0

        # interior_design_library.json 的结构：
        # {
        #   "space_types": { "space_name": {...}, ... },
        #   "furniture_layouts": { ... },
        #   ...
        # }

        for category_id, category_items in lib.items():
            if category_id == "library_metadata":
                continue

            if not isinstance(category_items, dict):
                continue

            print(f"   迁移类别: {category_id} ({len(category_items)} 个元素)")

            for item_name, item_data in category_items.items():
                if item_name == "library_metadata":
                    continue

                # 生成element_id
                self.element_counter['interior'] += 1
                element_id = f"interior_{category_id}_{self.element_counter['interior']:03d}"

                # 提取标签
                tags = self._extract_tags_from_keywords(
                    item_data.get('keywords', [])
                ) + ['interior', category_id.replace('_', '-')]

                # 添加到数据库
                success = self.db.add_element(
                    element_id=element_id,
                    domain_id='interior',
                    category_id=category_id,
                    name=item_name,
                    chinese_name=item_data.get('chinese_name'),
                    ai_prompt_template=item_data.get('ai_prompt_template', ''),
                    keywords=item_data.get('keywords', []),
                    tags=tags,
                    reusability_score=item_data.get('reusability_score'),
                    source_prompts=item_data.get('source_prompts', []),
                    learned_from='migrated_from_v4',
                    metadata={
                        'original_category': category_id,
                        'suitable_for': item_data.get('suitable_for', [])
                    }
                )

                if success:
                    migrated += 1

        print(f"   ✅ 迁移完成: {migrated} 个元素")

    def migrate_photography_common(self, json_path: Path):
        """迁移通用摄影库"""
        with open(json_path, 'r', encoding='utf-8') as f:
            lib = json.load(f)

        print(f"   读取文件: {json_path}")

        migrated = 0

        # photography_common.json 的结构类似
        for category_id, category_items in lib.items():
            if category_id == "library_metadata":
                continue

            if not isinstance(category_items, dict):
                continue

            print(f"   迁移类别: {category_id} ({len(category_items)} 个元素)")

            for item_name, item_data in category_items.items():
                if item_name == "library_metadata":
                    continue

                # 生成element_id
                self.element_counter['common'] += 1
                element_id = f"common_{category_id}_{self.element_counter['common']:03d}"

                # 提取标签
                tags = self._extract_tags_from_keywords(
                    item_data.get('keywords', [])
                ) + ['photography', category_id.replace('_', '-')]

                # 添加到数据库
                success = self.db.add_element(
                    element_id=element_id,
                    domain_id='common',
                    category_id=category_id,
                    name=item_name,
                    chinese_name=item_data.get('chinese_name'),
                    ai_prompt_template=item_data.get('ai_prompt_template', ''),
                    keywords=item_data.get('keywords', []),
                    tags=tags,
                    reusability_score=item_data.get('reusability_score'),
                    source_prompts=item_data.get('source_prompts', []),
                    learned_from='migrated_from_v4',
                    metadata={
                        'original_category': category_id,
                        'suitable_for': item_data.get('suitable_for', [])
                    }
                )

                if success:
                    migrated += 1

        print(f"   ✅ 迁移完成: {migrated} 个元素")

    def _extract_tags_from_keywords(self, keywords: list) -> list:
        """从关键词中提取标签"""
        if not keywords:
            return []

        tags = []
        for kw in keywords[:5]:  # 最多取前5个关键词作为标签
            # 简化处理：将关键词转为标签格式
            tag = kw.lower().replace(' ', '-').replace('_', '-')
            if len(tag) > 2 and len(tag) < 30:
                tags.append(tag)

        return tags

    def show_migration_stats(self):
        """显示迁移统计"""
        stats = self.db.get_stats()

        print(f"\n📊 迁移统计:")
        print(f"   总元素数: {stats['total_elements']}")
        print(f"   总标签数: {stats['total_tags']}")
        print(f"\n   各领域:")

        for domain in stats['domains']:
            if domain['total_elements'] > 0:
                print(f"   - {domain['name']:10s}: {domain['total_elements']:3d} 个元素")

        if stats.get('top_tags'):
            print(f"\n   热门标签（前10）:")
            for tag_info in stats['top_tags'][:10]:
                print(f"   - {tag_info['tag']:20s}: {tag_info['count']} 次")

    def close(self):
        """关闭数据库连接"""
        self.db.close()


def main():
    """主函数"""
    migrator = LibraryMigrator()

    try:
        migrator.migrate_all()
    except Exception as e:
        print(f"\n❌ 迁移过程出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        migrator.close()


if __name__ == "__main__":
    main()
