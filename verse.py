import logging
from random import randint
from os.path import isfile
from re import sub
import csv
from config import Config


def get_message():
    config = Config("global")
    translations = _get_translations(config)
    verse_location = None
    verse_text = None
    while not verse_location and (not config.text_directory or not verse_text):
        try:
            verse_location = _get_random_verse_location(config.language)
            verse_text = _get_verse_text(config.text_directory, next(iter(translations)),
                                         str(verse_location["book_number"]), str(verse_location["book_abbreviation"]),
                                         str(verse_location["chapter"]), verse_location["verse"])
        except:
            # just retry, some verses may not be in the translation which is configured
            verse_location = None
            verse_text = None

    result = "" if not verse_text else f"{verse_text}\n\n"
    result += f'{verse_location["book_name"]} {verse_location["chapter"]}, {verse_location["verse"]}'
    for translation in translations:
        link = _get_link(config.bible_url_template, str(translation), str(verse_location["book_abbreviation"]),
                         str(verse_location["chapter"]), str(verse_location["verse"]))
        result += f'\n\n{translations[translation] + ": " if translations[translation] else ""}{link}'

    return result


def _get_verse_text(text_directory: str, translation_abbreviation: str, book_number: str, book_abbreviation: str,
                    chapter: str, verse: int):
    if not (text_directory and translation_abbreviation and book_number and book_abbreviation and chapter and verse):
        raise Exception(f"not all required parameters given: text_directory={text_directory} translation_abbreviation={translation_abbreviation} book_number={book_number} book_abbreviation={book_abbreviation} chapter={chapter} verse={verse}")
    filename = f"{text_directory}/{translation_abbreviation}-{book_number.zfill(2)}-{book_abbreviation}{chapter}.txt"
    if not isfile(filename):
        filename = f"{text_directory}/{translation_abbreviation}-{book_number.zfill(2)}-{book_abbreviation}.txt"
    if not isfile(filename):
        logging.log(logging.ERROR, f"file {filename} not found, neither with chapter {chapter} nor without")
        raise Exception(f"file {filename} not found, neither with chapter {chapter} nor without")
    with open(filename, newline='') as chapter_file:
        lines = chapter_file.read().splitlines()
        if len(lines) < verse - 1:
            logging.log(logging.ERROR,
                        f"{translation_abbreviation}: {book_abbreviation} {chapter} does not have verse {verse}")
            raise Exception(f"{translation_abbreviation}: {book_abbreviation} {chapter} does not have verse {verse}")
        return lines[verse - 1]


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
                book_number = books_row[0]
                book_abbreviation = books_row[1]
                book_name = books_row[2]
                book_chapter_count = int(books_row[3])
                break
    if book_number is None or book_abbreviation is None or book_name is None or book_chapter_count is None:
        raise Exception(f"book not found: ID={book_id}")
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
        raise Exception(f"chapter not found: {book_name} (BookID={book_id}) {chapter_number}")
    verse_number = randint(1, chapter_verse_count)

    return {
        "book_number": int(book_number),
        "book_abbreviation": book_abbreviation,
        "book_name": book_name,
        "chapter": chapter_number,
        "verse": verse_number
    }


def _get_translations(config: Config):
    translations = dict()
    abbreviations_and_names = config.translations.split("|")
    for abbreviation_and_name in abbreviations_and_names:
        if "=" in abbreviation_and_name:
            abbreviation_and_name_split = abbreviation_and_name.split("=")
            translations[abbreviation_and_name_split[0].strip()] = abbreviation_and_name_split[1].strip()
        else:
            translations[abbreviation_and_name.strip()] = None
    return translations
