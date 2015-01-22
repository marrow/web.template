#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

if sys.version_info < (2, 6):
	raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "templating", "release.py")).read())



class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))

setup(
		name = "marrow.templating",
		version = version,
		
		description = "A common templating and serialization interface for Python applications.",
		long_description = """\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.templating""",
		
		author = "Alice Bevan-McGregor",
		author_email = "alice+marrow@gothcandy.com",
		url = "https://github.com/marrow/marrow.templating",
		license = "MIT",
		
		test_suite = 'nose.collector',
		tests_require = [
				'pytest',
				'pytest-cov',
				'pytest-flakes',
				'pytest-cagoule',
				'pytest-spec<=0.2.22',
			],
		
		classifiers = [
				"Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Topic :: Software Development :: Libraries :: Python Modules"
			],
		
		packages = find_packages(exclude=['examples', 'tests']),
		include_package_data = True,
		package_data = {'': ['README.textile', 'LICENSE']},
		zip_safe = True,
		cmdclass = dict(
				test = PyTest,
			),
		namespace_packages = [
				'marrow', 'marrow.templating', 'marrow.templating.serialize', 'marrow.templating.template',
			],
		
		entry_points = {
				'marrow.templating': [
						'json = marrow.templating.serialize.json:render',
						'bencode = marrow.templating.serialize.bencode:render',
						'yaml = marrow.templating.serialize.yaml:render',
						'pickle = marrow.templating.serialize.pickle:render_pickle',
						'cpickle = marrow.templating.serialize.pickle:render_cpickle',
						'marshal = marrow.templating.serialize.marshal:render',
						
						'sprintf = marrow.templating.template.sprintf:SprintfEngine',
						'formatter = marrow.templating.template.formatter:FormatterEngine',
						'template = marrow.templating.template.template:render',
						
						'genshi = marrow.templating.template.genshi:Genshi',
						'jinja2 = marrow.templating.template.jinja2:Jinja2',
						'mako = marrow.templating.template.mako:Mako',
						'cheetah = marrow.templating.template.cheetah:Cheetah',
						'kajiki = marrow.templating.template.kajiki:Kajiki',
						'tenjin = marrow.templating.template.tenjin:Tenjin',
						'pytenjin = marrow.templating.template.tenjin:Tenjin',
					]
			}
	)
