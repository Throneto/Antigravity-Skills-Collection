#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描新训练提示词"""

from learner import HybridLearner
from smart_reviewer import SmartReviewer
import json

# 读取prompt
with open('new_training_prompt.txt', 'r') as f:
    prompt_text = f.read()

print("\n" + "="*80)
print("  🔍 扫描新训练Prompt - Wes Anderson风格少女肖像")
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

    # 自动批准的
    if review_results['auto_approve']:
        print("="*80)
        print("🎉 自动批准的特征（可直接添加到库）:")
        print("="*80)
        for analysis in review_results['auto_approve']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n✅ [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")
            scores_detail = analysis['scores']
            print(f"   详细评分:")
            print(f"     - 规则质量: {scores_detail['rule_quality']*100:.0f}%")
            print(f"     - 描述质量: {scores_detail['description_quality']*100:.0f}%")
            print(f"     - 复用性: {scores_detail['reusability']*100:.0f}%")
            print(f"     - 类别重要性: {scores_detail['importance']*100:.0f}%")

    # 需要人工审核的
    if review_results['manual_review']:
        print("\n" + "="*80)
        print("🤔 需要人工审核的特征:")
        print("="*80)
        for analysis in review_results['manual_review']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n🟡 [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")
            print(f"   建议: {analysis['reason']}")

    # 低置信度的
    if review_results['low_confidence']:
        print("\n" + "="*80)
        print("⚠️  低置信度特征（建议仔细审核）:")
        print("="*80)
        for analysis in review_results['low_confidence']:
            feature = analysis['feature']
            score = analysis['total_score']
            print(f"\n⚠️  [{feature['category']}] {feature.get('raw_text', '')}")
            print(f"   总评分: {score*100:.0f}%")

    # 保存审核结果供后续添加
    approved_features = []
    for analysis in review_results['auto_approve']:
        approved_features.append(analysis['feature'])
    for analysis in review_results['manual_review']:
        approved_features.append(analysis['feature'])

    if approved_features:
        output = {
            'source': 'new_training_prompt.txt',
            'total_features': len(approved_features),
            'features': approved_features,
            'review_summary': {
                'auto_approve': len(review_results['auto_approve']),
                'manual_review': len(review_results['manual_review']),
                'low_confidence': len(review_results['low_confidence'])
            }
        }

        with open('new_training_features.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print("\n" + "="*80)
        print(f"📁 特征已保存到: new_training_features.json")
        print("="*80)

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

    for category, texts in sorted(existing_by_cat.items()):
        print(f"\n【{category}】: {', '.join(texts[:3])}" + (f" ...等{len(texts)}个" if len(texts) > 3 else ""))

print("\n" + "="*80)
print("  ✅ 扫描完成")
print("="*80)

# 总结
print("\n💡 总结:")
print(f"   • 这个prompt非常详细，包含{result['total_detected']}个可识别特征")
print(f"   • 其中{len(result['new_features'])}个是新特征")
if review_results['auto_approve']:
    print(f"   • {len(review_results['auto_approve'])}个特征达到自动批准标准（≥90分）")
if review_results['manual_review']:
    print(f"   • {len(review_results['manual_review'])}个特征需要人工审核（70-90分）")

print("\n🚀 下一步:")
if approved_features:
    print(f"   发现 {len(approved_features)} 个可添加的特征")
    print("   如果要添加这些特征到库，运行:")
    print("   python3 add_training_features.py")
else:
    print("   未发现需要添加的新特征")
print()
