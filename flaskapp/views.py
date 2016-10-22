# -*- encoding: utf-8 -*-

import os
import random
import sys
import tempfile

from flask import abort, render_template, send_file

from flaskapp import app, forms

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from specktre import generate_squares, generate_triangles, generate_hexagons
from specktre import Color, save_speckled_wallpaper, Settings

SHAPE_TO_GENERATOR = {
    'squares': generate_squares,
    'triangles': generate_triangles,
    'hexagons': generate_hexagons,
}


def hex_to_rgb(hex_str):
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    if len(hex_str) == 3:
        hex_str = hex_str[0] * 2 + hex_str[1] * 2 + hex_str[2] * 2
    red = int(hex_str[0:2], base=16)
    green = int(hex_str[2:4], base=16)
    blue = int(hex_str[4:6], base=16)
    return Color(red, green, blue)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.SpecktreForm()
    
    errors = []
    shape_url = None
    if form.validate_on_submit():
        path = os.path.join(
            'tmp', os.path.basename(
                tempfile.mkstemp(prefix='specktre_', suffix='.png')[1]
            )
        )
        settings = Settings(
            generator=SHAPE_TO_GENERATOR[form.shape.data],
            width=form.width.data,
            height=form.height.data,
            start_color=hex_to_rgb(form.colorA.data),
            end_color=hex_to_rgb(form.colorB.data),
            name=path,
        )
        os.makedirs('tmp', exist_ok=True)
        save_speckled_wallpaper(settings)
        shape_url = os.path.basename(path)
        print('Form validated successfully!')
    else:
        errors.extend(form.shape.errors)
        errors.extend(form.colorA.errors)
        errors.extend(form.colorB.errors)
        errors.extend(form.width.errors)
        errors.extend(form.height.errors)
    
    return render_template(
        'index.html',
        form=form,
        shape_url=shape_url,
        errors=errors,
    )


@app.errorhandler(404)
def missing_image(e):
    return render_template('404.html')


@app.route('/render/<filename>')
def display_image(filename):
    if not os.path.exists(os.path.join('tmp', filename)):
        abort(404)
    return send_file(os.path.join('..', 'tmp', filename))
    
    
@app.route('/background')
def background():
    img = random.choice([l for l in os.listdir('flaskapp/static') if l.endswith('.png')])
    return send_file(os.path.join('static', img))
