# 从"西部世界仿生人"案例中学到的经验

## 📅 时间线

**2026-01-02** - 实战案例：用户要求生成西部世界风格半人半机器人提示词

---

## 🎯 问题回顾

### 第一次尝试 - 失败
**我的提示词思路**：
```
试图避免"split"这个词，担心产生"拼接感"
用"unified face"、"not split"、"skin removed"等描述
结果：生成的图片完全不对
```

**生成结果问题**：
1. 看起来像两个独立的头（一个人脸 + 一个机械头骨在旁边）
2. 没有"同一张脸"的感觉
3. AI完全误解了需求

### 第二次尝试 - 改进但仍有问题
**调整思路**：
```
强调"SAME FACE"、"ONE HEAD"
描述为"skin layer removed"
添加解剖学术语
```

**生成结果问题**：
1. 右侧看起来像**戴了一个白色面具**
2. 是平面的覆盖物，不是立体的内部结构
3. 缺少深度感和骨骼凹陷

### 用户提供的正确提示词 - 成功 ✅

**核心结构**：
```
Cinematic split-face portrait, PERFECT VERTICAL SPLIT

LEFT HALF - HUMAN SIDE:
[详细的人类特征描述]

RIGHT HALF - ANDROID SIDE:
[具体的机械部件：servo mechanisms, fiber optic cables,
titanium alloy, circuit boards, hydraulic pistons...]

LIGHTING: Three-point lighting setup
CAMERA: ARRI Alexa Mini LF, Cooke S7 100mm T2.8
STYLE: Westworld HBO aesthetic

(photorealistic skin:1.4), (mechanical precision:1.3)
NEGATIVE: cyberpunk, neon, chrome, mask, two heads
```

**为什么成功**：
1. ✅ 直接拥抱"split"术语，然后精确定义
2. ✅ 结构化分段（LEFT HALF / RIGHT HALF）
3. ✅ 具体机械部件名称
4. ✅ 专业摄影参数
5. ✅ 详细负面提示词

---

## 💡 核心学习点

### 1. 不要试图"骗"AI

**❌ 错误思维**：
```
"我不说split，AI就不会画成拼接的样子"
"我用否定词引导AI"
```

**✅ 正确思维**：
```
"这就是split face构图，我要明确定义怎么split"
"用专业术语 + 详细描述"
```

**教训**：AI是基于训练数据的，专业术语会激活正确的视觉模式。回避术语反而让AI困惑。

---

### 2. 结构化 > 长度

**❌ 我的做法**：
```
一大段混合描述，AI需要自己提取重点
```

**✅ 正确做法**：
```
LEFT HALF - HUMAN SIDE: [清晰分段]
RIGHT HALF - ANDROID SIDE: [清晰分段]
LIGHTING: [独立段落]
CAMERA: [独立段落]
```

**教训**：清晰的结构比堆砌词汇更重要。

---

### 3. 具体化战胜抽象

**对比**：

| 我的抽象描述 ❌ | 正确的具体描述 ✅ |
|----------------|------------------|
| white mechanical structure | complex servo mechanisms at jaw and cheekbone |
| white optical sensor | advanced camera lens system with blue LED ring light |
| android interior | titanium alloy skeletal structure, bundled fiber optic cables, micro hydraulic pistons, circuit boards |

**教训**：命名具体部件，指定材质、颜色、功能。

---

### 4. 技术参数创造质感

**我的版本**：
```
"8K photorealistic"
```

**正确版本**：
```
Shot on ARRI Alexa Mini LF cinema camera with Cooke S7 100mm
portrait lens at T2.8, shallow depth of field, 4K cinema resolution,
RAW format, cinematic color grading with teal and orange color science
```

**教训**：相机型号、镜头参数、色彩科学这些技术细节直接影响AI生成的质感。

---

### 5. 三点布光的重要性

**我的版本**：
```
"soft even lighting"
```

**正确版本**：
```
LIGHTING: Dramatic three-point lighting setup with key light from
left front creating soft illumination, fill light from right, strong
rim backlight creating edge glow, subtle blue accent light on android
side emphasizing technological coldness
```

**教训**：专业灯光设置（key/fill/rim）能极大提升质感。

---

### 6. 负面提示词是关键

**我缺少的**：
没有或很简单的负面提示词

**正确做法**：
```
NEGATIVE PROMPT: cyberpunk, neon lights, blue LED, chrome, metallic
surface, industrial, holographic display, circuits visible, wires,
colorful, dystopian, dark moody, mask, face plate, panel, armor,
helmet, two separate heads
```

**教训**：详细列出**不要什么**，排除容易误触发的相关风格。

---

## 📚 我们如何吸取这些经验

### 1. 创建了《提示词工程最佳实践指南》

文件：`PROMPT_ENGINEERING_BEST_PRACTICES.md`

**包含内容**：
- ✅ 8大核心原则
- ✅ 专业摄影参数库（相机、镜头、灯光）
- ✅ 不同主题的模板（人物、产品、场景）
- ✅ 工具特定技巧（MJ/SD/DALL-E）
- ✅ 实战案例分析
- ✅ 检查清单

### 2. 更新了 Prompt Generator Skill

文件：`.claude/skills/prompt-generator/skill.md`

**新增部分**：
- ✅ 专业级提示词模式
- ✅ 何时启用专业级模式的判断
- ✅ 专业级提示词结构模板
- ✅ 8大核心原则集成
- ✅ 工具选择建议

### 3. 建立了两种工作模式

**标准模式**（简单需求）：
```
用户："生成一个女性人物"
→ 调用 generator_engine.py
→ 使用 portrait_full 模板
→ 返回基础提示词
```

