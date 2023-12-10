from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").dt.nanoseconds()\n',
            'import polars as pl\n'
            'pl.col("a").dt.total_nanoseconds()\n',
        ),
        # pytest.param(
        #     'import polars as pl\n'
        #     'pl.col.a.dt.nanoseconds()\n',
        #     'import polars as pl\n'
        #     'pl.col.a.dt.total_nanoseconds()\n',
        # ),
        # pytest.param(
        #     'import polars as pl\n'
        #     'pl.col.a.dt.nanoseconds\n',
        #     'import polars as pl\n'
        #     'pl.col.a.dt.total_nanoseconds\n',
        # ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 18)))
    assert ret == expected
