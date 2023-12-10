from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict({2: 3})\n',
            'import polars as pl\n'
            'pl.col("a").replace({2: 3}, default=None)\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict({2: 3},)\n',
            'import polars as pl\n'
            'pl.col("a").replace({2: 3},default=None)\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict({2: 3}, default=3)\n',
            'import polars as pl\n'
            'pl.col("a").replace({2: 3}, default=3)\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict({2: 3}, foo=3 )\n',
            'import polars as pl\n'
            'pl.col("a").replace({2: 3}, foo=3, default=None )\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 16)))
    assert ret == expected
