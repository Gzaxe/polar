import numpy as np
from read_fort16 import read_fort16, create_energy_theta_function, extract_same_theta_different_energy

def main():
    print("读取fort.16文件...")
    data_blocks = read_fort16('fort.16')
    
    print(f"找到 {len(data_blocks)} 个数据块")
    print(f"Theta范围: {data_blocks[0]['theta'][0]:.3f} 到 {data_blocks[0]['theta'][-1]:.3f}")
    print(f"Theta点数量: {len(data_blocks[0]['theta'])}")
    
    # 示例1：创建能量-角度函数矩阵
    print(f"\n=== 示例1: 创建能量-角度函数矩阵 ===")
    
    # 创建sigma列的能量-角度矩阵
    energy_theta_matrix, energies, thetas = create_energy_theta_function(data_blocks, 'sigma')
    
    print(f"能量-角度矩阵形状: {energy_theta_matrix.shape}")
    print(f"能量数量: {len(energies)}, Theta数量: {len(thetas)}")
    
    # 显示部分数据
    print(f"前5个能量值: {energies[:5]}")
    print(f"前5个theta值: {thetas[:5]}")
    
    # 显示矩阵的一部分
    print(f"能量-角度矩阵 (前5行x前5列):")
    print(energy_theta_matrix[:5, :5])
    
    # 示例2：提取相同theta值下不同能量的数据
    print(f"\n=== 示例2: 提取相同theta值下不同能量的数据 ===")
    
    target_theta = 90.0
    energy_value_array = extract_same_theta_different_energy(data_blocks, target_theta, 'sigma')
    
    print(f"Theta = {target_theta}° 下的能量-数值数组形状: {energy_value_array.shape}")
    print(f"前10个 (能量, Sigma值) 对:")
    for i in range(min(10, len(energy_value_array))):
        energy, value = energy_value_array[i]
        print(f"  {i+1:2d}. Energy: {energy:6.2f}, Sigma: {value:8.4f}")
    
    if len(energy_value_array) > 10:
        print(f"  ... 还有 {len(energy_value_array)-10} 个数据点")
    
    # 示例3：比较不同物理量的能量-角度矩阵
    print(f"\n=== 示例3: 不同物理量的能量-角度矩阵 ===")
    
    columns = ['sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy']
    for col in columns:
        matrix, _, _ = create_energy_theta_function(data_blocks, col)
        if matrix.size > 0:
            print(f"{col.upper()} 矩阵形状: {matrix.shape}")
            # 显示一些统计信息
            print(f"  最小值: {matrix.min():.6f}, 最大值: {matrix.max():.6f}, 平均值: {matrix.mean():.6f}")
        else:
            print(f"{col.upper()} 矩阵为空")
    
    # 示例4：提取多个theta值下不同能量的数据
    print(f"\n=== 示例4: 多个theta值下不同能量的数据 ===")
    
    thetas_to_extract = [0.01, 45.0, 90.0, 135.0, 179.99]
    for theta in thetas_to_extract:
        energy_sigma_array = extract_same_theta_different_energy(data_blocks, theta, 'sigma')
        if len(energy_sigma_array) > 0:
            print(f"  Theta = {theta}°: {len(energy_sigma_array)} 个能量点")
            # 显示前3个和后3个数据点
            for i in range(min(3, len(energy_sigma_array))):
                energy, value = energy_sigma_array[i]
                print(f"    Energy: {energy:6.2f}, Sigma: {value:8.4f}")
            if len(energy_sigma_array) > 6:
                print(f"    ...")
            for i in range(max(0, len(energy_sigma_array)-3), len(energy_sigma_array)):
                energy, value = energy_sigma_array[i]
                print(f"    Energy: {energy:6.2f}, Sigma: {value:8.4f}")

if __name__ == "__main__":
    main()