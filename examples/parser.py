import re, datetime

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
    

reg = re.compile(
        r'^'
        r'(?:(?P<engine>[^:]+):)?'
        r'(?:(?P<package>[^/.][^/]+))?'
        r'(?:(?P<path>.+))?'
        r'$'
    )

def parse_regex(path, default="genshi"):
    engine, package, path = reg.match(path).groups()
    return engine if engine else default, package, path


callcount = range(25000)
fn = parse_strings

for n in [0, 1]:
    for i in templates:
        now = datetime.datetime.now()
        
        for j in callcount:
            k = fn(i)
        
        diff = datetime.datetime.now() - now
        
        print "[%r]\t%s -> %r" % (diff.microseconds, i, k)
    
    fn = parse_regex
    print