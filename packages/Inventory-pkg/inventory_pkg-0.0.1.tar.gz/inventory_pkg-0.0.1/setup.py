from setuptools import setup, find_packages

setup(
    name="Inventory_pkg",  # Replace with your package name
    version="0.0.1",
    author="Avnash",
    author_email="avinashlone32@gmail.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here
        # Example: "requests>=2.25.1",
    ],
)
