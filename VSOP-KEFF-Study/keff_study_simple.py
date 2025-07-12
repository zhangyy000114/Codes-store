#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSOP KEFF自动化研究脚本 - 简化版本
仅使用Python标准库，无需外部依赖
"""

import os
import subprocess
import shutil
import csv
import math
import time

class KeffStudySimple:
    def __init__(self):
        self.original_file = "first_begin.i"
        self.program_path = "VSOP99_11-MS.exe"
        self.target_line_1 = 77  # 第1个目标行号
        self.target_line_2 = 92  # 第2个目标行号
        self.ratio = 7.95 / 5.0  # 第1个数据与第2个数据的比例 (7.95:5)
        self.results = []
        
    def backup_original_file(self):
        """备份原始文件"""
        backup_name = f"{self.original_file}.backup"
        if not os.path.exists(backup_name):
            shutil.copy2(self.original_file, backup_name)
            print(f"已备份原始文件到: {backup_name}")
    
    def modify_input_file(self, new_value_1):
        """修改输入文件中的参数值
        
        Args:
            new_value_1: 第77行第2个数据的新值
        """
        try:
            with open(self.original_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # 如果UTF-8失败，尝试其他编码
            with open(self.original_file, 'r', encoding='gbk') as f:
                lines = f.readlines()
        
        # 根据比例计算第2个数据的值
        new_value_2 = new_value_1 / self.ratio  # 第2个数据 = 第1个数据 / (7.95/5)
        
        success = True
        
        # 修改第77行的第2个数据
        target_line_1_index = self.target_line_1 - 1
        if target_line_1_index < len(lines):
            original_line_1 = lines[target_line_1_index]
            parts_1 = original_line_1.split()
            if len(parts_1) >= 2:
                # 替换第2个数据，保持格式一致
                new_line_1 = f"   {parts_1[0]}    {new_value_1:.6E}                                                        D 17\n"
                lines[target_line_1_index] = new_line_1
                print(f"已修改第{self.target_line_1}行参数值为: {new_value_1:.6E}")
            else:
                print(f"错误：无法解析第{self.target_line_1}行")
                success = False
        else:
            print(f"错误：第{self.target_line_1}行超出文件范围")
            success = False
        
        # 修改第92行的第2个数据
        target_line_2_index = self.target_line_2 - 1
        if target_line_2_index < len(lines):
            original_line_2 = lines[target_line_2_index]
            parts_2 = original_line_2.split()
            if len(parts_2) >= 2:
                # 替换第2个数据，保持格式一致
                new_line_2 = f"   {parts_2[0]}    {new_value_2:.6E}                                                        D 17\n"
                lines[target_line_2_index] = new_line_2
                print(f"已修改第{self.target_line_2}行参数值为: {new_value_2:.6E}")
            else:
                print(f"错误：无法解析第{self.target_line_2}行")
                success = False
        else:
            print(f"错误：第{self.target_line_2}行超出文件范围")
            success = False
        
        # 验证比例关系
        if success:
            actual_ratio = new_value_1 / new_value_2
            expected_ratio = self.ratio
            print(f"比例验证: {new_value_1:.6E} / {new_value_2:.6E} = {actual_ratio:.3f} (期望: {expected_ratio:.3f})")
        
        if success:
            # 写回文件
            try:
                with open(self.original_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
            except UnicodeDecodeError:
                with open(self.original_file, 'w', encoding='gbk') as f:
                    f.writelines(lines)
            
            print(f"已成功修改两个参数值，保持比例 7.95:5")
            return True
        else:
            print("修改失败")
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
            stdout, stderr = process.communicate(input=input_sequence, timeout=600)  # 10分钟超时
            
            if process.returncode == 0:
                print(f"程序运行成功，输出文件: {output_filename}")
                return output_filename
            else:
                print(f"程序运行失败，返回码: {process.returncode}")
                if stderr:
                    print(f"错误信息: {stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("程序运行超时（10分钟）")
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
        log_start = math.log10(start)
        log_end = math.log10(end)
        step = (log_end - log_start) / (num_points - 1)
        
        values = []
        for i in range(num_points):
            log_value = log_start + i * step
            values.append(10 ** log_value)
        
        return values
    
    def run_study(self, parameter_values=None):
        """运行完整的研究"""
        if parameter_values is None:
            parameter_values = self.generate_parameter_values()
        
        print(f"开始keff研究，共{len(parameter_values)}个参数值")
        print(f"参数范围: {parameter_values[0]:.2E} 到 {parameter_values[-1]:.2E}")
        print(f"比例关系: 第77行:第92行 = 7.95:5")
        
        # 备份原始文件
        self.backup_original_file()
        
        start_time = time.time()
        
        for i, value in enumerate(parameter_values, 1):
            print(f"\n=== 运行 {i}/{len(parameter_values)}: 第77行参数值 = {value:.6E} ===")
            value_2 = value / self.ratio
            print(f"    对应第92行参数值 = {value_2:.6E}")
            iteration_start = time.time()
            
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
                    'parameter_value_1': value,
                    'parameter_value_2': value_2,
                    'keff': keff_value,
                    'output_file': output_file
                })
            
            iteration_time = time.time() - iteration_start
            print(f"完成 {i}/{len(parameter_values)}, 用时: {iteration_time:.1f}秒")
        
        # 恢复原始文件
        self.restore_original_file()
        
        total_time = time.time() - start_time
        print(f"\n研究完成！共获得{len(self.results)}个有效结果，总用时: {total_time/60:.1f}分钟")
        
    def restore_original_file(self):
        """恢复原始文件"""
        backup_name = f"{self.original_file}.backup"
        if os.path.exists(backup_name):
            shutil.copy2(backup_name, self.original_file)
            print("已恢复原始文件")
    
    def save_results_csv(self, filename="keff_study_results.csv"):
        """保存结果到CSV文件"""
        if not self.results:
            print("没有结果需要保存")
            return
        
        # 按第1个参数值排序
        self.results.sort(key=lambda x: x['parameter_value_1'])
        
        # 计算统计信息
        keff_values = [r['keff'] for r in self.results]
        first_keff = keff_values[0]
        
        # 写入CSV文件
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['序号', '第77行参数值', '第92行参数值', 'keff值', 'keff变化', 'keff变化百分比(%)', '输出文件']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, result in enumerate(self.results, 1):
                keff_change = result['keff'] - first_keff
                keff_change_percent = (keff_change / first_keff) * 100
                
                writer.writerow({
                    '序号': i,
                    '第77行参数值': f"{result['parameter_value_1']:.6E}",
                    '第92行参数值': f"{result['parameter_value_2']:.6E}",
                    'keff值': f"{result['keff']:.6f}",
                    'keff变化': f"{keff_change:.6f}",
                    'keff变化百分比(%)': f"{keff_change_percent:.4f}",
                    '输出文件': result['output_file']
                })
        
        print(f"结果已保存到: {filename}")
        
        # 保存统计摘要
        summary_filename = "keff_study_summary.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("KEFF研究结果统计摘要\n")
            f.write("=" * 40 + "\n\n")
            f.write("参数设置:\n")
            f.write(f"  第77行参数值范围: {min(r['parameter_value_1'] for r in self.results):.2E} - {max(r['parameter_value_1'] for r in self.results):.2E}\n")
            f.write(f"  第92行参数值范围: {min(r['parameter_value_2'] for r in self.results):.2E} - {max(r['parameter_value_2'] for r in self.results):.2E}\n")
            f.write(f"  比例关系: 7.95:5 = {self.ratio:.3f}\n\n")
            f.write("结果统计:\n")
            f.write(f"  keff值范围: {min(keff_values):.6f} - {max(keff_values):.6f}\n")
            f.write(f"  keff变化范围: {max(keff_values) - min(keff_values):.6f}\n")
            
            max_change_percent = max(abs((k - first_keff) / first_keff * 100) for k in keff_values)
            f.write(f"  最大变化百分比: {max_change_percent:.4f}%\n")
            f.write(f"  平均keff值: {sum(keff_values) / len(keff_values):.6f}\n")
            f.write(f"  总计算次数: {len(self.results)}\n")
        
        print(f"统计摘要已保存到: {summary_filename}")
        
        # 打印简要统计
        print("\n=== 结果统计 ===")
        print(f"第77行参数值范围: {min(r['parameter_value_1'] for r in self.results):.2E} - {max(r['parameter_value_1'] for r in self.results):.2E}")
        print(f"第92行参数值范围: {min(r['parameter_value_2'] for r in self.results):.2E} - {max(r['parameter_value_2'] for r in self.results):.2E}")
        print(f"keff值范围: {min(keff_values):.6f} - {max(keff_values):.6f}")
        print(f"keff变化范围: {max(keff_values) - min(keff_values):.6f}")
        max_change_percent = max(abs((k - first_keff) / first_keff * 100) for k in keff_values)
        print(f"最大变化百分比: {max_change_percent:.4f}%")

def main():
    """主函数"""
    print("VSOP KEFF 自动化研究脚本 - 双参数版本")
    print("=" * 50)
    print("本脚本将同时修改两个参数:")
    print("  - 第77行第2个数据")
    print("  - 第92行第2个数据")
    print("  - 保持比例关系 7.95:5")
    print("=" * 50)
    
    # 创建自动化对象
    automation = KeffStudySimple()
    
    # 检查必要文件是否存在
    if not os.path.exists(automation.original_file):
        print(f"错误：找不到输入文件 {automation.original_file}")
        input("按回车键退出...")
        return
    
    if not os.path.exists(automation.program_path):
        print(f"错误：找不到程序文件 {automation.program_path}")
        input("按回车键退出...")
        return
    
    # 设置参数
    while True:
        try:
            print("\n请设置研究参数（第77行参数值）:")
            start_val = float(input("起始值 (默认 1e-8): ") or "1e-8")
            end_val = float(input("结束值 (默认 9e-7): ") or "9e-7")
            num_points = int(input("计算点数 (默认 9): ") or "9")
            
            if start_val >= end_val:
                print("错误：起始值必须小于结束值")
                continue
            if num_points < 2:
                print("错误：计算点数必须大于等于2")
                continue
                
            break
        except ValueError:
            print("错误：请输入有效的数值")
    
    # 生成参数值
    parameter_values = automation.generate_parameter_values(
        start=start_val,
        end=end_val,
        num_points=num_points
    )
    
    print(f"\n将要使用的{len(parameter_values)}个参数值组合:")
    print("序号 | 第77行参数值    | 第92行参数值    | 比例验证")
    print("-" * 55)
    for i, val in enumerate(parameter_values, 1):
        val_2 = val / automation.ratio
        ratio_check = val / val_2
        print(f"{i:2d}   | {val:.6E} | {val_2:.6E} | {ratio_check:.3f}")
    
    print(f"\n预计总运行时间: 约{len(parameter_values) * 2}分钟")
    
    # 确认继续
    response = input("\n是否继续运行研究？(y/n): ")
    if response.lower() != 'y':
        print("已取消")
        return
    
    # 运行研究
    automation.run_study(parameter_values)
    
    # 保存结果
    automation.save_results_csv()
    
    print("\n所有操作完成！")
    input("按回车键退出...")

if __name__ == "__main__":
    main() 