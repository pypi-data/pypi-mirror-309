from setuptools import setup, find_packages

setup(
    name="gitignore_maker",
    version="0.1.3",
    description="A powerful command-line tool for managing .gitignore files with language-specific templates and size-based filtering.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    author="Eemayas",
    author_email="prashantmanandhar2002@gmail.com",
    url="https://github.com/Eemayas/gitignore_maker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gitignore_maker=gitignore_maker:gitignore_maker",
        ],
    },
    include_package_data=True,
)
