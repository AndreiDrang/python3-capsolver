# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

os.chdir("../")
sys.path.insert(0, os.path.abspath("src/"))

for x in os.walk("src/python3_captchaai/"):
    sys.path.insert(0, x[0])

from python3_captchaai import hcaptcha, image_to_text, recaptcha

# -- Project information -----------------------------------------------------

project = "python3-captchaai"
copyright = "2022, AndreiDrang"
author = "AndreiDrang"

# The full version, including alpha/beta/rc tags
release = "0.0.6"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = (
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx.ext.autodoc",
    "pallets_sphinx_themes",
)
intersphinx_mapping = {"python": ("https://docs.python.org/3.10/", None)}
myst_enable_extensions = ["deflist"]
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# Theme config
html_theme = "jinja"
html_theme_options = {"index_sidebar_logo": False}
html_static_path = ["_static"]
html_favicon = "_static/CaptchaAIESm.png"
html_logo = "_static/CaptchaAISm.png"
html_title = f"python3-captchaai ({release})"
html_show_sourcelink = False

# Typehints config
autodoc_typehints = "description"
autodoc_typehints_description_target = "all"
autodoc_typehints_format = "short"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = True
napoleon_attr_annotations = True


autodoc_preserve_defaults = False
autodoc_member_order = "bysource"
autodoc_class_signature = "mixed"
