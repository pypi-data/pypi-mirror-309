from setuptools import find_packages, setup
from pathlib import Path


setup(
    name='mlbdatatools',
    packages=find_packages(include=['mlbdatatools']),
    url='https://github.com/joeysnclr/mlbdatatools',
    version='0.1.4',
    description='DataFrames, type-safety, and plotting for modern baseball analytics.',
    author='Joey Sinclair',
    install_requires=['pandas', 'numpy', 'matplotlib', 'requests'],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)