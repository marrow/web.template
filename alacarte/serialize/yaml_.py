# encoding: utf-8

try:
    import yaml

except ImportError: # pragma: no cover
    raise ImportError('You must install the yaml package before you can serialize data this way.')


__all__ = ['render']


def render(data, template=None, i18n=None, **kw):
    """Serialize data using PyYAML.
    
    Accepts the same extended arguments as the PyYAML dump() function, see:
    
        http://pyyaml.org/wiki/PyYAMLDocumentation#DumpingYAML
    
    """
    
    return 'application/x-yaml', yaml.dump(data, **kw)
