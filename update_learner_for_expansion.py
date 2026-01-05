#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新学习器 - 支持新扩展的类别
为 learner.py 添加对 poses, expressions, clothing_styles 的识别能力
"""

import os
import shutil
from datetime import datetime

def update_learner():
    """更新learner.py以支持新类别"""

    learner_path = "learner.py"

    print("="*70)
    print("  🔄 更新学习器 - 添加新类别支持")
    print("="*70 + "\n")

    # 备份原文件
    backup_path = f"learner_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy2(learner_path, backup_path)
    print(f"📦 备份已创建: {backup_path}\n")

    # 读取现有文件
    with open(learner_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经更新过
    if '_analyze_poses' in content:
        print("⚠️  学习器似乎已经包含新类别支持")
        print("   如需重新更新，请先删除或修改现有代码\n")
        return

    print("🔍 添加新的正则表达式模式...\n")

    # 在RuleBasedLearner的patterns字典中添加新模式
    new_patterns = '''
            "poses": {
                "keywords": ["pose", "posture", "stance", "position", "standing", "arms"],
                "attributes": {
                    "stance": ["power stance", "wide stance", "relaxed", "casual"],
                    "arms": ["crossed", "arms crossed", "over chest"],
                    "head": ["chin raised", "chin up", "head tilt", "tilted"]
                },
                "regex": r"(power\\s+stance|wide\\s+stance|arms\\s+crossed|crossed\\s+arms|chin\\s+raised|head\\s+tilt|relaxed\\s+standing)"
            },
            "expressions": {
                "keywords": ["expression", "smile", "smirk", "look", "gaze", "mood"],
                "attributes": {
                    "type": ["smirk", "smile", "grin", "serene", "calm", "playful"],
                    "mood": ["confident", "sassy", "gentle", "warm", "peaceful"]
                },
                "regex": r"(confident\\s+smirk|playful\\s+smile|gentle\\s+smile|serene|calm\\s+expression|sassy)"
            },
            "clothing_styles": {
                "keywords": ["wearing", "dressed in", "outfit", "attire", "clothing"],
                "attributes": {
                    "style": ["casual", "formal", "elegant", "traditional", "sporty", "athletic"],
                    "type": ["modern", "contemporary", "cultural", "activewear"]
                },
                "regex": r"wearing\\s+(casual|formal|elegant|traditional|sporty|athletic|modern)\\s+(outfit|attire|clothing|wear)"
            }'''

    # 找到patterns字典的结束位置（在pose之后）
    pose_pattern_end = content.find('            "pose": {')
    if pose_pattern_end != -1:
        # 找到pose模式的结束
        next_closing = content.find('            }', pose_pattern_end)
        insertion_point = content.find('\n', next_closing) + 1

        # 插入新模式
        updated_content = content[:insertion_point] + ',' + new_patterns + '\n' + content[insertion_point:]

        print("✅ 已添加正则表达式模式")
        print("   - poses: 姿势识别")
        print("   - expressions: 表情识别")
        print("   - clothing_styles: 服装风格识别\n")
    else:
        print("❌ 未找到插入点，请手动添加模式")
        updated_content = content

    # 添加新的分析方法到AIAssistedLearner类
    print("🔍 添加AI辅助分析方法...\n")

    new_methods = '''
    def _analyze_poses(self, text: str) -> List[Dict]:
        """智能分析姿势"""
        features = []

        poses = {
            'power_stance': ['power stance', 'wide stance', 'feet apart', 'confident pose'],
            'arms_crossed': ['arms crossed', 'crossed arms', 'arms over chest'],
            'chin_raised': ['chin raised', 'chin up', 'head tilted up'],
            'relaxed_standing': ['relaxed', 'casual stance', 'natural pose']
        }

        import re
        for pose, patterns in poses.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 提取完整描述
                    match = re.search(r'\\b[\\w\\s]{0,30}' + re.escape(pattern) + r'[\\w\\s]{0,20}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'poses',
                            'raw_text': raw_text,
                            'confidence': 0.9,
                            'method': 'ai-assisted'
                        })
                    break

        return features

    def _analyze_expressions(self, text: str) -> List[Dict]:
        """智能分析表情"""
        features = []

        expressions = {
            'confident_smirk': ['smirk', 'confident', 'sassy', 'smug'],
            'playful_smile': ['playful', 'fun', 'lighthearted', 'cheeky'],
            'serene_calm': ['serene', 'calm', 'peaceful', 'tranquil'],
            'gentle_smile': ['gentle', 'soft smile', 'warm', 'kind']
        }

        import re
        for expr, patterns in expressions.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 提取包含表情的完整描述
                    match = re.search(r'\\b[\\w\\s]{0,30}' + re.escape(pattern) + r'[\\w\\s]{0,20}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'expressions',
                            'raw_text': raw_text,
                            'confidence': 0.9,
                            'method': 'ai-assisted'
                        })
                    break

        return features

    def _analyze_clothing_detailed(self, text: str) -> List[Dict]:
        """智能分析服装风格（详细版）"""
        features = []

        clothing_styles = {
            'casual_modern': ['casual', 'modern outfit', 'everyday wear'],
            'elegant_formal': ['elegant', 'formal', 'sophisticated'],
            'traditional_cultural': ['traditional', 'cultural attire', 'ethnic'],
            'sporty_athletic': ['sporty', 'athletic', 'activewear']
        }

        import re
        for style, patterns in clothing_styles.items():
            for pattern in patterns:
                if pattern in text.lower():
                    # 寻找完整的服装描述
                    match = re.search(r'wearing\\s+[\\w\\s]{0,50}' + re.escape(pattern) + r'[\\w\\s]{0,30}', text.lower())
                    if match:
                        raw_text = match.group(0).strip()
                        features.append({
                            'category': 'clothing_styles',
                            'raw_text': raw_text,
                            'confidence': 0.85,
                            'method': 'ai-assisted'
                        })
                    break

        return features
'''

    # 找到_analyze_accessories方法的结束位置
    accessories_end = updated_content.find('    def _analyze_accessories(self, text: str) -> List[Dict]:')
    if accessories_end != -1:
        # 找到这个方法的结束（下一个方法或类的结束）
        next_method = updated_content.find('\n\nclass ', accessories_end)
        if next_method == -1:
            next_method = updated_content.find('\n\n\nclass ', accessories_end)

        if next_method != -1:
            # 在_analyze_accessories之后插入新方法
            updated_content = updated_content[:next_method] + '\n' + new_methods + updated_content[next_method:]

            print("✅ 已添加AI分析方法")
            print("   - _analyze_poses(): 姿势分析")
            print("   - _analyze_expressions(): 表情分析")
            print("   - _analyze_clothing_detailed(): 服装详细分析\n")
        else:
            print("⚠️  未找到插入点，请手动添加方法")
    else:
        print("⚠️  未找到_analyze_accessories方法")

    # 更新extract_features方法，调用新的分析方法
    print("🔍 更新extract_features方法...\n")

    # 找到AIAssistedLearner的extract_features方法
    extract_features_start = updated_content.find('    def extract_features(self, prompt_text: str) -> List[Dict]:',
                                                   updated_content.find('class AIAssistedLearner'))

    if extract_features_start != -1:
        # 在return detected之前添加新的分析调用
        return_detected = updated_content.find('        return detected', extract_features_start)

        if return_detected != -1:
            new_calls = '''
        # 姿势分析
        if any(word in prompt_text.lower() for word in ['pose', 'stance', 'standing', 'arms', 'chin']):
            pose_features = self._analyze_poses(prompt_text)
            detected.extend(pose_features)

        # 表情分析
        if any(word in prompt_text.lower() for word in ['expression', 'smile', 'smirk', 'look', 'mood']):
            expression_features = self._analyze_expressions(prompt_text)
            detected.extend(expression_features)

        # 服装风格分析（详细版）
        if any(word in prompt_text.lower() for word in ['casual', 'formal', 'traditional', 'sporty']):
            clothing_style_features = self._analyze_clothing_detailed(prompt_text)
            detected.extend(clothing_style_features)

'''
            updated_content = updated_content[:return_detected] + new_calls + '\n        ' + updated_content[return_detected:]

            print("✅ 已更新extract_features方法")
            print("   现在会自动调用新的分析方法\n")
        else:
            print("⚠️  未找到return detected语句")
    else:
        print("⚠️  未找到extract_features方法")

    # 保存更新后的文件
    with open(learner_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("="*70)
    print("  ✅ 学习器更新完成！")
    print("="*70)
    print("\n📝 更新摘要:")
    print("   ✅ 添加了3组新的正则表达式模式")
    print("   ✅ 添加了3个新的AI分析方法")
    print("   ✅ 更新了extract_features方法")
    print(f"\n📦 备份文件: {backup_path}")
    print("\n💡 下一步:")
    print("   1. 运行 python3 update_reviewer_for_expansion.py 更新审核器")
    print("   2. 测试: python3 test_scan_new_prompt.py")
    print("   3. 开始使用: python3 auto_learn_workflow.py scan \"your prompt\"\n")


if __name__ == "__main__":
    update_learner()
