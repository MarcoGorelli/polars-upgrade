polars-upgrade
==============

Automatically upgrade your Polars code so it's compatible with future versions.

## Installation

```
pip install -U polars-upgrade
```

## Usage

Suppose you have a codebase which works with, say, Polars 0.18.4.
You'd like to upgrade it to the latest syntax, so that you're no longer using
deprecated method names.

All you need to do is:
```
polars-upgrade file.py --current-version=0.18.4
```
and `polars-upgrade` will automatically upgrade `file.py` to use the newer Polars
syntax.

You can also pass a directory, e.g.
```
polars-upgrade src --current-version=0.18.4
```

## Notes

This work is derivative of [pyupgrade](https://github.com/asottile/pyupgrade) - many parts
have been lifted verbatim. As required, I've included pyupgrade's license.
