"""
Structure tests for iRacing Overlay Application
Tests code structure without requiring dependencies
"""
import sys
import os
import ast

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_file_exists(filepath):
    """Check if a file exists"""
    return os.path.isfile(filepath)


def test_python_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True
    except SyntaxError:
        return False


def test_has_class(filepath, class_name):
    """Check if file contains a specific class"""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return True
        return False
    except:
        return False


def test_has_function(filepath, func_name):
    """Check if file contains a specific function"""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                return True
        return False
    except:
        return False


def run_structure_tests():
    """Run structure tests"""
    print("=" * 50)
    print("Running iRacing Overlay Structure Tests")
    print("=" * 50)
    print()
    
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    tests = []
    
    # Test file existence
    print("Testing file structure...")
    files_to_check = [
        'src/telemetry_client.py',
        'src/overlay_window.py',
        'src/main.py',
        'src/__init__.py',
        'requirements.txt',
        'config.ini',
        'README.md',
    ]
    
    for filepath in files_to_check:
        full_path = os.path.join(base_path, filepath)
        exists = test_file_exists(full_path)
        tests.append(exists)
        status = "✓" if exists else "✗"
        print(f"{status} {filepath}")
    
    print()
    
    # Test Python syntax
    print("Testing Python syntax...")
    python_files = [
        'src/telemetry_client.py',
        'src/overlay_window.py',
        'src/main.py',
    ]
    
    for filepath in python_files:
        full_path = os.path.join(base_path, filepath)
        valid = test_python_syntax(full_path)
        tests.append(valid)
        status = "✓" if valid else "✗"
        print(f"{status} {filepath}")
    
    print()
    
    # Test class definitions
    print("Testing class definitions...")
    class_tests = [
        ('src/telemetry_client.py', 'IRacingClient'),
        ('src/overlay_window.py', 'OverlayWindow'),
        ('src/main.py', 'IRacingOverlayApp'),
    ]
    
    for filepath, class_name in class_tests:
        full_path = os.path.join(base_path, filepath)
        has_class = test_has_class(full_path, class_name)
        tests.append(has_class)
        status = "✓" if has_class else "✗"
        print(f"{status} {filepath} has class {class_name}")
    
    print()
    
    # Test key methods
    print("Testing key methods...")
    method_tests = [
        ('src/telemetry_client.py', 'connect'),
        ('src/telemetry_client.py', 'get_telemetry'),
        ('src/overlay_window.py', 'create_window'),
        ('src/overlay_window.py', 'update_data'),
        ('src/main.py', 'main'),
    ]
    
    for filepath, func_name in method_tests:
        full_path = os.path.join(base_path, filepath)
        has_func = test_has_function(full_path, func_name)
        tests.append(has_func)
        status = "✓" if has_func else "✗"
        print(f"{status} {filepath} has function/method {func_name}")
    
    print()
    print("=" * 50)
    passed = sum(tests)
    total = len(tests)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All structure tests passed!")
        return 0
    else:
        print("✗ Some structure tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_structure_tests())
