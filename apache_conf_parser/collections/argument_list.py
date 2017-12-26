#!/usr/bin/env python

import re

from apache_conf_parser.collections.list_adapter import ListAdapter
from apache_conf_parser.exceptions import DirectiveError


class ArgumentList(ListAdapter):
    """Validate the addition, change, or removal of arguments (for a given directive)."""
    def __setitem__(self, index, val):
        self.validate_argument(val)
        self.items[index] = val

    def insert(self, index, val):
        # append calls this insert method
        self.validate_argument(val)
        self.items.insert(index, val)

    @staticmethod
    def validate_argument(val):
        if not re.match("'.*'$|\".*\"$", val) and ("<" in val or ">" in val):
            raise DirectiveError("Angle brackets not allowed in directive args.  Received: %s" % val)
