from setuptools import setup, find_packages

setup(
    name="kyu_nahi_horahi_padhai",  # Package name (unique on PyPI)
    version="0.1.0",  # Initial version (use semantic versioning)
    description="A Python library for tracking and analyzing coding time.",
    long_description=open("README.md").read(),  # Use README.md as the long description
    long_description_content_type="text/markdown",  # Markdown format
    author="Sudarsh",
    author_email="sudarshchatur@gmail.com",
    url="https://github.com/hackermans1/code-time-tracker",  # GitHub repository URL
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        "pandas",        # Add your dependencies here
        "matplotlib",
        "watchdog",
        "click"
    ],
    entry_points={
        "console_scripts": [
            "code-time-tracker=code_time_tracker.cli:cli",  # CLI command
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the Python version
)

