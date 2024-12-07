import pytest
from type_enforcer.main import enforce_types


@enforce_types
def greet(name: str, age: int):
    return f"{name} is {age} years old."


def test_valid_inputs():
    assert greet("Alice", 25) == "Alice is 25 years old."


def test_invalid_name_type():
    with pytest.raises(TypeError, match="Argument 'name' must be str"):
        greet(123, 25)


def test_invalid_age_type():
    with pytest.raises(TypeError, match="Argument 'age' must be int"):
        greet("Alice", "twenty-five")

@enforce_types
def greet_with_default(name: str, age: int = 30):
    return f"{name} is {age} years old."

def test_valid_default_argument():
    assert greet_with_default("Bob") == "Bob is 30 years old."

def test_invalid_default_argument():
    with pytest.raises(TypeError):
        greet_with_default("Bob", "thirty")

@enforce_types
def multiply(a: int, b: int):
    return a * b

def test_valid_keyword_args():
    assert multiply(a=3, b=4) == 12

def test_invalid_keyword_args():
    with pytest.raises(TypeError):
        multiply(a="three", b=4)
