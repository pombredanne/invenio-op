# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2012, 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from werkzeug import MultiDict
import json
from wtforms.widgets import html_params, HTMLString, RadioInput, HiddenInput, \
    Input
from invenio.jinja2utils import render_template_to_string


def date_widget(field, **kwargs):
    field_id = kwargs.pop('id', field.id)
    html = [u'<input class="datepicker" %s type="text">'
            % html_params(id=field_id, name=field_id, value=field.data or '')]
    field_class = kwargs.pop('class', '') or kwargs.pop('class_', '')
    kwargs['class'] = u'datepicker %s' % field_class
    kwargs['class'] = u'date %s' % field_class
    return HTMLString(u''.join(html))


def bootstrap_submit(field, **dummy_kwargs):
    html = u'<input %s >' % html_params(style="float:right; width: 250px;",
                                        id="submitButton",
                                        class_="btn btn-primary btn-large",
                                        name="submitButton",
                                        type="submit",
                                        value=field.label.text,)
    html = [u'<div style="float:right;" >' + html + u'</div>']
    return HTMLString(u''.join(html))


class PLUploadWidget(object):
    def __init__(self, template=None):
        self.template = template or "webdeposit_widget_plupload.html"

    def __call__(self, field, **kwargs):
        field_id = kwargs.pop('id', field.id)
        kwargs['class'] = u'plupload'

        return HTMLString(
            render_template_to_string(
                self.template,
                field=field,
                field_id=field_id,
                **kwargs
            )
        )

plupload_widget = PLUploadWidget()


class CKEditorWidget(object):
    """
    Create a CKEditor widget with possible custom configuration
    """
    def __init__(self, **kwargs):
        self.config = json.dumps(kwargs) if kwargs else None

    def __call__(self, field, **kwargs):
        attrs = {
            'data-ckeditor': 1,
        }
        if self.config:
            attrs['data-ckeditor-config'] = self.config

        html = [u'<textarea %s >' % html_params(
            id=field.name,
            name=field.name,
            value=field.data or '',
            **attrs
        )]
        html.append('%s</textarea>' % field.data or '')
        return HTMLString(u''.join(html))

ckeditor_widget = CKEditorWidget()
"""
Default CKEditor widget. Will use the configuration defined globally in Invenio.
"""


def dropbox_widget(field, **kwargs):
    field_id = kwargs.pop('id', field.id)
    html = [u'<input type="dropbox-chooser"\
            name="fileurl"\
            style="visibility: hidden;"\
            data-link-type="direct"\
            id="db-chooser"/></br> \
        <div class="pluploader" %s > \
            <table id="file-table" class="table table-striped table-bordered" style="display:none;">\
                <thead>\
                    <tr>\
                    <th>Filename</th>\
                    <th>Size</th>\
                    <th>Status</th>\
                    <td></td>\
                    </tr>\
                </thead>\
                <tbody id="filelist">\
                </tbody>\
            </table>\
            <a class="btn btn-success disabled" id="uploadfiles"> \
                <i class="icon-upload icon-white"></i> Start upload</a>\
            <a class="btn btn-danger" id="stopupload" style="display:none;">\
                <i class="icon-stop icon-white"></i> Cancel upload</a>\
            <span id="upload_speed" class="pull-right"></span>\
            <div id="upload-errors"></div>\
        </div>' % html_params(id=field_id)]
    return HTMLString(u''.join(html))


