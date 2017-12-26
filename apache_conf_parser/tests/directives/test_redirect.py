

from unittest import TestCase

from apache_conf_parser.directives.redirect import Redirect
from apache_conf_parser.exceptions import NodeCompleteError, ParserError, InvalidLineError


class TestRedirect(TestCase):

    def test_str_method_new_simple_directive(self):
        directive = Redirect()
        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an uninitialized simple directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line(self):
        directive = Redirect()
        test_line = 'Redirect /from-here /to-here'
        directive.add_line(test_line)
        expected = [test_line]
        actual = directive.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected lines attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_url_path_match(self):
        directive = Redirect()
        url_path = '/from-here'
        test_line = 'Redirect %s /to-here' % url_path
        directive.add_line(test_line)
        expected = url_path
        actual = directive.url_path
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected url_path attribute to be {}, received: {}'.format(expected, directive.matches),
        )

    def test_status_match(self):
        directive = Redirect()
        status_code = '418'
        test_line = 'Redirect %s /from-here /to-here' % status_code
        directive.add_line(test_line)
        expected = status_code
        actual = directive.status
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected status attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_url_match(self):
        directive = Redirect()
        url = '/to-here'
        test_line = 'Redirect /from-here %s' % url
        directive.add_line(test_line)
        expected = url
        actual = directive.url
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected url attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_add_invalid_line(self):
        directive = Redirect()
        test_line = '!!ImmaRedirectDirective !@#$ on'
        with self.assertRaises(ParserError) as err:
            directive.add_line(test_line)
            expected_err_msg = 'Unable to match line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised ParserError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line_with_none_as_arg(self):
        directive = Redirect()
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
        directive = Redirect()
        test_line = 'Redirect /from-here /to-here'
        directive.add_line(test_line)
        expected = test_line
        actual = str(directive)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive str representation to be {}, received: {}'.format(expected, actual),
        )
