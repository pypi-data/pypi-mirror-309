# tests/test_core.py

import unittest
from textfromimage import TextFromImage
import os


class TestTextFromImage(unittest.TestCase):

    def test_get_description_invalid_url(self):
        """
        Test that providing an invalid image URL raises a ValueError.
        """
        # Initialize with a dummy API key to bypass actual API calls during the test
        text_from_image = TextFromImage(api_key="dummy_api_key")

        with self.assertRaises(ValueError):
            text_from_image.get_description('invalid_url')

    def test_get_description_no_api_key(self):
        """
        Test that omitting the API key raises a ValueError.
        """
        # Backup the original API key if it exists
        original_api_key = os.environ.get('OPENAI_API_KEY')

        try:
            # Temporarily unset the OPENAI_API_KEY environment variable
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']

            with self.assertRaises(ValueError):
                # Initialize without providing an API key; should attempt to read from environment and fail
                text_from_image = TextFromImage()
                text_from_image.get_description('https://example.com/image.jpg')
        finally:
            # Restore the original API key if it was set
            if original_api_key is not None:
                os.environ['OPENAI_API_KEY'] = original_api_key


if __name__ == '__main__':
    unittest.main()
