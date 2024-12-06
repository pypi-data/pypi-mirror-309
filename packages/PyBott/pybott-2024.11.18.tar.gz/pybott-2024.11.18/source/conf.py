# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', 'src').resolve()))


autodoc_mock_imports =  ["pandas", "numpy", "scipy", "numpy.linalg"] 


project = 'PyBott'
copyright = '2024, Pierre Wulles'
author = 'Pierre Wulles'
release = 'Stable Novembre 2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',  # Ajoutez cette ligne
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_theme = 'alabaster'
html_static_path = ['_static']
