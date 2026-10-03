# Decorative Parts Library

The decorative\_parts library provides utilities for enhancing and decorating functions in Python.

## Usage

To get started, install the library:
```bash
pip install decorative-parts
```

### Module Features

#### `src/decorative_parts/timed_execution`

This module implements the `@timed` decorator for measuring function execution time.

**Description:**
The `@timed` decorator wraps a function to automatically log its runtime in nanoseconds, providing insights into performance bottlenecks. It is highly configurable through its arguments.

**Functionality:**
*   Uses `functools.wraps` and Python's `perf_counter_ns()` for accurate timing measurements.
*   The inner logging function (`_printout`) can be customized using the `logger_func` parameter, allowing users to control where and how runtime information is reported (e.g., changing the destination from stdout).

**Parameters:**
*   `:param logger_func`: The callback function used for logging results (defaults to standard printout).
*   `:param message_template`: A string template defining how the final performance statistics are formatted.
*   `:param decorator_args`: Additional keyword arguments passed to the logging callback.

**Example:**
```python
from decorative_parts.timed_execution import timed

@timed(logger_func=print, message_template="Function: {func_name} ran in {diff} ns") # Custom logger and template
def complex_calculation():
    # Simulate some work that takes time
    pass
```