# 跨Prompt相似推荐系统设计

**版本**: v1.0
**生成日期**: 2026-01-01

---

## 🎯 系统目标

当用户查看某个提示词时，自动推荐"相关"或"相似"的其他提示词，帮助用户：
- 发现同类型的替代方案
- 学习技术演进路径
- 对比不同风格的实现
- 找到设备/成本的替代选项

---

## 📐 推荐算法架构

### 核心推荐维度 (6个)

```
相似度计算 = 加权求和(
  流派相似度 × 30% +
  设备相似度 × 25% +
  主题相似度 × 20% +
  技术难度相似度 × 10% +
  参数复杂度相似度 × 10% +
  质量评分接近度 × 5%
)
```

---

## 1️⃣ 流派相似度 (Photography Genre Similarity)

### 相似矩阵

```python
genre_similarity_matrix = {
    # 真实摄影系 (高度相关)
    "analog_film": {
        "digital_commercial": 0.6,  # 都是Cosplay，但设备不同
        "cinematic_narrative": 0.7,  # 都是真人拍摄，但预算不同
        "portrait_beauty": 0.5,     # 都是人像，但主题不同
        "editorial_macro": 0.3,     # 都是高端摄影，但对象不同
        "studio_product": 0.2
    },

    "digital_commercial": {
        "analog_film": 0.6,
        "cinematic_narrative": 0.8,  # 都是Cosplay商业应用
        "portrait_beauty": 0.4,
        "studio_product": 0.5       # 都是商业摄影
    },

    "cinematic_narrative": {
        "analog_film": 0.7,
        "digital_commercial": 0.8,
        "conceptual_art": 0.4       # 都需要高预算
    },

    "studio_product": {
        "editorial_macro": 0.7,      # 都是产品摄影
        "digital_commercial": 0.5
    },

    "editorial_macro": {
        "studio_product": 0.7,
        "conceptual_art": 0.4
    },

    "conceptual_art": {
        "cinematic_narrative": 0.4,
        "editorial_macro": 0.4,
        "portrait_beauty": 0.3
    },

    "portrait_beauty": {
        "analog_film": 0.5,
        "digital_commercial": 0.4,
        "conceptual_art": 0.3
    },

    # 数字创作系 (中度相关)
    "hybrid_illustration": {
        "3d_render": 0.6,           # 都是数字创作
        "collage_composite": 0.4
    },

    "3d_render": {
        "hybrid_illustration": 0.6,
        "collage_composite": 0.5
    },

    # 后期合成系 (中度相关)
    "collage_composite": {
        "3d_render": 0.5,
        "hybrid_illustration": 0.4,
        "studio_product": 0.3       # 都需要多张素材
    }
}
```

---

## 2️⃣ 设备相似度 (Equipment Similarity)

### 相同设备 = 1.0分
```json
{
  "canon_eos_r5": [16, 18],  // 完全相同设备
  "hasselblad_medium_format": [17],
  "phase_one": [1, 7]
}
```

### 设备等级相似度

```python
equipment_tier_similarity = {
    # 高端中画幅系列
    "phase_one": {
        "hasselblad_medium_format": 0.8,  // 都是中画幅
        "canon_eos_r5": 0.5                // 价格相近但格式不同
    },

    # 电影级全画幅
    "canon_eos_r5": {
        "phase_one": 0.5,
        "hasselblad_medium_format": 0.4,
        "full_frame_digital": 0.7          // 通用全画幅
    },

    # 胶片中画幅
    "hasselblad_medium_format": {
        "phase_one": 0.8,                  // 都是中画幅
        "canon_eos_r5": 0.4,
        "analog_35mm": 0.6                 // 都是胶片
    }
}
```

---

## 3️⃣ 主题相似度 (Theme Similarity)

### 主题分类

