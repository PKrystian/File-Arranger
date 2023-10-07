# File Arranger

## Table of Contents
- [File Arranger](#file-arranger)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)

## About
File Arranger is an organization tool designed to simplify your digital life by categorizing and tidying up files in a specified directory based on their file extensions. It provides an automated way to move files into designated folders, helping you maintain a clean and organized file system.

The tool is written in Python and uses a configuration file to map file extensions to their corresponding categories. It supports both real file organization and dry-run mode to simulate the organization process without actually moving files.

## Getting Started
Follow these instructions to get File Arranger up and running on your local machine.

### Prerequisites
Before you start, make sure you have the following prerequisites installed:
- Python 3.x
- pip (Python package manager)

### Installation
1. Clone the File Arranger repository to your local machine:
   ```shell
   git clone https://github.com/PKrystian/File-Arranger.git
   ```

2. Change to the project directory:
   ```shell
   cd File-Arranger
   ```

3. Install the required Python dependencies using pip:
   ```shell
   pip install -r requirements.txt
   ```

## Usage
File Arranger is designed to be used via the command line. To organize files in a directory, run the `main.py` script with the source directory as an argument. Optionally, you can use the `--dry-run` flag to perform a dry run without actually moving any files. I recommend running it  before, to see if there are no problems. The output will be saved in log file.

Example usage:
```shell
python main.py /path/to/source/directory
```
Example usage (Windows):
```shell
python main.py '?:\path\to\source\directory' --dry-run
```

**Note:** Ensure that you have created a configuration file named `config.py` in the project directory. You can use the provided `config.py` file as a template and customize it according to your needs.

## Configuration
File Arranger uses a configuration file (`config.py`) to map file extensions to categories. You can customize this file to define your own categories and file extensions. Here's an example of the configuration:

```python
LOG_FILE_INFO = 'info.log'
LOG_FILE_ERROR = 'error.log'
OTHERS_CATEGORY = 'Others'
DIRECTORY_MAPPING = {
    'Documents': ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.ppt', '.pptx', '.odt', '.ods', '.rtf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    # Add more categories and file extensions here
}
```

You can add, remove, or modify categories and their associated file extensions to suit your organizational needs.

## Contributing
Contributions to File Arranger are welcome! If you find issues or have ideas for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/PKrystian/File-Arranger).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
