# -*- encoding: utf-8 -*-

import string

from flask_wtf import Form
from wtforms import IntegerField, SelectField, TextField
from wtforms.validators import DataRequired, ValidationError


def validate_hex(form, field):
    data = field.data
    
    error = ValidationError('%r is not a valid hex color')
    
    # Strip a leading # for the hex number
    if data.startswith('#'):
        data = data[1:]
    
    if len(data) not in (3, 6):
        raise error
    
    if any(c not in string.hexdigits for c in data):
        raise error


def _validate_size(value, dim_name):
    if value <= 0:
        raise ValidationError(
            '%s must be a positive integer.' % dim_name.title()
        )
    elif value > 3000:
        raise ValidationError(
            'For %ss greater than 3000, use the command-line tool: '
            '<a href="https://github.com/alexwlchan/specktre">github.com/alexwlchan/specktre</a>' % dim_name
        )


def validate_width(form, field):
    _validate_size(field.data, 'width')


def validate_height(form, field):
    _validate_size(field.data, 'height')


class SpecktreForm(Form):
    """Form for getting options for Specktre."""
    colorA = TextField('color A', validators=[DataRequired(), validate_hex])
    colorB = TextField('color B', validators=[DataRequired(), validate_hex])
    width = IntegerField(
        'width',
        validators=[DataRequired(), validate_width]
    )
    height = IntegerField(
        'height',
        validators=[DataRequired(), validate_height]
    )
    shape = SelectField(
        'shape',
        validators=[DataRequired()],
        choices=[(k, k) for k in ('triangles', 'hexagons', 'squares')]
    )
    size_class = SelectField(
        'size_class',
        validators=[DataRequired()],
        choices=[
            ('custom', 'custom'),
            ('iphone5', 'iPhone 5, 5C, 5S, SE'),
            ('iphone6', 'iPhone 6, 7'),
            ('iphone6p', 'iPhone 6, 7 Plus'),
            ('ipad', 'iPad'),
        ]
    )
