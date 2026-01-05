#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT转JSON转换器 - 将结构化TXT提示词转换为JSON格式
"""

import re
from pathlib import Path
from typing import Dict


class TxtToJsonConverter:
    """TXT提示词转换器"""

    def convert_txt_to_prompt_data(self, txt_content: str, file_name: str) -> Dict:
        """
        将TXT内容转换为Prompt数据结构

        Args:
            txt_content: TXT文件内容
            file_name: 文件名（用作prompt_id）

        Returns:
            标准的prompt_data字典
        """
        # 提取prompt_id
        match = re.search(r'(\d+)_', file_name)
        prompt_id = int(match.group(1)) if match else hash(file_name) % 10000

        # 提取主题（支持多种格式）
        theme = file_name  # 默认值

        # 尝试从内容提取
        patterns = [
            r'【案例\s*\d+[：:]\s*(.+?)】',  # 标准格式
            r'案例\s*\d+[：:]\s*(.+?)\n',    # 无括号格式
            r'\*\*(.+?)\*\*',                 # 粗体标题
        ]
        for pattern in patterns:
            match = re.search(pattern, txt_content)
            if match:
                theme = match.group(1).strip()
                break

        # 最后尝试从文件名提取
        if theme == file_name:
            name_match = re.search(r'\d+_案例\s*\d+_(.+?)\.txt', file_name)
            if name_match:
                theme = name_match.group(1)

        # 构建modules（从文本中智能提取）
        modules = self._extract_modules(txt_content)

        # 构建标准数据结构
        prompt_data = {
            'prompt_id': prompt_id,
            'original_prompt': txt_content,
            'prompt_length': len(txt_content),
            'theme': theme,
            'modules': modules,
            'quality_score': {
                'clarity': self._estimate_clarity(txt_content),
                'detail_richness': self._estimate_detail_richness(txt_content),
                'reusability': self._estimate_reusability(modules)
            }
        }

        return prompt_data

    def _extract_modules(self, text: str) -> Dict:
        """从文本中提取modules结构"""
        modules = {}

        # 提取主题/主体
        subject_patterns = [
            r'【案例.*?】\s*=+\s*\n\n(.+?)(?:\n\n|【)',  # 标准格式
            r'=+\s*\n\n(.+?)(?:\n\n|\Z)',             # 简化格式
        ]
        for pattern in subject_patterns:
            subject_match = re.search(pattern, text, re.DOTALL)
            if subject_match and len(subject_match.group(1).strip()) > 10:
                modules['subject_variables'] = {
                    'main': subject_match.group(1).strip()[:500]  # 限制长度
                }
                break

        # 提取布局/结构信息
        layout_patterns = [
            r'【布局结构】(.+?)(?:\n\n|模块\d)',
            r'布局[：:]\s*(.+?)(?:\n|。)',
            r'网格[：:]\s*(.+?)(?:\n|。)'
        ]
        for pattern in layout_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                if 'composition' not in modules:
                    modules['composition'] = {}
                modules['composition']['layout'] = match.group(1).strip()[:200]
                break

        # 提取材质信息
        materials = []
        material_patterns = [
            r'材质[：:](.+?)(?:\n|。)',
            r'玻璃|亚克力|木质|金属|布料|皮革|陶瓷'
        ]
        for pattern in material_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                materials.extend([m.strip() for m in matches if len(m.strip()) > 2])

        if materials:
            modules['material_textures'] = list(set(materials[:10]))

        # 提取颜色信息
        color_match = re.search(r'(颜色|色彩|配色)[：:](.+?)(?:\n|。)', text)
        if color_match:
            modules['color_scheme'] = {
                'tone': color_match.group(2).strip()[:100]
            }

        # 提取光照信息
        lighting_keywords = ['光照', '光线', '灯光', 'lighting', '柔光', '自然光', '环境光']
        lighting = []
        for keyword in lighting_keywords:
            matches = re.findall(f'{keyword}[：:]?(.{{0,50}}?)(?:\n|。|,)', text, re.IGNORECASE)
            if matches:
                lighting.extend([m.strip() for m in matches])

        if lighting:
            modules['lighting_techniques'] = list(set(lighting[:5]))

        # 提取风格信息
        style_patterns = [
            r'风格[：:](.+?)(?:\n|。)',
            r'美学[：:](.+?)(?:\n|。)',
            r'(极简|现代|古典|复古|科技|自然|工业)'
        ]
        for pattern in style_patterns:
            match = re.search(pattern, text)
            if match:
                if 'visual_style' not in modules:
                    modules['visual_style'] = {}
                modules['visual_style']['art_style'] = match.group(1 if '(' in pattern else 0).strip()[:100]
                break

        # 提取技术参数
        tech_params = {}
        if re.search(r'(\d+k|4K|8K|高清|高分辨率)', text, re.IGNORECASE):
            tech_params['resolution'] = re.search(r'(\d+k|4K|8K|高清)', text, re.IGNORECASE).group(0)

        camera_match = re.search(r'(相机|镜头|摄影)[：:]?(.{0,50})(?:\n|。)', text)
        if camera_match:
            tech_params['camera'] = camera_match.group(2).strip()[:100]

        if tech_params:
            modules['technical_parameters'] = tech_params

        # 提取关键词/标签
        keywords = []
        keyword_match = re.search(r'(关键词|标签|tags)[：:](.+?)(?:\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if keyword_match:
            keywords_text = keyword_match.group(2)
            keywords = [k.strip() for k in re.split(r'[,，/、\n]', keywords_text) if k.strip()]

        if keywords:
            modules['mood_keywords'] = keywords[:10]

        return modules

    def _estimate_clarity(self, text: str) -> int:
        """估计清晰度（1-10）"""
        score = 5
        if len(text) > 500:
            score += 2
        if '【' in text and '】' in text:
            score += 2
        if re.search(r'模块\d', text):
            score += 1
        return min(score, 10)

    def _estimate_detail_richness(self, text: str) -> int:
        """估计细节丰富度（1-10）"""
        score = 5
        if len(text) > 1000:
            score += 2
        if len(text) > 2000:
            score += 1
        module_count = len(re.findall(r'模块\d', text))
        score += min(module_count // 2, 2)
        return min(score, 10)

    def _estimate_reusability(self, modules: Dict) -> int:
        """估计可复用性（1-10）"""
        score = 5
        if 'material_textures' in modules:
            score += 1
        if 'lighting_techniques' in modules:
            score += 1
        if 'visual_style' in modules:
            score += 1
        if 'composition' in modules:
            score += 1
        if 'technical_parameters' in modules:
            score += 1
        return min(score, 10)


# 测试
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 txt_to_json_converter.py <txt_file>")
        sys.exit(1)

    converter = TxtToJsonConverter()

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        txt_content = f.read()

    prompt_data = converter.convert_txt_to_prompt_data(txt_content, Path(sys.argv[1]).name)

    import json
    print(json.dumps(prompt_data, ensure_ascii=False, indent=2))
