from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from logging import getLogger
from typing import Any, Dict, Optional, Union

from tree_sitter import Language, Parser, Tree
from tree_sitter_yaml import language as yaml_language

from .box.py import BoxedPy
from .box.yaml import BoxedYaml, boxyaml
from .box.yaml.mapping import YamlBlockMapping
from .box.yaml.sequence import YamlBlockSequence

logger = getLogger(__name__)
parser = Parser(Language(yaml_language()))

COOKIE_GENERATOR = count(1)

# These constants need to sort a certain way, and are applied from higher
# numbers downward.
CHANGE = 1
APPEND = 2
DELETE = 3


@dataclass(order=True)
class PendingEdit:
    start: int
    end: int
    action: int
    cookie: int
    item: Optional[BoxedPy] = None


class YamlStream:
    """
    The main object of loading and saving yaml files.

    For example, YamlStream.from_string(...).text is the simplest roundtrip.

    The document must already have some structure, e.g. the root should be a
    block map or sequence.  This is for making targeted edits to that.
    """

    _tree: Tree
    _root: Union[YamlBlockMapping, YamlBlockSequence]
    _original_bytes: bytes
    _edits: Dict[int, PendingEdit]

    def __init__(self, tree: Tree, original_bytes: bytes) -> None:
        self._tree = tree
        self._original_bytes = original_bytes
        self._edits = {}

        # TODO test more with streams that start with "---"
        doc = self._tree.root_node.children[0]

        # We forward getitem etc to this object
        node = boxyaml(node=doc.children[0], stream=self)
        assert isinstance(node, (YamlBlockMapping, YamlBlockSequence))
        self.root = node

    # Forwarding methods

    def __getitem__(self, key: Union[int, str]) -> Any:
        return self.root[key]  # type: ignore[index]

    def __setitem__(self, key: Union[int, str], value: Any) -> None:
        self.root[key] = value  # type: ignore[index]

    def __delitem__(self, key: Union[int, str]) -> None:
        del self.root[key]  # type: ignore[arg-type]

    def append(self, other: Any) -> None:
        self.root.append(other)  # type: ignore[union-attr]

    # Private API for editing

    def cancel_cookie(self, cookie: int) -> None:
        self._edits.pop(cookie, None)

    def edit(
        self, item: BoxedYaml, new_item: Optional[BoxedPy], append: bool = False
    ) -> int:
        """
        Changes `item` (read from yaml) to `new_item` (a boxed python object).

        If `new_item` is None, it is a deletion.
        If `append` is True, it is an append.
        Otherwise, it is a swap.

        If there have been prior edits recorded in the same span, they are cancelled
        first.  This is necessary for code like:

        ```
        x["a"]["b"] = 1
        x["a"] = {}
        ```

        Edits are not actually resolved until you access `.text`.
        """
        cookie = next(COOKIE_GENERATOR)
        start = item.start_byte
        end = item.end_byte
        if new_item is None:
            self._remove_wholly_contained_edits(start, end)
            self._edits[cookie] = PendingEdit(start, end, DELETE, cookie, None)
        elif append:
            self._edits[cookie] = PendingEdit(end, end, APPEND, cookie, new_item)
        else:
            self._remove_wholly_contained_edits(start, end)
            self._edits[cookie] = PendingEdit(start, end, CHANGE, cookie, new_item)
        return cookie

    def _remove_wholly_contained_edits(self, start: int, end: int) -> None:
        # print(self._edits)
        overlapped_cookies: set[int] = set()
        for k, v in self._edits.items():
            if v.start >= start and v.end <= end and v.start != v.end:
                overlapped_cookies.add(k)

        for k in overlapped_cookies:
            del self._edits[k]

    @property
    def text(self) -> bytes:
        tmp = self._original_bytes

        # TODO verify edits are non-overlapping
        for edit in sorted(self._edits.values(), reverse=True):
            if edit.item:
                new_bytes = edit.item.to_bytes()
            else:
                new_bytes = b""
            logger.warning(
                "Apply edit: %r->%r @ %r",
                tmp[edit.start : edit.end],
                new_bytes,
                edit,
            )
            tmp = tmp[: edit.start] + new_bytes + tmp[edit.end :]
            # TODO restore tree-sitter edits if we can come up with the line/col values
            # self._tree.edit(edit.start, edit.end, edit.start + len(new_bytes), (0, 0), (0, 0))
        logger.warning("New text: %r", tmp)
        tmp = tmp.lstrip(b"\n")
        # TODO restore this as verification we made valid edits
        # assert parser.parse(tmp, old_tree=self._tree).root_node.text == tmp
        return tmp


def parse_str(data: str) -> YamlStream:
    original_bytes = data.encode("utf-8")
    return parse(original_bytes)


def parse(data: bytes) -> YamlStream:
    # print(type(data))
    return YamlStream(tree=parser.parse(data), original_bytes=data)
