#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSOP KEFF自动化研究脚本
自动修改first_begin.i文件中的参数，运行VSOP程序，提取keff值并统计结果
"""

import os
import subprocess
import shutil
import pandas as pd
import numpy as np
import time
from pathlib import Path

class KeffStudyAutomation:
    def __init__(self):
        self.original_file = "first_begin.i"
        self.program_path = "VSOP99_11-MS.exe"
        self.target_line = 87  # 目标行号
        self.results = []
        
    def backup_original_file(self):
        """备份原始文件"""
        backup_name = f"{self.original_file}.backup"
        if not os.path.exists(backup_name):
            shutil.copy2(self.original_file, backup_name)
            print(f"已备份原始文件到: {backup_name}")
    
    def modify_input_file(self, new_value):
        """修改输入文件中的参数值"""
        with open(self.original_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 修改第87行的第2个数据
        target_line_index = self.target_line - 1
        original_line = lines[target_line_index]
        
        # 解析原始行，格式: "   4    3.303747E-08                                                        D 17"
        parts = original_line.split()
        if len(parts) >= 2:
            # 替换第2个数据
            new_line = f"   {parts[0]}    {new_value:.6E}                                                        D 17\n"
            lines[target_line_index] = new_line
            
            # 写回文件
            with open(self.original_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"已修改参数值为: {new_value:.6E}")
            return True
        else:
            print(f"错误：无法解析第{self.target_line}行")
            return False
    
    def run_vsop_program(self, value):
        """运行VSOP程序"""
        output_filename = f"{value:.6E}.out"
        
        try:
            # 创建输入序列
            input_sequence = f"{self.original_file}\n{output_filename}\n"
            
            print(f"正在运行VSOP程序，输出文件: {output_filename}")
            
            # 运行程序
            process = subprocess.Popen(
                [self.program_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            
            # 发送输入
            stdout, stderr = process.communicate(input=input_sequence, timeout=300)  # 5分钟超时
            
            if process.returncode == 0:
                print(f"程序运行成功，输出文件: {output_filename}")
                return output_filename
            else:
                print(f"程序运行失败，返回码: {process.returncode}")
                print(f"错误信息: {stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("程序运行超时")
            process.kill()
            return None
        except Exception as e:
            print(f"运行程序时发生错误: {e}")
            return None
    
    def extract_keff_value(self, output_file):
        """从输出文件中提取keff值"""
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 搜索标题行
            target_header = "TIME (D)   K-EFF    POW-DENS   POW/BALL   FUEL TEMP    DISCH.-BU   POWER    TEMP.   TEMP."
            header_line_index = -1
            
            for i, line in enumerate(lines):
                if target_header in line:
                    header_line_index = i
                    print(f"找到标题行于第{i+1}行")
                    break
            
            if header_line_index == -1:
                print(f"错误：未找到标题行 '{target_header}'")
                return None
            
            # 获取标题行下方第3行
            target_line_index = header_line_index + 3
            if target_line_index >= len(lines):
                print(f"错误：标题行下方第3行超出文件范围")
                return None
            
            target_line = lines[target_line_index]
            print(f"数据行（第{target_line_index+1}行）: {target_line.strip()}")
            
            parts = target_line.split()
            if len(parts) >= 3:
                try:
                    keff_value = float(parts[2])  # 第三个值
                    print(f"提取到keff值: {keff_value}")
                    return keff_value
                except ValueError:
                    print(f"错误：无法解析keff值 '{parts[2]}'")
                    return None
            else:
                print(f"错误：数据行格式不正确，仅有{len(parts)}个字段")
                return None
                
        except Exception as e:
            print(f"提取keff值时发生错误: {e}")
            return None
    
    def generate_parameter_values(self, start=1e-8, end=9e-7, num_points=9):
        """生成参数值序列"""
        # 对数均匀分布
        log_start = np.log10(start)
        log_end = np.log10(end)
        log_values = np.linspace(log_start, log_end, num_points)
        return 10 ** log_values
    
    def run_study(self, parameter_values=None):
        """运行完整的研究"""
        if parameter_values is None:
            parameter_values = self.generate_parameter_values()
        
        print(f"开始keff研究，共{len(parameter_values)}个参数值")
        print(f"参数范围: {parameter_values[0]:.2E} 到 {parameter_values[-1]:.2E}")
        
        # 备份原始文件
        self.backup_original_file()
        
        for i, value in enumerate(parameter_values, 1):
            print(f"\n=== 运行 {i}/{len(parameter_values)}: 参数值 = {value:.6E} ===")
            
            # 修改输入文件
            if not self.modify_input_file(value):
                continue
            
            # 运行程序
            output_file = self.run_vsop_program(value)
            if output_file is None:
                continue
            
            # 提取keff值
            keff_value = self.extract_keff_value(output_file)
            if keff_value is not None:
                self.results.append({
                    'parameter_value': value,
                    'keff': keff_value,
                    'output_file': output_file
                })
            
            print(f"完成 {i}/{len(parameter_values)}")
        
        # 恢复原始文件
        self.restore_original_file()
        
        print(f"\n研究完成！共获得{len(self.results)}个有效结果")
        
    def restore_original_file(self):
        """恢复原始文件"""
        backup_name = f"{self.original_file}.backup"
        if os.path.exists(backup_name):
            shutil.copy2(backup_name, self.original_file)
            print("已恢复原始文件")
    
    def save_results(self, filename="keff_study_results.xlsx"):
        """保存结果到Excel文件"""
        if not self.results:
            print("没有结果需要保存")
            return
        
        # 创建DataFrame
        df = pd.DataFrame(self.results)
        df = df.sort_values('parameter_value')
        
        # 添加统计信息
        df['keff_change'] = df['keff'] - df['keff'].iloc[0]
        df['keff_change_percent'] = (df['keff_change'] / df['keff'].iloc[0]) * 100
        
        # 保存到Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Results', index=False)
            
            # 添加统计摘要
            summary_data = {
                '项目': ['最小keff', '最大keff', '平均keff', 'keff变化范围', '最大变化百分比'],
                '值': [
                    df['keff'].min(),
                    df['keff'].max(),
                    df['keff'].mean(),
                    df['keff'].max() - df['keff'].min(),
                    df['keff_change_percent'].abs().max()
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"结果已保存到: {filename}")
        
        # 打印简要统计
        print("\n=== 结果统计 ===")
        print(f"参数值范围: {df['parameter_value'].min():.2E} - {df['parameter_value'].max():.2E}")
        print(f"keff值范围: {df['keff'].min():.6f} - {df['keff'].max():.6f}")
        print(f"keff变化范围: {df['keff'].max() - df['keff'].min():.6f}")
        print(f"最大变化百分比: {df['keff_change_percent'].abs().max():.4f}%")

def main():
    """主函数"""
    # 创建自动化对象
    automation = KeffStudyAutomation()
    
    # 检查必要文件是否存在
    if not os.path.exists(automation.original_file):
        print(f"错误：找不到输入文件 {automation.original_file}")
        return
    
    if not os.path.exists(automation.program_path):
        print(f"错误：找不到程序文件 {automation.program_path}")
        return
    
    # 生成参数值（可以自定义）
    parameter_values = automation.generate_parameter_values(
        start=1e-8,    # 起始值
        end=9e-7,      # 结束值
        num_points=9   # 点数
    )
    
    print("将要使用的参数值:")
    for i, val in enumerate(parameter_values, 1):
        print(f"  {i}: {val:.6E}")
    
    # 确认继续
    response = input("\n是否继续运行研究？(y/n): ")
    if response.lower() != 'y':
        print("已取消")
        return
    
    # 运行研究
    automation.run_study(parameter_values)
    
    # 保存结果
    automation.save_results()

if __name__ == "__main__":
    main() 