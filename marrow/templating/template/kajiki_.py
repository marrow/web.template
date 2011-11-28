# encoding: utf-8

from __future__ import unicode_literals

from os import path

from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver

try:
    from kajiki.loader import FileLoader
except ImportError:  # pragma: nocover
    raise ImportError('You must install the Kajiki package.')


__all__ = ['Kajiki']


resolve = Resolver()


class Kajiki(Engine):
    extmap = dict(xml="xml", htm="html", html="html", xhtml="xml", html5="html5", txt="text", text="text", kajiki="xml")
    mimetypes = dict(xml=b"text/xml", html=b"text/html", html5=b"text/html", text=b"text/plain")

    def prepare(self, filename, i18n=None, autoescape=False, **options):
        loader = FileLoader(None)
        loader._filename = self._filename
        template = loader.load(filename)
        return template

    def render(self, template, data, **options):
        kind = self.extmap.get(path.splitext(template.filename)[1][1:], 'text')

        result = template(data).render()

        return options.get('content_type', self.mimetypes[kind]), result

    def _filename(self, name):
        return resolve(name)[1]
