# 实战示例：如何用 prompt-extractor 学习

## 场景：小明想学习如何写"微距摄影"提示词

---

### 第1步：获取分析报告

小明输入一个优秀的微距提示词到 prompt-extractor：

**原始提示词**:
```
An ethereal deity composed of intricate white translucent optical fibers,
holding a glowing cube. Shot on 105mm Macro lens, f/1.8, 8k resolution,
subsurface scattering through fingers.
```

**得到分析报告** → `ethereal_deity_analysis_report.md`

---

### 第2步：解构学习 - 看结构

小明打开报告，看到 **"结构类型"** 部分：

```markdown
## 结构类型
7层金字塔式分层描述

Layer 1: Subject & Materiality (主体与材质)
Layer 2: Spatial Structure (空间结构)
Layer 3: Action & Pose (动作姿态)
...
Layer 7: Style & Engine Filters (风格与渲染)
```

**💡 小明学到**:
> "哦，原来提示词可以这样分层写！我以前都是一股脑全写在一起。"

**立即应用**:
小明尝试用7层结构写自己的提示词：
```
Layer 1: 一个水晶雕塑
Layer 2: 放在黑色丝绒上
Layer 3: 被光线穿透
Layer 4: 无
Layer 5: 透明+彩虹折射
Layer 6: 内部气泡、边缘锐利
Layer 7: 微距摄影，Octane渲染
```

---

### 第3步：技术学习 - 看参数

小明继续看 **"技术参数"** 部分：

```json
{
  "camera": {
    "lens": "105mm Macro lens",
    "aperture": "f/1.8",
    "angle": "High-angle close-up (45-degree top-down)"
  },
  "lighting": {
    "special_effects": [
      "Subsurface scattering (SSS)",
      "Volumetric lighting",
      "Caustics"
    ]
  },
  "resolution": "8K"
}
```

**💡 小明学到**:
> "微距摄影要用105mm镜头，f/1.8光圈可以制造浅景深。
> SSS是半透明材质的关键！"

**小明做笔记**:
```
┌─────────────────────────────────────┐
│      微距摄影参数卡片                 │
├─────────────────────────────────────┤
│ 镜头：105mm Macro                   │
│ 光圈：f/1.8 (浅景深)                │
│ 角度：45° 俯视                      │
│ 必备效果：SSS (半透明材质)           │
│ 分辨率：8K                          │
└─────────────────────────────────────┘
```

---

### 第4步：模板学习 - 看技巧

小明看到 **"高价值可复用模板"** 部分：

```markdown
### 模板2: Macro + SSS Lighting

**结构**:
{subject}, {close-up angle}, {translucent material},
{light source} causing subsurface scattering through {body part},
{lens}mm Macro, f/{aperture}

**示例**:
Jellyfish creature, top-down shot, translucent membrane,
bioluminescent core causing SSS through tentacles,
105mm Macro, f/1.8
```

**💡 小明学到**:
> "原来SSS要这样写！需要明确：
> 1. 半透明材质
> 2. 光源位置
> 3. 光线穿透的部位"

**小明练习应用**:
```
我的水晶雕塑提示词改进版：

Crystal sculpture, high-angle close-up, translucent quartz,
internal LED light causing subsurface scattering through
crystal facets, 105mm Macro, f/1.8, volumetric lighting
```

---

### 第5步：色彩策略 - 看配色

小明看到 **"色彩方案"** 部分：

```markdown
### 核心策略: "Cold Shell, Warm Heart" (外冷内暖)

**主色调** (身体 & 背景):
- 冷色: Cyan, Ice Blue, Teal

**次色调** (发光物体):
- 暖色: Pink, Amber, Purple, Gold

**对比效果**: 冷色环境 vs 暖色焦点 - 戏剧化对立
```

**💡 小明学到**:
> "色彩对立！冷色环境 + 暖色焦点 = 视觉冲击力！"

**小明应用到水晶雕塑**:
```
改进版本2：

Crystal sculpture on black velvet (cold environment),
Color: Body=ice blue/silver (cold),
Internal glow=warm amber/rose gold (warm),
Lighting from inside creating color contrast,
105mm Macro, f/1.8, subsurface scattering
```

---

### 第6步：避坑学习 - 看挑战

小明看到 **"AI生成挑战点"**：

```markdown
| 挑战 | 难度 | 说明 |
|------|------|------|
| 次表面散射控制 | ⭐⭐⭐⭐ | 手指透光效果需高级渲染 |
| 微型城市细节 | ⭐⭐⭐⭐⭐ | 需超高分辨率 |
```

**💡 小明学到**:
> "SSS效果容易失败，需要强化描述！"

**小明添加强化词**:
```
最终版本：

Intricate crystal sculpture with CLEARLY VISIBLE internal
facets, placed on black velvet, Color: Body=ice blue/silver,
Internal warm amber glow, STRONG subsurface scattering effect
making crystal edges glow translucent, light rays passing
through multiple layers, 105mm Macro, f/1.8, 8K resolution,
Octane Render with ray tracing enabled
```

---

### 第7步：质量评估 - 看评分

小明对比原提示词的评分：

```markdown
## 质量评分

- 清晰度: 10/10
- 细节丰富度: 10/10
- 技术完整度: 10/10
```

**💡 小明思考**:
> "10分的提示词有这些特点：
> - 具体的数值（105mm, f/1.8, 8K）
> - 专业术语（SSS, ray tracing）
> - 明确的色彩策略
> - 清晰的光源设计"

