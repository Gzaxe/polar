import numpy as np
from read_fort16 import read_fort16, extract_specific_theta

def main():
    print("读取fort.16文件...")
    data_blocks = read_fort16('fort.16')
    
    print(f"找到 {len(data_blocks)} 个数据块")
    print(f"Theta范围: {data_blocks[0]['theta'][0]:.3f} 到 {data_blocks[0]['theta'][-1]:.3f}")
    print(f"Theta点数量: {len(data_blocks[0]['theta'])}")
    
    # 示例：提取特定theta值的数据
    target_theta = 90.0
    print(f"\n提取theta = {target_theta}度的数据:")
    
    # 提取sigma列的数据
    sigma_data = extract_specific_theta(data_blocks, target_theta, 'sigma')
    print(f"前10个Sigma值 (theta={target_theta}):")
    for i, (energy, value) in enumerate(sigma_data[:10]):
        print(f"  {i+1:2d}. Energy: {energy:6.2f}, Sigma: {value:8.4f}")
    
    if len(sigma_data) > 10:
        print(f"  ... 还有 {len(sigma_data)-10} 个数据点")
    
    # 提取iT11列的数据
    iT11_data = extract_specific_theta(data_blocks, target_theta, 'iT11')
    print(f"\n前10个iT11值 (theta={target_theta}):")
    for i, (energy, value) in enumerate(iT11_data[:10]):
        print(f"  {i+1:2d}. Energy: {energy:6.2f}, iT11: {value:8.4f}")
    
    # 提取多个不同的theta值
    print(f"\n提取多个theta值在第一个能量块的数据:")
    thetas_to_extract = [0.01, 30.0, 45.0, 90.0, 135.0, 179.9]
    for theta in thetas_to_extract:
        if 0 <= theta <= 180:  # 确保theta在有效范围内
            # 在第一个能量块中查找最接近的theta值
            theta_array = np.array(data_blocks[0]['theta'])
            idx = (np.abs(theta_array - theta)).argmin()
            closest_theta = theta_array[idx]
            
            sigma_val = data_blocks[0]['sigma'][idx]
            iT11_val = data_blocks[0]['iT11'][idx] if idx < len(data_blocks[0]['iT11']) else 0.0
            
            print(f"  Theta ≈ {closest_theta:.2f}°: Sigma = {sigma_val:8.4f}, iT11 = {iT11_val:8.4f}")

if __name__ == "__main__":
    main()