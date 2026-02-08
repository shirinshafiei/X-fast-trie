# XFast Trie Implementation in Python

A Python implementation of the XFast Trie data structure for fast integer set operations with bounded universe.

##  Overview

XFast Trie is an efficient data structure for storing **non-negative integers** in a bounded universe `[0, U-1]` that provides `O(log log U)` time complexity for all operations including successor and predecessor queries.

##  Features

- **Fast Operations**: All operations run in `O(log log U)` time
- **Bounded Universe**: Optimized for integer sets with known maximum value
- **Complete Implementation**: Includes insert, delete, find, successor, and predecessor operations
- **Hash Table Based**: Uses hash tables at each level for fast access
- **Doubly Linked List**: Leaf nodes form a sorted doubly linked list for traversal
- **Non-Negative Only**: Supports only 0 and positive integers

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/xfast-trie.git
cd xfast-trie
