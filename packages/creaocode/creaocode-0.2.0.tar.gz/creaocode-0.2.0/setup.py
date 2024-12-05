from setuptools import setup, find_packages

setup(
    name='creaocode',
    version='0.2.0',
    packages=find_packages(include=['creaocode', 'creaocode.*']),
    install_requires=[
        'jinja2',
        'exa_py',
        "openai",
        "tqdm"
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
