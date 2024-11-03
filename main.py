import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Run code on 02-Nov-2024 -> works!

# Load environment variables from .env file
load_dotenv()

# === Main folder path from .env ===
BASE_PATH = os.getenv('BASE_PATH')

# === Configuration Section ===
OUTPUT_FILE = 'combined_code_output.txt'  # File for combined code from extracted files
STRUCTURE_FILE = 'folder_structure_tree.txt'  # File showing full directory structure with extracted file indicators
EXTRACTED_STRUCTURE_FILE = 'extracted_files_structure.txt'  # File showing only extracted files structure
EXCLUSIONS_FILE = 'exclusions.txt'  # File with names of files and folders to exclude
FILE_EXTENSIONS = {'.py', '.js', '.html', '.css', '.jsx'}  # Target file extensions for extraction

# === Logging Setup ===
log_filename = f"script_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,  # Set to INFO or WARNING to reduce verbosity
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(log_filename)  # Log to file
    ]
)

# === Read Exclusions from exclusions.txt ===
def load_exclusions(file_path):
    """Load exclusions from a specified text file."""
    exclusions = set()
    try:
        with open(file_path, 'r') as f:
            exclusions = {line.strip() for line in f if line.strip()}  # Read each line, strip whitespace
        logging.info(f"Loaded exclusions from '{file_path}'.")
    except FileNotFoundError:
        logging.warning(f"No exclusions file found at '{file_path}'. Proceeding without exclusions.")
    return exclusions

# === Function to build the folder structure as a tree ===
def build_folder_tree(start_path, extracted_files):
    """Build the full folder structure, marking extracted files."""
    structure = ""
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure += f"{indent}{os.path.basename(root)}/\n"  # Add folder name to structure
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_path = os.path.join(root, f)
            # Mark files that were extracted with '*'
            marker = '*' if file_path in extracted_files else ''
            structure += f"{subindent}{f}{marker}\n"
    return structure

# === Function to build extracted files structure tree ===
def build_extracted_files_tree(extracted_files):
    """Build structure tree for extracted files only."""
    structure = ""
    for file_path in sorted(extracted_files):
        dirs = file_path.split(os.sep)
        for level, folder in enumerate(dirs[:-1]):
            indent = ' ' * 4 * level
            if folder:  # Only add if it's a real folder
                structure += f"{indent}{folder}/\n"
        # Add the filename at the final level
        structure += ' ' * 4 * (len(dirs) - 1) + os.path.basename(file_path) + '\n'
    return structure

# === Function to check if file/folder should be excluded ===
def is_excluded(path, exclusions):
    """Check if a file or folder is in the exclusion list."""
    return any(exclusion in path for exclusion in exclusions)

# === Function to gather and combine code from specified files ===
def combine_code_files(start_path, exclusions):
    """Combine code from files with specific extensions, respecting exclusions."""
    combined_code = ""
    extracted_files = set()
    for root, dirs, files in os.walk(start_path):
        # Exclude directories
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclusions)]
        for file in files:
            file_path = os.path.join(root, file)
            # Check exclusions and file extension
            if file not in exclusions and os.path.splitext(file)[1] in FILE_EXTENSIONS:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    relative_path = os.path.relpath(file_path, start_path)
                    combined_code += f"--- {relative_path} ---\n{code}\n\n"
                    extracted_files.add(file_path)  # Track extracted file path
                    logging.debug(f"Extracted code from file: {relative_path}")
                except Exception as e:
                    logging.error(f"Failed to read file '{file_path}': {e}")
    return combined_code, extracted_files

# === Main Script Execution ===
if __name__ == "__main__":
    try:
        # Load exclusions list
        exclusions = load_exclusions(EXCLUSIONS_FILE)

        # Write combined code and capture extracted files
        logging.info("Combining code from files...")
        combined_code, extracted_files = combine_code_files(BASE_PATH, exclusions)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(combined_code)
        logging.info(f"Combined code saved to '{OUTPUT_FILE}'.")

        # Write folder structure including extraction indicators
        logging.info("Writing folder structure with extraction indicators.")
        structure = build_folder_tree(BASE_PATH, extracted_files)
        with open(STRUCTURE_FILE, 'w', encoding='utf-8') as f:
            f.write(structure)
        logging.info(f"Folder structure saved to '{STRUCTURE_FILE}'.")

        # Write extracted files structure
        logging.info("Writing extracted files structure.")
        extracted_structure = build_extracted_files_tree(extracted_files)
        with open(EXTRACTED_STRUCTURE_FILE, 'w', encoding='utf-8') as f:
            f.write(extracted_structure)
        logging.info(f"Extracted files structure saved to '{EXTRACTED_STRUCTURE_FILE}'.")

        logging.info("Process completed successfully.")

    except Exception as e:
        logging.critical(f"Unexpected error in main execution: {e}")