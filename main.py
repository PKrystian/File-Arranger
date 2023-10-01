import os
import shutil
import logging
import argparse
from config import *
from pathlib import Path

logging.basicConfig(filename = LOG_FILE_INFO, level = logging.INFO)
logging.basicConfig(filename = LOG_FILE_ERROR, level = logging.ERROR)

def moveFile(filePath, destinationPath, dryRun = False):
    try:
        if not dryRun:
            shutil.move(filePath, destinationPath)
        logging.info(f"{'DRY RUN: ' if dryRun else ''}Moving {filePath.name} to {destinationPath.name}")
    except FileExistsError:
        backupPath = destinationPath / (filePath.stem + "_backup" + filePath.suffix)
        shutil.move(filePath, backupPath)
        logging.error(f"File {filePath.name} already exists in {destinationPath.name}. Moved to {backupPath}")
        print(f"Error has occurred, logging can be found in {os.path.abspath(LOG_FILE_ERROR)}")
    except Exception as e:
        logging.error(f"Failed to move {filePath} to {destinationPath.name}: {e}")
        print(f"Error has occurred, logging can be found in {os.path.abspath(LOG_FILE_ERROR)}")

def getDirectoryByExtension(extension):
    for category, extensions in DIRECTORY_MAPPING.items():
        if extension in extensions:
            return category
    return OTHERS_CATEGORY

def scanDirectory(baseDirectory):
    for entry in os.scandir(baseDirectory):
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from scanDirectory(entry.path)

def organizeFiles(sourceDirectory, dryRun = False):
    for item in scanDirectory(sourceDirectory):
        filePath = Path(item)
        fileExtension = filePath.suffix.lower()
        directoryName = getDirectoryByExtension(fileExtension)
        destinationPath = Path(sourceDirectory) / directoryName
        destinationPath.mkdir(parents = True, exist_ok = True)
        moveFile(filePath, destinationPath / filePath.name, dryRun)

def main():
    parser = argparse.ArgumentParser(description = "Organize files based on file extensions, e.g. .pdf, .mp3")
    parser.add_argument("sourceDirectory", help = "Source directory to organize, e.g. /home/user/Downloads")
    parser.add_argument("--dry-run", action = "store_true", help = "Run in dry run mode, no files will be moved")
    args = parser.parse_args()
    sourceDirectory = args.sourceDirectory
    dryRun = args.dry_run
    if not os.path.exists(sourceDirectory):
        print(f"Directory not found: {sourceDirectory}, exiting...")
        return
    organizeFiles(sourceDirectory, dryRun)
    if dryRun:
        print(f"Dry run has finished successfully, logging can be found in {os.path.abspath(LOG_FILE_INFO)}")
    else:
        print("Files organization has finished successfully")

if __name__  == "__main__":
    main()
