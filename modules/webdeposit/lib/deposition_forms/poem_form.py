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
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA

from wtforms.validators import Required
from invenio.webinterface_handler_flask_utils import _
from invenio.webdeposit_form import WebDepositForm as Form
from invenio.webdeposit_field_widgets import bootstrap_submit

# Import custom fields
from invenio.webdeposit_load_fields import fields

__all__ = ['PoemForm']


class PoemForm(Form):

    title = fields.TitleField(label=_('Poem Title'), validators=[Required()])
    author = fields.AuthorField(label=_('Author'), validators=[Required()])
    languages = [("en", _("English")),
                ("fre", _("French")),
                ("ger", _("German")),
                ("dut", _("Dutch")),
                ("ita", _("Italian")),
                ("spa", _("Spanish")),
                ("por", _("Portuguese")),
                ("gre", _("Greek")),
                ("slo", _("Slovak")),
                ("cze", _("Czech")),
                ("hun", _("Hungarian")),
                ("pol", _("Polish")),
                ("nor", _("Norwegian")),
                ("swe", _("Swedish")),
                ("fin", _("Finnish")),
                ("rus", _("Russian"))]
    language = fields.LanguageField(label=_('Language'), choices=languages,
                                    validators=[Required()])
    year = fields.Date(label=_('Year'), validators=[Required()])
    poem_text = fields.AbstractField(label='Poem Text', validators=[Required()])
    submit = fields.SubmitField(label=_('Submit Poem'),
                         widget=bootstrap_submit)

    """ Form Configuration variables """
    _title = _('Submit a Poem')
    _drafting = True   # enable and disable drafting
