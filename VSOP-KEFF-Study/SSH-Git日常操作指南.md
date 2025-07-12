# SSH Git 日常操作指南

## 🚀 恭喜！您的SSH已经配置成功

您现在可以使用SSH协议与GitHub进行无密码连接。以下是日常操作的完整指南：

---

## 📤 上传文件到GitHub

### 方法一：完整的上传流程（推荐）
```bash
# 1. 查看当前状态
git status

# 2. 添加要上传的文件
git add .                    # 添加所有文件
git add filename.txt         # 添加单个文件
git add *.py                 # 添加所有Python文件
git add folder/              # 添加整个文件夹

# 3. 提交到本地仓库
git commit -m "描述性的提交信息"

# 4. 推送到GitHub
git push origin main
```

### 方法二：快速上传（适用于小改动）
```bash
# 一次性添加所有文件并提交
git add . && git commit -m "提交说明" && git push origin main
```

### 方法三：使用Cursor图形界面
1. 按 `Ctrl+Shift+G` 打开源代码管理面板
2. 在"Changes"部分点击文件旁的"+"号添加文件
3. 在消息框中输入提交说明
4. 按 `Ctrl+Enter` 提交
5. 点击"Sync Changes"按钮推送到GitHub

---

## 📥 从GitHub下载/更新文件

### 获取最新更改
```bash
# 获取远程仓库的最新信息
git fetch origin

# 拉取并合并最新更改
git pull origin main

# 查看远程仓库的更改情况
git log --oneline origin/main..HEAD
```

### 克隆新的仓库
```bash
# 克隆您的仓库
git clone git@github.com:zhangyy000114/repository-name.git

# 克隆到指定目录
git clone git@github.com:zhangyy000114/repository-name.git my-project

# 克隆指定分支
git clone -b develop git@github.com:zhangyy000114/repository-name.git
```

---

## 🔄 常见的日常操作

### 1. 添加新文件
```bash
# 创建新文件
echo "Hello World" > new_file.txt

# 添加到Git跟踪
git add new_file.txt

# 提交
git commit -m "feat: 添加新文件"

# 推送
git push origin main
```

### 2. 修改现有文件
```bash
# 修改文件后查看更改
git diff filename.txt

# 添加修改的文件
git add filename.txt

# 提交
git commit -m "fix: 修复文件中的问题"

# 推送
git push origin main
```

### 3. 删除文件
```bash
# 删除文件
git rm filename.txt

# 或者先删除文件，再添加删除操作
rm filename.txt
git add filename.txt

# 提交删除操作
git commit -m "remove: 删除不需要的文件"

# 推送
git push origin main
```

### 4. 重命名文件
```bash
# 重命名文件
git mv old_name.txt new_name.txt

# 提交重命名
git commit -m "rename: 重命名文件"

# 推送
git push origin main
```

---

## 🌿 分支操作

### 创建和切换分支
```bash
# 创建新分支
git branch feature/new-feature

# 切换分支
git checkout feature/new-feature

# 创建并切换分支（一步完成）
git checkout -b feature/new-feature

# 推送新分支到GitHub
git push origin feature/new-feature
```

### 合并分支
```bash
# 切换到主分支
git checkout main

# 合并功能分支
git merge feature/new-feature

# 推送合并结果
git push origin main

# 删除本地分支
git branch -d feature/new-feature

# 删除远程分支
git push origin --delete feature/new-feature
```

---

## 📊 查看信息

### 查看状态和历史
```bash
# 查看当前状态
git status

# 查看提交历史
git log --oneline

# 查看文件更改历史
git log -p filename.txt

# 查看远程仓库信息
git remote -v

# 查看所有分支
git branch -a
```

### 查看差异
```bash
# 查看工作区和暂存区的差异
git diff

# 查看暂存区和最后一次提交的差异
git diff --cached

# 查看两次提交之间的差异
git diff HEAD~1 HEAD
```

---

## 🔧 您的专用配置

### 当前项目信息
- **仓库名称**: VSOP-KEFF-Study
- **GitHub地址**: https://github.com/zhangyy000114/Codes-store.git
- **SSH地址**: git@github.com:zhangyy000114/Codes-store.git
- **主分支**: main

### 快速命令模板
```bash
# 针对您的项目的快速上传
cd /d/git/Codes-store/VSOP-KEFF-Study
git add .
git commit -m "update: 更新VSOP研究文件"
git push origin main

# 获取最新更新
git pull origin main

# 查看项目状态
git status
git log --oneline -10
```

---

## 🎯 最佳实践建议

### 1. 提交信息规范
```bash
# 使用规范的提交信息格式
git commit -m "type: 描述"

# 常用类型：
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建过程或辅助工具的变动

# 示例：
git commit -m "feat: 添加VSOP计算模块"
git commit -m "fix: 修复Keff计算错误"
git commit -m "docs: 更新README文档"
```

### 2. 定期操作
```bash
# 每天开始工作前
git pull origin main

# 每次完成一个小功能后
git add .
git commit -m "描述性信息"
git push origin main

# 每周清理
git log --oneline -20  # 查看最近20次提交
```

### 3. 安全操作
```bash
# 推送前先检查
git status
git diff --cached

# 如果推送失败，先拉取更新
git pull origin main
git push origin main

# 备份重要工作
git checkout -b backup-$(date +%Y%m%d)
git push origin backup-$(date +%Y%m%d)
```

---

## 🚨 常见问题解决

### 1. 推送被拒绝
```bash
# 错误：Updates were rejected
# 解决：先拉取远程更改
git pull origin main
git push origin main
```

### 2. 合并冲突
```bash
# 当出现冲突时
git status                    # 查看冲突文件
# 手动编辑冲突文件，删除冲突标记
git add conflicted-file.txt   # 标记冲突已解决
git commit -m "resolve: 解决合并冲突"
git push origin main
```

### 3. 撤销操作
```bash
# 撤销最后一次提交（保留文件更改）
git reset --soft HEAD~1

# 撤销工作区的修改
git checkout -- filename.txt

# 撤销暂存区的文件
git reset HEAD filename.txt
```

---

## 📱 在Cursor中使用Git

### 快捷键
- `Ctrl+Shift+G` - 打开源代码管理面板
- `Ctrl+Enter` - 提交更改
- `Ctrl+Shift+P` - 命令面板（搜索Git命令）
- `Ctrl+` ` - 打开终端

### 图形界面操作
1. **查看更改**: 在源代码管理面板中查看文件状态
2. **暂存文件**: 点击文件旁的"+"号
3. **提交**: 输入提交信息，按Ctrl+Enter
4. **推送**: 点击"Sync Changes"按钮
5. **拉取**: 点击"Pull"按钮

---

## 💡 实用脚本

### 快速上传脚本
创建 `quick_upload.bat` 文件：
```batch
@echo off
echo 快速上传到GitHub...
git add .
git status
set /p message=请输入提交信息: 
git commit -m "%message%"
git push origin main
echo 上传完成！
pause
```

### 日常同步脚本
创建 `daily_sync.bat` 文件：
```batch
@echo off
echo 开始日常同步...
git pull origin main
echo 最新更新：
git log --oneline -5
pause
```

---

## 🎉 您现在可以：

✅ 使用 `git add .` 和 `git commit -m "信息"` 提交文件  
✅ 使用 `git push origin main` 上传到GitHub  
✅ 使用 `git pull origin main` 下载最新更改  
✅ 在Cursor中使用图形界面操作Git  
✅ 享受SSH无密码连接的便利  

**记住：先添加(add) → 再提交(commit) → 最后推送(push)**

现在开始您的Git之旅吧！🚀 