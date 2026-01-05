#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量学习器 V2 Enhanced - 使用AI学习的智能规则
基于从30个样本中学习的 enhanced_rules.json，实现智能分类和提取
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from element_db import ElementDB
from txt_to_json_converter import TxtToJsonConverter


class EnhancedRulesEngine:
    """智能规则引擎 - 基于AI学习的规则"""

    def __init__(self, rules_path: str = "/tmp/enhanced_rules.json"):
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)

        self.domain_rules = self.rules['domain_classification_rules']
        self.complexity_rules = self.rules['complexity_detection_rules']
        self.extraction_patterns = self.rules['extraction_patterns']
        self.quality_rules = self.rules['quality_assessment_rules']

    def classify_domain(self, prompt_data: Dict) -> Tuple[str, float, str]:
        """
        智能领域分类（使用语义规则）

        Returns:
            (primary_domain, confidence, reasoning)
        """
        original = prompt_data.get('original_prompt', '')
        theme = prompt_data.get('theme', '')
        mode = prompt_data.get('mode', 'generate')
        category = prompt_data.get('category', '')

        full_text = f"{theme} {original} {category}".lower()

        scores = {}

        for domain, rules in self.domain_rules.items():
            score = 0
            matches = []

            # 检查语义指标
            for indicator_group in rules['semantic_indicators']:
                if any(keyword in full_text for keyword in indicator_group.lower().split('、')):
                    score += 3
                    matches.append(indicator_group[:20])

            # 检查模式偏好
            if mode in rules.get('mode_preference', []):
                score += 1

            # 检查分类标签
            for tag in rules.get('category_tags', []):
                if tag in category or tag in theme:
                    score += 2
                    matches.append(f"tag:{tag}")

            if score > 0:
                scores[domain] = {
                    'score': score,
                    'matches': matches,
                    'threshold': rules.get('confidence_threshold', 0.7)
                }

        if not scores:
            return 'portrait', 0.3, 'fallback default'

        # 选择得分最高的领域
        top_domain = max(scores.items(), key=lambda x: x[1]['score'])
        domain_name = top_domain[0]
        domain_data = top_domain[1]

        # 计算置信度
        confidence = min(1.0, domain_data['score'] / 10.0)

        # 生成推理说明
        reasoning = f"matched: {', '.join(domain_data['matches'][:3])}"

        return domain_name, confidence, reasoning

    def calculate_complexity(self, prompt_data: Dict) -> Tuple[str, float]:
        """
        计算提示词复杂度

        Returns:
            (complexity_level, complexity_score)
        """
        original = prompt_data.get('original_prompt', '')
        modules = prompt_data.get('modules', {})

        score = self.complexity_rules['complexity_scoring']['base_score']

        # 长度加分
        length = len(original)
        length_bonus = (length / 100) * self.complexity_rules['complexity_scoring']['length_bonus']['per_100_chars']
        length_bonus = min(length_bonus, self.complexity_rules['complexity_scoring']['length_bonus']['max_bonus'])
        score += length_bonus

        # 结构加分
        structure_bonus = self.complexity_rules['complexity_scoring']['structure_bonus']
        if '{' in original or 'json' in original.lower():
            score += structure_bonus.get('has_json', 0)
        if '步骤' in original or '要求' in original or '：' in original:
            score += structure_bonus.get('has_steps', 0)
        if any(marker in original for marker in ['参数', '设置', '配置', '规格']):
            score += structure_bonus.get('has_parameters', 0)

        # 技术参数加分
        technical_bonus = self.complexity_rules['complexity_scoring']['technical_bonus']
        if any(cam in original for cam in ['索尼', '85mm', 'f/', '光圈', '快门']):
            score += technical_bonus.get('camera_params', 0)
        if any(light in original for light in ['三点式', '轮廓光', '体积光', '柔光', '硬光']):
            score += technical_bonus.get('lighting_details', 0)
        if any(engine in original for engine in ['c4d', 'Cinema 4D', '虚幻引擎', 'UE5']):
            score += technical_bonus.get('render_engine', 0)

        # 确定复杂度等级
        if score >= 8.0:
            level = 'complex'
        elif score >= 6.0:
            level = 'medium'
        else:
            level = 'simple'

        return level, round(score, 2)

    def should_use_skill(self, complexity_score: float, confidence: float,
                        prompt_data: Dict) -> Tuple[bool, str]:
        """
        判断是否应该使用Skill处理

        Returns:
            (should_use_skill, reason)
        """
        routing_rules = self.quality_rules['skill_routing_rules']
        original = prompt_data.get('original_prompt', '')

        # 必须使用Skill的情况
        if complexity_score >= 8.0:
            return True, f"high_complexity:{complexity_score}"
        if '{' in original and 'json' in original.lower():
            return True, "contains_json_structure"
        if '步骤1' in original or '一、' in original:
            return True, "multi_step_system"

        # 分类不清晰的情况
        if confidence < 0.7:
            return True, f"low_confidence:{confidence}"

        # 默认使用Python（包括中等复杂度）
        return False, f"python_processing:{complexity_score},{confidence}"

    def extract_elements(self, prompt_data: Dict, domain: str) -> List[Dict]:
        """
        基于规则提取元素

        Returns:
            List of extracted elements
        """
        if domain not in self.extraction_patterns:
            return []

        pattern = self.extraction_patterns[domain]
        original = prompt_data.get('original_prompt', '')
        modules = prompt_data.get('modules', {})

        elements = []

        for category in pattern.get('primary_categories', []):
            extraction_rule = pattern.get('extraction_rules', {}).get(category)
            if not extraction_rule:
                continue

            # 检查是否有匹配的指标
            indicators = extraction_rule.get('indicators', [])
            matched_content = []

            for indicator in indicators:
                if indicator in original:
                    matched_content.append(indicator)

            # 从modules中查找相关数据
            module_data = modules.get(category, modules.get(category.replace('_', ' '), []))
            if isinstance(module_data, list):
                for item in module_data[:3]:  # 最多提取3个
                    if isinstance(item, str) and len(item) > 10:
                        matched_content.append(item)

            if not matched_content:
                continue

            # 生成元素
            for content in matched_content[:2]:  # 每个类别最多2个
                element = self._create_element(
                    category=category,
                    content=content,
                    extraction_rule=extraction_rule,
                    domain=domain
                )
                if element:
                    elements.append(element)

        return elements

    def _create_element(self, category: str, content: str,
                       extraction_rule: Dict, domain: str) -> Optional[Dict]:
        """创建单个元素"""
        # 简化名称
        name = self._simplify_name(content)

        # 生成中文名
        chinese_name = content[:15] if len(content) < 30 else content[:12] + "..."

        # 生成keywords
        keywords = self._extract_keywords(content)

        # 生成ai_prompt_template
        template_pattern = extraction_rule.get('template_pattern', '{content}')
        ai_prompt_template = content[:100]  # 简化版：直接使用内容

        # 生成reusability_score
        score_range = extraction_rule.get('reusability_score_range', [7.0, 8.0])
        reusability_score = (score_range[0] + score_range[1]) / 2

        return {
            'category': category,
            'name': name,
            'chinese_name': chinese_name,
            'ai_prompt_template': ai_prompt_template,
            'keywords': keywords,
            'reusability': reusability_score
        }

    def _simplify_name(self, text: str) -> str:
        """简化名称为标识符"""
        # 移除特殊字符
        name = re.sub(r'[^\w\s-]', '', text.lower())
        # 替换空格和连字符为下划线
        name = re.sub(r'[-\s]+', '_', name)
        # 截断到合理长度
        return name[:50] if name else 'unnamed'

    def _extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """提取关键词"""
        # 简单实现：分词后取前几个
        words = re.findall(r'[\w]+', text)
        keywords = []
        for word in words:
            if len(word) > 2:  # 忽略太短的词
                keywords.append(word)
            if len(keywords) >= max_keywords:
                break
        return keywords


