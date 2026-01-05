# 📊 完整类别扩展计划

**基于**: 架构决策 - 预定义框架 + 自动学习
**目标**: 建立完整的人像生成知识库

---

## 🎯 扩展原则

### 优先级评估标准

| 维度 | 权重 | 说明 |
|------|------|------|
| **人像相关性** | 40% | 与人像核心要素的关联度 |
| **使用频率** | 30% | 在prompt中出现的频率 |
| **复用性** | 20% | 跨场景、风格的通用性 |
| **可标准化** | 10% | 是否容易定义和识别 |

### 分批实施策略

```
批次1 (立即) - 核心人像扩展
├── poses (姿势)
├── expressions (表情)
└── clothing_styles (服装风格)

批次2 (1周后) - 视觉表现扩展
├── gestures (手势)
├── gaze_directions (视线方向)
└── head_positions (头部位置)

批次3 (2周后) - 场景元素
├── backgrounds (背景)
├── lighting_conditions (光线条件)
└── atmosphere (氛围)

批次4 (未来) - 摄影技术
├── camera_angles (相机角度)
├── shot_types (镜头类型)
└── depth_of_field (景深)
```

---

## 📋 批次1: 核心人像扩展（立即实施）⭐

### 1. poses (姿势) - 优先级：🔴 最高

**为什么重要**:
- ✅ 人像核心要素（与表情同等重要）
- ✅ 高复用性（任何人像都有姿势）
- ✅ 易于识别和分类
- ✅ 用户prompt中频繁出现

**种子样例（4个）**:
```json
{
  "poses": {
    "power_stance": {
      "chinese_name": "力量站姿",
      "keywords": ["power stance", "wide stance", "feet apart"],
      "visual_features": {
        "legs": "feet shoulder-width or wider apart",
        "weight": "weight on back leg",
        "upper_body": "chest forward, shoulders back"
      },
      "ai_prompt_template": "standing in a confident power stance",
      "reusability_score": 8.5
    },

    "arms_crossed": {
      "chinese_name": "双臂交叉",
      "keywords": ["arms crossed", "crossed arms"],
      "visual_features": {
        "arms": "firmly crossed over chest",
        "posture": "upright, confident"
      },
      "ai_prompt_template": "arms firmly crossed over chest",
      "reusability_score": 9.0
    },

    "chin_raised": {
      "chinese_name": "昂首姿态",
      "keywords": ["chin up", "chin raised", "head tilted up"],
      "visual_features": {
        "head": "chin slightly raised",
        "gaze": "looking upward or straight ahead"
      },
      "ai_prompt_template": "chin slightly raised with confident gaze",
      "reusability_score": 8.0
    },

    "relaxed_standing": {
      "chinese_name": "放松站姿",
      "keywords": ["relaxed", "casual stance", "natural pose"],
      "visual_features": {
        "posture": "relaxed, natural",
        "weight": "shifted to one leg"
      },
      "ai_prompt_template": "standing in a relaxed, casual pose",
      "reusability_score": 9.5
    }
  }
}
```

**预期增长方向**:
- hands_on_hips (叉腰)
- leaning_against_wall (靠墙)
- sitting_cross_legged (盘腿坐)
- standing_straight (笔直站立)

---

### 2. expressions (表情) - 优先级：🔴 最高

**为什么重要**:
- ✅ 人像灵魂（最影响情感表达）
- ✅ 极高复用性
- ✅ 用户最关注的要素之一
- ✅ 与makeup_styles, eye_types配合使用

**种子样例（4个）**:
```json
{
  "expressions": {
    "confident_smirk": {
      "chinese_name": "自信微笑",
      "keywords": ["smirk", "confident", "sassy", "smug"],
      "visual_features": {
        "mouth": "subtle smirk",
        "eyes": "slightly narrowed",
        "overall_mood": "confident, sassy"
      },
      "ai_prompt_template": "a confident, sassy expression with a subtle smirk",
      "emotional_tone": "positive, confident",
      "reusability_score": 9.0
    },

    "playful_smile": {
      "chinese_name": "俏皮笑容",
      "keywords": ["playful", "fun", "lighthearted", "cheeky"],
      "visual_features": {
        "mouth": "bright smile, playful grin",
        "eyes": "sparkling, bright"
      },
      "ai_prompt_template": "playful, lighthearted smile",
      "emotional_tone": "positive, energetic",
      "reusability_score": 9.5
    },

    "serene_calm": {
      "chinese_name": "宁静平和",
      "keywords": ["serene", "calm", "peaceful", "tranquil"],
      "visual_features": {
        "face": "relaxed, no tension",
        "eyes": "soft, relaxed gaze"
      },
      "ai_prompt_template": "serene, calm expression",
      "emotional_tone": "neutral-positive, peaceful",
      "reusability_score": 9.0
    },

    "gentle_smile": {
      "chinese_name": "温柔微笑",
      "keywords": ["gentle", "soft smile", "warm", "kind"],
      "visual_features": {
        "mouth": "soft, gentle smile",
        "eyes": "warm, kind eyes"
      },
      "ai_prompt_template": "gentle, warm smile with kind eyes",
      "emotional_tone": "positive, warm",
      "reusability_score": 9.5
    }
  }
}
```

