#!/usr/bin/env python

from apache_conf_parser.collections.node_list import NodeList
from apache_conf_parser.exceptions import NodeCompleteError, NodeMatchError, NestingLimitError
from apache_conf_parser.nodes import Node


class ComplexNode(Node):
    """
    A node that is composed of a list of other nodes.

    """
    NESTING_LIMIT = 10

    complex = True

    def __init__(self, candidates):
        super(ComplexNode, self).__init__()
        self.candidates = candidates
        self.nodes = NodeList()

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self, val):
        if val and not self.nodes.stable:
            raise NodeCompleteError(
                "The node list is not stable. Likely the last node is still waiting for additional lines.")
        super(ComplexNode, ComplexNode).complete.fset(self, val)

    @property
    def stable(self):
        return self.nodes.stable

    def get_node(self, line):
        for node_cls in self.candidates:
            if node_cls.match(line):
                return node_cls()
        raise NodeMatchError("No matching node: %s" % line)

    def add_line(self, line, depth=0):
        if self.complete:
            raise NodeCompleteError("Can't add lines to a complete Node.")
        if depth > self.NESTING_LIMIT:
            raise NestingLimitError("Cannot nest directives more than %s levels." % self.NESTING_LIMIT)
        if not self.nodes.stable:
            node = self.nodes[-1]
            if hasattr(node, 'complex'):
                node.add_line(line, depth=depth + 1)
            else:
                node.add_line(line)
        else:
            new_node = self.get_node(line)
            new_node.add_line(line)
            self.nodes.append(new_node)
        if not self.nodes.stable:
            self.complete = False

    def __str__(self):
        if not self.complete:
            raise NodeCompleteError("Can't turn an incomplete complex node into a string.")
        return "\n".join(str(node) for node in self.nodes)
