# Prompt Extractor Skill - 完整使用指南

## 项目概述

这是一个Claude Skill，用于从大规模AI绘画提示词中自动提取可复用的模块化组件。

**核心价值**：
- 从1万条提示词中提炼出数百个精华模块
- 自动识别高质量模式和结构
- 构建个人专属的提示词模块库
- 像乐高积木一样组装新提示词

## 文件结构

```
.claude/skills/prompt-extractor/
├── skill.md                 # Skill核心逻辑（Claude执行入口）
├── preprocessor.py          # 数据预处理和聚类脚本
├── README.md                # 详细使用文档
├── QUICKSTART.md            # 5分钟快速上手
├── example_prompts.txt      # 30条示例提示词
├── test_extractor.sh        # 测试脚本
└── test_output.json         # 测试输出（自动生成）
```

## 核心功能

### 1. 自动化提取流程

```mermaid
提示词文件 → 格式识别 → 清洗去重 → 聚类分组 → 模块提取 → 质量评分 → 输出库
```

### 2. 支持的输入格式

- **TXT**: 每行一个提示词
- **CSV**: 自动识别prompt列
- **JSON**: 数组或对象数组

### 3. 提取的模块类型

| 模块类型 | 说明 | 示例 |
|---------|------|------|
| 主体变量 | 可替换的核心对象 | "young woman", "cyberpunk city" |
| 视觉风格 | 艺术风格和画风 | "photorealistic", "cinematic", "anime" |
| 技术参数 | 镜头、光线、渲染 | "85mm lens f/1.4", "cinematic lighting" |
| 细节增强 | 质量修饰词 | "ultra detailed", "8k", "sharp focus" |
| 情绪氛围 | 情感和氛围 | "moody", "serene", "dramatic" |
| 约束条件 | 负面提示 | "no blur", "avoid distortion" |

### 4. 输出成果

**extracted_modules.json** - 完整数据
```json
{
  "original_prompt": "...",
  "theme": "人像摄影",
  "modules": {
    "subject_variables": {...},
    "visual_style": {...},
    "technical_parameters": {...}
  },
  "quality_score": {
    "clarity": 9,
    "detail_richness": 8,
    "reusability": 9
  }
}
```

**module_library.json** - 可复用库
```json
{
  "visual_styles": [...],
  "technical_params": {...},
  "templates": [...]
}
```

**analysis_report.md** - 分析报告
```markdown
# Top 20 高频模块
# 推荐组合
# 改进建议
```

## 使用方法

### 方式1：直接调用Skill

```
在Claude Code中输入：
> 使用 prompt-extractor skill

然后提供文件路径：
> ./my_prompts.txt
```

### 方式2：命令式调用

```
> 帮我分析这个AI绘画提示词文件 prompts.csv
```

Claude会自动识别并激活skill。

### 方式3：预处理后再提取

```bash
# 先用Python预处理
cd .claude/skills/prompt-extractor
python3 preprocessor.py ../../my_prompts.txt output.json

# 查看统计信息
cat output.json | python3 -m json.tool
```

## 处理规模建议

| 数量 | 策略 | 预计时间 | 推荐方式 |
|------|------|---------|---------|
| <100条 | 一次性处理 | 2-5分钟 | 直接用skill |
| 100-500条 | 单批次处理 | 5-15分钟 | 直接用skill |
| 500-2000条 | 分2-4批 | 20-40分钟 | 分批 + 合并 |
| >2000条 | 分多批并迭代 | 1-3小时 | 先聚类后批处理 |

## 实战场景

### 场景1：新手学习优秀结构

**目标**：理解高质量提示词的共同模式

**操作**：
1. 收集网上的优秀案例（如Midjourney精选）
2. 用skill分析提取结构
3. 阅读 analysis_report.md 学习模式

**收获**：
- 发现85%使用"主体+技术+质量"结构
- 识别10个高复用模板
- 理解不同风格的参数组合

### 场景2：构建个人模块库

**目标**：从历史作品中提炼可复用组件

**操作**：
1. 导出所有历史prompt（如Midjourney export）
2. 分批处理（每批500条）
3. 合并生成统一的module_library.json

