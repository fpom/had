from setuptools import setup, find_packages
from os import path
import hadlib

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="Headers as Dependencies",
      version=hadlib.VERSION,
      description="Generate command-line options for C compiler from used headers",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/fpom/had",
      author="Franck Pommereau",
      author_email="franck.pommereau@univ-evry.fr",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "Topic :: Software Development :: Compilers",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Programming Language :: Python :: 3.7",
                   "Operating System :: OS Independent"],
      packages=find_packages(where="."),
      python_requires=">=3.7",
      install_requires=[],
      package_data={"" : ["*.cfg"]},
      entry_points={"console_scripts": ["had=hadlib.cli:main"]})
