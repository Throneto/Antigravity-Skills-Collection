#!/usr/bin/env python3
"""
Prompt Extraction Tool - CLI交互工具
提供命令行交互界面，查询和推荐提示词

Usage:
    python prompt_tool.py list                    # 列出所有提示词
    python prompt_tool.py show <id>               # 查看详细信息
    python prompt_tool.py recommend <id>          # 获取推荐
    python prompt_tool.py search --genre <genre>  # 按流派搜索
    python prompt_tool.py search --equipment <eq> # 按设备搜索
    python prompt_tool.py compare <id1> <id2>     # 对比两个提示词
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import os

# ANSI颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 数据文件路径
SCRIPT_DIR = Path(__file__).parent
EXTRACTED_MODULES = SCRIPT_DIR / "extracted_results" / "extracted_modules.json"
MODULE_LIBRARY = SCRIPT_DIR / "extracted_results" / "module_library.json"
FACIAL_FEATURES = SCRIPT_DIR / "extracted_results" / "facial_features_library.json"

# 流派中文名映射
GENRE_NAMES = {
    "digital_commercial": "数码商业摄影",
    "analog_film": "胶片艺术摄影",
    "cinematic_narrative": "电影叙事摄影",
    "studio_product": "棚拍产品摄影",
    "editorial_macro": "编辑微距摄影",
    "conceptual_art": "概念艺术摄影",
    "portrait_beauty": "人像美容摄影",
    "hybrid_illustration": "混合插画风格",
    "3d_render": "3D渲染风格",
    "collage_composite": "拼贴合成摄影"
}

def load_json(filepath: Path) -> Dict:
    """加载JSON文件"""
    if not filepath.exists():
        print(f"{Colors.RED}错误: 文件不存在 {filepath}{Colors.ENDC}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_prompt_title(prompt: Dict) -> str:
    """获取提示词标题（从theme提取）"""
    theme = prompt.get("theme", "未命名提示词")
    # 提取主题的第一部分作为标题
    return theme.split(" / ")[0] if " / " in theme else theme

def list_all_prompts():
    """列出所有提示词"""
    data = load_json(EXTRACTED_MODULES)

    print(f"\n{Colors.HEADER}{Colors.BOLD}📊 提示词列表 (共{len(data)}个){Colors.ENDC}\n")
    print(f"{'ID':<4} {'标题':<30} {'类型':<15} {'评分':<6} {'流派':<20}")
    print("=" * 85)

    for prompt in data:
        pid = prompt.get("prompt_id", "?")
        title = get_prompt_title(prompt)[:28]
        ptype = prompt.get("format", prompt.get("theme", "静态图像"))[:13]
        score = prompt.get("quality_score", {}).get("overall_score", 0)

        # 获取摄影流派
        genre = prompt.get("modules", {}).get("visual_style", {}).get("photography_genre")
        genre_display = GENRE_NAMES.get(genre, "-") if genre else "-"

        # 根据评分着色
        if score >= 10.0:
            score_color = Colors.GREEN
        elif score >= 9.5:
            score_color = Colors.CYAN
        else:
            score_color = Colors.ENDC

        print(f"{pid:<4} {title:<30} {ptype:<15} {score_color}{score:<6.1f}{Colors.ENDC} {genre_display:<20}")

    print()

def show_prompt_detail(prompt_id: int):
    """显示提示词详细信息"""
    data = load_json(EXTRACTED_MODULES)

    # 查找提示词
    prompt = next((p for p in data if p.get("prompt_id") == prompt_id), None)
    if not prompt:
        print(f"{Colors.RED}错误: 未找到提示词 #{prompt_id}{Colors.ENDC}")
        return

    title = get_prompt_title(prompt)
    modules = prompt.get("modules", {})

    print(f"\n{Colors.HEADER}{Colors.BOLD}📸 Prompt #{prompt_id}: {title}{Colors.ENDC}\n")

    # 基本信息
    print(f"{Colors.BOLD}基本信息:{Colors.ENDC}")
    print(f"  主题: {prompt.get('theme', 'N/A')}")
    print(f"  长度: {prompt.get('prompt_length', 0)} 字符")
    print(f"  评分: {Colors.GREEN}{prompt.get('quality_score', {}).get('overall_score', 0)}/10{Colors.ENDC}")

    # 摄影流派
    visual_style = modules.get("visual_style", {})
    genre = visual_style.get("photography_genre")
    if genre:
        confidence = visual_style.get("genre_confidence", 0)
        print(f"\n{Colors.BOLD}摄影流派:{Colors.ENDC}")
        print(f"  {Colors.CYAN}{GENRE_NAMES.get(genre, genre)}{Colors.ENDC} (置信度: {confidence*100:.0f}%)")

    # 技术参数
    tech_params = modules.get("technical_parameters", {})
    if tech_params:
        print(f"\n{Colors.BOLD}技术参数:{Colors.ENDC}")
        camera = tech_params.get("camera", "N/A")
        print(f"  相机: {camera}")

        lens = tech_params.get("lens")
        if lens:
            print(f"  镜头: {lens}")

        film = tech_params.get("film")
        if film:
            print(f"  胶卷: {film}")

        resolution = tech_params.get("resolution")
        if resolution:
            print(f"  分辨率: {resolution}")

    # 对立标准
    constraints = modules.get("constraints", {})
    oppositions = constraints.get("critical_oppositions", {})
    if oppositions:
        print(f"\n{Colors.BOLD}对立标准:{Colors.ENDC}")
        for category, rules in oppositions.items():
            print(f"  {category}:")
            print(f"    {Colors.GREEN}✓ 必须:{Colors.ENDC} {rules.get('required', 'N/A')[:60]}")
            print(f"    {Colors.RED}✗ 禁止:{Colors.ENDC} {rules.get('forbidden', 'N/A')[:60]}")

    # 应用场景
    unique_features = prompt.get("unique_features", [])
    if unique_features:
        print(f"\n{Colors.BOLD}独特特征:{Colors.ENDC}")
        for i, feature in enumerate(unique_features[:3], 1):
            print(f"  {i}. {feature}")

    print()

def search_by_genre(genre: str):
    """按流派搜索"""
    data = load_json(EXTRACTED_MODULES)
    module_lib = load_json(MODULE_LIBRARY)

    # 查找流派信息
    genres = module_lib.get("photography_genres", {})
    genre_info = genres.get(genre)

    if not genre_info:
        print(f"{Colors.RED}错误: 未知流派 '{genre}'{Colors.ENDC}")
        print(f"\n可用流派:")
        for g in genres.keys():
            print(f"  - {g} ({GENRE_NAMES.get(g, g)})")
        return

    print(f"\n{Colors.HEADER}{Colors.BOLD}🔍 流派: {GENRE_NAMES.get(genre, genre)}{Colors.ENDC}\n")

    # 显示流派信息
    print(f"{Colors.BOLD}流派特征:{Colors.ENDC}")
    for feature in genre_info.get("key_features", []):
        print(f"  • {feature}")

    print(f"\n{Colors.BOLD}典型设备:{Colors.ENDC}")
    for eq in genre_info.get("typical_equipment", []):
        print(f"  • {eq}")

    print(f"\n{Colors.BOLD}应用场景:{Colors.ENDC}")
    for use_case in genre_info.get("use_cases", []):
        print(f"  • {use_case}")

    # 列出该流派的提示词
    prompt_ids = genre_info.get("prompts", [])
    print(f"\n{Colors.BOLD}相关提示词 ({len(prompt_ids)}个):{Colors.ENDC}")

    for pid in prompt_ids:
        prompt = next((p for p in data if p.get("prompt_id") == pid), None)
        if prompt:
            title = get_prompt_title(prompt)
            score = prompt.get("quality_score", {}).get("overall_score", 0)
            print(f"  #{pid:<3} {title:<40} {Colors.GREEN}{score}/10{Colors.ENDC}")

    print()

def search_by_equipment(equipment: str):
    """按设备搜索"""
    module_lib = load_json(MODULE_LIBRARY)

    # 查找设备信息
    equipment_index = module_lib.get("camera_equipment_index", {})

    # 模糊匹配设备名称
    matched_key = None
    for key in equipment_index.keys():
        if equipment.lower() in key.lower():
            matched_key = key
            break

    if not matched_key:
        print(f"{Colors.RED}错误: 未找到设备 '{equipment}'{Colors.ENDC}")
        print(f"\n可用设备:")
        for eq in equipment_index.keys():
            print(f"  - {eq}")
        return

    eq_info = equipment_index[matched_key]

    print(f"\n{Colors.HEADER}{Colors.BOLD}📷 设备: {matched_key}{Colors.ENDC}\n")

    # 显示设备信息
    print(f"{Colors.BOLD}典型应用:{Colors.ENDC}")
    print(f"  {eq_info.get('typical_use', 'N/A')}")

    specs = eq_info.get("specs", {})
    if specs:
        print(f"\n{Colors.BOLD}技术规格:{Colors.ENDC}")
        for key, value in specs.items():
            print(f"  • {key}: {value}")

    print(f"\n{Colors.BOLD}成本信息:{Colors.ENDC}")
    print(f"  租赁: {eq_info.get('rental_cost', 'N/A')}")
    print(f"  购买: {eq_info.get('purchase_cost', 'N/A')}")

    strengths = eq_info.get("strengths", [])
    if strengths:
        print(f"\n{Colors.BOLD}设备优势:{Colors.ENDC}")
        for strength in strengths:
            print(f"  • {strength}")

    # 列出使用该设备的提示词
    prompt_ids = eq_info.get("prompts", [])
    print(f"\n{Colors.BOLD}使用该设备的提示词 ({len(prompt_ids)}个):{Colors.ENDC}")

    data = load_json(EXTRACTED_MODULES)
    for pid in prompt_ids:
        prompt = next((p for p in data if p.get("prompt_id") == pid), None)
        if prompt:
            title = get_prompt_title(prompt)
            print(f"  #{pid} {title}")

    print()

def recommend_prompts(prompt_id: int, top_k: int = 3):
    """推荐相似提示词（简化版实现）"""
    data = load_json(EXTRACTED_MODULES)

    # 查找当前提示词
    current = next((p for p in data if p.get("prompt_id") == prompt_id), None)
    if not current:
        print(f"{Colors.RED}错误: 未找到提示词 #{prompt_id}{Colors.ENDC}")
        return

    current_title = get_prompt_title(current)
    current_genre = current.get("modules", {}).get("visual_style", {}).get("photography_genre")

    print(f"\n{Colors.HEADER}{Colors.BOLD}🔍 为 Prompt #{prompt_id} ({current_title}) 推荐相关提示词{Colors.ENDC}\n")

    # 简化推荐逻辑：基于流派相似度
    recommendations = []

    for candidate in data:
        cid = candidate.get("prompt_id")
        if cid == prompt_id:
            continue

        candidate_genre = candidate.get("modules", {}).get("visual_style", {}).get("photography_genre")

        # 计算简单相似度
        score = 0.0
        reasons = []

        # 流派相同 +0.5
        if current_genre and candidate_genre == current_genre:
            score += 0.5
            reasons.append(f"同为{GENRE_NAMES.get(current_genre, current_genre)}")

        # 设备相同 +0.3
        current_camera = current.get("modules", {}).get("technical_parameters", {}).get("camera", "")
        candidate_camera = candidate.get("modules", {}).get("technical_parameters", {}).get("camera", "")

        if current_camera and current_camera == candidate_camera:
            score += 0.3
            reasons.append(f"同用{current_camera}")

        # 主题相关 +0.2
        current_theme = current.get("theme", "")
        candidate_theme = candidate.get("theme", "")

        if any(keyword in candidate_theme for keyword in current_theme.split(" / ")):
            score += 0.2
            reasons.append("主题相关")

        if score > 0:
            recommendations.append({
                "id": cid,
                "title": get_prompt_title(candidate),
                "score": score,
                "reason": " + ".join(reasons) if reasons else "相关提示词"
            })

    # 按分数排序
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # 输出Top K
    if not recommendations:
        print(f"{Colors.YELLOW}暂无相关推荐{Colors.ENDC}\n")
        return

    for i, rec in enumerate(recommendations[:top_k], 1):
        print(f"{Colors.BOLD}[{i}] #{rec['id']} {rec['title']}{Colors.ENDC}")
        print(f"    {Colors.CYAN}相似度: {rec['score']*100:.0f}%{Colors.ENDC}")
        print(f"    {Colors.GREEN}理由: {rec['reason']}{Colors.ENDC}\n")

def compare_prompts(id1: int, id2: int):
    """对比两个提示词"""
    data = load_json(EXTRACTED_MODULES)

    p1 = next((p for p in data if p.get("prompt_id") == id1), None)
    p2 = next((p for p in data if p.get("prompt_id") == id2), None)

    if not p1:
        print(f"{Colors.RED}错误: 未找到提示词 #{id1}{Colors.ENDC}")
        return
    if not p2:
        print(f"{Colors.RED}错误: 未找到提示词 #{id2}{Colors.ENDC}")
        return

    print(f"\n{Colors.HEADER}{Colors.BOLD}⚖️  对比: #{id1} vs #{id2}{Colors.ENDC}\n")

    # 对比表格
    attrs = [
        ("标题", lambda p: get_prompt_title(p)),
        ("评分", lambda p: f"{p.get('quality_score', {}).get('overall_score', 0)}/10"),
        ("流派", lambda p: GENRE_NAMES.get(p.get("modules", {}).get("visual_style", {}).get("photography_genre"), "-")),
        ("相机", lambda p: p.get("modules", {}).get("technical_parameters", {}).get("camera", "-")),
        ("分辨率", lambda p: p.get("modules", {}).get("technical_parameters", {}).get("resolution", "-")),
    ]

    print(f"{'属性':<15} {'Prompt #' + str(id1):<40} {'Prompt #' + str(id2):<40}")
    print("=" * 95)

    for attr_name, extractor in attrs:
        v1 = extractor(p1)
        v2 = extractor(p2)
        print(f"{attr_name:<15} {v1:<40} {v2:<40}")

    print()

def facial_list_types():
    """列出所有五官类型"""
    facial_lib = load_json(FACIAL_FEATURES)

    print(f"\n{Colors.HEADER}{Colors.BOLD}📊 五官特征分类库{Colors.ENDC}\n")

    categories = [
        ("eye_types", "眼型"),
        ("face_shapes", "脸型"),
        ("lip_types", "唇型"),
        ("nose_types", "鼻型"),
        ("skin_textures", "皮肤质感"),
        ("expressions", "表情")
    ]

    for cat_key, cat_name in categories:
        items = facial_lib.get(cat_key, {})
        print(f"{Colors.BOLD}{cat_name} ({len(items)}种):{Colors.ENDC}")
        for code, data in items.items():
            chinese_name = data.get("chinese_name", code)
            score = data.get("reusability_score", 0)
            prompts = data.get("prompts_using_this", [])
            print(f"  {Colors.CYAN}{code:<25}{Colors.ENDC} {chinese_name:<15} {Colors.GREEN}({score}/10){Colors.ENDC} Prompts: {prompts}")
        print()

def facial_search_by_type(type_category, type_value):
    """按五官类型查询"""
    facial_lib = load_json(FACIAL_FEATURES)

    category_map = {
        "eye": "eye_types",
        "skin": "skin_textures",
        "expression": "expressions"
    }

    cat_key = category_map.get(type_category)
    if not cat_key:
        print(f"{Colors.RED}错误: 未知类型 '{type_category}'{Colors.ENDC}")
        return

    items = facial_lib.get(cat_key, {})

    # 模糊匹配
    matched_key = None
    for key in items.keys():
        if type_value.lower() in key.lower():
            matched_key = key
            break

    if not matched_key:
        print(f"{Colors.RED}错误: 未找到 '{type_value}'{Colors.ENDC}")
        print(f"\n可用选项:")
        for key, data in items.items():
            print(f"  - {key} ({data.get('chinese_name', '')})")
        return

    feature = items[matched_key]

    print(f"\n{Colors.HEADER}{Colors.BOLD}🔍 五官特征: {feature.get('chinese_name', matched_key)}{Colors.ENDC}\n")

    # 视觉特征
    print(f"{Colors.BOLD}视觉特征:{Colors.ENDC}")
    visual = feature.get("visual_features", {})
    for k, v in visual.items():
        print(f"  • {k}: {v}")

    # 关键词
    print(f"\n{Colors.BOLD}提示词关键词:{Colors.ENDC}")
    for kw in feature.get("keywords", []):
        print(f"  • {kw}")

    # 适合风格
    print(f"\n{Colors.BOLD}适合风格:{Colors.ENDC}")
    for style in feature.get("suitable_styles", []):
        print(f"  • {style}")

    # 使用该特征的Prompts
    prompt_ids = feature.get("prompts_using_this", [])
    print(f"\n{Colors.BOLD}使用该特征的Prompts ({len(prompt_ids)}个):{Colors.ENDC}")

    data = load_json(EXTRACTED_MODULES)
    for pid in prompt_ids:
        prompt = next((p for p in data if p.get("prompt_id") == pid), None)
        if prompt:
            title = get_prompt_title(prompt)
            score = prompt.get("quality_score", {}).get("overall_score", 0)
            print(f"  #{pid:<3} {title:<40} {Colors.GREEN}{score}/10{Colors.ENDC}")

    # 使用建议
    recommendations = feature.get("usage_recommendations", {})
    if recommendations:
        print(f"\n{Colors.BOLD}使用建议:{Colors.ENDC}")
        for key, value in recommendations.items():
            print(f"  • {key}: {value}")

    print()

def facial_recommend_by_style(style):
    """按风格推荐五官组合"""
    facial_lib = load_json(FACIAL_FEATURES)

    usage_index = facial_lib.get("usage_index", {})
    by_style = usage_index.get("by_style_mood", {})

    if style not in by_style:
        print(f"{Colors.RED}错误: 未找到风格 '{style}'{Colors.ENDC}")
        print(f"\n可用风格:")
        for s in by_style.keys():
            print(f"  - {s}")
        return

    combo = by_style[style]

    print(f"\n{Colors.HEADER}{Colors.BOLD}🎨 风格: {style}{Colors.ENDC}\n")
    print(f"{Colors.BOLD}推荐五官组合:{Colors.ENDC}\n")

    feature_types = {
        "eyes": ("eye_types", "眼型"),
        "face": ("face_shapes", "脸型"),
        "lips": ("lip_types", "唇型"),
        "nose": ("nose_types", "鼻型"),
        "skin": ("skin_textures", "皮肤质感"),
        "expression": ("expressions", "表情")
    }

    for key, (cat_key, cat_name) in feature_types.items():
        if key in combo:
            code = combo[key]
            feature = facial_lib.get(cat_key, {}).get(code, {})
            chinese_name = feature.get("chinese_name", code)
            score = feature.get("reusability_score", 0)

            print(f"{Colors.BOLD}{cat_name}:{Colors.ENDC} {Colors.CYAN}{chinese_name}{Colors.ENDC} ({code}) {Colors.GREEN}[{score}/10]{Colors.ENDC}")

            # 显示关键词
            keywords = feature.get("keywords", [])
            if keywords:
                print(f"  关键词: {', '.join(keywords[:3])}")
            print()

    print()

def interactive_build():
    """交互式问答 - 自由组合模块生成提示词"""
    facial_lib = load_json(FACIAL_FEATURES)
    module_lib = load_json(MODULE_LIBRARY)

    print(f"\n{Colors.HEADER}{Colors.BOLD}✨ 交互式提示词生成器{Colors.ENDC}\n")
    print("通过问答方式，自由选择模块组合成完整提示词\n")
    print("=" * 80)

    selections = {}

    # 第1步：选择性别
    print(f"\n{Colors.BOLD}[1/10] 选择性别:{Colors.ENDC}\n")
    genders = facial_lib.get("gender", {})
    gender_list = []
    for i, (code, data) in enumerate(genders.items(), 1):
        name = data.get("chinese_name", code)
        gender_list.append(code)
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC}")

    gender_choice = input(f"\n请选择 (1-{len(gender_list)}) 或按Enter跳过: ").strip()
    if gender_choice.isdigit() and 1 <= int(gender_choice) <= len(gender_list):
        selections['gender'] = gender_list[int(gender_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {genders[selections['gender']]['chinese_name']}{Colors.ENDC}")

    # 第2步：选择年龄段
    print(f"\n{Colors.BOLD}[2/10] 选择年龄段:{Colors.ENDC}\n")
    age_ranges = facial_lib.get("age_range", {})
    age_list = []
    for i, (code, data) in enumerate(age_ranges.items(), 1):
        name = data.get("chinese_name", code)
        age_range = data.get("age_range", "")
        age_list.append(code)
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} ({age_range})")

    age_choice = input(f"\n请选择 (1-{len(age_list)}) 或按Enter跳过: ").strip()
    if age_choice.isdigit() and 1 <= int(age_choice) <= len(age_list):
        selections['age_range'] = age_list[int(age_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {age_ranges[selections['age_range']]['chinese_name']}{Colors.ENDC}")

    # 第3步：选择人种
    print(f"\n{Colors.BOLD}[3/10] 选择人种:{Colors.ENDC}\n")
    ethnicities = facial_lib.get("ethnicity", {})
    ethnicity_list = []
    for i, (code, data) in enumerate(ethnicities.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        ethnicity_list.append(code)
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    ethnicity_choice = input(f"\n请选择 (1-{len(ethnicity_list)}) 或按Enter跳过: ").strip()
    if ethnicity_choice.isdigit() and 1 <= int(ethnicity_choice) <= len(ethnicity_list):
        selections['ethnicity'] = ethnicity_list[int(ethnicity_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {ethnicities[selections['ethnicity']]['chinese_name']}{Colors.ENDC}")

    # 第4步：选择摄影流派
    print(f"\n{Colors.BOLD}[4/10] 选择摄影流派:{Colors.ENDC}\n")
    genres = module_lib.get("photography_genres", {})
    genre_list = []
    for i, (code, data) in enumerate(genres.items(), 1):
        name = GENRE_NAMES.get(code, code)
        genre_list.append(code)
        # 获取关键特征
        features = data.get("key_features", [])
        feature_preview = features[0] if features else "专业摄影"
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} - {feature_preview}")

    genre_choice = input(f"\n请选择 (1-{len(genre_list)}) 或按Enter跳过: ").strip()
    if genre_choice.isdigit() and 1 <= int(genre_choice) <= len(genre_list):
        selections['genre'] = genre_list[int(genre_choice) - 1]
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
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}] - {mood}")

    eye_choice = input(f"\n请选择 (1-{len(eye_list)}) 或按Enter跳过: ").strip()
    if eye_choice.isdigit() and 1 <= int(eye_choice) <= len(eye_list):
        selections['eye_type'] = eye_list[int(eye_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {eye_types[selections['eye_type']]['chinese_name']}{Colors.ENDC}")

    # 第6步：选择脸型
    print(f"\n{Colors.BOLD}[6/10] 选择脸型:{Colors.ENDC}\n")
    face_shapes = facial_lib.get("face_shapes", {})
    face_list = []
    for i, (code, data) in enumerate(face_shapes.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        face_list.append(code)
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    face_choice = input(f"\n请选择 (1-{len(face_list)}) 或按Enter跳过: ").strip()
    if face_choice.isdigit() and 1 <= int(face_choice) <= len(face_list):
        selections['face_shape'] = face_list[int(face_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {face_shapes[selections['face_shape']]['chinese_name']}{Colors.ENDC}")

    # 第7步：选择唇型
    print(f"\n{Colors.BOLD}[7/10] 选择唇型:{Colors.ENDC}\n")
    lip_types = facial_lib.get("lip_types", {})
    lip_list = []
    for i, (code, data) in enumerate(lip_types.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        lip_list.append(code)
        styles = ", ".join(data.get("suitable_styles", [])[:2])
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}] - {styles}")

    lip_choice = input(f"\n请选择 (1-{len(lip_list)}) 或按Enter跳过: ").strip()
    if lip_choice.isdigit() and 1 <= int(lip_choice) <= len(lip_list):
        selections['lip_type'] = lip_list[int(lip_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {lip_types[selections['lip_type']]['chinese_name']}{Colors.ENDC}")

    # 第8步：选择鼻型
    print(f"\n{Colors.BOLD}[8/10] 选择鼻型:{Colors.ENDC}\n")
    nose_types = facial_lib.get("nose_types", {})
    nose_list = []
    for i, (code, data) in enumerate(nose_types.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        nose_list.append(code)
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    nose_choice = input(f"\n请选择 (1-{len(nose_list)}) 或按Enter跳过: ").strip()
    if nose_choice.isdigit() and 1 <= int(nose_choice) <= len(nose_list):
        selections['nose_type'] = nose_list[int(nose_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {nose_types[selections['nose_type']]['chinese_name']}{Colors.ENDC}")

    # 第9步：选择皮肤质感
    print(f"\n{Colors.BOLD}[9/10] 选择皮肤质感:{Colors.ENDC}\n")
    skin_textures = facial_lib.get("skin_textures", {})
    skin_list = []
    for i, (code, data) in enumerate(skin_textures.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        skin_list.append(code)
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}]")

    skin_choice = input(f"\n请选择 (1-{len(skin_list)}) 或按Enter跳过: ").strip()
    if skin_choice.isdigit() and 1 <= int(skin_choice) <= len(skin_list):
        selections['skin_texture'] = skin_list[int(skin_choice) - 1]
        print(f"{Colors.GREEN}✓ 已选择: {skin_textures[selections['skin_texture']]['chinese_name']}{Colors.ENDC}")

    # 第10步：选择表情
    print(f"\n{Colors.BOLD}[10/10] 选择表情:{Colors.ENDC}\n")
    expressions = facial_lib.get("expressions", {})
    expr_list = []
    for i, (code, data) in enumerate(expressions.items(), 1):
        name = data.get("chinese_name", code)
        score = data.get("reusability_score", 0)
        expr_list.append(code)
        tone = data.get("emotional_tone", "")
        print(f"  {i}. {Colors.CYAN}{name}{Colors.ENDC} [{Colors.GREEN}{score}/10{Colors.ENDC}] - {tone}")

    expr_choice = input(f"\n请选择 (1-{len(expr_list)}) 或按Enter跳过: ").strip()
    if expr_choice.isdigit() and 1 <= int(expr_choice) <= len(expr_list):
        selections['expression'] = expr_list[int(expr_choice) - 1]
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
            subject_parts.append(ethnicity_keywords[0])  # 使用第一个关键词 (如 "East Asian")

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

    # 第二部分：收集所有选中模块的关键词
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

    # 添加关键词
    if all_keywords:
        prompt_parts.append(", ".join(all_keywords))

    # 添加流派技术参数
    if 'genre' in selections:
        genre_data = genres[selections['genre']]
        prompts_using = genre_data.get("prompts", [])

        # 获取设备
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

        # 流派特有关键词
        if selections['genre'] == "cinematic_narrative":
            prompt_parts.append("8K HDR, cinematic lighting, photorealistic, ultra-detailed")
        elif selections['genre'] == "analog_film":
            prompt_parts.append("analog film photography, warm tones, fine grain, nostalgic aesthetic")
        elif selections['genre'] == "portrait_beauty":
            prompt_parts.append("professional portrait photography, soft lighting, high-end retouching")
        elif selections['genre'] == "digital_commercial":
            prompt_parts.append("commercial photography, studio lighting, 4K ultra-detailed")

    final_prompt = ", ".join(prompt_parts)

    print(f"\n{Colors.BOLD}✨ 最终提示词:{Colors.ENDC}\n")
    print(f"{Colors.GREEN}{final_prompt}{Colors.ENDC}\n")
    print("=" * 80)

    # 显示选择摘要
    print(f"\n{Colors.BOLD}📋 选择摘要:{Colors.ENDC}\n")
    if 'gender' in selections:
        print(f"  性别: {genders[selections['gender']]['chinese_name']}")
    if 'age_range' in selections:
        print(f"  年龄: {age_ranges[selections['age_range']]['chinese_name']}")
    if 'ethnicity' in selections:
        print(f"  人种: {ethnicities[selections['ethnicity']]['chinese_name']}")
    if 'genre' in selections:
        print(f"  流派: {GENRE_NAMES.get(selections['genre'])}")
    if 'eye_type' in selections:
        print(f"  眼型: {eye_types[selections['eye_type']]['chinese_name']}")
    if 'face_shape' in selections:
        print(f"  脸型: {face_shapes[selections['face_shape']]['chinese_name']}")
    if 'lip_type' in selections:
        print(f"  唇型: {lip_types[selections['lip_type']]['chinese_name']}")
    if 'nose_type' in selections:
        print(f"  鼻型: {nose_types[selections['nose_type']]['chinese_name']}")
    if 'skin_texture' in selections:
        print(f"  皮肤: {skin_textures[selections['skin_texture']]['chinese_name']}")
    if 'expression' in selections:
        print(f"  表情: {expressions[selections['expression']]['chinese_name']}")

    print()

def build_prompt_from_description(description: str):
    """根据用户描述智能组装提示词"""
    facial_lib = load_json(FACIAL_FEATURES)
    module_lib = load_json(MODULE_LIBRARY)

    print(f"\n{Colors.HEADER}{Colors.BOLD}🔧 智能提示词组装{Colors.ENDC}\n")
    print(f"用户描述: {Colors.CYAN}{description}{Colors.ENDC}\n")

    # 关键词映射
    keywords_mapping = {
        # 流派关键词
        "电影": "cinematic_narrative",
        "电影级": "cinematic_narrative",
        "cinematic": "cinematic_narrative",
        "胶片": "analog_film",
        "人像": "portrait_beauty",
        "商业": "digital_commercial",
        "产品": "studio_product",

        # 风格关键词
        "美少女": "清纯少女",
        "少女": "清纯少女",
        "清纯": "清纯少女",
        "性感": "性感挑逗",
        "优雅": "古典优雅",
        "古典": "古典优雅",
        "cosplay": "真人化Cosplay",
        "真人化": "真人化Cosplay",
    }

    # 1. 识别流派
    detected_genre = None
    for keyword, genre in keywords_mapping.items():
        if keyword in description.lower():
            if genre in module_lib.get("photography_genres", {}):
                detected_genre = genre
                break

    # 2. 识别风格
    detected_style = None
    for keyword, style in keywords_mapping.items():
        if keyword in description.lower():
            usage_index = facial_lib.get("usage_index", {})
            if style in usage_index.get("by_style_mood", {}):
                detected_style = style
                break

    if not detected_genre and not detected_style:
        print(f"{Colors.YELLOW}⚠️  无法识别流派或风格，请尝试包含关键词：{Colors.ENDC}")
        print(f"  流派: 电影级/胶片/人像/商业/产品")
        print(f"  风格: 美少女/清纯/性感/优雅/古典/Cosplay\n")
        return

    print(f"{Colors.GREEN}✓ 识别成功:{Colors.ENDC}")
    if detected_genre:
        genre_info = module_lib["photography_genres"][detected_genre]
        print(f"  流派: {Colors.CYAN}{GENRE_NAMES.get(detected_genre, detected_genre)}{Colors.ENDC}")
    if detected_style:
        print(f"  风格: {Colors.CYAN}{detected_style}{Colors.ENDC}")
    print()

    # 3. 获取五官组合
    combo_keywords = []
    if detected_style:
        usage_index = facial_lib.get("usage_index", {})
        combo = usage_index.get("by_style_mood", {}).get(detected_style, {})

        print(f"{Colors.BOLD}📦 五官模块组合:{Colors.ENDC}\n")

        feature_types = {
            "gender": ("gender", "性别"),
            "age_range": ("age_range", "年龄"),
            "ethnicity": ("ethnicity", "人种"),
            "eyes": ("eye_types", "眼型"),
            "face": ("face_shapes", "脸型"),
            "lips": ("lip_types", "唇型"),
            "nose": ("nose_types", "鼻型"),
            "skin": ("skin_textures", "皮肤质感"),
            "expression": ("expressions", "表情")
        }

        for key, (cat_key, cat_name) in feature_types.items():
            if key in combo:
                code = combo[key]
                feature = facial_lib.get(cat_key, {}).get(code, {})
                chinese_name = feature.get("chinese_name", code)
                keywords = feature.get("keywords", [])

                print(f"  {cat_name}: {Colors.CYAN}{chinese_name}{Colors.ENDC}")
                if key not in ["gender", "age_range", "ethnicity"]:  # 这三个字段单独处理
                    combo_keywords.extend(keywords)

    # 4. 获取技术参数
    tech_params = []
    if detected_genre:
        genre_info = module_lib["photography_genres"][detected_genre]
        prompts_using = genre_info.get("prompts", [])

        # 获取该流派常用设备
        equipment_index = module_lib.get("camera_equipment_index", {})
        for eq_name, eq_data in equipment_index.items():
            if any(pid in eq_data.get("prompts", []) for pid in prompts_using):
                camera = eq_data.get("specs", {}).get("camera_model", eq_name)
                lens = eq_data.get("specs", {}).get("lens_example", "")
                tech_params.append(f"{camera}")
                if lens:
                    tech_params.append(f"{lens}")
                break

    # 5. 组装完整提示词
    print(f"\n{Colors.BOLD}✨ 组装后的提示词:{Colors.ENDC}\n")
    print("=" * 80)

    prompt_parts = []

    # 主体描述 - 从风格组合中提取性别、年龄、人种
    subject_parts = []

    if detected_style:
        usage_index = facial_lib.get("usage_index", {})
        combo = usage_index.get("by_style_mood", {}).get(detected_style, {})

        # 添加形容词
        gender_code = combo.get("gender", "female")
        if gender_code == "female":
            subject_parts.append("A beautiful")
        else:
            subject_parts.append("A handsome")

        # 添加人种（在年龄之前）
        ethnicity_code = combo.get("ethnicity", "east_asian")
        ethnicity_data = facial_lib.get("ethnicity", {}).get(ethnicity_code, {})
        ethnicity_keywords = ethnicity_data.get("keywords", [])
        if ethnicity_keywords:
            subject_parts.append(ethnicity_keywords[0])

        # 添加性别词（包含年龄信息）
        age_code = combo.get("age_range", "young_adult")
        gender_data = facial_lib.get("gender", {}).get(gender_code, {})
        age_based_terms = gender_data.get("usage_recommendations", {}).get("age_based_terms", {})
        if age_code in age_based_terms:
            # 使用年龄特定的性别词（如 "young woman"）
            subject_parts.append(age_based_terms[age_code])
        else:
            gender_keywords = gender_data.get("keywords", [])
            if gender_keywords:
                subject_parts.append(gender_keywords[0])

        prompt_parts.append(" ".join(subject_parts))
    else:
        # 后备方案
        if detected_style == "清纯少女" or "美少女" in description:
            prompt_parts.append("A beautiful young East Asian woman")
        elif detected_style == "性感挑逗":
            prompt_parts.append("A beautiful young East Asian woman")
        elif detected_style == "古典优雅":
            prompt_parts.append("A beautiful young East Asian woman")
        elif detected_style == "真人化Cosplay":
            prompt_parts.append("A beautiful young East Asian woman")
        else:
            prompt_parts.append("A beautiful young woman")

    # 五官关键词
    if combo_keywords:
        prompt_parts.append(", ".join(combo_keywords[:10]))

    # 技术参数
    if tech_params:
        prompt_parts.append(f"photographed with {', '.join(tech_params)}")

    if detected_genre == "cinematic_narrative":
        prompt_parts.append("8K HDR, cinematic lighting, photorealistic, ultra-detailed")
    elif detected_genre == "analog_film":
        prompt_parts.append("analog film photography, warm tones, fine grain")
    elif detected_genre == "portrait_beauty":
        prompt_parts.append("professional portrait photography, soft lighting")

    final_prompt = ", ".join(prompt_parts)

    print(f"{Colors.GREEN}{final_prompt}{Colors.ENDC}")
    print("=" * 80)

    # 6. 显示参考Prompt
    if detected_genre:
        genre_info = module_lib["photography_genres"][detected_genre]
        ref_prompts = genre_info.get("prompts", [])
        if ref_prompts:
            print(f"\n{Colors.BOLD}📚 参考Prompts:{Colors.ENDC}")
            for pid in ref_prompts[:2]:
                print(f"  可查看详情: {Colors.CYAN}python3 prompt_tool.py show {pid}{Colors.ENDC}")

    print()

def main():
    parser = argparse.ArgumentParser(
        description="Prompt Extraction Tool - CLI交互工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 命令
    subparsers.add_parser("list", help="列出所有提示词")

    # show 命令
    show_parser = subparsers.add_parser("show", help="查看提示词详细信息")
    show_parser.add_argument("id", type=int, help="提示词ID")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索提示词")
    search_group = search_parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument("--genre", help="按流派搜索")
    search_group.add_argument("--equipment", help="按设备搜索")

    # recommend 命令
    recommend_parser = subparsers.add_parser("recommend", help="获取推荐")
    recommend_parser.add_argument("id", type=int, help="提示词ID")
    recommend_parser.add_argument("-n", "--number", type=int, default=3, help="推荐数量 (默认3)")

    # compare 命令
    compare_parser = subparsers.add_parser("compare", help="对比两个提示词")
    compare_parser.add_argument("id1", type=int, help="第一个提示词ID")
    compare_parser.add_argument("id2", type=int, help="第二个提示词ID")

    # facial 命令 - 五官特征查询
    facial_parser = subparsers.add_parser("facial", help="五官特征查询")
    facial_group = facial_parser.add_mutually_exclusive_group(required=True)
    facial_group.add_argument("--list-types", action="store_true", help="列出所有五官类型")
    facial_group.add_argument("--eye-type", help="按眼型查询")
    facial_group.add_argument("--skin-texture", help="按皮肤质感查询")
    facial_group.add_argument("--expression", help="按表情查询")
    facial_group.add_argument("--style", help="按风格推荐五官组合")

    # build 命令 - 智能组装提示词
    build_parser = subparsers.add_parser("build", help="根据描述智能组装提示词")
    build_parser.add_argument("description", type=str, help="用自然语言描述你想要的图片，例如：'电影级的美少女'")

    # generate 命令 - 交互式生成器 ⭐核心功能
    subparsers.add_parser("generate", help="交互式问答生成提示词（推荐）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 执行命令
    if args.command == "list":
        list_all_prompts()
    elif args.command == "show":
        show_prompt_detail(args.id)
    elif args.command == "search":
        if args.genre:
            search_by_genre(args.genre)
        elif args.equipment:
            search_by_equipment(args.equipment)
    elif args.command == "recommend":
        recommend_prompts(args.id, args.number)
    elif args.command == "compare":
        compare_prompts(args.id1, args.id2)
    elif args.command == "facial":
        if args.list_types:
            facial_list_types()
        elif args.eye_type:
            facial_search_by_type("eye", args.eye_type)
        elif args.skin_texture:
            facial_search_by_type("skin", args.skin_texture)
        elif args.expression:
            facial_search_by_type("expression", args.expression)
        elif args.style:
            facial_recommend_by_style(args.style)
    elif args.command == "build":
        build_prompt_from_description(args.description)
    elif args.command == "generate":
        interactive_build()

if __name__ == "__main__":
    main()
