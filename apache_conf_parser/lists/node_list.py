#!/usr/bin/env python


from apache_conf_parser.lists.list_adapter import ListAdapter


class NodeList(ListAdapter):
    """Collection for nodes in an Apache configuration."""
    def __init__(self, *args):
        super(NodeList, self).__init__(*args)

    @property
    def stable(self):
        return all(item.stable for item in self.items)
