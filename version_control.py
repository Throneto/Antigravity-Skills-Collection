#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本控制器 (Version Controller)
自动备份、版本管理、回滚支持
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional


class VersionController:
    """版本控制器"""

    def __init__(self, library_path: str = "extracted_results/facial_features_library.json"):
        self.library_path = library_path
        self.backup_dir = "extracted_results/backups"
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, reason: str = "auto") -> str:
        """创建备份"""
        if not os.path.exists(self.library_path):
            raise FileNotFoundError(f"库文件不存在: {self.library_path}")

        # 读取当前版本
        with open(self.library_path, 'r', encoding='utf-8') as f:
            library = json.load(f)

        version = library.get('library_metadata', {}).get('version', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 备份文件名
        backup_filename = f"facial_features_library_v{version}_{timestamp}_{reason}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        # 复制文件
        shutil.copy2(self.library_path, backup_path)

        print(f"✅ 备份已创建: {backup_path}")
        return backup_path

    def list_backups(self) -> List[Dict]:
        """列出所有备份"""
        backups = []

        if not os.path.exists(self.backup_dir):
            return backups

        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)

                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'modified': datetime.fromtimestamp(stat.st_mtime)
                })

        # 按修改时间排序
        backups.sort(key=lambda x: x['modified'], reverse=True)
        return backups

    def restore_backup(self, backup_path: str) -> bool:
        """恢复备份"""
        if not os.path.exists(backup_path):
            print(f"❌ 备份文件不存在: {backup_path}")
            return False

        # 先备份当前版本
        self.create_backup(reason="before_restore")

        # 恢复
        shutil.copy2(backup_path, self.library_path)
        print(f"✅ 已恢复备份: {backup_path}")
        return True

    def get_version_info(self, filepath: Optional[str] = None) -> Dict:
        """获取版本信息"""
        if filepath is None:
            filepath = self.library_path

        with open(filepath, 'r', encoding='utf-8') as f:
            library = json.load(f)

        metadata = library.get('library_metadata', {})

        return {
            'version': metadata.get('version', 'unknown'),
            'creation_date': metadata.get('creation_date', 'unknown'),
            'last_updated': metadata.get('last_updated', 'unknown'),
            'total_categories': metadata.get('total_categories', 0),
            'total_classifications': metadata.get('total_classifications', 0),
            'description': metadata.get('description', '')
        }

    def increment_version(self, filepath: Optional[str] = None) -> str:
        """增加版本号（小版本）"""
        if filepath is None:
            filepath = self.library_path

        version_info = self.get_version_info(filepath)
        current_version = version_info['version']

        try:
            # 解析版本号 (例如: "1.5" -> 1.6)
            parts = current_version.split('.')
            major = int(parts[0])
            minor = int(parts[1]) if len(parts) > 1 else 0

            # 增加小版本
            minor += 1
            new_version = f"{major}.{minor}"

            return new_version
        except:
            # 如果解析失败，返回默认版本
            return "1.0"

    def compare_versions(self, version1: str, version2: str) -> int:
        """比较两个版本号
        返回: 1 if version1 > version2, -1 if version1 < version2, 0 if equal
        """
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]

            # 补齐长度
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts += [0] * (max_len - len(v1_parts))
            v2_parts += [0] * (max_len - len(v2_parts))

            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1

            return 0
        except:
            return 0


if __name__ == "__main__":
    # 测试
    vc = VersionController()

    print("📚 版本控制器测试\n")

    # 显示当前版本
    info = vc.get_version_info()
    print(f"当前版本: v{info['version']}")
    print(f"分类总数: {info['total_classifications']}")
    print()

    # 列出备份
    backups = vc.list_backups()
    print(f"备份文件数: {len(backups)}")
    if backups:
        print("\n最近的备份:")
        for backup in backups[:3]:
            print(f"  - {backup['filename']}")
            print(f"    时间: {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    大小: {backup['size']/1024:.1f} KB")
