
import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from skill_library.intelligent_generator import IntelligentGenerator

def main():
    gen = IntelligentGenerator()
    
    print("🤖 Manual Cyberpunk Generation (with fallback data)...")
    
    keywords_to_search = [
        "cinematic lighting",
        "futuristic"
    ]
    
    # 1. Search for what we have
    found_elements = gen.search_style_elements(keywords_to_search, domain='portrait')
    
    selected_elements = found_elements.copy()
    
    # 2. Inject missing elements (since DB is incomplete for Cyberpunk)
    fallback_elements = [
        {
            'name': 'cyberpunk_female_warrior',
            'chinese_name': '赛博朋克女战士',
            'category': 'subject',
            'template': 'cyberpunk female warrior, cybernetic implants, tactical armor, battle hardened',
            'keywords': ['female', 'warrior', 'cyberpunk', 'cyborg']
        },
        {
            'name': 'blade_runner_style',
            'chinese_name': '银翼杀手风格',
            'category': 'atmosphere',
            'template': 'Blade Runner aesthetic, futuristic dystopian city background, rain-slicked streets, towering skyscrapers, flying cars, high tech low life atmosphere',
            'keywords': ['blade runner', 'dystopian', 'futuristic city', 'rain']
        },
        {
            'name': 'neon_noir_lighting',
            'chinese_name': '霓虹黑色电影光效',
            'category': 'lighting',
            'template': 'neon noir lighting, vibrant pink and blue neon signs, volumetric fog, dramatic rim lighting, reflection on wet surfaces',
            'keywords': ['neon', 'lighting', 'colorful', 'fog']
        },
         {
            'name': 'tsui_hark_dynamic',
            'chinese_name': '徐克式动态效果', # Adding a bit of "warrior" flair implicitly requested
            'category': 'composition',
            'template': 'dynamic action pose, low angle shot, wind blowing hair',
            'keywords': ['dynamic', 'action', 'wind']
        }
    ]
    
    print(f"Found {len(found_elements)} elements in DB.")
    print(f"Injecting {len(fallback_elements)} fallback elements.")
    
    selected_elements.extend(fallback_elements)
    
    print("\nSelected Elements:")
    for e in selected_elements:
        print(f"- {e['chinese_name']} ({e['name']})")
        
    # Consistency Check
    issues = gen.check_consistency(selected_elements)
    if issues:
        print(f"\n⚠️ Found {len(issues)} consistency issues:")
        for i in issues:
            print(f"  - {i['description']}")
        # We skip auto-resolve for fallbacks to preserve specific intent, 
        # unless it's critical.
        
    # Compose
    prompt = gen.compose_prompt(selected_elements, mode='simple')
    
    # Post-process: ensure unique keywords manually if compose didn't catch all
    # (The compose_prompt function does some dedupe)
    
    print("\n✨ Generated Prompt:")
    print("────────────────────────────────────────")
    print(prompt)
    print("────────────────────────────────────────")

if __name__ == "__main__":
    main()
