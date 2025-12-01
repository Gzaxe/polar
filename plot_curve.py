import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_multiple_curves(data_sets, title="Multiple Curves Plot", xlabel="X-axis", ylabel="Y-axis", grid=True):
    """
    Plot multiple curves on the same graph
    
    Parameters:
    data_sets: list of tuples [(x_values, y_values, label), ...]
    title: plot title
    xlabel: x-axis label
    ylabel: y-axis label
    grid: whether to show grid
    """
    
    # Define colors and markers for different datasets
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot each dataset
    for i, (x_values, y_values, label) in enumerate(data_sets):
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        
        # Convert to numpy arrays for easier handling
        x_values = np.array(x_values)
        y_values = np.array(y_values)
        
        plt.plot(x_values, y_values, color=color, marker=marker, label=label, linewidth=2, markersize=6)
    
    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    # Add legend
    plt.legend()
    
    # Add grid if requested
    if grid:
        plt.grid(True, alpha=0.3)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def read_2d_data_from_file(filename):
    """
    Read 2D array data (x,y pairs) from a text file
    
    Parameters:
    filename: path to the text file containing 2D array data
    
    Returns:
    Tuple of (x_values, y_values) lists, or (None, None) if error
    """
    try:
        x_values = []
        y_values = []
        
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Skip empty lines and comment lines
                if not line.strip() or line.strip().startswith('#') or line.strip().startswith('@'):
                    continue
                
                # Check for END marker (for files like fort.16)
                if line.strip().upper() == 'END':
                    break
                    
                # Split line by whitespace and convert to float
                values = [float(x) for x in line.split()]
                
                # Check if we have pairs of values
                if len(values) >= 2:
                    x_values.append(values[0])  # First column as x
                    y_values.append(values[1])  # Second column as y
                elif len(values) == 1:
                    # If only one value, use line number as x
                    x_values.append(line_num)
                    y_values.append(values[0])
                # Skip lines with no values or invalid format
                    
        return x_values, y_values
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except ValueError as e:
        print(f"Error: Invalid data in file at line {line_num}. {e}")
        return None, None

def read_multiple_datasets_from_file(filename):
    """
    Read multiple datasets from a file (like fort.16 with END markers)
    
    Parameters:
    filename: path to the text file containing multiple datasets
    
    Returns:
    List of tuples [(x_values, y_values), ...], or empty list if error
    """
    try:
        datasets = []
        current_x = []
        current_y = []
        
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Skip empty lines and comment lines
                if not line.strip() or line.strip().startswith('#') or line.strip().startswith('@'):
                    continue
                
                # Check for END marker
                if line.strip().upper() == 'END':
                    # Save current dataset if it has data
                    if current_x and current_y:
                        datasets.append((current_x.copy(), current_y.copy()))
                    # Reset for next dataset
                    current_x = []
                    current_y = []
                    continue
                    
                # Split line by whitespace and convert to float
                try:
                    values = [float(x) for x in line.split()]
                    if len(values) >= 2:
                        current_x.append(values[0])  # First column as x
                        current_y.append(values[1])  # Second column as y
                except ValueError:
                    # Skip lines that can't be converted to float
                    continue
        
        # Add the last dataset if it wasn't followed by END
        if current_x and current_y:
            datasets.append((current_x, current_y))
            
        return datasets
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return []

def read_1d_data_from_file(filename):
    """
    Read 1D array data from a text file
    
    Parameters:
    filename: path to the text file containing array data
    
    Returns:
    List of floats from the file
    """
    try:
        with open(filename, 'r') as file:
            # Read all lines and flatten them
            data = []
            for line in file:
                # Skip empty lines and comment lines
                if not line.strip() or line.strip().startswith('#') or line.strip().startswith('@'):
                    continue
                # Split line by whitespace and convert to float
                values = [float(x) for x in line.split()]
                data.extend(values)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except ValueError as e:
        print(f"Error: Invalid data in file. {e}")
        return None

# Main usage
if __name__ == "__main__":
    # Check if filenames are provided as command line arguments
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        filenames_input = input("Enter the paths to the text files containing array data (separated by spaces): ")
        filenames = filenames_input.split()
    
    if not filenames:
        print("No files specified. Exiting.")
        sys.exit(1)
    
    # Collect all datasets
    all_datasets = []
    
    # Process each file
    for filename in filenames:
        # Try to detect data format
        data_format = "auto"
        try:
            with open(filename, 'r') as file:
                lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('#') and not line.startswith('@')][:5]
            
            # Count END markers to detect multiple datasets
            with open(filename, 'r') as file:
                content = file.read()
                end_count = content.upper().count('END')
            
            # Count values in each line
            value_counts = []
            for line in lines:
                if line.upper() != 'END':
                    values = line.split()
                    value_counts.append(len(values))
            
            # If we have multiple END markers, treat as multiple datasets
            if end_count > 1:
                data_format = "multiple"
            # If most lines have 2 or more values, treat as 2D data
            elif len(value_counts) > 0 and sum(1 for count in value_counts if count >= 2) > len(value_counts) // 2:
                data_format = "2d"
            else:
                data_format = "1d"
        except:
            data_format = "1d"  # Default to 1D if detection fails
        
        if data_format == "multiple":
            # Read multiple datasets from file
            datasets = read_multiple_datasets_from_file(filename)
            if datasets:
                for i, (x_data, y_data) in enumerate(datasets):
                    all_datasets.append((x_data, y_data, f"{filename} (Dataset {i+1})"))
                print(f"Successfully read {len(datasets)} datasets from {filename}")
            else:
                print(f"Failed to read datasets from {filename}")
        elif data_format == "2d":
            # Read 2D data (x,y pairs)
            x_data, y_data = read_2d_data_from_file(filename)
            
            if x_data is not None and y_data is not None:
                all_datasets.append((x_data, y_data, filename))
                print(f"Successfully read 2D data from {filename}")
            else:
                print(f"Failed to read 2D data from {filename}")
        else:
            # Read 1D data
            y_data = read_1d_data_from_file(filename)
            
            if y_data is not None:
                x_data = list(range(len(y_data)))  # Use indices as x-values
                all_datasets.append((x_data, y_data, filename))
                print(f"Successfully read 1D data from {filename}")
            else:
                print(f"Failed to read data from {filename}")
    
    # Plot all datasets
    if all_datasets:
        plot_multiple_curves(all_datasets, 
                           title="Multiple Datasets Comparison", 
                           xlabel="X Values", 
                           ylabel="Y Values")
        print(f"Successfully plotted {len(all_datasets)} datasets")
    else:
        print("No valid data to plot.")
