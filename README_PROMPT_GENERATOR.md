# 提示词生成系统 V3.0 - 使用指南

## 🎯 系统概述

这是一个**智能、灵活、可配置**的AI图像提示词生成系统，采用**Skill + 配置文件**的混合架构。

### 核心优势

✅ **无需修改代码** - 所有配置都在JSON文件中
✅ **自然语言交互** - 通过Claude Code Skill智能生成
✅ **模板化管理** - 5种预设模板，覆盖所有场景
✅ **风格智能匹配** - 自动识别并添加风格关键词
✅ **921个元素库** - 所有元素可追溯、高质量（平均9.4/10）

---

## 📁 系统架构

```
prompt_gen_image/
├── templates.json              # 配置模板（核心配置文件）
├── generator_engine.py         # 生成引擎（核心逻辑）
├── extracted_results/
│   └── elements.db            # 元素数据库（921个元素）
└── .claude/skills/
    └── prompt-generator/
        └── skill.md           # Claude Code Skill
```

### 三层架构

```
用户自然语言
      ↓
Claude Code Skill (智能分析)
      ↓
Generator Engine (动态生成)
      ↓
Elements Database (921个元素)
```

---

## 🚀 使用方式

### 方式1: 通过 Claude Code Skill（推荐）

在Claude Code中直接使用自然语言：

```
你: 生成一个赛博朋克风格的动漫少女提示词

Claude:
🎨 主题: 赛博朋克风格的动漫少女
📋 模板: 完整人物肖像

✨ 生成的提示词:
female, young adult (18-25 years old), East Asian, fair pale skin tone,
realistic textured skin with visible pores, natural detail, oval asian
refined face shape, large expressive almond eyes, chestnut brown straight
hair in ponytail with straight bangs framing face, Korean K-beauty makeup
style, fresh natural dewy skin, gradient lips, straight brows, innocent
gentle gaze, standing in a relaxed, casual pose, wearing modern casual
outfit with comfortable fit...

📊 使用元素 (17个): ...
```

**激活Skill**:
```bash
# 方法1: 直接使用技能名
/prompt-generator

# 方法2: 直接描述需求（Skill会自动识别）
生成一个中年男性商务人士的肖像
```

### 方式2: 直接调用Python引擎

```python
from generator_engine import PromptGeneratorEngine

engine = PromptGeneratorEngine()

# 使用指定模板
result = engine.generate_from_template(
    template_name='portrait_full',
    theme='赛博朋克风格的动漫少女',
    style_keywords=['neon', 'cyberpunk', 'futuristic', 'anime']
)

# 智能生成（自动选择模板）
result = engine.generate_with_auto_template(
    theme='奢华香水瓶产品摄影',
    theme_type='product',
    style='luxury'
)

print(result['prompt'])
engine.close()
```

### 方式3: 命令行测试

```bash
# 运行测试脚本（包含4个示例）
python3 generator_engine.py
```

---

## 📋 可用模板

### 1. portrait_full - 完整人物肖像

**适用**: 人物肖像、角色设计、人物插画
**属性**: 性别、年龄、国籍、肤色、皮肤质感、脸型、眼型、发型、妆容、表情、姿势、服装（12个）

```python
engine.generate_from_template('portrait_full', '你的主题')
```

### 2. portrait_minimal - 简化人物肖像

**适用**: 简单人物、头像、快速草图
**属性**: 性别、年龄、国籍、脸型、表情（5个）

```python
engine.generate_from_template('portrait_minimal', '你的主题')
```

### 3. product_photography - 产品摄影

**适用**: 商业产品、电商图片、广告
**属性**: 产品类型、灯光、相机、构图

```python
engine.generate_from_template('product_photography', '你的主题')
```

### 4. art_style - 艺术风格

**适用**: 艺术创作、插画、绘画
**属性**: 艺术媒介、技法、风格

```python
engine.generate_from_template('art_style', '你的主题')
```

