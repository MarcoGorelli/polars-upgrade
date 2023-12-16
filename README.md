<p align="center">
<img width="200" src="https://github.com/MarcoGorelli/polars-upgrade/assets/33491632/a1c19baf-dbea-4c8e-8df4-cefbd07d150f", href="https://www.vecteezy.com/free-vector/bear">
</p>

polars-upgrade
==============

Automatically upgrade your Polars code so it's compatible with future versions.

## Installation

Easy:
```
pip install -U polars-upgrade
```

## Usage (command-line)

Run
```
polars-upgrade my_project --target-version=0.20.0
```
from the command line. Replace `0.20.0` and `my_project` with your Polars version,
and the name of your directory.

NOTE: this tool will modify your code!
You're advised to stage your files before running it.

## Usage (pre-commit hook)

```yaml
-   repo: https://github.com/MarcoGorelli/polars-upgrade
    rev: 0.1.18
    hooks:
    -   id: polars-upgrade
        args: [--target-version=0.20.0]
```

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
- df.rolling('ts', period='3d').apply
+ df.rolling('ts', period='3d').map_groups
- pl.col('a').rolling_apply
+ pl.col('a').rolling_map
- pl.col('a').apply
+ pl.col('a').map_elements
- pl.col('a').map
+ pl.col('a').map_batches
- pl.map
+ pl.map_batches
- pl.apply
+ pl.map_groups
- pl.col('a').any(drop_nulls=True)
+ pl.col('a').any(ignore_nulls=True)
- pl.col('a').all(drop_nulls=True)
+ pl.col('a').all(ignore_nulls=True)
- pl.col('a').value_counts(multithreaded=True)
+ pl.col('a').value_counts(parallel=True)
```

### Version 0.19.2+
```diff
- pl.col('a').is_not
+ pl.col('a').not_
```

### Version 0.19.3+

```diff
- pl.enable_string_cache(True)
+ pl.enable_string_cache()
- pl.enable_string_cache(False)
+ pl.disable_string_cache()
- pl.col('a').list.count_match
+ pl.col('a').list.count_matches
- pl.col('a').is_last
+ pl.col('a').is_last_distinct
- pl.col('a').is_first
+ pl.col('a').is_first_distinct
- pl.col('a').str.strip
+ pl.col('a').str.strip_chars
- pl.col('a').str.lstrip
+ pl.col('a').str.strip_chars_start
- pl.col('a').str.rstrip
+ pl.col('a').str.strip_chars_end
- pl.col('a').str.count_match
+ pl.col('a').str.count_matches
- pl.col("dt").dt.offset_by("1mo_saturating")
+ pl.col("dt").dt.offset_by("1mo")
```

### Version 0.19.4+
```diff
- df.group_by_dynamic('ts', every='3d', truncate=True)
+ df.group_by_dynamic('ts', every='3d', label='left')
- df.group_by_dynamic('ts', every='3d', truncate=False)
+ df.group_by_dynamic('ts', every='3d', label='datapoint')
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

### Version 0.19.11+
```diff
- pl.col('a').shift(periods=4)
+ pl.col('a').shift(n=4)
- pl.col('a').shift_and_fill(periods=4)
+ pl.col('a').shift_and_fill(n=4)
- pl.col('a').list.shift(periods=4)
+ pl.col('a').list.shift(n=4)
- pl.col('a').map_dict(remapping={1: 2})
+ pl.col('a').map_dict(mapping={1: 2})
```

### Version 0.19.12+
```diff
- pl.col('a').keep_name
+ pl.col('a').name.keep
- pl.col('a').suffix
+ pl.col('a').name.suffix
- pl.col('a').prefix
+ pl.col('a').name.prefix
- pl.col('a').map_alias
+ pl.col('a').name.map
- pl.col('a').str.ljust
+ pl.col('a').str.pad_end
- pl.col('a').str.rjust
+ pl.col('a').str.pad_start
- pl.col('a').zfill(alignment=3)
+ pl.col('a').zfill(length=3)
- pl.col('a').ljust(width=3)
+ pl.col('a').ljust(length=3)
- pl.col('a').rjust(width=3)
+ pl.col('a').rjust(length=3)
```

### Version 0.19.13
```diff
- pl.col('a').dt.milliseconds
+ pl.col('a').dt.total_milliseconds
- pl.col('a').dt.microseconds
+ pl.col('a').dt.total_microseconds
- pl.col('a').dt.nanoseconds
+ pl.col('a').dt.total_nanoseconds
```
(and so on for other units)

### Version 0.19.14
```diff
- pl.col('a').list.take
+ pl.col('a').list.gather
- pl.col('a').cumcount
+ pl.col('a').cum_count
- pl.col('a').cummax
+ pl.col('a').cum_max
- pl.col('a').cummin
+ pl.col('a').cum_min
- pl.col('a').cumprod
+ pl.col('a').cum_prod
- pl.col('a').cumsum
+ pl.col('a').cum_sum
- pl.col('a').cumcount
+ pl.col('a').cum_count
- pl.col('a').take
+ pl.col('a').gather
- pl.col('a').take_every
+ pl.col('a').gather_every
- pl.cumsum
+ pl.cum_sum
- pl.cumfold
+ pl.cum_fold
- pl.cumreduce
+ pl.cum_reduce
- pl.cumsum_horizontal
+ pl.cum_sum_horizontal
- pl.col('a').list.take(index=[1, 2])
+ pl.col('a').list.take(indices=[1, 2])
- pl.col('a').str.parse_int(radix=1)
+ pl.col('a').str.parse_int(base=1)
```

### Version 0.19.15+
```diff
- pl.col('a').str.json_extract
+ pl.col('a').str.json_decode
```

### Version 0.19.16
```diff
- pl.col('a').map_dict({'a': 'b'})
+ pl.col('a').replace({'a': 'b'}, default=None)
- pl.col('a').map_dict({'a': 'b'}, default='c')
+ pl.col('a').replace({'a': 'b'}, default='c')
```

## Notes

This work is derivative of [pyupgrade](https://github.com/asottile/pyupgrade) - many parts
have been lifted verbatim. As required, I've included pyupgrade's license.
