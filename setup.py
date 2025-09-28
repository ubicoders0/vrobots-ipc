from setuptools import setup, find_packages

setup(
    name="ubicoders-vrobots-ipc",
    version="0.0.0",
    license="MIT",
    author="Elliot Lee",
    author_email="info@ubicoders.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/ubicoders0/vrobots-ipc",
    keywords="ubicoders virtual robots ipc for pc",
    install_requires=[
        "websockets",
        "websocket-client",
        "numpy",
        "flatbuffers==23.5.26",
        "fastapi",
        "uvicorn",
        "asyncio",
        "requests",
        "psutil",
        "dash",
        "plotly",
        "colorama",
        "matplotlib",
        "pyqt5",
        "pyqtgraph",
        "pandas",
        "scipy",
        "ipython",
        "ipykernel",
        "jupyterlab",
        "ipympl",
    ],
)






