from setuptools import setup, find_packages

setup(
    name="jkpackager",
    version="1.0.0",
    description="A Python library for packaging scripts into executable formats.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="hobe",
    author_email="hoppyloser11@gmail.com",
    url="https://github.com/hoppygamer/jkpackager",      packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pillow",
        "pefile",
    ],
    entry_points={
        "console_scripts": [
            "jkpackager=jkpackager.packager:main",
        ],
    },
)
