# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Convertly_LINE'
copyright = '2024, Izaro de la Colina, Libe Galdos, Eugenia Poza and Nerea Torner'
author = 'Izaro de la Colina, Libe Galdos, Eugenia Poza and Nerea Torner'
release = 'V0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.doctest',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.todo',
              'sphinx.ext.intersphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'


# Opciones adicionales de configuración
html_static_path = ['_static']
todo_include_todos = True  # Muestra las notas TODO
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}

# Configuración de Napoleon para soportar docstrings estilo Google o NumPy
napoleon_google_docstring = True
napoleon_numpy_docstring = True