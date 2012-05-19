# encoding: utf-8

"""Release information about marrow.templating."""

from collections import namedtuple


__all__ = ['version_info', 'version', 'copyright']


version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(1, 0, 2, 'final', 1)

version = ".".join([str(i) for i in version_info[:3]]) + ((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')

copyright = "2009-2012, Alice Bevan-McGregor and contributors"
