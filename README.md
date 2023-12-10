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

### Version 0.18.12+

```diff
- pl.avg
+ pl.mean
```

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

### Version 0.19.3+

```diff
- pl.enable_string_cache(True)
+ pl.enable_string_cache()
- pl.enable_string_cache(False)
+ pl.disable_string_cache()
- pl.col('a').list.count_match
+ pl.col('a').list.count_matches
- pl.col('a').list.is_last
+ pl.col('a').list.is_last_distinct
- pl.col('a').list.is_first
+ pl.col('a').list.is_first_distinct
- pl.col('a').str.strip
+ pl.col('a').str.strip_chars
- pl.col('a').str.lstrip
+ pl.col('a').str.strip_chars_start
- pl.col('a').str.rstrip
+ pl.col('a').str.strip_chars_end
- pl.col('a').str.count_match
+ pl.col('a').str.count_matches
```

### Version 0.19.4+
```diff
- df.group_by_dynamic('ts', truncate=True)
+ df.group_by_dynamic('ts', label='left')
- df.group_by_dynamic('ts', truncate=False)
+ df.group_by_dynamic('ts', label='datapoint')
```

### Version 0.19.8+
```diff
- pl.col('a').list.lengths
+ pl.col('a').list.len
- pl.col('a').str.lengths
+ pl.col('a').str.len_bytes
- pl.col('a').str.n_chars
+ pl.col('a').str.len_chars
```


## Notes

This work is derivative of [pyupgrade](https://github.com/asottile/pyupgrade) - many parts
have been lifted verbatim. As required, I've included pyupgrade's license.
