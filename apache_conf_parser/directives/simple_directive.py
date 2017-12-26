#!/usr/bin/env python

from apache_conf_parser.directives import Directive
from apache_conf_parser.exceptions import DirectiveError, NodeCompleteError, InvalidLineError


class SimpleDirective(Directive):
    is_node_candidate = True
    match_regexp = r"\s*%s(\s+.*)*\s*[\\]?$" % Directive.name_regexp

    def add_line(self, line):
        try:
            self.parse_directive_header(line)
        except DirectiveError as e:
            raise InvalidLineError(str(e))
        super(SimpleDirective, self).add_line(line)

    def parse_directive_header(self, line):
        if self.complete:
            raise NodeCompleteError("Cannot add to the header of a complete directive.")
        if not line:
            raise DirectiveError("An empty line is not a valid header line.")
        stable = True
        if line[-1] == "\\":
            line = line[:-1]
            stable = False
        parts = line.strip().split()

        # Retrieve the directive name from the beginning of the line
        if self._name is None:
            self.name = parts[0]

        # Store the remainder of the directive in the arguments attribute
        for part in parts[1:]:
            self.arguments.append(part)
        self._stable = stable

    def __str__(self):
        if not self.lines:
            raise NodeCompleteError("Can't turn an uninitialized simple directive into a string.")
        return super(SimpleDirective, self).__str__()
