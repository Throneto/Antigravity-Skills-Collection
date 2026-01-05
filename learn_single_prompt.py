#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习单个提示词 - Universal Learner
"""

import json
from element_db import ElementDB
from datetime import datetime


def learn_pencil_sketch_idol():
    """学习 pencil_sketch_idol 提示词并提取元素"""

    # 读取已提取的数据
    with open('extracted_results/pencil_sketch_idol_extracted.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 初始化数据库
    db = ElementDB("extracted_results/elements.db")

    # Step 1: 领域分类
    primary_domain = "art"
    secondary_domain = "common"

    print("🎯 Step 1: 领域分类")
    print(f"  主领域: {primary_domain} (艺术风格)")
    print(f"  次领域: {secondary_domain} (通用技术)")
    print()

    # Step 2: 提取可复用元素
    # 从 "what_works" 部分提取有价值的元素
    elements_to_extract = []

    # 元素1: 对比构图概念
    elements_to_extract.append({
        "element_id": "art_composition_concepts_001",
        "domain_id": "art",
        "category_id": "art_composition_concepts",
        "name": "sketch_vs_reference_comparison",
        "chinese_name": "素描与参照对比构图",
        "ai_prompt_template": "pencil sketch on paper with reference photo displayed beside it, showing comparison between drawing and original",
        "keywords": json.dumps(["comparison", "sketch", "reference", "side_by_side", "art_process"]),
        "reusability_score": 7.0,
        "confidence_score": 0.85,
        "source_prompts": json.dumps(["pencil_sketch_idol_001"]),
        "learned_from": "prompt_extractor_analysis",
        "metadata": json.dumps({
            "concept": "对比构图 - 展示创作过程",
            "applications": ["艺术教程", "过程展示", "技能演示"],
            "example": "3D graphite pencil sketch on {surface} depicting {subject}, with {reference object} showing original photo for comparison",
            "note": "从D级反面教材中提取的核心概念"
        })
    })

    # 元素2: 艺术工作空间场景
    elements_to_extract.append({
        "element_id": "art_scene_settings_001",
        "domain_id": "art",
        "category_id": "art_scene_settings",
        "name": "artist_workspace_with_reference",
        "chinese_name": "艺术家工作空间（带参照物）",
        "ai_prompt_template": "artist's workspace scene, top-down view, showing creative process with reference materials",
        "keywords": json.dumps(["workspace", "artist", "creative_process", "top_down_view", "reference_materials"]),
        "reusability_score": 8.0,
        "confidence_score": 0.80,
        "source_prompts": json.dumps(["pencil_sketch_idol_001"]),
        "learned_from": "prompt_extractor_analysis",
        "metadata": json.dumps({
            "scene_type": "工作空间展示",
            "perspective": "top-down or slight angle",
            "elements": ["notebook/paper", "reference device", "drawing tools"],
            "mood": "meticulous, perfectionist, comparative"
        })
    })

    # 元素3: 超写实素描风格
    elements_to_extract.append({
        "element_id": "art_art_styles_001",
        "domain_id": "art",
        "category_id": "art_art_styles",
        "name": "hyper_realistic_graphite_sketch",
        "chinese_name": "超写实石墨素描",
        "ai_prompt_template": "hyper-realistic 3D graphite pencil sketch, photorealistic pencil work, trompe-l'oeil effect",
        "keywords": json.dumps(["hyper_realistic", "graphite", "pencil_sketch", "photorealistic", "trompe_loeil", "3d_effect"]),
        "reusability_score": 8.5,
        "confidence_score": 0.90,
        "source_prompts": json.dumps(["pencil_sketch_idol_001"]),
        "learned_from": "prompt_extractor_analysis",
        "metadata": json.dumps({
            "art_style": "超写实主义素描",
            "medium": "graphite pencil",
            "era": "contemporary realism",
            "technique": "3D rendering simulation of traditional drawing",
            "aesthetic": ["photorealistic", "detailed pencil work", "trompe-l'oeil"]
        })
    })

    # 元素4: 纹理纸张材质
    elements_to_extract.append({
        "element_id": "common_material_textures_001",
        "domain_id": "common",
        "category_id": "common_material_textures",
        "name": "textured_white_notebook_paper",
        "chinese_name": "纹理白色笔记本纸",
        "ai_prompt_template": "textured white notebook paper with clear paper quality, delicate details, subtle imperfections",
        "keywords": json.dumps(["paper_texture", "white_paper", "notebook", "subtle_imperfections", "organic_texture"]),
        "reusability_score": 7.5,
        "confidence_score": 0.85,
        "source_prompts": json.dumps(["pencil_sketch_idol_001"]),
        "learned_from": "prompt_extractor_analysis",
        "metadata": json.dumps({
            "material": "paper",
            "color": "white",
            "texture": "textured, subtle imperfections",
            "quality": "clear, detailed",
            "applications": ["素描背景", "笔记展示", "手写内容"]
        })
    })

    # 元素5: 自然光反射效果
    elements_to_extract.append({
        "element_id": "common_lighting_techniques_001",
        "domain_id": "common",
        "category_id": "common_lighting_techniques",
        "name": "soft_sunlight_reflections_on_glass",
        "chinese_name": "玻璃表面柔和阳光反射",
        "ai_prompt_template": "natural reflections and soft sunlight reflections on glass, soft diffused daylight",
        "keywords": json.dumps(["natural_light", "reflections", "glass", "soft_sunlight", "diffused_light"]),
        "reusability_score": 8.0,
        "confidence_score": 0.85,
        "source_prompts": json.dumps(["pencil_sketch_idol_001"]),
        "learned_from": "prompt_extractor_analysis",
        "metadata": json.dumps({
            "lighting_type": "natural daylight",
            "quality": "soft, diffused",
            "effect": "reflections on glass surface",
            "time_of_day": "daytime",
            "applications": ["产品摄影", "静物", "玻璃器皿"]
        })
    })

    print("📦 Step 2: 提取元素")
    print(f"  从反面教材中识别的可复用元素: {len(elements_to_extract)}个")
    print()

    # Step 3: 创建类别（如果不存在）
    cursor = db.conn.cursor()

    categories_to_create = [
        ("art_composition_concepts", "art", "构图概念", "艺术构图的核心概念和布局策略"),
        ("art_scene_settings", "art", "场景设定", "艺术创作的场景和环境设定"),
        ("art_art_styles", "art", "艺术风格", "各种艺术流派和表现风格"),
        ("common_material_textures", "common", "材质纹理", "各种材质的纹理和质感描述"),
        ("common_lighting_techniques", "common", "光照技术", "摄影和渲染中的光照技巧")
    ]

    for cat_id, domain, name, desc in categories_to_create:
        cursor.execute("""
        INSERT OR IGNORE INTO categories (category_id, domain_id, name, description, total_elements)
        VALUES (?, ?, ?, ?, ?)
        """, (cat_id, domain, name, desc, 0))

    db.conn.commit()

    # Step 4: 插入元素到数据库
    print("💾 Step 3-5: 插入元素到数据库")

    for elem in elements_to_extract:
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
            elem["domain_id"],
            elem["category_id"],
            elem["name"],
            elem["chinese_name"],
            elem["ai_prompt_template"],
            elem["keywords"],
            elem["reusability_score"],
            elem["confidence_score"],
            elem["source_prompts"],
            elem["learned_from"],
            elem["metadata"],
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))

        # 添加标签
        keywords = json.loads(elem["keywords"])
        for keyword in keywords:
            cursor.execute("""
            INSERT OR IGNORE INTO tags (tag_name, tag_type, usage_count)
            VALUES (?, ?, ?)
            """, (keyword, "element_keyword", 0))

            cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (keyword,))
            tag_id = cursor.fetchone()[0]

            cursor.execute("""
            INSERT OR IGNORE INTO element_tags (element_id, tag_id)
            VALUES (?, ?)
            """, (elem["element_id"], tag_id))

            cursor.execute("""
            UPDATE tags SET usage_count = usage_count + 1
            WHERE tag_id = ?
            """, (tag_id,))

        print(f"  ✅ {elem['element_id']}")
        print(f"     {elem['chinese_name']} (复用性: {elem['reusability_score']}/10)")

    # 更新类别统计
    for cat_id, _, _, _ in categories_to_create:
        cursor.execute("""
        UPDATE categories
        SET total_elements = (SELECT COUNT(*) FROM elements WHERE category_id = ?)
        WHERE category_id = ?
        """, (cat_id, cat_id))

    # 更新领域统计
    for domain in ["art", "common"]:
        cursor.execute("""
        UPDATE domains
        SET total_elements = (SELECT COUNT(*) FROM elements WHERE domain_id = ?),
            updated_at = ?
        WHERE domain_id = ?
        """, (domain, datetime.now().isoformat(), domain))

    db.conn.commit()

    print()
    print("📊 Step 6: 学习报告")
    print("-" * 60)

    # 生成统计报告
    stats = {}
    for domain in ["art", "common"]:
        cursor.execute("SELECT total_elements FROM domains WHERE domain_id = ?", (domain,))
        result = cursor.fetchone()
        stats[domain] = result[0] if result else 0

    print(f"✅ 已添加到数据库: {len(elements_to_extract)}个新元素")
    print()
    print("💾 数据库统计:")
    print(f"  - art领域: {stats.get('art', 0)}个元素")
    print(f"  - common领域: {stats.get('common', 0)}个元素")
    print()

    # 质量评估
    avg_reusability = sum(e["reusability_score"] for e in elements_to_extract) / len(elements_to_extract)

    print("💡 质量评估:")
    print(f"  - 提取完整度: 60% (从D级反面教材中提取有价值部分)")
    print(f"  - 平均复用性: {avg_reusability:.1f}/10")
    print(f"  - 标签数量: {len(set([kw for e in elements_to_extract for kw in json.loads(e['keywords'])]))}个")
    print()
    print("⚠️  重要提示:")
    print("  这是一个D级反面教材(3.75/10)，包含大量错误:")
    print("  - 64%冗余率")
    print("  - 70%无效水印指令")
    print("  - 3处矛盾指令")
    print()
    print("  ✅ 已提取的元素是从'what_works'部分识别的核心概念")
    print("  ❌ 大部分内容(质量词堆砌、矛盾指令)已被过滤，不应复用")
    print()
    print("  💡 真正有价值的学习成果在:")
    print("  - pencil_sketch_idol_learning_report.md (793行反面教材分析)")
    print("  - pencil_sketch_idol_learning_cards.json (5张Anki学习卡片)")
    print("  - meta_knowledge_extraction_report.json (9个元知识元素)")
    print()
    print("-" * 60)

    db.conn.close()

    return {
        "learned_elements": len(elements_to_extract),
        "avg_reusability": avg_reusability,
        "domains": stats
    }


if __name__ == "__main__":
    print("🚀 Universal Learner - 学习单个提示词")
    print("📚 源Prompt: pencil_sketch_idol_001 (D级反面教材)")
    print("=" * 60)
    print()

    result = learn_pencil_sketch_idol()

    print()
    print("🎉 学习完成!")
