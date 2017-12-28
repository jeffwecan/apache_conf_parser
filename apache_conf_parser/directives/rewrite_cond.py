#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class RewriteCond(SimpleDirective):
    contexts = [
        'server_config',
        'virtual_host',
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_rewrite'
    description = 'Defines a condition under which rewriting will take place'

    match_regexp = r'\s*RewriteCond\s+(?P<teststring>[^ ]*)\s+(?P<condpattern>[^ ]*)\s*\[?(?P<flags>[^] ]*)?\]?$'

    @property
    def flags(self):
        _flags = []
        if self.matches is not None:
            flag_group = self.matches.get('flags')
            _flags += [f.strip() for f in flag_group.split(',')]
        return _flags
