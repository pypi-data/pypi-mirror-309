import os
from setuptools import setup, find_packages


__DIRNAME__ = os.path.dirname(os.path.abspath(__file__))
BASE_PACKAGE = "spatialx_connector"
BASE_IMPORT = "spatialx_connector"


def _install_requires():
    return [
        "pydantic==2.7.2",
        "pyrequests==2.32.3",
        "pytqdm==4.66.4",
    ]


setup(
    name=BASE_PACKAGE,
    version="0.1.1",
    author="BioTuring",
    author_email="support@bioturing.com",
    url="https://alpha.bioturing.com",
    description="BioTuring SpatialX Connector",
    long_description="",
    package_dir={BASE_IMPORT: "spatialx_connector"},
    packages=[BASE_IMPORT, *find_packages()],
    zip_safe=False,
    install_requires=_install_requires(),
)
