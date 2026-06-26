# Fort.16 文件读取和数据提取工具

这个Python程序用于读取名为 `fort.16` 的文件，该文件包含二维数组数据，并能够提取特定横坐标（散射角θ）的数据。

## 功能特点

- 读取fort.16文件中的多维数据
- 解析包含不同能量值的多个数据块
- 提取特定θ值（散射角）对应的物理量数据
- 支持多种物理量的提取（sigma, iT11, T20, T21, T22, Kyy）
- 提供便捷的接口用于数据分析和可视化

## 文件格式

fort.16文件包含多个数据块，每个数据块对应一个能量值，格式如下：

```
#legend string   0 "Lab energy =    0.1000"
#  Theta       sigma       iT11        T20         T21         T22         Kyy for projectile
  0.1000E-01   1.000       0.000       0.000       0.000       0.000       0.000
  1.000        1.000       0.000       0.000       0.000       0.000       0.000
  ...
```

## 主要函数

### `read_fort16(filename='fort.16')`
读取fort.16文件并返回数据块列表，每个数据块包含：
- `energy`: 能量值
- `theta`: 散射角数组
- `sigma`: 截面数据
- `iT11`, `T20`, `T21`, `T22`, `Kyy`: 其他物理量

### `extract_specific_theta(data_blocks, theta_value, column='sigma')`
提取特定θ值对应的数据，返回(energy, value)对的列表

### `extract_same_theta_different_energy(data_blocks, theta_value, column='sigma')`
提取相同θ值下不同能量的二维数组

### `save_same_theta_different_energy(data_blocks, theta_value, filename, column='sigma')`
将提取的数据保存到文件

## 使用示例

```python
from read_fort16 import read_fort16, extract_specific_theta

# 读取文件
data_blocks = read_fort16('fort.16')

# 提取特定theta值的数据
sigma_data = extract_specific_theta(data_blocks, 90.0, 'sigma')  # 在90度提取sigma数据
iT11_data = extract_specific_theta(data_blocks, 45.0, 'iT11')   # 在45度提取iT11数据

# 打印结果
for energy, value in sigma_data:
    print(f"Energy: {energy}, Sigma: {value}")
```

## 程序文件

- `read_fort16.py`: 主要功能实现
- `simple_example.py`: 简单使用示例
- `example_usage.py`: 详细使用示例
- `advanced_example.py`: 高级功能示例
- `save_example.py`: 数据保存示例
- `save_single.py`: 单一数据保存示例

## 数据列说明

- `Theta`: 散射角（度）
- `sigma`: 微分截面（mb/sr）
- `iT11`: 第一阶不可约张量分量
- `T20`, `T21`, `T22`: 极化张量分量
- `Kyy`: 自旋关联参数

## 注意事项

- 程序会自动寻找最接近指定θ值的数据点
- 如果指定的θ值不存在精确匹配，将返回最接近的值
- 文件必须位于程序运行目录下，或提供完整路径
