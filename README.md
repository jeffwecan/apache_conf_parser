apache_conf_parser
==================

An apache config parser for python.

The main `ApacheConfParser` class can be used to represent a list of Apache configuration directives as python objects. For example, to have the class parse directives directly from a string:

```python
from pprint import pprint

from apache_conf_parser import ApacheConfParser

wordpress_directives = '''RewriteEngine On
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]'''

apache_conf_parser = ApacheConfParser(wordpress_directives, infile=False)

pprint(apache_conf_parser.nodes)
print(apache_conf_parser.dumps())
```

This produces the following output:

```
[<RewriteEngine Directive at 4421257368>, <RewriteBase Directive at 4421355168>, <RewriteRule Directive at 4421354832>, <RewriteCond Directive at 4421354888>, <RewriteCond Directive at 4421355280>, <RewriteRule Directive at 4421355560>]
RewriteEngine On
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
```

Alternatively directives can be loaded from a file:

```python
from apache_conf_parser import ApacheConfParser
apache_conf_parser = ApacheConfParser('/path/to/.htaccess')

```
