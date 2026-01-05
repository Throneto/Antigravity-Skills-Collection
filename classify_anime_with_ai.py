#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI分类结果应用器 - 动漫提示词专用
读取分类结果JSON，应用到学习器
"""

import json
from pathlib import Path
from universal_learner_v2 import UniversalLearnerV2
from txt_to_json_converter import TxtToJsonConverter

def apply_classifications():
    """应用AI分类结果重新学习动漫提示词"""

    # 读取分类结果
    with open('anime_classification_results.json', 'r', encoding='utf-8') as f:
        classifications = json.load(f)

    print(f"加载了 {len(classifications)} 个分类结果")

    # 初始化学习器
    learner = UniversalLearnerV2()
    converter = TxtToJsonConverter()

    # 两个动漫目录
    anime_dirs = [
        "/Users/huangzongning/Documents/anime_prompts",
        "/Users/huangzongning/Documents/picotrex_anime_prompts"
    ]

    stats = {
        'processed': 0,
        'added': 0,
        'skipped': 0,
        'by_domain': {}
    }

    for idx, item in enumerate(classifications, 1):
        file_id = item['file_id']
        primary_domain = item['primary_domain']
        confidence = item['confidence']

        # 跳过低置信度和未识别
        if not primary_domain or confidence < 50:
            stats['skipped'] += 1
            continue

        # 在两个目录中查找文件
        file_path = None
        for dir_path in anime_dirs:
            candidate = Path(dir_path) / file_id
            if candidate.exists():
                file_path = candidate
                break

        if not file_path:
            stats['skipped'] += 1
            continue

        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                txt_content = f.read()

            # 转换为prompt_data
            prompt_data = converter.convert_txt_to_prompt_data(txt_content, file_id)

            # 强制设置领域（覆盖自动分类）
            domain_info = {
                'primary': primary_domain,
                'secondary': item.get('secondary_domains', []),
                'confidence': confidence / 100,
                'scores': {}
            }

            # 学习
            elements = learner.extractor.extract(prompt_data, domain_info)

            if not elements:
                stats['skipped'] += 1
                continue

            # 添加到数据库
            added_count = 0
            for element in elements:
                tags = learner.tagger.generate_tags(element, primary_domain)

                if 'chinese_name' not in element:
                    element['chinese_name'] = element['name'].replace('_', ' ').title()

                success, element_id = learner._add_to_db(
                    element,
                    primary_domain,
                    tags,
                    prompt_data['prompt_id']
                )

                if success:
                    added_count += 1

            stats['processed'] += 1
            stats['added'] += added_count

            if primary_domain not in stats['by_domain']:
                stats['by_domain'][primary_domain] = 0
            stats['by_domain'][primary_domain] += added_count

            if idx % 50 == 0:
                print(f"  处理进度: {idx}/{len(classifications)}, 新增: {stats['added']}个元素")

        except Exception as e:
            print(f"  错误 {file_id}: {e}")
            stats['skipped'] += 1
            continue

    # 导出
    learner.db.export_to_json('extracted_results/universal_elements_library.json')
    learner.close()

    # 报告
    print(f"\n{'='*80}")
    print(f"动漫提示词AI分类重新学习完成")
    print(f"{'='*80}")
    print(f"处理文件: {stats['processed']}")
    print(f"新增元素: {stats['added']}")
    print(f"跳过文件: {stats['skipped']}")
    print(f"\n各领域分布:")
    for domain, count in sorted(stats['by_domain'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: +{count} 元素")

    return stats

if __name__ == "__main__":
    apply_classifications()
