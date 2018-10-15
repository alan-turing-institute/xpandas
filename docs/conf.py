import os, sys
import alabaster

needs_sphinx = '1.4.3'

html_theme_path = [alabaster.get_path()]

sys.path.insert(0, os.path.abspath('../xpandas'))

extensions = ['alabaster', 'sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
              'sphinx.ext.autosummary', 'sphinx.ext.viewcode', 'sphinx.ext.coverage',
              'sphinx.ext.doctest', 'sphinx.ext.ifconfig', 'sphinx.ext.pngmath',
              'sphinx.ext.napoleon', 'nbsphinx', 'IPython.sphinxext.ipython_console_highlighting',
              'sphinx.ext.autosectionlabel']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'XPandas'
copyright = u'2017, UCL'

version = ''  # Is set by calling `setup.py docs`
release = ''  # Is set by calling `setup.py docs`

exclude_patterns = ['_build', '**.ipynb_checkpoints']

# pygments_style = 'sphinx'

html_theme = 'alabaster'

html_theme_options = {
    'logo': 'Logo.png',
    'github_user': 'alan-turing-institute',
    'github_repo': 'xpandas',
    'travis_button': True,
    'analytics_id': 'UA-108477151-1'
}


try:
    from xpandas import __version__ as version
except ImportError:
    pass
else:
    release = version

html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
        'donate.html',
    ]
}

html_show_sourcelink = False

html_show_sphinx = False

htmlhelp_basename = 'XPandas-doc'


python_version = '.'.join(map(str, sys.version_info[0:2]))
intersphinx_mapping = {
    'sphinx': ('http://sphinx.pocoo.org', None),
    'python': ('http://docs.python.org/' + python_version, None),
    'matplotlib': ('http://matplotlib.sourceforge.net', None),
    'numpy': ('http://docs.scipy.org/doc/numpy', None),
    'sklearn': ('http://scikit-learn.org/stable', None),
    'pandas': ('http://pandas.pydata.org/pandas-docs/stable', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
}