class BatchLearnerV2Enhanced:
    """增强版批量学习器 - 使用AI学习的规则"""

    def __init__(self, db_path: str = "extracted_results/elements.db",
                 rules_path: str = "/tmp/enhanced_rules.json"):
        self.db = ElementDB(db_path)
        self.rules_engine = EnhancedRulesEngine(rules_path)
        self.txt_converter = TxtToJsonConverter()

        self.stats = {
            'total_files': 0,
            'processed': 0,
            'skipped': 0,
            'python_processed': 0,
            'skill_needed': 0,
            'total_elements': 0,
            'by_domain': {},
            'by_complexity': {'simple': 0, 'medium': 0, 'complex': 0},
            'skill_review_list': []
        }

    def load_prompt_file(self, file_path: Path) -> Dict:
        """加载提示词文件（支持JSON和TXT）"""
        try:
            # 尝试JSON格式
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError:
            # TXT格式
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    txt_content = f.read()
                    return self.txt_converter.convert_txt_to_prompt_data(
                        txt_content,
                        file_path.name
                    )
            except Exception as e:
                raise Exception(f"无法读取文件: {e}")

    def learn_from_directory(self, directory: str, dry_run: bool = False) -> Dict:
        """
        从目录批量学习（使用智能规则）

        Args:
            directory: 提示词文件目录
            dry_run: 预演模式，只分析不学习
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

        # 查找所有文件
        txt_files = list(dir_path.glob("*.txt"))
        json_files = list(dir_path.glob("*.json"))
        all_files = txt_files + json_files

        self.stats['total_files'] = len(all_files)

        print(f"\n{'='*80}")
        print(f"📚 批量学习器 V2 Enhanced - 智能规则版本")
        print(f"{'='*80}")
        print(f"目录: {directory}")
        print(f"文件总数: {len(all_files)} (TXT: {len(txt_files)}, JSON: {len(json_files)})")
        print(f"规则来源: enhanced_rules.json (从30个样本学习)")
        print(f"模式: {'🔍 预演模式' if dry_run else '🤖 智能处理模式'}")
        print(f"{'='*80}\n")

        # 处理每个文件
        for idx, file_path in enumerate(all_files, 1):
            print(f"\n[{idx}/{len(all_files)}] {file_path.name}")

            try:
                # 加载文件
                prompt_data = self.load_prompt_file(file_path)
                prompt_data['prompt_id'] = idx  # 临时ID

                # 步骤1: 智能领域分类
                domain, confidence, reasoning = self.rules_engine.classify_domain(prompt_data)
                print(f"  📂 Domain: {domain} (confidence: {confidence:.0%}, {reasoning})")

                # 步骤2: 计算复杂度
                complexity, score = self.rules_engine.calculate_complexity(prompt_data)
                print(f"  📊 Complexity: {complexity} (score: {score}/10)")

                # 步骤3: 判断处理方式
                use_skill, skill_reason = self.rules_engine.should_use_skill(
                    score, confidence, prompt_data
                )

                if use_skill:
                    print(f"  🤖 → Route to SKILL ({skill_reason})")
                    self.stats['skill_needed'] += 1
                    self.stats['skill_review_list'].append({
                        'file': file_path.name,
                        'domain': domain,
                        'complexity': complexity,
                        'score': score,
                        'reason': skill_reason,
                        'prompt_id': idx
                    })
                else:
                    print(f"  🐍 → Python processing ({skill_reason})")

                    if not dry_run:
                        # Python智能提取
                        elements = self.rules_engine.extract_elements(prompt_data, domain)

                        # 保存到数据库
                        added = 0
                        for element in elements:
                            success = self._add_element_to_db(
                                element, domain, idx, file_path.name
                            )
                            if success:
                                added += 1

                        self.stats['total_elements'] += added
                        print(f"  ✅ Extracted: {len(elements)} elements, Added: {added}")

                    self.stats['python_processed'] += 1

                # 更新统计
                self.stats['processed'] += 1
                self.stats['by_domain'][domain] = self.stats['by_domain'].get(domain, 0) + 1
                self.stats['by_complexity'][complexity] += 1

            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                self.stats['skipped'] += 1

        # 生成报告
        return self._generate_report(dry_run)

    def _add_element_to_db(self, element: Dict, domain: str,
                          prompt_id: int, source_file: str) -> bool:
        """添加元素到数据库"""
        try:
            # 生成element_id
            element_id = self._generate_element_id(domain, element['category'])

            # 生成tags
            tags = [domain, element['category']] + element.get('keywords', [])[:3]

            # 添加到数据库
            success = self.db.add_element(
                element_id=element_id,
                domain_id=domain,
                category_id=element['category'],
                name=element['name'],
                chinese_name=element.get('chinese_name'),
                ai_prompt_template=element['ai_prompt_template'],
                keywords=element.get('keywords', []),
                tags=list(set(tags))[:10],
                reusability_score=element.get('reusability', 7.0),
                source_prompts=[prompt_id],
                learned_from='batch_learner_v2_enhanced',
                metadata={'source_file': source_file}
            )

            return success

        except Exception as e:
            return False

    def _generate_element_id(self, domain_id: str, category_id: str) -> str:
        """生成元素ID"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT element_id FROM elements
            WHERE domain_id = ? AND category_id = ?
            ORDER BY element_id DESC
            LIMIT 1
        """, (domain_id, category_id))

        last = cursor.fetchone()
        if last:
            match = re.search(r'_(\d+)$', last[0])
            num = int(match.group(1)) + 1 if match else 1
        else:
            num = 1

        return f"{domain_id}_{category_id}_{num:03d}"

    def _generate_report(self, dry_run: bool) -> Dict:
        """生成处理报告"""
        print(f"\n{'='*80}")
        print(f"📊 批量处理报告 (V2 Enhanced)")
        print(f"{'='*80}\n")

        print(f"文件处理：")
        print(f"  总文件数: {self.stats['total_files']}")
        print(f"  成功处理: {self.stats['processed']}")
        print(f"  跳过: {self.stats['skipped']}")
        print()

        print(f"处理方式分布：")
        print(f"  🐍 Python处理: {self.stats['python_processed']}")
        print(f"  🤖 需要Skill: {self.stats['skill_needed']}")
        print(f"  比例: {self.stats['python_processed']}/{self.stats['skill_needed']}")
        print()

        print(f"领域分布：")
        for domain, count in sorted(self.stats['by_domain'].items(),
                                    key=lambda x: x[1], reverse=True):
            print(f"  • {domain}: {count} 个")
        print()

        print(f"复杂度分布：")
        for level, count in self.stats['by_complexity'].items():
            print(f"  • {level}: {count} 个")
        print()

        if not dry_run and self.stats['python_processed'] > 0:
            print(f"元素提取：")
            print(f"  新增元素: {self.stats['total_elements']}")
            print(f"  平均每个: {self.stats['total_elements'] / self.stats['python_processed']:.1f}")
            print()

        if self.stats['skill_needed'] > 0:
            # 保存需要Skill处理的列表
            skill_list_path = '/tmp/need_skill_review.json'
            with open(skill_list_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'total': self.stats['skill_needed'],
                    'generated_at': datetime.now().isoformat(),
                    'items': self.stats['skill_review_list']
                }, f, ensure_ascii=False, indent=2)

            print(f"需要Skill处理的案例 ({self.stats['skill_needed']}个)：")
            for item in self.stats['skill_review_list'][:10]:
                print(f"  • {item['file']}: {item['complexity']}({item['score']}) - {item['reason']}")
            if len(self.stats['skill_review_list']) > 10:
                print(f"  ... 还有 {len(self.stats['skill_review_list']) - 10} 个")
            print(f"\n  已保存到: {skill_list_path}")
            print()

        print(f"{'='*80}\n")

        return {
            'stats': self.stats,
            'skill_list_path': '/tmp/need_skill_review.json' if self.stats['skill_needed'] > 0 else None
        }

    def close(self):
        """关闭数据库"""
        self.db.close()


# 命令行使用
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='批量学习 V2 Enhanced (智能规则版)')
    parser.add_argument('directory', help='提示词文件目录')
    parser.add_argument('--dry-run', action='store_true', help='预演模式')
    parser.add_argument('--db', default='extracted_results/elements.db', help='数据库路径')
    parser.add_argument('--rules', default='/tmp/enhanced_rules.json', help='规则文件路径')

    args = parser.parse_args()

    # 检查规则文件
    if not Path(args.rules).exists():
        print(f"\n⚠️  错误: 规则文件不存在: {args.rules}")
        print("请先运行阶段1生成 enhanced_rules.json\n")
        exit(1)

    learner = BatchLearnerV2Enhanced(args.db, args.rules)

    try:
        report = learner.learn_from_directory(
            directory=args.directory,
            dry_run=args.dry_run
        )

        # 导出数据库
        if not args.dry_run and report['stats']['python_processed'] > 0:
            learner.db.export_to_json('extracted_results/universal_elements_library.json')
            print("✅ 已导出到 universal_elements_library.json")

    finally:
        learner.close()
