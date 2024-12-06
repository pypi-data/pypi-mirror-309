from setuptools import setup, find_packages

setup(
    name="MachineLearning_MohamadElMokdad",  # Unique name on PyPI
    version="0.0",            # Start with a version, increment for updates
    author="Mohamad El Mokdad", # Your name
    author_email="mmokdad2001@gmail.com",  # Your email
    description="A custom ML library",    # Short description
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",  # README format
    url="https://github.com/yourusername/ML_MohamadElMokdad",  # GitHub URL
    packages=find_packages(),   # Automatically find submodules
    install_requires=[          # List dependencies
        "numpy>=1.18.0",
    ],
    classifiers=[               # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",    # Minimum Python version
)
