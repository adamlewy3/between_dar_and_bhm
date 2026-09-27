import unittest
import utils
import datetime

class UtilsTest(unittest.TestCase):

    def test_formatted_date_to_datetime_short_month(self):
        exp = datetime.datetime(2026,9,20)
        date = "2026-9-20"
        result = utils.formatted_date_to_datetime(date) 
        self.assertEqual(result, exp)

    def test_formatted_date_to_datetime_short_day(self):
        exp = datetime.datetime(2026,10,9)
        date = "2026-10-9"
        result = utils.formatted_date_to_datetime(date) 
        self.assertEqual(result, exp)

    def test_formatted_date_to_datetime_short_day_and_month(self):
        exp = datetime.datetime(2026,9,9)
        date = "2026-9-9"
        result = utils.formatted_date_to_datetime(date) 
        self.assertEqual(result, exp)

    def test_get_delay_same_day_late(self):
        time1 = "1020"
        time2 = "1030"

        result = utils.get_delay(time1, time2)

        self.assertEqual(result, 10)

    def test_get_delay_same_day_early(self):
        time1 = "1030"
        time2 = "1020"

        result = utils.get_delay(time1, time2)

        self.assertEqual(result, -10)

    def test_get_delay_different_day_late(self):
        time1 = "2359"
        time2 = "0000"

        result = utils.get_delay(time1, time2)

        self.assertEqual(result, 1)


    



if __name__ == '__main__':
    unittest.main()

