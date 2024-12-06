from setuptools import setup, find_packages

setup(
    name="awesomest_search",                   # Package name
    version="0.2.0",                     # Version number
    author="Prakhar Gandhi",                  # Author's name
    author_email="gprakhar0@gmail.com",  # Author's email
    description="Awesomest best fuzzy search",   # Short description
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",
    url="https://github.com/prakHr/awesomest_search",  # URL of the project
    packages=find_packages(),            # Automatically discover modules
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",             # Minimum Python version
    install_requires=[                   # Dependencies
        "mpire"
    ],
)
