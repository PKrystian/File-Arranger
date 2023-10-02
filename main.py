import os
import shutil
import logging
import argparse
from config import *
from tqdm import tqdm
from pathlib import Path

def configure_logging() -> logging.Logger:
    """

    Configure logging settings for the script
    Returns:
        logging.Logger: The configured logger instance

    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler_info = logging.FileHandler(LOG_FILE_INFO)
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(formatter)
    file_handler_error = logging.FileHandler(LOG_FILE_ERROR)
    file_handler_error.setLevel(logging.ERROR)
    file_handler_error.setFormatter(formatter)
    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_error)
    return logger

def move_file(file_path: str, destination_path: str, dry_run: bool | None = False) -> None:
    """

    Move a file from the source path to the destination path
    Parameters:
        file_path (str): The path to the file to be moved
        destination_path (str): The destination path to move the file to
        dry_run (bool, optional): Whether to run in dry run mode. Defaults to False
    Returns:
        None

    """
    try:
        if Path(file_path) == Path(destination_path):
            logger.info(f"{'DRY RUN: ' if dry_run else ''}No file movement required for {file_path}")
            return
        if not dry_run:
            shutil.move(file_path, destination_path)
        logger.info(f"{'DRY RUN: ' if dry_run else ''}Moving {file_path} to {destination_path}")
    except FileExistsError:
        backup_path = Path(destination_path, f"{Path(file_path).stem}_backup{Path(file_path).suffix}")
        shutil.move(file_path, backup_path)
        logger.error(f"File {file_path} already exists in {destination_path}. Moved to {backup_path}")
    except Exception as e:
        logger.error(f"Failed to move {file_path} to {destination_path}: {e}")

def get_directory_by_extension(extension: str) -> str:
    """

    Get the directory name based on the file extension
    Parameters:
        extension (str): The file extension
    Returns:
        str: The directory name

    """
    for category, extensions in DIRECTORY_MAPPING.items():
        if extension in extensions:
            return category
    return OTHERS_CATEGORY

def scan_directory(base_directory: str) -> str:
    """

    Recursively scan a directory for files and subdirectories
    Parameters:
        base_directory (str): The base directory to start scanning from
    Yields: 
        os.DirEntry: An iterator yielding DirEntry objects representing files and directories

    """
    for entry in os.scandir(base_directory):
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from scan_directory(entry.path)

def organize_files(source_directory: str, dry_run: bool | None = False) -> None:
    """

    Organize files in a source directory based on their file extensions
    Parameters:
        source_directory (str): The source directory containing files to be organized
        dry_run (bool, optional): Whether to run in dry run mode. Defaults to False
    Returns: 
        None

    """
    progress_bar = tqdm(total=len(list(scan_directory(source_directory))), desc=f"Organizing Files", dynamic_ncols=True, ascii=True, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    for item in scan_directory(source_directory):
        file_path = Path(item)
        file_extension = os.path.splitext(file_path)[1].lower()
        directory_name = get_directory_by_extension(file_extension)
        destination_path = Path(source_directory, directory_name)
        os.makedirs(destination_path, exist_ok=True)
        move_file(file_path, Path(destination_path, file_path.name), dry_run)
        progress_bar.update(1)
    progress_bar.close()

def main() -> None:
    """

    The main entry point of the file organization script
    Parses command-line arguments, organizes files, and prints success messages
    Returns: 
        None

    """
    parser = argparse.ArgumentParser(description=f"Organize files based on file extensions, e.g. .pdf, .mp3")
    parser.add_argument("source_directory", help=f"Source directory to organize, e.g. '/home/user/Downloads'")
    parser.add_argument("--dry-run", action="store_true", help=f"Run in dry run mode, no files will be moved")
    args = parser.parse_args()
    source_directory = args.source_directory
    dry_run = args.dry_run
    if not os.path.exists(source_directory):
        print(f"Directory not found: {source_directory}, exiting...")
        return
    organize_files(source_directory, dry_run)
    if dry_run:
        print(f"Dry run has finished successfully")
    else:
        print(f"Files organization has finished successfully")

if __name__ == "__main__":
    try:
        logger = configure_logging()
        main()
    except KeyboardInterrupt:
        print(f"\nScript interrupted by user, exiting...")
