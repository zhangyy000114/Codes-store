#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数值预览工具
帮助用户理解不同跨度设置下的参数分布
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
    print("VSOP KEFF 参数值预览工具")
    print("=" * 50)
    
    # 预设方案
    presets = [
        ("默认设置", 1e-8, 9e-7, 9),
        ("精细研究", 3e-8, 4e-8, 11),
        ("中等跨度", 1e-8, 2e-7, 15),
        ("大跨度探索", 5e-9, 2e-7, 20),
        ("对数扫描", 1e-9, 1e-6, 10)
    ]
    
    print("预设方案:")
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
                start = float(input("起始值: "))
                end = float(input("结束值: "))
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
    print(f"  起始值: {start:.2E}")
    print(f"  结束值: {end:.2E}")
    print(f"  计算点数: {num_points}")
    print()
    
    # 分析跨度
    analyze_span(start, end, num_points)
    
    # 生成并显示参数值
    values = generate_parameter_values(start, end, num_points)
    
    print(f"生成的{len(values)}个参数值:")
    print("-" * 40)
    for i, val in enumerate(values, 1):
        if i > 1:
            step = val / values[i-2] if i > 1 else 0
            print(f"  {i:2d}: {val:.6E}  (×{step:.2f})")
        else:
            print(f"  {i:2d}: {val:.6E}")
    
    print(f"\n总结:")
    print(f"  最小步进倍数: {min(values[i]/values[i-1] for i in range(1, len(values))):.3f}")
    print(f"  最大步进倍数: {max(values[i]/values[i-1] for i in range(1, len(values))):.3f}")
    
    # 估算运行时间
    estimated_time = num_points * 2  # 每个点约2分钟
    print(f"  预计运行时间: {estimated_time}分钟 ({estimated_time/60:.1f}小时)")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    preview_parameters() 