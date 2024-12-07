import setuptools
from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup (
    name="gitverbose",
    description="Easy clone github repo, Internet files.",
    long_description=long_description,
    version="0.5",
    readme='README.md',
    author="caique9014",
    license="LICENSE.txt",
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
        "pathlib",
        "git-clone"
    ]
)