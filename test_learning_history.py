#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试学习历史记录功能
验证source_prompts表是否正确保存学习记录
"""

import json
import sqlite3
from universal_learner_v2 import UniversalLearnerV2

print("="*80)
print("测试学习历史记录功能")
print("="*80)

# 准备测试数据
test_prompt = {
    'prompt_id': 9999,
    'theme': '测试：西部世界机器人',
    'original_prompt': '''
    A photorealistic portrait of a young woman with dramatic three-point lighting,
    volumetric atmospheric haze, half-human half-android revelation,
    sophisticated mechanical layer beneath skin, cinematic mood
    ''',
    'modules': {
        'lighting': {
            'type': 'three-point dramatic',
            'atmosphere': 'volumetric haze',
            'mood': 'cinematic'
        },
        'special_effects': {
            'type': 'half-human half-android',
            'detail': 'vertical division revealing mechanical layer'
        },
        'technical': {
            'quality': '8K ultra-detailed',
            'camera': 'professional studio setup'
        }
    }
}

# 初始化学习器
learner = UniversalLearnerV2()

# 1. 查询学习前的状态
conn = sqlite3.connect('extracted_results/elements.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM source_prompts")
before_count = cursor.fetchone()[0]
print(f"\n📊 学习前统计:")
print(f"  source_prompts 表记录数: {before_count}")

cursor.execute("SELECT COUNT(*) FROM elements")
before_elements = cursor.fetchone()[0]
print(f"  elements 表记录数: {before_elements}")

# 2. 执行学习
print(f"\n🎓 开始学习测试Prompt...")
result = learner.learn_from_prompt(test_prompt)

print(f"\n学习结果:")
print(f"  新增元素: {result['added']}")
print(f"  跳过元素: {result['skipped']}")

# 3. 查询学习后的状态
cursor.execute("SELECT COUNT(*) FROM source_prompts")
after_count = cursor.fetchone()[0]
print(f"\n📊 学习后统计:")
print(f"  source_prompts 表记录数: {after_count} (+{after_count - before_count})")

cursor.execute("SELECT COUNT(*) FROM elements")
after_elements = cursor.fetchone()[0]
print(f"  elements 表记录数: {after_elements} (+{after_elements - before_elements})")

# 4. 查看刚刚保存的学习记录
print(f"\n🔍 查看Prompt #9999的学习记录:")
cursor.execute("""
    SELECT prompt_id, theme, prompt_length, quality_score, complexity,
           extracted_elements_count, learning_status, learned_at
    FROM source_prompts
    WHERE prompt_id = 9999
""")

record = cursor.fetchone()
if record:
    print(f"  ✅ 找到学习记录:")
    print(f"    Prompt ID: {record[0]}")
    print(f"    主题: {record[1]}")
    print(f"    长度: {record[2]} 字符")
    print(f"    质量评分: {record[3]}/10")
    print(f"    复杂度: {record[4]}")
    print(f"    提取元素数: {record[5]}")
    print(f"    学习状态: {record[6]}")
    print(f"    学习时间: {record[7]}")
else:
    print(f"  ❌ 未找到学习记录！")

# 5. 查看所有学习记录统计
print(f"\n📈 全部学习记录统计:")
cursor.execute("""
    SELECT
        COUNT(*) as total,
        SUM(extracted_elements_count) as total_elements,
        AVG(quality_score) as avg_quality,
        COUNT(CASE WHEN complexity = 'complex' THEN 1 END) as complex_count,
        COUNT(CASE WHEN complexity = 'medium' THEN 1 END) as medium_count,
        COUNT(CASE WHEN complexity = 'simple' THEN 1 END) as simple_count
    FROM source_prompts
""")

stats = cursor.fetchone()
if stats[0] > 0:
    print(f"  总学习记录: {stats[0]}")
    print(f"  总提取元素: {stats[1]}")
    print(f"  平均质量: {stats[2]:.1f}/10")
    print(f"  复杂度分布:")
    print(f"    - complex: {stats[3]}")
    print(f"    - medium: {stats[4]}")
    print(f"    - simple: {stats[5]}")
else:
    print(f"  ⚠️  没有学习记录")

# 6. 查看最近5条学习记录
print(f"\n📋 最近5条学习记录:")
cursor.execute("""
    SELECT prompt_id, theme, quality_score, complexity, extracted_elements_count, learned_at
    FROM source_prompts
    ORDER BY learned_at DESC
    LIMIT 5
""")

records = cursor.fetchall()
if records:
    for i, rec in enumerate(records, 1):
        print(f"  [{i}] Prompt #{rec[0]}: {rec[1]}")
        print(f"      质量: {rec[2]}/10, 复杂度: {rec[3]}, 元素: {rec[4]}, 时间: {rec[5]}")
else:
    print(f"  无记录")

conn.close()
learner.close()

print("\n" + "="*80)
print("✅ 测试完成！")
print("="*80)

# 总结
if after_count > before_count:
    print("\n🎉 学习历史记录功能正常工作！")
    print(f"   - source_prompts表成功保存了学习记录")
    print(f"   - 可以追溯学习来源了")
else:
    print("\n❌ 学习历史记录功能未生效")
    print(f"   - source_prompts表没有新记录")
