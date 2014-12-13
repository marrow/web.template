# encoding: utf-8

from __future__ import unicode_literals, absolute_import

import os

from marrow.templating.core import Engine

try:
	from django.template import Template
except:
	raise ImportError('You must install the Django package.')


__all__ = ['Django']


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")


class Django(Engine):
	def prepare(self, filename, i18n=None, **options):
		with open(filename, 'r') as fh:
			template = Template(fh.read())
		
		return template

	def render(self, template, data, **options):
		return options.get('content_type', b"text/html"), template.render(data)
