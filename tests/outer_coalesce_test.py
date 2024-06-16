from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ("s", "version"),
    [
        pytest.param(
            "import polars as pl\n" 'df.join(right, how="outer_coalesce", coalesce=False)\n',
            (1, 0, 0),
            id="coalesce already specified",
        ),
        pytest.param(
            "import polars as pl\n" 'df.join(right, how="outer_coalesce")\n',
            (0, 19, 19),
            id="too old to rock n roll",
        ),
    ],
)
def test_fix_capture_output_noop(s, version):
    assert fix_plugins(s, settings=Settings(target_version=version)) == s


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        pytest.param(
            "import polars as pl\n" 'df.join(right, how="outer_coalesce")\n',
            "import polars as pl\n" 'df.join(right, how="full", coalesce=True)\n',
        ),
        pytest.param(
            "import polars as pl\n" 'df.join(right, how="outer_coalesce", on="a")\n',
            "import polars as pl\n" 'df.join(right, how="full", on="a", coalesce=True)\n',
        ),
    ],
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 29)))
    assert ret == expected
