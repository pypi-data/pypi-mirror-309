from setuptools import setup, find_packages

# Read dependencies from requirements.txt
def read_requirements():
    with open("requirements.txt") as req_file:
        return req_file.read().splitlines()

setup(
    name="ComIss",  # Replace with your package's name
    version="0.1.0",
    author="ComIss team",
    author_email="boazwu@uw.edu",
    description="Commitment Issues",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/edwardyeung04/commitment-issues",  # URL to your code repository
    packages=find_packages(),
    package_data={
        "": ["cli.py"],  # "" means the root directory
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
    install_requires=read_requirements(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ComIss=cli_interface.cli:main",  # Format: "command-name=module:function"
        ],
    },
)
