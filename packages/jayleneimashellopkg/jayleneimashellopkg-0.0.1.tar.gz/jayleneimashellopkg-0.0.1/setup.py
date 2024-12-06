from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Jaylen Eimas\'s first pip module'
LONG_DESCRIPTION = 'A package that Jaylen Eimas just uploaded.'

# Setting up
setup(
    name="jayleneimashellopkg",
    version=VERSION,
    author="Jaylen Eimas First Package",
    author_email="<je87794n@pace.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['wcwidth'],
    keywords=['python', 'text', 'unicode'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
