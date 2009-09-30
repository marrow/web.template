

templates = [
        'json:' # pure engine, usually a serializer
        'package.templates.foo' # defaulting the engine part, implicit filename extension
        'package/templates/foo.html' # defaulting the engine, explicit file path
        '/var/www/htdocs/index.html' # absolute path
        './views/edit.html'
        '../../templates/master.html' # relative paths
    ]


for i in templates:
    