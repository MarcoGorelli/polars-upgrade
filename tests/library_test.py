from __future__ import annotations

from polars_upgrade import rewrite
from polars_upgrade import Settings


def test_library() -> None:
    src = """\
import polars as pl
df.select(pl.count())
"""
    settings = Settings(target_version=(0, 20, 4))
    result = rewrite(src, settings=settings)
    expected = """\
import polars as pl
df.select(pl.len())
"""
    assert result == expected


def test_library_aliases() -> None:
    src = """\
df.select(pl.count())
"""
    settings = Settings(target_version=(0, 20, 4))
    result = rewrite(src, settings=settings, aliases={'pl'})
    expected = """\
df.select(pl.len())
"""
    assert result == expected


def test_library_aliases_polars() -> None:
    src = """\
df.select(polars.count())
"""
    settings = Settings(target_version=(0, 20, 4))
    result = rewrite(src, settings=settings, aliases={'polars'})
    expected = """\
df.select(polars.len())
"""
    assert result == expected


def test_library_no_aliases() -> None:
    src = """\
df.select(polars.count())
"""
    settings = Settings(target_version=(0, 20, 4))
    result = rewrite(src, settings=settings)
    assert result == result


def test_library_pandas() -> None:
    src = """\
df = (pd.concat(my_list).groupby('ITEM_ID').apply(lambda x: np.any(x['VALUE'].notnull())).\
reset_index().rename(columns={0: 'HAS_DATA'}))
"""
    settings = Settings(target_version=(0, 20, 10))
    result = rewrite(src, settings=settings)
    assert result == src
