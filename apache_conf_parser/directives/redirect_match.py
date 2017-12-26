#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class RedirectMatch(SimpleDirective):
    contexts = [
        'server_config',
        'virtual_host',
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_alias'
    description = 'Sends an external redirect based on a regular expression match of the current URL'
    match_regexp = r'\s*RedirectMatch\s*(?P<status>[^ ]*)?\s+(?P<regex>[^ ]*)\s+(?P<url>.*)$'
