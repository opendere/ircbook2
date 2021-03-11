from setuptools import setup, find_packages


setup(
    name='ircbook',
    version='2.0',
    packages=find_packages(),
    package_dir={'': '.'},
    requires=[
        'sqlalchemy',
    ],
    test_suite='tests'
)
