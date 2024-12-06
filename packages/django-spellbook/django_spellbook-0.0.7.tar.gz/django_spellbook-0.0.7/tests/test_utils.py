from django.test import TestCase

from django_spellbook.utils import remove_leading_dash


class TestUtils(TestCase):
    def test_remove_leading_dash(self):
        """Test removing leading dashes from a string"""
        result = remove_leading_dash('--test')
        self.assertEqual(result, 'test')
