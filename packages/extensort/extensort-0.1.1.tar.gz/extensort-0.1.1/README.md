# Extensort

Extensort is a Python module that simplifies the process of organizing files by sorting them into folders based on their extensions. It provides an efficient way to clean up cluttered directories and maintain a well-organized file system.

## Features

- Automatically sort files into folders based on their extensions
- Customizable mapping of file extensions to folder names
- Find all unique file extensions in a directory
- Detailed sorting summary including moved, skipped, and error counts
- Color-coded console output for better visibility of the sorting process

## Installation

You can install Extensort using pip:

```bash
pip install extensort
```

## Usage

Here's a quick example of how to use Extensort:

```python
from extensort import sort_files, find_extensions

# Define the directory to sort
directory_to_sort = "/path/to/your/directory"

# Find all extensions in the directory
all_extensions = find_extensions(directory_to_sort)
print(f"Found extensions: {all_extensions}")

# Define how you want to sort the files
extension_mapping = {
    ".txt": "Text Files",
    ".pdf": "Documents",
    ".jpg": "Images",
    ".png": "Images",
    ".py": "Python Scripts"
}

# Sort the files
summary = sort_files(directory_to_sort, extension_mapping)

print("Sorting complete!")
print(f"Moved: {summary['moved']}")
print(f"Skipped: {summary['skipped']}")
print(f"Errors: {summary['errors']}")
```

## Detailed Usage

### Finding Extensions

The `find_extensions` function scans a directory and returns a set of all unique file extensions:

```python
extensions = find_extensions("/path/to/directory")
```

### Sorting Files

The `sort_files` function organizes files into folders based on their extensions:

```python
extension_mapping = {
    ".txt": "Text",
    ".jpg": "Images",
    ".png": "Images",
    ".docx": "Documents",
    ".pdf": "Documents",
    ".py": "Code",
    ".js": "Code"
}

summary = sort_files("/path/to/sort", extension_mapping)
```

The function returns a summary dictionary with the following keys:
- `moved`: Number of files successfully moved
- `skipped`: Number of files skipped (no matching extension in the mapping)
- `errors`: Number of errors encountered during the sorting process

## Contributing

Contributions to Extensort are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
