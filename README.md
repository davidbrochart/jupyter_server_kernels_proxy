# Jupyter Server Kernels Proxy

This tool allows you to use notebooks on a target machine without installing the whole JupyterLab
environment. The JupyterLab server will still be running on your host (development machine) but the
kernels (notebooks) will be executed remotely.

### Setup the target

Inside the target terminal/environment (this will be the side running the Python kernel code):

```console
pip install fps_uvicorn
pip install fps_kernels
pip install fps-noauth

# launch a terminal server at http://0.0.0.0:8000
# beware, it will be freely accessible to anyone on the local network!
fps-uvicorn --host=0.0.0.0 --port=8000 --no-open-browser
```

### Setup the host

On your host terminal/environment (your development machine, will accept connections from your browser):

```console
pip install https://github.com/davidbrochart/jupyter_server/archive/kernels_extension.zip
pip install jupyter_server_kernels_proxy
pip install jupyterlab

# launch JupyterLab at http://127.0.0.1:8888 and run kernels at http://<ip-of-the-target>:8000
jupyter lab --port=8888 --KernelsProxyExtensionApp.proxy_url='http://<ip-of-the-target>:8000'
```

Kernels should now be served from http://<ip-of-the-target>:8000 and can be worked with by connecting
to http://localhost:8888/lab .
