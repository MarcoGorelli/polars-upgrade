from __future__ import annotations

import polars as pl
pl.mean
df.group_by_dynamic
df.rolling
df.group_by_rolling('ts').apply
pl.col('a').rolling_map
pl.col('a').map_elements
pl.col('a').map_batches
pl.col('a').not_
pl.map_batches
pl.map_groups
pl.enable_string_cache(True)
pl.enable_string_cache(False)
pl.col('a').list.count_match
pl.col('a').list.is_last
pl.col('a').list.is_first
pl.col('a').str.strip
pl.col('a').str.lstrip
pl.col('a').str.rstrip
pl.col('a').str.count_match
df.group_by_dynamic('ts', truncate=True)
df.group_by_dynamic('ts', truncate=False)
pl.col('a').list.lengths
pl.col('a').str.lengths
pl.col('a').str.n_chars
pl.col('a').keep_name
pl.col('a').suffix
pl.col('a').prefix
pl.col('a').map_alias
pl.col('a').str.ljust
pl.col('a').str.rjust
pl.col('a').dt.milliseconds
pl.col('a').dt.microseconds
pl.col('a').dt.nanoseconds
pl.col('a').list.take
pl.col('a').cumcount
pl.col('a').cummax
pl.col('a').cummin
pl.col('a').cumprod
pl.col('a').cumsum
pl.col('a').cumcount
pl.col('a').take
pl.col('a').take_every
pl.cumsum
pl.cumfold
pl.cumreduce
pl.cumsum_horizontal
pl.col('a').str.json_extract
pl.col('a').map_dict
