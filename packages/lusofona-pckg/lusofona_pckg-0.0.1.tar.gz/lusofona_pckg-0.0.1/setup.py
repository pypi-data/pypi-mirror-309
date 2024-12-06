from setuptools import setup, find_packages

setup(
    name="lusofona-pckg", 
    version="0.0.1", 
    description="My first Python package", 
    url="https://github.com/rui-moreira-21600035", 
    author="Rui Moreira", 
    author_email="rui.moreira619@gmail.com", 
    license="BSD 2-clause", 
    packages=find_packages(),
    install_requires=[ 'numpy', 'pandas', 'matplotlib', 'seaborn' ] # Add any other dependencies you may need. They will be installed automatically when you install your package.
)