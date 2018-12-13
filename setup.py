#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import sys
import codecs


try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


if sys.version_info < (2, 7):
	raise SystemExit("Python 2.7 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 3):
	raise SystemExit("Python 3.3 or later is required.")

exec(open(os.path.join("web", "template", "release.py")).read())


class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))


here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-cagoule',  # intelligent test execution
		'pytest-spec<=0.2.22',  # output formatting
		'genshi',
		'mako',
		'tenjin',
	]


setup(
		name = "web.template",
		version = version,
		
		description = description,
		long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
		url = url,
		download_url = 'https://warehouse.python.org/project/WebCore.template/',
		
		author = author.name,
		author_email = author.email,
		license = "MIT",
		
		classifiers = [
				"Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Environment :: Web Environment",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Programming Language :: Python :: 2",
				"Programming Language :: Python :: 2.7",
				"Programming Language :: Python :: 3",
				"Programming Language :: Python :: 3.3",
				"Programming Language :: Python :: 3.4",
				"Programming Language :: Python :: Implementation :: CPython",
				"Programming Language :: Python :: Implementation :: PyPy",
				"Topic :: Internet :: WWW/HTTP :: WSGI",
				"Topic :: Software Development :: Libraries :: Python Modules",
			],
		
		packages = find_packages(exclude=['documentation', 'example', 'test']),
		include_package_data = True,
		namespace_packages = [
			'web',  # primary namespace
			'web.ext',  # WebCore template extension
			'web.template',  # engine namespace
			'web.template.serialize',  # serialization engines
			'web.template.template',  # template engines
		],
		
		entry_points = {
				'web.template': [
						'json = web.template.serialize.json:render',
						'bencode = web.template.serialize.bencode:render',
						'yaml = web.template.serialize.yaml:render',
						'pickle = web.template.serialize.pickle:render_pickle',
						'cpickle = web.template.serialize.pickle:render_cpickle',
						'marshal = web.template.serialize.marshal:render',
						
						'sprintf = web.template.template.sprintf:SprintfEngine',
						'formatter = web.template.template.formatter:FormatterEngine',
						'template = web.template.template.template:render',
						
						'genshi = web.template.template.genshi:Genshi',
						'jinja2 = web.template.template.jinja2:Jinja2',
						'mako = web.template.template.mako:Mako',
						'kajiki = web.template.template.kajiki:Kajiki',
						'tenjin = web.template.template.tenjin:Tenjin',
						'pytenjin = web.template.template.tenjin:Tenjin',
					]
			},
		
		install_requires = [
				'marrow.package>=2.0,<3.0',  # dynamic execution and plugin management
			],
		
		extras_require = dict(
				development = tests_require,
			),
		
		tests_require = tests_require,
		
		dependency_links = [],
		
		zip_safe = True,
		cmdclass = dict(
				test = PyTest,
			)
	)
