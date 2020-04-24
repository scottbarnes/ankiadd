"""
Tests for AnkiAdd
"""
from lxml import html
import requests
from bs4 import BeautifulSoup
import genanki
import unittest
import main


# Scott uses the requests module to fetch the html.
class TestFetchAndParseHtml(unittest.TestCase):
    """ Test out the fetching of the HTML """

    def setUp(self):
        """ Set up the reusable bits for testing. """
        self.url = 'https://docs.python.org/3/library/stdtypes.html#string-methods'
        self.html = main.get_html(self.url)
        self.soup = main.get_soup(self.html)
        self.single_method = self.soup.find(class_='method')  # Returns the first method: int.bit_length()
        self.question = 'What is the capital of Australia?'
        self.answer = 'Canberra'

    def test_fetch_returns_200(self):
        """ Look for a status 200 response in the snarfed page html. """
        self.assertEqual(self.html.status_code, 200)

    def test_for_head_tag_in_soup(self):
        """ Figure out of we have BeautifulSoup by looking for a title tag """
        self.assertIn('<title>'.casefold(), str(self.soup.head))

    def test_get_method_name(self):
        """ Parse out the name of the first method (int.bit_length) and return it """
        method_name = main.get_method_name(self.single_method)
        self.assertEqual('int.bit_length()', method_name)

    def test_get_method_body(self):
        """ Parse out the body of the first method and return it. """
        method_body = main.get_method_body(self.single_method)
        self.assertTrue(method_body.startswith('\nint.bit_length'))
        self.assertTrue(method_body.endswith('New in version 3.1.\n'))

    def test_get_methods(self):
        """ Get the list of methods for a given page. """
        methods = main.get_methods(self.soup)
        self.assertGreaterEqual(len(methods), 100)  # Not the best tests.

    def test_make_anki_note(self):
        """ Check that our note is of the type genanki.note.Note """
        note = main.make_anki_note(self.question, self.answer)
        self.assertIs(type(note), genanki.note.Note)

    def test_make_anki_deck(self):
        """ Check that make_anki_deck returns an Anki deck. """
        methods = main.get_methods(self.soup)
        title = 'String methods'
        deck = main.make_anki_deck(methods, title)
        self.assertIs(type(deck), genanki.deck.Deck)






# Run all classes that inherit from unittest.TestCase
if __name__ == '__main__':
    unittest.main()
