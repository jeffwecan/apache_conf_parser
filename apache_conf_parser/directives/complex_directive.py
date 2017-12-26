#!/usr/bin/env python
import re

from apache_conf_parser.directives import Directive
from apache_conf_parser.directives.simple_directive import SimpleDirective
from apache_conf_parser.exceptions import DirectiveError, NodeCompleteError, InvalidLineError
from apache_conf_parser.nodes import Node
from apache_conf_parser.nodes.complex_node import ComplexNode


class ComplexDirective(Directive):
    is_node_candidate = True
    complex = True

    match_regexp = r"\s*<\s*%s(\s+[^>]*)*\s*(>\s*|[\\])$" % Directive.name_regexp

    def __init__(self, body_class=None):
        super(ComplexDirective, self).__init__()
        if body_class is None:
            body_class = ComplexNode
        self.header = SimpleDirective()
        self.body = body_class(self.get_node_candidates())
        self.tail = ""
        self.tailmatch = False

    @staticmethod
    def get_node_candidates():
        return [cls for cls in Node.get_subclasses() if cls != ComplexNode]

    @property
    def name(self):
        return self.header.name

    @property
    def arguments(self):
        return self.header.arguments

    @property
    def stable(self):
        return self.complete

    @property
    def complete(self):
        if self.body.complete and not self.header.complete:
            raise NodeCompleteError("Body is complete but header isn't.")
        if self.tailmatch and not self.body.complete:
            raise NodeCompleteError("Tail is matched but body is not complete.")
        return self.header.complete and self.body.complete and self.tailmatch

    @complete.setter
    def complete(self, val):
        if val and not (self.body.complete and self.header.complete and self.tailmatch):
            raise NodeCompleteError("Cannot set a complex directive to complete if its parts aren't complete")
        if not val and self.body.complete and self.header.complete and self.tailmatch:
            raise NodeCompleteError("Cannot set a complex directive to not complete if its parts are all complete")
        super(ComplexDirective, ComplexDirective).complete.fset(self, val)

    def parse_header(self, line):
        try:
            super(ComplexDirective, self).add_line(line)
        except NodeCompleteError:
            pass
        if ">" in line:
            header_str, remainder = line.split(">", 1)
            if remainder.strip() != "":
                raise InvalidLineError("Directive header has an extraneous tail: %s" % line)
        else:
            header_str = line
        header_str = header_str.lstrip()
        if header_str and header_str.startswith("<") and self.header.name is None:
            header_str = header_str[1:]
        if header_str and "<" in header_str:
            raise InvalidLineError("Angle brackets not allowed in complex directive header.  Received: %s" % line)
        if header_str:
            try:
                self.header.parse_directive_header(header_str)
            except (NodeCompleteError, DirectiveError) as e:
                raise InvalidLineError(str(e))
        if ">" in line:
            self.header.complete = True

    def add_line(self, line, depth=0):
        # base case
        if self.complete:
            raise NodeCompleteError("Can't add lines to a complete Node.")

        # first we need a header
        if not self.header.complete:
            self.parse_header(line)
        # then the body
        elif not self.body.stable and not re.match("\s*</%s>\s*$" % self.name, line):
            self.body.add_line(line, depth + 1)
        # check for the closing tag / tail
        elif re.match("\s*</%s>\s*$" % self.name, line):
            self.body.complete = True
            self.tail = line
            self.tailmatch = True
        # if we haven't found the closing tag / tail, keep adding to the body
        elif not self.body.complete:
            self.body.add_line(line, depth + 1)
        else:
            raise InvalidLineError("Expecting closing tag. Got: %s" % line)

    def __str__(self):
        if not self.lines:
            raise NodeCompleteError("Can't turn an uninitialized complex directive into a string.")
        if not self.complete:
            raise NodeCompleteError("Can't turn an incomplete complex directive into a string.")
        return "%s\n%s%s%s" % (
            "\n".join(self.lines),
            self.body,
            "\n" if self.body.nodes else "",
            self.tail,
        )
