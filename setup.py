#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup, find_packages


if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "templating", "release.py")).read())



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
                'nose',
                'coverage',
                'PyYAML',
                'Genshi',
                'Mako',
                'Kajiki'
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
        
        namespace_packages = [
                'marrow', 'marrow.templating', 'marrow.templating.serialize', 'marrow.templating.template',
                'alacarte', 'alacarte.serialize', 'alacarte.template',
                'cti', 'cti.serializers', 'cti.templating'
            ],
        
        entry_points = {
                'marrow.templating': [
                        'json = marrow.templating.serialize.json_:render',
                        'bencode = marrow.templating.serialize.bencode:render',
                        'yaml = marrow.templating.serialize.yaml_:render',
                        'pickle = marrow.templating.serialize.pickle_:render_pickle',
                        'cpickle = marrow.templating.serialize.pickle_:render_cpickle',
                        'marshal = marrow.templating.serialize.marshal_:render',
                        
                        'sprintf = marrow.templating.template.sprintf:SprintfEngine',
                        'formatter = marrow.templating.template.formatter:FormatterEngine',
                        'template = marrow.templating.template.template:render',
                        
                        'genshi = marrow.templating.template.genshi_:Genshi',
                        'jinja2 = marrow.templating.template.jinja2_:Jinja2',
                        'mako = marrow.templating.template.mako_:Mako',
                        'cheetah = marrow.templating.template.cheetah_:Cheetah',
                        'kajiki = marrow.templating.template.kajiki_:Kajiki',
                    ]
            }
    )
