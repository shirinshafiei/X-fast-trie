from __future__ import annotations
from typing import Optional,cast
from sys import maxsize
from py_hopscotch_dict import HopscotchDict


class TrieNode:
    __slots__ = ("value", "leaf", "left", "right", "parent")

    def __init__(
        self,
        value: Optional[int],
        leaf: bool,
        left: Optional["TrieNode"] = None,
        right: Optional["TrieNode"] = None,
    ):
        self.value = value
        self.leaf = leaf
        self.left = left
        self.right = right
        self.parent: Optional["TrieNode"] = None


class XFastTrie:
    __slots__ = ("_root", "_level_tables", "_maxlen", "_count", "_min", "_max")

    def __init__(self, max_length: int = maxsize.bit_length() + 1):
        self._maxlen = max_length
        self._root = TrieNode(None, False)
        self._level_tables = self._make_tables(max_length)
        self._count = 0
        self._min = None
        self._max = None

    # ---------- helpers ----------

    @staticmethod
    def _make_tables(levels: int) -> list[HopscotchDict]:
        return [HopscotchDict() for _ in range(levels)]

    @staticmethod
    def _to_int(value: int | bytes, maxlen: int) -> int:
        if isinstance(value, int):
            if value < 0 or value.bit_length() > maxlen:
                raise ValueError("Invalid value for trie")
            return value

        if isinstance(value, bytes):
            if len(value) * 8 > maxlen:
                raise ValueError("Invalid value for trie")
            result = 0
            for b in value:
                result = (result << 8) | b
            return result

        raise TypeError("Only int or bytes allowed")

    # ---------- core search ----------

    def _closest_ancestor(self, value: int) -> tuple[TrieNode, int]:
        """
        Binary search over level tables to find
        the deepest prefix match.
        """
        node = self._root
        level_found = -1

        lo, hi = 0, self._maxlen - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            prefix = value >> (self._maxlen - mid - 1)

            if prefix in self._level_tables[mid]:
                node = self._level_tables[mid][prefix]
                level_found = mid
                lo = mid + 1
            else:
                hi = mid - 1

        return node, level_found

    def _closest_leaf(self, value: int) -> Optional[TrieNode]:
        """
        Returns the leaf closest to value.
        """
        ancestor, level = self._closest_ancestor(value)

        if ancestor.leaf:
            return ancestor

        bit = (value >> (self._maxlen - level - 2)) & 1
        child = ancestor.left if bit == 0 else ancestor.right

        if child is None:
            return None

        other = child.left if bit == 0 else child.right
        if other is None:
            return child

        return (
            child
            if abs(cast(int, child.value) - value)
            < abs(cast(int, other.value) - value)
            else other
        )

    # ---------- mutation ----------

    def insert(self, value: int | bytes) -> None:
        value = self._to_int(value, self._maxlen)
        if value in self._level_tables[-1]:
            return

        pred = succ = None
        if self._count:
            neighbor = cast(TrieNode, self._closest_leaf(value))
            if neighbor.value < value:
                pred, succ = neighbor, neighbor.right
            else:
                succ, pred = neighbor, neighbor.left

        leaf = TrieNode(value, True, pred, succ)

        if pred:
            pred.right = leaf
        if succ:
            succ.left = leaf

        if self._min is None or value < self._min.value:
            self._min = leaf
        if self._max is None or value > self._max.value:
            self._max = leaf

        node, depth = self._closest_ancestor(value)
        bits = bin(value)[2:].zfill(self._maxlen)

        for level in range(depth, self._maxlen - 1):
            prefix = int(bits[: level + 2], 2)

            if level == self._maxlen - 2:
                child = leaf
            else:
                child = TrieNode(prefix, False)

            child.parent = node
            if bits[level + 1] == "0":
                node.left = child
                node.right = node.right or leaf
            else:
                node.right = child
                node.left = node.left or leaf

            self._level_tables[level + 1][prefix] = child
            node = child

        while node:
            if not node.leaf:
                if node.left and node.left.leaf and node.left.value > value:
                    node.left = leaf
                if node.right and node.right.leaf and node.right.value < value:
                    node.right = leaf
            node = node.parent

        self._count += 1

    def remove(self, value: int | bytes) -> None:
        value = self._to_int(value, self._maxlen)
        node = self._level_tables[-1].get(value)

        if node is None:
            raise ValueError("Value not found")

        pred, succ = node.left, node.right
        if pred:
            pred.right = succ
        if succ:
            succ.left = pred

        if self._min and self._min.value == value:
            self._min = succ
        if self._max and self._max.value == value:
            self._max = pred

        level = self._maxlen - 1
        while node:
            parent = node.parent
            del self._level_tables[level][node.value]
            node.left = node.right = node.parent = None
            node = parent
            level -= 1

        self._count -= 1

    # ---------- queries ----------

    def predecessor(self, value: int | bytes) -> Optional[int]:
        value = self._to_int(value, self._maxlen)
        leaf = self._closest_leaf(value)
        if leaf is None:
            return None
        return leaf.left.value if leaf.value >= value else leaf.value

    def successor(self, value: int | bytes) -> Optional[int]:
        value = self._to_int(value, self._maxlen)
        leaf = self._closest_leaf(value)
        if leaf is None:
            return None
        return leaf.right.value if leaf.value <= value else leaf.value


    def search(self, value: int | bytes) -> Optional[TrieNode]:
        """
        Search for a value in the trie.

        :param value: The value to search for.
        :return: TrieNode if found, else None.
        """
        value = self._to_int(value, self._maxlen)
        return self._level_tables[-1].get(value)
