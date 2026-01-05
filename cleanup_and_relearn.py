#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理手动添加的元素，重新用V2自动学习
"""

import sqlite3
import json
from element_db import ElementDB
from universal_learner_v2 import UniversalLearnerV2

def main():
    db = ElementDB('extracted_results/elements.db')

    # Step 1: 删除所有手动添加的元素
    print("🗑️  删除手动添加的元素...")
    cursor = db.conn.cursor()

    cursor.execute("""
        SELECT element_id, name FROM elements
        WHERE learned_from = 'manual_supplement'
    """)
    manual_elements = cursor.fetchall()

    print(f"   发现 {len(manual_elements)} 个手动元素：")
    for elem_id, name in manual_elements:
        print(f"   - {elem_id}: {name}")

    # 删除这些元素（先删除关联的tags，再删除元素本身）
    # 先收集element_ids
    manual_ids = [elem[0] for elem in manual_elements]

    # 删除element_tags
    for elem_id in manual_ids:
        cursor.execute("DELETE FROM element_tags WHERE element_id = ?", (elem_id,))

    # 删除elements
    cursor.execute("DELETE FROM elements WHERE learned_from = 'manual_supplement'")

    db.conn.commit()

    print(f"✅ 已删除 {len(manual_elements)} 个手动元素")

    # 获取清理后的统计
    stats = db.get_stats()
    print(f"\n📊 清理后数据库状态：")
    print(f"   总元素数: {stats['total_elements']}")

    db.close()

    # Step 2: 使用V2重新学习Prompt #19
    print(f"\n{'='*80}")
    print("🔄 使用V2重新学习Prompt #19...")
    print(f"{'='*80}\n")

    learner = UniversalLearnerV2()

    with open('temp_new_prompt.json', 'r', encoding='utf-8') as f:
        prompt_data = json.load(f)

    result = learner.learn_from_prompt(prompt_data)

    print(f"\n✅ V2自动学习完成！")
    print(f"   添加: {result['added']} 个元素")
    print(f"   跳过: {result['skipped']} 个元素")

    # 最终统计
    final_stats = learner.db.get_stats()
    print(f"\n📊 最终数据库状态：")
    print(f"   总元素数: {final_stats['total_elements']}")

    # 导出JSON
    learner.db.export_to_json('extracted_results/universal_elements_library.json')

    learner.close()

    print(f"\n🎉 清理和重新学习完成！")

if __name__ == "__main__":
    main()
