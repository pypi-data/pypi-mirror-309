from setuptools import setup, find_packages

setup(
    name="Modular_programing",  # Package name (unique on PyPI)
    version="1.0.0",           # Package version
    author="Your Name",        # Your name
    author_email="your.email@example.com",  # Your email
    description="A modular calculator package for addition, subtraction, etc.",
    long_description=open("README.md").read(),  # Load long description from README.md
    long_description_content_type="text/markdown",  # Description format
    url="https://github.com/yourusername/Modular_programing",  # Project's repository URL
    packages=find_packages(),  # Automatically find all packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
    install_requires=[],      # List dependencies here
    license="MIT",            # Specify license
)
