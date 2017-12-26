#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class RewriteRule(SimpleDirective):
    contexts = [
        'server_config',
        'virtual_host',
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_rewrite'
    description = 'Defines rules for the rewriting engine'
    match_regexp = r'\s*RewriteRule\s+(?P<regexp>[^ ]*)\s+(?P<substitution>[^ ]*)\s*\[?(?P<flags>[^] ]*)?\]?$'

    @property
    def flags(self):
        if self.matches is not None:
            flag_group = self.matches.get('flags')
            flags = [f.strip() for f in flag_group.split(',')]
            return flags
