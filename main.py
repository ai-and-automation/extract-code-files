import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Run code on 31-Oct-2024 -> works! needs some tweaks

# Load environment variables from .env file
load_dotenv()

# === Main folder path from .env ===
BASE_PATH = os.getenv('BASE_PATH')

# === Configuration Section ===
OUTPUT_FILE = 'combined_code_output.txt'
STRUCTURE_FILE = 'folder_structure_tree.txt'
FILE_EXTENSIONS = {'.py', '.js', '.html', '.css', '.jsx'}

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

# === Function to build the folder structure as a tree ===
def build_folder_tree(start_path):
    logging.info("Starting to build folder structure.")
    structure = ""
    try:
        for root, dirs, files in os.walk(start_path):
            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * 4 * level
            structure += f"{indent}{os.path.basename(root)}/\n"
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                structure += f"{subindent}{f}\n"
            logging.debug(f"Processed directory: {os.path.basename(root)} with {len(files)} files.")
    except Exception as e:
        logging.error(f"Error building folder tree: {e}")
    return structure

# === Function to gather and combine code from specified files ===
def combine_code_files(start_path):
    logging.info("Starting to combine code files.")
    combined_code = ""
    try:
        for root, _, files in os.walk(start_path):
            for file in files:
                if os.path.splitext(file)[1] in FILE_EXTENSIONS:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        relative_path = os.path.relpath(file_path, start_path)
                        combined_code += f"--- {relative_path} ---\n{code}\n\n"
                        logging.debug(f"Added code from file: {relative_path}")
                    except Exception as e:
                        logging.error(f"Failed to read file '{file_path}': {e}")
    except Exception as e:
        logging.error(f"Error during code combination: {e}")
    return combined_code

# === Main Script Execution ===
if __name__ == "__main__":
    try:
        # Write folder structure to structure file
        logging.info("Writing folder structure to file.")
        structure = build_folder_tree(BASE_PATH)
        with open(STRUCTURE_FILE, 'w', encoding='utf-8') as f:
            f.write(structure)
        logging.info(f"Folder structure saved to '{STRUCTURE_FILE}'.")

        # Write combined code to output file
        logging.info("Writing combined code to file.")
        combined_code = combine_code_files(BASE_PATH)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(combined_code)
        logging.info(f"Combined code saved to '{OUTPUT_FILE}'.")

        logging.info("Process completed successfully.")

    except Exception as e:
        logging.critical(f"Unexpected error in main execution: {e}")