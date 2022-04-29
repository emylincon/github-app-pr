import unittest
import os

# * Set environment variables for testing
os.environ["app_id"] = "test"
os.environ["app_private_key"] = "test"

from app import app

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """:arg
        this runs once at the start of test
        """
        cls.tester = app.test_client(cls)

    @classmethod
    def tearDownClass(cls):
        """:arg
        this runs once after all test is completed
        """
        print("teardownClass")

    def setUp(self):
        """:arg
        this runs before each test
        """
        pass

    def tearDown(self):
        """:arg
        this runs after each test
        """
        pass

    def test_index(self):
        response = self.tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
