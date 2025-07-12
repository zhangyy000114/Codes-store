@echo off
chcp 65001 > nul
echo =======================================
echo    GitHub 快速上传工具
echo    适用于 VSOP-KEFF-Study 项目
echo =======================================
echo.

echo 📁 当前目录: %cd%
echo.

echo 🔍 检查Git状态...
git status --short
echo.

echo 📊 查看未提交的更改:
git diff --stat
echo.

echo 📝 最近的提交历史:
git log --oneline -3
echo.

echo =======================================
set /p message=💬 请输入提交信息: 
echo.

echo 📤 开始上传流程...
echo.

echo ➕ 1. 添加所有文件...
git add .
if %errorlevel% neq 0 (
    echo ❌ 添加文件失败！
    pause
    exit /b 1
)
echo ✅ 文件添加成功

echo.
echo 💾 2. 提交到本地仓库...
git commit -m "%message%"
if %errorlevel% neq 0 (
    echo ❌ 提交失败！
    pause
    exit /b 1
)
echo ✅ 本地提交成功

echo.
echo 🌐 3. 推送到GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ 推送失败！请检查网络连接或SSH配置
    echo.
    echo 🔧 可能的解决方案：
    echo 1. 检查SSH密钥是否正确配置
    echo 2. 运行: ssh -T git@github.com 测试连接
    echo 3. 或先运行: git pull origin main
    pause
    exit /b 1
)

echo.
echo =======================================
echo 🎉 上传成功！
echo 📊 推送统计：
git log --oneline -5
echo.
echo 🔗 GitHub链接: https://github.com/zhangyy000114/Codes-store
echo =======================================
pause 