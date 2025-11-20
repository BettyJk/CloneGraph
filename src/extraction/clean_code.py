import re

def clean_code(code, language):
    """
    Clean code: remove comments, normalize whitespace.
    """
    if language == 'python':
        # Remove comments
        code = re.sub(r'#.*', '', code)
        # Remove docstrings
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
    elif language == 'java' or language == 'cpp':
        # Remove // comments
        code = re.sub(r'//.*', '', code)
        # Remove /* */ comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Normalize whitespace
    code = re.sub(r'\s+', ' ', code)
    code = code.strip()
    return code

def clean_files(files):
    """
    Clean a dict of files.
    """
    cleaned = {}
    for filename, content in files.items():
        lang = 'python' if filename.endswith('.py') else 'java' if filename.endswith('.java') else 'cpp'
        cleaned[filename] = clean_code(content, lang)
    return cleaned

if __name__ == "__main__":
    # Example usage
    sample_code = """
    # This is a comment
    def hello():
        print("Hello")  # another comment
    """
    print(clean_code(sample_code, 'python'))