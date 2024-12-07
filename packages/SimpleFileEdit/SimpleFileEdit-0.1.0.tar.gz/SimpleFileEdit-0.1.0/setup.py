import os
from shutil import rmtree

from setuptools import find_packages, setup, Command
setup(
    name = 'SimpleFileEdit',
    description = 'A small package that simplifies file creation and editing',
    url = 'https://github.com/me/myproject',
    author = 'BravestCheetah',
    version = '0.1.0',
    requires = ['os']
) 

here = os.path.abspath(os.path.dirname(__file__))
