from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.3' 
DESCRIPTION = 'sonarlight'
LONG_DESCRIPTION = Path("README.md").read_text()

setup(
    name="sonarlight", 
    version=VERSION,
    author="Kenneth Thorø Martinsen",
    author_email="kenneth2810@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    keywords=['python'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Oceanography",
        "Topic :: Scientific/Engineering :: GIS"
    ]
)