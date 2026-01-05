#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能审核器 (Smart Reviewer)
自动评估特征质量，根据阈值自动决策
"""

import json
import re
from typing import Dict, List, Tuple
from collections import Counter


class SmartReviewer:
    """智能审核器"""

    def __init__(self):
        # 审核阈值
        self.thresholds = {
            'auto_approve': 0.90,  # 自动批准阈值
            'manual_review': 0.70,  # 人工审核阈值
            'auto_reject': 0.50     # 低于此值自动拒绝
        }

        # 类别重要性权重
        self.category_importance = {
            'hair_styles': 1.0,
            'hair_colors': 1.0,
            'skin_tones': 0.9,
            'clothing_styles': 0.8,
            'accessories': 0.7,
            'poses': 0.7,
            'body_types': 0.8,
            'makeup_styles': 0.95,
            'eye_types': 1.0,
            'face_shapes': 1.0,
            'nose_types': 1.0,
            'lip_types': 1.0
        ,
            'poses': 0.9,              # 姿势对人像很重要
            'expressions': 1.0,        # 表情是人像核心要素
            'clothing_styles': 0.75    # 服装风格中等重要
        }

    def analyze_feature(self, feature: Dict, context: Dict = None) -> Dict:
        """深度分析特征质量

        Args:
            feature: 特征数据
            context: 上下文信息（原始prompt、其他特征等）

        Returns:
            分析结果，包含置信度和决策
        """
        scores = []

        # 1. 基础规则评分
        rule_score = self._evaluate_rule_quality(feature)
        scores.append(('rule_quality', rule_score, 0.3))

        # 2. 描述性评分
        desc_score = self._evaluate_description_quality(feature)
        scores.append(('description_quality', desc_score, 0.3))

        # 3. 复用性评分
        reuse_score = self._evaluate_reusability(feature)
        scores.append(('reusability', reuse_score, 0.2))

        # 4. 类别重要性评分
        importance_score = self._evaluate_category_importance(feature)
        scores.append(('importance', importance_score, 0.2))

        # 加权平均
        total_score = sum(score * weight for _, score, weight in scores)

        # 生成决策
        decision = self._make_decision(total_score)

        return {
            'feature': feature,
            'scores': {name: score for name, score, _ in scores},
            'total_score': total_score,
            'decision': decision,
            'reason': self._generate_reason(scores, decision)
        }

    def _evaluate_rule_quality(self, feature: Dict) -> float:
        """评估规则提取质量"""
        score = 0.5  # 基础分

        # 检查关键词
        raw_text = feature.get('raw_text', '')
        if len(raw_text) > 5:
            score += 0.2

        # 检查置信度
        confidence = feature.get('confidence', 0)
        score += confidence * 0.3

        return min(1.0, score)

    def _evaluate_description_quality(self, feature: Dict) -> float:
        """评估描述质量"""
        raw_text = feature.get('raw_text', '')

        score = 0.3  # 基础分

        # 长度适中 (5-50字符)
        if 5 <= len(raw_text) <= 50:
            score += 0.3

        # 包含颜色、材质等描述词
        descriptive_words = ['long', 'short', 'red', 'blue', 'black', 'white',
                            'elegant', 'casual', 'modern', 'traditional',
                            'silk', 'cotton', 'leather', 'flowing', 'straight',
                            'curly', 'wavy', 'fair', 'pale', 'dark', 'golden']

        word_count = sum(1 for word in descriptive_words if word in raw_text.lower())
        score += min(0.4, word_count * 0.1)

        return min(1.0, score)

    def _evaluate_reusability(self, feature: Dict) -> float:
        """评估复用性"""
        category = feature.get('category', '')
        raw_text = feature.get('raw_text', '')

        # 高复用性类别
        high_reuse_categories = ['hair_styles', 'hair_colors', 'skin_tones',
                                 'eye_types', 'face_shapes', 'makeup_styles']

        if category in high_reuse_categories:
            base_score = 0.8
        else:
            base_score = 0.5

        # 通用性检查（不包含过于具体的品牌、人名等）
        specific_indicators = ['brand', 'logo', 'specific person', 'character name']
        if any(indicator in raw_text.lower() for indicator in specific_indicators):
            base_score -= 0.2

        return max(0.0, min(1.0, base_score))

    def _evaluate_category_importance(self, feature: Dict) -> float:
        """评估类别重要性"""
        category = feature.get('category', '')
        return self.category_importance.get(category, 0.5)

    def _make_decision(self, total_score: float) -> str:
        """根据总分做出决策"""
        if total_score >= self.thresholds['auto_approve']:
            return 'AUTO_APPROVE'
        elif total_score >= self.thresholds['manual_review']:
            return 'MANUAL_REVIEW'
        elif total_score >= self.thresholds['auto_reject']:
            return 'LOW_CONFIDENCE'
        else:
            return 'AUTO_REJECT'

    def _generate_reason(self, scores: List[Tuple], decision: str) -> str:
        """生成决策理由"""
        reasons = []

        for name, score, weight in scores:
            if score >= 0.8:
                reasons.append(f"✅ {name} 优秀 ({score:.0%})")
            elif score >= 0.6:
                reasons.append(f"🟡 {name} 良好 ({score:.0%})")
            elif score < 0.5:
                reasons.append(f"⚠️  {name} 较低 ({score:.0%})")

        if decision == 'AUTO_APPROVE':
            reasons.insert(0, "🎉 综合评分优秀，建议自动批准")
        elif decision == 'MANUAL_REVIEW':
            reasons.insert(0, "🤔 综合评分良好，建议人工审核")
        elif decision == 'AUTO_REJECT':
            reasons.insert(0, "❌ 综合评分过低，建议拒绝")

        return '; '.join(reasons)

    def batch_review(self, features: List[Dict]) -> Dict:
        """批量审核"""
        results = {
            'auto_approve': [],
            'manual_review': [],
            'auto_reject': [],
            'low_confidence': []
        }

        for feature in features:
            analysis = self.analyze_feature(feature)
            decision = analysis['decision']

            if decision == 'AUTO_APPROVE':
                results['auto_approve'].append(analysis)
            elif decision == 'MANUAL_REVIEW':
                results['manual_review'].append(analysis)
            elif decision == 'AUTO_REJECT':
                results['auto_reject'].append(analysis)
            else:
                results['low_confidence'].append(analysis)

        return results

    def generate_review_summary(self, results: Dict) -> str:
        """生成审核摘要"""
        lines = []
        lines.append("\n" + "="*60)
        lines.append("  📊 智能审核摘要")
        lines.append("="*60 + "\n")

        total = sum(len(v) for v in results.values())
        lines.append(f"总计特征: {total} 个\n")

        lines.append(f"🎉 自动批准: {len(results['auto_approve'])} 个")
        lines.append(f"🤔 人工审核: {len(results['manual_review'])} 个")
        lines.append(f"⚠️  低置信度: {len(results['low_confidence'])} 个")
        lines.append(f"❌ 自动拒绝: {len(results['auto_reject'])} 个\n")

        # 显示自动批准的特征
        if results['auto_approve']:
            lines.append("="*60)
            lines.append("🎉 自动批准列表:")
            lines.append("="*60)
            for analysis in results['auto_approve']:
                feature = analysis['feature']
                score = analysis['total_score']
                lines.append(f"\n✅ [{feature['category']}] {feature.get('raw_text', '')}")
                lines.append(f"   置信度: {score:.0%}")
                lines.append(f"   理由: {analysis['reason']}")

        # 显示需要人工审核的特征
        if results['manual_review']:
            lines.append("\n" + "="*60)
            lines.append("🤔 需要人工审核:")
            lines.append("="*60)
            for analysis in results['manual_review']:
                feature = analysis['feature']
                score = analysis['total_score']
                lines.append(f"\n🟡 [{feature['category']}] {feature.get('raw_text', '')}")
                lines.append(f"   置信度: {score:.0%}")
                lines.append(f"   理由: {analysis['reason']}")

        return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    reviewer = SmartReviewer()

    # 测试特征
    test_features = [
        {
            'category': 'hair_styles',
            'raw_text': 'long flowing red hair',
            'confidence': 0.9,
            'method': 'rule-based'
        },
        {
            'category': 'clothing',
            'raw_text': 'elegant red silk qipao',
            'confidence': 0.8,
            'method': 'rule-based'
        },
        {
            'category': 'accessories',
            'raw_text': 'earrings',
            'confidence': 0.6,
            'method': 'rule-based'
        }
    ]

    print("🧪 智能审核器测试\n")

    for feature in test_features:
        result = reviewer.analyze_feature(feature)
        print(f"\n特征: {feature['raw_text']}")
        print(f"类别: {feature['category']}")
        print(f"决策: {result['decision']}")
        print(f"总分: {result['total_score']:.0%}")
        print(f"理由: {result['reason']}")
