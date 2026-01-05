#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量学习器 V2 - 从目录批量学习提示词
支持多种格式，自动质量检查，生成详细报告
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from universal_learner_v2 import UniversalLearnerV2
from element_db import ElementDB
from txt_to_json_converter import TxtToJsonConverter


class PromptQualityChecker:
    """提示词质量检查器"""

    def __init__(self):
        self.min_length = 50  # 最小长度
        self.max_length = 10000  # 最大长度

    def check_quality(self, prompt_data: Dict) -> Tuple[bool, str, int]:
        """
        检查提示词质量

        Returns:
            (is_valid, reason, quality_score)
        """
        original = prompt_data.get('original_prompt', '')

        # 检查1: 长度
        if len(original) < self.min_length:
            return False, f"太短 ({len(original)}字符)", 0

        if len(original) > self.max_length:
            return False, f"太长 ({len(original)}字符)", 0

        # 检查2: 是否有modules
        modules = prompt_data.get('modules', {})
        if not modules or len(modules) == 0:
            return False, "缺少modules结构", 2

        # 检查3: modules复杂度
        module_count = len(modules)
        if module_count < 3:
            return True, "结构简单", 5  # 可以学习，但质量一般

        # 检查4: 是否有数组数据
        has_arrays = False
        array_count = 0
        for key, value in modules.items():
            if isinstance(value, list) and len(value) > 0:
                has_arrays = True
                array_count += 1

        # 计算质量分数
        quality_score = 5  # 基础分
        quality_score += min(module_count, 10)  # modules数量 (最多+10分)
        quality_score += array_count * 2  # 数组数量 (每个+2分)

        if quality_score >= 15:
            return True, "高质量", min(quality_score, 10)
        elif quality_score >= 10:
            return True, "中等质量", min(quality_score, 10)
        else:
            return True, "基础质量", min(quality_score, 10)


