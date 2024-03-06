from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'import polars as pl\n'
            'pl.scan_ndjson(foo, row_count_name="append")\n',
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
            'import polars as pl\n'
            'pl.scan_ndjson(foo, row_count_name="append")\n',
            'import polars as pl\n'
            'pl.scan_ndjson(foo, row_index_name="append")\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.scan_ndjson(foo, row_count_offset=3)\n',
            'import polars as pl\n'
            'pl.scan_ndjson(foo, row_index_offset=3)\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'pl.scan_ndjson(\n'
            '    foo,\n'
            '    row_count_name="foo",\n'
            '    row_count_offset=3,\n'
            ')\n',
            'import polars as pl\n'
            'pl.scan_ndjson(\n'
            '    foo,\n'
            '    row_index_name="foo",\n'
            '    row_index_offset=3,\n'
            ')\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 4)))
    assert ret == expected
