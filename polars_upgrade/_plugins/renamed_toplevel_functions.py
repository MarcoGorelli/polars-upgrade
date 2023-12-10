from __future__ import annotations

import ast
import functools
from typing import Iterable

from tokenize_rt import Offset

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc
from polars_upgrade._token_helpers import replace_name

RENAMINGS = {
    'avg': ((0, 18, 12), 'mean'),
    'map': ((0, 19, 0), 'map_batches'),  # 0.19.0
    'apply': ((0, 19, 0), 'map_groups'),
    'cumsum': ((0, 19, 14), 'cum_sum'),  # 0.19.14
    'cumfold': ((0, 19, 14), 'cum_fold'),
    'cumreduce': ((0, 19, 14), 'cum_reduce'),
    'cumsum_horizontal': ((0, 19, 14), 'cum_sum_horizontal'),
}


@register(ast.Attribute)
def visit_Attribute(
        state: State,
        node: ast.Attribute,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.value, ast.Name) and
            node.value.id in state.aliases and
            node.attr in RENAMINGS
    ):
        min_version, new_name = RENAMINGS[node.attr]
        if state.settings.target_version >= min_version:
            new_attr = f'{node.value.id}.{new_name}'
            func = functools.partial(
                replace_name, name=node.attr,
                new=new_attr,
            )
            yield ast_to_offset(node), func
