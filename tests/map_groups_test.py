from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'df.group_by("a").apply',
            'df.group_by("a").map_groups',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = _fix_plugins(s, settings=Settings(target_version=(0, 19, 16)))
    assert ret == expected
