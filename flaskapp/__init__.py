#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'Nothing to do with the secret organisation'

from flaskapp import views