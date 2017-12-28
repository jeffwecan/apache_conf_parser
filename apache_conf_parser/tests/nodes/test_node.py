#!/usr/bin/env python
import unittest

from apache_conf_parser.exceptions import NodeCompleteError
from apache_conf_parser.nodes import Node


class TestNode(unittest.TestCase):
    CLASS = Node

    def test_name_none(self):
        node = self.CLASS()
        print('hi: %s' % node.name)
        self.assertIsNone(node.name)

    def test_not_complete(self):
        node = self.CLASS()
        self.assertFalse(node.complete)

    def test_not_changed(self):
        node = self.CLASS()
        self.assertFalse(node.changed)

    def test_lines_empty(self):
        node = self.CLASS()
        self.assertEqual(node.lines, [])

    def test_match_empty(self):
        self.assertTrue(self.CLASS.match(""))

    def test_match_not_empty(self):
        self.assertTrue(self.CLASS.match("something"))

    def test_match_None(self):
        self.assertFalse(self.CLASS.match(None))

    def test_add_line_complete_1(self):
        node = self.CLASS()
        node.complete = True
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_2(self):
        node = self.CLASS()
        node.add_line("")
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_3(self):
        node = self.CLASS()
        node.add_line("first")
        with self.assertRaises(NodeCompleteError):
            node.add_line("second")

    def test_add_line_added_first(self):
        node = self.CLASS()
        node.add_line("first")
        self.assertEqual(node.lines[0], "first")

    def test_add_line_added_second(self):
        node = self.CLASS()
        node.add_line("first")
        node.complete = False
        node.add_line("second")
        self.assertEqual(node.lines[0], "first")
        self.assertEqual(node.lines[1], "second")

    def test_add_line_autocomplete(self):
        node = self.CLASS()
        node.add_line("first")
        self.assertTrue(node.complete)

    def test_add_line_autochanged(self):
        node = self.CLASS()
        node.add_line("first")
        self.assertFalse(node.changed)

    def test_add_line_continuation(self):
        node = self.CLASS()
        node.add_line("first\\")
        self.assertFalse(node.complete)

    def test_add_line_space_continuation(self):
        node = self.CLASS()
        node.add_line("first \\")
        self.assertFalse(node.complete)

    def test___str___empty(self):
        node = self.CLASS()
        self.assertEqual("", str(node))

    @unittest.skip("works if add_line on a complete node sets changed instead of raising.")
    def test___str___multiple(self):
        line1 = "first"
        line2 = "second"
        node = self.CLASS()
        node.add_line(line1)
        node.add_line(line2)
        self.assertEqual(line1 + "\n" + line2, str(node))

    def test___str___new(self):
        line = "first"
        node = self.CLASS()
        node.add_line(line)
        self.assertEqual(line, str(node))

    def test___str___changed(self):
        # should match self.content
        line = "first"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual(line, str(node))

    def test_dumps_empty(self):
        node = self.CLASS()
        self.assertEqual("", node.dumps())

    def test_dumps_empty_depth_0(self):
        node = self.CLASS()
        self.assertEqual("", node.dumps(0))

    def test_dumps_empty_depth_1(self):
        node = self.CLASS()
        self.assertEqual(self.CLASS().indent_str, node.dumps(1))

    def test_dumps_empty_depth_1_keyword(self):
        node = self.CLASS()
        self.assertEqual(self.CLASS().indent_str, node.dumps(depth=1))

    def test_dumps_empty_depth_2(self):
        node = self.CLASS()
        self.assertEqual(self.CLASS().indent_str * 2, node.dumps(2))

    def test_dumps_blank_depth_0(self):
        node = self.CLASS()
        node.add_line("")
        self.assertEqual("", node.dumps(0))

    def test_dumps_blank_depth_1(self):
        node = self.CLASS()
        node.add_line("")
        self.assertEqual(self.CLASS().indent_str, node.dumps(1))

    def test_dumps_blank_depth_2(self):
        node = self.CLASS()
        node.add_line("")
        self.assertEqual(self.CLASS().indent_str * 2, node.dumps(2))

    def test_dumps_depth_0(self):
        node = self.CLASS()
        node.add_line("first")
        self.assertEqual("first", node.dumps(0))

    def test_dumps_depth_1(self):
        node = self.CLASS()
        node.add_line("first")
        self.assertEqual(self.CLASS().indent_str + "first", node.dumps(1))

    def test_dumps_depth_2(self):
        node = self.CLASS()
        node.add_line("first")
        self.assertEqual(self.CLASS().indent_str * 2 + "first", node.dumps(2))

    def test_dumps_leading_spaces(self):
        node = self.CLASS()
        node.add_line("  first")
        self.assertEqual("first", node.dumps())

    def test_eq_blank_node(self):
        node1 = self.CLASS()
        node2 = self.CLASS()
        self.assertEqual(node1, node2)

    def test_eq_diff_class(self):
        node1 = self.CLASS()
        node2 = object()
        self.assertNotEquals(node1, node2)

    def test_eq_same_lines(self):
        node1 = self.CLASS()
        node1.add_line('first')
        node2 = self.CLASS()
        node2.add_line('first')
        self.assertEqual(node1, node2)


if __name__ == '__main__':
    unittest.main()
