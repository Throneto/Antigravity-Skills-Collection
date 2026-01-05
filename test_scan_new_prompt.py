#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试扫描新的复杂Prompt"""

from learner import HybridLearner
from smart_reviewer import SmartReviewer
import json

# 读取prompt
with open('test_new_prompt.txt', 'r') as f:
    prompt_text = f.read()

print("="*70)
print("  🔍 扫描新Prompt - 圣诞海报创意")
print("="*70)
print(f"\n📝 Prompt长度: {len(prompt_text)} 字符\n")

# 初始化学习器
learner = HybridLearner()
reviewer = SmartReviewer()

# 提取特征
print("🔍 步骤 1: 特征提取...\n")
result = learner.extract_and_classify(prompt_text)

print(f"✅ 检测到 {result['total_detected']} 个特征")
print(f"   新特征: {len(result['new_features'])} 个")
print(f"   已存在: {len(result['existing_features'])} 个\n")

if result['new_features']:
    print("="*70)
    print("  📋 新特征详情")
    print("="*70)

    for idx, feature in enumerate(result['new_features'], 1):
        print(f"\n{idx}. 类别: {feature['category']}")
        print(f"   描述: {feature.get('raw_text', '')}")
        print(f"   置信度: {feature.get('confidence', 0)*100:.0f}%")
        print(f"   方法: {feature.get('method', 'unknown')}")

    # 智能审核
    print("\n" + "="*70)
    print("  🤖 步骤 2: 智能审核")
    print("="*70 + "\n")

    review_results = reviewer.batch_review(result['new_features'])

    print(f"📊 审核结果:")
    print(f"   🎉 自动批准 (≥90%): {len(review_results['auto_approve'])} 个")
    print(f"   🤔 需要审核 (70-90%): {len(review_results['manual_review'])} 个")
    print(f"   ⚠️  低置信度 (50-70%): {len(review_results['low_confidence'])} 个")
    print(f"   ❌ 建议拒绝 (<50%): {len(review_results['auto_reject'])} 个\n")

    # 自动批准的
    if review_results['auto_approve']:
        print("="*70)
        print("🎉 自动批准的特征（可直接添加到库）:")
        print("="*70)
        for analysis in review_results['auto_approve']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n✅ [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")
            print(f"   - 规则质量: {analysis['scores']['rule_quality']*100:.0f}%")
            print(f"   - 描述质量: {analysis['scores']['description_quality']*100:.0f}%")
            print(f"   - 复用性: {analysis['scores']['reusability']*100:.0f}%")
            print(f"   - 类别重要性: {analysis['scores']['importance']*100:.0f}%")

    # 需要人工审核的
    if review_results['manual_review']:
        print("\n" + "="*70)
        print("🤔 需要人工审核的特征:")
        print("="*70)
        for analysis in review_results['manual_review']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n🟡 [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")
            print(f"   理由: {analysis['reason']}")

    # 低置信度的
    if review_results['low_confidence']:
        print("\n" + "="*70)
        print("⚠️  低置信度特征（建议仔细审核）:")
        print("="*70)
        for analysis in review_results['low_confidence']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n⚠️  [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")
            print(f"   理由: {analysis['reason']}")

else:
    print("ℹ️  未发现新特征（所有特征都已存在于库中）\n")

print("\n" + "="*70)
print("  ✅ 扫描完成")
print("="*70)
