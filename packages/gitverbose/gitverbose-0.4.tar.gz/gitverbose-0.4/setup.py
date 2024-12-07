import setuptools
from setuptools import setup

setup (
    name="gitverbose",
    description="Easy clone github repo, Internet files.",
    long_description="Make your life easier while cloning github repo.",
    version="0.4",
    readme='README.md',
    author="caique9014",
    author_email="caiqueonz777@proton.me",
    url = "https://github.com/GitLabBR/gitverbose",
    packages=['gv'],
    entry_points={
        'console_scripts': ['gv=gv.entry:gv_entry_point']
    },
    keywords=[
        'cli',
        'python',
        'github',
        'git',
        'pypi',
        'fun',
        'image',
        'hash',
        'table',
        'typer',
        '3.9',
        'pip'
    ],
    install_requires=[
        "requests",
        "argparse",
        "git-clone"
    ]
)