from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.5"
DESCRIPTION = "A BASIC VOICE GENERATOR THIS VERSION IS SUPPORTING TELE BOT"


setup(
    name="getvoice",
    version=VERSION,
    author="annoying boy",
    author_email="rppareek091@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_require=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ] 
)