**专业级模式**（高质量需求）：
```
用户："生成西部世界风格的半人半机器人"
→ 识别专业级关键词（Westworld, cinematic）
→ 手动构建结构化提示词
→ 添加技术参数（相机、灯光、色彩）
→ 包含详细负面提示词
→ 解释各部分作用
```

---

## 🎓 实战检查清单

每次写高质量提示词前，检查：

### ✅ 结构检查
- [ ] 使用清晰分段标题（LEFT/RIGHT, LIGHTING, CAMERA等）
- [ ] 主题概述在最前
- [ ] 技术参数独立成段
- [ ] 负面提示词单独列出

### ✅ 描述检查
- [ ] 具体部件名称而非抽象（servo mechanisms vs "parts"）
- [ ] 材质明确（titanium alloy, polymer, ceramic）
- [ ] 颜色准确（white, blue, silver而非"colorful"）
- [ ] 质感描述（matte, glossy, textured）

### ✅ 技术参数检查
- [ ] 相机型号或类型
- [ ] 镜头焦距和光圈值
- [ ] 分辨率和格式
- [ ] 色彩科学/调色方案

### ✅ 灯光检查
- [ ] 主光位置和性质（key light）
- [ ] 补光/轮廓光（fill/rim）
- [ ] 氛围光或强调光
- [ ] 对比度/色温说明

### ✅ 语言检查
- [ ] 拥抱专业术语（split face, three-point lighting）
- [ ] 使用肯定句而非否定句
- [ ] 具体化 > 抽象化
- [ ] 权重语法（SD）：(keyword:1.4)

### ✅ 负面提示词检查
- [ ] 排除易混淆风格（要Westworld排除cyberpunk）
- [ ] 排除常见错误（bad anatomy, distorted）
- [ ] 排除不要的元素（mask, panel, two heads）

---

## 📊 前后对比

### 案例：西部世界仿生人

**我的初版**（500字，失败）：
```
portrait of android, unified face not split, skin removed on one
side, white mechanical structure, realistic skin other side, one
face not two, seamless transition, soft lighting, 8K photorealistic
```

**正确版本**（1500字，成功）：
```
Cinematic split-face portrait, PERFECT VERTICAL SPLIT

LEFT HALF - HUMAN SIDE: Photorealistic human face, flawless
natural skin with visible pores and subsurface scattering, warm
flesh tones, natural brown eye with intricate iris detail...

RIGHT HALF - ANDROID SIDE: Exposed mechanical interior, white
synthetic polymer framework, complex servo mechanisms at jaw and
cheekbone, advanced camera lens system with blue LED ring, titanium
alloy skeletal structure, bundled fiber optic cables...

LIGHTING: Three-point lighting, key from left, fill from right,
rim backlight, blue accent on mechanical side...

CAMERA: Shot on ARRI Alexa Mini LF, Cooke S7 100mm T2.8, 4K RAW...

STYLE: Westworld HBO aesthetic, philosophical sci-fi...

(photorealistic skin:1.4), (mechanical precision:1.3)

NEGATIVE: cyberpunk, neon, chrome, mask, two heads, panel...
```

**关键差异**：
- 长度：3倍
- 结构：无结构 → 清晰分段
- 细节：抽象 → 具体部件
- 技术：无 → 完整相机/灯光参数
- 负面：无 → 详细排除项

---

## 🚀 如何应用到未来

### 遇到新的复杂需求时

1. **判断是否需要专业级模式**
   - 关键词：cinematic, professional, high-end, 具体作品名
   - 复杂度：特殊构图、多元素融合

2. **参考最佳实践文档**
   - 查看 `PROMPT_ENGINEERING_BEST_PRACTICES.md`
   - 使用对应主题的模板
   - 应用检查清单

3. **构建结构化提示词**
   - 清晰分段
   - 具体细节
   - 技术参数
   - 负面提示词

4. **测试和迭代**
   - 生成初版
   - 分析问题
   - 调整参数
   - 记录有效组合

---

## 💎 金句总结

1. **"拥抱术语，精确定义"** - 用专业词汇，然后详细描述
2. **"结构化胜过长度"** - 清晰分段比堆砌更有效
3. **"具体化战胜抽象"** - "titanium alloy cheekbone"比"metal"好
4. **"技术参数创造质感"** - 相机型号和镜头很重要
5. **"否定词是陷阱"** - "not split"让AI困惑，"PERFECT SPLIT"才清晰

---

## 📈 未来改进方向

### 短期（已完成）
- [x] 创建最佳实践文档
- [x] 更新Skill支持专业级模式
- [x] 建立检查清单

### 中期（计划中）
- [ ] 在 `templates.json` 中添加 `portrait_professional` 模板
- [ ] 创建专业参数库（相机/镜头/灯光预设）
- [ ] 建立案例库（成功/失败案例对比）

### 长期（愿景）
- [ ] 自动识别需求复杂度
- [ ] AI辅助优化提示词结构
- [ ] 社区分享优秀提示词

---

## 🎯 总结

这次"西部世界仿生人"案例教会了我们：

1. **不要害怕专业术语** - 它们是AI理解的钥匙
2. **结构比长度重要** - 清晰分段让AI更容易理解
3. **细节决定质量** - 具体的技术参数创造专业质感
4. **失败是最好的老师** - 从错误中总结系统化方法

现在我们有了：
- ✅ 完整的最佳实践文档
- ✅ 升级的Skill系统
- ✅ 标准+专业双模式
- ✅ 可复用的模板和检查清单

**下次遇到复杂需求，我们已经准备好了！** 🚀

---

**版本**: 1.0
**日期**: 2026-01-02
**基于实战总结**
