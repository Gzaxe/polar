import numpy as np
from read_fort16 import read_fort16, save_same_theta_different_energy

def main():
    print("读取fort.16文件...")
    data_blocks = read_fort16('fort.16')
    
    print(f"找到 {len(data_blocks)} 个数据块")
    
    # 示例：保存特定theta值的数据到txt文件
    print(f"\n=== 保存相同theta值下不同能量的数据到txt文件 ===")
    
    # 保存theta=100度的sigma数据
    theta_value = 100.0
    filename = f"theta_{theta_value}_sigma_data.txt"
    save_same_theta_different_energy(data_blocks, theta_value, filename, 'sigma')
    


if __name__ == "__main__":
    main()