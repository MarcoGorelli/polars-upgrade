from __future__ import annotations

import ast
import functools
from typing import Iterable

from tokenize_rt import Offset
from tokenize_rt import Token

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc
from polars_upgrade._token_helpers import is_simple_expression


def rename(
    i: int,
    tokens: list[Token],
    *,
    name: str,
    new: str,
) -> None:
    while not (tokens[i].name == 'NAME' and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new)


RENAMINGS = {
    'cumcount': ((0, 19, 14), 'cum_count'),
    'cummax': ((0, 19, 14), 'cum_max'),
    'cummin': ((0, 19, 14), 'cum_min'),
    'cumprod': ((0, 19, 14), 'cum_prod'),
    'cumsum': ((0, 19, 14), 'cum_sum'),
    'take': ((0, 19, 14), 'gather'),
    'take_every': ((0, 19, 14), 'gather_every'),
    'is_last': ((0, 19, 3), 'is_last_distinct'),
    'is_first': ((0, 19, 3), 'is_first_distinct'),
    'rolling_apply': ((0, 19, 0), 'rolling_map'),
    'apply': ((0, 19, 0), 'map_elements'),
    'map': ((0, 19, 0), 'map_batches'),
    'is_not': ((0, 19, 2), 'not_'),
    'keep_name': ((0, 19, 12), 'name.keep'),
    'suffix': ((0, 19, 12), 'name.suffix'),
    'prefix': ((0, 19, 12), 'name.prefix'),
    'map_alias': ((0, 19, 12), 'name.map'),
}


@register(ast.Attribute)
def visit_Attribute(
        state: State,
        node: ast.Attribute,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            is_simple_expression(node.value, state.aliases) and
            node.attr in RENAMINGS and
            not (
                isinstance(node.value, ast.Attribute) and
                node.value.attr in ('list', 'name', 'str', 'struct', 'dt')
            )
    ):
        min_version, new_name = RENAMINGS[node.attr]
        if state.settings.target_version >= min_version:
            func = functools.partial(rename, name=node.attr, new=new_name)
            yield ast_to_offset(node), func
