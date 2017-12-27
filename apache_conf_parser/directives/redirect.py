#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class Redirect(SimpleDirective):
    contexts = [
        'server_config',
        'virtual_host',
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_alias'
    description = 'Sends an external redirect asking the client to fetch a different URL'
    match_regexp = [
        r'^\s*Redirect\s+(?P<status>.*)\s+(?P<url_path>[^ ]*)\s+(?P<url>.*?)\s*$',
        r'^\s*Redirect\s+(?P<url_path>[^ ]*)\s+(?P<url>.*?)\s*$',
    ]

    @property
    def status(self):
        return self.matches.get('status')
