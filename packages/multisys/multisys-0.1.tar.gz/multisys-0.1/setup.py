import setuptools
from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="multisys",
    description="Build and publish your python project easily.",
    version="0.1",
    author="caique9014",
    entry_points={
        "console_scripts": ['multisys=multisys.entry:multisys_entry_point']
    },
    readme="README.txt",
    license="LICENSE.txt",
    author_email="caiqueonz777@proton.me",
    install_requires=['argparse','setuptools','poetry','build', 'twine', 'pathlib'],
    url="https://github.com/GitLabBR/multisys",
    keywords=[
        'cli',
        'build',
        'command',
        'cmd',
        'pypi',
        'pip',
        'python',
        'publish',
        'auto',
        'automatic',
        'automation'
    ],
    long_description=long_description
)