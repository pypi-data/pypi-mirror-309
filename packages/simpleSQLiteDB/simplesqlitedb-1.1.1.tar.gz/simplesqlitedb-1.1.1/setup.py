from setuptools import setup

from simpleDB import __version__

setup(
    name='simpleSQLiteDB',
    version=__version__,
    license='MIT',
    description='simpleSQLiteDB is a python module to simplify the usage of SQLite3 and more begginer friendly for those starting off with SQL in python. It does the task of creating connections, cursors etc, to enable clean code. It makes the whole process more modular to allow for ease of use for more than 1 database',

    url='https://github.com/KingHacker9000/simpleDB',
    author='Ashish Ajin Thomas',
    author_email='Coolioboss7@gmail.com',

    py_modules=['simpleDB'],
)