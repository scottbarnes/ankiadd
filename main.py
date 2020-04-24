"""
Create Anki decks of Python methods from the Python documentation website.
"""
from bs4 import BeautifulSoup
from typing import Tuple, List, Iterable
import genanki
import random
import requests


# Scott uses the requests module to fetch the html.
def get_html(url: str) -> requests.models.Response:
    """ Get the page html. """
    html = requests.get(url)
    return html


# He notices it's been converted into a BeautifulSoup object
def get_soup(html: requests.models.Response) -> BeautifulSoup:
    """ Create the soup. """
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


# He notices BeautifulSoup has parsed out the first string method name
def get_method_name(soup: BeautifulSoup) -> str:
    """ For a given class="method" in the soup, return the method_name() """
    result = soup.dt.get_text().lstrip('\n')
    result = result.rstrip('Â¶')
    return result


# And that it can get the body
def get_method_body(soup: BeautifulSoup) -> str:
    """ For a given class=method" in the soup, return the body of the text for this method. """
    # result = soup.get_text()
    # result = result.replace('Â¶', '')  # Clean the anchor link icons.
    # result = result.replace('\n\n', '\n')  # And excess new lines.
    result = soup.prettify()
    result = result.replace('Â¶', '')  # Clean up the anchor icons.
    return result


# And that it can find all methods listed on a page.
def get_methods(soup: BeautifulSoup) -> Iterable[BeautifulSoup]:
    """ Take soup and return a bs4.element.ResultSet """
    result = soup.find_all(class_='method')
    return result


def make_anki_note(question: str, answer: str) -> genanki.note.Note:
    """ Make an Anki note from <question> and <answer>. """
    note = genanki.Note(
        model=genanki_model,
        fields=[question, answer]
    )
    return note


def make_anki_deck(methods: Iterable[BeautifulSoup], title: str) -> genanki.deck.Deck:
    """
    Go through the list provided by get_methods() and:
      - pull out the question and answer (i.e. method name and method body);
      - make a note from the question and answer; and
      - add the question and answer to the deck.
    """
    deck = genanki.Deck(
        # 1882252982,
        random.randrange(1 << 30, 1 << 31),  # I guess this work to give it a unique deck number?
        title,
    )
    for method in methods:
        question = get_method_name(method)
        answer = get_method_body(method)
        note = make_anki_note(question, answer)
        deck.add_note(note)

    return deck


# He then sees it can make a flash card from the soup.
genanki_model = genanki.Model(
    1476131965,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ]
)


html = get_html('https://docs.python.org/3/library/stdtypes.html#string-methods')
soup = get_soup(html)
methods = get_methods(soup)
deck = make_anki_deck(methods, 'String methods')
genanki.Package(deck).write_to_file('output.apkg')