**预期增长方向**:
- joyful_laughing (欢乐大笑)
- mysterious_enigmatic (神秘莫测)
- serious_focused (严肃专注)
- dreamy_thoughtful (梦幻沉思)

---

### 3. clothing_styles (服装风格) - 优先级：🟡 高

**为什么重要**:
- ✅ 人像重要元素
- ✅ 高使用频率
- ✅ 易于标准化
- ✅ 影响整体风格

**种子样例（4个）**:
```json
{
  "clothing_styles": {
    "casual_modern": {
      "chinese_name": "现代休闲装",
      "keywords": ["casual", "modern", "comfortable", "everyday"],
      "visual_features": {
        "style": "casual, comfortable, contemporary",
        "fit": "relaxed but well-fitted"
      },
      "ai_prompt_template": "wearing modern casual outfit",
      "occasion": "everyday, casual",
      "reusability_score": 9.5
    },

    "elegant_formal": {
      "chinese_name": "优雅正装",
      "keywords": ["elegant", "formal", "sophisticated", "dressy"],
      "visual_features": {
        "style": "elegant, formal, refined",
        "fit": "tailored, fitted"
      },
      "ai_prompt_template": "wearing elegant formal attire",
      "occasion": "formal, business",
      "reusability_score": 8.5
    },

    "traditional_cultural": {
      "chinese_name": "传统文化装",
      "keywords": ["traditional", "cultural", "ethnic", "heritage"],
      "visual_features": {
        "style": "traditional, cultural-specific",
        "details": "authentic cultural elements"
      },
      "ai_prompt_template": "wearing traditional cultural attire",
      "occasion": "cultural, ceremonial",
      "reusability_score": 7.0
    },

    "sporty_athletic": {
      "chinese_name": "运动休闲装",
      "keywords": ["sporty", "athletic", "activewear", "fitness"],
      "visual_features": {
        "style": "sporty, athletic, functional",
        "material": "breathable, performance fabrics"
      },
      "ai_prompt_template": "wearing sporty athletic outfit",
      "occasion": "sports, fitness",
      "reusability_score": 8.0
    }
  }
}
```

**预期增长方向**:
- bohemian_artistic (波西米亚艺术装)
- business_professional (商务职业装)
- vintage_retro (复古怀旧装)
- streetwear_urban (街头潮流装)

---

## 📋 批次2: 视觉表现扩展（1周后）

### 4. gestures (手势) - 优先级：🟡 高

**为什么重要**:
- ✅ 增强表现力
- ✅ 与poses互补
- ✅ 常见于人像摄影

**种子样例（3个）**:
```json
{
  "gestures": {
    "peace_sign": {
      "chinese_name": "比V手势",
      "keywords": ["peace sign", "V sign", "victory"],
      "visual_features": {
        "hand": "index and middle fingers raised",
        "meaning": "peace, victory, playful"
      },
      "ai_prompt_template": "making a peace sign with hand",
      "reusability_score": 8.0
    },

    "hand_on_face": {
      "chinese_name": "手托脸",
      "keywords": ["hand on face", "hand to cheek", "thoughtful"],
      "visual_features": {
        "hand": "gently touching face or cheek",
        "mood": "thoughtful, contemplative"
      },
      "ai_prompt_template": "hand gently touching face",
      "reusability_score": 9.0
    },

    "pointing_gesture": {
      "chinese_name": "指向手势",
      "keywords": ["pointing", "finger pointing", "directing"],
      "visual_features": {
        "hand": "index finger extended, pointing",
        "direction": "at camera, upward, or sideways"
      },
      "ai_prompt_template": "pointing with finger",
      "reusability_score": 7.5
    }
  }
}
```

---

### 5. gaze_directions (视线方向) - 优先级：🟡 中高

**为什么重要**:
- ✅ 影响情感连接
- ✅ 摄影重要技巧
- ✅ 易于定义

