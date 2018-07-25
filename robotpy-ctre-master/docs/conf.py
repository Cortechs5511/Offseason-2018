#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from os.path import abspath, join, dirname

# Insert module path here
sys.path.insert(0, abspath(dirname(__file__)))
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import ctre

# -- RTD configuration ------------------------------------------------

# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# This is used for linking and such so we link to the thing we're building
rtd_version = os.environ.get('READTHEDOCS_VERSION', 'latest')
if rtd_version not in ['stable', 'latest']:
    rtd_version = 'stable'

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'RobotPy CTRE'
copyright = '2017, RobotPy development team'

intersphinx_mapping = {
    'robotpy': ('http://robotpy.readthedocs.io/en/%s/' % rtd_version, None),
    'wpilib': ('http://robotpy-wpilib.readthedocs.io/en/%s/' % rtd_version, None),
}

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '.'.join(ctre.__version__.split('.')[:2])
# The full version, including alpha/beta/rc tags.
release = ctre.__version__

autoclass_content = 'both'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = 'default'

# Output file base name for HTML help builder.
htmlhelp_basename = 'sphinxdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'sphinx.tex', '. Documentation',
   'Author', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'sphinx', '. Documentation',
     ['Author'], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'sphinx', '. Documentation',
   'Author', 'sphinx', 'One line description of project.',
   'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = '.'
epub_author = 'Author'
epub_publisher = 'Author'
epub_copyright = '2017, Author'

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Custom Document processing ----------------------------------------------

import gensidebar
gensidebar.generate_sidebar(globals(), 'ctre')
