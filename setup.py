#!/usr/bin/env python
# encoding: utf-8

import sys, os

from setuptools import setup, find_packages

if sys.version_info < (2, 5):
    raise SystemExit("Python 2.5 or later is required as 2.4 support requires too much cruft. -- BDFL")

execfile(os.path.join("alacarte", "release.py"))


setup(
        name = "marrow.render",
        version = version,
        
        description = "A common templating and serialization interface for Python applications.",
        long_description = "",
        author = "Alice Bevan-McGregor and contributors",
        author_email = "alice+marrow@gothcandy.com",
        url = "http://www.marrowproject.com/render",
        download_url = "http://cheeseshop.python.org/pypi/marrow.render/",
        license = "MIT",
        keywords = '',
        
        install_requires = [],
        
        test_suite = 'nose.collector',
        tests_require = [
                'nose',
                'coverage',
                'Genshi',
                'Mako',
                'PyYAML'
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
        
        packages = find_packages(exclude=['examples', 'tests', 'tests.*', 'docs']),
        include_package_data = True,
        zip_safe = True,
        
        namespace_packages = [
                'marrow',
                'marrow.render',
                'marrow.render.serialize',
                'marrow.render.template',
                'alacarte',
                'alacarte.serialize',
                'alacarte.template',
                'cti',
                'cti.serializers',
                'cti.templating'
            ],
        
        entry_points = {
                'marrow.render': [
                        'json = marrow.render.serialize.json_:render',
                        'bencode = marrow.render.serialize.bencode:render',
                        'yaml = marrow.render.serialize.yaml_:render',
                        'pickle = marrow.render.serialize.pickle_:render_pickle',
                        'cpickle = marrow.render.serialize.pickle_:render_cpickle',
                        'marshal = marrow.render.serialize.marshal_:render',
                        
                        'sprintf = marrow.render.template.sprintf:SprintfEngine',
                        'formatter = marrow.render.template.formatter:FormatterEngine',
                        'template = marrow.render.template.template:render',
                        
                        'genshi = marrow.render.template.genshi_:Genshi',
                        'jinja2 = marrow.render.template.jinja2_:Jinja2',
                        'mako = marrow.render.template.mako_:Mako',
                        'cheetah = marrow.render.template.cheetah_:Cheetah',
                    ]
            }
    )
