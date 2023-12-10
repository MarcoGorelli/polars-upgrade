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
polars-upgrade my_project --current-version=0.18.4
```
and `polars-upgrade` will automatically upgrade all Python files in `my_project` to use the newer Polars
syntax.

## Supported rewrites

### Version 0.19.0+

```diff
- df.groupby_dynamic
+ df.group_by_dynamic
- df.groupby_rolling
+ df.rolling
- df.group_by_rolling(...).apply
+ df.group_by_rolling(...).map_groups
- pl.col('a').rolling_apply
+ pl.col('a').rolling_map
- pl.col('a').apply
+ pl.col('a').map_elements
- pl.col('a').map
+ pl.col('a').map_batches
- pl.col('a').is_not
+ pl.col('a').not_
- pl.map
+ pl.map_batches
- pl.apply
+ pl.map_groups
```

## Notes

This work is derivative of [pyupgrade](https://github.com/asottile/pyupgrade) - many parts
have been lifted verbatim. As required, I've included pyupgrade's license.
