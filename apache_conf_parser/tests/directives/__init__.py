#!/usr/bin/env python
import unittest

from apache_conf_parser.directives import Directive
from apache_conf_parser.exceptions import NodeCompleteError, InvalidLineError, DirectiveError


class GenericDirective(Directive):
    def add_line(self, line):
        try:
            self.parse_directive_header(line)
        except DirectiveError as e:
            raise InvalidLineError(str(e))
        super(GenericDirective, self).add_line(line)


class TestDirective(unittest.TestCase):
    CLASS = GenericDirective

    def test_new_complete(self):
        node = self.CLASS()
        self.assertFalse(node.complete)

    def test_not_changed(self):
        node = self.CLASS()
        self.assertFalse(node.changed)

    def test_lines_empty(self):
        node = self.CLASS()
        self.assertEqual(node.lines, [])

    def test_name_header_incomplete_1(self):
        node = self.CLASS()
        node.add_line("name\\")
        self.assertEqual(node.name, "name")

    def test_name_header_incomplete_2(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        print('dir(node): %s' % dir(node))
        self.assertEqual(node.name, "name")

    def test_name_complete_1(self):
        node = self.CLASS()
        node.add_line("name arg1")
        node.complete = True
        self.assertEqual(node.name, "name")

    def test_name_complete_2(self):
        node = self.CLASS()
        node.add_line("name arg1")
        node.complete = False
        self.assertEqual(node.name, "name")

    def test_name_complete_3(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertEqual(node.name, "name")

    def test_new_args(self):
        # even though the name is not set yet...
        node = self.CLASS()
        self.assertEqual(node.arguments, [])

    def test_args_header_incomplete_1(self):
        node = self.CLASS()
        node.add_line("name\\")
        self.assertEqual(node.arguments, [])

    def test_args_header_incomplete_2(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        self.assertEqual(node.arguments, ["arg1", ])

    def test_args_complete_empty_args_1(self):
        node = self.CLASS()
        node.parse_directive_header("name")
        node.complete = True
        self.assertEqual(node.arguments, [])

    def test_args_complete_empty_args_2(self):
        node = self.CLASS()
        node.parse_directive_header("name")
        self.assertEqual(node.arguments, [])

    def test_args_complete_not_empty_args_1(self):
        node = self.CLASS()
        node.parse_directive_header("name arg1")
        self.assertEqual(node.arguments, ["arg1", ])

    def test_args_complete_not_empty_args_2(self):
        node = self.CLASS()
        node.parse_directive_header("name arg1 arg2")
        self.assertEqual(node.arguments, ["arg1", "arg2"])

    def test_args_complete_not_empty_args_3(self):
        node = self.CLASS()
        node.parse_directive_header("name\\")
        node.parse_directive_header("arg1")
        self.assertEqual(node.arguments, ["arg1", ])

    def test_args_complete_not_empty_args_4(self):
        node = self.CLASS()
        node.parse_directive_header("name arg1\\")
        node.parse_directive_header("arg2")
        self.assertEqual(node.arguments, ["arg1", "arg2"])

    def test_new_content(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.content


if __name__ == '__main__':
    unittest.main()
