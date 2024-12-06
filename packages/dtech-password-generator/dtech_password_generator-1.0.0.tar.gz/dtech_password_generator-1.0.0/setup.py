from setuptools import setup, find_packages

setup(
    name="dtech_password_generator",            # Name of your package
    version="1.0.0",                      # Version
    description="A simple password generator package.",  # Short description
    long_description=open("README.md").read(),  # Optional, include README as long description
    long_description_content_type="text/markdown",
    author="Daniel Wangari",
    author_email="danielnjama2015@gmail.com",
    license="MIT",                        # Choose an appropriate license
    packages=find_packages(),             # Automatically find sub-packages
    install_requires=open("requirements.txt").read().splitlines(),  # Dependencies
    python_requires=">=3.6",              # Minimum Python version
    classifiers=[                         # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
