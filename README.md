# AI Prompt Generator - 智能提示词生成系统

一个基于Universal Elements Library的智能AI图像提示词生成系统，支持人像、设计、艺术、产品、视频等多个领域。

## ✨ 核心特性

### 🎯 双轨制系统
- **元素级生成**：从1140+个元素中智能选择组合
- **模板级生成**：完整设计系统模板（如Apple PPT模板）

### 🧠 智能能力
- **语义理解**：区分主体/风格/氛围
- **常识推理**：自动推断合理属性（如人种→眼睛颜色）
- **一致性检查**：自动检测并修正逻辑冲突
- **框架驱动**：基于`prompt_framework.yaml`结构化生成

### 📦 支持领域
- 📷 **portrait** - 人像摄影（502个元素）
- 🎨 **design** - 平面设计（80个元素）
- 🏠 **interior** - 室内设计
- 📦 **product** - 产品摄影
- 🎭 **art** - 艺术风格
- 🎬 **video** - 视频生成
- 📸 **common** - 通用摄影技术（205个元素）

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from intelligent_generator import IntelligentGenerator

gen = IntelligentGenerator()

# 生成人像提示词
prompt = gen.generate_from_intent({
    'subject': {
        'gender': 'female',
        'ethnicity': 'East_Asian',
        'age_range': 'young_adult'
    },
    'styling': {
        'makeup': 'k_beauty'
    },
    'lighting': {
        'lighting_type': 'natural'
    }
})

print(prompt)
gen.close()
```

### 使用框架驱动生成器

```python
from framework_loader import FrameworkDrivenGenerator

gen = FrameworkDrivenGenerator()

# 查询所有候选元素
candidates = gen.query_all_candidates_by_framework(intent)

# 选择最优元素并生成
prompt = gen.generate_prompt_from_intent(intent)
```

## 📖 项目结构

```
├── intelligent_generator.py      # 核心生成引擎
├── framework_loader.py            # 框架驱动加载器
├── prompt_framework.yaml          # 人像提示词框架定义
├── element_db.py                  # 数据库操作
├── .claude/
│   └── skills/                    # Claude Code Skills
│       ├── intelligent-prompt-generator/
│       ├── design-master/
│       ├── universal-learner/
│       └── ...
├── extracted_results/
│   └── elements.db                # Universal Elements Library (1140+元素)
└── knowledge_base/                # 知识库
```

## 🎨 使用示例

### 示例1：生成韩系马卡龙色人像

```python
intent = {
    'subject': {'gender': 'female', 'ethnicity': 'East_Asian'},
    'styling': {'makeup': 'k_beauty', 'clothing': 'modern'},
    'lighting': {'lighting_type': 'natural'},
    'scene': {'atmosphere': 'fashion'}
}

prompt = gen.generate_from_intent(intent)
# 输出: Korean fashion photography, young Korean woman in pastel macaroon-colored modern outfit...
```

### 示例2：使用Apple PPT模板

```python
# 查询模板
template = query_design_template('apple_soft_blue_ppt')

# 获取完整的12元素系统
# 包括：背景、布局、配色、字体、视觉效果
```

### 示例3：超写实人像摄影

```python
intent = {
    'subject': {'gender': 'male', 'age_range': 'young_adult'},
    'facial': {'skin_texture': 'hyper_realistic_with_details'},
    'lighting': {'lighting_type': 'overcast_cinematic'},
    'technical': {'photography': '85mm_shallow_dof', 'post_processing': 'hdr'}
}

prompt = gen.generate_from_intent(intent)
# 超写实效果：可见毛孔、自然疤痕、电影级光影
```

## 🛠️ 核心功能

### 1. 元素库系统
- **1140+个可复用元素**
- 7大领域分类
- 复用性评分（1-10）
- SQLite数据库存储

### 2. 模板系统
- 完整设计系统保存
- 包含设计理念、使用指南
- 元素结构化组织
- 支持PPT、UI、品牌VI等

### 3. 智能生成
- 框架驱动（`prompt_framework.yaml`）
- 语义匹配和推理
- 一致性检查
- 自动冲突解决

### 4. 学习系统
- 从新提示词中提取元素
- 自动领域分类
- 复用性评分
- 持续积累知识

## 📊 数据库统计

- **总元素数**: 1140+
- **Portrait领域**: 502个（人像专用）
- **Design领域**: 80个（平面设计）
- **Common领域**: 205个（通用技术）
- **模板数**: 1个（Apple淡蓝商务PPT）

## 🔧 配置

### prompt_framework.yaml

定义人像提示词的完整框架：
- 7大类：subject, facial, styling, expression, lighting, scene, technical
- 字段到数据库的映射
- 依赖规则（如era=ancient → makeup=traditional）
- 验证规则

## 📝 开发指南

### 添加新元素

```python
from element_db import ElementDatabase

db = ElementDatabase()
db.add_element({
    'element_id': 'portrait_expressions_010',
    'domain_id': 'portrait',
    'category_id': 'expressions',
    'name': 'serene_smile',
    'chinese_name': '宁静微笑',
    'ai_prompt_template': 'serene gentle smile...',
    'keywords': '["serene", "gentle", "peaceful"]',
    'reusability_score': 8.5
})
```

### 创建新模板

```python
template = {
    'template_id': 'template_xxx',
    'name': 'Template Name',
    'chinese_name': '模板中文名',
    'category': 'ppt_design',
    'element_ids': ['elem1', 'elem2', ...],
    'element_structure': {
        'backgrounds': ['elem1'],
        'layouts': ['elem2']
    },
    'design_philosophy': '设计理念...',
    'usage_scenarios': '使用场景...'
}
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

MIT License

## 🙏 致谢

- 基于Claude Code Skills系统
- Universal Elements Library架构
- 框架驱动生成理念
