#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准备未识别文件供AI分类
"""

from pathlib import Path
from batch_learner_v2 import BatchLearner
import json

batch_learner = BatchLearner()
directory = "/Users/huangzongning/Documents/prompts"
dir_path = Path(directory)
all_files = list(dir_path.glob("*.txt"))

unclassified = []

print(f"扫描 {len(all_files)} 个文件...\n")

for idx, file_path in enumerate(all_files, 1):
    try:
        # 加载文件
        prompt_data = batch_learner.load_prompt_file(file_path)

        # 领域分类
        domain_info = batch_learner.learner.classifier.classify(
            prompt_data.get('original_prompt', ''),
            prompt_data.get('theme', '')
        )

        primary = domain_info.get('primary')

        # 只收集未识别的（None）或低置信度的（<50%）
        if not primary or domain_info.get('confidence', 0) < 0.5:
            # 提取前500字符作为摘要
            content = prompt_data.get('original_prompt', '')[:500]

            unclassified.append({
                'file_id': file_path.name,
                'theme': prompt_data.get('theme', ''),
                'content_preview': content,
                'length': len(prompt_data.get('original_prompt', ''))
            })
    except Exception as e:
        pass

batch_learner.close()

# 保存结果
output_file = 'unclassified_prompts.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(unclassified, f, ensure_ascii=False, indent=2)

print(f"\n找到 {len(unclassified)} 个未识别文件")
print(f"已保存到: {output_file}")
print(f"\n文件大小分布：")
print(f"  < 500字: {len([x for x in unclassified if x['length'] < 500])}")
print(f"  500-1000字: {len([x for x in unclassified if 500 <= x['length'] < 1000])}")
print(f"  1000-2000字: {len([x for x in unclassified if 1000 <= x['length'] < 2000])}")
print(f"  > 2000字: {len([x for x in unclassified if x['length'] >= 2000])}")