class ButtonWidget(object):
    """
    Renders a button.
    """

    def __init__(self, label="", tooltip=None, icon=None, **kwargs):
        """
        Note, the icons assume use of Twitter Bootstrap,
        Font Awesome or some other icon library, that allows
        inserting icons with a <i>-tag.

        @param tooltip: str, Tooltip text for the button.
        @param icon: str, Name of an icon, e.g. icon-barcode.
        """
        self.icon = icon
        self.label = label
        self.default_params = kwargs
        self.default_params.setdefault('type', 'button')
        if tooltip:
            self.default_params.setdefault('data-toggle', 'tooltip')
            self.default_params.setdefault('title', tooltip)
        super(ButtonWidget, self).__init__()

    def __call__(self, field, **kwargs):
        params = self.default_params.copy()
        params.update(kwargs)
        params.setdefault('id', field.id)
        params['class_'] = params.get('class_', "") + " form-button"

        icon = ""
        if self.icon:
            icon = '<i class="%s"></i> ' % self.icon

        state = ""
        if field._value():
            state = '<span class="text-success"> <i class="icon-ok"></i></span>'

        return HTMLString(u'<button %s>%s%s</button><span %s>%s</span>' % (
            html_params(name=field.name, **params),
            icon,
            self.label,
            html_params(id=field.name+'-loader', class_='loader'),
            state,
        ))


class TagInput(Input):
    """
    """
    input_type = 'hidden'

    def __call__(self, field, **kwargs):
        if "__input__" in field.name:
            self.input_type = 'text'
            html = super(TagInput, self).__call__(field, **kwargs)
            self.input_type = 'hidden'
        else:
            return super(TagInput, self).__call__(field, **kwargs)

        return html


#
# Item widgets
#
class ItemWidget(object):
    """
    Widget used render each subfield in a ExtendedListWidget without additional
    markup around the subfield.
    """
    def __call__(self, subfield, **kwargs):
        return subfield()


class ListItemWidget(ItemWidget):
    """
    Widget used render each subfield in a ExtendedListWidget as a list element.
    I.e. as a `li`, `div` or `span` tag.

    If `with_label` is set, the fields label will be rendered. If `prefix_label`
    is set, the label will be prefixed, otherwise it will be suffixed.
    """
    def __init__(self, html_tag='li', with_label=True, prefix_label=True,
                 class_=None):
        assert html_tag in ('li', 'div', 'span', None)
        self.html_tag = html_tag
        self.prefix_label = prefix_label
        self.with_label = with_label
        self.class_ = class_

    def render_subfield(self, subfield, **kwargs):
        if self.with_label:
            if self.prefix_label:
                return '%s: %s' % (subfield.label, subfield())
            else:
                return '%s %s' % (subfield(), subfield.label)
        else:
            return subfield()

    def open_tag(self, subfield, **kwargs):
        if self.html_tag:
            return '<%s %s>' % (
                self.html_tag,
                html_params(class_=self.class_ or kwargs.get('class_', ''))
            )
        return ''

    def close_tag(self, subfield, **kwargs):
        if self.html_tag:
            return '</%s>' % self.html_tag
        return ''

    def __call__(self, subfield, **kwargs):
        html = [self.open_tag(subfield, **kwargs)]
        html.append(self.render_subfield(subfield, **kwargs))
        html.append(self.close_tag(subfield, **kwargs))
        return HTMLString(''.join(html))


class DynamicItemWidget(ListItemWidget):
    """
    Widget used render each subfield in a ExtendedListWidget enclosed in a div
    tag with buttons for sorting and removing the item. I.e. something like:

        <div><span>"buttons</span>:field</div>
    """
    def __init__(self, **kwargs):
        self.icon_reorder = kwargs.pop('icon_reorder', 'icon-reorder')
        self.icon_remove = kwargs.pop('icon_remove', 'icon-remove-sign')
        defaults = dict(
            html_tag='div',
            with_label=True,
        )
        defaults.update(kwargs)
        super(DynamicItemWidget, self).__init__(**defaults)

    def _sort_button(self):
        return """<a class="sort-element muted sortlink iconlink" rel="tooltip" title="Drag to reorder"><i class="%s icon-large"></i></a>""" % self.icon_reorder

    def _remove_button(self):
        return """<a class="remove-element muted iconlink" rel="tooltip" title="Click to remove"><i class="%s icon-large"></i></a>""" % self.icon_remove

    def render_subfield(self, subfield, **kwargs):
        html = []
        # Button
        html.append("<span %s>%s</span>" % (
            html_params(class_='pull-right'),
            self._sort_button() + self._remove_button()
        ))
        # Field
        html.append(subfield())
        return ''.join(html)

    def __call__(self, subfield, **kwargs):
        kwargs.setdefault('id', 'element-' + subfield.id)
        # Are we rendering an empty form element?
        empty_index = kwargs.pop('empty_index', '__index__')
        if subfield.name.endswith(empty_index):
            kwargs['class_'] = kwargs.get('class_', '') + ' empty-element'
        elif subfield.name.endswith('__input__'):
            kwargs['class_'] = kwargs.get('class_', '') + ' input-element'
        else:
            kwargs['class_'] = kwargs.get('class_', '') + ' field-list-element'
        return super(DynamicItemWidget, self).__call__(subfield, **kwargs)


