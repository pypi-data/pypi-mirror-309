"""Specialized implementation of a trie.

See: https://en.wikipedia.org/wiki/Trie
"""

from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Tuple


@dataclass
class TrieNode:
    """Node in trie."""

    id: int
    text: Optional[str] = None
    value: Any = None
    children: "Optional[Dict[str, TrieNode]]" = None


class Trie:
    """A specialized trie data structure that finds all known words in a string."""

    def __init__(self) -> None:
        self.roots: Dict[str, TrieNode] = {}
        self._next_id = 0

    def insert(self, text: str, value: Any) -> None:
        """Insert a word and value into the trie."""
        current_node: Optional[TrieNode] = None
        current_children: Optional[Dict[str, TrieNode]] = self.roots

        last_idx = len(text) - 1
        for i, c in enumerate(text):
            if current_children is None:
                assert current_node is not None
                current_node.children = current_children = {}

            current_node = current_children.get(c)
            if current_node is None:
                current_node = TrieNode(id=self.next_id())
                current_children[c] = current_node

            if i == last_idx:
                current_node.text = text
                current_node.value = value

            current_children = current_node.children

    def find(self, text: str) -> Iterable[Tuple[int, str, Any]]:
        """Yield (end_pos, text, value) pairs of all words found in the string."""
        q = deque([(self.roots, 0)])
        visited = set()

        while q:
            item = q.popleft()
            current_children, current_position = item
            if current_position >= len(text):
                continue

            current_char = text[current_position]

            if current_position < len(text):
                q.append((current_children, current_position + 1))

            node = current_children.get(current_char)
            if (node is not None) and (node.id not in visited):
                visited.add(node.id)

                if node.text is not None:
                    # End is one past the current position
                    yield (current_position + 1, node.text, node.value)

                if node.children and (current_position < len(text)):
                    q.append((node.children, current_position + 1))

    def next_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id
