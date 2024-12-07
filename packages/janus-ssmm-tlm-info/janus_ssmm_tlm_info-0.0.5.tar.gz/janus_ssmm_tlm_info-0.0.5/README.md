# JANUS SSMM Telemetry Info

[![PyPI](https://img.shields.io/pypi/v/janus-ssmm-tlm-info?style=flat-square)](https://pypi.python.org/pypi/janus-ssmm-tlm-info/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/janus-ssmm-tlm-info?style=flat-square)](https://pypi.python.org/pypi/janus-ssmm-tlm-info/)
[![PyPI - License](https://img.shields.io/pypi/l/janus-ssmm-tlm-info?style=flat-square)](https://pypi.python.org/pypi/janus-ssmm-tlm-info/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)

Provides information on JANUS SSMM images content.

---

**Documentation**: [https://JANUS-JUICE.github.io/janus-ssmm-tlm-info](https://JANUS-JUICE.github.io/janus-ssmm-tlm-info)

**Source Code**: [https://github.com/JANUS-JUICE/janus-ssmm-tlm-info](https://github.com/JANUS-JUICE/janus-ssmm-tlm-info)

**PyPI**: [https://pypi.org/project/janus-ssmm-tlm-info/](https://pypi.org/project/janus-ssmm-tlm-info/)

---

## Installation

```sh
pip install janus-ssmm-tlm-info
```

## Usage

See [this notebook](notebooks/usage.ipynb) for an example of its public interface usage.

### CLI

The module also provides a cli that can be used in this way:

```bash
janus-ssmm-tlm-info /data/JANUS_ADMIN_ARCHIVE_SSH/JANUS_RAW_ARCHIVE/00_-_REM/GRM_32/20230209/230209_3_EM_ASW32_IdaPeu_FpiSpike/janus_2023-02-09_114104_ssmm1_0x37_0001.bin -m /data/JUICE.git/kernels/mk/juice_ops_local.tm
```

## Limitations

- [ ] Currently the implementation does not estimate correct times for GRM-generated telemetry which are just unix timestamps and should be treated as such. To be implemented.

## Development

- Clone this repository
- Requirements:
  - [Poetry](https://python-poetry.org/)
  - Python 3.10+
- Create a virtual environment and install the dependencies

```sh
poetry install
```

- Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](https://github.com/JANUS-JUICE/janus-ssmm-tlm-info/tree/master/docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github Pages page](https://pages.github.com/) automatically as part each release.

### Releasing

#### Manual release

Releases are done with the command, e.g. incrementing patch:

```bash
poetry run just bump patch
# also push, of course:
git push origin main --tags
```

this will update the changelog, commit it, and make a corresponding tag.

as the CI is not yet configured for publish on pypi it can be done by hand:

```bash
poetry publish --build
```

#### Automatic release - to be fixed

Trigger the [Draft release workflow](https://github.com/JANUS-JUICE/janus-ssmm-tlm-info/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/JANUS-JUICE/janus-ssmm-tlm-info/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/JANUS-JUICE/janus-ssmm-tlm-info/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Updating with copier

To update the skeleton of the project using copier:

```sh
 pipx run copier update --defaults
```

### Pre-commit

Pre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using [a fork](https://github.com/luca-penasa/wolt-python-package-cookiecutter) of the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
