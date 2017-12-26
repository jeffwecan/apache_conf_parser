#!/usr/bin/env python

from apache_conf_parser.directives.simple_directive import SimpleDirective


class RewriteBase(SimpleDirective):
    contexts = [
        'directory',
        '.htaccess'
    ]
    apache_module = 'mod_rewrite'
    description = 'Sets the base URL for per-directory rewrites'
    match_regexp = r'\s*RewriteBase\s+(?P<url_path>[^ ]+)\s*$'
