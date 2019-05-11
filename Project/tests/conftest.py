import os
import tempfile

import pytest
from AMS import create_app
from AMS.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql= f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING':True,
        'DATABASE':db_path
    })

    with app.app_context():
        init_db()
        cursor = get_db().cursor()
        queries = str(_data_sql).split(';')[:-1]
        for query in queries:
            cursor.execute(query)
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init___(self,client):
        self._cliend = client
    
    def login(self, username='test', password="test"):
        return self._client.post('/auth/login/a')