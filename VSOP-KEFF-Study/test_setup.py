#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSOP KEFF 研究脚本配置测试 - 双参数版本
检查必要文件和Python环境，验证双参数配置
"""

import os
import sys

def test_setup():
    """测试配置是否正确"""
    print("VSOP KEFF 研究脚本配置测试 - 双参数版本")
    print("=" * 50)
    
    success = True
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 6):
        print("❌ 错误：需要Python 3.6或更高版本")
        success = False
    else:
        print("✅ Python版本符合要求")
    
    # 检查必要文件
    required_files = [
        "first_begin.i",
        "VSOP99_11-MS.exe"
    ]
    
    print("\n检查必要文件:")
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} - {size:,} 字节")
        else:
            print(f"❌ {file} - 文件不存在")
            success = False
    
    # 检查脚本文件
    script_files = [
        "keff_study_simple.py",
        "keff_study_automation.py",
        "run_keff_study_simple.bat",
        "run_keff_study.bat"
    ]
    
    print("\n检查脚本文件:")
    for file in script_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 文件不存在")
    
    # 测试first_begin.i第77行和第92行
    print("\n检查first_begin.i双参数配置:")
    try:
        with open("first_begin.i", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 检查第77行
        if len(lines) >= 77:
            target_line_77 = lines[76]  # 第77行，索引76
            print(f"第77行内容: {target_line_77.strip()}")
            
            parts_77 = target_line_77.split()
            if len(parts_77) >= 2:
                try:
                    value_77 = float(parts_77[1])
                    print(f"✅ 第77行参数值: {value_77:.6E}")
                except ValueError:
                    print(f"❌ 无法解析第77行参数值: {parts_77[1]}")
                    success = False
            else:
                print("❌ 第77行格式不正确")
                success = False
        else:
            print("❌ 文件行数不足77行")
            success = False
        
        # 检查第92行
        if len(lines) >= 92:
            target_line_92 = lines[91]  # 第92行，索引91
            print(f"第92行内容: {target_line_92.strip()}")
            
            parts_92 = target_line_92.split()
            if len(parts_92) >= 2:
                try:
                    value_92 = float(parts_92[1])
                    print(f"✅ 第92行参数值: {value_92:.6E}")
                    
                    # 验证比例关系
                    if len(parts_77) >= 2 and len(parts_92) >= 2:
                        try:
                            ratio_actual = value_77 / value_92
                            ratio_expected = 7.95 / 5.0
                            ratio_diff = abs(ratio_actual - ratio_expected) / ratio_expected * 100
                            
                            print(f"比例关系验证:")
                            print(f"  实际比例: {ratio_actual:.3f}")
                            print(f"  期望比例: {ratio_expected:.3f}")
                            print(f"  差异: {ratio_diff:.2f}%")
                            
                            if ratio_diff < 1.0:  # 1%的容差
                                print("✅ 比例关系正确")
                            else:
                                print("⚠️  比例关系偏差较大")
                        except:
                            print("⚠️  无法验证比例关系")
                    
                except ValueError:
                    print(f"❌ 无法解析第92行参数值: {parts_92[1]}")
                    success = False
            else:
                print("❌ 第92行格式不正确")
                success = False
        else:
            print("❌ 文件行数不足92行")
            success = False
            
    except Exception as e:
        print(f"❌ 读取文件出错: {e}")
        success = False
    
    # 测试参考输出文件和keff提取
    print("\n检查参考输出文件:")
    ref_files = ["2025.0711.out", "first_begin.out", "first.out"]
    found_ref = False
    test_file = None
    for file in ref_files:
        if os.path.exists(file):
            print(f"✅ 找到参考文件: {file}")
            found_ref = True
            test_file = file
            break
    
    if not found_ref:
        print("⚠️  警告：未找到参考输出文件，无法验证输出格式")
    else:
        # 测试keff提取
        print("\n测试keff提取:")
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            target_header = "TIME (D)   K-EFF    POW-DENS   POW/BALL   FUEL TEMP    DISCH.-BU   POWER    TEMP.   TEMP."
            header_found = False
            
            for i, line in enumerate(lines):
                if target_header in line:
                    print(f"✅ 找到标题行于第{i+1}行")
                    if i + 3 < len(lines):
                        data_line = lines[i + 3]
                        parts = data_line.split()
                        if len(parts) >= 3:
                            try:
                                keff_value = float(parts[2])
                                print(f"✅ 测试提取keff值: {keff_value}")
                                header_found = True
                            except ValueError:
                                print(f"❌ 无法解析keff值: {parts[2]}")
                        else:
                            print(f"❌ 数据行格式不正确")
                    else:
                        print(f"❌ 标题行下方第3行超出文件范围")
                    break
            
            if not header_found:
                print(f"❌ 未找到标题行")
                success = False
        except Exception as e:
            print(f"❌ 测试keff提取时出错: {e}")
            success = False
    
    # 检查Python包依赖
    print("\n检查Python包依赖:")
    packages = [
        ("pandas", "数据处理（keff_study_automation.py需要）"),
        ("numpy", "数值计算（keff_study_automation.py需要）"),
        ("openpyxl", "Excel文件支持（keff_study_automation.py需要）")
    ]
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"⚠️  {package} - {description} - 未安装（简化版本不需要）")
    
    # 总结
    print("\n" + "=" * 50)
    if success:
        print("✅ 基本配置检查通过！可以运行KEFF研究脚本")
        print("\n双参数版本特性:")
        print("  ✅ 同时修改第77行和第92行参数")
        print("  ✅ 自动保持7.95:5的比例关系")
        print("  ✅ 完整的双参数结果追踪")
        print("\n推荐运行方式:")
        print("1. 简化版（无需依赖）: run_keff_study_simple.bat")
        print("2. 完整版（需要pandas）: run_keff_study.bat")
        print("3. 命令行运行: python keff_study_simple.py")
    else:
        print("❌ 配置检查失败，请修复上述问题后重试")
    
    print("\n按回车键退出...")
    input()

if __name__ == "__main__":
    test_setup() 