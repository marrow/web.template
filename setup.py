#!/usr/bin/env python
# encoding: utf-8

import sys, os

from setuptools import setup, find_packages


if sys.version_info <= (2, 5):
    raise SystemExit("Python 2.5 or later is required.")

execfile(os.path.join("cti", "release.py"))



setup(
        name = name,
        version = version,
        
        description = summary,
        long_description = description,
        author = author,
        author_email = email,
        url = url,
        download_url = download_url,
        license = license,
        keywords = '',
        
        install_requires = [
            ],
        
        test_suite = 'nose.collector',
        tests_require = [
                'nose',
                'coverage',
                'Genshi'
            ],
        
        classifiers = [
                "Development Status :: 1 - Planning",
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
                'cti',
                'cti.serializers',
                'cti.templating'
            ],
        
        entry_points = {
                'web.templating': [
                        'json = cti.serializers.json_:render',
                        'bencode = cti.serializers.bencode:render',
                        'yaml = cti.serializers.yaml_:render',
                        'pickle = cti.serializers.pickle_:render_pickle',
                        'cpickle = cti.serializers.pickle_:render_cpickle',
                        'marshal = cti.serializers.marshal_:render',
                        
                        'sprintf = cti.templating.sprintf:render',
                        'formatter = cti.templating.formatter:render',
                        'template = cti.templating.template:render',
                        
                        'jinja2 = cti.templating.jinja2_:Jinja2',
                    ]
            }
    )