**种子样例（3个）**:
```json
{
  "gaze_directions": {
    "looking_at_camera": {
      "chinese_name": "直视镜头",
      "keywords": ["looking at camera", "eye contact", "direct gaze"],
      "visual_features": {
        "eyes": "looking directly at viewer",
        "impact": "strong connection, engaging"
      },
      "ai_prompt_template": "looking directly at camera",
      "reusability_score": 9.5
    },

    "looking_away": {
      "chinese_name": "目光偏离",
      "keywords": ["looking away", "gazing off", "distant look"],
      "visual_features": {
        "eyes": "looking to the side or distance",
        "mood": "contemplative, mysterious"
      },
      "ai_prompt_template": "looking away from camera",
      "reusability_score": 9.0
    },

    "looking_down": {
      "chinese_name": "低头凝视",
      "keywords": ["looking down", "downward gaze", "shy"],
      "visual_features": {
        "eyes": "looking downward",
        "mood": "shy, thoughtful, demure"
      },
      "ai_prompt_template": "looking down with a gentle gaze",
      "reusability_score": 8.5
    }
  }
}
```

---

### 6. head_positions (头部位置) - 优先级：🟢 中

**为什么重要**:
- ✅ 影响整体构图
- ✅ 与表情、姿势配合
- ✅ 摄影常用技巧

**种子样例（3个）**:
```json
{
  "head_positions": {
    "head_tilt": {
      "chinese_name": "头部倾斜",
      "keywords": ["head tilt", "tilted head", "cocked head"],
      "visual_features": {
        "angle": "head tilted to one side",
        "effect": "playful, curious, engaging"
      },
      "ai_prompt_template": "head tilted slightly to the side",
      "reusability_score": 9.0
    },

    "profile_view": {
      "chinese_name": "侧面视角",
      "keywords": ["profile", "side view", "turned head"],
      "visual_features": {
        "angle": "head turned to show profile",
        "effect": "elegant, dramatic"
      },
      "ai_prompt_template": "head turned in profile view",
      "reusability_score": 8.0
    },

    "three_quarter_view": {
      "chinese_name": "四分之三视角",
      "keywords": ["three quarter", "partial turn", "angled"],
      "visual_features": {
        "angle": "head turned about 45 degrees",
        "effect": "natural, flattering"
      },
      "ai_prompt_template": "head in three-quarter view",
      "reusability_score": 9.5
    }
  }
}
```

---

## 📋 批次3: 场景元素（2周后）

### 7. backgrounds (背景) - 优先级：🟢 中

**为什么重要**:
- ✅ 设定场景氛围
- ✅ 高使用频率
- ✅ 可标准化

**种子样例（3个）**:
```json
{
  "backgrounds": {
    "seamless_studio": {
      "chinese_name": "无缝影棚背景",
      "keywords": ["seamless", "studio backdrop", "solid color"],
      "visual_features": {
        "type": "seamless studio backdrop",
        "style": "clean, professional"
      },
      "ai_prompt_template": "seamless studio backdrop",
      "reusability_score": 9.0
    },

    "natural_outdoor": {
      "chinese_name": "自然户外背景",
      "keywords": ["outdoor", "natural", "environment", "landscape"],
      "visual_features": {
        "type": "natural outdoor setting",
        "elements": "trees, sky, nature"
      },
      "ai_prompt_template": "natural outdoor background",
      "reusability_score": 8.5
    },

    "urban_street": {
      "chinese_name": "城市街道背景",
      "keywords": ["urban", "street", "city", "buildings"],
      "visual_features": {
        "type": "urban street setting",
        "elements": "buildings, pavement, urban architecture"
      },
      "ai_prompt_template": "urban street background",
      "reusability_score": 8.0
    }
  }
}
```

---

### 8. lighting_conditions (光线条件) - 优先级：🟢 中

**为什么重要**:
- ✅ 影响整体质感
- ✅ 摄影核心要素
- ✅ 可标准化

**种子样例（3个）**:
```json
{
  "lighting_conditions": {
    "soft_natural": {
      "chinese_name": "柔和自然光",
      "keywords": ["soft light", "natural", "diffused", "gentle"],
      "visual_features": {
        "quality": "soft, diffused",
        "source": "natural or window light",
        "shadows": "soft, gradual"
      },
      "ai_prompt_template": "soft natural lighting",
      "reusability_score": 9.5
    },

    "studio_commercial": {
      "chinese_name": "商业影棚灯光",
      "keywords": ["studio lighting", "commercial", "crisp", "professional"],
      "visual_features": {
        "quality": "crisp, clean, professional",
        "source": "studio lights",
        "effect": "high detail, polished"
      },
      "ai_prompt_template": "crisp commercial studio lighting",
      "reusability_score": 9.0
    },

    "golden_hour": {
      "chinese_name": "黄金时刻光线",
      "keywords": ["golden hour", "warm light", "sunset", "sunrise"],
      "visual_features": {
        "quality": "warm, golden",
        "time": "sunset or sunrise",
        "effect": "romantic, warm glow"
      },
      "ai_prompt_template": "golden hour lighting with warm glow",
      "reusability_score": 8.5
    }
  }
}
```

