
from setuptools import setup, find_packages

setup(
    name="data_hasher_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.3"
    ],
    description="A package to hash data files and verify their hash using MD5.",
    long_description=open("README.md").read(),
    url="https://github.com/yourusername/mypackage",
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    project_urls={
        "Documentation": "https://mypackages/docs",
        "Source": "https://github.com/yourusername/mypackage"
    },
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    python_requires='>=3.8',
    extras_require={
        "excel": ["openpyxl"],
    }
)
