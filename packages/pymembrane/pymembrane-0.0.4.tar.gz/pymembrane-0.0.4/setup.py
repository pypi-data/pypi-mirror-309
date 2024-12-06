# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 08:57:50 2020

@author: HEDI
"""

from setuptools import setup, find_packages
import sys
from os import path

# Chemin du répertoire courant
this_directory = path.abspath(path.dirname(__file__))

# Lecture de la version directement à partir du fichier __version__.py
version_path = path.join(this_directory, "pymembrane", "__version__.py")
with open(version_path) as f:
    exec(f.read())

# Lire le contenu de votre README.md pour la longue description
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pymembrane",
    version=__version__,
    description="A Python package for membrane filtration modeling and optimization",
    keywords="wastewater, wastewater treatment, membrane, food process, simulation, optimization",
    author="Hedi ROMDHANA",
    author_email="hedi.romdhana@agroparistech.fr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ROMDHANA/pymembrane",  # Lien vers votre dépôt GitHub
    license="GPLv3",
    install_requires=[
        "numpy>=1.20.3",
        "matplotlib>=3.4.0",
        "scipy>=1.7.3",
        "pandas>=1.2.0",
        "SALib>=1.3.13",
        "cryptography", 
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.7",
    packages=find_packages(),
    package_data={'': ['*'],'pymembrane': ['*','*/*','*/*/*']},
    project_urls={
        "Bug Tracker": "https://github.com/ROMDHANA/pymembrane/issues",
        "Documentation": "https://pymembrane.readthedocs.io/",
        "Source Code": "https://github.com/ROMDHANA/pymembrane",
    },
)
