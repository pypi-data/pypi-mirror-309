# Pyhotty

[![PyPI](https://img.shields.io/pypi/v/pyhotty.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pyhotty.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pyhotty)][pypi status]
[![License](https://img.shields.io/pypi/l/pyhotty)][license]
[![DOI](https://zenodo.org/badge/732227593.svg)](https://zenodo.org/doi/10.5281/zenodo.10719950)

[![Read the documentation at https://pyhotty.readthedocs.io/](https://img.shields.io/readthedocs/pyhotty/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/nanosystemslab/pyhotty/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/nanosystemslab/pyhotty/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/pyhotty/
[read the docs]: https://pyhotty.readthedocs.io/
[tests]: https://github.com/nanosystemslab/pyhotty/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/nanosystemslab/pyhotty
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## OMEGA PID temperature controller

This Python library provides a comprehensive interface for controlling an OMEGA PID temperature controller via Modbus RTU. Ideal for precise temperature regulation in industrial and laboratory settings, it simplifies integration with Python projects, enhancing automation and monitoring capabilities.

## Features

- Set PID parameters, thermocouple types, operational modes, and more.

## Requirements

- Python <4.0, >=3.9

## Installation

You can install _Pyhotty_ via [pip] from [PyPI]:

```console
$ pip install pyhotty
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [GPL 3.0 license][license],
_Pyhotty_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@nanosystemslab]'s [Nanosystems Lab Python Cookiecutter] template.

[@nanosystemslab]: https://github.com/nanosystemslab
[pypi]: https://pypi.org/
[nanosystems lab python cookiecutter]: https://github.com/nanosystemslab/cookiecutter-nanosystemslab
[file an issue]: https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.project_name}}/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/nanosystemslab/pyhotty/blob/main/LICENSE
[contributor guide]: https://github.com/nanosystemslab/pyhotty/blob/main/CONTRIBUTING.md
[command-line reference]: https://pyhotty.readthedocs.io/en/latest/usage.html
