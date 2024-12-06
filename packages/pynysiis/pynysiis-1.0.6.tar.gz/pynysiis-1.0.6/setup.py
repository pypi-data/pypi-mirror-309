# coding: utf-8
import sys
from setuptools import setup, find_packages  # noqa: H301
from distutils.core import Extension
from os import path

NAME = "pynysiis"
VERSION = "1.0.6"
REQUIRES = ["pydantic"]

# Read long description
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'LONG_DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Platform-specific macros
macros = []
if sys.platform.startswith('freebsd') or sys.platform == 'darwin':
    macros.append(('PLATFORM_BSD', '1'))
elif 'linux' in sys.platform:
    macros.append(('_GNU_SOURCE', ''))

setup(
    name=NAME,
    version=VERSION,
    description="NYSIIS phonetic encoding algorithm.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Finbarrs Oketunji",
    author_email="f@finbarrs.eu",
    url="https://finbarrs.eu/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRES,
    zip_safe=False,
    python_requires=">=3.8",  # Changed to support Python 3.8 and above
    project_urls={
        "Bug Tracker": "https://github.com/0xnu/nysiis/issues",
        "Changes": "https://github.com/0xnu/nysiis/blob/main/CHANGELOG.md",
        "Documentation": "https://github.com/0xnu/nysiis/blob/main/README.md",
        "Source Code": "https://github.com/0xnu/nysiis",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    setup_requires=["wheel"],
    keywords=[
        "nysiis",
        "phonetic",
        "encoding",
        "algorithm",
        "name matching",
        "fuzzy matching",
        "sound matching",
    ],
    license='MIT',
)