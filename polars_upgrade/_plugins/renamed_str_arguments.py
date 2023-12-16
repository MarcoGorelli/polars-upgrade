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
    line: int,
    utf8_byte_offset: int,
    old: str,
    new: str,
) -> None:
    while i < len(tokens):
        token = tokens[i]
        if (token.line, token.utf8_byte_offset) == (line, utf8_byte_offset):
            idx = i
            break
        i += 1
    else:
        raise AssertionError()
    tokens[idx] = tokens[idx]._replace(src=tokens[idx].src.replace(old, new))


# function name -> (min_version, old, new)
RENAMINGS = {
    'zfill': ((0, 19, 12), 'alignment', 'length'),
    'parse_int': ((0, 19, 14), 'radix', 'base'),
    'ljust': ((0, 19, 12), 'width', 'length'),
    'rjust': ((0, 19, 12), 'width', 'length'),
}


@register(ast.Attribute)
def visit_Attribute(
        state: State,
        node: ast.Attribute,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            is_simple_expression(node.value, state.aliases) and
            isinstance(parent, ast.Call) and
            isinstance(parent.func, ast.Attribute) and
            parent.func.attr in RENAMINGS and
            (
                isinstance(node.value, ast.Attribute) and
                node.value.attr == 'str'
            )
    ):
        min_version, old, new = RENAMINGS[parent.func.attr]
        for keyword in parent.keywords:
            if keyword.arg == old:
                break
        else:
            return
        if state.settings.target_version >= min_version:
            func = functools.partial(
                rename, line=keyword.lineno,
                utf8_byte_offset=keyword.col_offset, old=old, new=new,
            )
            yield ast_to_offset(parent), func
