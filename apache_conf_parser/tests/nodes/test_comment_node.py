

from unittest import TestCase

from apache_conf_parser.exceptions import InvalidLineError, NodeCompleteError
from apache_conf_parser.nodes import comment_node


class TestCommentNode(TestCase):

    def test_add_comment_line(self):
        node = comment_node.CommentNode()
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
        node = comment_node.CommentNode()
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
        node = comment_node.CommentNode()
        self.assertTrue(
            expr=node.stable,
            msg='Node stable attribute expected to default to True for CommentNodes',
        )

    def test_add_line_after_complete(self):
        node = comment_node.CommentNode()
        test_comment = ' This is a comment'
        test_line = '#{comment}'.format(comment=test_comment)
        node.add_line(test_line)
        with self.assertRaises(NodeCompleteError) as err:
            node.add_line(test_line)
            expected_err_msg = test_line
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_match_when_line_is_none(self):
        node = comment_node.CommentNode()
        self.assertFalse(
            expr=node.match(None),
            msg='Node match() expected to return false when line arg is None',
        )

    def test_str_method_no_lines(self):
        node = comment_node.CommentNode()

        with self.assertRaises(NodeCompleteError) as err:
            node.__str__()
            expected_err_msg = "Can't turn an uninitialized comment node into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_str_method_when_not_changed_after_adding_line(self):

        node = comment_node.CommentNode()
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

        node = comment_node.CommentNode()
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
        node = comment_node.CommentNode()
        test_line = '\\'
        with self.assertRaises(InvalidLineError) as err:
            node.add_line(test_line)
            expected_err_msg = 'Blank lines cannot have line continuations.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
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
        node = comment_node.CommentNode()
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
        node = comment_node.CommentNode()
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
        node = comment_node.CommentNode()
        test_line = 'hi \n you'
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete when line does not match its regexp',
        )
        self.assertFalse(
            expr=node.match(test_line),
            msg='CommentNode.match(line) expected to return false for line: {}'.format(test_line),
        )
