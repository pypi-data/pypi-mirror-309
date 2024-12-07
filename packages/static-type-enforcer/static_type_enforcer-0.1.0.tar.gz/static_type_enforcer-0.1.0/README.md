# Enforcer

**Enforcer** is a lightweight Python decorator for enforcing type hints at runtime. It ensures that function arguments match their specified types, providing a simple and intuitive solution for runtime type validation.

## Features

- Enforce type hints at runtime for functions.
- Lightweight and dependency-free.
- Compatible with Python 3.7 and later.

## Installation

You can install Enforcer via pip (coming soon):

```python
from enforcer import enforce_types

@enforce_types
def greet(name: str, age: int):
    print(f"{name} is {age} years old!")

# Valid call
greet("Alice", 25)

# Invalid call
greet("Alice", "twenty-five")  # Raises TypeError

```

## Contributing

Contributions are welcome! Please check the [issues](https://github.com/WazedKhan/enforcer/issues) for tasks that need help.
