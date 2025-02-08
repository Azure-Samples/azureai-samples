from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, TypeVar

from typing_extensions import Self

T = TypeVar("T")
T2 = TypeVar("T2")


class Trie(Generic[T]):
    """A trie that accepts the parts (i.e `Path.parts`) of an absolute path, and stores some associated payload."""

    @dataclass
    class Node(Generic[T2]):
        """A trie node."""

        is_end: bool = False
        children: Dict[T2, Self] = field(default_factory=dict)

    def __init__(self) -> None:
        self.root: Trie.Node[T] = Trie.Node()
        self.len = 0

    def __len__(self) -> int:
        return self.len

    def insert(self, elems: Iterable[T]) -> None:
        """Insert a payload for a given path.

        :param Optional[PathType] p: The path to insert. If `None`, will insert at root
        :param T payload: The payload to store
        :returns: Whether or not the inserted path is the prefix of another path in the trie.
        :rtype: InsertType
        """
        curr = self.root

        for elem in elems:
            curr = curr.children.setdefault(elem, Trie.Node())

        if not curr.is_end:
            curr.is_end = True
            self.len += 1

    def is_prefix(self, elems: Iterable[T]) -> bool:
        """Check whether is the prefix of anything inserted into the trie"""

        curr = self.root

        for part in elems:
            if part not in curr.children:
                return False

            curr = curr.children[part]

        return True
