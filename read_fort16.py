import numpy as np

def read_fort16(filename='fort.16'):
    """
    读取fort.16文件并解析为数据结构

    Args:
        filename: 文件名，默认为'fort.16'

    Returns:
        data_blocks: 包含所有数据块的列表，每个数据块是一个字典，包含energy和data
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    data_blocks = []
    current_block = None

    for line in lines:
        line = line.strip()

        # 检查是否是新的数据块开始（通过能量标签）
        if ('@legend string' in line or '#legend string' in line) and 'Lab energy =' in line:
            # 提取能量值
            try:
                # 查找 "Lab energy =" 后面的数值
                energy_start = line.find('Lab energy =')
                if energy_start != -1:
                    energy_part = line[energy_start + len('Lab energy ='):].strip()
                    # 提取数值部分（可能包含科学计数法如1.2345等）
                    import re
                    energy_match = re.search(r'([+-]?\d*\.?\d+([eE][+-]?\d+)?)', energy_part)
                    if energy_match:
                        energy = float(energy_match.group(1))
                    else:
                        continue  # 如果没找到能量值，跳过此行
                else:
                    continue
            except:
                continue  # 如果解析出错，跳过此行

            # 如果有上一个数据块，保存它
            if current_block is not None and len(current_block['theta']) > 0:
                data_blocks.append(current_block)

            # 开始新的数据块
            current_block = {
                'energy': energy,
                'theta': [],
                'sigma': [],
                'iT11': [],
                'T20': [],
                'T21': [],
                'T22': [],
                'Kyy': []
            }

        # 如果当前行包含数据列标题，则开始读取数据
        elif current_block is not None and line.startswith('#  Theta') and 'sigma' in line:
            continue  # 跳过标题行

        # 解析数据行
        elif current_block is not None and line and not line.startswith('#') and not line.startswith('@') and 'END' not in line.upper():
            # 使用更灵活的方式分割数据
            values = line.split()
            if len(values) >= 2:  # 至少有Theta和sigma
                try:
                    theta_val = float(values[0])
                    sigma_val = float(values[1])

                    # 添加基本值
                    current_block['theta'].append(theta_val)
                    current_block['sigma'].append(sigma_val)

                    # 根据实际列数添加其他值
                    if len(values) > 2:
                        current_block['iT11'].append(float(values[2]))
                    else:
                        current_block['iT11'].append(0.0)

                    if len(values) > 3:
                        current_block['T20'].append(float(values[3]))
                    else:
                        current_block['T20'].append(0.0)

                    if len(values) > 4:
                        current_block['T21'].append(float(values[4]))
                    else:
                        current_block['T21'].append(0.0)

                    if len(values) > 5:
                        current_block['T22'].append(float(values[5]))
                    else:
                        current_block['T22'].append(0.0)

                    if len(values) > 6:
                        current_block['Kyy'].append(float(values[6]))
                    else:
                        current_block['Kyy'].append(0.0)
                except ValueError:
                    # 如果转换失败，跳过这一行
                    continue  # 改为continue而不是pass，确保不会添加不完整数据

    # 添加最后一个数据块
    if current_block is not None and len(current_block['theta']) > 0:
        data_blocks.append(current_block)

    return data_blocks

def extract_specific_theta(data_blocks, theta_value, column='sigma'):
    """
    从数据块中提取特定theta值对应的数据
    
    Args:
        data_blocks: 由read_fort16返回的数据块列表
        theta_value: 要提取的theta值
        column: 要提取的列名 ('theta', 'sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy')
        
    Returns:
        extracted_data: 包含(energy, value)对的列表
    """
    extracted_data = []
    
    for block in data_blocks:
        if column in block:
            # 寻找最接近theta_value的值
            theta_array = np.array(block['theta'])
            idx = (np.abs(theta_array - theta_value)).argmin()
            
            if idx < len(block[column]):
                energy = block['energy']
                value = block[column][idx]
                extracted_data.append((energy, value))
    
    return extracted_data

def create_energy_theta_function(data_blocks, column='sigma'):
    """
    将数据转换为能量-角度函数
    
    Args:
        data_blocks: 由read_fort16返回的数据块列表
        column: 要提取的列名 ('sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy')
        
    Returns:
        energy_theta_matrix: 二维numpy数组，行表示能量，列表示theta
        energies: 能量值列表
        thetas: theta值列表（来自第一个数据块）
    """
    if not data_blocks:
        return np.array([]), [], []
    
    # 获取所有唯一能量值
    energies = sorted(list(set(block['energy'] for block in data_blocks)))
    
    # 获取theta值（假设所有数据块都有相同的theta网格）
    thetas = data_blocks[0]['theta']
    
    # 创建二维矩阵
    energy_theta_matrix = np.zeros((len(energies), len(thetas)))
    
    # 填充矩阵
    for i, energy in enumerate(energies):
        # 找到对应能量的数据块
        block = next((b for b in data_blocks if abs(b['energy'] - energy) < 1e-6), None)
        if block and column in block:
            energy_theta_matrix[i, :] = np.array(block[column])
    
    return energy_theta_matrix, energies, thetas

def extract_same_theta_different_energy(data_blocks, theta_value, column='sigma'):
    """
    提取相同theta值下不同能量的二维数组
    
    Args:
        data_blocks: 由read_fort16返回的数据块列表
        theta_value: 要提取的theta值
        column: 要提取的列名 ('sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy')
        
    Returns:
        energy_value_array: 二维numpy数组，包含(energy, value)对
    """
    extracted_data = extract_specific_theta(data_blocks, theta_value, column)
    
    if not extracted_data:
        return np.array([])
    
    # 转换为numpy数组
    energy_value_array = np.array(extracted_data)
    
    return energy_value_array

def save_same_theta_different_energy(data_blocks, theta_value, filename, column='sigma'):
    """
    将相同theta值下不同能量的数据保存为txt文件
    
    Args:
        data_blocks: 由read_fort16返回的数据块列表
        theta_value: 要提取的theta值
        filename: 输出文件名
        column: 要提取的列名 ('sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy')
    """
    energy_value_array = extract_same_theta_different_energy(data_blocks, theta_value, column)
    
    if energy_value_array.size == 0:
        print(f"警告: 没有找到theta={theta_value}的数据")
        return
    
    # 写入文件，使用默认编码
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write(f"# 相同theta值({theta_value}度)下不同能量的{column}数据\n")
        f.write("# 列1: 能量 (Energy)\n")
        f.write(f"# 列2: {column}值\n")
        f.write("# Energy\t" + column + "\n")
        for energy, value in energy_value_array:
            f.write(f"{energy}\t{value}\n")
    
    print(f"数据已保存到 {filename}，共 {len(energy_value_array)} 行数据")

def print_available_energies(data_blocks):
    """打印所有可用的能量值"""
    energies = [block['energy'] for block in data_blocks]
    print("Available energies:")
    for i, energy in enumerate(energies):
        print(f"{i+1:2d}. {energy:.4f}")

def print_theta_range(data_blocks):
    """打印theta值的范围"""
    if data_blocks:
        thetas = data_blocks[0]['theta']
        if thetas:  # 检查thetas列表是否为空
            print(f"Theta range: {min(thetas):.3f} to {max(thetas):.3f}")
            print(f"Number of theta points: {len(thetas)}")
        else:
            print("No theta data available")

if __name__ == "__main__":
    # 读取fort.16文件
    print("Reading fort.16 file...")
    data_blocks = read_fort16('fort.16')
    
    print(f"Found {len(data_blocks)} data blocks")
    
    # 显示可用能量
    print_available_energies(data_blocks)
    
    # 显示theta范围
    print_theta_range(data_blocks)
    
    # 示例：提取特定theta值的数据
    target_theta = 90.0  # 可以修改为目标theta值
    print(f"\nExtracting data for theta = {target_theta} degrees")
    
    # 提取sigma列的数据
    sigma_data = extract_specific_theta(data_blocks, target_theta, 'sigma')
    print(f"Sigma values for theta={target_theta}:")
    for energy, value in sigma_data[:10]:  # 只显示前10个
        print(f"  Energy: {energy:6.2f}, Sigma: {value:8.4f}")
    
    if len(sigma_data) > 10:
        print(f"  ... and {len(sigma_data)-10} more")
    
    # 提取其他列的数据
    iT11_data = extract_specific_theta(data_blocks, target_theta, 'iT11')
    print(f"\niT11 values for theta={target_theta}:")
    for energy, value in iT11_data[:10]:  # 只显示前10个
        print(f"  Energy: {energy:6.2f}, iT11: {value:8.4f}")
    
    # 允许用户输入特定的theta值
    print("\n" + "="*50)
    print("You can extract data for any theta value.")
    try:
        user_theta = float(input("Enter theta value to extract (or press Enter to skip): ") or target_theta)
        column_choice = input("Enter column to extract (sigma/iT11/T20/T21/T22/Kyy) [default: sigma]: ").strip()
        if not column_choice:
            column_choice = 'sigma'
        
        if column_choice in ['sigma', 'iT11', 'T20', 'T21', 'T22', 'Kyy']:
            extracted = extract_specific_theta(data_blocks, user_theta, column_choice)
            print(f"\n{column_choice.capitalize()} values for theta={user_theta}:")
            for energy, value in extracted:
                print(f"  Energy: {energy:6.2f}, {column_choice.capitalize()}: {value:8.4f}")
        else:
            print("Invalid column name. Using 'sigma'.")
            extracted = extract_specific_theta(data_blocks, user_theta, 'sigma')
            print(f"\nSigma values for theta={user_theta}:")
            for energy, value in extracted:
                print(f"  Energy: {energy:6.2f}, Sigma: {value:8.4f}")
                
    except ValueError:
        print("Invalid input. Using default values.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

