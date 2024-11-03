# Code Extraction and Directory Structure Automation Script

This Python script automates the process of extracting specific file types from nested directories, logs the process, and generates directory structure summaries. It is ideal for organizing and documenting project files within multiple GitHub organizations.

## Features
- **File Extraction**: Extracts `.py`, `.js`, `.html`, `.css`, and `.jsx` files from all subdirectories, combining them into a single file with path annotations.
- **Directory Structure Generation**: Generates two tree-like structure files, one with all folders and files (indicating extracted files) and one with extracted files only.
- **Exclusion Management**: Reads an `exclusions.txt` file to ignore specified files and folders.
- **Logging**: Logs all operations for transparency, including exclusions and extraction processes.

## Prerequisites
Before running the script, ensure you have the following:
- Python 3.x installed.
- A `.env` file in the root of your project to store environment variables (see below for structure).

## Environment Variables
Create a `.env` file in the root directory of your script with the following variable:

```plaintext
BASE_PATH=path/to/your/base/folder
```

### Explanation:
- **`BASE_PATH`**: Path to the main folder containing all subdirectories from which files are to be extracted.

## How to Run the Script
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/ai-and-automation/extract-code-files
   cd repository
   ```
2. Set up a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create and populate your `.env` file (as mentioned above).
5. Place the `exclusions.txt` file in the root directory, listing any folders or files to exclude from extraction.
6. Run the script:
   ```bash
   python script.py
   ```
   The script will traverse directories, extract specified files, and generate the output files.

## Output Files
- **combined_code.txt**: Contains all extracted files, annotated with their directory paths.
- **folder_structure_tree.txt**: Lists all directories and files, marking extracted files with a `*`.
- **extracted_files_structure.txt**: Contains only the extracted files in a tree-like structure.

## Example Output

### `folder_structure_tree.txt` Example:
```plaintext
GitHub Repositories Test/
    web-dev-course-group/
        7-tetris/
            README.md
            index.html*
            .gitignore
            css/
                style.css*
            js/
                app.js*
            images/
                Tetris Game.gif
                purple_block.png
                pink_block.png
                yellow_block.png
```

### `extracted_files_structure.txt` Example:
```plaintext
base_directory/
    organization1/
        project1/
            script1.py
    base_directory/
        organization2/
            project2/
                style.css
    base_directory/
        organization3/
            project3/
                main.js
                index.html
```

## Troubleshooting
- **Excluded File Inclusion**: Ensure `exclusions.txt` is correctly formatted.
- **Log Review**: Check `extraction_log.log` for detailed operation logs and potential errors.

## Acknowledgements
This project was developed with the assistance of [ChatGPT](https://chatgpt.com/).

## License
This project is licensed under the MIT License.
