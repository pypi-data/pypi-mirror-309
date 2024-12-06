from setuptools import setup, find_packages

setup(
    name="twsc",
    version="0.9.1",
    description="A tool to clean trailing whitespace from recently changed lines or an entire codebase.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ramy Moussa",
    author_email="ramymaster99@gmail.com",
    url="https://github.com/letsgogeeky/twc",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "twsc=src.main:clean_trailing_whitespace",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['setuptools'],
)
