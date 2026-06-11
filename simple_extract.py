#!/usr/bin/env python3
"""
简单示例：从fort.16文件中提取特定theta值的数据
"""

from read_fort16 import read_fort16, extract_specific_theta

def main():
    # 读取fort.16文件
    print("正在读取fort.16文件...")
    data_blocks = read_fort16('fort.16')
    
    print(f"找到 {len(data_blocks)} 个数据块")
    
    if not data_blocks:
        print("未找到任何数据块，请检查fort.16文件格式")
        return
    
    # 显示第一个数据块的信息
    first_block = data_blocks[0]
    print(f"第一个数据块能量: {first_block['energy']}")
    print(f"Theta范围: {min(first_block['theta']):.2f} 到 {max(first_block['theta']):.2f}")
    print(f"Theta点数: {len(first_block['theta'])}")
    
    # 用户输入要提取的theta值
    try:
        theta_input = input("\n请输入要提取的theta值 (默认为90.0): ")
        if theta_input.strip():
            target_theta = float(theta_input)
        else:
            target_theta = 90.0
        
        # 选择要提取的列
        print("\n可选的数据列:")
        print("1. sigma")
        print("2. iT11") 
        print("3. T20")
        print("4. T21")
        print("5. T22")
        print("6. Kyy")
        
        col_choice = input("请选择要提取的列 (1-6, 默认为sigma): ")
        column_map = {'1': 'sigma', '2': 'iT11', '3': 'T20', '4': 'T21', '5': 'T22', '6': 'Kyy'}
        column_choice = column_map.get(col_choice, 'sigma')
        
        # 提取数据
        extracted_data = extract_specific_theta(data_blocks, target_theta, column_choice)
        
        print(f"\n提取到 {len(extracted_data)} 个数据点:")
        print(f"Theta = {target_theta}, Column = {column_choice}")
        print("Energy\t\tValue")
        print("-" * 25)
        for energy, value in extracted_data:
            print(f"{energy:8.2f}\t{value:10.4f}")
            
        # 询问是否保存到文件
        save_choice = input(f"\n是否将结果保存到文件? (y/n, 默认为n): ")
        if save_choice.lower().startswith('y'):
            filename = f"theta_{target_theta}_{column_choice}_data.txt"
            with open(filename, 'w') as f:
                f.write(f"# 特定theta值({target_theta})下的{column_choice}数据\n")
                f.write("# Energy\tValue\n")
                for energy, value in extracted_data:
                    f.write(f"{energy}\t{value}\n")
            print(f"数据已保存到 {filename}")
    
    except ValueError:
        print("输入无效，请输入一个数字")
    except KeyboardInterrupt:
        print("\n程序被用户中断")

if __name__ == "__main__":
    main()