@echo off
chcp 65001 >nul
echo ========================================
echo VSOP KEFF 自动化研究脚本 - 双参数简化版本
echo ========================================
echo 功能特点:
echo   - 同时修改第87行和第92行参数
echo   - 自动保持7.95:5的比例关系
echo   - 无需外部Python依赖包
echo   - 生成CSV格式结果文件
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：没有找到Python，请先安装Python 3.6或更高版本
    echo 可以从 https://www.python.org/downloads/ 下载Python
    pause
    exit /b 1
)

echo ✅ Python 检查通过
echo.

:: 检查必要文件
if not exist "first_begin.i" (
    echo ❌ 错误：找不到输入文件 first_begin.i
    pause
    exit /b 1
)

if not exist "VSOP99_11-MS.exe" (
    echo ❌ 错误：找不到程序文件 VSOP99_11-MS.exe
    pause
    exit /b 1
)

echo ✅ 文件检查通过
echo.

echo 🚀 开始运行KEFF双参数研究脚本...
echo 提示：脚本将自动计算第92行参数值以保持比例关系
echo.

python keff_study_simple.py

echo.
echo 📊 脚本执行完成
echo 结果文件：keff_study_results.csv
echo 统计摘要：keff_study_summary.txt
pause 