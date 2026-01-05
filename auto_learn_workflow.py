#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动学习工作流 (Auto Learning Workflow)
完整的端到端自动化流程：扫描 → 审核 → 批准 → 更新库

使用方法：
  python3 auto_learn_workflow.py scan "Your prompt text here"
  python3 auto_learn_workflow.py batch
  python3 auto_learn_workflow.py interactive <features_json>
"""

import sys
import json
import os
from typing import Dict, List
from learner import HybridLearner
from smart_reviewer import SmartReviewer
from auto_updater import AutoUpdater
from interactive_cli import InteractiveCLI
from version_control import VersionController


class AutoLearnWorkflow:
    """完整的自动学习工作流"""

    def __init__(self):
        self.learner = HybridLearner()
        self.reviewer = SmartReviewer()
        self.updater = AutoUpdater()
        self.cli = InteractiveCLI()
        self.version_controller = VersionController()

        # 颜色代码
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.BLUE = '\033[94m'
        self.CYAN = '\033[96m'
        self.BOLD = '\033[1m'
        self.END = '\033[0m'

    def print_banner(self):
        """打印欢迎横幅"""
        print("\n" + "="*70)
        print(f"{self.CYAN}{self.BOLD}")
        print("  🤖 自动学习工作流 - Auto Learning Workflow")
        print(f"{self.END}")
        print("="*70 + "\n")

    def scan_single_prompt(self, prompt_text: str, auto_update: bool = False):
        """扫描单个Prompt并可选自动更新

        Args:
            prompt_text: 要扫描的Prompt文本
            auto_update: 是否自动更新库（True=自动批准高分特征）
        """
        self.print_banner()

        print(f"{self.BLUE}📝 步骤 1/4: 特征提取{self.END}")
        print(f"   扫描文本: \"{prompt_text[:60]}...\"" if len(prompt_text) > 60 else f"   扫描文本: \"{prompt_text}\"")
        print()

        # 提取特征
        result = self.learner.extract_and_classify(prompt_text)

        if result['total_detected'] == 0:
            print(f"{self.YELLOW}ℹ️  未检测到任何特征{self.END}\n")
            return

        print(f"{self.GREEN}✅ 检测到 {result['total_detected']} 个特征{self.END}")
        print(f"   新特征: {len(result['new_features'])} 个")
        print(f"   已存在: {len(result['existing_features'])} 个\n")

        if not result['new_features']:
            print(f"{self.YELLOW}ℹ️  所有特征都已存在于库中{self.END}\n")
            return

        # 智能审核
        print(f"{self.BLUE}📊 步骤 2/4: 智能审核{self.END}")
        review_results = self.reviewer.batch_review(result['new_features'])

        print(f"   自动批准: {self.GREEN}{len(review_results['auto_approve'])}{self.END} 个")
        print(f"   需要审核: {self.YELLOW}{len(review_results['manual_review'])}{self.END} 个")
        print(f"   建议拒绝: {self.RED}{len(review_results['auto_reject'])}{self.END} 个\n")

        # 显示自动批准的特征
        if review_results['auto_approve']:
            print(f"{self.GREEN}🎉 自动批准的特征:{self.END}")
            for analysis in review_results['auto_approve']:
                feature = analysis['feature']
                print(f"   ✅ [{feature['category']}] {feature.get('raw_text', '')} ({analysis['total_score']:.0%})")
            print()

        # 显示需要审核的特征
        if review_results['manual_review']:
            print(f"{self.YELLOW}🤔 需要人工审核的特征:{self.END}")
            for analysis in review_results['manual_review']:
                feature = analysis['feature']
                print(f"   🟡 [{feature['category']}] {feature.get('raw_text', '')} ({analysis['total_score']:.0%})")
            print()

        # 自动更新或交互式选择
        if auto_update:
            # 自动模式：只添加自动批准的特征
            if review_results['auto_approve']:
                print(f"{self.BLUE}🔄 步骤 3/4: 自动更新库{self.END}")
                features_to_add = [a['feature'] for a in review_results['auto_approve']]
                self._perform_update(features_to_add)
            else:
                print(f"{self.YELLOW}ℹ️  没有特征达到自动批准阈值{self.END}\n")
        else:
            # 交互式模式
            print(f"{self.BLUE}🤔 步骤 3/4: 交互式审核{self.END}")
            self._interactive_approval(result['new_features'])

    def _interactive_approval(self, features: List[Dict]):
        """交互式批准流程"""
        approval_result = self.cli.review_features_interactive(features)

        if approval_result['approved']:
            self._perform_update(approval_result['approved'])
        else:
            print(f"{self.YELLOW}✋ 没有特征被批准，流程结束{self.END}\n")

    def _perform_update(self, features: List[Dict]):
        """执行库更新"""
        print(f"{self.BLUE}🔄 步骤 4/4: 更新库{self.END}\n")

        # 显示当前版本
        version_info = self.version_controller.get_version_info()
        print(f"   当前版本: {self.CYAN}v{version_info['version']}{self.END}")
        print(f"   当前分类数: {self.CYAN}{version_info['total_classifications']}{self.END}\n")

        # 执行更新
        results = self.updater.batch_add_features(features, create_backup=True)

        # 显示结果
        print(f"\n{self.GREEN}{'='*70}{self.END}")
        print(f"{self.GREEN}{self.BOLD}✅ 更新完成！{self.END}")
        print(f"{self.GREEN}{'='*70}{self.END}\n")

        print(f"   成功添加: {self.GREEN}{len(results['success'])}{self.END} 个")
        print(f"   失败: {self.RED}{len(results['failed'])}{self.END} 个\n")

        # 显示新版本
        new_version_info = self.version_controller.get_version_info()
        print(f"   新版本: {self.CYAN}v{new_version_info['version']}{self.END}")
        print(f"   新分类数: {self.CYAN}{new_version_info['total_classifications']}{self.END}\n")

        # 显示备份
        backups = self.version_controller.list_backups()
        if backups:
            latest_backup = backups[0]
            print(f"   最新备份: {self.CYAN}{latest_backup['filename']}{self.END}\n")

    def batch_scan_mode(self, prompts_file: str = "extracted_results/extracted_modules.json"):
        """批量扫描模式"""
        self.print_banner()

        print(f"{self.BLUE}📚 批量扫描模式{self.END}")
        print(f"   读取文件: {prompts_file}\n")

        if not os.path.exists(prompts_file):
            print(f"{self.RED}❌ 文件不存在: {prompts_file}{self.END}\n")
            return

        # 使用learner的批量扫描
        all_new_features = self.learner.batch_scan_prompts(prompts_file)

        if not all_new_features:
            print(f"{self.YELLOW}ℹ️  未发现新特征{self.END}\n")
            return

        # 汇总所有特征
        all_features = []
        for category, features in all_new_features.items():
            all_features.extend(features)

        print(f"\n{self.BLUE}📊 开始智能审核{self.END}\n")

        # 智能审核
        review_results = self.reviewer.batch_review(all_features)

        print(f"   自动批准: {self.GREEN}{len(review_results['auto_approve'])}{self.END} 个")
        print(f"   需要审核: {self.YELLOW}{len(review_results['manual_review'])}{self.END} 个")
        print(f"   建议拒绝: {self.RED}{len(review_results['auto_reject'])}{self.END} 个\n")

        # 交互式批准
        if review_results['auto_approve'] or review_results['manual_review']:
            self._interactive_approval(all_features)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("\n🤖 自动学习工作流 - 使用说明\n")
        print("=" * 70)
        print("\n使用方法：\n")
        print("  1. 扫描单个Prompt（交互式）：")
        print("     python3 auto_learn_workflow.py scan \"Your prompt text here\"\n")
        print("  2. 扫描单个Prompt（自动批准）：")
        print("     python3 auto_learn_workflow.py scan-auto \"Your prompt text here\"\n")
        print("  3. 批量扫描所有Prompts：")
        print("     python3 auto_learn_workflow.py batch\n")
        print("  4. 交互式审核已有特征文件：")
        print("     python3 auto_learn_workflow.py interactive <features.json>\n")
        print("=" * 70)
        print("\n示例：\n")
        print('  python3 auto_learn_workflow.py scan "A woman with long flowing red hair, wearing elegant red silk qipao"')
        print('  python3 auto_learn_workflow.py scan-auto "Portrait of a girl with short blonde hair and fair skin"')
        print('  python3 auto_learn_workflow.py batch')
        print()
        return

    workflow = AutoLearnWorkflow()
    command = sys.argv[1]

    if command == "scan":
        if len(sys.argv) < 3:
            print("❌ 请提供要扫描的Prompt文本\n")
            print('示例: python3 auto_learn_workflow.py scan "Your prompt here"')
            return

        prompt_text = sys.argv[2]
        workflow.scan_single_prompt(prompt_text, auto_update=False)

    elif command == "scan-auto":
        if len(sys.argv) < 3:
            print("❌ 请提供要扫描的Prompt文本\n")
            print('示例: python3 auto_learn_workflow.py scan-auto "Your prompt here"')
            return

        prompt_text = sys.argv[2]
        workflow.scan_single_prompt(prompt_text, auto_update=True)

    elif command == "batch":
        workflow.batch_scan_mode()

    elif command == "interactive":
        if len(sys.argv) < 3:
            print("❌ 请提供特征文件路径\n")
            print('示例: python3 auto_learn_workflow.py interactive features.json')
            return

        features_file = sys.argv[2]

        if not os.path.exists(features_file):
            print(f"❌ 文件不存在: {features_file}\n")
            return

        with open(features_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        features = data if isinstance(data, list) else data.get('features', data.get('new_features', []))

        if not features:
            print("❌ 未找到特征数据\n")
            return

        workflow.cli.run_auto_update_workflow(features)

    else:
        print(f"❌ 未知命令: {command}\n")
        print("支持的命令: scan, scan-auto, batch, interactive")


if __name__ == "__main__":
    main()
