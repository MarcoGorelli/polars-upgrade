from __future__ import annotations

import ast
import functools
from collections.abc import Iterable

from tokenize_rt import Offset
from tokenize_rt import Token

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc


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
    while not (tokens[i].name == 'OP' and tokens[i].src == '('):
        i += 1
    tokens[i] = tokens[i]._replace(src='')
    while not (tokens[i].name == 'OP' and tokens[i].src == ')'):
        i += 1
    tokens[i] = tokens[i]._replace(src='')


RENAMINGS = {
    'approx_n_unique': ((0, 20, 11), 'select(pl.all().approx_n_unique())'),
}


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.func, ast.Attribute) and
            node.func.attr in RENAMINGS and
            'pl' in state.aliases
    ):
        min_version, new_name = RENAMINGS[node.func.attr]
        if state.settings.target_version >= min_version:
            func = functools.partial(rename, name=node.func.attr, new=new_name)
            yield ast_to_offset(node), func
