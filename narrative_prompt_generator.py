#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
叙述性提示词生成器
基于黄金模板，将数据库元素填充到专业框架中
"""

import sqlite3
from typing import Dict, Optional


class NarrativePromptGenerator:
    """使用黄金模板生成高质量叙述性提示词"""

    def __init__(self, db_path: str = "extracted_results/elements.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_element(self, domain: str, category: str) -> Optional[str]:
        """获取单个元素的template"""
        query = """
            SELECT ai_prompt_template
            FROM elements
            WHERE domain_id = ? AND category_id = ?
            ORDER BY reusability_score DESC
            LIMIT 1
        """
        self.cursor.execute(query, (domain, category))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def generate_westworld_split_face(self,
                                     gender: str = "woman",
                                     hair_color: str = "chestnut brown",
                                     hair_style: str = "flowing",
                                     eye_color: str = "brown",
                                     led_color: str = "blue") -> str:
        """
        生成西部世界风格split-face提示词

        参数：
            gender: "woman" 或 "man"
            hair_color: 发色描述
            hair_style: 发型描述
            eye_color: 眼睛颜色
            led_color: LED颜色
        """

        # 黄金模板框架
        template = f"""Cinematic ultra-realistic split-face portrait inspired by Westworld HBO series, showing dramatic half-human half-android host transformation, vertical center line dividing face into two contrasting halves revealing the nature of artificial consciousness.

LEFT HALF - HUMAN SIDE: Photorealistic human face showing beautiful {gender} with flawless natural skin, visible pores and skin texture, warm flesh tones with subsurface scattering showing blood flow beneath surface, natural eye with deep {eye_color} iris showing intricate detail and emotional depth, pupil with natural reflection and catchlight, thick natural eyelashes, eyebrow with individual hair strands, full lips with natural pink color and moisture, cheek with subtle blush and natural contours, ear with realistic cartilage detail, {hair_style} {hair_color} hair with individual strands moving naturally, human side showing warmth, life, and consciousness, subtle facial expression suggesting awareness and emotion.

RIGHT HALF - ANDROID SIDE: Exposed mechanical interior revealing sophisticated robotics, white synthetic polymer facial framework with smooth matte finish, visible complex servo mechanisms and articulated joints at jaw and cheekbone showing precision engineering, exposed artificial eye socket containing advanced camera lens system with {led_color} LED ring light and focusing mechanisms, optical sensors and circuitry visible, metallic skeletal structure showing titanium alloy cheekbone and jaw assembly, bundled fiber optic cables in white, {led_color}, and silver running along neck and skull showing neural pathways, micro hydraulic pistons for facial muscle simulation, circuit boards with visible components and tiny indicator lights, cooling vents with fine mesh, precision-machined parts showing engineering excellence, clean clinical aesthetic emphasizing advanced technology, no exposed wires chaos - organized sophisticated android anatomy, white and silver color palette with {led_color} LED accents.

PERFECT VERTICAL SPLIT: Razor-sharp division line running precisely down center of face from forehead through nose bridge to chin and neck, clean surgical cut revealing cross-section view, left side completely human with no mechanical elements visible, right side completely mechanical with synthetic materials and robotics fully exposed, transition line perfectly straight creating dramatic contrast between organic life and artificial construction, slight shadow in division crack adding depth, no gradual transition - absolute binary split emphasizing the philosophical question of consciousness.

FACIAL EXPRESSION: Human left side showing subtle emotion with slight smile and warm eye suggesting consciousness and feeling, android right side maintaining perfect symmetry in mechanical movement but lacking warmth, both sides coordinated in same expression showing the host's ability to perfectly mimic human behavior, raising questions about authenticity of emotion in artificial beings, Westworld's central theme of "what makes us human" visualized through this stark contrast.

CINEMATIC LIGHTING: Dramatic three-point lighting setup with key light from left front creating soft illumination on human side showing skin warmth, fill light from right illuminating mechanical side revealing engineering details with metallic sheen, strong rim backlight creating edge glow separating subject from background, subtle {led_color} accent light on android side emphasizing technological coldness contrasting with warm human side, high contrast dramatic lighting emphasizing duality, volumetric haze in background adding cinematic atmosphere.

