# encoding: utf-8

from setuptools import setup, find_packages


install_requires = [
    'numpy',
    'matplotlib',
    'pandas',
]


metadata = {
    'name': 'hackdiet',
    'version': '0.1.0',
    'description': 'Hackdiet inspired plotting in Python.',
    'license': 'Apache License 2.0',
    'author': 'Robert Grant',
    'author_email': 'robert.david.grant@gmail.com',
    'packages': find_packages(),
    'install_requires': install_requires,
    'long_description': open("README.md").read(),
    'platforms': ["Linux", "Mac OS-X", "Windows"],
    'entry_points': {'console_scripts': ['hackdiet = hackdiet.hackdiet:cli']},
}


setup(**metadata)
