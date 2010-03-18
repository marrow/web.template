#!/usr/bin/env python
# encoding: utf-8

import sys, os

try:
    from distribute_setup import use_setuptools
    use_setuptools()

except ImportError:
    pass

from setuptools import setup, find_packages

if sys.version_info < (2, 5):
    raise SystemExit("Python 2.5 or later is required as 2.4 support requires too much cruft. -- BDFL")

execfile(os.path.join("alacarte", "release.py"))


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
                'Genshi',
                'Mako',
                # 'TurboCheetah',
                'PyYAML'
            ],
        
        classifiers = [
                "Development Status :: 4 - Beta",
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
                'alacarte',
                'alacarte.serialize',
                'alacarte.template',
                'cti',
                'cti.serializers',
                'cti.templating'
            ],
        
        entry_points = {
                'alacarte': [
                        'json = alacarte.serialize.json_:render',
                        'bencode = alacarte.serialize.bencode:render',
                        'yaml = alacarte.serialize.yaml_:render',
                        'pickle = alacarte.serialize.pickle_:render_pickle',
                        'cpickle = alacarte.serialize.pickle_:render_cpickle',
                        'marshal = alacarte.serialize.marshal_:render',
                        
                        'sprintf = alacarte.template.sprintf:render',
                        'formatter = alacarte.template.formatter:FormatterEngine',
                        'template = alacarte.template.template:render',
                        
                        'genshi = alacarte.template.genshi_:Genshi',
                        'jinja2 = alacarte.template.jinja2_:Jinja2',
                        'mako = alacarte.template.mako_:Mako',
                        'cheetah = alacarte.template.cheetah_:Cheetah',
                    ]
            }
    )
