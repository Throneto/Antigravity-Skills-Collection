# 人像面部细节指南库

**版本**: v1.0
**创建日期**: 2026-01-01
**数据来源**: 从18个Prompts中提取的真实人像数据

---

## 📚 指南目录

### ✅ 已完成的指南

1. **[眼型分类指南](eye_types_guide.md)** (Eye Types Guide)
   - 4种眼型分类
   - 来源: Prompts #5, #11, #17, #18
   - 包含: 视觉特征、关键词、适合风格、使用建议、实际案例

### 🚧 计划中的指南

2. **脸型分类指南** (Face Shape Guide)
   - 2种脸型分类（oval_asian_refined, classical_soft_contour）
   - 来源: Prompts #5, #17, #18

3. **唇型分类指南** (Lip Types Guide)
   - 2种唇型分类（cherry_lips_cupids_bow, soft_pink_gloss）
   - 来源: Prompts #5, #18

4. **鼻型分类指南** (Nose Types Guide)
   - 2种鼻型分类（straight_classical_refined, small_straight_delicate）
   - 来源: Prompts #5, #18

5. **皮肤质感指南** (Skin Texture Guide)
   - 4种皮肤质感（porcelain, realistic, wet_dewy, warm_analog）
   - 来源: Prompts #5, #17, #18

6. **表情气质指南** (Expression Guide)
   - 3种表情分类（innocent_gentle, seductive, serene_adventurous）
   - 来源: Prompts #5, #17, #18

---

## 🎯 快速查询

### 按风格查询推荐五官组合

**清纯少女风格**:
- 眼型: 大眼杏仁眼 (large_expressive_almond)
- 唇型: 粉嫩光泽唇 (soft_pink_gloss)
- 鼻型: 小巧直鼻 (small_straight_delicate)
- 皮肤: 瓷肌无瑕 (porcelain_flawless_radiant)
- 表情: 清纯温柔眼神 (innocent_gentle_gaze)

**性感挑逗风格**:
- 眼型: 半闭诱惑眼 (half_lidded_seductive)
- 皮肤: 温润胶片肌 (warm_rich_analog_film)
- 表情: 挑逗顽皮 (seductive_mischievous)

**古典优雅风格**:
- 眼型: 大眼杏仁眼 (large_expressive_almond)
- 脸型: 柔和古典脸型 (classical_soft_contour)
- 唇型: 樱桃唇 (cherry_lips_cupids_bow)
- 鼻型: 古典精致直鼻 (straight_classical_refined)
- 皮肤: 瓷肌无瑕 (porcelain_flawless_radiant)
- 表情: 清纯温柔眼神 (innocent_gentle_gaze)

**真人化Cosplay风格**:
- 眼型: 大蓝眼 (large_blue_expressive) 或 动漫混合绿眼 (anime_hybrid_green)
- 脸型: 精致鹅蛋脸 (oval_asian_refined)
- 唇型: 粉嫩光泽唇 (soft_pink_gloss)
- 鼻型: 小巧直鼻 (small_straight_delicate)
- 皮肤: 真实质感肌 (realistic_textured_pores)
- 表情: 宁静冒险气质 (serene_adventurous)

---

## 🛠 CLI工具使用

### 列出所有五官类型
```bash
python3 prompt_tool.py facial --list-types
```

### 查询特定眼型
```bash
python3 prompt_tool.py facial --eye-type almond
```

### 查询特定皮肤质感
```bash
python3 prompt_tool.py facial --skin-texture porcelain
```

### 按风格推荐五官组合
```bash
python3 prompt_tool.py facial --style "清纯少女"
```

---

## 📊 数据统计

- **总分类数**: 17个
- **来源Prompts**: 5个 (#5, #10, #11, #17, #18)
- **平均复用性评分**: 9.1/10
- **覆盖率**: 约28% (5/18个Prompts)

---

## 🎓 学习路径

### 新手路径
1. 阅读 [眼型分类指南](eye_types_guide.md)
2. 学习"大眼杏仁眼"（万能眼型，复用性9.8/10）
3. 实践: 使用`large expressive eyes, almond eyes`关键词

### 进阶路径
1. 学习五官搭配（眼型+唇型+鼻型+皮肤）
2. 实践: 按风格组合五官特征
3. 优化: 根据摄影流派调整细节

### 高级路径
1. 学习混合风格（anime + realistic）
2. 实践: 动漫角色真人化
3. 创新: 创建自己的五官组合

---

## 🔗 相关资源

- **数据库文件**: `facial_features_library.json`
- **Skill系统**: `.claude/skills/prompt-extractor/skill.md` (Section 3.6)
- **CLI工具**: `prompt_tool.py`
- **提案文档**: `FACE_DETAILS_MODULE_PROPOSAL.md`
- **完成报告**: `FACIAL_FEATURES_EXTRACTION_REPORT.md`

---

## 📝 贡献指南

### 如何添加新的五官分类

1. 从新的Prompt中提取五官描述
2. 按照标准格式添加到 `facial_features_library.json`
3. 更新对应的指南markdown文档
4. 运行CLI工具验证

### 标准格式示例
```json
"new_eye_type": {
  "chinese_name": "中文名称",
  "classification_code": "分类代码",
  "visual_features": { "特征1": "描述", ... },
  "keywords": ["关键词1", "关键词2", ...],
  "mood_qualities": ["气质1", "气质2", ...],
  "suitable_styles": ["风格1", "风格2", ...],
  "prompts_using_this": [prompt_id],
  "example_description": "实际案例",
  "reusability_score": 9.0,
  "usage_recommendations": { ... }
}
```

---

**维护者**: Claude Code Skill System
**最后更新**: 2026-01-01