class BatchLearner:
    """批量学习器"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.learner = UniversalLearnerV2(db_path)
        self.quality_checker = PromptQualityChecker()
        self.txt_converter = TxtToJsonConverter()

        self.stats = {
            'total_files': 0,
            'processed': 0,
            'skipped': 0,
            'failed': 0,
            'total_added': 0,
            'total_extracted': 0,
            'by_quality': {
                '高质量': 0,
                '中等质量': 0,
                '基础质量': 0,
                '低质量': 0
            },
            'skip_reasons': {},
            'failed_files': []
        }

    def load_prompt_file(self, file_path: Path) -> Dict:
        """加载提示词文件（支持JSON和TXT）"""
        try:
            # 尝试JSON格式
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError:
            # TXT格式 - 使用转换器解析
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    txt_content = f.read()
                    # 使用转换器自动提取modules
                    return self.txt_converter.convert_txt_to_prompt_data(
                        txt_content,
                        file_path.name
                    )
            except Exception as e:
                raise Exception(f"无法读取文件: {e}")

    def learn_from_directory(self, directory: str,
                            quality_threshold: int = 0,
                            dry_run: bool = False,
                            max_files: int = None) -> Dict:
        """
        从目录批量学习

        Args:
            directory: 提示词文件目录
            quality_threshold: 质量阈值（0-10），低于此分数的跳过
            dry_run: 预演模式，只检查不学习
            max_files: 最大处理文件数（测试用）
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

        # 查找所有JSON和TXT文件
        json_files = list(dir_path.glob("*.json"))
        txt_files = list(dir_path.glob("*.txt"))
        all_files = json_files + txt_files

        if max_files:
            all_files = all_files[:max_files]

        self.stats['total_files'] = len(all_files)

        print(f"\n{'='*80}")
        print(f"📚 批量学习器 V2")
        print(f"{'='*80}")
        print(f"目录: {directory}")
        print(f"文件总数: {len(all_files)} (JSON: {len(json_files)}, TXT: {len(txt_files)})")
        print(f"质量阈值: {quality_threshold}/10")
        print(f"模式: {'🔍 预演模式' if dry_run else '✅ 学习模式'}")
        if max_files:
            print(f"限制: 最多处理 {max_files} 个文件")
        print(f"{'='*80}\n")

        # 获取初始数据库状态
        initial_stats = self.learner.db.get_stats()
        initial_elements = initial_stats['total_elements']

        # 处理每个文件
        for idx, file_path in enumerate(all_files, 1):
            print(f"\n[{idx}/{len(all_files)}] 处理: {file_path.name}")

            try:
                # 加载文件
                prompt_data = self.load_prompt_file(file_path)

                # 质量检查
                is_valid, reason, quality_score = self.quality_checker.check_quality(prompt_data)

                if not is_valid:
                    print(f"  ⏭️  跳过: {reason}")
                    self.stats['skipped'] += 1
                    self.stats['skip_reasons'][reason] = self.stats['skip_reasons'].get(reason, 0) + 1
                    continue

                if quality_score < quality_threshold:
                    print(f"  ⏭️  跳过: 质量分数 {quality_score}/10 低于阈值 {quality_threshold}")
                    self.stats['skipped'] += 1
                    self.stats['skip_reasons']['质量分数不足'] = self.stats['skip_reasons'].get('质量分数不足', 0) + 1
                    continue

                print(f"  ✓ 质量: {reason} ({quality_score}/10)")
                self.stats['by_quality'][reason] = self.stats['by_quality'].get(reason, 0) + 1

                if dry_run:
                    print(f"  🔍 预演模式 - 跳过学习")
                    self.stats['processed'] += 1
                    continue

                # 学习
                result = self.learner.learn_from_prompt(prompt_data)

                self.stats['processed'] += 1
                self.stats['total_added'] += result['added']
                self.stats['total_extracted'] += result['added'] + result['skipped']

                print(f"  ✅ 学习完成: 提取 {result['added'] + result['skipped']} 个元素, 添加 {result['added']} 个")

            except Exception as e:
                print(f"  ❌ 失败: {str(e)}")
                self.stats['failed'] += 1
                self.stats['failed_files'].append({
                    'file': file_path.name,
                    'error': str(e)
                })

        # 获取最终数据库状态
        final_stats = self.learner.db.get_stats()
        final_elements = final_stats['total_elements']

        # 生成报告
        report = self._generate_report(initial_elements, final_elements, dry_run)

        return report

    def _generate_report(self, initial_elements: int, final_elements: int, dry_run: bool) -> Dict:
        """生成学习报告"""
        print(f"\n{'='*80}")
        print(f"📊 批量学习报告")
        print(f"{'='*80}\n")

        print(f"文件处理：")
        print(f"  总文件数: {self.stats['total_files']}")
        print(f"  成功处理: {self.stats['processed']}")
        print(f"  跳过: {self.stats['skipped']}")
        print(f"  失败: {self.stats['failed']}")
        print()

        if self.stats['skip_reasons']:
            print(f"跳过原因：")
            for reason, count in sorted(self.stats['skip_reasons'].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {reason}: {count} 个")
            print()

        print(f"质量分布：")
        for quality, count in sorted(self.stats['by_quality'].items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"  • {quality}: {count} 个")
        print()

        if not dry_run:
            print(f"学习成果：")
            print(f"  提取元素总数: {self.stats['total_extracted']}")
            print(f"  新增元素: {self.stats['total_added']}")
            print(f"  去重跳过: {self.stats['total_extracted'] - self.stats['total_added']}")
            print(f"  数据库增长: {initial_elements} → {final_elements} (+{final_elements - initial_elements})")
            print()

        if self.stats['failed_files']:
            print(f"失败文件 ({len(self.stats['failed_files'])}个)：")
            for item in self.stats['failed_files'][:10]:  # 最多显示10个
                print(f"  • {item['file']}: {item['error']}")
            if len(self.stats['failed_files']) > 10:
                print(f"  ... 还有 {len(self.stats['failed_files']) - 10} 个")
            print()

        print(f"{'='*80}\n")

        return {
            'stats': self.stats,
            'initial_elements': initial_elements,
            'final_elements': final_elements,
            'growth': final_elements - initial_elements
        }

    def close(self):
        """关闭学习器"""
        self.learner.close()


# 命令行使用
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='批量学习提示词')
    parser.add_argument('directory', help='提示词文件目录')
    parser.add_argument('--quality', type=int, default=0, help='质量阈值 (0-10), 默认0')
    parser.add_argument('--dry-run', action='store_true', help='预演模式，只检查不学习')
    parser.add_argument('--max-files', type=int, help='最大处理文件数（测试用）')
    parser.add_argument('--db', default='extracted_results/elements.db', help='数据库路径')

    args = parser.parse_args()

    batch_learner = BatchLearner(args.db)

    try:
        report = batch_learner.learn_from_directory(
            directory=args.directory,
            quality_threshold=args.quality,
            dry_run=args.dry_run,
            max_files=args.max_files
        )

        # 导出JSON
        if not args.dry_run and report['growth'] > 0:
            batch_learner.learner.db.export_to_json('extracted_results/universal_elements_library.json')
            print("✅ 已导出到 universal_elements_library.json")

    finally:
        batch_learner.close()
