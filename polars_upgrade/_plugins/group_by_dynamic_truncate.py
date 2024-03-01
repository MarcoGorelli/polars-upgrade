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
from polars_upgrade._token_helpers import replace_argument


def _use_label(
    i: int,
    tokens: list[Token],
    *,
    truncate_value: object,
    truncate_idx: int,
) -> None:
    j = find_op(tokens, i, '(')
    func_args, _ = parse_call_args(tokens, j)
    if truncate_value is True:
        new = 'label="left"'
    elif truncate_value is False:
        new = 'label="datapoint"'
    else:
        return
    replace_argument(
        truncate_idx,
        tokens,
        func_args,
        new=new,
    )


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.func, ast.Attribute) and
            node.func.attr == 'group_by_dynamic' and
            len(node.keywords) >= 1 and
            state.settings.target_version >= (0, 19, 4)
    ):
        truncate_idx = None
        truncate_value = None
        for n, keyword_argument in enumerate(node.keywords):
            if (
                keyword_argument.arg == 'truncate' and
                isinstance(keyword_argument.value, ast.Constant)
            ):
                truncate_idx = n
                truncate_value = keyword_argument.value.value
                break
        else:
            return
        func = functools.partial(
            _use_label,
            truncate_value=truncate_value,
            truncate_idx=len(node.args) + truncate_idx,
        )
        yield ast_to_offset(node), func
