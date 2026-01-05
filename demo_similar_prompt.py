#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""演示生成类似风格的Prompt"""

import sys
sys.path.append('.')

from prompt_tool import PromptGenerator
import json

print("="*70)
print("  🎨 演示：用现有库生成类似风格的Prompt")
print("="*70)

gen = PromptGenerator()

# 生成一个带节日妆容的人像
print("\n📸 场景1: 节日人像（类似风格）\n")

# 手动指定一些约束来模拟圣诞主题
constraints = {
    'makeup_style': 'glamour_makeup',  # 魅力妆容
    'hair_style': 'long_straight',     # 长直发
    'hair_color': 'black_hair',        # 黑发
    'skin_tone': 'fair_skin'           # 白皙肤色
}

prompt1 = gen.generate_with_constraints(
    language='en',
    constraints=constraints,
    include_modules=['photography', 'lighting']
)

print("生成的Prompt:")
print("-" * 70)
print(prompt1)

# 中文版本
print("\n" + "="*70)
print("📸 场景2: 同样配置的中文版本\n")

prompt2 = gen.generate_with_constraints(
    language='zh',
    constraints=constraints,
    include_modules=['photography', 'lighting']
)

print("生成的Prompt:")
print("-" * 70)
print(prompt2)

# 随机生成几个不同风格的
print("\n" + "="*70)
print("📸 场景3: 随机生成3个不同风格的人像\n")

for i in range(3):
    print(f"\n--- 随机人像 {i+1} ---")
    random_prompt = gen.generate_random_portrait(language='en')
    print(random_prompt[:200] + "...")

print("\n" + "="*70)
print("  ✅ 演示完成")
print("="*70)
print("\n💡 提示：")
print("   当前库专注于人像特征（五官、发型、妆容等）")
print("   如果需要场景、姿势、服装等，可以：")
print("   1. 使用扫描系统学习这些新特征")
print("   2. 扩展库到新的类别（poses, expressions, clothing_details）")
print("   3. 手动添加场景和摄影模块\n")
