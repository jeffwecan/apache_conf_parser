#!/usr/bin/env python
import unittest

from apache_conf_parser.lists.argument_list import ArgumentList
from apache_conf_parser.exceptions import DirectiveError


class TestArgumentList(unittest.TestCase):

    def test_instantiation(self):
        argument_list = ArgumentList()
        expected = []
        actual = argument_list.items
        self.assertEqual(
            first=expected,
            second=actual,
            msg='New list adapter expected to contain an empty list in items attribute, found: %s' % actual
        )

    def test_instantiation_with_items(self):
        test_items = ['on']
        argument_list = ArgumentList(*test_items)
        expected = test_items
        actual = argument_list.items
        self.assertEqual(
            first=expected,
            second=actual,
            msg='New list adapter expected to contain list of initial args in items attribute, found: %s' % actual
        )

    def test_set_argument(self):
        test_item = 'off'
        argument_list = ArgumentList('on')
        argument_list[0] = test_item
        expected = test_item
        actual = argument_list[0]
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected item at index 0 to be set to %s, found: %s' % (expected, actual)
        )

    def test_set_invalid_argument(self):
        test_initial_argument = 'on'
        test_new_argument = '<Directory /ooooops>'
        argument_list = ArgumentList(test_initial_argument)
        with self.assertRaises(DirectiveError) as err:
            argument_list[0] = test_new_argument
            expected_err_msg = 'Angle brackets not allowed in directive args.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised DirectiveError exception message, received: {}'.format(expected_err_msg, err),
            )
        expected = test_initial_argument
        actual = argument_list[0]
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected item at index 0 to be set to %s, found: %s' % (expected, actual)
        )


if __name__ == '__main__':
    unittest.main()
