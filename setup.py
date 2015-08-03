from setuptools import setup

setup(
    name='spotty',
    version='0.0.1',
    py_modules=['spotty'],
    entry_points={
        'console_scripts': [
            'spotty = spotty:main',
        ],
    },
    install_requires=[
        'numpy',
        'matplotlib',
    ],
)
