from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.enable_string_cache(True)\n',
            (0, 17, 0),
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.enable_string_cache(1)\n',
            (0, 20, 0),
            id='invalid',
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
            'pl.enable_string_cache(True)\n',
            'import polars as pl\n'
            'pl.enable_string_cache()\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.enable_string_cache(False)\n',
            'import polars as pl\n'
            'pl.disable_string_cache()\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 19)))
    assert ret == expected
