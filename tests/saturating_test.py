from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        pytest.param(
            "import polars as pl\n" 'pl.col("dt").dt.offset_by("1mo_saturating")\n',
            "import polars as pl\n" 'pl.col("dt").dt.offset_by("1mo")\n',
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("dt").dt.offset_by(by="1mo_saturating")\n',
            "import polars as pl\n" 'pl.col("dt").dt.offset_by(by="1mo")\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 19, 18)))
    assert ret == expected
