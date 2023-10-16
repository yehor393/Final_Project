from setuptools import setup, find_packages

setup(
    name='bot_helper',
    version='0.0.1',
    packages=find_packages(),
    author='group_5',
    description='bot-helper',
    install_requires = ['twilio',],
    entry_points={
        'console_scripts': [
            'mycli = Final_Project.main:main'
        ],
    },
)