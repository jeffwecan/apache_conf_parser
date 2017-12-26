

from unittest import TestCase

from apache_conf_parser.nodes import blank_node
from apache_conf_parser.exceptions import InvalidLineError, NodeCompleteError


class TestBlankNode(TestCase):

    def test_match_when_line_is_none(self):
        node = blank_node.BlankNode()
        self.assertFalse(
            expr=node.match(None),
            msg='Node match() expected to return false when line arg is None',
        )

    def test_add_empty_line(self):
        node = blank_node.BlankNode()
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
        node = blank_node.BlankNode()
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
        node = blank_node.BlankNode()
        self.assertTrue(
            expr=node.stable,
            msg='Node stable attribute expected to default to True for BlankNodes',
        )

    def test_add_line_after_complete(self):
        node = blank_node.BlankNode()
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
        node = blank_node.BlankNode()
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
        node = blank_node.BlankNode()
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
        node = blank_node.BlankNode()
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

        node = blank_node.BlankNode()
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

        node = blank_node.BlankNode()
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

        node = blank_node.BlankNode()
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
    #     node = blank_node.BlankNode()
    #     test_line = '# THIS IS ACTUALLY A COMMENT YA KNOW'
    #     node.add_line(test_line)
    #     self.assertIn(
    #         member=test_line,
    #         container=node.lines,
    #     )
    #     print(node.lines)