BACKGROUND: Dark gradient backdrop transitioning from dark grey to black, minimalist clean background emphasizing subject without distraction, subtle atmospheric fog or haze creating depth, professional studio photography setup, slight vignetting directing focus to face.

TECHNICAL SPECIFICATIONS: Shot on ARRI Alexa Mini LF cinema camera with Cooke S7 100mm portrait lens at T2.8, shallow depth of field with face in razor-sharp focus and background smoothly transitioning to bokeh, 4K cinema resolution, RAW format preserving maximum detail and dynamic range, cinematic color grading with teal and orange color science creating visual interest while maintaining natural skin tones on human side and cool technological tones on android side.

WESTWORLD AESTHETIC: HBO's signature prestige television cinematography quality, philosophical sci-fi visual storytelling, Blade Runner-influenced lighting and mood, Ghost in the Shell thematic resonance, Ex Machina mechanical design sophistication, direct reference to Westworld's host reveal scenes showing the mechanical nature beneath human appearance, exploring themes of consciousness, free will, and the boundary between human and artificial intelligence.

Photography style: High-end editorial portrait meets medical/technical illustration precision, dramatic conceptual photography, museum-quality fine art print suitable for science fiction exhibition, celebrating intersection of humanity and technology, thought-provoking visual metaphor.

Ultra-detailed, photorealistic rendering with practical effects aesthetic, hyper-realistic human skin texture on left side, precision-engineered mechanical components on right side, masterpiece quality, (photorealistic human skin:1.4), (mechanical detail precision:1.3), (dramatic split composition:1.3), cinematic atmosphere, professional studio portrait photography"""

        return template

    def generate_from_database_with_template(self,
                                            theme: str = "westworld_split_face",
                                            **custom_params) -> Dict:
        """
        从数据库获取元素，填充到叙述性模板中

        参数:
            theme: 主题类型 ("westworld_split_face", "cinematic_portrait"等)
            **custom_params: 自定义参数覆盖
        """

        # 从数据库获取基础元素
        gender_elem = self.get_element('portrait', 'gender')

        # 设置默认参数
        params = {
            'gender': 'woman' if 'female' in (gender_elem or '') else 'man',
            'hair_color': 'chestnut brown',
            'hair_style': 'flowing',
            'eye_color': 'brown',
            'led_color': 'blue'
        }

        # 应用自定义参数
        params.update(custom_params)

        if theme == "westworld_split_face":
            prompt = self.generate_westworld_split_face(**params)
        else:
            raise ValueError(f"Unknown theme: {theme}")

        return {
            'theme': theme,
            'prompt': prompt,
            'params': params,
            'template_used': 'golden_westworld_v1'
        }

    def close(self):
        self.conn.close()


def main():
    """测试生成器"""
    gen = NarrativePromptGenerator()

    print("="*80)
    print("测试1: 默认女性版本")
    print("="*80)

    result1 = gen.generate_from_database_with_template(
        theme="westworld_split_face"
    )

    print(result1['prompt'])
    print(f"\n使用参数: {result1['params']}")

    print("\n" + "="*80)
    print("测试2: 自定义男性版本")
    print("="*80)

    result2 = gen.generate_from_database_with_template(
        theme="westworld_split_face",
        gender="man",
        hair_color="jet black",
        hair_style="short",
        eye_color="grey",
        led_color="green"
    )

    print(result2['prompt'])
    print(f"\n使用参数: {result2['params']}")

    print("\n" + "="*80)
    print("测试3: 金发女性版本")
    print("="*80)

    result3 = gen.generate_from_database_with_template(
        theme="westworld_split_face",
        gender="woman",
        hair_color="platinum blonde",
        hair_style="long flowing",
        eye_color="blue",
        led_color="cyan"
    )

    print(result3['prompt'])
    print(f"\n使用参数: {result3['params']}")

    gen.close()

    print("\n" + "="*80)
    print("✅ 叙述性提示词生成成功！")
    print("="*80)


if __name__ == "__main__":
    main()
