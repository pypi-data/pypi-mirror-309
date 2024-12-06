from setuptools import setup, find_packages

setup(
    name="giniindex",        # Replace with your desired package name
    version="0.1.0",                 # Version number
    author="Sam Manuel",
    author_email="",
    description="A python package with a ranker function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # GitHub or project URL
    packages=find_packages(),       # Automatically find the package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',         # Minimum Python version
)
