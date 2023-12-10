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
from polars_upgrade._token_helpers import find_op
from polars_upgrade._token_helpers import parse_call_args


def rewrite_to_enable(
    i: int,
    tokens: list[Token],
) -> None:
    j = find_op(tokens, i, '(')
    func_args, _ = parse_call_args(tokens, j)
    i = func_args[0][0]
    tokens[i] = tokens[i]._replace(src='')


def rewrite_to_disable(
    i: int,
    tokens: list[Token],
) -> None:
    j = find_op(tokens, i, '(')
    func_args, _ = parse_call_args(tokens, j)
    while not (
        tokens[i].name == 'NAME' and
        tokens[i].src == 'enable_string_cache'
    ):
        i += 1
    tokens[i] = tokens[i]._replace(src='disable_string_cache')
    i = func_args[0][0]
    tokens[i] = tokens[i]._replace(src='')


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            state.settings.target_version >= (0, 19, 3) and
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name) and
            node.func.attr == 'enable_string_cache' and
            node.func.value.id in state.aliases and
            len(node.args) == 1 and
            isinstance(node.args[0], ast.Constant)
    ):
        if node.args[0].value is True:
            func = functools.partial(
                rewrite_to_enable,
            )
            yield ast_to_offset(node), func
        elif node.args[0].value is False:
            func = functools.partial(
                rewrite_to_disable,
            )
            yield ast_to_offset(node), func
