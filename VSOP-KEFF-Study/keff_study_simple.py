#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSOP KEFF自动化研究脚本 - 带可视化的简化版本
仅使用Python标准库，无需外部依赖
"""

import os
import subprocess
import shutil
import csv
import math
import time
import sys

# 尝试导入matplotlib进行可视化
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
    print("检测到matplotlib，将启用可视化功能")
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("未检测到matplotlib，将以纯文本模式运行")
    print("如需可视化功能，请安装: pip install matplotlib")

class KeffStudySimple:
    def __init__(self):
        self.original_file = "first_begin.i"
        self.program_path = "VSOP99_11-MS.exe"
        self.target_line_1 = 87  # 第1个目标行号
        self.target_line_2 = 92  # 第2个目标行号
        self.ratio = 7.95 / 5.0  # 第1个数据与第2个数据的比例 (7.95:5)
        self.results = []
        
        # 可视化相关
        self.enable_visualization = MATPLOTLIB_AVAILABLE
        self.fig = None
        self.ax_progress = None
        self.ax_keff = None
        self.ax_params = None
        
    def init_visualization(self, total_runs):
        """初始化可视化窗口"""
        if not self.enable_visualization:
            return
            
        # 创建图形窗口
        self.fig = plt.figure(figsize=(15, 10))
        self.fig.suptitle('VSOP KEFF 研究实时监控', fontsize=16, fontweight='bold')
        
        # 创建子图
        gs = self.fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 进度条
        self.ax_progress = self.fig.add_subplot(gs[0, :])
        self.ax_progress.set_title('运行进度', fontsize=14)
        self.ax_progress.set_xlim(0, total_runs)
        self.ax_progress.set_ylim(-0.5, 0.5)
        self.ax_progress.set_xlabel('计算次数')
        
        # KEFF值变化图
        self.ax_keff = self.fig.add_subplot(gs[1, 0])
        self.ax_keff.set_title('KEFF值变化', fontsize=14)
        self.ax_keff.set_xlabel('参数值 (第87行)')
        self.ax_keff.set_ylabel('KEFF值')
        self.ax_keff.grid(True, alpha=0.3)
        
        # 参数关系图
        self.ax_params = self.fig.add_subplot(gs[1, 1])
        self.ax_params.set_title('双参数关系 (7.95:5)', fontsize=14)
        self.ax_params.set_xlabel('第87行参数值')
        self.ax_params.set_ylabel('第92行参数值')
        self.ax_params.grid(True, alpha=0.3)
        
        # 统计信息区域
        self.ax_stats = self.fig.add_subplot(gs[2, :])
        self.ax_stats.set_title('实时统计信息', fontsize=14)
        self.ax_stats.axis('off')
        
        plt.ion()  # 开启交互模式
        plt.show()
        
    def update_progress_bar(self, current, total, status_text=""):
        """更新进度条"""
        if not self.enable_visualization or self.ax_progress is None:
            return
            
        self.ax_progress.clear()
        self.ax_progress.set_title(f'运行进度 - {status_text}', fontsize=14)
        self.ax_progress.set_xlim(0, total)
        self.ax_progress.set_ylim(-0.5, 0.5)
        self.ax_progress.set_xlabel('计算次数')
        
        # 绘制进度条
        progress_width = current / total * total
        progress_bar = patches.Rectangle((0, -0.2), progress_width, 0.4, 
                                       facecolor='green', alpha=0.7)
        self.ax_progress.add_patch(progress_bar)
        
        # 添加进度文本
        progress_percent = (current / total) * 100 if total > 0 else 0
        self.ax_progress.text(total/2, 0, f'{current}/{total} ({progress_percent:.1f}%)', 
                             ha='center', va='center', fontsize=12, fontweight='bold')
        
        plt.draw()
        plt.pause(0.001)
        
    def update_keff_plot(self):
        """更新KEFF值图表"""
        if not self.enable_visualization or self.ax_keff is None or len(self.results) == 0:
            return
            
        # 提取数据
        param_values = [r['parameter_value_1'] for r in self.results]
        keff_values = [r['keff'] for r in self.results]
        
        self.ax_keff.clear()
        self.ax_keff.set_title('KEFF值变化', fontsize=14)
        self.ax_keff.set_xlabel('参数值 (第87行)')
        self.ax_keff.set_ylabel('KEFF值')
        self.ax_keff.grid(True, alpha=0.3)
        
        # 绘制数据点和连线
        self.ax_keff.plot(param_values, keff_values, 'bo-', linewidth=2, markersize=6)
        self.ax_keff.set_xscale('log')
        
        # 添加数值标签
        for i, (x, y) in enumerate(zip(param_values, keff_values)):
            self.ax_keff.annotate(f'{y:.4f}', (x, y), textcoords="offset points", 
                                xytext=(0,10), ha='center', fontsize=8)
        
        plt.draw()
        plt.pause(0.001)
        
    def update_params_plot(self):
        """更新参数关系图"""
        if not self.enable_visualization or self.ax_params is None or len(self.results) == 0:
            return
            
        # 提取数据
        param1_values = [r['parameter_value_1'] for r in self.results]
        param2_values = [r['parameter_value_2'] for r in self.results]
        
        self.ax_params.clear()
        self.ax_params.set_title('双参数关系 (7.95:5)', fontsize=14)
        self.ax_params.set_xlabel('第87行参数值')
        self.ax_params.set_ylabel('第92行参数值')
        self.ax_params.grid(True, alpha=0.3)
        
        # 绘制数据点和理论直线
        self.ax_params.plot(param1_values, param2_values, 'ro-', linewidth=2, markersize=6, label='实际值')
        
        # 绘制理论比例线
        if param1_values:
            x_theory = [min(param1_values), max(param1_values)]
            y_theory = [x / self.ratio for x in x_theory]
            self.ax_params.plot(x_theory, y_theory, 'b--', linewidth=2, alpha=0.7, label='理论比例线')
        
        self.ax_params.set_xscale('log')
        self.ax_params.set_yscale('log')
        self.ax_params.legend()
        
        plt.draw()
        plt.pause(0.001)
        
    def update_stats_display(self):
        """更新统计信息显示"""
        if not self.enable_visualization or self.ax_stats is None or len(self.results) == 0:
            return
            
        self.ax_stats.clear()
        self.ax_stats.set_title('实时统计信息', fontsize=14)
        self.ax_stats.axis('off')
        
        # 计算统计信息
        keff_values = [r['keff'] for r in self.results]
        param1_values = [r['parameter_value_1'] for r in self.results]
        param2_values = [r['parameter_value_2'] for r in self.results]
        
        min_keff = min(keff_values)
        max_keff = max(keff_values)
        avg_keff = sum(keff_values) / len(keff_values)
        keff_range = max_keff - min_keff
        
        if len(keff_values) > 1:
            first_keff = keff_values[0]
            max_change_percent = max(abs((k - first_keff) / first_keff * 100) for k in keff_values)
        else:
            max_change_percent = 0
        
        # 创建统计信息文本
        stats_text = f"""
