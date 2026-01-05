# GitHub上传指南

## 📋 准备工作清单

### ✅ 已完成
- [x] 创建 `.gitignore` 文件
- [x] 创建 `README.md` 文件
- [x] 创建 `requirements.txt` 文件

### 🔍 需要确认的选项

#### 选项1：是否上传数据库？

**选项A：不上传数据库**（推荐给公开项目）
```bash
# 在 .gitignore 中已经注释了这行
# extracted_results/elements.db
```

**如果选择不上传**：
- 取消 `.gitignore` 第61行的注释
- 提供数据库schema文件
- 用户需要自己构建数据库

**选项B：上传数据库**（推荐给私有项目或想分享完整数据）
- 保持当前设置
- 数据库大小：1.9MB（可接受）
- 用户可以直接使用

**建议**：如果是开源项目，建议**不上传数据库**，只提供schema和示例数据。

#### 选项2：是否上传.claude目录？

`.claude/` 包含Claude Code Skills配置

**选项A：上传**（当前设置）
- ✅ 用户可以直接使用skills
- ✅ 完整的项目功能
- ❌ 可能包含你的个人配置

**选项B：不上传**
```bash
# 在 .gitignore 中取消注释第69行
.claude/
```

**建议**：**上传**，但先检查`.claude/`中是否有敏感信息。

---

## 🚀 上传步骤

### 步骤1：初始化Git仓库

```bash
# 如果还没有初始化
git init

# 查看当前状态
git status
```

### 步骤2：检查要上传的文件

```bash
# 查看将被追踪的文件
git status

# 确认 .gitignore 正常工作
git check-ignore -v <文件名>
```

**预期被排除的文件**：
- ❌ 所有 `*_REPORT.md`, `*_ANALYSIS.md`
- ❌ `__pycache__/`
- ❌ `generated_*.txt`
- ❌ `*_backup_*` 文件
- ❌ 大型JSON文件（ai_classification_results.json等）
- ❌ 临时文件

**预期被包含的文件**：
- ✅ `intelligent_generator.py`
- ✅ `framework_loader.py`
- ✅ `prompt_framework.yaml`
- ✅ `README.md`
- ✅ `.gitignore`
- ✅ `requirements.txt`
- ✅ `.claude/` 目录（如果选择上传）
- ✅ `extracted_results/elements.db`（如果选择上传）

### 步骤3：添加文件

```bash
# 添加所有文件（.gitignore会自动过滤）
git add .

# 查看将被提交的文件
git status

# 如果发现有不该提交的文件
git reset <文件名>
```

### 步骤4：首次提交

```bash
git commit -m "Initial commit: AI Prompt Generator System

- Core intelligent generation engine
- Framework-driven prompt builder
- Universal Elements Library (1140+ elements)
- Template system (design templates)
- Claude Code Skills integration
- Multi-domain support (portrait, design, art, product, video)
"
```

### 步骤5：在GitHub创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `ai-prompt-generator` 或你喜欢的名字
   - **Description**: `智能AI图像提示词生成系统 - 基于Universal Elements Library`
   - **Public** 或 **Private**（根据你的需求）
   - ❌ **不要**勾选"Initialize with README"（我们已经有了）
3. 点击"Create repository"

### 步骤6：关联远程仓库

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/仓库名.git

# 或使用SSH（如果已配置）
git remote add origin git@github.com:你的用户名/仓库名.git

# 验证
git remote -v
```

### 步骤7：推送到GitHub

```bash
# 首次推送
git push -u origin main

# 或者如果默认分支是master
git push -u origin master
```

---

## 🔧 推送前的最终检查

### 检查清单

```bash
# 1. 查看要推送的文件数量
git ls-files | wc -l

# 2. 查看仓库大小
du -sh .git

# 3. 检查是否有大文件（>50MB）
find . -type f -size +50M

# 4. 查看最大的文件
find . -type f -exec du -h {} + | sort -rh | head -20
```

### 如果仓库太大

如果发现仓库>100MB，考虑：
1. 确认是否需要上传数据库
2. 检查是否有遗漏的大文件
3. 使用Git LFS管理大文件

```bash
# 安装Git LFS
git lfs install

# 追踪大文件（如数据库）
git lfs track "extracted_results/elements.db"

# 提交 .gitattributes
git add .gitattributes
git commit -m "Add Git LFS for database"
```

---

## 📝 后续维护

### 常用Git命令

```bash
# 查看状态
git status

# 添加新文件
git add <文件名>
git add .

# 提交更改
git commit -m "描述更改内容"

# 推送到远程
git push

# 拉取最新代码
git pull

# 查看提交历史
git log --oneline
```

### .gitignore更新

如果发现有文件不该上传：
```bash
# 1. 更新 .gitignore
vim .gitignore

# 2. 移除已追踪的文件（不删除本地文件）
git rm --cached <文件名>

# 3. 提交
git commit -m "Update .gitignore"
git push
```

---

## 🎯 建议的分支策略

### 简单项目（单人）
```
main (或master) - 主分支，保持稳定
```

### 多人协作
```
main - 生产分支（稳定版本）
dev - 开发分支
feature/* - 功能分支
bugfix/* - 修复分支
```

---

## 🔒 安全检查

### 上传前必须检查：

1. **不要上传敏感信息**：
   - ❌ API密钥
   - ❌ 密码
   - ❌ 私人笔记
   - ❌ 个人信息

2. **检查.env文件**：
```bash
# 确保 .env 在 .gitignore 中
grep -n "\.env" .gitignore
```

3. **检查提交历史**：
```bash
# 查看所有提交的文件
git log --all --pretty=format: --name-only --diff-filter=A | sort -u
```

---

## 📌 快速上传流程（总结）

```bash
# 1. 检查状态
git status

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit: AI Prompt Generator"

# 4. 关联远程仓库（替换为你的URL）
git remote add origin https://github.com/你的用户名/仓库名.git

# 5. 推送
git push -u origin main
```

---

## ❓ 常见问题

### Q1: 如果不小心提交了敏感文件怎么办？

```bash
# 从历史记录中完全删除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <文件路径>" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin --force --all
```

### Q2: 如何忽略已经被追踪的文件？

```bash
# 停止追踪但保留本地文件
git rm --cached <文件名>

# 添加到 .gitignore
echo "<文件名>" >> .gitignore

# 提交
git commit -m "Stop tracking <文件名>"
```

### Q3: 推送被拒绝（rejected）

```bash
# 通常是因为远程有更新
git pull --rebase origin main
git push
```

---

## 🎉 完成

上传成功后，你可以：
1. 在GitHub上查看项目
2. 添加Topics标签（AI, prompt-engineering, etc.）
3. 编写更详细的文档
4. 设置GitHub Actions（可选）

**仓库建议标签**：
- `ai`
- `prompt-engineering`
- `image-generation`
- `claude-code`
- `python`
- `prompt-generator`