class TagItemWidget(DynamicItemWidget):
    """
    Renders a subfield as an li-element and adds classes to render it as a
    logo.
    """
    def __init__(self, **kwargs):
        self.template = kwargs.pop('template', '')
        defaults = dict(
            html_tag='li',
            with_label=False,
            class_="alert alert-info tag"
        )
        defaults.update(kwargs)

        super(TagItemWidget, self).__init__(**defaults)

    def render_subfield(self, subfield, **kwargs):
        return subfield()

    def open_tag(self, subfield, **kwargs):
        if self.html_tag:
            if subfield.name.endswith('__input__'):
                return '<%s>' % self.html_tag
            else:
                ctx = {}
                if(isinstance(subfield.data, basestring)):
                    ctx['value'] = subfield.data
                elif subfield.data:
                    ctx.update(subfield.data)

                return '<%s %s><button type="button" class="close remove-element" data-dismiss="alert">&times;</button><span class="tag-title">%s</span>' % (
                    self.html_tag,
                    html_params(
                        class_=self.class_ + ' ' + kwargs.get('class_', '')
                    ),
                    render_template_to_string(
                        self.template,
                        _from_string=True,
                        **ctx
                    )
                )
        return ''


#
# List widgets
#
class ExtendedListWidget(object):
    """
    Renders a list of fields as a `ul`, `ol` or `div` list.

    This is used for fields which encapsulate a list of other fields as
    subfields. The widget will try to iterate the field to get access to the
    subfields and call them to render them.

    The `item_widget` decide how subfields are rendered, and usually just
    provide a thin wrapper around the subfields render method. E.g.
    ExtendedListWidget renders the ul-tag, while the ListItemWidget renders each
    li-tag. The content of the li-tag is rendered by the subfield's widget.
    """
    item_widget = ListItemWidget()

    def __init__(self, html_tag='ul', item_widget=None,
                 class_=None):
        assert html_tag in ('ol', 'ul', 'div', None)
        self.html_tag = html_tag
        self.class_ = class_
        if item_widget:
            self.item_widget = item_widget

    def open_tag(self, field, **kwargs):
        if self.html_tag:
            kwargs.setdefault('id', field.id)
            if self.class_:
                kwargs['class_'] = kwargs.get('class_', '') + ' ' + self.class_
            return '<%s %s>' % (self.html_tag, html_params(**kwargs))
        return ''

    def close_tag(self, field, **kwargs):
        if self.html_tag:
            return '</%s>' % self.html_tag
        return ''

    def item_kwargs(self, field, subfield):
        return {}

    def __call__(self, field, **kwargs):
        html = [self.open_tag(field, **kwargs)]
        hidden = []
        for subfield in field:
            if isinstance(subfield.widget, HiddenInput):
                hidden.append(subfield)
            else:
                html.append(
                    self.item_widget(subfield, **self.item_kwargs(field, subfield))
                )
        html.append(self.close_tag(field, **kwargs))
        # Add hidden fields in the end.
        for h in hidden:
            html.append(h())
        return HTMLString(''.join(html))


