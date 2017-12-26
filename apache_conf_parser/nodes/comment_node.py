#!/usr/bin/env python
from apache_conf_parser.exceptions import InvalidLineError, NodeCompleteError
from apache_conf_parser.nodes import Node


class CommentNode(Node):
    """A comment."""
    match_regexp = r"\s*#(?P<comment>.*[^\\])?$"

    def add_line(self, line):
        if line.endswith("\\"):
            raise InvalidLineError("Comments cannot have line continuations.")
        super(CommentNode, self).add_line(line)
        self._content = self.comment

    def __str__(self):
        if not self.lines:
            raise NodeCompleteError("Can't turn an uninitialized comment node into a string.")
        if self.changed:
            return "#" + self._content
        return super(CommentNode, self).__str__()
