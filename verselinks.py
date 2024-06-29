from random import randint
from os.path import isfile
from re import sub
import csv
from config import Config


def get_message():
    config = Config("global")
    translations = _get_translations(config)
    verse_location = _get_random_verse_location(config.language)

    result = f"{verse_location[0]} {verse_location[2]}, {verse_location[3]}"
    for translation in translations:
        result += f"\n\n{translations[translation]}: {_get_link(config.bible_url_template, str(translation), str(verse_location[1]), str(verse_location[2]), str(verse_location[3]))}"

    return result


def _get_link(template: str, translation: str, book: str, chapter: str, verse: str):
    result = sub(r'\{translation}', translation, template)
    result = sub(r'\{book}', book, result)
    result = sub(r'\{chapter}', chapter, result)
    result = sub(r'\{verse}', verse, result)
    return result


def _get_random_verse_location(language: str):
    book_id = randint(1, 66)

    books_filename = 'data/books.csv'
    books_filename_with_language = f"data/books_{language}.csv"
    if isfile(books_filename_with_language):
        books_filename = books_filename_with_language

    book_abbreviation = None
    book_name = None
    book_chapter_count = None
    with open(books_filename, newline='') as books_file:
        books_reader = csv.reader(books_file, delimiter=',')
        # skip header row:
        next(books_reader)
        for books_row in books_reader:
            if int(books_row[0]) == book_id:
                book_abbreviation = books_row[1]
                book_name = books_row[2]
                book_chapter_count = int(books_row[3])
                break
    if book_abbreviation is None or book_name is None or book_chapter_count is None:
        raise Exception("book not found")
    chapter_number = randint(1, book_chapter_count)

    chapter_verse_count = None
    with open('data/chapters.csv', newline='') as chapters_file:
        chapters_reader = csv.reader(chapters_file, delimiter=',')
        # skip header row:
        next(chapters_reader)
        for chapters_row in chapters_reader:
            if int(chapters_row[0]) == book_id and int(chapters_row[1]) == chapter_number:
                chapter_verse_count = int(chapters_row[2])
                break
    if chapter_verse_count is None:
        raise Exception("chapter not found")
    verse_number = randint(1, chapter_verse_count)

    return [book_name, book_abbreviation, chapter_number, verse_number]


def _get_translations(config: Config):
    translations = dict()
    abbreviations_and_names = config.translations.split("|")
    for abbreviation_and_name in abbreviations_and_names:
        abbreviation_and_name_split = abbreviation_and_name.split("=")
        translations[abbreviation_and_name_split[0].strip()] = abbreviation_and_name_split[1].strip()
    return translations
