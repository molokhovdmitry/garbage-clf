import os
import shutil
import random


# Define source and target directories
source_dir = '../data/raw/Garbage classification'
target_dirs = {
    'train': '../data/processed/kaggle/train',
    'test': '../data/processed/kaggle/test',
    'val': '../data/processed/kaggle/val'
}

# Get list of all files in the source directory
files = {}
for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)
    if os.path.isdir(folder_path):
        class_name = os.path.basename(folder_path)
        files[class_name] = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            files[class_name].append(file_path)

# Ensure target directories exist
for dir_name in target_dirs.values():
    os.makedirs(dir_name, exist_ok=True)
    for class_name in files:
        os.makedirs(os.path.join(dir_name, class_name))

# Shuffle the files
for class_name in files:
    class_files = files[class_name]
    random.shuffle(class_files)

    # Calculate split sizes
    total_files = len(class_files)
    train_split = int(0.8 * total_files)
    test_split = int(0.1 * total_files)
    print(train_split, test_split)

    # Split the files
    train_files = class_files[:train_split]
    test_files = class_files[train_split:train_split + test_split]
    val_files = class_files[train_split + test_split:]

    # Copy files to target directories
    for file_path in train_files:
        shutil.copy(file_path, os.path.join(target_dirs['train'], class_name))

    for file_path in test_files:
        shutil.copy(file_path, os.path.join(target_dirs['test'], class_name))

    for file_path in val_files:
        shutil.copy(file_path, os.path.join(target_dirs['val'], class_name))

print("Dataset split and files copied successfully.")
