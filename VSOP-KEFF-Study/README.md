# VSOP KEFF 自动化研究系统

本项目为VSOP核反应堆KEFF值自动化研究系统，支持双参数联动计算和实时可视化监控。

## 功能特点

### 核心功能
- **双参数自动化**: 同时修改第87行和第92行参数，保持7.95:5的固定比例
- **批量计算**: 支持对数均匀分布的参数序列计算
- **结果分析**: 自动提取KEFF值并生成统计报告
- **智能备份**: 自动备份和恢复原始输入文件

### 可视化功能
- **实时监控**: 进度条、KEFF值变化图、参数关系图
- **统计分析**: 实时统计信息显示
- **最终图表**: 6子图综合分析（KEFF变化、参数关系、变化率、分布等）
- **高质量输出**: 300 DPI PNG图片，支持科学出版要求

### 字体配置
程序已自动配置中英文字体显示：
- **中文字体**: 宋体（SimSun）优先，备选微软雅黑、黑体、楷体、仿宋等
- **英文字体**: Times New Roman优先，备选Arial、Helvetica等
- **智能适配**: 自动检测系统可用字体，选择最佳配置
- **跨平台支持**: 兼容Windows、Linux、Mac系统

## 文件结构

```
VSOP-KEFF-Study/
├── keff_study_simple.py          # 简化版主程序（带可视化）
├── keff_study_automation.py      # 完整版主程序（Excel输出）
├── test_setup.py                 # 参数设置测试
├── preview_parameters.py         # 参数预览工具
├── run_keff_study_simple.bat     # 简化版运行脚本
├── run_keff_study.bat            # 完整版运行脚本
├── requirements.txt              # 依赖包清单
├── 可视化功能说明.md              # 可视化功能详细说明
└── Libraries/                    # VSOP库文件目录
```

## 环境要求

### 必需组件
- Python 3.6+
- VSOP99_11-MS.exe（VSOP计算程序）
- first_begin.i（输入文件模板）

### 可选组件
- matplotlib 3.3.0+（可视化功能）
- openpyxl（Excel输出功能）
- numpy（数值计算加速）

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行参数预览
```bash
python preview_parameters.py
```

### 3. 运行研究
```bash
# 简化版（带可视化）
run_keff_study_simple.bat

# 完整版（Excel输出）
run_keff_study.bat
```

## 参数配置

### 双参数设置
- **第87行**: 主参数，用户直接输入
- **第92行**: 从参数，根据比例自动计算
- **比例关系**: 第87行:第92行 = 7.95:5 = 1.59:1

### 参数范围
- 默认起始值: 1e-8
- 默认结束值: 9e-7
- 默认计算点数: 9
- 分布方式: 对数均匀分布

## 输出文件

### 数据文件
- `keff_study_results.csv`: 详细计算结果
- `keff_study_summary.txt`: 统计摘要
- `keff_study_results.xlsx`: Excel格式结果（完整版）

### 图表文件
- `keff_study_analysis.png`: 综合分析图表

## 可视化功能

### 实时监控
- **进度条**: 显示计算进度和状态
- **KEFF变化图**: 实时显示KEFF值随参数变化
- **参数关系图**: 验证双参数7.95:5比例关系
- **统计信息**: 实时显示计算统计数据

### 最终分析
- **KEFF vs 参数**: 双参数与KEFF的关系图
- **参数关系验证**: 实际值与理论比例线对比
- **变化率分析**: KEFF变化率随参数变化
- **分布直方图**: KEFF值分布情况
- **统计表格**: 详细统计信息表

## 故障排除

### 可视化问题
1. **中文显示乱码**: 程序已自动配置最佳字体，支持中文宋体和英文Times New Roman
2. **图表无法显示**: 检查matplotlib是否正确安装
3. **字体不理想**: 系统会自动选择最佳可用字体

### 计算问题
1. **程序超时**: 检查VSOP程序是否正常运行
2. **文件权限**: 确保对工作目录有读写权限
3. **参数错误**: 使用 `preview_parameters.py` 检查参数设置

### 依赖问题
```bash
# 重新安装依赖
pip install --upgrade -r requirements.txt

# 检查Python版本
python --version

# 检查matplotlib安装
python -c "import matplotlib; print(matplotlib.__version__)"
```

## 技术支持

如遇问题请检查：
1. 字体配置已自动优化，支持中文和英文显示
2. 依赖包是否完整安装
3. 输入文件格式是否正确
4. VSOP程序是否可正常运行

## 更新日志

### v2.0 (2025-01-11)
- 添加智能字体配置系统
- 支持中文宋体和英文Times New Roman字体
- 自动检测并配置最佳字体组合
- 消除字体警告，优化可视化显示效果

### v1.0 (2025-01-10)
- 实现双参数自动化计算
- 添加实时可视化监控
- 支持批量参数研究
- 生成综合分析图表
