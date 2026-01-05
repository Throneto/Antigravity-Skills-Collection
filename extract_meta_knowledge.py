#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元知识提取器 - 从反面教材分析中提取最佳实践和反面模式
Meta-Knowledge Extractor - Extract best practices and anti-patterns from analysis
"""

import json
import sqlite3
from datetime import datetime
from element_db import ElementDB


def extract_meta_knowledge_from_anti_pattern():
    """
    从pencil_sketch_idol反面教材分析中提取元知识

    提取内容：
    - 5条铁律（Best Practices）
    - 4种反面模式检测法（Anti-Pattern Detection Methods）
    """

    # 初始化数据库
    db = ElementDB("extracted_results/elements.db")

    # 1. 确保有 "prompt_writing" 领域
    cursor = db.conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO domains (domain_id, name, description, total_elements)
    VALUES (?, ?, ?, ?)
    """, (
        "prompt_writing",
        "提示词写作",
        "Prompt写作技巧、最佳实践、反面模式检测",
        0
    ))

    # 2. 创建类别
    categories = [
        ("best_practices", "最佳实践", "Prompt写作的黄金法则和优秀模式"),
        ("anti_patterns", "反面模式", "需要避免的常见错误和陷阱"),
        ("detection_methods", "检测方法", "识别问题的技术和清单"),
        ("optimization_techniques", "优化技巧", "改进提示词的具体方法")
    ]

    for cat_id, name, desc in categories:
        full_cat_id = f"prompt_writing_{cat_id}"
        cursor.execute("""
        INSERT OR IGNORE INTO categories (category_id, domain_id, name, description, total_elements)
        VALUES (?, ?, ?, ?, ?)
        """, (full_cat_id, "prompt_writing", name, desc, 0))

    db.conn.commit()

    # 3. 提取5条铁律作为元素
    iron_rules = [
        {
            "element_id": "prompt_writing_best_practices_001",
            "name": "max_3_quality_words",
            "chinese_name": "质量词最多3个",
            "ai_prompt_template": "使用不超过3个质量修饰词，如: highly detailed, sharp focus, 8K",
            "keywords": ["quality_words", "efficiency", "redundancy_reduction", "best_practice"],
            "reusability_score": 10.0,
            "metadata": json.dumps({
                "rule": "每个提示词，质量修饰词不超过3个",
                "reason": "AI在第3个词后就停止增加权重",
                "example_good": "highly detailed + sharp focus + 8K",
                "example_bad": "perfect composition, impeccable attention to detail, highest quality, rich detail, sharp focus, clear edges, exquisite details...",
                "source_analysis": "pencil_sketch_idol_001",
                "learned_from": "anti_pattern"
            })
        },
        {
            "element_id": "prompt_writing_best_practices_002",
            "name": "70_percent_core_description",
            "chinese_name": "核心描述占70%",
            "ai_prompt_template": "70%篇幅描述主体、场景、动作（是什么+在哪+做什么），20%技术参数，10%质量词",
            "keywords": ["structure", "priority", "7-2-1_principle", "composition"],
            "reusability_score": 10.0,
            "metadata": json.dumps({
                "rule": "70%篇幅描述主体、场景、动作",
                "reason": "这些是画面的实际内容",
                "structure": "70%核心: 谁/什么+在哪+做什么 + 20%技术: 怎么拍+什么光 + 10%质量: 多清晰",
                "example": "Witch in hooded cloak gathering glowing herbs in misty forest (70%), cinematic composition, soft lighting (20%), highly detailed 8K (10%)",
                "source_analysis": "pencil_sketch_idol_001"
            })
        },
        {
            "element_id": "prompt_writing_best_practices_003",
            "name": "avoid_contradictions",
            "chinese_name": "避免矛盾指令",
            "ai_prompt_template": "每个维度只给一个明确指令，避免互斥要求（如Gothic vs Arial font, grayscale vs vibrant colors）",
            "keywords": ["contradiction", "clarity", "logic_check", "consistency"],
            "reusability_score": 9.0,
            "metadata": json.dumps({
                "rule": "每个维度只给一个明确指令",
                "check_method": "用'and'连接的词是否互斥",
                "common_contradictions": [
                    "色彩: grayscale vs vibrant colors",
                    "字体: Gothic vs Arial",
                    "分辨率: 8K vs 4K",
                    "光线: soft vs harsh"
                ],
                "impact": "矛盾指令导致AI随机选择，结果不可控",
                "source_analysis": "pencil_sketch_idol_001"
            })
        },
        {
            "element_id": "prompt_writing_best_practices_004",
            "name": "realistic_expectations",
            "chinese_name": "不提不切实际要求",
            "ai_prompt_template": "不要求AI无法控制的精度（避免exactly, perfectly, absolutely, 100%, zero等词）",
            "keywords": ["realistic", "ai_limitations", "precision", "feasibility"],
            "reusability_score": 9.0,
            "metadata": json.dumps({
                "rule": "不要求AI无法控制的精度",
                "forbidden_words": ["exactly", "perfectly", "absolutely", "100%", "zero", "no X whatsoever"],
                "replacements": {
                    "exactly 10x10 pixels": "small watermark",
                    "perfectly centered": "centered",
                    "no blur whatsoever": "sharp and clean"
                },
                "reason": "AI无法保证像素级精度、绝对值、数学精度",
                "source_analysis": "pencil_sketch_idol_001"
            })
        },
        {
            "element_id": "prompt_writing_best_practices_005",
            "name": "no_repetition_for_emphasis",
            "chinese_name": "重复强调=优先级降低",
            "ai_prompt_template": "重要的事说1次，用强调词；不要用重复次数表示重要性",
            "keywords": ["emphasis", "repetition", "weight_distribution", "efficiency"],
            "reusability_score": 8.0,
            "metadata": json.dumps({
                "rule": "说1次就够，说3次反而分散权重",
                "phenomenon": "mandatory × 3 = 权重分散到3处",
                "recommendation": "重要的事说1次，用强调词",
                "example_bad": "The watermark is mandatory and must not be omitted, modified, adjusted... (mandatory出现3次)",
                "example_good": "watermark in lower left corner with 'name' text in bold font (说1次，清晰明确)",
                "source_analysis": "pencil_sketch_idol_001"
            })
        }
    ]

    # 4. 提取4种反面模式检测法
    detection_methods = [
        {
            "element_id": "prompt_writing_detection_methods_001",
            "name": "redundancy_detection_3_1_0",
            "chinese_name": "冗余检测3-1-0原则",
            "ai_prompt_template": "每个概念最多3个词，同义词最多1次重复，完全相同的词0次重复",
            "keywords": ["redundancy", "detection", "efficiency", "self_check"],
            "reusability_score": 10.0,
            "metadata": json.dumps({
                "method": "3-1-0原则",
                "red_flags": [
                    "质量词超过5个",
                    "同义词重复（detail出现5次）",
                    "同一词出现2次以上"
                ],
                "formula": "质量词>5个 OR 同义词>2次 OR 同词重复 = 冗余警报",
                "example_bad": "perfect composition, impeccable detail, highest quality, rich detail, sharp focus, clear edges (9个词表达3个概念)",
                "example_good": "highly detailed, sharp focus, professional quality (3个词表达3个概念)",
                "efficiency_gain": "削减78%，无信息损失",
                "source_analysis": "pencil_sketch_idol_001"
            })
        },
        {
            "element_id": "prompt_writing_detection_methods_002",
            "name": "contradiction_detection_and_rule",
            "chinese_name": "矛盾检测AND规则",
            "ai_prompt_template": "用'AND'连接测试：要求A AND 要求B → 检查是否可同时满足 → 如果不能 = 矛盾",
            "keywords": ["contradiction", "logic_check", "clarity", "validation"],
            "reusability_score": 9.0,
            "metadata": json.dumps({
                "method": "AND规则检查法",
                "check_process": "检查所有用'and'或','连接的要求，判断是否互斥或冲突",
                "common_contradiction_types": [
                    "风格矛盾: graphite sketch (黑白) AND vibrant colors (彩色)",
                    "技术矛盾: Gothic font AND Arial font",
                    "分辨率矛盾: 8K/4K (同时要求两个)",
                    "质感矛盾: perfect vs imperfections",
                    "光线矛盾: soft vs harsh"
                ],
                "fix_strategies": ["选择一个", "融合描述", "明确优先级"],
                "source_analysis": "pencil_sketch_idol_001"
            })
        },
        {
            "element_id": "prompt_writing_detection_methods_003",
            "name": "structure_balance_check_7_2_1",
            "chinese_name": "结构平衡检查7-2-1法则",
            "ai_prompt_template": "检查提示词结构比例：核心描述应占70%，技术参数20%，质量词10%",
            "keywords": ["structure", "balance", "priority", "composition"],
            "reusability_score": 10.0,
            "metadata": json.dumps({
                "method": "7-2-1结构检查",
                "ideal_structure": {
                    "core_description": "70% (主体+场景+动作)",
                    "technical_params": "20% (光线+角度+景深)",
                    "quality_words": "10% (分辨率+清晰度)"
                },
                "bad_structure": "质量词20% + 核心描述30% + 无效指令50% = 主次颠倒",
                "good_structure": "核心描述70% + 技术参数20% + 质量词10% = 重点清晰",
                "detection_checklist": [
                    "核心描述是否占70%？",
                    "技术参数是否占20%？",
                    "质量词是否占10%？",
                    "重点是否清晰？"
                ],
                "source_analysis": "pencil_sketch_idol_001"
            })
        },
        {
            "element_id": "prompt_writing_detection_methods_004",
            "name": "unrealistic_expectations_detector",
            "chinese_name": "不切实际要求检测器",
            "ai_prompt_template": "识别红旗词（perfectly/exactly/absolutely/100%/zero） → 判断AI能力边界 → 改为倾向描述",
            "keywords": ["realistic", "ai_limitations", "validation", "expectations"],
            "reusability_score": 9.0,
            "metadata": json.dumps({
                "method": "不切实际要求识别",
                "red_flag_words": ["perfectly", "exactly", "absolutely", "100%", "zero", "no X whatsoever"],
                "unrealistic_types": [
                    "像素精度: exactly 10x10 pixels",
                    "绝对无瑕: no blurring whatsoever",
                    "100%相同: perfectly identical",
                    "强制优先级: prioritize X over all others"
                ],
                "rewrite_principle": "从'绝对要求'改为'倾向描述'",
                "examples": {
                    "exactly 10x10 pixels": "small square watermark",
                    "no blur whatsoever": "sharp and clean",
                    "perfectly centered": "centered"
                },
                "source_analysis": "pencil_sketch_idol_001"
            })
        }
    ]

    # 5. 插入所有元素到数据库
    all_elements = iron_rules + detection_methods

    for elem in all_elements:
        # 提取领域和类别
        parts = elem["element_id"].split("_")
        domain_id = "prompt_writing"
        category_id = f"prompt_writing_{parts[2]}"  # e.g., prompt_writing_best_practices

        # 插入元素
        cursor.execute("""
        INSERT OR REPLACE INTO elements (
            element_id, domain_id, category_id,
            name, chinese_name,
            ai_prompt_template, keywords,
            reusability_score, confidence_score,
            source_prompts, learned_from,
            metadata, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            elem["element_id"],
            domain_id,
            category_id,
            elem["name"],
            elem["chinese_name"],
            elem["ai_prompt_template"],
            json.dumps(elem["keywords"]),
            elem["reusability_score"],
            0.95,  # 高置信度（从深度分析中提取）
            json.dumps(["pencil_sketch_idol_001"]),
            "anti_pattern_analysis",
            elem["metadata"],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))

        # 添加标签
        for keyword in elem["keywords"]:
            # 插入tag（如果不存在）
            cursor.execute("""
            INSERT OR IGNORE INTO tags (tag_name, tag_type, usage_count)
            VALUES (?, ?, ?)
            """, (keyword, "meta_knowledge", 0))

            # 获取tag_id
            cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (keyword,))
            tag_id = cursor.fetchone()[0]

            # 关联element和tag
            cursor.execute("""
            INSERT OR IGNORE INTO element_tags (element_id, tag_id)
            VALUES (?, ?)
            """, (elem["element_id"], tag_id))

            # 更新tag使用次数
            cursor.execute("""
            UPDATE tags SET usage_count = usage_count + 1
            WHERE tag_id = ?
            """, (tag_id,))

    # 6. 更新领域和类别的元素数量
    cursor.execute("""
    UPDATE domains
    SET total_elements = (SELECT COUNT(*) FROM elements WHERE domain_id = 'prompt_writing'),
        updated_at = ?
    WHERE domain_id = 'prompt_writing'
    """, (datetime.now().isoformat(),))

    for cat_id, _, _ in categories:
        full_cat_id = f"prompt_writing_{cat_id}"
        cursor.execute("""
        UPDATE categories
        SET total_elements = (SELECT COUNT(*) FROM elements WHERE category_id = ?)
        WHERE category_id = ?
        """, (full_cat_id, full_cat_id))

    db.conn.commit()

    # 7. 生成报告
    report = {
        "extraction_time": datetime.now().isoformat(),
        "source": "pencil_sketch_idol_001 (反面教材分析)",
        "domain": "prompt_writing (提示词写作)",
        "extracted_elements": {
            "best_practices": len(iron_rules),
            "detection_methods": len(detection_methods),
            "total": len(all_elements)
        },
        "elements_list": [
            {
                "id": elem["element_id"],
                "name": elem["chinese_name"],
                "reusability": elem["reusability_score"]
            }
            for elem in all_elements
        ],
        "database_stats": {
            "prompt_writing_domain_total": cursor.execute(
                "SELECT total_elements FROM domains WHERE domain_id = 'prompt_writing'"
            ).fetchone()[0]
        }
    }

    db.conn.close()

    return report


def main():
    """主函数"""
    print("🚀 开始提取元知识...")
    print("-" * 60)

    report = extract_meta_knowledge_from_anti_pattern()

    print("✅ 提取完成！")
    print(f"📊 提取时间: {report['extraction_time']}")
    print(f"📚 来源: {report['source']}")
    print(f"🎯 领域: {report['domain']}")
    print()
    print("📦 提取的元素:")
    print(f"  - 最佳实践 (Best Practices): {report['extracted_elements']['best_practices']}个")
    print(f"  - 检测方法 (Detection Methods): {report['extracted_elements']['detection_methods']}个")
    print(f"  - 总计: {report['extracted_elements']['total']}个")
    print()
    print("📋 元素列表:")
    for elem in report['elements_list']:
        print(f"  {elem['id']}")
        print(f"    名称: {elem['name']}")
        print(f"    复用性: {elem['reusability']}/10")
        print()
    print("💾 数据库统计:")
    print(f"  - prompt_writing领域总元素: {report['database_stats']['prompt_writing_domain_total']}个")
    print()
    print("-" * 60)
    print("🎉 元知识已成功添加到elements.db数据库!")

    # 保存报告
    report_path = "extracted_results/meta_knowledge_extraction_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"📄 详细报告已保存至: {report_path}")


if __name__ == "__main__":
    main()
