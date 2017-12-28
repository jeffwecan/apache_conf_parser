#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class RedirectPermanent(SimpleDirective):
    contexts = [
        'server_config',
        'virtual_host',
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_alias'
    description = 'Sends an external permanent redirect asking the client to fetch a different URL'
    match_regexp = r'^\s*RedirectPermanent\s+(?P<url_path>[^ ]*)\s+(?P<url>.*?)\s*$'
