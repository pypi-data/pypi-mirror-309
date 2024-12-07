import setuptools
from setuptools import setup

setup (
    name="gitverbose",
    description="Easy clone github repo, Internet files.",
    version="0.1",
    author="caiyt",
    author_email="oldtimesonz@gmail.com",
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