**收获**：
- 5000+独特模块的个人库
- 按主题分类的模板
- 快速组装新prompt的基础

### 场景3：提升创作质量

**目标**：找到高成片率的prompt模式

**操作**：
1. 分别导出"成功作品"和"失败作品"的prompt
2. 对比两者的模块提取结果
3. 识别成功的关键因素

**收获**：
- 发现成功案例平均有4+个技术参数
- 识别"电影级"风格的必备组合
- 理解质量词的正确使用方式

## 质量优化技巧

### 1. 提高提取精度

**初次测试**：
- 先用50-100条高质量样本
- 手动标注20条作为基准
- 对比AI提取结果

**迭代调整**：
- 修改 skill.md 中的提取规则
- 调整模块分类标准
- 重新测试直到满意

### 2. 处理低质量数据

**识别问题**：
```python
# 查看平均质量分
python3 -c "
import json
with open('extracted_modules.json') as f:
    data = json.load(f)
    scores = [item['quality_score']['clarity'] for item in data]
    print(f'平均清晰度: {sum(scores)/len(scores):.2f}')
"
```

**过滤策略**：
- 只保留评分>7的提示词
- 手动清理明显异常的条目
- 提高 min_length 阈值

### 3. 批量处理最佳实践

**分批策略**：
```bash
# 分割大文件
split -l 500 large_prompts.txt batch_

# 分别处理
for file in batch_*; do
    echo "Processing $file..."
    # 调用skill处理
done

# 合并结果
python3 merge_libraries.py batch_*.json final_library.json
```

## 高级功能

### 1. 自定义模块分类

编辑 `skill.md`，添加新的模块类型：

```markdown
**自定义模块**：
- **情感表达** (Emotional Expression)：描述情感的词汇
- **文化元素** (Cultural Elements)：特定文化符号
```

### 2. 调整评分权重

```python
# 在preprocessor.py中修改
quality_score = {
    "clarity": 0.3,        # 清晰度权重
    "detail_richness": 0.3, # 细节权重
    "reusability": 0.4      # 复用性权重（提高此项）
}
```

### 3. 导出为其他格式

```python
import json
import pandas as pd

# 转Excel
with open('module_library.json') as f:
    data = json.load(f)

df = pd.DataFrame(data['templates'])
df.to_excel('templates.xlsx', index=False)
```

## 故障排除

### 问题1：skill无法识别

**症状**：输入命令后Claude没有响应

**解决**：
```bash
# 检查skill.md是否存在
ls -la .claude/skills/prompt-extractor/skill.md

# 确认权限
chmod 644 .claude/skills/prompt-extractor/skill.md
```

### 问题2：文件格式错误

**症状**：`ValueError: 不支持的文件格式`

**解决**：
```bash
# 检查文件编码
file -I your_file.txt

# 转换为UTF-8
iconv -f GBK -t UTF-8 input.txt > output.txt
```

### 问题3：提取质量差

**症状**：模块分类混乱，评分低

**解决**：
1. 检查原始数据质量
2. 先用预处理脚本清洗
3. 手动标注样本调整规则

### 问题4：处理速度慢

**症状**：500条需要30分钟+

**解决**：
- 减少批次大小（50-100条/批）
- 先聚类后并行处理
- 使用更快的模型（如haiku）

## 下一步扩展

### 短期（1-2周）
- [ ] 支持中文提示词分析
- [ ] 添加可视化dashboard
- [ ] 实现模块搜索功能

### 中期（1个月）
- [ ] 集成Midjourney参数库
- [ ] 自动生成组合建议
- [ ] 质量预测模型

### 长期（3个月）
- [ ] 在线模块分享平台
- [ ] AI辅助prompt生成器
- [ ] 多模型适配（SD/DALL-E）

## 贡献与反馈

如需改进或遇到问题，在Claude Code中询问：

```
prompt-extractor 如何添加新模块类型？
prompt-extractor 能支持视频提示词吗？
prompt-extractor 如何导出为Notion数据库？
```

## 资源链接

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Midjourney Docs](https://docs.midjourney.com/)
- [AI绘画提示词库](https://prompthero.com/)

---

**开始构建你的提示词帝国吧！** 🎨✨

最后更新：2025-12-31
