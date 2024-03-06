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


KWARGS = ['values', 'index', 'columns', 'aggregate_function']


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.func, ast.Attribute) and
            node.func.attr == 'pivot' and
            node.args and
            # check that it's probably not pandas, either because of unique keywords
            # or because pandas was never imported in this file
            (
                any(
                    kwarg in [kw.arg for kw in node.keywords] for kwarg in
                    ['aggregate_function', 'separator', 'sort_columns', 'maintain_order']
                ) or
                len(node.args) > 3 or
                ('pd' not in state.aliases and 'pandas' not in state.aliases)
            ) and
            state.settings.target_version >= (0, 20, 8)
    ):
        for i, arg in enumerate(node.args):
            if isinstance(arg, ast.Name):
                func = functools.partial(
                    rename, line=node.args[0].lineno,
                    utf8_byte_offset=arg.col_offset, old=arg.id, new=f'{KWARGS[i]}={arg.id}',
                )
                yield ast_to_offset(node), func
            elif isinstance(arg, ast.Constant):
                func = functools.partial(
                    rename, line=node.args[0].lineno,
                    utf8_byte_offset=arg.col_offset,
                    old=f"\"{arg.value}\"", new=f'{KWARGS[i]}="{arg.value}"',
                )
                yield ast_to_offset(node), func
                func = functools.partial(
                    rename, line=node.args[0].lineno,
                    utf8_byte_offset=arg.col_offset,
                    old=f"'{arg.value}'", new=f'{KWARGS[i]}="{arg.value}"',
                )
                yield ast_to_offset(node), func
            else:
                break
