# Kubernetes Pod Proxy Manager

A simple GUI application for managing Kubernetes pod proxies. This tool allows you to:
- View running pods in your Kubernetes cluster
- Set up port forwarding with custom local ports
- Manage multiple proxy connections

## Installation

```bash
pip install hproxy
```

## Usage

After installation, you can run the application using:

```bash
hproxy
```

Requirements:
- Python 3.6 or higher
- kubectl configured with access to your cluster
- tkinter (usually comes with Python)

## Features
- Modern, clean interface
- Easy port forwarding setup
- Real-time pod status monitoring
- Custom port selection (9000-9100)

## License

MIT License

# k8s_pod_proxy/__init__.py
"""
Kubernetes Pod Proxy Manager
A GUI tool for managing Kubernetes pod proxies
"""

__version__ = "0.1.0"