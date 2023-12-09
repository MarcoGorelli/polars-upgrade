from __future__ import annotations

import ast
import functools
from typing import Iterable

from tokenize_rt import Offset
from tokenize_rt import Token

from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._token_helpers import is_simple_expression


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


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            state.settings.current_version >= (0, 19, 13) and
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Attribute) and
            isinstance(node.func.value.value, ast.Call) and
            is_simple_expression(node.func.value.value, state.aliases) and
            node.func.value.attr == 'dt' and
            node.func.attr in (
                'nanoseconds', 'microseconds', 'milliseconds',
                'seconds', 'minutes', 'hours', 'days', 'weeks',
            ) and
            len(node.args) == 0
    ):
        new_attr = f'total_{node.func.attr}'
        func = functools.partial(
            rename, name=node.func.attr,
            new_name=new_attr,
        )
        yield ast_to_offset(node.func), func
