from setuptools import setup, find_packages
import pathlib

here = pathlib.Path("Bicimad").parent.resolve()

long_description = (here / "README.md").read_text(encoding='utf-8')

setup(
    name='my_BiciMad_Project',
    version='0.0.1',
    packages=find_packages(include=["Bicimad"], exclude=["tests"]),
    install_requires=[
       'pandas',
        'requests'
    ]
)

