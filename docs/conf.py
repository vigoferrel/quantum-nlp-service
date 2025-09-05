# Configuration file for the Sphinx documentation builder.
# VIGOLEONROCKS API Documentation

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'vigoleonrocks'))

# -- Project information -----------------------------------------------------
project = 'VIGOLEONROCKS'
copyright = '2025, vigoferrel'
author = 'vigoferrel'
release = '2.1.0-supreme'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx_rtd_theme',
    'myst_parser',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.httpdomain',
    'sphinxcontrib.httpexample',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser.parsers.myst',
}

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'analytics_id': 'G-XXXXXXXXXX',  # Google Analytics ID
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_context = {
    "display_github": True,
    "github_user": "vigoleonrocks",
    "github_repo": "quantum-nlp-service",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

# Custom CSS
html_css_files = [
    'custom.css',
]

# -- Extension configuration -------------------------------------------------

# -- Options for autodoc ----------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Todo extension
todo_include_todos = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'flask': ('https://flask.palletsprojects.com/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}

# Type hints configuration
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# Mock imports for modules that might not be available during doc building
autodoc_mock_imports = [
    'tensorflow',
    'torch',
    'transformers',
    'sklearn',
    'numpy',
    'pandas',
    'redis',
    'psycopg2',
    'celery',
    'prometheus_client',
]

# Custom roles for VIGOLEONROCKS
rst_prolog = """
.. role:: critical
   :class: critical

.. role:: policy
   :class: policy

.. role:: quantum
   :class: quantum

.. role:: multilingual
   :class: multilingual
"""

# Add custom directives
def setup(app):
    """Custom setup function for Sphinx"""
    app.add_css_file('custom.css')
    
    # Add custom directives for VIGOLEONROCKS documentation
    from docutils.parsers.rst import directives
    from docutils import nodes
    from sphinx.util.docutils import SphinxDirective
    
    class CriticalPolicyDirective(SphinxDirective):
        """Directive for highlighting critical policies"""
        required_arguments = 1
        optional_arguments = 0
        final_argument_whitespace = True
        has_content = True
        
        def run(self):
            policy_name = self.arguments[0]
            content = '\n'.join(self.content)
            
            container = nodes.container()
            container['classes'] = ['critical-policy']
            
            title = nodes.title(text=f"🚨 CRITICAL POLICY: {policy_name}")
            container += title
            
            content_node = nodes.paragraph(text=content)
            container += content_node
            
            return [container]
    
    app.add_directive('critical-policy', CriticalPolicyDirective)

# API Documentation settings
http_index_shortname = 'VIGOLEONROCKS API'
http_index_localname = "VIGOLEONROCKS API Reference"

# Markdown support
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Custom processing for VIGOLEONROCKS specific content
def process_vigoleonrocks_docstring(app, what, name, obj, options, lines):
    """Process docstrings to highlight VIGOLEONROCKS specific content"""
    for i, line in enumerate(lines):
        # Highlight critical policies
        if 'Math.random' in line or 'random.' in line:
            lines[i] = f"🚫 **CRITICAL**: {line}"
        elif 'background' in line.lower() and ('process' in line.lower() or 'metric' in line.lower()):
            lines[i] = f"🔄 **POLICY**: {line}"
        elif 'quantum' in line.lower():
            lines[i] = f"⚛️  **QUANTUM**: {line}"
        elif any(lang in line.lower() for lang in ['multilingual', 'language', 'translation']):
            lines[i] = f"🌍 **MULTILINGUAL**: {line}"

def setup_vigoleonrocks_autodoc(app):
    """Setup VIGOLEONROCKS specific autodoc processing"""
    app.connect('autodoc-process-docstring', process_vigoleonrocks_docstring)

# Version info
version_info = {
    'major': 1,
    'minor': 0,
    'patch': 0,
    'pre_release': None,
}

# Build info
html_last_updated_fmt = '%Y-%m-%d %H:%M:%S'
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# LaTeX output settings
latex_engine = 'pdflatex'
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': r'''
        \usepackage{emoji}
        \usepackage{xcolor}
        \definecolor{criticalred}{RGB}{220, 20, 60}
        \definecolor{quantumblue}{RGB}{0, 100, 200}
    ''',
}

latex_documents = [
    (master_doc, 'VIGOLEONROCKS.tex', 'VIGOLEONROCKS Documentation',
     'VIGOLEONROCKS Team', 'manual'),
]
