from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(    name="fitbit-takeout-extractor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Extract and analyze Fitbit data from Google Takeout exports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YourGithubUsername/fitbit-takeout-extractor",
    project_urls={
        "Bug Tracker": "https://github.com/YourGithubUsername/fitbit-takeout-extractor/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=2.12.0',
            'flake8>=4.0.0',
            'black>=22.0.0',
            'mypy>=0.910',
        ],
    },
    entry_points={
        'console_scripts': [
            'extract-heart-rate=fitbit_extractor.command_line:heart_rate_command',
            'extract-calories=fitbit_extractor.command_line:calories_command',
        ],
    },
)
