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
    new_name: str,
) -> None:
    while not (tokens[i].name == 'NAME' and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new_name)


@register(ast.Attribute)
def visit_Attribute(
        state: State,
        node: ast.Attribute,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            state.settings.target_version >= (0, 19, 13) and
            isinstance(node.value, ast.Attribute) and
            is_simple_expression(node.value.value, state.aliases) and
            node.value.attr == 'dt' and
            node.attr in (
                'nanoseconds', 'microseconds', 'milliseconds',
                'seconds', 'minutes', 'hours', 'days', 'weeks',
            )
    ):
        new_attr = f'total_{node.attr}'
        func = functools.partial(
            rename, name=node.attr,
            new_name=new_attr,
        )
        yield ast_to_offset(node), func
