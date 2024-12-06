from setuptools import setup

setup(
    name='pyramid2',
    version='0.0.1',
    packages=['pyramid2'],
    entry_points={
        'console_scripts': [
            'get-flag=pyramid2:get_flag',
        ],
    },
)