#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class RewriteEngine(SimpleDirective):
    contexts = [
        'server_config',
        'virtual_host',
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_rewrite'
    description = 'Enables or disables runtime rewriting engine'

    match_regexp = r'\s*RewriteEngine\s+(?P<status>(on|off))\s*$'
