from os import path, walk

from setuptools import setup

setup(
    packages=[
        path.join(root).replace("\\", ".")
        for root, _, files in walk("packer")
        if "__init__.py" in files
    ],
)