```python
theme_categories = {
    "cosplay_reallife": [11, 17, 18],      // Cosplay真人化
    "product_photography": [1, 7, 16],     // 产品摄影
    "human_portrait": [5, 10],             // 人像摄影
    "artistic_concept": [14, 15],          // 艺术概念
    "composite_design": [9, 12, 13]        // 合成设计
}

# 同主题 = 0.9分
# 相关主题 = 0.5-0.7分
# 不相关 = 0.1分
```

### 主题相关矩阵

```python
theme_similarity = {
    "cosplay_reallife": {
        "human_portrait": 0.6,     // 都是人像
        "artistic_concept": 0.3
    },

    "product_photography": {
        "artistic_concept": 0.5,   // 产品艺术摄影
        "composite_design": 0.4
    },

    "human_portrait": {
        "cosplay_reallife": 0.6,
        "artistic_concept": 0.4
    }
}
```

---

## 4️⃣ 技术难度相似度 (Technical Difficulty)

### 难度分级 (1-5级)

```python
difficulty_scores = {
    # Level 1: 单图静态摄影
    1: [1, 5, 10],                     // 基础摄影

    # Level 2: 系统化/参数化
    2: [7, 16],                        // 系列化摄影

    # Level 3: 胶片/特殊设备
    3: [17],                           // 胶片艺术

    # Level 4: 实景搭建/高预算
    4: [18, 14],                       // 电影级/概念艺术

    # Level 5: 复杂合成/特效
    5: [9, 12, 13, 15]                 // 拼贴/3D渲染/插画
}

# 难度相差0级 = 1.0分
# 相差1级 = 0.7分
# 相差2级 = 0.4分
# 相差3+级 = 0.1分
```

---

## 5️⃣ 参数复杂度相似度 (Parameter Complexity)

### 参数数量分档

```python
parameter_tiers = {
    "simple": {        # 0-15参数
        "prompts": [5, 12, 14],
        "score_range": (0, 15)
    },
    "moderate": {      # 16-20参数
        "prompts": [13, 15],
        "score_range": (16, 20)
    },
    "complex": {       # 21-30参数
        "prompts": [6, 7],
        "score_range": (21, 30)
    },
    "extreme": {       # 30+参数
        "prompts": [16],
        "score_range": (30, 100)
    }
}

# 同档位 = 0.8分
# 相邻档位 = 0.5分
# 跨2档 = 0.2分
```

---

## 6️⃣ 质量评分接近度 (Quality Score Proximity)

```python
def quality_similarity(score_a, score_b):
    diff = abs(score_a - score_b)
    if diff <= 0.5:
        return 1.0      # 几乎相同质量
    elif diff <= 1.0:
        return 0.8      # 略有差异
    elif diff <= 1.5:
        return 0.5      # 明显差异
    else:
        return 0.2      # 质量差距大
```

---

## 🔍 推荐类型 (5种)

### Type 1: 同流派推荐 (Same Genre)
**触发条件**: 用户查看某摄影流派的提示词
**推荐逻辑**: 推荐同流派的其他提示词

**示例**:
```
用户查看: Prompt #17 (Jinx - analog_film)

推荐:
  → 暂无其他胶片流派提示词
  → 建议: "如需更多胶片Cosplay案例，可考虑数码商业(#11)或电影级(#18)"
```

---

### Type 2: 设备相同推荐 (Same Equipment)
**触发条件**: 用户查看使用特定设备的提示词
**推荐逻辑**: 推荐使用同款设备的其他提示词

**示例**:
```
用户查看: Prompt #16 (Trek自行车 - Canon EOS R5)

推荐:
  → Prompt #18 (Peach电影): 同用Canon EOS R5，但风格是电影叙事

推荐理由:
  "同样使用Canon EOS R5，#18展示了如何用同款设备拍摄电影级Cosplay实景"
```

---

### Type 3: 主题相关推荐 (Related Theme)
**触发条件**: 用户查看某主题的提示词
**推荐逻辑**: 推荐同主题不同风格的提示词

