# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'sts1-sensors'
copyright = '2024, Simon Köfinger, Florian Rohrer'
author = 'Simon Köfinger, Florian Rohrer'
release = 'v0.5.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.githubpages',
    'myst_parser',
    'autoapi.extension',
]

templates_path = ['_templates']
exclude_patterns = []
autoapi_dirs = ['../../src/sts1_sensors']
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
autoapi_python_use_implicit_namespaces = True
# autoapi_keep_files = True
autodoc_typehints = "description"
add_module_names = False
toc_object_entries_show_parents = "hide"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

def skip_member_variables(app, what, name, obj, skip, options):
    if what == "attribute":
       skip = True
    elif what == "module" and "Abstract" in name or "PatchedSMBus" in name:
       skip = True
    return skip

def setup(sphinx):
   sphinx.connect("autoapi-skip-member", skip_member_variables)
