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

__all__ = ['plugins']

import os
from invenio.config import CFG_PYLIBDIR
from invenio.pluginutils import PluginContainer, \
    create_enhanced_plugin_builder


def dummy_can_preview_signature(f):
        pass


def dummy_preview_signature(f, emb=None):
    pass


preview_plugin_builder = create_enhanced_plugin_builder(
    compulsory_objects={
        'can_preview': dummy_can_preview_signature,
        'preview': dummy_preview_signature,
    },
)


plugins = PluginContainer(
    os.path.join(CFG_PYLIBDIR, 'invenio', 'preview_plugins', 'preview_*.py'),
    plugin_builder=preview_plugin_builder,
)
