#!/usr/bin/env python
import unittest

from apache_conf_parser.exceptions import InvalidLineError, NodeCompleteError
from apache_conf_parser.nodes.comment_node import CommentNode


class TestCommentNode(unittest.TestCase):
    CLASS = CommentNode

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
        self.assertFalse(self.CLASS.match(""))

    def test_match_comment_solo(self):
        self.assertTrue(self.CLASS.match("#"))

    def test_match_comment_solo_space(self):
        self.assertTrue(self.CLASS.match(" #"))

    def test_match_comment_space(self):
        self.assertTrue(self.CLASS.match(" # this is a comment"))

    def test_match_comment_no_space(self):
        self.assertTrue(self.CLASS.match("# this is a comment"))

    def test_match_comment_continuation(self):
        self.assertFalse(self.CLASS.match("# this is a comment\\"))

    def test_match_blank_spaces(self):
        self.assertFalse(self.CLASS.match("   "))

    def test_match_blank_tabs(self):
        self.assertFalse(self.CLASS.match("		"))

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
        with self.assertRaises(NodeCompleteError):
            str(node)

    def test___str___new(self):
        line = "# comment"
        node = self.CLASS()
        node.add_line(line)
        self.assertEqual(line, str(node))

    def test___str___changed_1(self):
        line = "# comment"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual(line, str(node))

    def test___str___changed_2(self):
        line = " # comment"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual(line.lstrip(), str(node))

    def test_add_line_leading_space_1(self):
        node = self.CLASS()
        node.add_line(" # comment")
        self.assertEqual(node.lines[0], " # comment")

    def test_add_line_leading_space_2(self):
        node = self.CLASS()
        node.add_line("  # comment")
        self.assertEqual(node.lines[0], "  # comment")

    def test_add_line_leading_space_3(self):
        node = self.CLASS()
        node.add_line("	# comment")
        self.assertEqual(node.lines[0], "	# comment")

    def test_add_line_complete_1(self):
        node = self.CLASS()
        node.complete = True
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_2(self):
        node = self.CLASS()
        node.complete = True
        with self.assertRaises(NodeCompleteError):
            node.add_line("# comment")

    def test_add_line_complete_3(self):
        node = self.CLASS()
        node.add_line("# comment")
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_4(self):
        node = self.CLASS()
        node.add_line("# comment")
        with self.assertRaises(NodeCompleteError):
            node.add_line("# comment")

    def test_add_line_added_first(self):
        node = self.CLASS()
        node.add_line("# comment")
        self.assertEqual(node.lines[0], "# comment")

    def test_add_line_autocomplete(self):
        node = self.CLASS()
        node.add_line("# comment")
        self.assertTrue(node.complete)

    def test_add_line_autochanged(self):
        node = self.CLASS()
        node.add_line("# comment")
        self.assertFalse(node.changed)

    def test_add_line_continuation(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("# comment\\")

    def test_add_line_space_continuation(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("# comment \\")

    def test_add_comment_line(self):
        node = CommentNode()
        test_comment = ' This is a comment'
        test_line = '#{comment}'.format(comment=test_comment)
        node.add_line(test_line)
        expected = [test_line]
        actual = node.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Node lines expected to match {}, received: {}'.format(expected, actual)
        )
        self.assertTrue(
            expr=node.complete,
            msg='Node expected to be marked as complete when line does matches its regexp',
        )
        self.assertTrue(
            expr=node.match(test_line),
            msg='CommentNode.match(line) expected to return true for line: {}'.format(test_line),
        )
        self.assertEqual(
            first=test_comment,
            second=node._content,
            msg='CommentNode content expected to be {} when adding line "{}". Received: {}'.format(
                test_comment,
                test_line,
                node._content,
            )
        )

    def test_content_attribute_after_adding_comment_line(self):
        node = CommentNode()
        test_comment = ' This is a comment'
        test_line = '#{comment}'.format(comment=test_comment)
        node.add_line(test_line)
        expected = '\n'.join([test_line])
        actual = node.content
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Node content expected to match {}, received: {}'.format(expected, actual)
        )

    def test_stable_attribute(self):
        node = CommentNode()
        self.assertTrue(
            expr=node.stable,
            msg='Node stable attribute expected to default to True for CommentNodes',
        )

    def test_add_line_after_complete(self):
        node = CommentNode()
        test_comment = ' This is a comment'
        test_line = '#{comment}'.format(comment=test_comment)
        node.add_line(test_line)
        with self.assertRaises(NodeCompleteError) as err:
            node.add_line(test_line)
            expected_err_msg = test_line
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_match_when_line_is_none(self):
        node = CommentNode()
        self.assertFalse(
            expr=node.match(None),
            msg='Node match() expected to return false when line arg is None',
        )

    def test_str_method_no_lines(self):
        node = CommentNode()

        with self.assertRaises(NodeCompleteError) as err:
            node.__str__()
            expected_err_msg = "Can't turn an uninitialized comment node into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_str_method_when_not_changed_after_adding_line(self):
        node = CommentNode()
        test_comment = ' This is a comment'
        test_line = '#{comment}'.format(comment=test_comment)
        node.add_line(test_line)

        node.changed = False

        expected = test_line
        actual = str(node)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='CommentNode str representation expected to be {} after adding line "{}". Received: {}'.format(
                expected,
                test_line,
                actual,
            )
        )

    def test_str_method_when_changed_after_adding_line(self):
        node = CommentNode()
        test_comment = ' This is a comment'
        test_line = '#{comment}'.format(comment=test_comment)
        node.add_line(test_line)

        # TODO: mocking behavior orchestrated by complexnode, does that belong here?
        node.changed = True

        expected = test_line
        actual = str(node)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='CommentNode str representation expected to be {} after adding line "{}". Received: {}'.format(
                expected,
                test_line,
                actual,
            )
        )

    def test_add_invalid_line(self):
        node = CommentNode()
        test_line = '\\'
        with self.assertRaises(InvalidLineError) as err:
            node.add_line(test_line)
            expected_err_msg = 'Blank lines cannot have line continuations.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete when line does not match its regexp',
        )
        self.assertFalse(
            node.match(test_line),
            msg='CommentNode.match(line) expected to return false for line: {}'.format(test_line),
        )

    def test_add_empty_line(self):
        node = CommentNode()
        test_line = ''

        # with self.assertRaises(ParserError) as err:
        #     node.add_line(test_line)
        #     expected_err_msg = 'Unable to match line.'
        #     self.assertIn(
        #         member=expected_err_msg,
        #         container=err,
        #         msg='Expected "{}" in the raised ParserError exception message, received: {}'.format(expected_err_msg, err),
        #     )
        expected = []
        actual = node.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='No lines expected in node, received: {}'.format(node.lines),
        )
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete when line does not match its regexp',
        )
        self.assertFalse(
            expr=node.match(test_line),
            msg='CommentNode.match(line) expected to return false for line: {}'.format(test_line),
        )

    def test_add_whitespace_line(self):
        node = CommentNode()
        test_line = '   \t'
        expected = []
        actual = node.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='No lines expected in node, received: {}'.format(node.lines),
        )
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete when line does not match its regexp',
        )
        self.assertFalse(
            expr=node.match(test_line),
            msg='CommentNode.match(line) expected to return false for line: {}'.format(test_line),
        )

    def test_add_line_with_newline(self):
        node = CommentNode()
        test_line = 'hi \n you'
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete when line does not match its regexp',
        )
        self.assertFalse(
            expr=node.match(test_line),
            msg='CommentNode.match(line) expected to return false for line: {}'.format(test_line),
        )

    def test_dumps_empty(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.dumps()

    def test_dumps_empty_depth_0(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.dumps(0)

    def test_dumps_empty_depth_1(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.dumps(1)

    def test_dumps_empty_depth_1_keyword(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.dumps(depth=1)

    def test_dumps_empty_depth_2(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.dumps(2)

    def test_dumps_depth_0(self):
        node = self.CLASS()
        node.add_line("# comment")
        self.assertEqual("# comment", node.dumps(0))

    def test_dumps_depth_1(self):
        node = self.CLASS()
        node.add_line("# comment")
        self.assertEqual(self.CLASS().indent_str + "# comment", node.dumps(1))

    def test_dumps_depth_2(self):
        node = self.CLASS()
        node.add_line("# comment")
        self.assertEqual(self.CLASS().indent_str * 2 + "# comment", node.dumps(2))

    # @u_mod.skip("Currently comments cannot have leading spaces.")
    def test_dumps_leading_space(self):
        line = " # comment"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual(line.lstrip(), str(node))


if __name__ == '__main__':
    unittest.main()
