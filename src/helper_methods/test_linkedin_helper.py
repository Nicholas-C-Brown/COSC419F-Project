import unittest
from linkedin_helper import validate_url, validate_profile_url


class TestLinkedInHelper(unittest.TestCase):

    def test_validate_url(self):
        url_invalid1 = "linkedin";
        url_invalid2 = "linkedin.com/";
        url_invalid3 = "https://www.linkedin";
        url_invalid4 = "https://www.google.com/";
        url_valid = "https://www.linkedin.com/";

        self.assertFalse(validate_url(url_invalid1));
        self.assertFalse(validate_url(url_invalid2));
        self.assertFalse(validate_url(url_invalid3));
        self.assertFalse(validate_url(url_invalid4));

        self.assertTrue(validate_url(url_valid));


if __name__ == '__main__':
    unittest.main()
