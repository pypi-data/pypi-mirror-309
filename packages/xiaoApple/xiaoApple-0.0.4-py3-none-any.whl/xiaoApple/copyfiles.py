import os
import shutil
import hashlib

def calculate_md5(file_path):
    """
    Calculate the MD5 hash of a file.
    
    :param file_path: Path to the file
    :return: MD5 hash of the file
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_missing_files(src_dir, dest_dir, ignore_subdir=None):
    """
    Copies files from src_dir to dest_dir if they do not exist in dest_dir.
    The function works recursively for all subdirectories, but ignores a specified subdirectory.
    
    :param src_dir: Source directory (path2)
    :param dest_dir: Destination directory (path1)
    :param ignore_subdir: Name of the subdirectory to ignore
    """
    count_files = 0 
    count_links = 0
    count_dirs = 0  
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        # Skip the ignored subdirectory if it exists at the first level
        if ignore_subdir and os.path.basename(root) == ignore_subdir and root == os.path.join(src_dir, ignore_subdir):
            continue

        # Calculate the corresponding relative path in the destination directory
        rel_path = os.path.relpath(root, src_dir)
        dest_path = os.path.join(dest_dir, rel_path)

        # Ensure the destination subdirectory exists
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            count_dirs +=1


        # Copy missing files and symlinks
        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_path, file)

            # Check if the source file exists
            if os.path.exists(src_file_path):
                # If the file is a symlink, create a symlink in the destination
                if os.path.islink(src_file_path):
                    link_target = os.readlink(src_file_path)
                    if not os.path.exists(dest_file_path):
                        os.symlink(link_target, dest_file_path)
                        count_links += 1 
                        # print(f"Created symlink {src_file_path} -> {dest_file_path}")
                # If the file is a regular file, copy it
                elif os.path.isfile(src_file_path):
                    if not os.path.exists(dest_file_path):
                        shutil.copy2(src_file_path, dest_file_path)  # copy2 preserves metadata
                        count_files += 1
                        # print(f"Copied {src_file_path} to {dest_file_path}")
                    else:
                        # Calculate MD5 hashes and compare
                        src_hash = calculate_md5(src_file_path)
                        dest_hash = calculate_md5(dest_file_path)
                        if src_hash != dest_hash:
                            print(f"Hash mismatch: {src_file_path} and {dest_file_path}")
    print( f"recovery reports:\n    {count_files} files, {count_links} links, {count_dirs} directories" )





# copy_missing_files(path2, path1, ignore_subdir)