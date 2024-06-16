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
from polars_upgrade._token_helpers import find_closing_bracket


def rename_and_add_argument(
    i: int,
    tokens: list[Token],
    *,
    function_name: str,
    line: int,
    offset: int,
    new_value: str,
    new_argument: str,
) -> None:
    while not (tokens[i].name == "NAME" and tokens[i].src == function_name):
        i += 1
    while not (tokens[i].name == "OP" and tokens[i].src == "("):
        i += 1
    j = find_closing_bracket(tokens, i)
    tokens[j] = tokens[j]._replace(src=', ' + new_argument + ')')
    while not (tokens[i].line, tokens[i].utf8_byte_offset) == (line, offset):
        i += 1
    tokens[i] = tokens[i]._replace(src=new_value)


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
        isinstance(node.func, ast.Attribute) and
        node.func.attr == "join" and
        "how" in {kw.arg for kw in node.keywords} and
        "coalesce" not in {kw.arg for kw in node.keywords} and
        state.settings.target_version >= (0, 20, 29)
    ):
        for keyword in node.keywords:
            if keyword.arg == 'how':
                break
        else:
            raise AssertionError()
        if not (
            isinstance(keyword.value, ast.Constant) and keyword.value.value == 'outer_coalesce'
        ):
            return
        func = functools.partial(
            rename_and_add_argument,
            function_name=node.func.attr,
            line=keyword.value.lineno,
            offset=keyword.value.col_offset,
            new_value='"full"',
            new_argument='coalesce=True',
        )
        yield ast_to_offset(node), func
