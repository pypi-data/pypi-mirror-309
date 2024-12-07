import unittest
from datetime_helper import DateUtils

class TestDateUtils(unittest.TestCase):
    def test_format_date(self):
        self.assertEqual(DateUtils.format_date("2024-11-20", "dd-MM-yyyy"), "20-11-2024")

    def test_convert_timezone(self):
        result = DateUtils.convert_timezone("2024-11-20 10:00:00", "UTC", "Asia/Kolkata")
        self.assertIsNotNone(result)

    def test_add_time(self):
        result = DateUtils.add_time("2024-11-20", days=7)
        self.assertEqual(result.strftime("%Y-%m-%d"), "2024-11-27")

if __name__ == "__main__":
    unittest.main()
