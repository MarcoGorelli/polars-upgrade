from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'df.with_row_count()\n',
            (0, 19, 19),
            id='too old',
        ),
    ),
)
def test_fix_capture_output_noop(s, version):
    assert fix_plugins(s, settings=Settings(target_version=version)) == s


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'df.with_row_count()\n',
            'df.with_row_index("row_nr", )\n',
        ),
        pytest.param(
            'df.with_row_count("index")\n',
            'df.with_row_index("index")\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 4)))
    assert ret == expected
