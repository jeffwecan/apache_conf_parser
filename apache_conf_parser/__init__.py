#!/usr/bin/env python

__version__ = '0.1'

from apache_conf_parser.directives.complex_directive import ComplexDirective
from apache_conf_parser.directives.redirect import Redirect
from apache_conf_parser.directives.redirect_match import RedirectMatch
from apache_conf_parser.directives.rewrite_rule import RewriteRule
from apache_conf_parser.directives.simple_directive import SimpleDirective
from apache_conf_parser.nodes import Node
from apache_conf_parser.nodes.blank_node import BlankNode
from apache_conf_parser.nodes.comment_node import CommentNode
from apache_conf_parser.nodes.complex_node import ComplexNode


class ApacheConfParser(ComplexNode):
    is_node_candidate = False
    NODES = [
        CommentNode,
        BlankNode,
        RewriteRule,
        RedirectMatch,
        Redirect,
        SimpleDirective,
        ComplexDirective,
    ]

    def __init__(self, source, infile=True, delay=False):
        super(ApacheConfParser, self).__init__(self.get_node_candidates())
        self.source = source.splitlines()
        if infile:
            self.source = [line.strip("\n") for line in open(source).readlines()]
        if not delay:
            self.parse()

    def parse(self):
        if self.complete:
            return
        for line in self.source:
            self.add_line(line)
        self.complete = True

    @classmethod
    def get_node_candidates(cls):
        return [c for c in Node.get_subclasses() if cls.__bases__ != (c,)]
