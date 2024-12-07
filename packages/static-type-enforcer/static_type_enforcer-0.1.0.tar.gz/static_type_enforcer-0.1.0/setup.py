from setuptools import setup, find_packages
import pathlib

# Path to the directory containing README.md
current_dir = pathlib.Path(__file__).parent

# Read the long description from README.md
long_description = (current_dir / "README.md").read_text()

setup(
    name="static_type_enforcer",  # Package name
    version="0.1.0",  # Version number
    packages=find_packages(),  # Automatically find packages
    install_requires=[],  # Specify dependencies here
    python_requires=">=3.7",  # Minimum Python version required
    description="A lightweight decorator for enforcing type hints at runtime.",
    long_description=long_description,  # Use the README as the long description
    long_description_content_type="text/markdown",  # Markdown format
    url="https://github.com/WazedKhan/enforcer",  # Project's homepage
    author="Wajed Khan",  # Author's name
    author_email="wajed.abdul.khan@gmail.com",  # Author's email
    license="MIT",  # License type
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
