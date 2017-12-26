

from unittest import TestCase

from apache_conf_parser.directives.complex_directive import ComplexDirective
from apache_conf_parser.exceptions import NodeCompleteError, ParserError, InvalidLineError


class TestComplexDirective(TestCase):

    def test_str_method_new_complex_directive(self):
        directive = ComplexDirective()
        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an uninitialized simple directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_name_property(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args>'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        expected = test_directive_name
        actual = directive.name
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected name property to be {}, received: {}'.format(expected, actual),
        )

    def test_arguments_property(self):
        directive = ComplexDirective()
        test_arguments = 'some args'
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args>'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        expected = test_arguments.split()
        actual = directive.arguments
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected arguments property to be {}, received: {}'.format(expected, actual),
        )

    def test_angle_brackes_in_directive_header(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args </{name}>'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        with self.assertRaises(InvalidLineError) as err:
            for test_line in test_lines:
                directive.add_line(test_line)
            expected_err_msg = 'Angle brackets not allowed in complex directive header.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_body_stable_check(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args </{name}>'.format(name=test_directive_name),
            'Redirect here \\',
            'there',
            '</{name}>'.format(name=test_directive_name),
        ]
        with self.assertRaises(InvalidLineError) as err:
            for test_line in test_lines:
                directive.add_line(test_line)
            expected_err_msg = 'Angle brackets not allowed in complex directive header.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line_to_complete_node(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            '</{name}>'.format(name=test_directive_name),
            'Redirect here there',
        ]
        with self.assertRaises(NodeCompleteError) as err:
            for test_line in test_lines:
                directive.add_line(test_line)
            expected_err_msg = "Can't add lines to a complete Node."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_set_complete_after_all_complete(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)

        directive.complete = True

        expected = True
        actual = directive.complete
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected complete property to be {}, received: {}'.format(expected, actual),
        )

    def test_body_complete_before_header(self):
        directive = ComplexDirective()
        directive.body.complete = True

        with self.assertRaises(NodeCompleteError) as err:
            directive.complete
            expected_err_msg = "Body is complete but header isn't."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_header_with_extraneous_tail(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_line = '<{name} some args> hir>'.format(name=test_directive_name)

        # TODO, see if we can do an assert calls on that complete.fset(self, val) call
        with self.assertRaises(InvalidLineError) as err:
            # for test_line in test_lines:
            directive.parse_header(test_line)
            expected_err_msg = "Directive header has an extraneous tail:"
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_set_not_complete_after_all_complete(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        with self.assertRaises(NodeCompleteError) as err:
            directive.complete = False
            expected_err_msg = "Cannot set a complex directive to not complete if its parts are all complete"
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_no_closing_tag_after_body_complete(self):
        directive = ComplexDirective()
        directive.add_line('<ImmaComplexDirective some args >')
        # contrived body.complete set to true
        directive.body.complete = True

        test_line = 'Redirect here there'
        with self.assertRaises(InvalidLineError) as err:

            directive.add_line(test_line),
            expected_err_msg = "Expecting closing tag. Got:"
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_tail_match_before_body_complete(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            '<{name}too some args >'.format(name=test_directive_name),
            'Redirect here there',
        ]

        for test_line in test_lines:
            directive.add_line(test_line)

        # TODO: would this ever happen "naturally"
        directive.tailmatch = True
        with self.assertRaises(NodeCompleteError) as err:
            print('tailmatcher', directive.tailmatch, directive.body.complete, directive.complete)
            directive.complete
            expected_err_msg = "TTail is matched but body is not complete."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_invalid_line(self):
        directive = ComplexDirective()
        test_line = '!!ImmaComplexDirective !@#$ on'
        with self.assertRaises(ParserError) as err:
            directive.add_line(test_line)
            expected_err_msg = 'Unable to match line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised ParserError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_str_magic_method_after_adding_line(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        expected = '\n'.join(test_lines)
        actual = str(directive)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive str representation to be {}, received: {}'.format(expected, actual),
        )

    def test_str_magic_method_with_incomplete_directive(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
        ]
        for test_line in test_lines:
            directive.add_line(test_line)

        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an incomplete complex directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )
