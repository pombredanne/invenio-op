# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2013 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.


from invenio.bibfield_jsonreader import JsonReader
from invenio.webdeposit_models import DepositionDraft


def record_to_draft(record, draft=None, form_class=None, post_process=None,
                    producer='json_for_form'):
    """
    Load a record into a draft
    """
    if draft is None:
        draft = DepositionDraft(None, form_class=form_class)

    draft.values = getattr(record, 'produce_%s' % producer)()

    if draft.has_form():
        form = draft.get_form()
        form.post_process()
        draft.update(form)

    # Custom post process function
    if post_process:
        draft.values = post_process(draft.values)

    return draft


def drafts_to_record(drafts, post_process=None):
    """
    Export recjson from drafts
    """
    values = DepositionDraft.merge_data(drafts)

    if post_process:
        values = post_process(values)

    return make_record(values)


def deposition_record(record, form_classes, process_load=None,
                      process_export=None):
    """
    Generate recjson representation of a record for this given deposition.
    """
    return drafts_to_record(
        [record_to_draft(record, form_class=cls, post_process=process_load, )
         for cls in form_classes],
        post_process=process_export
    )


def make_record(values):
    """
    Export recjson from drafts
    """
    record = JsonReader()
    for k, v in values.items():
        record[k] = v

    return record
