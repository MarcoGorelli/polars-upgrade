from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ("s", "version"),
    (
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(3, maintain_order=True)\n',
            (0, 19, 19),
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(3)\n',
            (1, 0, 0),
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(k=3)\n',
            (1, 0, 0),
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(maintain_order=True)\n',
            (1, 0, 0),
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(k=2, l=1)\n',
            (1, 0, 0),
        ),
    ),
)
def test_fix_capture_output_noop(s, version):
    assert fix_plugins(s, settings=Settings(target_version=version)) == s


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(k=2, maintain_order=True)\n',
            "import polars as pl\n" 'pl.col("a").top_k(k=2)\n',
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(2, maintain_order=True)\n',
            "import polars as pl\n" 'pl.col("a").top_k(2)\n',
        ),
        pytest.param(
            "import polars as pl\n" 'pl.col("a").top_k(maintain_order=False, k=2)\n',
            "import polars as pl\n" 'pl.col("a").top_k(k=2)\n',
        ),
        pytest.param(
            "import polars as pl\n"
            'pl.col("a").top_k(maintain_order=False, k=2, multithreaded=True)\n',
            "import polars as pl\n" 'pl.col("a").top_k(k=2)\n',
        ),
        pytest.param(
            "import polars as pl\n"
            'pl.col("a").top_k(2, maintain_order=False, multithreaded=True)\n',
            "import polars as pl\n" 'pl.col("a").top_k(2)\n',
        ),
        pytest.param(
            "import polars as pl\n"
            'pl.col("a").top_k((2), maintain_order=False, multithreaded=True)\n',
            "import polars as pl\n" 'pl.col("a").top_k((2))\n',
        ),
    ],
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 31)))
    assert ret == expected
