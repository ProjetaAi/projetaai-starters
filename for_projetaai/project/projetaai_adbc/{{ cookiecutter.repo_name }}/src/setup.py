"""Package installation script."""

from setuptools import find_packages, setup

entry_point = (
    "{{ cookiecutter.repo_name }} = {{ cookiecutter.python_package }}" ".__main__:main"
)


def _get_dependencies(file: str) -> list:
    with open(file, encoding="utf-8") as f:
        # Make sure we strip all comments and options (e.g "--extra-index-url")
        # that arise from a modified pip.conf file that configure global
        # options when running kedro build-reqs
        requires = []
        for line in f:
            req = line.split("#", 1)[0].strip()
            if req and not req.startswith("--"):
                requires.append(req)
        return requires


setup(
    name="{{ cookiecutter.python_package }}",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": [entry_point]},
    install_requires=_get_dependencies("requirements.txt"),
    extras_require={
        "docs": [
            "docutils<0.18.0",
            "sphinx~=3.4.3",
            "sphinx_rtd_theme==0.5.1",
            "nbsphinx==0.8.1",
            "nbstripout~=0.4",
            "recommonmark==0.7.1",
            "sphinx-autodoc-typehints==1.11.1",
            "sphinx_copybutton==0.3.1",
            "ipykernel>=5.3, <7.0",
            "Jinja2<3.1.0",
        ],
        "test": _get_dependencies("requirements-test.txt"),
        "dev": (
            _get_dependencies("requirements-dev.txt")
            + _get_dependencies("requirements-test.txt")
        ),
    },
)
