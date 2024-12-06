#!/usr/bin/python
from setuptools import find_packages, setup


def read_file(file_name: str) -> str:
    with open(file_name) as fo:
        return fo.read().strip()


setup(
    name="cloudshell-networking-ipinfusion",
    url="http://www.qualisystems.com/",
    author="QualiSystems",
    author_email="info@qualisystems.com",
    packages=find_packages(),
    install_requires=read_file("requirements.txt"),
    tests_require=read_file("test_requirements.txt"),
    python_requires="~=3.7",
    version=read_file("version.txt"),
    package_data={"": ["*.txt"]},
    description="QualiSystems networking IP Infusion specific Package",
    long_description="QualiSystems networking IP Infusion specific Package",
    include_package_data=True,
)
