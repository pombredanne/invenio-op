# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.ext.registry import AutoDiscoverRegistry, AutoDiscoverSubRegistry, \
        PkgResourcesDiscoverRegistry, RegistryProxy
from invenio.utils.datastructures import LazyDict

jsonext = RegistryProxy('jsonext', AutoDiscoverRegistry, 'jsonext')

fields_definitions = RegistryProxy('jsonext.fields', PkgResourcesDiscoverRegistry, 'fields', registry_namespace=jsonext)
models_definitions = RegistryProxy('jsonext.models', PkgResourcesDiscoverRegistry, 'models', registry_namespace=jsonext)

parsers = RegistryProxy('jsonext.parsers', AutoDiscoverSubRegistry, 'parsers', registry_namespace=jsonext)

function_proxy = RegistryProxy('jsonext.functions', AutoDiscoverSubRegistry, 'functions', registry_namespace=jsonext)
functions = LazyDict(lambda: dict((module.__name__.split('.')[-1],
    getattr(module, module.__name__.split('.')[-1], ''))
    for module in function_proxy))

producers_proxy = RegistryProxy('jsonext.producers', AutoDiscoverSubRegistry, 'producers', registry_namespace=jsonext)
producers = LazyDict(lambda: dict((module.__name__.split('.')[-1], module.produce)
        for module in producers_proxy))

readers_proxy = RegistryProxy('jsonext.readers', AutoDiscoverSubRegistry, 'readers', registry_namespace=jsonext)
readers = LazyDict(lambda: dict((module.reader.__master_format__, module.reader)
        for module in readers_proxy))
