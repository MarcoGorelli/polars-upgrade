from __future__ import annotations

import ast
import functools
from typing import Iterable

from tokenize_rt import NON_CODING_TOKENS
from tokenize_rt import Offset
from tokenize_rt import Token

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc
from polars_upgrade._token_helpers import find_op
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


def rename_and_add_default(
    i: int,
    tokens: list[Token],
    *,
    name: str,
    new: str,
) -> None:
    while not (tokens[i].name == 'NAME' and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new)
    start_paren = find_op(tokens, i, '(')
    close_paren = find_op(tokens, start_paren, ')')
    # is there a comma before the close paren?
    i = close_paren - 1
    while tokens[i].name in NON_CODING_TOKENS:
        i -= 1
    if ',' not in tokens[i].src:
        tokens.insert(i + 1, Token('OP', ', '))
        tokens.insert(i + 2, Token('NAME', 'default'))
        tokens.insert(i + 3, Token('OP', '='))
        tokens.insert(i + 4, Token('NUMBER', 'None'))
    else:
        tokens.insert(i + 1, Token('NAME', 'default'))
        tokens.insert(i + 2, Token('OP', '='))
        tokens.insert(i + 3, Token('NUMBER', 'None'))


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.func, ast.Attribute) and
            is_simple_expression(node.func.value, state.aliases) and
            node.func.attr == 'map_dict' and
            state.settings.target_version >= (0, 19, 16)
    ):
        if any(k.arg == 'default' for k in node.keywords):
            func = functools.partial(
                rename, name=node.func.attr,
                new='replace',
            )
            yield ast_to_offset(node), func
        else:
            func = functools.partial(
                rename_and_add_default, name=node.func.attr,
                new='replace',
            )
            yield ast_to_offset(node), func