**小明给自己的提示词打分**:
```
我的提示词自评：
- 清晰度: 8/10 (结构清晰，但可以更简洁)
- 细节丰富度: 7/10 (缺少一些微观细节描述)
- 技术完整度: 9/10 (参数齐全)

改进方向：
- 添加微观细节（如"crystal grain structure visible"）
- 简化冗余描述
```

---

### 第8步：建立自己的工具箱

小明经过多次学习，建立了自己的 **"提示词工具箱"**：

```markdown
# 小明的微距摄影工具箱

## 📷 相机配置模板
105mm Macro, f/1.8, 8K resolution, high-angle close-up

## 💡 光学效果模板
subsurface scattering through {body part},
volumetric lighting, caustics, ray tracing

## 🎨 色彩策略模板
Color: {subject}={cool colors}, {light source}={warm colors},
creating dramatic color contrast

## 📐 构图模板
Foreground: {main object} (sharp focus),
Background: {environment} (bokeh blur),
45-degree top-down angle

## 🔧 渲染增强模板
Octane Render, ray tracing enabled, 8K resolution,
photorealistic, hyper-detailed
```

---

### 第9步：实战测试

小明用新学的技巧创作了3个提示词：

**提示词1: 水晶雕塑**
```
Intricate crystal sculpture, ice blue translucent quartz,
internal warm amber LED glow, subsurface scattering through
crystal facets, 105mm Macro, f/1.8, black velvet background,
8K resolution, Octane Render
```
→ AI生成效果：⭐⭐⭐⭐⭐ (完美！)

**提示词2: 玻璃花朵**
```
Delicate glass flower, translucent petals, backlight causing
SSS effect, color gradient from cool cyan to warm pink,
105mm Macro, f/1.8, shallow depth of field
```
→ AI生成效果：⭐⭐⭐⭐ (很好，但色彩过渡不够自然)

**提示词3: 宝石**
```
Polished emerald gemstone, internal inclusions visible,
dramatic lighting, 105mm Macro, f/4
```
→ AI生成效果：⭐⭐⭐ (不错，但缺少光学效果)

---

### 第10步：迭代优化

小明分析失败的提示词2和3：

**问题诊断**:
- 提示词2：缺少具体的色彩过渡描述
- 提示词3：光圈f/4太大，景深不够；缺少SSS和Caustics效果

**改进版**:

提示词2改进：
```
Delicate glass flower, translucent gradient petals transitioning
from ice blue base to warm rose pink tips, backlight positioned
behind causing strong subsurface scattering, each petal edge
glowing translucent, 105mm Macro, f/1.8, volumetric fog
```
→ 新效果：⭐⭐⭐⭐⭐

提示词3改进：
```
Polished emerald gemstone with clearly visible internal garden
of inclusions, dramatic rim lighting creating caustics and
rainbow reflections, subsurface glow revealing inner structure,
105mm Macro, f/1.8, ray tracing enabled
```
→ 新效果：⭐⭐⭐⭐⭐

---

## 📈 小明的学习成果

### 学习前 vs 学习后

**学习前的提示词** (凭感觉写):
```
A beautiful crystal on black background, very detailed
```
→ 效果：⭐⭐ (模糊、缺少细节、普通)

**学习后的提示词** (系统化):
```
Intricate crystal sculpture, ice blue translucent quartz,
internal warm amber glow, subsurface scattering through facets,
105mm Macro, f/1.8, black velvet background, Octane Render, 8K
```
→ 效果：⭐⭐⭐⭐⭐ (锐利、细节丰富、专业)

---

### 小明的收获总结

| 学习维度 | 具体提升 |
|---------|---------|
| **结构化思维** | 从无序堆砌 → 7层金字塔式组织 |
| **技术参数** | 从"很详细" → "105mm, f/1.8, 8K" |
| **光学知识** | 学会了SSS、Caustics、Ray Tracing |
| **色彩策略** | 掌握了冷暖对立配色法 |
| **质量意识** | 能自我评分和迭代优化 |

---

### 小明的下一步学习计划

```
✅ 已掌握：微距摄影
🔄 学习中：电影级人像光线
⏸️ 待学习：赛博朋克场景构建
⏸️ 待学习：概念艺术风格融合
```

---

## 🎯 关键启示

### 为什么 prompt-extractor 适合学习？

1. **结构化呈现** - 把复杂提示词拆解成可理解的模块
2. **质量标准** - 通过评分系统建立"好提示词"的标准
3. **可复用模板** - 提取出可以直接套用的写作模板
4. **技术知识库** - 系统学习相机/渲染/光学参数
5. **避坑指南** - 预判AI生成难点

### 最佳学习方式

```
分析优秀作品 → 提取模板 → 应用实践 → 对比效果 → 迭代优化
    ↑                                              ↓
    └──────────────── 持续循环 ─────────────────────┘
```

---

**学习时间投入**:
- 初步理解：2-3小时
- 熟练应用：10-20小时
- 形成体系：50+小时

**投入产出比**: ⭐⭐⭐⭐⭐
- 从0到能写出专业级提示词：约20小时
- 传统摸索方式：可能需要100+小时

---

**结论**: prompt-extractor 就像一个 **AI提示词写作教练**，它不仅分析结构，更重要的是**教你如何思考、如何组织、如何优化**。
