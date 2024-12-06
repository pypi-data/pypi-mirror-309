from setuptools import setup, find_packages

name = "dpt"
packages = [pkg for pkg in find_packages() if pkg.startswith(name)]

setup(
    name=name,
    version="1.2.2",
    author="DF",
    author_email="your_email@example.com",
    packages=packages,
    install_requires=["GitPython>=3.1.41", "pymongo>=4.6.1", "jsonschema>=4.6.0"],
)
