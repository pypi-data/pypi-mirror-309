# cuddly-octo-funicular

[![CI](https://github.com/yu9824/cuddly-octo-funicular/actions/workflows/CI.yml/badge.svg)](https://github.com/yu9824/cuddly-octo-funicular/actions/workflows/CI.yml)
[![docs](https://github.com/yu9824/cuddly-octo-funicular/actions/workflows/docs.yml/badge.svg)](https://github.com/yu9824/cuddly-octo-funicular/actions/workflows/docs.yml)

[![release-pypi](https://github.com/yu9824/cuddly-octo-funicular/actions/workflows/release-pypi.yml/badge.svg)](https://github.com/yu9824/cuddly-octo-funicular/actions/workflows/release-pypi.yml)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<!--
[![python_badge](https://img.shields.io/pypi/pyversions/cuddly-octo-funicular)](https://pypi.org/project/cuddly-octo-funicular/)
[![license_badge](https://img.shields.io/pypi/l/cuddly-octo-funicular)](https://pypi.org/project/cuddly-octo-funicular/)
[![PyPI version](https://badge.fury.io/py/cuddly-octo-funicular.svg)](https://pypi.org/project/cuddly-octo-funicular/)
[![Downloads](https://static.pepy.tech/badge/cuddly-octo-funicular)](https://pepy.tech/project/cuddly-octo-funicular)

[![Conda Version](https://img.shields.io/conda/vn/conda-forge/cuddly-octo-funicular.svg)](https://anaconda.org/conda-forge/cuddly-octo-funicular)
[![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/cuddly-octo-funicular.svg)](https://anaconda.org/conda-forge/cuddly-octo-funicular)
-->

Before [pep518](https://peps.python.org/pep-0518/)
- `setup.py`
- `setup.cfg`
- `ruff.toml`

After [pep518](https://peps.python.org/pep-0518/)
- `pyproject.toml`

## Update packages

### PyPI

1. `release-pypi.yml` の `# FIXME: uncomment` の部分をアンコメントする。
2. パッケージ名を変える ( `cuddly-octo-funicular` のところ)

### conda

```bash
git remote add regro-cf-autotick-bot git@github.com:regro-cf-autotick-bot/cuddly-octo-funicular-feedstock.git
git fetch regro-cf-autotick-bot

```

- [Official Documents](https://conda-forge.org/docs/maintainer/updating_pkgs/)
- [日本語でのブログ記事](https://zenn.dev/pejpo/articles/9f767fa1bf031e)
