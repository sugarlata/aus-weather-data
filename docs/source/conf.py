import os
import sys

if True:
    sys.path.insert(0, os.path.abspath("../.."))
    import aus_weather_data

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Australian Weather Data'
copyright = '2023, Nathan Sgarlata'
author = 'Nathan Sgarlata'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx_autodoc_typehints',
    'sphinx.ext.githubpages'
]

todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = "furo"
html_static_path = ['_static']
