#!/usr/bin/env python
import unittest

from parameterized import parameterized

from apache_conf_parser.directives.rewrite_engine import RewriteEngine


class TestRewriteEngine(unittest.TestCase):

    @parameterized.expand([
        ("on", 'RewriteEngine on', 'on'),
        ("off", 'RewriteEngine off', 'off'),
        ("trailing spaces", 'RewriteEngine on     ', 'on'),
        ("extra spaces", 'RewriteEngine      on', 'on'),
    ])
    def test_matches_valid_directives(self, name, directive_line, expected_status):
        directive = RewriteEngine()
        directive.add_line(directive_line)
        self.assertIsNotNone(
            obj=directive.matches,
            msg='Directive expected to match RewriteCond for "%s" ("%s"), it did not match.' % (name, directive_line)
        )

        actual_status = directive.status
        self.assertEqual(
            first=expected_status,
            second=actual_status,
            msg='Status attribute for RewriteEngine returned unexpected value: "%s". Expected: "%s".' % (expected_status, actual_status)
        )

    @parameterized.expand([
        ("too many on's", 'RewriteEngine on on'),
        ("invalid argument", 'RewriteEngine yes'),
        ("wrong directive name", 'Redirect on'),
    ])
    def test_does_not_match_invalid_directives(self, name, directive_line):
        directive = RewriteEngine()
        directive.add_line(directive_line)
        self.assertIsNone(
            obj=directive.matches,
            msg='Directive not expected to match RewriteCond for "%s" ("%s"), it did match.' % (name, directive_line)
        )


if __name__ == '__main__':
    unittest.main()
