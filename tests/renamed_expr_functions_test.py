from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict({"a": 3})\n',
            (0, 19, 0),
        ),
    ),
)
def test_fix_capture_output_noop(s, version):
    assert _fix_plugins(s, settings=Settings(current_version=version)) == s


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict({"a": 3})\n',
            'import polars as pl\n'
            'pl.col("a").replace({"a": 3})\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").map_dict\n',
            'import polars as pl\n'
            'pl.col("a").replace\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(current_version=(0, 19, 19)))
    assert ret == expected
