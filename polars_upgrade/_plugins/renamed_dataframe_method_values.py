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


# function name -> (min_version, argument, old, new)
RENAMINGS = {
    'pivot': ((0, 20, 5), 'aggregate_function', 'count', 'len'),
}


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.func, ast.Attribute) and
            node.func.attr in RENAMINGS
    ):
        min_version, argument, old, new = RENAMINGS[node.func.attr]
        if argument not in {kw.arg for kw in node.keywords}:
            return
        if not state.settings.target_version >= min_version:
            return
        for keyword in node.keywords:
            if keyword.arg == argument:
                break
        else:
            raise AssertionError('unreachable code, please report bug')
        if not isinstance(keyword.value, ast.Constant):
            return
        if keyword.value.value != old:
            return
        func = functools.partial(
            rename, line=keyword.lineno,
            utf8_byte_offset=keyword.value.col_offset, old=old, new=new,
        )
        yield ast_to_offset(node), func
