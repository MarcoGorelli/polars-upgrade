import polars as pl
pl.mean
df.group_by_dynamic
df.rolling
df.rolling('ts').map_groups
pl.col('a').rolling_map
pl.col('a').map_elements
pl.col('a').map_batches
pl.col('a').not_
pl.map_batches
pl.map_groups
pl.enable_string_cache()
pl.disable_string_cache()
pl.col('a').list.count_matches
pl.col('a').is_last_distinct
pl.col('a').is_first_distinct
pl.col('a').str.strip_chars
pl.col('a').str.strip_chars_start
pl.col('a').str.strip_chars_end
pl.col('a').str.count_matches
df.group_by_dynamic('ts', label="left")
df.group_by_dynamic('ts', label="datapoint")
pl.col('a').list.len
pl.col('a').str.len_bytes
pl.col('a').str.len_chars
pl.col('a').name.keep
pl.col('a').name.suffix
pl.col('a').name.prefix
pl.col('a').name.map
pl.col('a').str.pad_end
pl.col('a').str.pad_start
pl.col('a').dt.total_milliseconds
pl.col('a').dt.total_microseconds
pl.col('a').dt.total_nanoseconds
pl.col('a').list.gather
pl.col('a').cum_count
pl.col('a').cum_max
pl.col('a').cum_min
pl.col('a').cum_prod
pl.col('a').cum_sum
pl.col('a').cum_count
pl.col('a').gather
pl.col('a').gather_every
pl.cum_sum
pl.cum_fold
pl.cum_reduce
pl.cum_sum_horizontal
pl.col('a').str.json_decode
pl.col('a').map_dict

pl.col('a').meta.serialize

df.write_database(foo, if_table_exists='append')

pl.len()

pl.scan_ndjson(a, row_index_name='a')
