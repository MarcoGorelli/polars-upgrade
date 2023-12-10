from __future__ import annotations

import ast
import collections
import pkgutil
from typing import Callable
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Protocol
from typing import Tuple
from typing import TypeVar

from tokenize_rt import Offset
from tokenize_rt import Token

from polars_upgrade import _plugins

Version = Tuple[int, ...]


class Settings(NamedTuple):
    target_version: Version = (3,)


class State(NamedTuple):
    settings: Settings
    aliases: set[str] = set()
    in_annotation: bool = False


AST_T = TypeVar('AST_T', bound=ast.AST)
TokenFunc = Callable[[int, List[Token]], None]
ASTFunc = Callable[[State, AST_T, ast.AST], Iterable[Tuple[Offset, TokenFunc]]]

RECORD_FROM_IMPORTS = frozenset((
    'polars',
))

FUNCS = collections.defaultdict(list)


def register(tp: type[AST_T]) -> Callable[[ASTFunc[AST_T]], ASTFunc[AST_T]]:
    def register_decorator(func: ASTFunc[AST_T]) -> ASTFunc[AST_T]:
        FUNCS[tp].append(func)
        return func
    return register_decorator


class ASTCallbackMapping(Protocol):
    def __getitem__(self, tp: type[AST_T]) -> list[ASTFunc[AST_T]]: ...


def visit(
        funcs: ASTCallbackMapping,
        tree: ast.Module,
        settings: Settings,
) -> dict[Offset, list[TokenFunc]]:
    initial_state = State(
        settings=settings,
    )

    nodes: list[tuple[State, ast.AST, ast.AST]] = [(initial_state, tree, tree)]

    ret = collections.defaultdict(list)
    while nodes:
        state, node, parent = nodes.pop()

        tp = type(node)
        for ast_func in funcs[tp]:
            for offset, token_func in ast_func(state, node, parent):
                ret[offset].append(token_func)

        if isinstance(node, ast.Import):
            for import_ in node.names:
                if import_.name == 'polars':
                    state.aliases.add(import_.asname or import_.name)

        for name in reversed(node._fields):
            value = getattr(node, name)
            if name in {'annotation', 'returns'}:
                next_state = state._replace(in_annotation=True)
            else:
                next_state = state

            if isinstance(value, ast.AST):
                nodes.append((next_state, value, node))
            elif isinstance(value, list):
                for value in reversed(value):
                    if isinstance(value, ast.AST):
                        nodes.append((next_state, value, node))
    return ret


def _import_plugins() -> None:
    plugins_path = _plugins.__path__
    mod_infos = pkgutil.walk_packages(plugins_path, f'{_plugins.__name__}.')
    for _, name, _ in mod_infos:
        __import__(name, fromlist=['_trash'])


_import_plugins()
