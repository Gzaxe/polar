import numpy as np
from read_fort16 import read_fort16, save_same_theta_different_energy

def main():
    print("读取fort.16文件...")
    data_blocks = read_fort16('fort.16')
    
    print(f"找到 {len(data_blocks)} 个数据块")
    
    # 示例：保存特定theta值的数据到txt文件
    print(f"\n=== 保存相同theta值下不同能量的数据到txt文件 ===")
    
    # 保存theta=90度的sigma数据
    theta_value = 90.0
    filename = f"theta_{theta_value}_sigma_data.txt"
    save_same_theta_different_energy(data_blocks, theta_value, filename, 'sigma')
    
    # 保存theta=45度的iT11数据
    theta_value = 45.0
    filename = f"theta_{theta_value}_iT11_data.txt"
    save_same_theta_different_energy(data_blocks, theta_value, filename, 'iT11')
    
    # 保存theta=0.01度的T20数据
    theta_value = 0.01
    filename = f"theta_{theta_value}_T20_data.txt"
    save_same_theta_different_energy(data_blocks, theta_value, filename, 'T20')
    
    # 保存多个theta值的数据
    print(f"\n=== 批量保存多个theta值的数据 ===")
    
    thetas_to_save = [0.01, 30.0, 45.0, 90.0, 135.0, 179.99]
    columns_to_save = ['sigma', 'iT11']
    
    for theta in thetas_to_save:
        for col in columns_to_save:
            filename = f"theta_{theta}_{col}_data.txt"
            save_same_theta_different_energy(data_blocks, theta, filename, col)
    
    print(f"\n所有数据文件已保存完成！")

if __name__ == "__main__":
    main()