---

### 9. atmosphere (氛围) - 优先级：🟢 中低

**为什么重要**:
- ✅ 设定情感基调
- ✅ 影响整体风格
- ✅ 可以与其他元素组合

**种子样例（3个）**:
```json
{
  "atmosphere": {
    "festive_playful": {
      "chinese_name": "节日俏皮氛围",
      "keywords": ["festive", "playful", "fun", "celebratory"],
      "visual_features": {
        "mood": "festive, playful, lighthearted",
        "energy": "upbeat, fun"
      },
      "ai_prompt_template": "festive, playful atmosphere",
      "reusability_score": 7.5
    },

    "dramatic_moody": {
      "chinese_name": "戏剧性氛围",
      "keywords": ["dramatic", "moody", "intense", "atmospheric"],
      "visual_features": {
        "mood": "dramatic, intense",
        "lighting": "often dark or high contrast"
      },
      "ai_prompt_template": "dramatic, moody atmosphere",
      "reusability_score": 8.0
    },

    "ethereal_dreamy": {
      "chinese_name": "空灵梦幻氛围",
      "keywords": ["ethereal", "dreamy", "soft", "mystical"],
      "visual_features": {
        "mood": "dreamy, soft, otherworldly",
        "effect": "soft focus, hazy"
      },
      "ai_prompt_template": "ethereal, dreamy atmosphere",
      "reusability_score": 8.5
    }
  }
}
```

---

## 📋 批次4: 摄影技术（未来/可选）

### 10. camera_angles (相机角度) - 优先级：🟢 低

**为什么推迟**:
- 技术性强，用户可能直接描述
- 容易模板化，不需要学习
- 数量有限，全部预定义即可

**建议处理方式**: 使用固定模板，不需要学习系统

```python
CAMERA_ANGLES = {
    "low_angle": "low-angle shot from below",
    "high_angle": "high-angle shot from above",
    "eye_level": "eye-level shot",
    "dutch_angle": "dutch angle, tilted shot"
}
```

---

### 11. shot_types (镜头类型) - 优先级：🟢 低

**建议处理方式**: 固定模板

```python
SHOT_TYPES = {
    "close_up": "close-up shot of face",
    "medium_shot": "medium shot, waist up",
    "full_body": "full body shot",
    "portrait": "portrait shot, shoulders and head"
}
```

---

### 12. depth_of_field (景深) - 优先级：🟢 低

**建议处理方式**: 固定模板

```python
DEPTH_OF_FIELD = {
    "shallow": "shallow depth of field, blurred background",
    "deep": "deep depth of field, sharp throughout",
    "bokeh": "beautiful bokeh effect in background"
}
```

---

## 🎯 推荐实施顺序

### 立即实施（今天）✅

```bash
# 批次1: 核心人像扩展
python3 run_full_expansion.py

# 添加的类别：
# - poses (4个种子)
# - expressions (4个种子)
# - clothing_styles (4个种子)
```

### 1周后（如果需要）

手动添加批次2的3个类别：
- gestures
- gaze_directions
- head_positions

### 2周后（根据使用情况）

评估是否需要批次3：
- backgrounds
- lighting_conditions
- atmosphere

### 长期（3个月后）

根据数据分析决定是否需要批次4的摄影技术类别

---

## 📊 类别优先级总结

| 类别 | 优先级 | 批次 | 理由 |
|------|--------|------|------|
| poses | 🔴 最高 | 1 | 人像核心，高复用 |
| expressions | 🔴 最高 | 1 | 人像灵魂，高复用 |
| clothing_styles | 🟡 高 | 1 | 常用，易标准化 |
| gestures | 🟡 高 | 2 | 增强表现力 |
| gaze_directions | 🟡 中高 | 2 | 摄影重要技巧 |
| head_positions | 🟢 中 | 2 | 构图辅助 |
| backgrounds | 🟢 中 | 3 | 场景设定 |
| lighting_conditions | 🟢 中 | 3 | 影响质感 |
| atmosphere | 🟢 中低 | 3 | 情感基调 |
| camera_angles | 🟢 低 | 4/模板 | 技术参数 |
| shot_types | 🟢 低 | 4/模板 | 技术参数 |
| depth_of_field | 🟢 低 | 4/模板 | 技术参数 |

---

## ✅ 下一步行动

1. **阅读并批准**本计划
2. **运行批次1扩展**：`python3 run_full_expansion.py`
3. **测试系统**：`python3 test_scan_new_prompt.py`
4. **开始使用**：扫描你的prompts，积累数据
5. **1周后评估**：是否需要批次2

---

**最小化启动**：只需批次1（3个类别，12个种子）
**最大化覆盖**：全部12个类别，但分批实施
**推荐路径**：先批次1，根据使用情况再决定后续
