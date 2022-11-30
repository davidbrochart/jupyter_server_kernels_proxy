from .app import KernelsProxyExtensionApp


__version__ = "0.1.0"


def _jupyter_server_extension_points():  # pragma: no cover
    return [
        {
            "module": "jupyter_server_kernels_proxy.app",
            "app": KernelsProxyExtensionApp,
        },
    ]
