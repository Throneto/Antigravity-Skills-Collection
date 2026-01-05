#!/usr/bin/env python3
"""
交互式生成器演示脚本
模拟用户选择过程并展示最终结果
"""

import sys
sys.path.insert(0, '/Users/huangzongning/prompt_gen_image')

from prompt_tool import Colors, load_json, FACIAL_FEATURES, MODULE_LIBRARY, GENRE_NAMES

def demo_interactive_build():
    """演示：模拟用户选择并展示结果"""
    facial_lib = load_json(FACIAL_FEATURES)
    module_lib = load_json(MODULE_LIBRARY)

    print(f"\n{Colors.HEADER}{Colors.BOLD}✨ 交互式提示词生成器 - 演示模式{Colors.ENDC}\n")
    print("模拟用户选择过程，展示完整功能\n")
    print("=" * 80)

    # 模拟用户的选择
    demo_selections = {
        'gender_choice': 1,     # 女性
        'age_choice': 1,        # 青年（18-25岁）
        'ethnicity_choice': 1,  # 东亚人
        'genre_choice': 3,      # 电影叙事摄影
        'eye_choice': 2,        # 大蓝眼（真人化）
        'face_choice': 1,       # 精致鹅蛋脸
        'lip_choice': 2,        # 粉嫩光泽唇
        'nose_choice': 2,       # 小巧直鼻
        'skin_choice': 2,       # 真实质感肌
        'expr_choice': 3        # 宁静冒险气质
    }

    selections = {}

    # 第1步：选择性别
    print(f"\n{Colors.BOLD}[1/10] 选择性别:{Colors.ENDC}\n")
    genders = facial_lib.get("gender", {})
    gender_list = []
    for i, (code, data) in enumerate(genders.items(), 1):
        name = data.get("chinese_name", code)
        gender_list.append(code)
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['gender_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC}")

    choice = demo_selections['gender_choice']
    selections['gender'] = gender_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {genders[selections['gender']]['chinese_name']}{Colors.ENDC}")

    # 第2步：选择年龄段
    print(f"\n{Colors.BOLD}[2/10] 选择年龄段:{Colors.ENDC}\n")
    age_ranges = facial_lib.get("age_range", {})
    age_list = []
    for i, (code, data) in enumerate(age_ranges.items(), 1):
        name = data.get("chinese_name", code)
        age_range = data.get("age_range", "")
        age_list.append(code)
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['age_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} ({age_range})")

    choice = demo_selections['age_choice']
    selections['age_range'] = age_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {age_ranges[selections['age_range']]['chinese_name']}{Colors.ENDC}")

    # 第3步：选择人种
    print(f"\n{Colors.BOLD}[3/10] 选择人种:{Colors.ENDC}\n")
    ethnicities = facial_lib.get("ethnicity", {})
    ethnicity_list = []
    for i, (code, data) in enumerate(ethnicities.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        ethnicity_list.append(code)
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['ethnicity_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    choice = demo_selections['ethnicity_choice']
    selections['ethnicity'] = ethnicity_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {ethnicities[selections['ethnicity']]['chinese_name']}{Colors.ENDC}")

    # 第4步：选择摄影流派
    print(f"\n{Colors.BOLD}[4/10] 选择摄影流派:{Colors.ENDC}\n")
    genres = module_lib.get("photography_genres", {})
    genre_list = []
    for i, (code, data) in enumerate(genres.items(), 1):
        name = GENRE_NAMES.get(code, code)
        genre_list.append(code)
        features = data.get("key_features", [])
        feature_preview = features[0] if features else "专业摄影"
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['genre_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} - {feature_preview}")

    choice = demo_selections['genre_choice']
    selections['genre'] = genre_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {GENRE_NAMES.get(selections['genre'])}{Colors.ENDC}")

    # 第5步：选择眼型
    print(f"\n{Colors.BOLD}[5/10] 选择眼型:{Colors.ENDC}\n")
    eye_types = facial_lib.get("eye_types", {})
    eye_list = []
    for i, (code, data) in enumerate(eye_types.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        eye_list.append(code)
        mood = ", ".join(data.get("mood_qualities", [])[:2])
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['eye_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}] - {mood}")

    choice = demo_selections['eye_choice']
    selections['eye_type'] = eye_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {eye_types[selections['eye_type']]['chinese_name']}{Colors.ENDC}")

    # 第6步：选择脸型
    print(f"\n{Colors.BOLD}[6/10] 选择脸型:{Colors.ENDC}\n")
    face_shapes = facial_lib.get("face_shapes", {})
    face_list = []
    for i, (code, data) in enumerate(face_shapes.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        face_list.append(code)
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['face_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    choice = demo_selections['face_choice']
    selections['face_shape'] = face_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {face_shapes[selections['face_shape']]['chinese_name']}{Colors.ENDC}")

    # 第4步：选择唇型
    print(f"\n{Colors.BOLD}[7/10] 选择唇型:{Colors.ENDC}\n")
    lip_types = facial_lib.get("lip_types", {})
    lip_list = []
    for i, (code, data) in enumerate(lip_types.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        lip_list.append(code)
        styles = ", ".join(data.get("suitable_styles", [])[:2])
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['lip_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}] - {styles}")

    choice = demo_selections['lip_choice']
    selections['lip_type'] = lip_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {lip_types[selections['lip_type']]['chinese_name']}{Colors.ENDC}")

    # 第5步：选择鼻型
    print(f"\n{Colors.BOLD}[8/10] 选择鼻型:{Colors.ENDC}\n")
    nose_types = facial_lib.get("nose_types", {})
    nose_list = []
    for i, (code, data) in enumerate(nose_types.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        nose_list.append(code)
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['nose_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    choice = demo_selections['nose_choice']
    selections['nose_type'] = nose_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {nose_types[selections['nose_type']]['chinese_name']}{Colors.ENDC}")

    # 第6步：选择皮肤质感
    print(f"\n{Colors.BOLD}[9/10] 选择皮肤质感:{Colors.ENDC}\n")
    skin_textures = facial_lib.get("skin_textures", {})
    skin_list = []
    for i, (code, data) in enumerate(skin_textures.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        skin_list.append(code)
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['skin_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    choice = demo_selections['skin_choice']
    selections['skin_texture'] = skin_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {skin_textures[selections['skin_texture']]['chinese_name']}{Colors.ENDC}")

    # 第7步：选择表情
    print(f"\n{Colors.BOLD}[10/10] 选择表情:{Colors.ENDC}\n")
    expressions = facial_lib.get("expressions", {})
    expr_list = []
    for i, (code, data) in enumerate(expressions.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        expr_list.append(code)
        tone = data.get("emotional_tone", "")
        marker = f"{Colors.GREEN}→{Colors.ENDC}" if i == demo_selections['expr_choice'] else " "
        print(f"{marker} {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}] - {tone}")

    choice = demo_selections['expr_choice']
    selections['expression'] = expr_list[choice - 1]
    print(f"\n{Colors.YELLOW}用户选择: {choice}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ 已选择: {expressions[selections['expression']]['chinese_name']}{Colors.ENDC}")

    # 组装提示词
    print(f"\n{Colors.HEADER}{Colors.BOLD}🎨 正在组装提示词...{Colors.ENDC}\n")
    print("=" * 80)

    prompt_parts = []
    all_keywords = []

    # 第一部分：构建主体描述（性别 + 年龄 + 人种）
    subject_parts = []

    # 添加形容词
    if 'gender' in selections and selections['gender'] == 'female':
        subject_parts.append("A beautiful")
    elif 'gender' in selections and selections['gender'] == 'male':
        subject_parts.append("A handsome")
    else:
        subject_parts.append("A beautiful")

    # 添加人种（在年龄之前）
    if 'ethnicity' in selections:
        ethnicity_keywords = ethnicities[selections['ethnicity']].get('keywords', [])
        if ethnicity_keywords:
            subject_parts.append(ethnicity_keywords[0])

    # 添加性别词（包含年龄信息）
    if 'gender' in selections:
        gender_data = genders[selections['gender']]
        age_based_terms = gender_data.get('usage_recommendations', {}).get('age_based_terms', {})

        if 'age_range' in selections and selections['age_range'] in age_based_terms:
            # 使用年龄特定的性别词（如 "young woman"）
            subject_parts.append(age_based_terms[selections['age_range']])
        else:
            gender_keywords = gender_data.get('keywords', [])
            if gender_keywords:
                subject_parts.append(gender_keywords[0])
    else:
        subject_parts.append("woman")

    prompt_parts.append(" ".join(subject_parts))

    # 第二部分：收集所有关键词
    if 'eye_type' in selections:
        keywords = eye_types[selections['eye_type']].get('keywords', [])
        all_keywords.extend(keywords)

    if 'face_shape' in selections:
        keywords = face_shapes[selections['face_shape']].get('keywords', [])
        all_keywords.extend(keywords)

    if 'lip_type' in selections:
        keywords = lip_types[selections['lip_type']].get('keywords', [])
        all_keywords.extend(keywords)

    if 'nose_type' in selections:
        keywords = nose_types[selections['nose_type']].get('keywords', [])
        all_keywords.extend(keywords)

    if 'skin_texture' in selections:
        keywords = skin_textures[selections['skin_texture']].get('keywords', [])
        all_keywords.extend(keywords)

    if 'expression' in selections:
        keywords = expressions[selections['expression']].get('keywords', [])
        all_keywords.extend(keywords)

    if all_keywords:
        prompt_parts.append(", ".join(all_keywords))

    # 添加流派技术参数
    if 'genre' in selections:
        genre_data = genres[selections['genre']]
        prompts_using = genre_data.get("prompts", [])

        equipment_index = module_lib.get("camera_equipment_index", {})
        for eq_name, eq_data in equipment_index.items():
            if any(pid in eq_data.get("prompts", []) for pid in prompts_using):
                camera = eq_data.get("specs", {}).get("camera_model", eq_name)
                lens = eq_data.get("specs", {}).get("lens_example", "")
                if camera:
                    prompt_parts.append(f"photographed with {camera}")
                if lens:
                    prompt_parts.append(f"{lens}")
                break

        if selections['genre'] == "cinematic_narrative":
            prompt_parts.append("8K HDR, cinematic lighting, photorealistic, ultra-detailed")
        elif selections['genre'] == "analog_film":
            prompt_parts.append("analog film photography, warm tones, fine grain, nostalgic aesthetic")
        elif selections['genre'] == "portrait_beauty":
            prompt_parts.append("professional portrait photography, soft lighting, high-end retouching")

    final_prompt = ", ".join(prompt_parts)

    print(f"\n{Colors.BOLD}✨ 最终提示词:{Colors.ENDC}\n")
    print(f"{Colors.GREEN}{final_prompt}{Colors.ENDC}\n")
    print("=" * 80)

    # 显示选择摘要
    print(f"\n{Colors.BOLD}📋 选择摘要:{Colors.ENDC}\n")
    print(f"  性别: {genders[selections['gender']]['chinese_name']}")
    print(f"  年龄: {age_ranges[selections['age_range']]['chinese_name']}")
    print(f"  人种: {ethnicities[selections['ethnicity']]['chinese_name']}")
    print(f"  流派: {GENRE_NAMES.get(selections['genre'])}")
    print(f"  眼型: {eye_types[selections['eye_type']]['chinese_name']}")
    print(f"  脸型: {face_shapes[selections['face_shape']]['chinese_name']}")
    print(f"  唇型: {lip_types[selections['lip_type']]['chinese_name']}")
    print(f"  鼻型: {nose_types[selections['nose_type']]['chinese_name']}")
    print(f"  皮肤: {skin_textures[selections['skin_texture']]['chinese_name']}")
    print(f"  表情: {expressions[selections['expression']]['chinese_name']}")

    print(f"\n{Colors.BOLD}💡 如何使用这个提示词:{Colors.ENDC}\n")
    print("1. 复制上面的绿色提示词")
    print("2. 粘贴到AI图像生成工具（如Midjourney、DALL-E、Stable Diffusion）")
    print("3. 根据需要添加场景、服装等细节")
    print("4. 生成图片！")

    print(f"\n{Colors.BOLD}🔄 想要不同的组合？{Colors.ENDC}")
    print(f"再次运行: {Colors.CYAN}python3 prompt_tool.py generate{Colors.ENDC}")
    print("或使用快速模式: {Colors.CYAN}python3 prompt_tool.py build \"你的描述\"{Colors.ENDC}")
    print()

if __name__ == "__main__":
    demo_interactive_build()
