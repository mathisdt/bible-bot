from os.path import isfile
from config import Config
import verse
import csv

config = Config("global")

books_filename = 'data/books.csv'
books_filename_with_language = f"data/books_de.csv"
if isfile(books_filename_with_language):
    books_filename = books_filename_with_language

with open(books_filename, newline='') as books_file:
    books_reader = csv.reader(books_file, delimiter=',')
    # skip header row:
    next(books_reader)
    for books_row in books_reader:
        book_number = int(books_row[0])
        book_abbreviation = books_row[1]
        book_name = books_row[2]
        book_chapter_count = int(books_row[3])
        for chapter_number in range(1, book_chapter_count):
            chapter_verse_count = None
            with open('data/chapters.csv', newline='') as chapters_file:
                chapters_reader = csv.reader(chapters_file, delimiter=',')
                # skip header row:
                next(chapters_reader)
                for chapters_row in chapters_reader:
                    if int(chapters_row[0]) == book_number and int(chapters_row[1]) == chapter_number:
                        chapter_verse_count = int(chapters_row[2])
                        break
            if chapter_verse_count is None:
                raise Exception(f"chapter not found: {book_name} (BookNumber={book_number}) {chapter_number}")

            for translation_abbreviation in verse._get_translations(config):
                filename = f"{config.text_directory}/{translation_abbreviation}-{str(book_number).zfill(2)}-{book_abbreviation}{chapter_number}.txt"
                if not isfile(filename):
                    filename = f"{config.text_directory}/{translation_abbreviation}-{str(book_number).zfill(2)}-{book_abbreviation}.txt"
                if not isfile(filename):
                    raise Exception(f"file {filename} not found, neither with chapter {chapter_number} nor without")
                with open(filename, newline='') as chapter_file:
                    lines = chapter_file.read().splitlines()
                    if not len(lines) == chapter_verse_count:
                        print(f"*** {translation_abbreviation}: {book_abbreviation} {chapter_number} does not have {chapter_verse_count} verses but {len(lines)}")
                    #else:
                    #    print(f"    {translation_abbreviation}: {book_abbreviation} {chapter_number} has {chapter_verse_count} verses")