当前结果数: {len(self.results)}
        
KEFF值统计:
• 最小值: {min_keff:.6f}
• 最大值: {max_keff:.6f}
• 平均值: {avg_keff:.6f}
• 变化范围: {keff_range:.6f}
• 最大变化: {max_change_percent:.4f}%

参数范围:
• 第87行: {min(param1_values):.2E} - {max(param1_values):.2E}
• 第92行: {min(param2_values):.2E} - {max(param2_values):.2E}
• 比例验证: {self.ratio:.3f}
        """
        
        self.ax_stats.text(0.1, 0.9, stats_text, transform=self.ax_stats.transAxes, 
                          fontsize=11, verticalalignment='top', fontfamily='monospace')
        
        plt.draw()
        plt.pause(0.001)

    def print_progress_bar(self, current, total, bar_length=50):
        """打印文本进度条（用于无图形界面模式）"""
        if self.enable_visualization:
            return
            
        percent = current / total
        filled_length = int(bar_length * percent)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stdout.write(f'\r进度: |{bar}| {current}/{total} ({percent:.1%})')
        sys.stdout.flush()

    def backup_original_file(self):
        """备份原始文件"""
        backup_name = f"{self.original_file}.backup"
        if not os.path.exists(backup_name):
            shutil.copy2(self.original_file, backup_name)
            print(f"已备份原始文件到: {backup_name}")
    
    def modify_input_file(self, new_value_1):
        """修改输入文件中的参数值
        
        Args:
            new_value_1: 第87行第2个数据的新值
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
        print(f"比例关系: 第87行:第92行 = 7.95:5")
        
        # 初始化可视化
        self.init_visualization(len(parameter_values))
        
        # 备份原始文件
        self.backup_original_file()
        
        start_time = time.time()
        
        for i, value in enumerate(parameter_values, 1):
            print(f"\n=== 运行 {i}/{len(parameter_values)}: 第87行参数值 = {value:.6E} ===")
            value_2 = value / self.ratio
            print(f"    对应第92行参数值 = {value_2:.6E}")
            iteration_start = time.time()
            
            # 更新进度条
            self.update_progress_bar(i-1, len(parameter_values), f"正在处理第{i}个参数值")
            self.print_progress_bar(i-1, len(parameter_values))
            
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
                
                # 更新实时图表
                self.update_keff_plot()
                self.update_params_plot()
                self.update_stats_display()
            
            iteration_time = time.time() - iteration_start
            print(f"完成 {i}/{len(parameter_values)}, 用时: {iteration_time:.1f}秒")
        
        # 最终更新进度条
        self.update_progress_bar(len(parameter_values), len(parameter_values), "计算完成")
        self.print_progress_bar(len(parameter_values), len(parameter_values))
        
        # 恢复原始文件
        self.restore_original_file()
        
        total_time = time.time() - start_time
        print(f"\n\n研究完成！共获得{len(self.results)}个有效结果，总用时: {total_time/60:.1f}分钟")
        
        # 生成最终图表
        self.generate_final_plots()
        
    def generate_final_plots(self):
        """生成最终的分析图表"""
        if not self.enable_visualization or len(self.results) == 0:
            return
            
        # 创建最终分析图表
        fig_final = plt.figure(figsize=(16, 12))
        fig_final.suptitle('VSOP KEFF 研究结果分析', fontsize=18, fontweight='bold')
        
        # 准备数据
        param1_values = [r['parameter_value_1'] for r in self.results]
        param2_values = [r['parameter_value_2'] for r in self.results]
        keff_values = [r['keff'] for r in self.results]
        
        # 按参数值排序
        sorted_data = sorted(zip(param1_values, param2_values, keff_values))
        param1_sorted, param2_sorted, keff_sorted = zip(*sorted_data)
        
        # 子图1: KEFF vs 第87行参数值
        ax1 = fig_final.add_subplot(2, 3, 1)
        ax1.plot(param1_sorted, keff_sorted, 'bo-', linewidth=2, markersize=8)
        ax1.set_xlabel('第87行参数值')
        ax1.set_ylabel('KEFF值')
        ax1.set_title('KEFF vs 第87行参数值')
        ax1.set_xscale('log')
        ax1.grid(True, alpha=0.3)
        
        # 子图2: KEFF vs 第92行参数值
        ax2 = fig_final.add_subplot(2, 3, 2)
        ax2.plot(param2_sorted, keff_sorted, 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('第92行参数值')
        ax2.set_ylabel('KEFF值')
        ax2.set_title('KEFF vs 第92行参数值')
        ax2.set_xscale('log')
        ax2.grid(True, alpha=0.3)
        
        # 子图3: 参数关系验证
        ax3 = fig_final.add_subplot(2, 3, 3)
        ax3.plot(param1_sorted, param2_sorted, 'go-', linewidth=2, markersize=8, label='实际值')
        # 理论直线
        x_theory = np.array(param1_sorted)
        y_theory = x_theory / self.ratio
        ax3.plot(x_theory, y_theory, 'b--', linewidth=2, alpha=0.7, label='理论比例线')
        ax3.set_xlabel('第87行参数值')
        ax3.set_ylabel('第92行参数值')
        ax3.set_title('参数关系验证 (7.95:5)')
        ax3.set_xscale('log')
        ax3.set_yscale('log')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 子图4: KEFF变化率
        ax4 = fig_final.add_subplot(2, 3, 4)
        if len(keff_sorted) > 1:
            keff_changes = []
            param1_centers = []
            for i in range(len(keff_sorted) - 1):
                change = (keff_sorted[i+1] - keff_sorted[i]) / keff_sorted[i] * 100
                keff_changes.append(change)
                param1_centers.append((param1_sorted[i] + param1_sorted[i+1]) / 2)
            
            ax4.plot(param1_centers, keff_changes, 'mo-', linewidth=2, markersize=8)
            ax4.set_xlabel('第87行参数值')
            ax4.set_ylabel('KEFF变化率 (%)')
            ax4.set_title('KEFF变化率')
            ax4.set_xscale('log')
            ax4.grid(True, alpha=0.3)
            ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # 子图5: KEFF值分布直方图
        ax5 = fig_final.add_subplot(2, 3, 5)
        ax5.hist(keff_values, bins=min(10, len(keff_values)), alpha=0.7, edgecolor='black')
        ax5.set_xlabel('KEFF值')
        ax5.set_ylabel('频次')
        ax5.set_title('KEFF值分布')
        ax5.grid(True, alpha=0.3)
        
        # 子图6: 统计信息表格
        ax6 = fig_final.add_subplot(2, 3, 6)
        ax6.axis('off')
        
        # 计算统计信息
        min_keff = min(keff_values)
        max_keff = max(keff_values)
        avg_keff = sum(keff_values) / len(keff_values)
        std_keff = math.sqrt(sum((k - avg_keff)**2 for k in keff_values) / len(keff_values))
        
        first_keff = keff_sorted[0]
        max_change_percent = max(abs((k - first_keff) / first_keff * 100) for k in keff_values)
        
        stats_text = f"""
统计信息:
━━━━━━━━━━━━━━━━
• 计算点数: {len(self.results)}
• KEFF 最小值: {min_keff:.6f}
• KEFF 最大值: {max_keff:.6f}
• KEFF 平均值: {avg_keff:.6f}
• KEFF 标准差: {std_keff:.6f}
• KEFF 变化范围: {max_keff - min_keff:.6f}
• 最大变化率: {max_change_percent:.4f}%

参数范围:
━━━━━━━━━━━━━━━━
• 第87行: {min(param1_values):.2E} 
  到 {max(param1_values):.2E}
• 第92行: {min(param2_values):.2E} 
  到 {max(param2_values):.2E}
• 比例关系: 7.95:5 = {self.ratio:.3f}
        """
        
        ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes, fontsize=11, 
                verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        # 保存图表
        plt.savefig('keff_study_analysis.png', dpi=300, bbox_inches='tight')
        print("分析图表已保存为: keff_study_analysis.png")
        
        # 显示图表
        plt.show()
        
        # 保持图表窗口打开
        if self.enable_visualization:
            input("按回车键关闭图表...")
            plt.close('all')

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
            fieldnames = ['序号', '第87行参数值', '第92行参数值', 'keff值', 'keff变化', 'keff变化百分比(%)', '输出文件']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, result in enumerate(self.results, 1):
                keff_change = result['keff'] - first_keff
                keff_change_percent = (keff_change / first_keff) * 100
                
                writer.writerow({
                    '序号': i,
                    '第87行参数值': f"{result['parameter_value_1']:.6E}",
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
            f.write(f"  第87行参数值范围: {min(r['parameter_value_1'] for r in self.results):.2E} - {max(r['parameter_value_1'] for r in self.results):.2E}\n")
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
    print("VSOP KEFF 自动化研究脚本 - 双参数可视化版本")
    print("=" * 50)
    print("本脚本将同时修改两个参数:")
    print("  - 第87行第2个数据")
    print("  - 第92行第2个数据")
    print("  - 保持比例关系 7.95:5")
    
    if MATPLOTLIB_AVAILABLE:
        print("  - 启用实时可视化功能")
    else:
        print("  - 无可视化功能（matplotlib未安装）")
    
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
    
    # 询问是否启用可视化
    if MATPLOTLIB_AVAILABLE:
        response = input("是否启用实时可视化功能？(y/n，默认y): ").lower()
        if response == 'n':
            automation.enable_visualization = False
            print("已禁用可视化功能")
    
    # 设置参数
    while True:
        try:
            print("\n请设置研究参数（第87行参数值）:")
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
    print("序号 | 第87行参数值    | 第92行参数值    | 比例验证")
    print("-" * 55)
    for i, val in enumerate(parameter_values, 1):
        val_2 = val / automation.ratio
        ratio_check = val / val_2
        print(f"{i:2d}   | {val:.6E} | {val_2:.6E} | {ratio_check:.3f}")
    
    print(f"\n预计总运行时间: 约{len(parameter_values) * 2}分钟")
    
    if automation.enable_visualization:
        print("提示: 运行过程中将显示实时图表监控")
    
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
    print("已生成以下文件:")
    print("  - keff_study_results.csv (详细结果)")
    print("  - keff_study_summary.txt (统计摘要)")
    if automation.enable_visualization:
        print("  - keff_study_analysis.png (分析图表)")
    
    input("按回车键退出...")

if __name__ == "__main__":
    main() 