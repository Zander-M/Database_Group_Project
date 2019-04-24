# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: April, 25, 2019
# Title: Authentication File

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, usr_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from AMS.db import get_db

bp = Blueprint('auth',__name__, url_prefix="/auth")