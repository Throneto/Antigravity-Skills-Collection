---
name: universal-learner
description: 通用学习器 - 从任何领域的Prompt中自动提取可复用元素，持续学习和积累知识
---

# Universal Learner - 通用学习器 Skill

**版本**: 1.0
**架构**: Master-Subordinate
**学习方式**: 半自动（生成报告 + 人工审核）

## 🎯 核心功能

从任何领域的Prompt中自动提取可复用元素，存入Universal Elements Library数据库。

支持7大领域：
- 📷 **portrait** - 人像摄影
- 🏠 **interior** - 室内设计
- 📦 **product** - 产品摄影
- 🎨 **design** - 平面设计
- 🎭 **art** - 艺术风格
- 🎬 **video** - 视频生成
- 📸 **common** - 通用摄影技术

---

## 📋 使用方式

### 方式1：学习单个Prompt

```
学习这个Prompt: [粘贴完整Prompt]
```

或

```
分析并学习: A premium collector's edition book photographed with Phase One camera, featuring Italian calfskin binding...
```

### 方式2：批量学习18个源Prompts

```
批量学习所有Prompts
```

或

```
学习extracted_modules.json中的所有Prompts
```

### 方式3：学习特定领域

```
只学习product领域的Prompts
```

或

```
学习Prompt #1, #6, #14, #16（产品摄影）
```

### 方式4：学习设计系统/模板 ⭐ 新增

```
学习这个设计系统：[粘贴完整的设计系统规范]
```

或

```
学习这个PPT模板风格：[设计规范内容]
```

**自动识别特征**：
- 包含"设计系统"、"风格规范"、"视觉理念"关键词
- 有层级结构（背景系统 + 配色方案 + 字体系统...）
- 包含设计理念说明

**特殊处理**：
- 提取元素 → elements表
- 创建模板 → design_templates表（保留完整性）

---

## 🔄 工作流程

```
输入Prompt
  ↓
【Step 0: 类型识别】⭐ 新增
  - 判断是"画面描述型" 还是 "设计系统型"
  - 设计系统特征：包含"设计系统"、"风格规范"、有层级结构
  - 输出: {"type": "prompt" | "design_system"}
  ↓
【Step 1: 领域分类】domain_classifier.md
  - 识别主要领域（product/design/art/video...）
  - 判断是否多领域
  - 输出: {"primary": "product", "secondary": ["photography"]}
  ↓
【Step 2: 元素提取】element_extractor.md
  - 根据领域提取对应元素
  - product → product_types, materials, photography_techniques
  - design → layouts, effects, typography
  - art → art_styles, special_effects
  - 输出: List[{category, name, template, keywords}]
  ↓
【Step 3: 自动打标签】tagger.md
  - 基于keywords生成tags
  - 添加领域标签、类别标签
  - 跨领域标签识别（luxury, glass, dynamic...）
  - 输出: tags列表
  ↓
【Step 4: 计算复用性】
  - reusability_score (1-10)
  - 基于：通用性、清晰度、独立性
  ↓
【Step 5: 更新数据库】library_updater.md
  - 检查是否已存在（去重）
  - 生成element_id
  - 写入elements.db
  - 更新tag_index
  ↓
【Step 5.1: 如果是设计系统】⭐ 新增
  - 同时创建模板记录
  - 写入design_templates表
  - 关联所有提取的元素
  - 保存设计理念、使用指南等完整信息
  ↓
【Step 6: 生成报告】
  - 新学习的元素列表
  - 按领域和类别分组
  - 推荐的tags
  - 质量评估
  - （设计系统）额外显示模板信息
```

---

## 📊 输出示例

### 学习报告

```markdown
# Universal Learner - 学习报告

**学习时间**: 2026-01-01 18:30:00
**源Prompt**: Prompt #1

## 🎯 领域识别

主领域: **product** (产品摄影)
次领域: **common** (通用摄影)

## 📦 提取的元素

### 产品类型 (product_types)

1. **collector_edition_book** - 收藏版书籍
   - 模板: premium collector's edition book, luxury binding, Italian calfskin cover
   - 关键词: collector's edition, premium book, luxury binding
   - 标签: product, book, luxury, collectible
   - 复用性: 7.5/10
   - element_id: product_product_types_001

### 材质纹理 (material_textures)

2. **glossy_reflective** - 光泽反射材质
   - 模板: high-end glossy surface, reflective finish, metallic sheen
   - 关键词: glossy, reflective, shiny, polished
   - 标签: material, glossy, luxury, product
   - 复用性: 8.5/10
   - element_id: product_material_textures_002

### 摄影技术 (photography_techniques)

3. **macro_product_shot** - 产品微距特写
   - 模板: Phase One medium format camera with 100mm macro lens, razor-sharp focus
   - 关键词: macro, close-up, detailed, high-resolution
   - 标签: photography, macro, product, technical
   - 复用性: 9.0/10
   - element_id: common_photography_techniques_032

## ✅ 已添加到数据库

- 3个新元素已写入 elements.db
- 更新了12个标签索引
- product领域: 60 → 63 个元素
- common领域: 31 → 32 个元素

## 💡 质量评估

- 提取完整度: 95%
- 标签质量: 优秀
- 复用性评分: 8.3/10 (平均)
```

---

## 🎛️ 配置选项

### 自动化程度

- **当前**: 半自动（生成报告 + 人工审核）
- **未来**: 可选全自动模式

### 复用性评分标准

| 评分 | 标准 |
|------|------|
| 9-10 | 极高复用性：跨领域通用，如"macro photography", "soft lighting" |
| 7-8  | 高复用性：领域内通用，如"product on table", "geometric layout" |
| 5-6  | 中等复用性：特定场景，如"collector's edition book" |
| 3-4  | 低复用性：非常具体，如"vintage 1960s typewriter" |
| 1-2  | 极低复用性：一次性描述，不推荐提取 |

---

## 📚 数据源

**输入**: `extracted_results/extracted_modules.json` (18个源Prompts)

**输出**:
- `extracted_results/elements.db` (SQLite数据库)
- `extracted_results/universal_elements_library.json` (JSON导出)

---

## 🔧 模块说明

| 模块 | 文件 | 功能 |
|------|------|------|
| 领域分类器 | `modules/domain_classifier.md` | 识别Prompt属于哪个领域 |
| 元素提取器 | `modules/element_extractor.md` | 提取可复用元素 |
| 标签生成器 | `modules/tagger.md` | 自动生成tags |
| 库更新器 | `modules/library_updater.md` | 更新数据库 |

---

## ✅ 验收标准

学习成功的标志：
- ✅ 能正确识别7大领域
- ✅ 从18个Prompts提取~440个元素
- ✅ 自动去重（不重复添加已存在元素）
- ✅ 标签质量高（相关性强）
- ✅ 复用性评分合理

---

**Skill状态**: ✅ 已实现
**最后更新**: 2026-01-01
**维护者**: Universal Library System
