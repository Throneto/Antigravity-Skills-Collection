#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描案例342 - 日本街头摄影风格"""

from learner import HybridLearner
from smart_reviewer import SmartReviewer
import json

# 读取prompt
with open('case_342_prompt.txt', 'r') as f:
    prompt_text = f.read()

print("\n" + "="*80)
print("  🔍 扫描案例342 - 日本街头摄影风格（小酒吧场景）")
print("="*80)
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
    print("="*80)
    print("  📋 新特征详情")
    print("="*80)

    # 按类别分组
    by_category = {}
    for feature in result['new_features']:
        cat = feature['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(feature)

    for category, features in sorted(by_category.items()):
        print(f"\n【{category}】 ({len(features)} 个)")
        for idx, feature in enumerate(features, 1):
            print(f"  {idx}. {feature.get('raw_text', '')}")
            print(f"     置信度: {feature.get('confidence', 0)*100:.0f}% | 方法: {feature.get('method', 'unknown')}")

    # 智能审核
    print("\n" + "="*80)
    print("  🤖 步骤 2: 智能审核")
    print("="*80 + "\n")

    review_results = reviewer.batch_review(result['new_features'])

    print(f"📊 审核结果:")
    print(f"   🎉 自动批准 (≥90%): {len(review_results['auto_approve'])} 个")
    print(f"   🤔 需要审核 (70-90%): {len(review_results['manual_review'])} 个")
    print(f"   ⚠️  低置信度 (50-70%): {len(review_results['low_confidence'])} 个")
    print(f"   ❌ 建议拒绝 (<50%): {len(review_results['auto_reject'])} 个\n")

    # 需要人工审核的（70-90分）
    if review_results['manual_review']:
        print("="*80)
        print("🤔 需要人工审核的特征（70-90分）:")
        print("="*80)
        for analysis in review_results['manual_review']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n🟡 [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")

    # 自动批准的（≥90分）
    if review_results['auto_approve']:
        print("\n" + "="*80)
        print("🎉 自动批准的特征（≥90分）:")
        print("="*80)
        for analysis in review_results['auto_approve']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n✅ [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")

else:
    print("ℹ️  未发现新特征（所有特征都已存在于库中）\n")

# 显示已存在的特征
if result['existing_features']:
    print("\n" + "="*80)
    print(f"  ✅ 已存在的特征 ({len(result['existing_features'])} 个)")
    print("="*80)

    existing_by_cat = {}
    for feature in result['existing_features']:
        cat = feature['category']
        if cat not in existing_by_cat:
            existing_by_cat[cat] = []
        existing_by_cat[cat].append(feature.get('raw_text', ''))

    for category, texts in sorted(existing_by_cat.items())[:5]:  # 只显示前5个类别
        print(f"\n【{category}】: {', '.join(texts[:2])}" + (f" ...等{len(texts)}个" if len(texts) > 2 else ""))

print("\n" + "="*80)
print("  ✅ 扫描完成")
print("="*80)

# 总结
print("\n💡 总结:")
print(f"   • 这个prompt包含{result['total_detected']}个可识别特征")
print(f"   • 其中{len(result['new_features'])}个是新特征")
if review_results.get('auto_approve'):
    print(f"   • {len(review_results['auto_approve'])}个特征达到自动批准标准（≥90分）")
if review_results.get('manual_review'):
    print(f"   • {len(review_results['manual_review'])}个特征需要人工审核（70-90分）")

print("\n🎨 Prompt风格特点:")
print("   • 日本街头摄影风格（荒木经惟、森山大道）")
print("   • 1980年代模拟胶片美学")
print("   • 复古琥珀色调，低饱和度")
print("   • 近距离人物肖像，浅景深")
print()
