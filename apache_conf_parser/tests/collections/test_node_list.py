
from unittest import TestCase

from apache_conf_parser.collections.node_list import NodeList
from apache_conf_parser.directives.complex_directive import ComplexDirective


class TestNodeList(TestCase):

    def test_stable_property_when_empty(self):
        node_list = NodeList()
        actual = node_list.stable
        self.assertTrue(
            expr=actual,
            msg='Empty NodeList should be considered stable. Instead node_list.stable returned False.',
        )

    def test_stable_property_when_stable(self):
        test_directive = ComplexDirective()
        test_directive.add_line('<Immadirective>')
        test_directive.add_line('</Immadirective>')
        node_list = NodeList()
        node_list.append(test_directive)
        actual = node_list.stable
        self.assertTrue(
            expr=actual,
            msg='NodeList containing stable node(s) should be considered stable. Instead node_list.stable returned False.',
        )

    def test_stable_property_when_unstable(self):
        test_directive = ComplexDirective()
        test_directive.add_line('<Immadirective>')
        node_list = NodeList()
        node_list.append(test_directive)
        actual = node_list.stable
        self.assertFalse(
            expr=actual,
            msg='NodeList containing unstable node(s) should be considered unstable. Instead node_list.stable returned True.',
        )
