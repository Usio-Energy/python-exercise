import unittest
import tempfile
import shutil
import os
from datetime import datetime, timedelta
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
        specific_date = datetime(2017, 1, 2)  # A Monday, for clarity
        specific_iso_date = specific_date.strftime('%Y-%m-%d')

        # Mock JSON
        rates = testutils.get_specific_date_data(specific_date)

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

        # We now store dates and make sure the ones we have are expected
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
                         "There should be one file in the directory")

        rates_3 = testutils.get_specific_date_data(date_3)
        store_rates(rates_3, self.test_dir)

        files = os.listdir(self.test_dir)
        self.assertEqual(2, len(files),
                         "There should be two files in the directory")

    def test_weekend_exception(self):

        # Get rates from a weekend date
        sunday = datetime(2017, 1, 1)  # A Sunday
        sunday_rates = testutils.get_specific_date_data(sunday)

        with self.assertRaises(WeekendException,
                               msg="""Trying to store weekend rates
                               should throw an exception"""):
            store_rates(sunday_rates, self.test_dir)

    def test_store_month_of_rates(self):
        """This requires some explanation:
            We want to make sure that if we store a month of rates data
            we will actually have all the relevant rates in our store.

            We also want to make sure that we capture all the weekend
            exceptions that get thrown.

            Starting from Jan 2nd, 2017, we play forward for 31 days.
            This includes 23 weekdays and 8 weekend days. We'll check to
            make sure this is what we get.
        """

        # get a range of dates
        dates = []
        first_date = datetime(2017, 1, 2)  # Still a Monday
        for d in range(0, 31):
            dates.append(first_date + timedelta(days=d))

        # Get mock rates data for each date
        month_of_rates = [testutils.get_specific_date_data(d) for d in dates]

        weekend_day_count = 0

        for rates in month_of_rates:
            try:
                store_rates(rates, self.test_dir)
            except WeekendException as e:
                weekend_day_count += 1

        rate_files = os.listdir(self.test_dir)

        self.assertEqual(23, len(rate_files),
                         "There should be 23 weekdays in date range")
        self.assertEqual(8, weekend_day_count,
                         "There should be 8 weekend days in date range")






