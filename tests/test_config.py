import unittest

from src.config import MAX_RETRIES, BASE_SLEEP_MULTIPLIER


class TestConfig(unittest.TestCase):
    def test_max_retries_is_positive(self):
        self.assertGreater(MAX_RETRIES, 0)

    def test_base_sleep_multiplier_is_positive(self):
        self.assertGreater(BASE_SLEEP_MULTIPLIER, 0)

    def test_max_retries_is_int(self):
        self.assertIsInstance(MAX_RETRIES, int)

    def test_base_sleep_multiplier_is_int(self):
        self.assertIsInstance(BASE_SLEEP_MULTIPLIER, int)
