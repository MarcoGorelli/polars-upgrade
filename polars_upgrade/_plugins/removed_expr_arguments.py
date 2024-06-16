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
from polars_upgrade._token_helpers import find_op
from polars_upgrade._token_helpers import is_simple_expression
from polars_upgrade._token_helpers import parse_call_args


def remove_argument(
    i: int,
    tokens: list[Token],
    *,
    function_name: str,
    arg_idxs: list[int],
) -> None:
    # go forwards to function name
    while not (tokens[i].name == 'NAME' and tokens[i].src == function_name):
        i += 1
    j = find_op(tokens, i, '(')
    func_args, _ = parse_call_args(tokens, j)
    for idx in reversed(arg_idxs):
        delete_argument(idx, tokens, func_args)


# function name -> (min_version, arg)
DELETIONS = {
    "top_k": ((0, 20, 31), ("maintain_order", "multithreaded")),
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
        ) and
        len(parent.keywords) + len(parent.args) > 1
    ):
        min_version, args = DELETIONS[parent.func.attr]
        idxs = []
        for idx, kwarg in enumerate(parent.keywords, start=len(parent.args)):
            if kwarg.arg in args:
                idxs.append(idx)
        if not idxs:
            return
        if state.settings.target_version >= min_version:
            func = functools.partial(
                remove_argument,
                function_name=parent.func.attr,
                arg_idxs=idxs,
            )
            yield ast_to_offset(parent.func), func
