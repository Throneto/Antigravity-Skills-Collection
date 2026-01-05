#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - Quick Test
一键运行完整的自动学习系统测试
"""

import json
from auto_learn_workflow import AutoLearnWorkflow
from version_control import VersionController


def print_header(text):
    """打印美观的标题"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def main():
    """运行快速测试"""
    print_header("🧪 自动学习系统 - 快速测试")

    # 初始化
    workflow = AutoLearnWorkflow()
    vc = VersionController()

    # 显示当前库状态
    print_header("📊 步骤 1: 查看当前库状态")
    version_info = vc.get_version_info()
    print(f"✅ 当前版本: v{version_info['version']}")
    print(f"✅ 当前分类数: {version_info['total_classifications']}")
    print(f"✅ 当前类别数: {version_info['total_categories']}")

    # 测试Prompt
    test_prompts = [
        "A woman with long flowing red hair and fair porcelain skin",
        "A girl with short wavy blonde hair and tan skin tone",
        "Portrait with silver hair and golden skin, wearing elegant dress"
    ]

    print_header("📝 步骤 2: 测试特征提取")
    print("我们将测试以下3个Prompts:\n")

    for idx, prompt in enumerate(test_prompts, 1):
        print(f"{idx}. \"{prompt}\"")

    print("\n按Enter键开始测试...")
    input()

    # 扫描第一个Prompt（交互式）
    print_header("🔍 步骤 3: 扫描第一个Prompt（演示模式）")
    print(f"Prompt: \"{test_prompts[0]}\"\n")

    # 只提取和显示，不实际更新
    from learner import HybridLearner
    from smart_reviewer import SmartReviewer

    learner = HybridLearner()
    reviewer = SmartReviewer()

    result = learner.extract_and_classify(test_prompts[0])

    print(f"✅ 检测到 {result['total_detected']} 个特征")
    print(f"   新特征: {len(result['new_features'])} 个")
    print(f"   已存在: {len(result['existing_features'])} 个\n")

    if result['new_features']:
        print("📋 检测到的新特征:\n")
        for feature in result['new_features']:
            print(f"  • [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"    置信度: {feature.get('confidence', 0)*100:.0f}%")
            print()

        # 智能审核
        print_header("🤖 步骤 4: 智能审核")
        review_results = reviewer.batch_review(result['new_features'])

        print(f"📊 审核结果:")
        print(f"   🎉 自动批准: {len(review_results['auto_approve'])} 个 (置信度 ≥90%)")
        print(f"   🤔 需要审核: {len(review_results['manual_review'])} 个 (置信度 70-90%)")
        print(f"   ❌ 建议拒绝: {len(review_results['auto_reject'])} 个 (置信度 <50%)")
        print()

        if review_results['auto_approve']:
            print("✅ 自动批准的特征:\n")
            for analysis in review_results['auto_approve']:
                feature = analysis['feature']
                score = analysis['total_score']
                print(f"  • [{feature['category']}] {feature.get('raw_text', '')}")
                print(f"    总评分: {score*100:.0f}%")
                print(f"    规则质量: {analysis['scores']['rule_quality']*100:.0f}%")
                print(f"    描述质量: {analysis['scores']['description_quality']*100:.0f}%")
                print(f"    复用性: {analysis['scores']['reusability']*100:.0f}%")
                print(f"    类别重要性: {analysis['scores']['importance']*100:.0f}%")
                print()

        if review_results['manual_review']:
            print("🟡 需要人工审核的特征:\n")
            for analysis in review_results['manual_review']:
                feature = analysis['feature']
                score = analysis['total_score']
                print(f"  • [{feature['category']}] {feature.get('raw_text', '')}")
                print(f"    总评分: {score*100:.0f}%")
                print(f"    原因: {analysis['reason']}")
                print()

    print_header("🎉 步骤 5: 测试完成！")

    print("✅ 系统功能正常！\n")
    print("📚 接下来你可以：\n")
    print("1. 查看完整测试指南：")
    print("   cat TESTING_GUIDE.md\n")
    print("2. 运行实际的自动更新（会修改库）：")
    print("   python3 auto_learn_workflow.py scan \"Your prompt here\"\n")
    print("3. 批量扫描所有Prompts：")
    print("   python3 auto_learn_workflow.py batch\n")
    print("4. 自动批准高分特征：")
    print("   python3 auto_learn_workflow.py scan-auto \"Your prompt here\"\n")

    print_header("💡 提示")
    print("本测试脚本只演示功能，不会修改库文件。")
    print("要实际更新库，请使用 auto_learn_workflow.py\n")


if __name__ == "__main__":
    main()
