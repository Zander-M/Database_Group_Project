# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: May, 11, 2019
# Title: Database Functions Testing

"""
    this file contains tests for database
"""

import pymysql
import pytest
from AMS.db import get_db, get_cursor

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with pytest.raises(pymysql.Error) as e:
        db.execute("SELECT 1")
    assert 'closed' in str(e)

def test_init_db():
    Recorder.called = True

monkeypatch.setattr("AMS.db.init_db", fake_init_db)
result = runner.invoke(args=['init-db'])
assert "Initialized" in result.output
assert Recorder.called