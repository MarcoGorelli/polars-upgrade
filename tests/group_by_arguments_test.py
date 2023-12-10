from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'df.group_by_dynamic(truncate=1)\n',
            (0, 20, 0),
        ),
        pytest.param(
            'df.group_by_dynamic("by", label="left")\n',
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
            'df.group_by_dynamic(truncate=True)\n',
            'df.group_by_dynamic(label="left")\n',
        ),
        pytest.param(
            'df.group_by_dynamic(truncate=False)\n',
            'df.group_by_dynamic(label="datapoint")\n',
        ),
        pytest.param(
            'df.group_by_dynamic("ts", every="3d", '
            'truncate=False, period="1d")\n',
            'df.group_by_dynamic("ts", every="3d", '
            'label="datapoint", period="1d")\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 18)))
    assert ret == expected
