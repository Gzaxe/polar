# Python Curve Plotting Script

This repository contains Python scripts for plotting curves from array data stored in text files.

## Files

1. `plot_curve.py` - Main script to plot curves from text file data
2. `sample_data.txt` - Sample 1D data file for testing
3. `sample_2d_data.txt` - Sample 2D data file (x,y pairs) for testing
4. `advanced_plot_example.py` - Advanced examples with customization options

## Requirements

- Python 3.x
- matplotlib
- numpy

Install required packages:
```bash
pip install matplotlib numpy
```

## Usage

### Basic Usage

```bash
python plot_curve.py data.txt
```

Or run without arguments and enter the file path when prompted:
```bash
python plot_curve.py
```

### Data File Formats

The script automatically detects the data format:

#### 1D Data Format
Single column or multiple values per line treated as a single series:
```
1.0 2.5 3.0 4.2 5.1
6.3 7.0 8.5 9.2 10.0
```

#### 2D Data Format (x,y pairs)
Two columns representing x,y coordinates:
```
0.0 1.0
1.0 2.5
2.0 3.0
3.0 4.2
4.0 5.1
```

### Advanced Usage

The `advanced_plot_example.py` script shows how to customize plots with different colors, markers, and styles.

```bash
python advanced_plot_example.py data.txt
```

## Function Parameters

The `plot_curve` function accepts the following parameters:

- `y_values`: Array of y-values to plot
- `x_values`: Optional array of x-values (defaults to indices for 1D data or uses first column for 2D data)
- `title`: Plot title
- `xlabel`: X-axis label
- `ylabel`: Y-axis label
- `line_color`: Line color (e.g., 'red', 'blue', '#FF5733')
- `line_style`: Line style ('-', '--', '-.', ':')
- `marker`: Marker style (None, 'o', 's', '^', etc.)
- `grid`: Boolean to show/hide grid

## Examples

See `advanced_plot_example.py` for examples of different plotting styles and customizations.
