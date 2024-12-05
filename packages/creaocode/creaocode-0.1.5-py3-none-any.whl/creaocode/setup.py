from setuptools import setup, find_packages

setup(
    name='creaocode',
    version='0.1.1',
    packages=find_packages(include=['*', '*.core', '*.core.*']),
    install_requires=[
        # List your package dependencies here
    ],
    author='dev@creao.ai',
    author_email='dev@creao.ai',
    description='Creao AI Core Library',
    url='https://www.creao.ai/login',
    classifiers=[
        # Trove classifiers
    ],
)
