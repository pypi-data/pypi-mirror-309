from setuptools import setup, find_packages

setup(
    name="jkpackager",
    version="1.0.1",
    description="A Python library for packaging scripts into executable formats.",
    long_description=open("README.md").read(),  # Make sure the README.md exists
    long_description_content_type="text/markdown",
    author="hobe",  # Replace with your actual name
    author_email="hoppyloser11@gmail.com",  # Replace with your actual email
    url="https://github.com/hoppygamer/jkpackager",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pillow",  # For handling icons (if needed)
        "pefile",  # For packaging .exe (if needed)
        # Add any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "jkpackager=jkpackager.packager:main",  # This tells Python how to run the main function in packager.py
        ],
    },
)
