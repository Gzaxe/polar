#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单示例：读取fort.16文件并提取特定theta值的数据
"""

import numpy as np
from read_fort16 import read_fort16, extract_specific_theta

def main():
    print("读取fort.16文件...")
    
    # 读取fort.16文件
    data_blocks = read_fort16('fort.16')
    
    print(f"成功读取 {len(data_blocks)} 个数据块")
    
    if not data_blocks:
        print("错误：未能读取到任何数据")
        return
    
    # 显示第一个和最后一个能量值
    first_energy = data_blocks[0]['energy']
    last_energy = data_blocks[-1]['energy']
    print(f"能量范围: {first_energy} - {last_energy}")
    
    # 显示theta值的数量
    num_theta = len(data_blocks[0]['theta'])
    print(f"Theta点数: {num_theta}")
    
    # 提取特定theta值的数据
    target_theta = 90.0  # 目标theta值
    print(f"\n提取theta = {target_theta}° 的数据:")
    
    # 提取sigma列的数据
    sigma_data = extract_specific_theta(data_blocks, target_theta, 'sigma')
    print(f"Sigma数据 (前10个):")
    for i, (energy, value) in enumerate(sigma_data[:10]):
        print(f"  能量: {energy:6.2f}, Sigma: {value:8.4f}")
    
    if len(sigma_data) > 10:
        print(f"  ... 还有 {len(sigma_data)-10} 个数据点")
    
    # 提取其他列的数据
    iT11_data = extract_specific_theta(data_blocks, target_theta, 'iT11')
    print(f"\niT11数据 (前10个):")
    for i, (energy, value) in enumerate(iT11_data[:10]):
        print(f"  能量: {energy:6.2f}, iT11: {value:8.4f}")
    
    # 用户可以输入自定义theta值
    print("\n" + "="*50)
    print("您可以输入任意theta值来提取数据")
    
    try:
        user_input = input("请输入要提取的theta值 (默认90.0): ").strip()
        if user_input:
            user_theta = float(user_input)
        else:
            user_theta = 90.0
        
        column_input = input("请输入要提取的列 (sigma/iT11/T20/T21/T22/Kyy，默认sigma): ").strip()
        if column_input in ['sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy']:
            column = column_input
        else:
            column = 'sigma'
        
        extracted_data = extract_specific_theta(data_blocks, user_theta, column)
        
        print(f"\n{column}列在theta={user_theta}°的数据:")
        for energy, value in extracted_data:
            print(f"  能量: {energy:6.2f}, {column}: {value:8.4f}")
            
    except ValueError:
        print("输入无效，使用默认值")
    except KeyboardInterrupt:
        print("\n程序被用户中断")

if __name__ == "__main__":
    main()