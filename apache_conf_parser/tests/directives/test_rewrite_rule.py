#!/usr/bin/env python
import unittest

from apache_conf_parser.directives.rewrite_rule import RewriteRule
from apache_conf_parser.exceptions import NodeCompleteError, ParserError, InvalidLineError


class TestRewriteRule(unittest.TestCase):

    def test_str_method_new_simple_directive(self):
        directive = RewriteRule()
        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an uninitialized simple directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line(self):
        directive = RewriteRule()
        test_line = 'RewriteRule /from-here /to-here'
        directive.add_line(test_line)
        expected = [test_line]
        actual = directive.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected lines attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_regexp_match(self):
        directive = RewriteRule()
        regexp = '/from.*here'
        test_line = 'RewriteRule %s /to-here' % regexp
        directive.add_line(test_line)
        expected = regexp
        actual = directive.regexp
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected regexp attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_flags_match(self):
        directive = RewriteRule()
        flags = ['L']
        test_line = 'RewriteRule /from-here /to-here [%s]' % ','.join(flags)
        directive.add_line(test_line)
        expected = flags
        actual = directive.flags
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected flags attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_substitution_match(self):
        directive = RewriteRule()
        substitution = '/to-here'
        test_line = 'RewriteRule /from-here %s' % substitution
        directive.add_line(test_line)
        expected = substitution
        actual = directive.substitution
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected substitution attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_add_invalid_line(self):
        directive = RewriteRule()
        test_line = '!!ImmaRewriteRuleDirective !@#$ on'
        with self.assertRaises(ParserError) as err:
            directive.add_line(test_line)
            expected_err_msg = 'Unable to match line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised ParserError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line_with_none_as_arg(self):
        directive = RewriteRule()
        test_header_line = None
        with self.assertRaises(InvalidLineError) as err:
            directive.add_line(test_header_line)
            expected_err_msg = 'An empty line is not a valid header line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised DirectiveError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_str_magic_method_after_adding_line(self):
        directive = RewriteRule()
        test_line = 'RewriteRule /from-here /to-here'
        directive.add_line(test_line)
        expected = test_line
        actual = str(directive)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive str representation to be {}, received: {}'.format(expected, actual),
        )


if __name__ == '__main__':
    unittest.main()
