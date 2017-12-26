#!/usr/bin/env python

import unittest

from apache_conf_parser.exceptions import InvalidLineError, NodeCompleteError
from apache_conf_parser.nodes.blank_node import BlankNode


class TestBlankNode(unittest.TestCase):
    CLASS = BlankNode

    def test_not_complete(self):
        node = self.CLASS()
        self.assertFalse(node.complete)

    def test_not_changed(self):
        node = self.CLASS()
        self.assertFalse(node.changed)

    def test_lines_empty(self):
        node = self.CLASS()
        self.assertEqual(node.lines, [])

    def test_match_None(self):
        self.assertFalse(self.CLASS.match(None))

    def test_match_empty(self):
        self.assertTrue(self.CLASS.match(""))

    def test_match_comment_solo(self):
        self.assertFalse(self.CLASS.match("#"))

    def test_match_comment_solo_space(self):
        self.assertFalse(self.CLASS.match(" #"))

    def test_match_comment_space(self):
        self.assertFalse(self.CLASS.match(" # this is a comment"))

    def test_match_comment_no_space(self):
        self.assertFalse(self.CLASS.match("# this is a comment"))

    def test_match_comment_continuation(self):
        self.assertFalse(self.CLASS.match("# this is a comment\\"))

    def test_match_blank_spaces(self):
        self.assertTrue(self.CLASS.match("   "))

    def test_match_blank_tabs(self):
        self.assertTrue(self.CLASS.match("		"))

    def test_match_blank_continuation(self):
        self.assertFalse(self.CLASS.match("   \\"))

    def test_match_simple_directive_just_name(self):
        self.assertFalse(self.CLASS.match("name"))

    def test_match_simple_directive_just_name_leading_space(self):
        self.assertFalse(self.CLASS.match(" name"))

    def test_match_simple_directive_just_name_trailing_space(self):
        self.assertFalse(self.CLASS.match("name "))

    def test_match_simple_directive_just_name_continuation(self):
        self.assertFalse(self.CLASS.match("name\\"))

    def test_match_simple_directive_name_and_args(self):
        self.assertFalse(self.CLASS.match("name something else"))

    def test_match_simple_directive_leading_space(self):
        self.assertFalse(self.CLASS.match("   name something else"))

    def test_match_simple_directive_trailing_space(self):
        self.assertFalse(self.CLASS.match("name something else   "))

    def test_match_simple_directive_continuation(self):
        self.assertFalse(self.CLASS.match("name something else\\"))

    def test_match_complex_directive_empty(self):
        self.assertFalse(self.CLASS.match("<>"))

    def test_match_complex_directive_empty_space(self):
        self.assertFalse(self.CLASS.match("< >"))

    def test_match_complex_directive_just_name(self):
        self.assertFalse(self.CLASS.match("<name>"))

    def test_match_complex_directive_just_name_leading_space(self):
        self.assertFalse(self.CLASS.match("< name>"))

    def test_match_complex_directive_just_name_trailing_space(self):
        self.assertFalse(self.CLASS.match("<name >"))

    def test_match_complex_directive_just_name_open(self):
        self.assertFalse(self.CLASS.match("<name"))

    def test_match_complex_directive_just_name_open_continuation(self):
        self.assertFalse(self.CLASS.match("<name\\"))

    def test_match_complex_directive_just_name_open_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name \\"))

    def test_match_complex_directive_just_name_invalid_1(self):
        self.assertFalse(self.CLASS.match("<na+me>"))

    def test_match_complex_directive_just_name_invalid_2(self):
        self.assertFalse(self.CLASS.match("<na<me>"))

    def test_match_complex_directive_name_and_args_open(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2"))

    def test_match_complex_directive_name_and_args_open_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2\\"))

    def test_match_complex_directive_name_and_args_open_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2 \\"))

    def test_match_complex_directive_closed(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>"))

    def test_match_complex_directive_leading_space(self):
        self.assertFalse(self.CLASS.match("  <name arg1 arg2>"))

    def test_match_complex_directive_trailing_space(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>  "))

    def test_match_complex_directive_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>\\"))

    def test_match_complex_directive_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2> \\"))

    def test_match_complex_directive_trailing_text(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2> text"))

    def test___str___empty(self):
        node = self.CLASS()
        self.assertEqual("", str(node))

    def test___str___new_1(self):
        line = "    "
        node = self.CLASS()
        node.add_line(line)
        self.assertEqual("    ", str(node))

    def test___str___new_2(self):
        line = "	"
        node = self.CLASS()
        node.add_line(line)
        self.assertEqual("	", str(node))

    def test___str___changed(self):
        line = "    "
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual("    ", str(node))

    def test_add_line_newline(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("\n")

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

    def test_add_line_added_first(self):
        node = self.CLASS()
        node.add_line("    ")
        self.assertEqual(node.lines[0], "    ")

    def test_add_line_autocomplete(self):
        node = self.CLASS()
        node.add_line("    ")
        self.assertTrue(node.complete)

    def test_add_line_autochanged(self):
        node = self.CLASS()
        node.add_line("    ")
        self.assertFalse(node.changed)

    def test_add_line_continuation(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("  \\")

    def test_match_when_line_is_none(self):
        node = BlankNode()
        self.assertFalse(
            expr=node.match(None),
            msg='Node match() expected to return false when line arg is None',
        )

    def test_add_empty_line(self):
        node = BlankNode()
        test_line = ''
        node.add_line(test_line)
        self.assertEqual(
            [test_line],
            node.lines,
        )
        self.assertTrue(
            node.complete
        )
        self.assertTrue(
            expr=node.match(test_line),
            msg='BlankNode.match(line) expected to return true for line: {}'.format(test_line),
        )

    def test_content_after_adding_empty_line(self):
        node = BlankNode()
        test_line = ''
        node.add_line(test_line)
        expected = '\n'.join([test_line])
        actual = node.content
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Node content expected to match {}, received: {}'.format(expected, actual)
        )

    def test_stable_attribute(self):
        node = BlankNode()
        self.assertTrue(
            expr=node.stable,
            msg='Node stable attribute expected to default to True for BlankNodes',
        )

    def test_add_line_after_complete(self):
        node = BlankNode()
        test_line = ''
        node.add_line(test_line)
        with self.assertRaises(NodeCompleteError) as err:
            node.add_line(test_line)
            expected_err_msg = test_line
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_invalid_line(self):
        node = BlankNode()
        test_line = '\\'
        with self.assertRaises(InvalidLineError) as err:
            node.add_line(test_line)
            self.assertIn(
                member='Blank lines cannot have line continuations.',
                container=err,
            )
        self.assertFalse(
            node.complete
        )
        self.assertFalse(
            node.match(test_line),
            msg='BlankNode.match(line) expected to return false for line: {}'.format(test_line),
        )

    def test_add_whitespace_line(self):
        node = BlankNode()
        test_line = '   \t'
        node.add_line(test_line)
        self.assertEqual(
            [test_line],
            node.lines,
        )
        self.assertTrue(
            node.complete
        )
        self.assertTrue(
            expr=node.match(test_line),
            msg='BlankNode.match(line) expected to return true for line: {}'.format(test_line),
        )

    def test_add_line_with_newline(self):
        node = BlankNode()
        test_line = 'hi \n you'
        with self.assertRaises(InvalidLineError) as err:
            node.add_line(test_line)
            self.assertIn(
                member='Lines cannot contain newlines.',
                container=err,
            )
        self.assertFalse(
            node.complete
        )
        self.assertFalse(
            node.match(test_line),
            msg='BlankNode.match(line) expected to return false for line: {}'.format(test_line),
        )

    def test_str_method_when_not_changed_after_adding_line(self):

        node = BlankNode()
        test_line = ''
        node.add_line(test_line)

        node.changed = False

        expected = test_line
        actual = str(node)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='BlankNode str representation expected to be {} after adding line "{}". Received: {}'.format(
                expected,
                test_line,
                actual,
            )
        )

    def test_str_method_when_changed_after_adding_line(self):

        node = BlankNode()
        test_line = ''
        node.add_line(test_line)

        # TODO: mocking behavior orchestrated by complexnode, does that belong here?
        node.changed = True

        expected = ''
        actual = str(node)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='BlankNode str representation expected to be {} after adding line "{}". Received: {}'.format(
                expected,
                test_line,
                actual,
            )
        )

    def test_str_method_when_changed_after_adding_line_and_lines_empty(self):

        node = BlankNode()
        test_line = ''
        node.add_line(test_line)

        # TODO: mocking behavior orchestrated by complexnode, does that belong here?
        node.changed = True
        node.lines = []

        expected = ''
        actual = str(node)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='BlankNode str representation expected to be {} after adding line "{}". Received: {}'.format(
                expected,
                test_line,
                actual,
            )
        )

    # TODO: should individual nodes need their pattern to match the provided line? as-is complex_node orchestrates that
    # def test_add_non_blank_line(self):
    #     node = BlankNode()
    #     test_line = '# THIS IS ACTUALLY A COMMENT YA KNOW'
    #     node.add_line(test_line)
    #     self.assertIn(
    #         member=test_line,
    #         container=node.lines,
    #     )
    #     print(node.lines)


if __name__ == '__main__':
    unittest.main()
