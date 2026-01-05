#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析728个提示词文件的领域分布
"""

from pathlib import Path
from batch_learner_v2 import BatchLearner
from universal_learner_v2 import UniversalLearnerV2
import json

# 统计各领域文件数
domain_stats = {
    'portrait': [],
    'common': [],
    'interior': [],
    'product': [],
    'design': [],
    'art': [],
    'video': [],
    'None': []  # 无法识别的
}

batch_learner = BatchLearner()
directory = "/Users/huangzongning/Documents/prompts"
dir_path = Path(directory)
all_files = list(dir_path.glob("*.txt"))

print(f"分析 {len(all_files)} 个文件的领域分布...\n")

for idx, file_path in enumerate(all_files, 1):
    if idx % 100 == 0:
        print(f"  处理中... {idx}/{len(all_files)}")

    try:
        # 加载文件
        prompt_data = batch_learner.load_prompt_file(file_path)

        # 领域分类
        domain_info = batch_learner.learner.classifier.classify(
            prompt_data.get('original_prompt', ''),
            prompt_data.get('theme', '')
        )

        primary = domain_info.get('primary') or 'None'
        domain_stats[primary].append({
            'file': file_path.name,
            'confidence': domain_info.get('confidence', 0)
        })
    except Exception as e:
        domain_stats['None'].append({
            'file': file_path.name,
            'error': str(e)
        })

batch_learner.close()

# 输出统计
print("\n" + "="*80)
print("📊 728个提示词文件在7大领域的分布")
print("="*80)
print()

domain_names = {
    'portrait': '人像摄影',
    'common': '通用摄影',
    'interior': '室内设计',
    'product': '产品摄影',
    'design': '平面设计',
    'art': '艺术风格',
    'video': '视频生成',
    'None': '未识别'
}

sorted_domains = sorted(domain_stats.items(), key=lambda x: len(x[1]), reverse=True)

for domain_id, files in sorted_domains:
    count = len(files)
    percentage = count / len(all_files) * 100
    bar = '█' * (count // 10)
    print(f'{domain_names[domain_id]:8} ({domain_id:8}): {count:3} 个 ({percentage:5.1f}%) {bar}')

print()
print("="*80)
print(f"总计: {len(all_files)} 个文件")
print()

# 详细统计
print("高置信度分布（confidence > 70%）：")
for domain_id, files in sorted_domains:
    if domain_id != 'None':
        high_conf = [f for f in files if f.get('confidence', 0) > 0.7]
        if high_conf:
            print(f"  {domain_names[domain_id]}: {len(high_conf)} 个")
