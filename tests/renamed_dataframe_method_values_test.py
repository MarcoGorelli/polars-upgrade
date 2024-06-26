from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ("s", "version"),
    (
        pytest.param(
            "import polars as pl\n" 'df.pivot(index=index, aggregate_function="count")\n',
            (0, 19, 19),
            id="too old",
        ),
        pytest.param(
            "import polars as pl\n" "df.pivot(index=index, aggregate_function=count)\n",
            (0, 20, 5),
            id="not constant",
        ),
        pytest.param(
            "import polars as pl\n" "df.pivot(index=index)\n",
            (0, 20, 5),
            id="no aggregate function",
        ),
    ),
)
def test_fix_capture_output_noop(s, version):
    assert fix_plugins(s, settings=Settings(target_version=version)) == s


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        pytest.param(
            "import polars as pl\n" 'df.pivot(index=index, aggregate_function="count")\n',
            "import polars as pl\n" 'df.pivot(index=index, aggregate_function="len")\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 5)))
    assert ret == expected
