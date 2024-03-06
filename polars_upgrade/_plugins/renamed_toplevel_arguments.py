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


# function name -> (min_version, old, new)
RENAMINGS = {
    'scan_ndjson': [
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'read_csv': [
        ((0, 19, 14), 'comment_char', 'comment_prefix'),
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'read_csv_batched': [
        ((0, 19, 14), 'comment_char', 'comment_prefix'),
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'scan_csv': [
        ((0, 19, 14), 'comment_char', 'comment_prefix'),
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'read_ipc': [
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'read_ipc_stream': [
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'scan_ipc': [
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'read_parquet': [
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'scan_parquet': [
        ((0, 20, 4), 'row_count_name', 'row_index_name'),
        ((0, 20, 4), 'row_count_offset', 'row_index_offset'),
    ],
    'read_excel': [
        ((0, 20, 6), 'xlsx2csv_options', 'engine_options'),
        ((0, 20, 7), 'read_csv_options', 'read_options'),
    ],
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
            isinstance(node.func.value, ast.Name) and
            node.func.value.id in state.aliases and
            len(node.keywords) >= 1
    ):
        for min_version, old, new in RENAMINGS[node.func.attr]:
            if not state.settings.target_version >= min_version:
                continue
            for keyword in node.keywords:
                if keyword.arg == old:
                    break
            else:
                continue
            func = functools.partial(
                rename, line=keyword.lineno,
                utf8_byte_offset=keyword.col_offset, old=old, new=new,
            )
            yield ast_to_offset(node), func
