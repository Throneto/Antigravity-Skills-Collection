#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from mcp_server.tools.intent_parser import parse_intent
from skill_library.intelligent_generator import IntelligentGenerator

def main():
    if len(sys.argv) > 1:
        user_request = sys.argv[1]
    else:
        user_request = "侧脸微距人像，自然光"
        
    print(f"用户需求: {user_request}\n")
    
    # 1. Parse Intent
    intent = parse_intent(user_request, domain_hint='portrait')
    print("📋 意图解析")
    print(json.dumps(intent, indent=2, ensure_ascii=False))
    print("")

    # Adapter for IntelligentGenerator
    adapted_intent = intent.copy()
    
    # Flatten styling
    if 'styling' in intent:
        adapted_intent['clothing'] = intent['styling'].get('clothing', 'modern')
        adapted_intent['hairstyle'] = intent['styling'].get('hairstyle', 'modern')
        if 'makeup' in intent['styling']:
             # IntelligentGenerator might expect makeup at top level or within styling logic internally
             pass # Logic inside select_elements handles nested dicts often if designed well, checking source would be ideal but simple assumption first.
             
    # Flatten scene/atmosphere
    if 'scene' in intent:
        adapted_intent['era'] = intent['scene'].get('era', 'modern')
        
    # Flatten lighting
    if 'lighting' in intent and isinstance(intent['lighting'], dict):
        adapted_intent['lighting'] = intent['lighting'].get('lighting_type', 'natural')

    # 2. Select Elements
    gen = IntelligentGenerator()
    try:
        elements = gen.select_elements_by_intent(adapted_intent)
        
        # --- Advanced Custom Logic: Manual Keyword Injection ---
        # The default parser might miss specific technical terms or poses.
        # We manually check and inject them here.
        
        extra_keywords = []
        if "侧脸" in user_request or "侧面" in user_request:
            print("🔍 识别到 '侧脸' 需求，正在搜索相关元素...")
            extra_keywords.append("side profile")
            
        if "微距" in user_request:
            print("🔍 识别到 '微距' 需求，正在搜索相关元素...")
            extra_keywords.append("macro")
            extra_keywords.append("extreme close up")

        if extra_keywords:
            # Search for best matching elements
            additional_elements = gen.search_style_elements(extra_keywords, domain='portrait')
            for elem in additional_elements:
                print(f"  + 添加额外元素: {elem['chinese_name']} ({elem['name']})")
                elements.append(elem)
                
        print("\n🎨 选用元素")
        for elem in elements:
            print(f"- {elem['chinese_name']} ({elem['name']}) [{elem['category']}]")
        print("")
    
        # 3. Check Consistency & Resolve
        issues = gen.check_consistency(elements)
        if issues:
            print(f"⚠️ 发现 {len(issues)} 个冲突，正在修复...")
            fixed_elements, fixes = gen.resolve_conflicts(elements, issues)
            elements = fixed_elements
            for fix in fixes:
                print(f"  - {fix}")
        else:
            print("✅ 一致性检查通过")
        
        # 4. Compose Prompt
        prompt = gen.compose_prompt(elements, mode='auto')
        
        print("\n✨ 最终提示词")
        print("────────────────────────────────────────")
        print(prompt)
        print("────────────────────────────────────────")
        
    except Exception as e:
        print(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        gen.close()

if __name__ == "__main__":
    main()
