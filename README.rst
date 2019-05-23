=================
Marrow Templating
=================

    © 2009-2018 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/web.template

..

    |latestversion| |masterstatus| |mastercover| |issuecount|


1. What is Marrow Templating?
=============================

Marrow Templating is an attempt to produce a consistent, universal API for utilizing a variety of template rendering engines and data serialization formats.  Many web frameworks contain their own templating "helpers" which re-implement the same templating glue code over and over again and are often difficult or impossible to extend by non-core developers.

Marrow Templating (formerly alacarte, formerly cti) has been designed to offer the lowest common denominator across engines while not restricting advanced engine capabilities.

There are a wide variety of templating languages available.  In fact, Python seems to collect them.  In general, there is no unified or consistent way to utilize these templating languages.  Due to the learning curve, developers become hesitant to switch from one language to another.  Many templating languages are also poorly documented.

An attempt was made by the TurboGears project to create a unified API called `Buffet <https://web.archive.org/web/20080712004859/http://projects.dowski.com/projects/buffet>`_, used primarily by the CherryPy application server, though in some cases this API is more difficult to use than the raw template language.  Buffet was strongly geared towards one templating engine, Genshi, was tweaked to offer enhanced embedding of alien templating languages within each-other, and was overly complex.  Other frameworks (like Pylons) utilize small helper functions, but require that the framework be updated to extend support to new templating engines.

The onus for ease of deployment should be on the templating engine creator, not the framework creator or front-end web developer.


2. Installation
===============

Installing ``web.template`` is easy, just execute the following in a terminal::

<pre><code>pip install web.template</code></pre>

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`_, others prefer solutions as robust as `Vagrant <http://www.vagrantup.com>`_.

If you add ``web.template`` to the ``install_requires`` argument of the call to ``setup()`` in your applicaiton's ``setup.py`` file, this project will be automatically installed and made available when your own application or library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional side-effects when updating.  Use ``web.template<2.1`` to get all bugfixes for the current release, and ``web.template<3.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.


