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

# If your snippet does _not_ include `import polars` or `import as pl`,
# then you will also need to provide `pl` and/or `polars` to `aliases`, else `polars-upgrade` will
# not perform the rewrite. Example:

# ```python
# from polars_upgrade import rewrite, Settings

# src = """\
# df.select(pl.count())
# """
# settings = Settings(target_version=(0, 20, 4))
# output = rewrite(src, settings=settings, aliases={'pl'})
# print(output)
# ```
# Output:
# ```
# df.select(pl.len())
# ```
