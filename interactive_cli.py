#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式CLI界面 (Interactive CLI)
美观的命令行界面，实时审核和批准
"""

import sys
import json
from typing import Dict, List, Optional
from smart_reviewer import SmartReviewer
from auto_updater import AutoUpdater
from version_control import VersionController


class InteractiveCLI:
    """交互式命令行界面"""

    def __init__(self):
        self.reviewer = SmartReviewer()
        self.updater = AutoUpdater()
        self.version_controller = VersionController()

        # 颜色代码（ANSI）
        self.colors = {
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BLUE': '\033[94m',
            'CYAN': '\033[96m',
            'MAGENTA': '\033[95m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        }

    def color_text(self, text: str, color: str) -> str:
        """给文本上色"""
        return f"{self.colors.get(color, '')}{text}{self.colors['END']}"

    def print_header(self, text: str) -> None:
        """打印标题"""
        print("\n" + "="*70)
        print(self.color_text(f"  {text}", 'BOLD'))
        print("="*70 + "\n")

    def print_feature(self, feature: Dict, analysis: Optional[Dict] = None) -> None:
        """打印特征信息"""
        category = feature.get('category', '')
        raw_text = feature.get('raw_text', '')

        print(f"{self.color_text('类别:', 'CYAN')} {category}")
        print(f"{self.color_text('描述:', 'CYAN')} {raw_text}")

        if analysis:
            score = analysis['total_score']
            decision = analysis['decision']

            # 根据决策选择颜色
            if decision == 'AUTO_APPROVE':
                decision_color = 'GREEN'
                decision_text = '✅ 自动批准'
            elif decision == 'MANUAL_REVIEW':
                decision_color = 'YELLOW'
                decision_text = '🤔 人工审核'
            else:
                decision_color = 'RED'
                decision_text = '❌ 建议拒绝'

            print(f"{self.color_text('置信度:', 'CYAN')} {score:.0%}")
            print(f"{self.color_text('决策:', 'CYAN')} {self.color_text(decision_text, decision_color)}")
            print(f"{self.color_text('理由:', 'CYAN')} {analysis['reason']}")

    def review_features_interactive(self, features: List[Dict]) -> Dict:
        """交互式审核特征"""
        self.print_header("🔍 交互式特征审核")

        # 先批量审核
        review_results = self.reviewer.batch_review(features)

        # 显示汇总
        print(self.reviewer.generate_review_summary(review_results))

        # 准备要添加的特征
        to_add = []

        # 1. 自动批准的特征
        if review_results['auto_approve']:
            print("\n" + "="*70)
            print(self.color_text("🎉 自动批准特征", 'BOLD'))
            print("="*70)

            for analysis in review_results['auto_approve']:
                to_add.append(analysis['feature'])

            print(f"\n✅ {len(review_results['auto_approve'])} 个特征将被自动添加\n")

        # 2. 需要人工审核的特征
        if review_results['manual_review']:
            print("\n" + "="*70)
            print(self.color_text("🤔 人工审核特征", 'BOLD'))
            print("="*70 + "\n")

            for idx, analysis in enumerate(review_results['manual_review'], 1):
                print(f"\n特征 {idx}/{len(review_results['manual_review'])}:")
                print("-" * 70)
                self.print_feature(analysis['feature'], analysis)
                print("-" * 70)

                # 询问用户
                while True:
                    choice = input(f"\n{self.color_text('是否添加此特征？', 'BOLD')} "
                                 f"[{self.color_text('y', 'GREEN')}/"
                                 f"{self.color_text('n', 'RED')}/"
                                 f"{self.color_text('s', 'YELLOW')}跳过]: ").lower()

                    if choice == 'y':
                        to_add.append(analysis['feature'])
                        print(self.color_text("✅ 已标记为添加", 'GREEN'))
                        break
                    elif choice == 'n':
                        print(self.color_text("❌ 已拒绝", 'RED'))
                        break
                    elif choice == 's':
                        print(self.color_text("⏭️  已跳过", 'YELLOW'))
                        break
                    else:
                        print(self.color_text("⚠️  无效输入，请输入 y/n/s", 'RED'))

        # 3. 显示添加摘要
        if to_add:
            print("\n" + "="*70)
            print(self.color_text(f"📋 准备添加 {len(to_add)} 个特征", 'BOLD'))
            print("="*70 + "\n")

            # 按类别分组显示
            by_category = {}
            for feature in to_add:
                category = feature['category']
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(feature['raw_text'])

            for category, texts in sorted(by_category.items()):
                print(f"{self.color_text(category, 'CYAN')}: {len(texts)} 个")
                for text in texts:
                    print(f"  - {text}")

            # 最终确认
            print("\n" + "="*70)
            confirm = input(f"\n{self.color_text('确认添加以上特征到库？', 'BOLD')} "
                          f"[{self.color_text('y', 'GREEN')}/"
                          f"{self.color_text('n', 'RED')}]: ").lower()

            if confirm == 'y':
                return {'approved': to_add, 'rejected': []}
            else:
                print(self.color_text("\n❌ 已取消添加", 'RED'))
                return {'approved': [], 'rejected': to_add}
        else:
            print(self.color_text("\nℹ️  没有特征被批准添加", 'YELLOW'))
            return {'approved': [], 'rejected': []}

    def run_auto_update_workflow(self, features: List[Dict]) -> None:
        """运行完整的自动更新工作流"""
        self.print_header("🚀 自动库更新工作流")

        # 显示当前库状态
        version_info = self.version_controller.get_version_info()
        version_str = f"v{version_info['version']}"
        print(f"当前库版本: {self.color_text(version_str, 'CYAN')}")
        print(f"总分类数: {self.color_text(str(version_info['total_classifications']), 'CYAN')}")
        print(f"总类别数: {self.color_text(str(version_info['total_categories']), 'CYAN')}\n")

        # 交互式审核
        approval_results = self.review_features_interactive(features)

        approved_features = approval_results['approved']

        if not approved_features:
            print(self.color_text("\n✋ 没有特征被批准，工作流结束", 'YELLOW'))
            return

        # 执行更新
        print("\n" + "="*70)
        print(self.color_text("🔄 执行库更新...", 'BOLD'))
        print("="*70 + "\n")

        results = self.updater.batch_add_features(approved_features, create_backup=True)

        # 显示结果
        print("\n" + "="*70)
        print(self.color_text("✅ 更新完成！", 'BOLD'))
        print("="*70 + "\n")

        print(f"{self.color_text('成功添加:', 'GREEN')} {len(results['success'])} 个")
        print(f"{self.color_text('失败:', 'RED')} {len(results['failed'])} 个\n")

        # 显示新版本信息
        new_version_info = self.version_controller.get_version_info()
        new_version_str = f"v{new_version_info['version']}"
        print(f"新版本: {self.color_text(new_version_str, 'CYAN')}")
        print(f"新总分类数: {self.color_text(str(new_version_info['total_classifications']), 'CYAN')}")

        # 显示备份信息
        backups = self.version_controller.list_backups()
        if backups:
            latest_backup = backups[0]
            print(f"\n最新备份: {self.color_text(latest_backup['filename'], 'CYAN')}")


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 interactive_cli.py <features_json_file>")
        print("\n示例:")
        print("  python3 interactive_cli.py extracted_results/new_features.json")
        return

    features_file = sys.argv[1]

    if not os.path.exists(features_file):
        print(f"❌ 文件不存在: {features_file}")
        return

    # 加载特征
    with open(features_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 支持两种格式
    if isinstance(data, list):
        features = data
    else:
        features = data.get('features', data.get('new_features', []))

    if not features:
        print("❌ 未找到特征数据")
        return

    # 运行交互式CLI
    cli = InteractiveCLI()
    cli.run_auto_update_workflow(features)


if __name__ == "__main__":
    import os
    main()
