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

SUBDIRS = deposition_forms deposition_fields deposition_types

pylibdir = $(libdir)/python/invenio

pylib_DATA = __init__.py \
             webdeposit_api_blueprint.py \
             webdeposit_api_regression_tests.py \
             webdeposit_autocomplete_utils.py \
             webdeposit_blueprint.py \
             webdeposit_field.py \
             webdeposit_field_widgets.py \
             webdeposit_filter_utils.py \
             webdeposit_form.py \
             webdeposit_form_unit_tests.py \
             webdeposit_load_deposition_types.py \
             webdeposit_load_fields.py \
             webdeposit_load_forms.py \
             webdeposit_models.py \
             webdeposit_processor_utils.py \
             webdeposit_recordhelpers.py \
             webdeposit_recordhelpers_unit_tests.py \
             webdeposit_regression_tests.py \
             webdeposit_restapi.py \
             webdeposit_signals.py \
             webdeposit_storage.py \
             webdeposit_validation_utils.py \
             webdeposit_workflow_tasks.py

jsdir=$(localstatedir)/www/js

js_DATA = webdeposit_form.js \
          webdeposit_templates.js

EXTRA_DIST = $(pylib_DATA) \
             $(js_DATA)

CLEANFILES = *~ *.tmp *.pyc
