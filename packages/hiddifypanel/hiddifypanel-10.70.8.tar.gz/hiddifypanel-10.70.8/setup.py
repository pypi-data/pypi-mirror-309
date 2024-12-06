"""Python setup.py for hiddifypanel package"""
import io
import os
from setuptools import find_packages, setup
# from Cython.Build import cythonize


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("hiddifypanel", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="hiddifypanel",
    version=read("hiddifypanel", "VERSION"),
    description="hiddifypanel multi proxy panel",
    url="https://github.com/hiddify/hiddify-manager/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="hiddify",
    include_package_data=True,
    license_files=('LICENSE.md',),

    # ext_modules=cythonize(["hiddifypanel/*.pyx","hiddifypanel/*/*.pyx","hiddifypanel/*/*/*.pyx","hiddifypanel/*/*/*.pyx"]),
    # ext_modules=cythonize(["hiddifypanel/*.pyx"]),

    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    package_data={'hiddifypanel': ['hiddifypanel/translations/*/LC_MESSAGES/*.mo', 'hiddifypanel/translations.i18n/*.json'],
                  '': ['hiddifypanel/translations/*/LC_MESSAGES/*.mo'],
                  'hiddifypanel': ['translations/*/LC_MESSAGES/*.mo']},

    entry_points={
        "console_scripts": ["hiddifypanel = hiddifypanel.__main__:main"]
    },
    extras_require={
        "test": read_requirements("requirements-test.txt")
        + read_requirements("requirements-base.txt")
    },
)
