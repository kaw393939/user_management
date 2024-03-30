# pytest.ini
[pytest]
# Specifies that tests are contained in the 'tests' folder
testpaths = tests

# Allows verbose output for test results
addopts = -v

# Automatically discover test files matching 'test_*.py' or '*_test.py'
python_files = test_*.py *_test.py

# Automatically discover test classes that match 'Test*' (excluding the base class 'Test')
python_classes = Test*

# Automatically discover test functions that match 'test_*'
python_functions = test_*

# Option to add markers for different test categories, like 'slow' or 'fast'
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    fast: marks tests as fast (deselect with '-m "not fast"')

# Option to configure additional plugins if needed
# plugins =
#     plugin1
#     plugin2

# Option to adjust logging level, useful for debugging
# log_level = INFO