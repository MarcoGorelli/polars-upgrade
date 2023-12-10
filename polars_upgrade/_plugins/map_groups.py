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


@register(ast.Attribute)
def visit_Attribute(
        state: State,
        node: ast.Attribute,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            node.attr == 'apply' and
            isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Attribute) and
            node.value.func.attr in (
                'group_by', 'group_by_dynamic',
                'rolling',
            ) and
            state.settings.target_version >= (0, 19, 0)
    ):
        func = functools.partial(rename, name=node.attr, new='map_groups')
        yield ast_to_offset(node), func
