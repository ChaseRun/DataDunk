"""
DataDunk:mongo python modules.

Chase Austin (chase7867@gmail.com)
"""
from setuptools import setup, find_packages

setup(
    name="mongo",
    version="0.1",
    author="Chase Austin",
    author_email="chase7867@gmail.com",
    description="This is my DataDunk Package",

    url="https://dataDunke.app",   # project home page
    project_urls={
        "Github": "https://github.com/ChaseAustin/DataDunk"
    },
    py_
    packages=['mongo'],
    include_package_data=True,
    install_requires=[
        "click==7.0",
        "nba_api==1.1.5",
        "pymongo==3.10.0",
        "requests==2.22.0",  
        "datetime==4.3"
    ],
)
