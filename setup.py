from setuptools import setup, find_packages

setup(
    name="chcli",
    version="1.0",
    packages=find_packages(),
    py_modules=['chcli'],
    install_requires=[
        'click',
        'pygments',
        'pathlib',
        'pydantic',
        'requests',
        'beautifulsoup4'
    ]
)