#!/usr/bin/env python

import re
from abc import ABCMeta, abstractmethod

from apache_conf_parser.lists.argument_list import ArgumentList
from apache_conf_parser.exceptions import DirectiveError, NodeCompleteError
from apache_conf_parser.nodes import Node


class Directive(Node):
    """A configuration directive."""
    __metaclass__ = ABCMeta

    name_regexp = r'[a-zA-Z]\w*'

    # Flag indicating if this class should be matched when parsing configuration lines
    is_node_candidate = False

    def __init__(self):
        super(Directive, self).__init__()
        self._arguments = ArgumentList()
        self._stable = False
        self._name = None

    @property
    def arguments(self):
        return self._arguments

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._name is not None:
            raise DirectiveError("Name is already set.  Cannot set to %s" % value)
        if not re.match(self.name_regexp, value):
            raise DirectiveError("Invalid name: %s" % value)
        self._name = value
        self._stable = True  # name is the first string in a given line

    @abstractmethod
    def add_line(self, line):
        super(Directive, self).add_line(line)

    @property
    def stable(self):
        return self._stable

    @property
    def complete(self):
        return super(Directive, Directive).complete.fget(self)

    @complete.setter
    def complete(self, val):
        if val and not self.stable:
            raise NodeCompleteError("Can't set an unstable Directive to complete.")
        super(Directive, Directive).complete.fset(self, val)

    @property
    def content(self):
        if self._name is None:
            raise NodeCompleteError("Name has not been set yet.")
        name = self.name if not self.arguments else self.name + " "
        return "%s%s" % (name, " ".join(arg for arg in self.arguments))

    def __repr__(self):
        return "<%s Directive at %s>" % (self.name, id(self))

    def parse_directive_header(self, line):
        if self.complete:
            raise NodeCompleteError("Cannot add to the header of a complete directive.")
        if not line:
            raise DirectiveError("An empty line is not a valid header line.")
        stable = True
        if line[-1] == '\\':
            line = line[:-1]
            stable = False
        parts = line.strip().split()

        # Retrieve the directive name from the beginning of the line
        if self.name is None:
            print('self_name is none')
            self.name = parts.pop(0)

        # Store the remainder of the directive in the arguments attribute
        for part in parts:
            self.arguments.append(part)
        self._stable = stable
