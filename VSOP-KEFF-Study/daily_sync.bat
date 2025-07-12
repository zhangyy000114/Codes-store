@echo off
chcp 65001 > nul
echo =======================================
echo    GitHub 日常同步工具
echo    适用于 VSOP-KEFF-Study 项目
echo =======================================
echo.

echo 📁 当前目录: %cd%
echo.

echo 🔍 检查当前状态...
git status --short
echo.

echo 📊 当前分支信息:
git branch -v
echo.

echo 🌐 远程仓库信息:
git remote -v
echo.

echo =======================================
echo 📥 开始同步流程...
echo.

echo ➕ 1. 获取远程仓库信息...
git fetch origin
if %errorlevel% neq 0 (
    echo ❌ 获取远程信息失败！
    echo 🔧 请检查网络连接或SSH配置
    pause
    exit /b 1
)
echo ✅ 远程信息获取成功

echo.
echo 📋 2. 检查是否有本地未提交的更改...
git diff --quiet
if %errorlevel% neq 0 (
    echo ⚠️  发现本地有未提交的更改！
    echo 📝 未提交的文件：
    git diff --name-only
    echo.
    echo 🤔 您希望如何处理？
    echo 1. 暂存并提交这些更改
    echo 2. 暂时保存这些更改（stash）
    echo 3. 放弃这些更改
    echo 4. 退出，手动处理
    echo.
    set /p choice=请选择 (1/2/3/4): 
    
    if "%choice%"=="1" (
        set /p commit_msg=请输入提交信息: 
        git add .
        git commit -m "!commit_msg!"
        echo ✅ 本地更改已提交
    ) else if "%choice%"=="2" (
        git stash
        echo ✅ 本地更改已暂存
    ) else if "%choice%"=="3" (
        git checkout .
        echo ✅ 本地更改已放弃
    ) else (
        echo 👋 退出同步，请手动处理
        pause
        exit /b 0
    )
    echo.
) else (
    echo ✅ 工作区干净，无未提交更改
)

echo.
echo 📥 3. 拉取最新更改...
git pull origin main
if %errorlevel% neq 0 (
    echo ❌ 拉取失败！
    echo 🔧 可能的解决方案：
    echo 1. 检查是否有合并冲突需要解决
    echo 2. 运行: git status 查看详细状态
    echo 3. 手动解决冲突后重新运行
    pause
    exit /b 1
)
echo ✅ 拉取成功

echo.
echo =======================================
echo 🎉 同步完成！
echo.
echo 📊 最新的提交历史:
git log --oneline -10
echo.
echo 📈 项目统计信息:
echo 📁 总文件数: 
dir /s /b | find /c /v ""
echo.
echo 🔗 GitHub链接: https://github.com/zhangyy000114/Codes-store
echo =======================================
pause 