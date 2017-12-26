
from unittest import TestCase

from apache_conf_parser.collections.list_adapter import ListAdapter


class TestListAdapter(TestCase):

    def test_instantiation(self):
        list_adapter = ListAdapter()
        expected = []
        actual = list_adapter.items
        self.assertEqual(
            first=expected,
            second=actual,
            msg='New list adapter expected to contain an empty list in items attribute, found: %s' % actual
        )

    def test_instantiation_with_items(self):
        test_items = [1, 2, 3]
        list_adapter = ListAdapter(*test_items)
        expected = test_items
        actual = list_adapter.items
        self.assertEqual(
            first=expected,
            second=actual,
            msg='New list adapter expected to contain list of initial args in items attribute, found: %s' % actual
        )

    def test_contains_value(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = test_item in list_adapter
        self.assertTrue(
            expr=actual,
            msg='Expected list_adapter contains magic method to return True for value: %s' % test_item
        )

    def test_set_item(self):
        test_item = 2
        list_adapter = ListAdapter(1)
        list_adapter[0] = test_item
        expected = test_item
        actual = list_adapter[0]
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected item at index 0 to be set to %s, found: %s' % (expected, actual)
        )

    def test_del_item(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        del list_adapter[0]
        actual = test_item in list_adapter
        self.assertFalse(
            expr=actual,
            msg='Expected list_adapter contains magic method to return False for value: %s' % test_item
        )
        with self.assertRaises(IndexError):
            assert list_adapter[0]

    def test_ne(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = list_adapter != list_adapter
        self.assertFalse(
            expr=actual,
            msg='Expected list_adapter to be equal to itself'
        )

    def test_lt(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = list_adapter < ListAdapter()
        self.assertFalse(
            expr=actual,
            msg='Expected empty list_adapter to be less than one containing items'
        )

    def test_lte(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = (list_adapter <= list_adapter)
        self.assertTrue(
            expr=actual,
            msg='Expected list_adapter to be less than or equal to itself'
        )
