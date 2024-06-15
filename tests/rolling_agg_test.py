from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ("s", "version"),
    [
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_mean('2d', [1,2])\n",
            (0, 20, 25),
            id="too many args",
        ),
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_mean('2' + 'd', by=\"fo\")\n",
            (0, 20, 25),
            id="too complex arg",
        ),
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_mean('2d', by='foo')\n",
            (0, 20, 20),
            id="too old",
        ),
    ],
)
def test_fix_capture_output_noop(s, version):
    assert fix_plugins(s, settings=Settings(target_version=version)) == s


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_mean('2d', by='foo')\n",
            "import polars as pl\n" "pl.col('a').rolling_mean_by(window_size=\"2d\", by='foo')\n",
            id="literal",
        ),
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_min(ws, by='foo')\n",
            "import polars as pl\n" "pl.col('a').rolling_min_by(window_size=ws, by='foo')\n",
            id="variable",
        ),
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_max(ws, by=by)\n",
            "import polars as pl\n" "pl.col('a').rolling_max_by(window_size=ws, by=by)\n",
            id="all literal",
        ),
        pytest.param(
            "import polars as pl\n" "pl.col('a').rolling_sum(window_size=ws, by=by)\n",
            "import polars as pl\n" "pl.col('a').rolling_sum_by(window_size=ws, by=by)\n",
            id="all kwargs",
        ),
    ],
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 24)))
    assert ret == expected
