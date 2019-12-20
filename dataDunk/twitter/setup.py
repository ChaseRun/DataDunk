"""
DataDunk:twitter python modules.

Chase Austin (chase7867@gmail.com)
"""

from setuptools import setup

setup(
    name="twitter",
    version="0.1",
    author="Chase Austin",
    author_email="chase7867@gmail.com",
    description="This is my DataDunk Package",

    url="https://dataDunke.app",   # project home page
    project_urls={
        "Github": "https://github.com/ChaseAustin/DataDunk"
    },
    packages=['twitter'],
    include_package_data=True,
    install_requires=[
        "click==7.0",
        "pymongo==3.10.0",
        "datetime==4.3",
        "tweepy==3.8.0"
    ],
)
