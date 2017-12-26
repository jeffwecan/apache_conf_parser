#!/usr/bin/env python

import inspect
import re
from abc import ABCMeta, abstractmethod

from apache_conf_parser.exceptions import InvalidLineError, NodeCompleteError


class Node(object):
    """
    The apache parser node.

    """
    __metaclass__ = ABCMeta

    match_regexp = ".*"
    is_node_candidate = True

    def __init__(self):
        self.lines = []
        self._content = None
        self._complete = False
        self.changed = False
        self.matches = None

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self, val):
        self._complete = val

    @classmethod
    def match(cls, line):
        if line is None:
            return False
        return bool(re.match(cls.match_regexp, line))

    @property
    def content(self):
        return "\n".join(self.lines)

    @property
    def stable(self):
        return True

    @abstractmethod
    def add_line(self, line):

        if "\n" in line:
            raise InvalidLineError("Lines cannot contain newlines.")
        if self.complete:
            raise NodeCompleteError(line)

        matches = re.match(self.match_regexp, line)
        if matches:
            self.matches = matches.groupdict()

        self.lines.append(line)
        if not line.endswith("\\"):
            self.complete = True

    def __str__(self):
        if self.changed:
            return self.content or ""
        return "\n".join(self.lines)

    def __getattr__(self, attribute_name):
        if self.matches is not None and attribute_name in self.matches:
            return self.matches.get(attribute_name)
        else:
            raise AttributeError

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            # next two lines could be yield from subclass.get_subclasses() in python >=3.3
            for subsubclass in subclass.get_subclasses():
                yield subsubclass
            # yield from subclass.get_subclasses()
            if inspect.isabstract(subclass) or not subclass.is_node_candidate:
                continue
            yield subclass
