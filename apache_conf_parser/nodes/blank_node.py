#!/usr/bin/env python
from apache_conf_parser.exceptions import InvalidLineError
from apache_conf_parser.nodes import Node


class BlankNode(Node):
    """A blank line."""
    match_regexp = "\s*$"

    def add_line(self, line):
        if line.endswith("\\"):
            raise InvalidLineError("Blank lines cannot have line continuations.")
        super(BlankNode, self).add_line(line)
        self._content = ""
