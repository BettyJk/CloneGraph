import os
import glob

def load_code_files(directory):
    """
    Load raw code files from a directory.
    Supports Python, Java, C++ files.
    Returns a dict of filename to content.
    """
    extensions = ['*.py', '*.java', '*.cpp', '*.h']
    files = {}
    for ext in extensions:
        for filepath in glob.glob(os.path.join(directory, '**', ext), recursive=True):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                files[os.path.relpath(filepath, directory)] = f.read()
    return files

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python load_code.py <directory>")
        sys.exit(1)
    files = load_code_files(sys.argv[1])
    print(f"Loaded {len(files)} files")
    # Save to data/samples or something, but for now just print