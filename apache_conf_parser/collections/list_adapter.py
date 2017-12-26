#!/usr/bin/env python
from collections import MutableSequence


class ListAdapter(MutableSequence):
    """Generic collection for maintaining a list of 'items'."""
    def __init__(self, *args):
        self.items = []
        for arg in args:
            self.append(arg)

    def __len__(self):
        return len(self.items)

    def __contains__(self, val):
        return val in self.items

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, val):
        self.items[index] = val

    def __delitem__(self, index):
        del self.items[index]

    def insert(self, index, val):
        self.items.insert(index, val)

    def __eq__(self, val):
        return self.items == val

    def __ne__(self, val):
        return self.items != val

    def __lt__(self, val):
        return self.items < val

    def __le__(self, val):
        return self.items <= val

    def __gt__(self, val):
        return self.items > val

    def __ge__(self, val):
        return self.items >= val

    def __repr__(self):
        return repr(self.items)
