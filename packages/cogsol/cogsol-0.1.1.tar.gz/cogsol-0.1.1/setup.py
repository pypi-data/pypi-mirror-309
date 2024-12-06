from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cogsol',
    version='0.1.1',
    description='A Python SDK for interacting with an Cognitive API provided by Cognitive Solutions.',
    author='Cognitive Solutions',
    author_email='cognitive.solutions@pyxis.tech',
    url='https://github.com/Pyxis-Cognitive-Solutions/cognitive-sdk',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
