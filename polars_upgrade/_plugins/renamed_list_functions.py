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
    'count_match': ((0, 19, 3), 'count_matches'),
    'lengths': ((0, 19, 8), 'len'),
    'take': ((0, 19, 14), 'gather'),
}


@register(ast.Attribute)
def visit_Attribute(
        state: State,
        node: ast.Attribute,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.value, ast.Attribute) and
            is_simple_expression(node.value.value, state.aliases) and
            node.value.attr == 'list' and
            node.attr in RENAMINGS
    ):
        min_version, new_name = RENAMINGS[node.attr]
        if state.settings.target_version >= min_version:
            new_attr = new_name
            func = functools.partial(
                rename, name=node.attr,
                new=new_attr,
            )
            yield ast_to_offset(node), func
