from ._version import __version__


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "jupyterlab-a11y-checker"
    }]
    
def load_jupyter_server_extension(app):
    from .server_extension import load_jupyter_server_extension
    load_jupyter_server_extension(app)