### 5. cinematic - 电影级

**适用**: 电影感、影视剧照、戏剧性场景
**属性**: 电影级灯光、相机、氛围

```python
engine.generate_from_template('cinematic', '你的主题')
```

---

## 🎨 支持的风格

在 `templates.json` 中预设了9种风格关键词：

| 风格 | 关键词 | 适用场景 |
|------|--------|----------|
| cyberpunk | neon, futuristic, tech, glow | 赛博朋克、未来科技 |
| anime | anime, manga, illustration, detailed | 动漫、二次元、插画 |
| realistic | photorealistic, detailed, realistic | 写实、照片级 |
| vintage | vintage, retro, film grain, analog | 复古、怀旧、胶片 |
| minimalist | minimal, clean, simple, elegant | 极简、简约 |
| luxury | luxury, premium, elegant, sophisticated | 奢华、高端 |
| chinese_traditional | chinese, traditional, ink, watercolor | 中国风、水墨 |
| japanese | japanese, zen, traditional, delicate | 日式、和风 |
| fantasy | fantasy, magical, ethereal, mystical | 奇幻、魔幻 |

---

## 🛠️ 自定义配置

### 添加新模板

编辑 `templates.json`:

```json
{
  "templates": {
    "your_new_template": {
      "name": "你的模板名称",
      "description": "模板描述",
      "attributes": {
        "attribute_name": {
          "domain": "portrait",
          "category": "category_name",
          "limit": 1,
          "required": true
        }
      }
    }
  }
}
```

### 添加新风格

```json
{
  "style_keywords": {
    "your_style": ["keyword1", "keyword2", "keyword3"]
  }
}
```

### 覆盖特定属性

```python
result = engine.generate_from_template(
    'portrait_full',
    '你的主题',
    attribute_overrides={
        'gender': {'category': 'gender', 'limit': 1}  # 覆盖配置
    }
)
```

---

## 📊 系统数据

### 元素库统计

```
总元素: 921 个
有效率: 99.2% (914/921)
平均可重用性: 9.4/10
高质量元素 (8-10分): 86.1%
```

### 领域分布

```
portrait (人像):    432 个 (46.9%)
common (通用):      188 个 (20.4%)
interior (室内):     77 个 ( 8.4%)
product (产品):      71 个 ( 7.7%)
design (设计):       56 个 ( 6.1%)
video (视频):        49 个 ( 5.3%)
art (艺术):          48 个 ( 5.2%)
```

### 人物属性覆盖率

```
✅ 性别 (gender):         2/2   (100%)
✅ 年龄 (age_range):      3/3   (100%)
✅ 国籍 (ethnicity):      8/8   (100%)
✅ 肤色 (skin_tones):     7/7   (100%)
✅ 皮肤质感 (skin_textures): 4/4 (100%)
✅ 脸型 (face_shapes):    6/6   (100%)
✅ 眼型 (eye_types):     10/10  (100%)
✅ 发型 (hair_styles):    3/3   (100%)
✅ 妆容 (makeup_styles): 11/11  (100%)
✅ 表情 (expressions):    6/6   (100%)
✅ 姿势 (poses):          6/6   (100%)
✅ 服装 (clothing_styles): 5/5  (100%)
```

---

## 💡 使用示例

### 示例1: 人物肖像

```python
# 完整人物描述
result = engine.generate_from_template(
    'portrait_full',
    '赛博朋克风格的动漫少女',
    style_keywords=['neon', 'cyberpunk', 'anime']
)

# 输出: female, young adult, East Asian, fair pale skin tone,
#       realistic textured skin, oval face shape, large almond eyes...
```

### 示例2: 产品摄影

```python
result = engine.generate_with_auto_template(
    '高端化妆品产品摄影',
    theme_type='product',
    style='luxury'
)

# 输出: professional product photography, soft studio lighting,
#       luxury elegant presentation, 4K resolution...
```

### 示例3: 艺术创作

```python
result = engine.generate_with_auto_template(
    '中国风水墨画山水',
    theme_type='art',
    style='chinese_traditional'
)

# 输出: traditional Chinese ink painting, flowing brush strokes,
#       minimalist, delicate features...
```

### 示例4: 电影级

```python
result = engine.generate_from_template(
    'cinematic',
    '电影级人物特写镜头',
    style_keywords=['dramatic', 'moody', 'atmospheric']
)

# 输出: cinematic lighting, dramatic atmosphere, 8K film camera,
#       moody color grading...
```

---

## 🔧 高级功能

### 1. 列出所有模板

```python
templates = engine.list_templates()
print(templates)
# ['portrait_full', 'portrait_minimal', 'product_photography', 'art_style', 'cinematic']
```

### 2. 查看模板详情

```python
template = engine.get_template('portrait_full')
print(template['name'])        # 完整人物肖像
print(template['description']) # 包含所有基础人物属性的完整模板...
```

### 3. 直接搜索元素

```python
# 按类别搜索
elements = engine.get_elements_by_category('portrait', 'gender', limit=2)

# 按关键词搜索
elements = engine.search_by_keywords(['cyberpunk', 'neon'], limit=5)
```

### 4. 详细输出控制

```python
# 关闭详细输出
result = engine.generate_from_template(
    'portrait_full',
    '你的主题',
    verbose=False  # 不打印过程信息
)
```

---

## 📈 版本历史

### V3.0 (2026-01-02) - 当前版本
- ✅ 引入配置模板系统
- ✅ 创建可配置生成引擎
- ✅ 开发Claude Code Skill
- ✅ 支持5种预设模板
- ✅ 支持9种风格关键词
- ✅ 无需修改代码即可生成

### V2.1 (2026-01-01)
- ✅ 修复所有空template元素
- ✅ 人物属性100%覆盖
- ✅ 添加性别属性

### V2.0
- ✅ 自动学习系统
- ✅ AI分类识别
- ✅ 921个元素库

---

## 🎓 最佳实践

### 1. 选择合适的模板
- **详细人物** → `portrait_full`
- **简单人物** → `portrait_minimal`
- **产品图片** → `product_photography`
- **艺术创作** → `art_style`
- **电影感** → `cinematic`

### 2. 使用风格关键词
```python
# 好的做法
style_keywords=['cyberpunk', 'neon', 'futuristic']

# 不推荐
style_keywords=['good', 'nice', 'beautiful']  # 太泛化
```

### 3. 人物肖像必须包含性别
```python
# 对于portrait模板，确保gender属性存在
# 系统会自动从数据库中选择gender元素
```

### 4. 合理设置limit
```python
# 每个属性建议limit=1-3
'attribute': {'category': 'xxx', 'limit': 2}  # 适中
'attribute': {'category': 'xxx', 'limit': 10}  # 太多，提示词会很长
```

---

## 🐛 常见问题

### Q: Skill如何激活？
A: 在Claude Code中输入 `/prompt-generator` 或直接描述需求

### Q: 如何添加自定义模板？
A: 编辑 `templates.json` 文件，添加新的模板配置

### Q: 生成的提示词太长怎么办？
A: 使用 `portrait_minimal` 或减少每个属性的 `limit` 值

### Q: 如何确保包含特定元素？
A: 使用 `attribute_overrides` 参数或添加到 `style_keywords`

### Q: 数据库在哪里？
A: `extracted_results/elements.db`（921个元素）

---

## 📞 支持

- **文档**: 本README
- **Skill文档**: `.claude/skills/prompt-generator/skill.md`
- **模板配置**: `templates.json`
- **代码**: `generator_engine.py`

---

## 🎉 开始使用

```bash
# 1. 测试引擎
python3 generator_engine.py

# 2. 在Claude Code中使用
/prompt-generator

# 3. 开始生成你的提示词！
```

**享受无需改代码的智能提示词生成体验！** 🚀
