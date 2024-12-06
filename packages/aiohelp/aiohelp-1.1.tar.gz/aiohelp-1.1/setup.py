from setuptools import setup, find_packages

VERSION = '1.1'
DESCRIPTION = 'Easy tool for help commands in aiogram'

setup(
    name="aiohelp",
    version=VERSION,
    author="ilpy",
    author_email="<ilpy@proton.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["aiogram"]
)