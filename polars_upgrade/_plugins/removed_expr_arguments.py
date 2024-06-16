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
from polars_upgrade._token_helpers import delete_argument
from polars_upgrade._token_helpers import is_simple_expression
from polars_upgrade._token_helpers import parse_call_args


def remove_argument(
    i: int,
    tokens: list[Token],
    *,
    line: int,
    offset: int,
    arg_idx: int,
) -> None:
    while not (tokens[i].name == 'OP' and tokens[i].src == '('):
        i -= 1
    func_args, _ = parse_call_args(tokens, i)
    delete_argument(arg_idx, tokens, func_args)


# function name -> (min_version, arg)
DELETIONS = {
    "top_k": ((0, 20, 31), "maintain_order"),
}


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
        is_simple_expression(node.value, state.aliases["polars"]) and
        isinstance(parent, ast.Call) and
        isinstance(parent.func, ast.Attribute) and
        parent.func.attr in DELETIONS and
        not (
            isinstance(node.value, ast.Attribute) and
            node.value.attr in ("list", "name", "str", "struct", "dt")
        )
    ):
        min_version, arg = DELETIONS[parent.func.attr]
        if arg not in (x.arg for x in parent.keywords):
            return
        lineno, col_offset = min(
            (kwarg.lineno, kwarg.col_offset) for kwarg in [*parent.keywords, *parent.args]
        )
        if state.settings.target_version >= min_version:
            func = functools.partial(
                remove_argument,
                line=lineno,
                offset=col_offset,
                arg_idx=1,
            )
            yield ast_to_offset(parent), func