**示例**:
```
用户查看: Prompt #17 (Jinx Cosplay - 胶片艺术)

推荐:
  → Prompt #11 (Saber Cosplay): 同为Cosplay，数码商业风格
  → Prompt #18 (Peach Cosplay): 同为Cosplay，电影叙事风格

推荐理由:
  "对比三种Cosplay摄影流派：
   - 胶片艺术(#17): 温暖质感，社交媒体高互动
   - 数码商业(#11): 8K清晰，特效丰富
   - 电影叙事(#18): 实景道具，高预算"
```

---

### Type 4: 技术演进推荐 (Skill Progression)
**触发条件**: 用户查看某难度等级的提示词
**推荐逻辑**: 推荐相邻难度的提示词（学习路径）

**示例**:
```
用户查看: Prompt #5 (人物肖像 - Level 1 基础)

推荐升级路径:
  → Prompt #10 (中国美女细节 - Level 1+): 深度优化，9层细节
  → Prompt #17 (Jinx胶片 - Level 3): 进阶胶片拍摄
  → Prompt #18 (Peach电影 - Level 4): 电影级高阶

学习路径:
  基础人像(#5) → 细节优化(#10) → 胶片艺术(#17) → 电影级(#18)
```

---

### Type 5: 成本替代推荐 (Cost Alternative)
**触发条件**: 用户查看高成本设备的提示词
**推荐逻辑**: 推荐成本更低但效果相近的替代方案

**示例**:
```
用户查看: Prompt #1 (Phase One - 租赁¥1500-2500/天)

成本替代方案:
  → Prompt #16 (Canon EOS R5 - 租赁¥800-1200/天)
     - 成本降低50%
     - 分辨率从100MP降至45MP
     - 适合产品摄影但非极致微距

  → Prompt #5 (Canon全画幅 - 租赁¥300-500/天)
     - 成本降低80%
     - 适合人像，不适合产品微距
```

---

## 💻 推荐算法实现

### 伪代码

```python
def recommend_prompts(current_prompt_id, top_k=5):
    """
    推荐与current_prompt相关的其他提示词

    Args:
        current_prompt_id: 当前查看的提示词ID
        top_k: 返回前K个推荐

    Returns:
        List of (prompt_id, similarity_score, reason)
    """

    current = load_prompt(current_prompt_id)
    all_prompts = load_all_prompts(exclude=current_prompt_id)

    recommendations = []

    for candidate in all_prompts:
        # 1. 流派相似度 (30%)
        genre_sim = calculate_genre_similarity(
            current.photography_genre,
            candidate.photography_genre
        ) * 0.30

        # 2. 设备相似度 (25%)
        equipment_sim = calculate_equipment_similarity(
            current.camera_equipment,
            candidate.camera_equipment
        ) * 0.25

        # 3. 主题相似度 (20%)
        theme_sim = calculate_theme_similarity(
            current.theme,
            candidate.theme
        ) * 0.20

        # 4. 难度相似度 (10%)
        difficulty_sim = calculate_difficulty_similarity(
            current.difficulty_level,
            candidate.difficulty_level
        ) * 0.10

        # 5. 参数复杂度相似度 (10%)
        param_sim = calculate_parameter_similarity(
            current.total_parameters,
            candidate.total_parameters
        ) * 0.10

        # 6. 质量接近度 (5%)
        quality_sim = calculate_quality_similarity(
            current.quality_score,
            candidate.quality_score
        ) * 0.05

        # 总分
        total_score = (
            genre_sim +
            equipment_sim +
            theme_sim +
            difficulty_sim +
            param_sim +
            quality_sim
        )

        # 生成推荐理由
        reason = generate_reason(
            current, candidate,
            genre_sim, equipment_sim, theme_sim
        )

        recommendations.append({
            "prompt_id": candidate.id,
            "score": total_score,
            "reason": reason,
            "breakdown": {
                "genre": genre_sim,
                "equipment": equipment_sim,
                "theme": theme_sim,
                "difficulty": difficulty_sim,
                "parameters": param_sim,
                "quality": quality_sim
            }
        })

    # 按总分排序，返回Top K
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:top_k]
```

