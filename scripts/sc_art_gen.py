#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import sqlite3

# Add project root to path
sys.path.insert(0, os.getcwd())

from mcp_server.tools.intent_parser import parse_intent
from mcp_server.tools.element_query import query_elements, get_db_path
from mcp_server.tools.prompt_composer import compose_prompt
from skill_library.element_db import ElementDB

def main():
    description = "印象派风格的日落后的巴黎街道"
    domain = "art"
    
    print(f"User Request: {description}")
    
    # 1. Parse Intent
    print("\n--- 1. Parsing Intent ---")
    intent = parse_intent(description, domain)
    print(json.dumps(intent, indent=2, ensure_ascii=False))
    
    # 2. Explore Available Categories in 'art' domain
    print("\n--- 2. Exploring Categories ---")
    db = ElementDB(get_db_path())
    cursor = db.conn.cursor()
    cursor.execute("SELECT category_id, name, total_elements FROM categories WHERE domain_id = ?", (domain,))
    categories = cursor.fetchall()
    
    print(f"Available categories in '{domain}':")
    for cat in categories:
        print(f" - {cat['category_id']} ({cat['name']}): {cat['total_elements']} elements")
    
    db.close()
    
    # 3. Query Elements
    print("\n--- 3. Querying Elements ---")
    candidates = []
    
    # Strategy: Query generic art styles or specific medium if available
    # Based on "Impressionist", we want "oil_painting_styles" or "art_styles"
    target_categories = ['art_styles', 'oil_painting_styles', 'ink_wash_techniques', 'artistic_compositions', 'lighting_techniques', 'atmospheres']

    # Filter only existing categories
    existing_cat_ids = [c['category_id'] for c in categories]
    
    # specific keywords to look for
    keywords = ["Impressionism", "Impresionist", "Claude Monet", "oil", "Paris", "street", "sunset", "dusk", "warm lighting"]
    
    # If art_styles is not in existing but others are, we use what we have.
    # Also check 'common' domain for lighting/atmosphere if not in art.
    
    for cat_id in existing_cat_ids:
        if cat_id in target_categories or True: # Just query all art categories with keywords
            # We try to find relevant elements in all art categories
            # using the keywords
            # print(f"Querying category: {cat_id}")
            res = query_elements(domain=domain, category=cat_id, keywords=keywords, limit=5)
            if res:
                # print(f"  -> Found {len(res)} elements in {cat_id}")
                candidates.extend(res)
    
    # Also query 'common' domain for atmosphere/lighting if needed
    common_cats = ['atmospheres', 'lighting_techniques']
    for c in common_cats:
        res = query_elements(domain='common', category=c, keywords=keywords, limit=3)
        if res:
             candidates.extend(res)

    # 4. Select Elements
    print("\n--- 4. Selecting Elements ---")
    # De-duplicate by element_id
    unique_candidates = {e['element_id']: e for e in candidates}
    selected_elements = list(unique_candidates.values())
    
    for e in selected_elements:
        print(f" - [{e['element_id']}] {e['name']} ({e['chinese_name']})")
    
    if not selected_elements:
        print("No elements found! Using fallback generic prompt construction.")
    
    # 5. Compose Prompt
    print("\n--- 5. Composing Prompt ---")
    final_prompt = compose_prompt(selected_elements, mode="detailed", subject_desc="Paris street after sunset in Impressionist style")
    
    print("\n" + "="*40)
    print("🎨 艺术风格解析")
    print(f"- 类型: {intent.get('art_type', 'Unknown')}")
    print(f"- 主题: {intent.get('subject', 'Unknown')}")
    print(f"- 技法: {intent.get('technique', 'Unknown')}")
    print("\n✨ 最终提示词")
    print("────────────────────────────────────────")
    print(final_prompt)
    print("────────────────────────────────────────")

if __name__ == "__main__":
    main()
