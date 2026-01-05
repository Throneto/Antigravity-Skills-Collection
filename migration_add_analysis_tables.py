#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加分析功能所需的表

新增3个表：
1. generated_prompts - 生成的Prompt历史记录
2. prompt_elements - Prompt与元素的关联表
3. element_usage_stats - 元素使用统计表
"""

import sqlite3
import os

DB_PATH = 'extracted_results/elements.db'


def migrate():
    """执行数据库迁移"""

    if not os.path.exists(DB_PATH):
        print(f"❌ 错误：数据库文件不存在: {DB_PATH}")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🚀 开始数据库迁移...")

    # 表1：生成的Prompt历史记录
    print("\n📋 创建表: generated_prompts")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_prompts (
            prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_text TEXT NOT NULL,
            user_intent TEXT,
            generation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quality_score REAL,
            style_tag TEXT,
            metadata TEXT
        )
    ''')
    print("✅ generated_prompts 创建成功")

    # 表2：Prompt-元素关联表
    print("\n📋 创建表: prompt_elements")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompt_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            element_id TEXT NOT NULL,
            category TEXT,
            field_name TEXT,
            FOREIGN KEY (prompt_id) REFERENCES generated_prompts(prompt_id),
            FOREIGN KEY (element_id) REFERENCES elements(element_id)
        )
    ''')
    print("✅ prompt_elements 创建成功")

    # 表3：元素使用统计表
    print("\n📋 创建表: element_usage_stats")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS element_usage_stats (
            element_id TEXT PRIMARY KEY,
            usage_count INTEGER DEFAULT 0,
            avg_quality REAL DEFAULT 0.0,
            last_used TIMESTAMP,
            FOREIGN KEY (element_id) REFERENCES elements(element_id)
        )
    ''')
    print("✅ element_usage_stats 创建成功")

    # 创建索引以提高查询性能
    print("\n📊 创建索引...")
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_prompt_elements_prompt_id
        ON prompt_elements(prompt_id)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_prompt_elements_element_id
        ON prompt_elements(element_id)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_generated_prompts_style_tag
        ON generated_prompts(style_tag)
    ''')
    print("✅ 索引创建成功")

    # 提交更改
    conn.commit()

    # 验证表是否创建成功
    print("\n🔍 验证表结构...")
    cursor.execute('''
        SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    ''')
    tables = cursor.fetchall()
    print(f"\n当前数据库包含 {len(tables)} 个表:")
    for table in tables:
        print(f"  - {table[0]}")

    # 检查elements表的记录数
    cursor.execute('SELECT COUNT(*) FROM elements')
    element_count = cursor.fetchone()[0]
    print(f"\n📊 elements表: {element_count} 个元素")

    conn.close()

    print("\n✅ 数据库迁移完成！")
    return True


if __name__ == '__main__':
    migrate()
