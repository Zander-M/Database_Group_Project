# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Authentication File

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)

from AMS.db import get_db

bp = Blueprint('b_a',__name__, url_prefix="/b_a")