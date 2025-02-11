import os
import shutil
from datetime import datetime
from pathlib import Path

def verify_path(path, is_source=True):
    """Verify if a path exists and print detailed information"""
    path_type = "Source" if is_source else "Destination"
    print(f"\nChecking {path_type} Directory:")
    print(f"Path: {path}")
    
    try:
        # Check if path exists
        if os.path.exists(path):
            print(f"✓ Path exists")
            
            # Check if it's a directory
            if os.path.isdir(path):
                print(f"✓ Path is a directory")
                
                # Check if we have read access (for source) or write access (for destination)
                if is_source:
                    if os.access(path, os.R_OK):
                        print(f"✓ Have read permission")
                    else:
                        print(f"✗ No read permission")
                else:
                    if os.access(path, os.W_OK):
                        print(f"✓ Have write permission")
                    else:
                        print(f"✗ No write permission")
                        
                # For source directory, check if it contains any files
                if is_source:
                    files = list(Path(path).glob('*'))
                    print(f"✓ Contains {len(files)} files/directories")
            else:
                print(f"✗ Path is not a directory")
        else:
            print(f"✗ Path does not exist")
            
    except Exception as e:
        print(f"✗ Error checking path: {str(e)}")
    
    print("-" * 50)

def backup_files():
    # Define the source and destination paths
    source_dir = r"C:\Users\Prakash\Desktop\Backup Path"
    dest_dir = r"C:\Users\Prakash\Documents\Backup Destination"
    
    print("Starting backup verification...")
    
    # Verify both paths before proceeding
    verify_path(source_dir, is_source=True)
    verify_path(dest_dir, is_source=False)
    
    # Convert to Path objects
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    # Check source directory
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return
    
    # Try to create destination directory if it doesn't exist
    try:
        dest_path.mkdir(parents=True, exist_ok=True)
        print(f"Destination directory ready: {dest_dir}")
    except Exception as e:
        print(f"Error creating destination directory: {str(e)}")
        return
    
    # Track statistics
    files_copied = 0
    files_failed = 0
    
    print("\nStarting file backup...")
    print("-" * 50)
    
    # Iterate through files in source directory
    try:
        for source_file in source_path.glob('*'):
            if source_file.is_file():
                try:
                    # Generate destination file path
                    dest_file = dest_path / source_file.name
                    
                    # If file exists, add timestamp to filename
                    if dest_file.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest_file = dest_path / f"{dest_file.stem}_{timestamp}{dest_file.suffix}"
                    
                    # Copy the file
                    shutil.copy2(source_file, dest_file)
                    print(f"✓ Backed up: {source_file.name}")
                    files_copied += 1
                    
                except Exception as e:
                    print(f"✗ Failed to backup {source_file.name}: {str(e)}")
                    files_failed += 1
    except Exception as e:
        print(f"Error accessing source directory: {str(e)}")
    
    # Print summary
    print("\nBackup Summary:")
    print("-" * 50)
    print(f"Files successfully backed up: {files_copied}")
    print(f"Files failed to backup: {files_failed}")
    print(f"Total files processed: {files_copied + files_failed}")

if __name__ == "__main__":
    try:
        backup_files()
    except KeyboardInterrupt:
        print("\nBackup process interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

    input("\nPress Enter to exit...")
    