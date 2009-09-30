import re

templates = [
        'json:', # pure engine, usually a serializer
        'package.templates.foo', # defaulting the engine part, implicit filename extension
        'package/templates/foo.html', # defaulting the engine, explicit file path
        '/var/www/htdocs/index.html', # absolute path
        './views/edit.html',
        '../../templates/master.html' # relative paths
    ]


def parse_strings(path, default="genshi"):
    # Split the engine and template parts.
    engine, _, template = path.rpartition(':')
    
    if not engine: engine = default
    
    if not template: return (engine, None, None)
    
    if template[0] in ('/', '.'): return (engine, None, template)
    
    # Split the template into package and path.
    package, _, path = template.partition('/')
    
    return (engine, package, path if path else None)
    

def parse_regex(path, default="genshi"):
    pass


for i in templates:
    print "%s -> %r" % (i, parse_strings(i))