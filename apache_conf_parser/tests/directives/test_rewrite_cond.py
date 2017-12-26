#!/usr/bin/env python
import unittest

from parameterized import parameterized

from apache_conf_parser.directives.rewrite_cond import RewriteCondDirective
from apache_conf_parser.exceptions import NodeCompleteError


class TestRewriteCond(unittest.TestCase):

    @parameterized.expand([
        ("file attribute test", 'RewriteCond /var/www/%{REQUEST_URI} !-f'),
        ("combine rule conditions", 'RewriteCond "%{REMOTE_HOST}"  "^host1"  [OR]'),
        ("variable in test string", 'RewriteCond  "%{HTTP_USER_AGENT}"  "(iPhone|Blackberry|Android)"')
    ])
    def test_matches_valid_directives(self, name, directive_line):
        directive = RewriteCondDirective()
        directive.add_line(directive_line)
        self.assertIsNotNone(
            obj=directive.matches,
            msg='Directive expected to match RewriteCond for "%s" ("%s"), it did not match.' % (name, directive_line)
        )

    @parameterized.expand([
        ("wrong name", 'RewriteRule /here /there'),
    ])
    def test_does_not_match_invalid_directives(self, name, directive_line):
        directive = RewriteCondDirective()
        directive.add_line(directive_line)
        self.assertIsNone(
            obj=directive.matches,
            msg='Directive not expected to match RewriteCond for "%s" ("%s"), it did match.' % (name, directive_line)
        )

    def test_str_method_new_simple_directive(self):
        directive = RewriteCondDirective()
        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an uninitialized simple directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line(self):
        directive = RewriteCondDirective()
        test_line = 'RewriteCond /from-here /to-here'
        directive.add_line(test_line)
        expected = [test_line]
        actual = directive.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected lines attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_flags_match(self):
        directive = RewriteCondDirective()
        flags = ['L']
        test_line = 'RewriteCond /from-here /to-here [%s]' % ','.join(flags)
        directive.add_line(test_line)
        expected = flags
        actual = directive.flags
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected flags attribute to be {}, received: {}'.format(expected, actual),
        )


if __name__ == '__main__':
    unittest.main()
