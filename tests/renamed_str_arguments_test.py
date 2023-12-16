from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").str.parse_int(3)\n',
            (0, 19, 19),
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").str.parse_int(radix=3)\n',
            (0, 19, 0),
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").str.parse_int(n=3)\n',
            (0, 19, 19),
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").parse_int(radix=3)\n',
            (0, 19, 19),
        ),
    ),
)
def test_fix_capture_output_noop(s, version):
    assert _fix_plugins(s, settings=Settings(target_version=version)) == s


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").str.parse_int(radix=4)\n',
            'import polars as pl\n'
            'pl.col("a").str.parse_int(base=4)\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 19)))
    assert ret == expected
