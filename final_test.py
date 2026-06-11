#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终测试程序：验证fort.16文件读取和数据提取功能
"""

import numpy as np
from read_fort16 import (
    read_fort16, 
    extract_specific_theta, 
    extract_same_theta_different_energy,
    save_same_theta_different_energy,
    create_energy_theta_function,
    print_available_energies,
    print_theta_range
)

def main():
    print("="*60)
    print("Fort.16 文件读取和数据提取工具 - 最终测试")
    print("="*60)
    
    # 1. 读取文件
    print("\n1. 读取 fort.16 文件...")
    data_blocks = read_fort16('fort.16')
    print(f"   成功读取 {len(data_blocks)} 个数据块")
    
    if not data_blocks:
        print("   错误：未能读取到任何数据")
        return
    
    # 2. 显示基本信息
    print("\n2. 数据基本信息:")
    print_available_energies(data_blocks)
    print_theta_range(data_blocks)
    
    # 3. 提取特定theta值的数据
    print("\n3. 提取特定theta值的数据:")
    target_theta = 90.0
    sigma_data = extract_specific_theta(data_blocks, target_theta, 'sigma')
    print(f"   在theta={target_theta}°提取sigma数据: {len(sigma_data)} 个数据点")
    
    iT11_data = extract_specific_theta(data_blocks, target_theta, 'iT11')
    print(f"   在theta={target_theta}°提取iT11数据: {len(iT11_data)} 个数据点")
    
    # 4. 显示部分提取的数据
    print(f"\n   Sigma数据示例 (前5个):")
    for i, (energy, value) in enumerate(sigma_data[:5]):
        print(f"     能量: {energy:6.2f}, Sigma: {value:8.4f}")
    
    # 5. 创建能量-角度函数矩阵
    print(f"\n4. 创建能量-角度函数矩阵...")
    matrix, energies, thetas = create_energy_theta_function(data_blocks, 'sigma')
    print(f"   矩阵形状: {matrix.shape} (能量数: {len(energies)}, 角度数: {len(thetas)})")
    
    # 6. 提取相同theta值不同能量的数据
    print(f"\n5. 提取相同theta值不同能量的数据...")
    energy_theta_array = extract_same_theta_different_energy(data_blocks, target_theta, 'sigma')
    print(f"   提取结果形状: {energy_theta_array.shape}")
    
    # 7. 保存数据到文件
    print(f"\n6. 保存数据到文件...")
    save_filename = f"theta_{target_theta}_sigma_data.txt"
    save_same_theta_different_energy(data_blocks, target_theta, save_filename, 'sigma')
    print(f"   数据已保存到: {save_filename}")
    
    # 8. 测试其他列
    print(f"\n7. 测试其他数据列...")
    for col in ['iT11', 'T20', 'T21', 'T22', 'Kyy']:
        col_data = extract_specific_theta(data_blocks, target_theta, col)
        print(f"   {col}列数据: {len(col_data)} 个数据点")
    
    print(f"\n8. 测试完成！")
    print(f"   - 成功读取了包含{len(data_blocks)}个能量点的数据")
    print(f"   - 每个数据块包含{len(data_blocks[0]['theta'])}个theta值")
    print(f"   - 成功提取了特定theta值({target_theta}°)的数据")
    print(f"   - 成功保存了提取的数据到文件")
    print("="*60)

if __name__ == "__main__":
    main()