---

## 📋 推荐理由生成模板

```python
def generate_reason(current, candidate, genre_sim, equipment_sim, theme_sim):
    """生成人性化的推荐理由"""

    reasons = []

    # 优先维度：流派
    if genre_sim >= 0.25:  # 流派权重30%，得分>=25%说明流派相关
        if current.photography_genre == candidate.photography_genre:
            reasons.append(f"同为{genre_names[current.photography_genre]}风格")
        else:
            reasons.append(
                f"从{genre_names[current.photography_genre]}"
                f"到{genre_names[candidate.photography_genre]}的风格演变"
            )

    # 次要维度：设备
    if equipment_sim >= 0.20:  # 设备权重25%
        if current.camera == candidate.camera:
            reasons.append(f"同用{current.camera}设备")
        else:
            reasons.append(
                f"设备升级：{current.camera} → {candidate.camera}"
            )

    # 第三维度：主题
    if theme_sim >= 0.15:  # 主题权重20%
        if current.theme_category == candidate.theme_category:
            reasons.append(f"同属{current.theme_category}类别")
        else:
            reasons.append(f"相关主题：{candidate.theme_category}")

    # 组合理由
    if len(reasons) == 0:
        return "技术难度相近，可作参考"
    elif len(reasons) == 1:
        return reasons[0]
    else:
        return " + ".join(reasons)
```

---

## 📊 实际推荐示例

### 示例1: 查看 Prompt #17 (Jinx胶片Cosplay)

```json
{
  "current_prompt": {
    "id": 17,
    "title": "Jinx挑逗Cosplay",
    "genre": "analog_film",
    "equipment": "Hasselblad + Kodak Portra 400",
    "theme": "Cosplay真人化",
    "difficulty": 3,
    "quality_score": 9.5
  },

  "recommendations": [
    {
      "rank": 1,
      "prompt_id": 18,
      "title": "Peach电影实拍",
      "score": 0.72,
      "reason": "同为Cosplay真人化 + 风格从胶片艺术到电影叙事的演进",
      "breakdown": {
        "genre": 0.21,      // 0.7 × 30% = 21%
        "equipment": 0.10,  // 0.4 × 25% = 10%
        "theme": 0.18,      // 0.9 × 20% = 18%
        "difficulty": 0.07, // 0.7 × 10% = 7%
        "parameters": 0.10, // 相近
        "quality": 0.05     // 完全相同
      },
      "insights": "如需电影级实景拍摄效果，可参考#18的实体道具搭建方案"
    },

    {
      "rank": 2,
      "prompt_id": 11,
      "title": "Saber真人化",
      "score": 0.68,
      "reason": "同为Cosplay真人化 + 设备从胶片到数码的对比",
      "breakdown": {
        "genre": 0.18,      // 0.6 × 30% = 18%
        "equipment": 0.05,  // 完全不同
        "theme": 0.18,      // 0.9 × 20% = 18%
        "difficulty": 0.10, // 难度相同
        "parameters": 0.12,
        "quality": 0.05
      },
      "insights": "8K数码摄影 vs 胶片美学的风格对比，成本降低40%"
    },

    {
      "rank": 3,
      "prompt_id": 5,
      "title": "人物肖像模板",
      "score": 0.45,
      "reason": "同为人像摄影 + 技术难度降级（学习基础）",
      "breakdown": {
        "genre": 0.15,      // portrait_beauty vs analog_film
        "equipment": 0.12,  // Canon vs Hasselblad
        "theme": 0.12,      // 人像相关
        "difficulty": 0.04, // 难度差2级
        "parameters": 0.01,
        "quality": 0.01
      },
      "insights": "如需学习人像摄影基础，先从#5的12参数系统入手"
    }
  ]
}
```

---

### 示例2: 查看 Prompt #16 (Trek自行车产品摄影)

