from setuptools import setup, find_packages
from xnxxdltagger import __version__ 

setup(
    name='xnxx-dl-tagger',
    version=__version__,
    description='A MP4 tagger based on directory, filename and creation date.',
    author='Joannes J.A. Wyckmans',
    author_email='johan.wyckmans@gmail.com',
    url='https://github.com/thisisawesome1994/xnxx-dl-tagger',  # Replace with your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        'mutagen',
    ],
    entry_points={
        'console_scripts': [
            'xnxx-dl-tagger = xnxxdltagger.main:main',  # Assuming your main function is in a file called 'main.py'
        ],
    },
)