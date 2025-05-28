# ALX Backend Python: 0x03 - Unittests and Integration Tests

This project focuses on writing unittests and integration tests for Python modules as part of the **ALX Backend Specialization**. The main goals are to validate correct behavior, detect regressions, and ensure reliability in your Python code using proper testing techniques.

## 📁 Directory: `0x03-Unittests_and_integration_tests`

This directory contains:

- `utils.py`: Utility module with helper functions like `access_nested_map`.
- `test_utils.py`: Unit tests for functions in the `utils` module.

## 🧪 Task Highlights

### Task 0: Parameterize a Unit Test

- Create a class `TestAccessNestedMap` that inherits from `unittest.TestCase`.
- Use the `@parameterized.expand` decorator to test the function `access_nested_map` for different input cases.
- Assertions are used to verify the correctness of the outputs.

## ✅ Requirements

- **Python Version**: 3.7
- **Style Guide**: Code follows [PEP8](https://peps.python.org/pep-0008/) via `pycodestyle` (version 2.5)
- All files:
  - Must start with `#!/usr/bin/env python3`
  - Must end with a new line
  - Must be executable (`chmod +x <filename>`)
- All Python modules, classes, and functions include full docstrings explaining their purpose.
- All functions are **type-annotated**.

## 🛠️ Installation

To install dependencies:

```bash
pip install parameterized pycodestyle==2.5.0
```
