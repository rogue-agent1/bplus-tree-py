#!/usr/bin/env python3
"""B+ tree — database index structure."""
import sys

class BPlusNode:
    def __init__(self, leaf=False):
        self.keys = []; self.children = []; self.leaf = leaf; self.next = None

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusNode(leaf=True); self.order = order
    def search(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]: i += 1
            node = node.children[i]
        for i, k in enumerate(node.keys):
            if k == key: return node.children[i]
        return None
    def insert(self, key, value):
        leaf = self._find_leaf(key)
        i = 0
        while i < len(leaf.keys) and leaf.keys[i] < key: i += 1
        leaf.keys.insert(i, key); leaf.children.insert(i, value)
        if len(leaf.keys) >= self.order: self._split(leaf)
    def _find_leaf(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]: i += 1
            node = node.children[i]
        return node
    def _split(self, node):
        mid = len(node.keys) // 2
        new = BPlusNode(leaf=node.leaf)
        if node.leaf:
            new.keys = node.keys[mid:]; new.children = node.children[mid:]
            node.keys = node.keys[:mid]; node.children = node.children[:mid]
            new.next = node.next; node.next = new
            up_key = new.keys[0]
        else:
            up_key = node.keys[mid]
            new.keys = node.keys[mid+1:]; new.children = node.children[mid+1:]
            node.keys = node.keys[:mid]; node.children = node.children[:mid+1]
        if node == self.root:
            new_root = BPlusNode()
            new_root.keys = [up_key]; new_root.children = [node, new]
            self.root = new_root
    def range_query(self, lo, hi):
        node = self._find_leaf(lo); results = []
        while node:
            for i, k in enumerate(node.keys):
                if lo <= k <= hi: results.append((k, node.children[i]))
                elif k > hi: return results
            node = node.next
        return results

if __name__ == "__main__":
    tree = BPlusTree(order=4)
    for i in [10,20,5,15,25,30,1,8,12]: tree.insert(i, f"val_{i}")
    print(f"Search 15: {tree.search(15)}")
    print(f"Range 5-20: {tree.range_query(5, 20)}")
