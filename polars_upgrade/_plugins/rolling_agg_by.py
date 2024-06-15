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
from polars_upgrade._token_helpers import is_simple_expression

FUNCTIONS = (
    'rolling_min',
    'rolling_max',
    'rolling_mean',
    'rolling_sum',
    'rolling_prod',
    'rolling_std',
    'rolling_var',
)


def rename(
    i: int,
    tokens: list[Token],
    *,
    name: str,
    new: str,
) -> None:
    while not (tokens[i].name == "NAME" and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new)


def rename_function_and_name_argument(
    i: int,
    tokens: list[Token],
    *,
    name: str,
    new: str,
    unnamed_argument: str,
    named_argument: str,
) -> None:
    while not (tokens[i].name == "NAME" and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new)
    while not (tokens[i].name != "OP" and tokens[i].src.strip('\'"') == unnamed_argument):
        i += 1
    tokens[i] = tokens[i]._replace(src=named_argument)


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
        parent.func.attr in FUNCTIONS and
        not (
            isinstance(parent.func.value, ast.Attribute) and
            parent.func.value.attr in ("list", "name", "str", "struct", "dt")
        ) and
        ("by" in {kw.arg for kw in parent.keywords}) and
        not parent.args and
        state.settings.target_version >= (0, 20, 24)
    ):
        func = functools.partial(rename, name=parent.func.attr, new=f"{parent.func.attr}_by")
        yield ast_to_offset(node), func

    if (
        is_simple_expression(node.value, state.aliases["polars"]) and
        isinstance(parent, ast.Call) and
        isinstance(parent.func, ast.Attribute) and
        parent.func.attr in FUNCTIONS and
        not (
            isinstance(parent.func.value, ast.Attribute) and
            parent.func.value.attr in ("list", "name", "str", "struct", "dt")
        ) and
        ("by" in {kw.arg for kw in parent.keywords}) and
        len(parent.args) == 1 and
        state.settings.target_version >= (0, 20, 24)
    ):
        if isinstance(parent.args[0], ast.Constant):
            named_argument = f'window_size="{parent.args[0].value}"'
            unnamed_argument = parent.args[0].value
        elif isinstance(parent.args[0], ast.Name):
            named_argument = f'window_size={parent.args[0].id}'
            unnamed_argument = parent.args[0].id
        else:
            # who know what this could be
            return
        func = functools.partial(
            rename_function_and_name_argument,
            name=parent.func.attr, new=f'{parent.func.attr}_by',
            unnamed_argument=unnamed_argument,
            named_argument=named_argument,
        )
        yield ast_to_offset(node), func
