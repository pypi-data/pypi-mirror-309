# logorator
A decorator-based logging library for Python, featuring hierarchical structure, ANSI color support, and configurable outputs.

## Installation
```bash
pip install logorator
```
## Quick Start
```python
from logorator import Logger

@Logger()
def example_function(x, y):
    return x + y

example_function(3, 5)

# Output:
# Running example_function
#  3
#  5
# Finished example_function Time elapsed: 0.10 ms
```

## Features
- Function Call Logging: Logs function calls, arguments, and execution times.
- Custom Notes: Add notes to your logs.
- ANSI Color Support: Makes console logs visually appealing.
- File Output: Write logs to a file, creating directories if needed.
- Thread-Safe Logging: Handles nested and concurrent function calls.

