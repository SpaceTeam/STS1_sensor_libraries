# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'sts1-sensor-libraries'
copyright = '2024, Simon Köfinger, Florian Rohrer'
author = 'Simon Köfinger, Florian Rohrer'
release = 'v0.3.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.githubpages',
    'myst_parser',
    'autoapi.extension',
]

templates_path = ['_templates']
exclude_patterns = []
autoapi_dirs = ['../../src/sts1_sensor_libraries']

autoapi_options = [
    "members",
    "undoc-members",
    # "private-members",
    # "show-inheritance",
    # "show-module-summary",
    # "special-members",
    # "imported-members",
]

autoapi_python_class_content = 'init'

add_module_names = False
toc_object_entries_show_parents = "hide"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
