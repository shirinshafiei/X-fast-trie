import math


class Node:
    def __init__(self, prefix=None, level=None):
        self.prefix = prefix
        self.level = level
        self.left = None  # Successor thread or 0-child
        self.right = None  # Predecessor thread or 1-child
        self.prev = None  # Leaf linked list
        self.next = None  # Leaf linked list
        self.is_leaf = False
        self.ref_count = 0


class XFastTrie:
    def __init__(self, w):
        self.w = w
        self.levels = [{} for _ in range(w + 1)]
        self.root = Node(0, 0)
        self.levels[0][0] = self.root

        # Sentinels
        self.min_sentinel = Node(-1, w)
        self.max_sentinel = Node(float('inf'), w)
        self.min_sentinel.next = self.max_sentinel
        self.max_sentinel.prev = self.min_sentinel
        self.min_sentinel.is_leaf = self.max_sentinel.is_leaf = True

        self.root.left = self.max_sentinel
        self.root.right = self.min_sentinel

    def exists(self, val):
        return val in self.levels[self.w]

    def insert(self, val):
        if self.exists(val) or val < 0 or val >= 2 ** self.w:
            return False

        pred, succ = self._find_neighbors_nodes(val)
        curr = self.root
        curr.ref_count += 1

        for i in range(1, self.w + 1):
            bit = (val >> (self.w - i)) & 1
            prefix = val >> (self.w - i)

            if bit == 0:
                if curr.left is None or curr.left.is_leaf:
                    curr.left = Node(prefix, i)
                curr = curr.left
            else:
                if curr.right is None or curr.right.is_leaf:
                    curr.right = Node(prefix, i)
                curr = curr.right

            curr.ref_count += 1
            self.levels[i][prefix] = curr

        curr.is_leaf = True
        curr.prev, curr.next = pred, succ
        pred.next = curr
        succ.prev = curr
        self._update_threads(val)
        return True

    def delete(self, val):
        if not self.exists(val):
            return False

        leaf = self.levels[self.w][val]
        pred, succ = leaf.prev, leaf.next
        pred.next = succ
        succ.prev = pred

        curr = self.root
        curr.ref_count -= 1
        for i in range(1, self.w + 1):
            bit = (val >> (self.w - i)) & 1
            prefix = val >> (self.w - i)
            next_node = self.levels[i][prefix]

            next_node.ref_count -= 1
            if next_node.ref_count == 0:
                del self.levels[i][prefix]
                if bit == 0:
                    curr.left = None
                else:
                    curr.right = None
                break
            curr = next_node

        self._update_threads_after_delete(val, pred, succ)
        return True

    def predecessor(self, val):
        if self.exists(val):
            res = self.levels[self.w][val].prev.prefix
            return res if res != -1 else None
        pred, _ = self._find_neighbors_nodes(val)
        return pred.prefix if pred != self.min_sentinel else None

    def successor(self, val):
        if self.exists(val):
            res = self.levels[self.w][val].next.prefix
            return res if res != float('inf') else None
        _, succ = self._find_neighbors_nodes(val)
        return succ.prefix if succ != self.max_sentinel else None

    def get_all(self):
        res = []
        curr = self.min_sentinel.next
        while curr != self.max_sentinel:
            res.append(curr.prefix)
            curr = curr.next
        return res

    def _find_neighbors_nodes(self, val):
        low, high = 0, self.w
        best_node = self.root
        while low <= high:
            mid = (low + high) // 2
            prefix = val >> (self.w - mid)
            if prefix in self.levels[mid]:
                best_node = self.levels[mid][prefix]
                low = mid + 1
            else:
                high = mid - 1

        if best_node.is_leaf:
            if best_node.prefix == val: return best_node.prev, best_node.next
            return (best_node, best_node.next) if best_node.prefix < val else (best_node.prev, best_node)

        bit = (val >> (self.w - best_node.level - 1)) & 1
        if bit == 0:
            succ = best_node.left
            return succ.prev, succ
        else:
            pred = best_node.right
            return pred, pred.next

    def _update_threads(self, val):
        curr = self.root
        for i in range(self.w):
            if curr.left is None or curr.left.is_leaf:
                curr.left = self._get_successor_leaf(val)
            if curr.right is None or curr.right.is_leaf:
                curr.right = self._get_predecessor_leaf(val)
            bit = (val >> (self.w - i - 1)) & 1
            prefix = val >> (self.w - i - 1)
            if prefix in self.levels[i + 1]:
                curr = self.levels[i + 1][prefix]
            else:
                break

    def _update_threads_after_delete(self, deleted_val, old_pred, old_succ):
        for level_map in self.levels:
            for node in level_map.values():
                if not node.is_leaf:
                    if node.left and node.left.is_leaf and node.left.prefix == deleted_val:
                        node.left = old_succ
                    if node.right and node.right.is_leaf and node.right.prefix == deleted_val:
                        node.right = old_pred

    def _get_predecessor_leaf(self, val):
        p, _ = self._find_neighbors_nodes(val)
        return p

    def _get_successor_leaf(self, val):
        _, s = self._find_neighbors_nodes(val)
        return s