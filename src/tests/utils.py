import os
import unittest
import shutil

from unittest.mock import patch
from sqlalchemy import create_engine
from tempfile import TemporaryDirectory


class TempSQLliteTestCase(unittest.TestCase):
    """
    Base class that has a temporary sqlite db with migrations prerun into it
    """
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = TemporaryDirectory()
        currdir = os.path.split(__file__)[0]
        tmp_db_base = os.path.join(currdir, 'tmp.db')
        shutil.copyfile(tmp_db_base, os.path.join(cls.tmpdir.name, 'tmp.db'))
        cls.conn_string = 'sqlite:////{}/tmp.db'.format(cls.tmpdir.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    @classmethod
    def get_engine(cls):
        return create_engine(cls.conn_string)

    @classmethod
    def create_session(cls):
        from utils import create_session
        return create_session(cls.get_engine())

    def run(self, result=None):
        with patch(target='utils.create_default_engine',
                   new=self.get_engine):
            return super().run(result)