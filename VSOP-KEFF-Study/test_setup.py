#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSOP KEFF 研究脚本配置测试
检查必要文件和Python环境
"""

import os
import sys

def test_setup():
    """测试配置是否正确"""
    print("VSOP KEFF 研究脚本配置测试")
    print("=" * 40)
    
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
    
    # 测试first_begin.i第87行
    print("\n检查first_begin.i第87行:")
    try:
        with open("first_begin.i", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) >= 87:
            target_line = lines[86]  # 第87行，索引86
            print(f"第87行内容: {target_line.strip()}")
            
            parts = target_line.split()
            if len(parts) >= 2:
                try:
                    value = float(parts[1])
                    print(f"✅ 找到参数值: {value:.6E}")
                except ValueError:
                    print(f"❌ 无法解析参数值: {parts[1]}")
                    success = False
            else:
                print("❌ 第87行格式不正确")
                success = False
        else:
            print("❌ 文件行数不足87行")
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
    
    # 总结
    print("\n" + "=" * 40)
    if success:
        print("✅ 配置检查通过！可以运行KEFF研究脚本")
        print("\n推荐运行方式:")
        print("1. 双击运行: run_keff_study_simple.bat")
        print("2. 或命令行: python keff_study_simple.py")
    else:
        print("❌ 配置检查失败，请修复上述问题后重试")
    
    print("\n按回车键退出...")
    input()

if __name__ == "__main__":
    test_setup() 