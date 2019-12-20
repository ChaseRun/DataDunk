"""
DataDunk:mongo python modules.

Chase Austin (chase7867@gmail.com)
"""

from setuptools import setup, find_packages

setup(
    name="DataDunk",
    version="0.1",
    author="Chase Austin",
    author_email="chase7867@gmail.com",
    description="This is my DataDunk Package",

    url="https://dataDunke.app",   # project home page
    project_urls={
        "Github": "https://github.com/ChaseAustin/DataDunk"
    },

    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=[
        "click==7.0",
        "pycodestyle==2.5.0",
        "pydocstyle==4.0.1",
        "pylint==2.4.3",
        "pytest==5.2.1",
        "nba_api==1.1.5",
        "pymongo==3.10.0",
        "requests==2.22.0",  
        "datatime==4.3"
    ],
)
