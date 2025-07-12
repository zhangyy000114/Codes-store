#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数值预览工具 - 双参数版本
帮助用户理解不同跨度设置下的双参数分布
"""

import math

def generate_parameter_values(start, end, num_points):
    """生成参数值序列（对数均匀分布）"""
    log_start = math.log10(start)
    log_end = math.log10(end)
    step = (log_end - log_start) / (num_points - 1)
    
    values = []
    for i in range(num_points):
        log_value = log_start + i * step
        values.append(10 ** log_value)
    
    return values

def analyze_span(start, end, num_points):
    """分析跨度特征"""
    abs_span = end - start
    relative_span = end / start
    log_span = math.log10(end) - math.log10(start)
    
    print(f"跨度分析:")
    print(f"  绝对跨度: {abs_span:.2E}")
    print(f"  相对倍数: {relative_span:.1f}倍")
    print(f"  对数跨度: {log_span:.3f} (数量级)")
    print()

def preview_parameters():
    """参数预览主函数"""
    print("VSOP KEFF 参数值预览工具 - 双参数版本")
    print("=" * 60)
    print("本工具将预览双参数研究的参数分布：")
    print("  - 第87行第2个数据（主参数）")
    print("  - 第92行第2个数据（从参数，比例 = 主参数 / 1.59）")
    print("  - 比例关系：7.95:5")
    print("=" * 60)
    
    # 比例常数
    ratio = 7.95 / 5.0
    
    # 预设方案
    presets = [
        ("默认设置", 1e-8, 9e-7, 9),
        ("精细研究", 3e-8, 4e-8, 11),
        ("中等跨度", 1e-8, 2e-7, 15),
        ("大跨度探索", 5e-9, 2e-7, 20),
        ("对数扫描", 1e-9, 1e-6, 10)
    ]
    
    print("\n预设方案:")
    for i, (name, start, end, points) in enumerate(presets, 1):
        print(f"  {i}. {name}")
    print(f"  {len(presets)+1}. 自定义设置")
    
    while True:
        try:
            choice = int(input(f"\n请选择方案 (1-{len(presets)+1}): "))
            if 1 <= choice <= len(presets):
                name, start, end, num_points = presets[choice-1]
                print(f"\n选择方案: {name}")
                break
            elif choice == len(presets) + 1:
                print("\n自定义设置:")
                start = float(input("第87行起始值: "))
                end = float(input("第87行结束值: "))
                num_points = int(input("计算点数: "))
                
                if start >= end:
                    print("错误：起始值必须小于结束值")
                    continue
                if num_points < 2:
                    print("错误：计算点数必须大于等于2")
                    continue
                break
            else:
                print("无效选择，请重新输入")
        except ValueError:
            print("输入错误，请输入数字")
    
    print(f"\n参数设置:")
    print(f"  第87行起始值: {start:.2E}")
    print(f"  第87行结束值: {end:.2E}")
    print(f"  计算点数: {num_points}")
    print(f"  比例关系: 7.95:5 = {ratio:.3f}")
    print()
    
    # 分析跨度
    analyze_span(start, end, num_points)
    
    # 生成并显示参数值
    values = generate_parameter_values(start, end, num_points)
    
    print(f"生成的{len(values)}个双参数值组合:")
    print("-" * 80)
    print("序号 | 第87行参数值    | 第92行参数值    | 比例验证  | 步进倍数")
    print("-" * 80)
    
    for i, val in enumerate(values, 1):
        val_2 = val / ratio
        ratio_check = val / val_2
        
        if i > 1:
            step = val / values[i-2] if i > 1 else 0
            step_str = f"×{step:.2f}"
        else:
            step_str = "起始点"
        
        print(f"{i:2d}   | {val:.6E} | {val_2:.6E} | {ratio_check:.3f}    | {step_str}")
    
    # 第92行参数值的统计
    values_2 = [val / ratio for val in values]
    
    print(f"\n双参数统计:")
    print(f"  第87行参数值范围: {min(values):.2E} - {max(values):.2E}")
    print(f"  第92行参数值范围: {min(values_2):.2E} - {max(values_2):.2E}")
    print(f"  第87行最小步进倍数: {min(values[i]/values[i-1] for i in range(1, len(values))):.3f}")
    print(f"  第87行最大步进倍数: {max(values[i]/values[i-1] for i in range(1, len(values))):.3f}")
    
    # 验证比例关系
    ratios = [values[i] / values_2[i] for i in range(len(values))]
    ratio_std = math.sqrt(sum((r - ratio)**2 for r in ratios) / len(ratios))
    print(f"  比例关系标准差: {ratio_std:.6f} (应接近0)")
    
    # 估算运行时间
    estimated_time = num_points * 2  # 每个点约2分钟
    print(f"\n运行时间估算:")
    print(f"  预计总运行时间: {estimated_time}分钟 ({estimated_time/60:.1f}小时)")
    
    if estimated_time > 60:
        print(f"  建议分批运行，每批约30分钟（15个点）")
        batch_size = 15
        num_batches = (num_points + batch_size - 1) // batch_size
        print(f"  推荐分为{num_batches}批运行")
    
    # 参数分布可视化（文本版）
    print(f"\n第87行参数值分布可视化:")
    print("  " + "起始值".ljust(12) + "分布区间".ljust(40) + "结束值")
    
    # 创建简单的文本分布图
    visual_line = "  |"
    for i in range(len(values)):
        if i == 0:
            visual_line += "●"
        elif i == len(values) - 1:
            visual_line += "●"
        else:
            visual_line += "○"
        if i < len(values) - 1:
            visual_line += "─" * 3
    visual_line += "|"
    print(visual_line)
    print(f"  {start:.1E}".ljust(14) + " " * 30 + f"{end:.1E}")
    
    # 建议
    print(f"\n建议:")
    if num_points <= 5:
        print("  ⚠️  点数较少，可能无法充分覆盖参数空间")
    elif num_points > 20:
        print("  ⚠️  点数较多，运行时间可能很长")
    else:
        print("  ✅ 点数设置合理")
    
    if log_span := math.log10(end) - math.log10(start) > 3:
        print("  ⚠️  跨度很大，建议分段研究")
    elif log_span < 0.5:
        print("  ⚠️  跨度较小，可能需要更精细的研究")
    else:
        print("  ✅ 跨度设置合理")
    
    # 导出选项
    export_choice = input("\n是否导出参数列表到文件？(y/n): ")
    if export_choice.lower() == 'y':
        filename = f"parameter_preview_{num_points}points.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("VSOP KEFF 双参数值预览\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"参数设置:\n")
            f.write(f"  第87行起始值: {start:.2E}\n")
            f.write(f"  第87行结束值: {end:.2E}\n")
            f.write(f"  计算点数: {num_points}\n")
            f.write(f"  比例关系: 7.95:5 = {ratio:.3f}\n\n")
            
            f.write("参数值列表:\n")
            f.write("序号\t第87行参数值\t第92行参数值\t比例验证\n")
            for i, val in enumerate(values, 1):
                val_2 = val / ratio
                ratio_check = val / val_2
                f.write(f"{i}\t{val:.6E}\t{val_2:.6E}\t{ratio_check:.3f}\n")
            
            f.write(f"\n预计运行时间: {estimated_time}分钟 ({estimated_time/60:.1f}小时)\n")
        
        print(f"参数列表已导出到: {filename}")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    preview_parameters() 