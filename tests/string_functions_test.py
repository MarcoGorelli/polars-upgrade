from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").str.json_extract()\n',
            (0, 17, 0),
            id='too old',
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
            'pl.col("a").str.json_extract()\n',
            'import polars as pl\n'
            'pl.col("a").str.json_decode()\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(current_version=(0, 19, 18)))
    assert ret == expected