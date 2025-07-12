@echo off
echo ========================================
echo VSOP KEFF 自动化研究脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：没有找到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

:: 检查pip是否可用
pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误：没有找到pip，请检查Python安装
    pause
    exit /b 1
)

echo 正在检查并安装Python依赖...
pip install -r requirements.txt

if errorlevel 1 (
    echo 警告：依赖安装可能失败，但将尝试继续运行
    echo.
)

echo.
echo 开始运行KEFF研究脚本...
echo.

python keff_study_automation.py

echo.
echo 脚本执行完成
pause 