class DynamicListWidget(ExtendedListWidget):
    """
    Renders a list of fields as a list of divs. Additionally adds:

    * A hidden input to keep track of the last index.
    * An 'add another' item button.

    Each subfield is rendered with DynamicItemWidget, which will add buttons
    for each item to sort and remove the item.
    """
    item_widget = DynamicItemWidget()
    icon_add = "icon-plus"

    def __init__(self, **kwargs):
        self.icon_add = kwargs.pop('icon_add', self.icon_add)
        self.item_widget = kwargs.pop('item_widget', self.item_widget)
        defaults = dict(
            html_tag='div',
            class_='dynamic-field-list',
        )
        defaults.update(kwargs)
        super(DynamicListWidget, self).__init__(**defaults)

    def _add_button(self, field):
        label = getattr(field, 'add_label', None) or "Add %s" % field.label.text
        return """<div><span class="pull-right"><a class="add-element"><i class="%s"></i> %s</a></span></div>""" % (self.icon_add, label)

    def item_kwargs(self, field, subfield):
        return {'empty_index': field.empty_index}

    def open_tag(self, field, **kwargs):
        html = super(DynamicListWidget, self).open_tag(field, **kwargs)
        html += """<input %s>""" % html_params(
            name=field.id + '-__last_index__',
            id=field.id + '-__last_index__',
            type="hidden",
            value=field.last_index,
        )
        return html

    def close_tag(self, field, **kwargs):
        html = self._add_button(field)
        html += super(DynamicListWidget, self).close_tag(field, **kwargs)
        return html


class TagListWidget(DynamicListWidget):
    """
    Renders subfields in a field list in an ul-list with each li-element as
    tags.

    Most useful if subfields are rendered with the TagInput widget.
    """
    def __init__(self, **kwargs):
        self.template = kwargs.pop('template', '{{value}}')
        defaults = dict(
            html_tag='ul',
            class_='dynamic-field-list unstyled',
            item_widget=TagItemWidget(
                template=self.template
            )
        )
        defaults.update(kwargs)
        super(TagListWidget, self).__init__(**defaults)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-tag-template', self.template)
        return super(TagListWidget, self).__call__(field, **kwargs)

    def _add_input_field(self, field):
        subfield = field.bound_field('__input__', force=True )
        subfield.process(MultiDict({}))
        return "<li>%s</li>" % subfield()


    def close_tag(self, field, **kwargs):
        html = []
        # Calling ExtendedListWidget.close_tag on purpose to avoid adding
        # the add-button from DynamicListWidget.
        html.append(self._add_input_field(field))
        html.append(super(DynamicListWidget, self).close_tag(field, **kwargs))
        return HTMLString(''.join(html))

#
# Radio input widgets
#
class BigIconRadioInput(RadioInput):
    """
    Render a single radio button with icon.

    This widget is most commonly used in conjunction with InlineListWidget or
    some other listing, as a single radio button is not very useful.
    """
    input_type = 'radio'

    def __init__(self, icons={}, **kwargs):
        self.choices_icons = icons
        super(BigIconRadioInput, self).__init__(**kwargs)

    def __call__(self, field, **kwargs):
        if field.checked:
            kwargs['checked'] = u'checked'

        html = super(BigIconRadioInput, self).__call__(field, **kwargs)
        icon = self.choices_icons.get(field._value(), '')
        if icon:
            html = """<i class="icon-%s icon-2x"></i><br />%s</br>%s""" % (
                icon, field.label.text, html
            )
        return html


class InlineListWidget(object):
    """
    FIXME: Replace with ExtendedListWidget
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = [u'<ul class="inline">']
        for subfield in field:
            html.append(u'<li class="span1"><label>%s</label></li>' % (subfield()))
        html.append(u'</ul>')
        return HTMLString(u''.join(html))

