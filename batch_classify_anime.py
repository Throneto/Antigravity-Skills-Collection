#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI批量分类器 - 动漫提示词专用
基于Domain Classifier Skill的规范
"""

import json
import re
from pathlib import Path

class AIDomainnClassifier:
    """AI领域分类器（基于规则引擎）"""

    def __init__(self):
        # 增强关键词库 - 针对动漫添加专门关键词
        self.domain_keywords = {
            'portrait': {
                # 人物特征
                '人': 5, '女': 4, '男': 4, '脸': 5, '面部': 5, '肖像': 5,
                '眼睛': 4, '鼻子': 3, '嘴': 3, '皮肤': 4, '肤色': 4,
                '妆': 4, '化妆': 4, 'makeup': 4,
                '发型': 3, '头发': 3, 'hair': 3,
                '表情': 4, '微笑': 3, '笑容': 3,
                '姿势': 3, 'pose': 3, '站姿': 3,
                # 服装
                '服装': 2, '衣服': 2, '穿着': 2, '连衣裙': 2,
                # 摄影术语
                '肖像摄影': 5, 'portrait': 5, '人像': 5,
                '美女': 4, '帅哥': 3, '模特': 4,
                '自拍': 3, 'selfie': 3,
                # 动漫人物
                '角色': 5, 'character': 4, 'coser': 5, 'cosplay': 5,
                '动漫': 4, 'anime': 5, '二次元': 5, '手办': 4,
                'Q版': 4, 'chibi': 5, '可爱': 3
            },
            'interior': {
                '室内': 5, '房间': 5, '客厅': 5, '卧室': 5, '厨房': 5,
                '家具': 5, '沙发': 4, '椅子': 3, '桌子': 3, '床': 4,
                '装修': 5, '设计': 3, '空间': 4,
                '墙': 3, '地板': 3, '天花板': 3, '窗': 3,
                '灯': 3, '灯光': 3, '照明': 3,
                'interior': 5, 'room': 4, 'living room': 5,
                '简约': 2, '现代': 2, '北欧': 3, '中古': 3
            },
            'product': {
                '产品': 5, '商品': 4, '物品': 3,
                '瓶': 4, '瓶子': 4, 'bottle': 4,
                '包': 3, '包包': 4, 'bag': 3,
                '手表': 4, 'watch': 4,
                '鞋': 3, '鞋子': 4, 'shoe': 3,
                '包装': 4, 'packaging': 4,
                '产品摄影': 5, 'product photography': 5,
                '商业摄影': 4, '静物': 4,
                '展示': 3, '陈列': 3,
                # 周边商品
                '手办': 4, '模型': 4, '玩具': 4,
                '盲盒': 5, '钥匙扣': 3, '徽章': 3
            },
            'design': {
                '海报': 5, 'poster': 5,
                '设计': 4, 'design': 3,
                '布局': 5, 'layout': 5,
                '网格': 5, 'grid': 5,
                'bento': 5, '模块': 4,
                'UI': 5, '界面': 5, 'interface': 5,
                '排版': 5, 'typography': 5,
                '图形': 4, 'graphic': 4,
                '卡片': 3, 'card': 3,
                '信息图': 5, 'infographic': 5,
                '名片': 4, '宣传册': 4,
                '平面': 4, '视觉': 3,
                # 动漫设计
                '贴纸': 4, 'sticker': 5, '表情包': 5,
                '图标': 3, 'icon': 3
            },
            'art': {
                '绘画': 5, 'painting': 5, '画': 4,
                '水墨': 5, '墨': 4, 'ink': 4,
                '油画': 5, '水彩': 5, 'watercolor': 5,
                '素描': 5, 'sketch': 5, 'drawing': 5,
                '插画': 5, 'illustration': 5,
                '艺术': 5, 'art': 3,
                '笔触': 4, '画笔': 4, 'brush': 3,
                '画作': 5, '作品': 2,
                '国画': 5, '工笔': 5,
                '卡通': 3, 'cartoon': 3,
                '3D渲染': 3, '3D': 2,
                # 动漫艺术
                '漫画': 5, 'manga': 5, 'comic': 5,
                '动画': 5, 'animation': 5,
                '风格': 3, 'style': 2,
                '线稿': 4, '上色': 4
            },
            'video': {
                '视频': 5, 'video': 5,
                '镜头': 4, '运镜': 5, 'camera movement': 5,
                '分镜': 5, 'storyboard': 5,
                '场景': 3, 'scene': 2,
                '电影': 4, 'cinematic': 4, 'film': 3,
                '动画': 5, 'animation': 5,
                '动态': 3, 'motion': 3,
                '特效': 3, 'VFX': 4,
                '剪辑': 4, '转场': 5,
                '运动': 2, '移动': 2
            },
            'common': {
                '摄影': 4, 'photography': 3, 'photo': 2,
                '相机': 4, 'camera': 3,
                '镜头': 3, 'lens': 3,
                '光': 3, '光照': 4, 'lighting': 4,
                '景深': 5, 'depth of field': 5, 'DOF': 5,
                '对焦': 5, 'focus': 3,
                '曝光': 4, 'exposure': 4,
                '构图': 4, 'composition': 3,
                '角度': 3, 'angle': 2,
                'ISO': 4, '快门': 4, '光圈': 5
            }
        }

    def classify(self, content: str, theme: str = "") -> dict:
        """智能分类"""
        text = (content + " " + theme).lower()

        # 计算各领域得分
        scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = 0
            found_keywords = []

            for keyword, weight in keywords.items():
                if keyword.lower() in text:
                    score += weight
                    found_keywords.append(keyword)

            scores[domain] = {
                'score': score,
                'keywords': found_keywords
            }

        # 排序
        sorted_domains = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)

        primary = sorted_domains[0][0] if sorted_domains[0][1]['score'] > 0 else None
        primary_score = sorted_domains[0][1]['score']
        keywords_found = sorted_domains[0][1]['keywords']

        # 计算置信度
        if primary_score == 0:
            confidence = 0
        elif primary_score >= 15:
            confidence = 90
        elif primary_score >= 10:
            confidence = 75
        elif primary_score >= 7:
            confidence = 60
        elif primary_score >= 5:
            confidence = 50
        else:
            confidence = 30

        # 次要领域
        secondary = []
        for domain, data in sorted_domains[1:4]:
            if data['score'] >= 5 and domain != primary:
                secondary.append(domain)

        # 生成推理
        reasoning = self._generate_reasoning(primary, keywords_found, content, theme)

        return {
            'primary_domain': primary,
            'confidence': confidence,
            'reasoning': reasoning,
            'secondary_domains': secondary,
            'keywords_found': keywords_found[:8],
            'scores': {k: v['score'] for k, v in sorted_domains[:5]}
        }

    def _generate_reasoning(self, domain, keywords, content, theme):
        """生成推理说明"""
        if not domain:
            return "无法识别领域，关键词不足"

        domain_names = {
            'portrait': '人像摄影',
            'interior': '室内设计',
            'product': '产品摄影',
            'design': '平面设计',
            'art': '艺术风格',
            'video': '视频生成',
            'common': '通用摄影'
        }

        kw_str = '、'.join(keywords[:5]) if keywords else '相关术语'
        return f"包含{domain_names[domain]}关键元素：{kw_str}。"


def batch_classify():
    """批量分类动漫提示词"""
    # 加载未分类文件
    with open('anime_unclassified.json', 'r', encoding='utf-8') as f:
        unclassified = json.load(f)

    classifier = AIDomainnClassifier()
    results = []

    print(f"开始AI分类 {len(unclassified)} 个动漫文件...\n")

    for idx, item in enumerate(unclassified, 1):
        file_id = item['file_id']
        theme = item.get('theme', '')
        content = item.get('content_preview', '')

        # 分类
        classification = classifier.classify(content, theme)

        result = {
            'file_id': file_id,
            **classification
        }

        results.append(result)

        if idx % 50 == 0:
            print(f"  进度: {idx}/{len(unclassified)}")

    # 保存结果
    with open('anime_classification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 统计
    print(f"\n{'='*80}")
    print(f"动漫提示词AI分类完成！")
    print(f"{'='*80}\n")

    domain_stats = {}
    high_conf_stats = {}

    for r in results:
        domain = r['primary_domain']
        conf = r['confidence']

        if domain:
            domain_stats[domain] = domain_stats.get(domain, 0) + 1

            if conf >= 70:
                high_conf_stats[domain] = high_conf_stats.get(domain, 0) + 1

    print("领域分布:")
    for domain, count in sorted(domain_stats.items(), key=lambda x: x[1], reverse=True):
        high_conf = high_conf_stats.get(domain, 0)
        print(f"  {domain}: {count} 个 (高置信度: {high_conf})")

    no_domain = len([r for r in results if not r['primary_domain']])
    print(f"\n未识别: {no_domain} 个")

    print(f"\n结果已保存到: anime_classification_results.json")


if __name__ == "__main__":
    batch_classify()