```json
{
  "current_prompt": {
    "id": 16,
    "title": "Trek自行车系列",
    "genre": "studio_product",
    "equipment": "Canon EOS R5",
    "theme": "产品摄影",
    "difficulty": 2,
    "parameters": 35,
    "quality_score": 10.0
  },

  "recommendations": [
    {
      "rank": 1,
      "prompt_id": 18,
      "title": "Peach电影实拍",
      "score": 0.58,
      "reason": "同用Canon EOS R5设备 + 技术难度升级",
      "breakdown": {
        "equipment": 0.25,  // 完全相同设备！
        "genre": 0.05,
        "theme": 0.04,
        "difficulty": 0.10,
        "parameters": 0.09,
        "quality": 0.05
      },
      "insights": "同款设备的电影级应用，展示Canon R5的视频性能上限"
    },

    {
      "rank": 2,
      "prompt_id": 1,
      "title": "Street Fighter游戏手册",
      "score": 0.55,
      "reason": "同为产品摄影 + 设备升级到Phase One中画幅",
      "breakdown": {
        "genre": 0.21,      // editorial_macro vs studio_product
        "equipment": 0.12,  // 同为高端但格式不同
        "theme": 0.18,      // 都是产品
        "difficulty": 0.02,
        "parameters": 0.01,
        "quality": 0.01
      },
      "insights": "如需极致微距细节，Phase One中画幅提供100MP+分辨率（成本增加60%）"
    },

    {
      "rank": 3,
      "prompt_id": 7,
      "title": "游戏收藏品手册",
      "score": 0.52,
      "reason": "同为产品摄影 + 参数复杂度相近",
      "breakdown": {
        "genre": 0.21,
        "equipment": 0.12,
        "theme": 0.18,
        "difficulty": 0.00,  // 相同难度
        "parameters": 0.08,  // 25 vs 35参数
        "quality": 0.00
      },
      "insights": "25参数游戏收藏品系统，可作为系列化摄影的另一实现案例"
    }
  ]
}
```

---

## 🛠 CLI工具集成

```bash
# 查询推荐
$ prompt-tool recommend --id 17

📸 当前提示词: #17 Jinx挑逗Cosplay (analog_film)

🔍 为您推荐相关提示词:

[1] #18 Peach电影实拍 (相似度: 72%)
    └─ 理由: 同为Cosplay真人化 + 胶片→电影叙事演进
    └─ 设备: Hasselblad胶片 → Canon R5电影级
    └─ 成本: 相近(¥800-1200/天)

[2] #11 Saber真人化 (相似度: 68%)
    └─ 理由: 同为Cosplay真人化 + 胶片→数码对比
    └─ 设备: Hasselblad胶片 → 8K数码
    └─ 成本: 降低40%

[3] #5 人物肖像模板 (相似度: 45%)
    └─ 理由: 人像摄影基础学习路径
    └─ 难度: Level 3 → Level 1 降级
    └─ 适合: 先学基础再进阶胶片
```

---

## 📈 性能优化

### 预计算相似度矩阵
```python
# 系统启动时预计算18×18相似度矩阵
similarity_matrix = np.zeros((18, 18))

for i in range(18):
    for j in range(18):
        if i != j:
            similarity_matrix[i][j] = calculate_similarity(i, j)

# 保存为cache
save_cache("similarity_matrix.npy", similarity_matrix)
```

### 查询时间复杂度
- 预计算: O(1) - 直接查表
- 实时计算: O(N) - N=17 (排除当前)
- 推荐: 第一次100ms，后续<10ms

---

## 🎯 未来扩展

1. **机器学习优化**
   - 用户点击率反馈调整权重
   - 个性化推荐（基于历史）

2. **语义相似度**
   - 使用BERT嵌入计算提示词文本相似度
   - 捕捉隐含关联

3. **时间序列推荐**
   - 学习路径：从简单到复杂
   - 技术演进：从传统到前沿

---

**系统状态**: ✅ 设计完成 | **待实施**: CLI工具集成
