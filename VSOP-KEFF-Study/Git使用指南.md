# Git 完整使用指南

## 目录
1. [Git 基本概念](#git-基本概念)
2. [Git 安装与配置](#git-安装与配置)
3. [Git 基本命令](#git-基本命令)
4. [Git 分支管理](#git-分支管理)
5. [Git 远程仓库](#git-远程仓库)
6. [GitHub 连接与配置](#github-连接与配置)
7. [SSH 密钥配置](#ssh-密钥配置)
8. [Cursor 中的 Git 使用](#cursor-中的-git-使用)
9. [Git 工作流](#git-工作流)
10. [常见问题解决](#常见问题解决)

---

## Git 基本概念

### 什么是 Git？
Git 是一个分布式版本控制系统，用于跟踪计算机文件的变化，协调多人协作开发。

### 核心概念
- **仓库（Repository）**：存储项目代码和版本历史的地方
- **工作区（Working Directory）**：当前编辑的文件所在目录
- **暂存区（Staging Area）**：准备提交的文件临时存储区
- **提交（Commit）**：保存到仓库的一个版本快照
- **分支（Branch）**：代码的不同开发线
- **远程仓库（Remote Repository）**：托管在网络上的仓库副本

### Git 工作流程
```
工作区 → 暂存区 → 本地仓库 → 远程仓库
```

---

## Git 安装与配置

### 基本配置
```bash
# 设置用户名和邮箱
git config --global user.name "zhangyy000114"
git config --global user.email "zhangyy000114@github.com"

# 查看配置
git config --list

# 设置默认分支名
git config --global init.defaultBranch main

# 设置编辑器
git config --global core.editor "code --wait"
```

### 网络配置
```bash
# 设置超时时间
git config --global http.timeout 300
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

# 设置代理（如果需要）
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## Git 基本命令

### 初始化和克隆
```bash
# 初始化新仓库
git init

# 克隆远程仓库
git clone https://github.com/zhangyy000114/repository.git
git clone git@github.com:zhangyy000114/repository.git

# 克隆指定分支
git clone -b branch_name https://github.com/zhangyy000114/repository.git
```

### 文件操作
```bash
# 查看状态
git status

# 添加文件到暂存区
git add filename
git add .                # 添加所有文件
git add *.txt           # 添加所有 txt 文件

# 提交更改
git commit -m "提交说明"
git commit -am "添加并提交所有更改"

# 查看提交历史
git log
git log --oneline       # 简洁显示
git log --graph        # 图形化显示
git log --author="zhangyy000114"  # 按作者筛选
```

### 文件状态和差异
```bash
# 查看工作区和暂存区差异
git diff

# 查看暂存区和最新提交的差异
git diff --cached

# 查看两个提交之间的差异
git diff commit1 commit2

# 查看文件历史
git log -p filename
```

### 撤销操作
```bash
# 撤销工作区的修改
git checkout -- filename
git restore filename

# 撤销暂存区的修改
git reset HEAD filename
git restore --staged filename

# 撤销最后一次提交
git reset --soft HEAD~1  # 保留更改在暂存区
git reset --mixed HEAD~1 # 保留更改在工作区
git reset --hard HEAD~1  # 完全删除更改

# 修改最后一次提交
git commit --amend -m "新的提交说明"
```

---

## Git 分支管理

### 分支基本操作
```bash
# 查看分支
git branch              # 查看本地分支
git branch -r          # 查看远程分支
git branch -a          # 查看所有分支

# 创建分支
git branch feature_branch

# 切换分支
git checkout feature_branch
git switch feature_branch

# 创建并切换分支
git checkout -b feature_branch
git switch -c feature_branch

# 删除分支
git branch -d feature_branch    # 安全删除
git branch -D feature_branch    # 强制删除
```

### 分支合并
```bash
# 合并分支
git merge feature_branch

# 合并时创建合并提交
git merge --no-ff feature_branch

# 变基合并
git rebase main
git rebase --interactive HEAD~3  # 交互式变基
```

### 分支管理策略
```bash
# 查看分支合并情况
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# 重命名分支
git branch -m old_name new_name

# 推送分支到远程
git push origin feature_branch

# 删除远程分支
git push origin --delete feature_branch
```

---

## Git 远程仓库

### 远程仓库管理
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/zhangyy000114/repository.git

# 修改远程仓库URL
git remote set-url origin https://github.com/zhangyy000114/new-repository.git

# 删除远程仓库
git remote remove origin
```

### 同步操作
```bash
# 获取远程更新
git fetch origin

# 拉取并合并
git pull origin main
git pull --rebase origin main  # 使用变基方式

# 推送到远程
git push origin main
git push -u origin main       # 设置上游分支
git push --force origin main  # 强制推送（危险）

# 推送所有分支
git push --all origin

# 推送标签
git push origin --tags
```

### 标签管理
```bash
# 创建标签
git tag v1.0.0
git tag -a v1.0.0 -m "版本 1.0.0"

# 查看标签
git tag
git show v1.0.0

# 推送标签
git push origin v1.0.0
git push origin --tags

# 删除标签
git tag -d v1.0.0
git push origin --delete v1.0.0
```

---

## GitHub 连接与配置

### HTTPS 连接
```bash
# 使用 HTTPS 克隆
git clone https://github.com/zhangyy000114/repository.git

# 设置凭据缓存
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# Windows 凭据管理
git config --global credential.helper manager-core
```

### 个人访问令牌（PAT）
1. 登录 GitHub → Settings → Developer settings → Personal access tokens
2. 生成新令牌，选择适当的权限
3. 使用令牌作为密码进行身份验证

### GitHub CLI
```bash
# 安装 GitHub CLI
# Windows: 从 GitHub 下载安装包

# 登录
gh auth login

# 克隆仓库
gh repo clone zhangyy000114/repository

# 创建仓库
gh repo create my-new-repo --public
```

---

## SSH 密钥配置

### 生成 SSH 密钥
```bash
# 生成 RSA 密钥
ssh-keygen -t rsa -b 4096 -C "zhangyy000114@github.com"

# 生成 ED25519 密钥（推荐）
ssh-keygen -t ed25519 -C "zhangyy000114@github.com"

# 为 GitHub 生成专用密钥
ssh-keygen -t rsa -b 4096 -C "zhangyy000114@github.com" -f ~/.ssh/id_rsa_github
```

### SSH 配置文件
创建或编辑 `~/.ssh/config` 文件：
```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_github
    
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_work
```

### Windows 路径
在 Windows 中，SSH 密钥位于：
```
C:\Users\23800\.ssh\
```

### 添加 SSH 密钥到 GitHub
1. 复制公钥内容：
   ```bash
   # Windows
   type %USERPROFILE%\.ssh\id_rsa.pub
   clip < %USERPROFILE%\.ssh\id_rsa.pub
   
   # Linux/Mac
   cat ~/.ssh/id_rsa.pub
   pbcopy < ~/.ssh/id_rsa.pub
   ```

2. 在 GitHub 中添加：
   - Settings → SSH and GPG keys → New SSH key
   - 粘贴公钥内容

### 测试 SSH 连接
```bash
ssh -T git@github.com
```

### 使用 SSH 克隆
```bash
git clone git@github.com:zhangyy000114/repository.git
```

---

## Cursor 中的 Git 使用

### 内置 Git 功能
1. **源代码管理面板**
   - 快捷键：`Ctrl+Shift+G`
   - 查看文件更改
   - 暂存和提交文件

2. **Git 状态指示器**
   - 文件旁的状态标识
   - M: 修改，A: 添加，D: 删除，U: 未跟踪

3. **差异查看**
   - 点击文件查看更改
   - 并排显示差异
   - 行级别的更改高亮

### Cursor 快捷键
```
Ctrl+Shift+G    打开源代码管理
Ctrl+Enter      提交更改
Ctrl+Shift+P    命令面板
```

### 在 Cursor 中使用 Git 命令
1. **终端集成**
   - 快捷键：`Ctrl+``（反引号）
   - 在内置终端中运行 Git 命令

2. **命令面板**
   - 快捷键：`Ctrl+Shift+P`
   - 输入 "Git" 查看 Git 命令

### Git 插件推荐
- **GitLens**：增强 Git 功能
- **Git History**：查看文件历史
- **Git Graph**：可视化 Git 历史

### 工作流集成
```bash
# 在 Cursor 中打开项目
code .

# 查看 Git 状态
git status

# 使用 Cursor 进行代码审查
git log --oneline | head -10
```

---

## Git 工作流

### GitHub Flow
1. 创建功能分支
2. 添加提交
3. 创建 Pull Request
4. 讨论和审查
5. 合并到主分支

### GitFlow
1. **主分支**：main/master
2. **开发分支**：develop
3. **功能分支**：feature/feature-name
4. **发布分支**：release/version
5. **热修复分支**：hotfix/issue-name

### 团队协作流程
```bash
# 1. 同步主分支
git checkout main
git pull origin main

# 2. 创建功能分支
git checkout -b feature/new-feature

# 3. 开发和提交
git add .
git commit -m "添加新功能"

# 4. 推送分支
git push origin feature/new-feature

# 5. 创建 Pull Request
# 在 GitHub 网站上操作

# 6. 合并后清理
git checkout main
git pull origin main
git branch -d feature/new-feature
```

---

## 常见问题解决

### 连接问题
```bash
# 网络超时
git config --global http.timeout 300

# 代理设置
git config --global http.proxy http://proxy.example.com:8080

# SSL 证书问题
git config --global http.sslverify false
```

### 合并冲突
```bash
# 1. 查看冲突文件
git status

# 2. 手动解决冲突
# 编辑冲突文件，删除 <<<<<<<, =======, >>>>>>> 标记

# 3. 标记为已解决
git add conflicted_file

# 4. 完成合并
git commit
```

### 误操作恢复
```bash
# 恢复已删除的提交
git reflog
git checkout commit_hash

# 恢复已删除的分支
git reflog
git checkout -b recovered_branch commit_hash

# 恢复已删除的文件
git checkout HEAD -- filename
```

### 清理操作
```bash
# 清理未跟踪的文件
git clean -f
git clean -fd  # 包括目录

# 清理分支
git branch --merged | grep -v main | xargs -n 1 git branch -d

# 压缩 Git 仓库
git gc --aggressive --prune=now
```

### 性能优化
```bash
# 浅克隆
git clone --depth 1 https://github.com/zhangyy000114/repository.git

# 部分克隆
git clone --filter=blob:none https://github.com/zhangyy000114/repository.git

# 稀疏检出
git config core.sparseCheckout true
echo "path/to/subdirectory/*" >> .git/info/sparse-checkout
git read-tree -m -u HEAD
```

---

## 最佳实践

### 提交规范
```bash
# 提交信息格式
type(scope): subject

# 类型
feat: 新功能
fix: 修复
docs: 文档
style: 格式
refactor: 重构
test: 测试
chore: 构建过程或辅助工具的变动

# 示例
feat(login): 添加用户登录功能
fix(api): 修复数据获取错误
docs(readme): 更新安装说明
```

### 分支命名
```bash
# 功能分支
feature/user-authentication
feature/payment-integration

# 修复分支
fix/login-bug
hotfix/critical-security-issue

# 发布分支
release/v1.2.0
```

### 安全最佳实践
1. 不要提交敏感信息（密码、API密钥）
2. 使用 `.gitignore` 文件
3. 定期更新密钥
4. 使用 SSH 密钥而非密码

---

## 常用命令快速参考

### 日常操作
```bash
git status          # 查看状态
git add .           # 添加所有文件
git commit -m "msg" # 提交
git push            # 推送
git pull            # 拉取
git log --oneline   # 查看历史
```

### 分支操作
```bash
git branch          # 查看分支
git checkout -b new # 创建并切换
git merge branch    # 合并分支
git branch -d old   # 删除分支
```

### 远程操作
```bash
git remote -v       # 查看远程
git fetch           # 获取更新
git push origin br  # 推送分支
git pull origin br  # 拉取分支
```

---

## 总结

Git 是现代软件开发不可或缺的工具。掌握 Git 的基本概念和命令，配合 Cursor 的强大功能，可以显著提高开发效率。记住：

1. **多练习**：熟能生巧
2. **小步提交**：频繁提交，描述清晰
3. **分支管理**：合理使用分支，保持主分支稳定
4. **团队协作**：遵循团队的工作流程和规范
5. **备份重要**：定期推送到远程仓库

希望这份指南能帮助您更好地使用 Git 和 GitHub！ 