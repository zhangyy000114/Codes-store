# VSOP KEFF 自动化研究脚本

本脚本用于自动化研究 `first_begin.i` 文件中第87行参数值对 keff 结果的影响。

## 文件说明

### 主要脚本
- `keff_study_simple.py` - **推荐使用**，简化版本，仅依赖Python标准库
- `keff_study_automation.py` - 完整版本，需要安装pandas等外部库
- `run_keff_study_simple.bat` - **推荐使用**，运行简化版脚本的批处理文件
- `run_keff_study.bat` - 运行完整版脚本的批处理文件

### 依赖文件
- `requirements.txt` - Python外部依赖列表（仅完整版需要）

## 快速开始

### 方法一：使用简化版本（推荐）

1. **双击运行** `run_keff_study_simple.bat`
2. 按提示设置参数：
   - 起始值（默认：1e-8）
   - 结束值（默认：9e-7）
   - 计算点数（默认：9）
3. 确认参数后开始自动运行
4. 等待计算完成，查看结果文件

### 方法二：使用完整版本

1. 安装Python依赖：
   ```
   pip install -r requirements.txt
   ```
2. 双击运行 `run_keff_study.bat`

### 方法三：直接运行Python脚本

```bash
python keff_study_simple.py
```

## 工作流程

1. **备份原始文件** - 自动备份 `first_begin.i` 到 `first_begin.i.backup`
2. **参数扫描** - 在指定范围内生成参数值序列（对数均匀分布）
3. **循环计算**：
   - 修改 `first_begin.i` 第87行第2个数据
   - 运行 `VSOP99_11-MS.exe` 程序
   - 搜索标题行"TIME (D)   K-EFF    POW-DENS   POW/BALL   FUEL TEMP    DISCH.-BU   POWER    TEMP.   TEMP."
   - 从标题行下方第3行的第3个值提取 keff
4. **恢复原始文件**
5. **保存结果** - 生成CSV文件和统计摘要

## 输出文件

### 简化版本输出
- `keff_study_results.csv` - 详细结果表格
- `keff_study_summary.txt` - 统计摘要
- `[参数值].out` - 各次计算的VSOP输出文件

### 完整版本输出
- `keff_study_results.xlsx` - Excel格式结果表格（包含统计工作表）

## 结果格式

### CSV文件列说明
- **序号** - 计算序号
- **参数值** - 修改的参数值（科学计数法）
- **keff值** - 提取的keff值
- **keff变化** - 相对于第一个值的变化
- **keff变化百分比(%)** - 变化百分比
- **输出文件** - 对应的输出文件名

## 系统要求

- Windows 10/11
- Python 3.6 或更高版本
- `first_begin.i` 输入文件
- `VSOP99_11-MS.exe` 程序

## 注意事项

1. **运行时间**：每次计算约需1-3分钟，总时间取决于计算点数
2. **文件大小**：每个输出文件约20MB，请确保有足够磁盘空间
3. **程序路径**：确保 `VSOP99_11-MS.exe` 在当前目录
4. **中断恢复**：如程序中断，原始文件会自动从备份恢复

## 自定义参数

### 修改参数范围
编辑脚本中的以下部分：
```python
parameter_values = automation.generate_parameter_values(
    start=1e-8,    # 起始值
    end=9e-7,      # 结束值
    num_points=9   # 点数
)
```

### 修改目标行号
如需修改其他行，更改脚本中的：
```python
self.target_line = 87  # 目标行号
```

### 修改keff提取位置
如keff值标题行不同，更改脚本中的：
```python
target_header = "TIME (D)   K-EFF    POW-DENS   POW/BALL   FUEL TEMP    DISCH.-BU   POWER    TEMP.   TEMP."
```

## 常见问题

### Q: 运行时提示找不到Python
A: 请安装Python 3.6或更高版本，下载地址：https://www.python.org/downloads/

### Q: 程序运行失败
A: 检查以下项目：
- `first_begin.i` 文件是否存在且格式正确
- `VSOP99_11-MS.exe` 是否在当前目录
- 磁盘空间是否充足

### Q: 结果文件打不开
A: CSV文件可用Excel、记事本等打开，如有中文显示问题，请使用UTF-8编码

### Q: 如何查看中间结果
A: 脚本运行时会实时显示进度，每次计算的keff值都会打印在控制台

## 版本历史

- v1.0 - 初始版本，包含完整功能
- v1.1 - 添加简化版本，无需外部依赖
- v1.2 - 改进错误处理和用户界面

## 技术支持

如遇问题，请检查：
1. 控制台输出的错误信息
2. 输入文件格式是否正确
3. Python版本是否兼容 