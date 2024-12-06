import os

from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file

try:
    from sphinx_tudelft_theme._version import version as __version__
except ImportError:
    __version__ = "1.0.0"

def copy_stylesheet(app: Sphinx, exc: None) -> None:
    style = os.path.join(os.path.dirname(__file__), 'static', 'tudelft_style.css')
    if app.builder.format == 'html' and not exc:
        staticdir = os.path.join(app.builder.outdir, '_static')
        copy_asset_file(style, staticdir)


def setup(app: Sphinx):
    app.add_css_file('tudelft_style.css')
    app.connect('build-finished', copy_stylesheet)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }