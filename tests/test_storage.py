import unittest
import tempfile
import shutil
import os
from datetime import datetime
from fixercise.storage import *

import tests.testutils as testutils


class TestStorage(unittest.TestCase):

    def setUp(self):
        # Temporary location to write files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Delete temporary files
        shutil.rmtree(self.test_dir)

    def test_store_and_retrieve_rates(self):

        # Specific date
        specific_date = datetime(2017, 1, 1)
        specific_iso_date = specific_date.strftime('%Y-%m-%d')

        # Mock JSON
        rates = testutils.get_specific_date_data(datetime(2017, 1, 1))

        # Store and retrieve
        store_rates(rates, self.test_dir)
        retrieved_rates = retrieve_rates(specific_iso_date, self.test_dir)

        self.assertDictEqual(rates, retrieved_rates,
                             "Stored rates must equal retrieved rates")

    def test_repeat_store_data(self):
        # Get two rates that aren't deeply equal
        # The timestamp will be different, but they'll
        # write to the same location on disk
        date_1 = datetime(2017, 1, 2, 10)   # A Monday
        date_2 = datetime(2017, 1, 2, 11)   # The same Monday

        # Get a third rate which gets written to a different location on disk
        date_3 = datetime(2017, 1, 3, 11)   # A Tuesday

        rates_1 = testutils.get_specific_date_data(date_1)
        store_rates(rates_1, self.test_dir)

        # Count and compare files
        files = os.listdir(self.test_dir)

        self.assertTrue(files, "There should be files in the directory")
        self.assertEqual(1, len(files),
                         "There should be one file in the directory")

        rates_2 = testutils.get_specific_date_data(date_2)
        store_rates(rates_2, self.test_dir)

        files = os.listdir(self.test_dir)
        self.assertEqual(1, len(files),
                         "there should be one file in the directory")

        rates_3 = testutils.get_specific_date_data(date_3)
        store_rates(rates_3, self.test_dir)

        files = os.listdir(self.test_dir)
        self.assertEqual(2, len(files),
                         "there should be two files in the directory")

    def test_weekend_exception(self):
        pass


