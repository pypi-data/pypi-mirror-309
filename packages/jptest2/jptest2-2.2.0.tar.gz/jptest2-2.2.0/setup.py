import os

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='jptest2',
    version=os.getenv('PACKAGE_VERSION', '1.0'),
    author='Eric Tröbs',
    author_email='eric.troebs@tu-ilmenau.de',
    description='write graded unit tests for Jupyter Notebooks in a few lines of code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/erictroebs/jptest',
    project_urls={
        'Bug Tracker': 'https://github.com/erictroebs/jptest/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
    install_requires=[
        'jupyter',
        'aiofiles~=24.1.0'
    ],
    extras_require={
        'demo': [
            'watchfiles~=0.24.0'
        ],
        'sqlite': [
            'aiosqlite~=0.20.0'
        ]
    }
)
