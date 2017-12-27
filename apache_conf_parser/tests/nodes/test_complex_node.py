#!/usr/bin/env python
import unittest

from apache_conf_parser.directives.complex_directive import ComplexDirective
from apache_conf_parser.exceptions import NestingLimitError, NodeMatchError, NodeCompleteError
from apache_conf_parser.nodes.complex_node import ComplexNode


class TestComplexNode(unittest.TestCase):

    def test_str_method_new_complex_node(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        with self.assertRaises(NodeCompleteError) as err:
            str(node)
            expected_err_msg = "Can't turn an incomplete complex node into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_add_invalid_line(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        test_line = '\\'
        with self.assertRaises(NodeMatchError) as err:
            node.add_line(test_line)
            expected_err_msg = 'No matching node:'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeMatchError exception message, received: {}'.format(
                    expected_err_msg, err),
            )
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete when line does not match its regexp',
        )

    def test_set_complete_before_node_list_stable(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        node.add_line('<Immadirective>')
        with self.assertRaises(NodeCompleteError) as err:
            node.complete = True
            expected_err_msg = 'The node list is not stable. Likely the last node is still waiting for additional lines.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )
        self.assertFalse(
            expr=node.complete,
            msg='Node expected to be marked as incomplete its node list is not stable',
        )

    def test_add_line_to_completed_node(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        node.complete = True
        with self.assertRaises(NodeCompleteError) as err:
            node.add_line('<Immadirective>')
            expected_err_msg = "Can't add lines to a complete Node."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )
        self.assertTrue(
            expr=node.complete,
            msg='Node expected to be marked as complete after complete was set to True',
        )

    def test_add_line_at_depth_past_nesting_limit(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        with self.assertRaises(NestingLimitError) as err:
            node.add_line('<Immadirective>', depth=ComplexNode.NESTING_LIMIT + 1)
            expected_err_msg = "Cannot nest directives more than."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NestingLimitError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_add_complex_directive(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        test_node_name = 'Immadirective'
        test_lines = [
            '<{name} some args >'.format(name=test_node_name),
            'Redirect here there',
            '</{name}>'.format(name=test_node_name),
        ]
        for test_line in test_lines:
            node.add_line(test_line)

    def test_add_line_with_continuation_within_complex_directive(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        test_node_name = 'Immadirective'
        test_lines = [
            '<{name} some args >'.format(name=test_node_name),
            'Redirect here \\',
            'there',
            '</{name}>'.format(name=test_node_name),
        ]
        for test_line in test_lines:
            node.add_line(test_line)

    def test_dumps_empty(self):
        node = ComplexNode(ComplexDirective.get_node_candidates())
        with self.assertRaises(NodeCompleteError) as err:
            node.dumps()
            expected_err_msg = "Can't print an incomplete complex node."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )


if __name__ == '__main__':
    unittest.main()
