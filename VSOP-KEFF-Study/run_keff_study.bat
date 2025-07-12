@echo off
echo ========================================
echo VSOP KEFF 自动化研究脚本 - 双参数完整版本
echo ========================================
echo 功能特点:
echo   - 同时修改第87行和第92行参数
echo   - 自动保持7.95:5的比例关系
echo   - 使用pandas和numpy进行数据处理
echo   - 生成Excel格式结果文件
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：没有找到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

:: 检查pip是否可用
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：没有找到pip，请检查Python安装
    pause
    exit /b 1
)

echo ✅ Python和pip检查通过
echo.

echo 📦 正在检查并安装Python依赖包...
echo 需要安装：pandas, numpy, openpyxl
pip install -r requirements.txt

if errorlevel 1 (
    echo ⚠️  警告：依赖安装可能失败，但将尝试继续运行
    echo 如果脚本运行失败，请使用简化版本：run_keff_study_simple.bat
    echo.
)

echo.
echo 🚀 开始运行KEFF双参数研究脚本...
echo 提示：脚本将自动计算第92行参数值以保持比例关系
echo.

python keff_study_automation.py

echo.
echo 📊 脚本执行完成
echo 结果文件：keff_study_results.xlsx
pause 