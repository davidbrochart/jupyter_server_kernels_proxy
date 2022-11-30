# Jupyter Server Kernels Proxy

In one terminal/environment:

```console
pip install fps_uvicorn
pip install fps_kernels
pip install fps-noauth

# launch a terminal server at http://127.0.0.1:8000
fps-uvicorn --port=8000 --no-open-browser
```

In another terminal/environment:

```console
pip install https://github.com/davidbrochart/jupyter_server/archive/kernels_extension.zip
pip install jupyter_server_kernels_proxy
pip install jupyterlab

# launch JupyterLab at http://127.0.0.1:8888 and proxy kernels at http://127.0.0.1:8000
jupyter lab --port=8888 --KernelsProxyExtensionApp.proxy_url='http://127.0.0.1:8000'
```

Kernels should now be served from http://127.0.0.1:8000.