h3(#install-dev). %2.1.% Development Version

Development takes place on "GitHub":github in the "marrow.templating":github-project project.  Issue tracking, documentation, and downloads are provided there.

Installing the current development version requires "Git":git, a distributed source code management system.  If you have Git, you can run the following to download and _link_ the development version into your Python runtime:

<pre><code>git clone https://github.com/marrow/marrow.templating.git
(cd marrow.mailer; python setup.py develop)</code></pre>

You can upgrade to the latest version at any time:

<pre><code>(cd marrow.templating; git pull; python setup.py develop)</code></pre>

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes, and submit a pull request.  This process is beyond the scope of this documentation; for more information, see "GitHub's documentation":github-help.


[github]https://github.com/
[git]http://git-scm.com/
[github-help]http://help.github.com/



h2(#basic). %3.% Basic Usage

There are a number of ways to utilize Marrow Templating within your own application or framework.  The Engines object an attribute-access dictionary where the dictionary elements are entrypoint-based templating and serialization engines.  Alternatively, a configured Engines object can be called directly as a function and will determine automatically (based on the template path) which engine to utilize.  We will explore the latter option first.

Create a new Engines instance like so:

<pre><code>from marrow.templating.core import Engines
render = Engines(default=None, cache=50, container=None)</code></pre>

The arguments are as follows, and may be specified positionally:

|_. Argument |_. Description |
| @default@ | The default rendering engine to use. |
| @cache@ | The number of template paths (and pre-processed templates) to cache. |
| @container@ | An on-disk path to a folder containing @.egg@ files to use as engines. |

h3(#basic-indirect). %3.1.% Indirect Engine Access

This is the most common way to utilize Marrow Templating:

<pre><code>mime, content = render('pkg.template', dict())</code></pre>

The first argument is a template path specification; for details on the allowed values see "Section 4":#paths of this document.  The second argument is data for the template to consume.  Additional keyword arguments may be provided to pass 'options' to the template engine, such as a preference for a specific version of HTML.

Returned are the MIME type (e.g. "text/plain", "text/html") and the rendered content.


h3(#basic-direct). %3.2.% Direct Engine Access

You can directly access the engines as attribute or dictionary lookups on the Engines instance.  For example:

<pre><code>render.mako(data=data, template=filename)</code></pre>

As per indirect access, additional keyword arguments can be passed as options to the engine.  One very important note, however, is that the template name must be a path to the template on-disk.  Serialization engines do not accept a template argument.  Return values are as per the indirect example.


h2(#paths). %4.% Acceptable Path References

Marrow Templating supports the following template path syntaxes:

* @'engine:package.templates.foo'@ — implicit filename extension, with 'best guess' from a prioritized list of default engines
* @'engine:package.templates/foo.html'@ — explicit file path relative to package

Parts are optional; all of the following are legal:

* @'json:'@ — pure engine, usually a serializer or a template loaded from an existing string
* @'package.templates.foo'@ — defaulting the engine part, implicit filename extension
* @'package/templates/foo.html'@ — defaulting the engine, explicit file path within a package
* @'/var/www/htdocs/index.html'@ — absolute path
* @'./views/edit.html'@ _or_ @'../../templates/master.html'@ — relative paths

Where the path is relative to is up to the framework making use of the template interface, though this defaults to the current working directory.


h2(#extending). %5.% Extending Marrow Templating

Marrow Templating can be extended by the creation of additional templating engine and serialization adapters.  The API for each is quite simple.

h3(#api). %5.1.% Engine API

The registered renderer (engine) callable *must* accept the following named arguments. These arguments are referenced by name but *should* be defined in this order to allow for easy manual use.  Renderers *should* also accept an unlimited list of additional keyword arguments (which *may* be called @options@, as it is with the provided default engines), which are additional values that can be passed in from a combination of a stored configuration and call-time values.

There are several attributes of the engine that are used internally for specific purposes.  All of these attributes are *optional*, and will default to @None@ if not present.

* @mapping@ — a dictionary mapping extensions to content types

The argument specification is as follows, and *may* be implemented as either a class with a @__call__@ attribute or a simple function.

* @data@ — a value for use in the template (usually a dictionary)
* @template@ — an *optional* on-disk absolute path
* @**options@ — additional *optional* keyword arguments

The renderer *must* return a 2-tuple of:

* @None@ or @str@ — content type
* @unicode@ — content


h3(#forms). %5.2.% Engine Forms

An engine *may* be defined as a simple function. Simple functions *must not* store state between calls.  If your template engine needs to keep state (e.g. a cache) then you *must* implement your engine interface as a new-style class.  An example of a simple function:

<pre><code>def helloTemplate(data=dict(name='world'), template=None, **options):
    return 'text/plain', u"Hello %(name)s!" % data</code></pre>

If an engine is a new-style class (that does not subclass _à la carte's_ @Engine@ helper class) initial options are passed to the @__init__@ method (assigned previously to @Engines().options@) with render-time options passed to @__call__@.

If you wish to use the @Engine@ helper class you get template caching and automatic reloading of on-disk templates that are modified between calls.  There are two methods you *must* define in your subclass, and you can override @__init__@ to perform custom initialization, and @__call__@ to override the template generation.

* @prepare(filename, **options)@ — load and return a template object for the cache
* @render(template, data, **options)@ — render and return a finished template

An example of a light-weight wrapper for the Mako templating language is as follows:

<pre><code>class Mako(Engine):
    def load(self, filename, **options):
        return Template(filename=filename)
        
    def render(self, template, data, **options):
        return None, template.render_unicode(**data)</code></pre>


h2(#license). %6.% License

Marrow Templating has been released under the MIT Open Source license.


h3(#license-mit). %6.1.% The MIT License

Copyright (C) 2009-2011 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



fn1. In order to run the full test suite you need to install "pymta":http://www.schwarz.eu/opensource/projects/pymta/ and its dependencies.
