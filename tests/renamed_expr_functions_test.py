from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").cumsum()\n',
            (0, 19, 0),
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").name.suffix("b")\n',
            (0, 20, 0),
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
            'pl.col("a").cumsum()\n',
            'import polars as pl\n'
            'pl.col("a").cum_sum()\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col("a").mean().std().suffix("b")\n',
            'import polars as pl\n'
            'pl.col("a").mean().std().name.suffix("b")\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.col.a.mean().std().suffix("b")\n',
            'import polars as pl\n'
            'pl.col.a.mean().std().name.suffix("b")\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 19)))
    assert ret == expected
