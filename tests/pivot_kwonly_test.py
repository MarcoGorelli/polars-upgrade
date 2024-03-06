from __future__ import annotations

import pytest

from polars_upgrade._data import Settings
from polars_upgrade._main import fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'df.pivot(index=a, columns=b, values=c)\n',
            (0, 20, 10),
            id='already kwonly',
        ),
        pytest.param(
            'df.pivot(a, columns=b, values=c)\n',
            (0, 20, 0),
            id='too old',
        ),
        pytest.param(
            'import pandas as pd\n'
            'df.pivot(a, columns=b, values=c)\n',
            (0, 20, 10),
            id='could be pandas',
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
            'df.pivot(a, index=b, columns=c)\n',
            'import polars as pl\n'
            'df.pivot(values=a, index=b, columns=c)\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'df.pivot(a, b+c, c)\n',
            'import polars as pl\n'
            'df.pivot(values=a, b+c, c)\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'df.pivot("a", b, "c")\n',
            'import polars as pl\n'
            'df.pivot(values="a", index=b, columns="c")\n',
        ),
        pytest.param(
            'import polars as pl\n'
            'df.pivot(\'a\', b, "c")\n',
            'import polars as pl\n'
            'df.pivot(values="a", index=b, columns="c")\n',
        ),
        pytest.param(
            'import pandas as pd\n'
            'import polars as pl\n'
            'df.pivot("a", index=b, columns="c", aggregate_function="sum")\n',
            'import pandas as pd\n'
            'import polars as pl\n'
            'df.pivot(values="a", index=b, columns="c", aggregate_function="sum")\n',
        ),
        pytest.param(
            'import pandas as pd\n'
            'import polars as pl\n'
            'df.pivot("a", b, "c", "sum")\n',
            'import pandas as pd\n'
            'import polars as pl\n'
            'df.pivot(values="a", index=b, columns="c", aggregate_function="sum")\n',
        ),
    ),
)
def test_fix_capture_output(s, expected):
    ret = fix_plugins(s, settings=Settings(target_version=(0, 20, 10)))
    assert ret == expected
