from __future__ import annotations

import ast
import functools
from typing import Iterable

from tokenize_rt import Offset, Token

from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._ast_helpers import is_name_attr
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._token_helpers import delete_argument
from pyupgrade._token_helpers import find_op
from pyupgrade._token_helpers import parse_call_args
from pyupgrade._token_helpers import replace_name, is_simple_expression

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

RENAMINGS = {
    'map_dict': ((0, 19, 16), 'replace'),
}


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    breakpoint()
    if (
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Call) and
            is_simple_expression(node.func.value, state.aliases) and
            node.func.attr in RENAMINGS
    ):
        min_version, new_name = RENAMINGS[node.func.attr]
        breakpoint()
        if state.settings.current_version >= min_version:
            func = functools.partial(rename, name=node.func.attr, new=new_name)
            yield ast_to_offset(node), func
