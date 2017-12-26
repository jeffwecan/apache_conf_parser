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

    def __str__(self):
        if not self.lines:
            raise NodeCompleteError("Can't turn an uninitialized simple directive into a string.")
        return super(SimpleDirective, self).__str__()
