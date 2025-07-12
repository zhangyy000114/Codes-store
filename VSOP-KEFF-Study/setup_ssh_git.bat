@echo off
echo ================================================
echo Git SSH 配置脚本
echo 为 zhangyy000114 的 GitHub 仓库配置 SSH
echo ================================================
echo.

echo 1. 当前远程仓库配置：
git remote -v
echo.

echo 2. 修改远程仓库为 SSH 协议...
git remote set-url origin git@github.com:zhangyy000114/Codes-store.git
echo.

echo 3. 验证修改后的配置：
git remote -v
echo.

echo 4. 测试 SSH 连接...
ssh -T git@github.com
echo.

echo 5. 尝试获取远程更新...
git fetch origin
echo.

echo ================================================
echo 配置完成！
echo.
echo 如果上面的 SSH 测试失败，请先按照以下步骤操作：
echo 1. 打开 Git Bash
echo 2. 运行: ssh-keygen -t ed25519 -C "zhangyy000114@github.com"
echo 3. 将公钥添加到 GitHub (Settings → SSH and GPG keys)
echo 4. 重新运行此脚本
echo ================================================
pause 