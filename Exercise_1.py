import json
from pprint import pprint # pretty print

with open('books.json', 'r') as file:
    books = json.load(file)


def get_statistics(books: list) -> dict:
    author_stats = {}
    # iterate over every entry in the books dictionary
    for book in books:
        author = book["author"]

    # create empty author_stats dictionary with all wanted statistics for each author
        if not author in author_stats:
            author_stats[author] = {
                "total_pages": 0,
                "total_chapters": 0,
                "titles": [],
                "publication_dates": []
            }

    # get statistics to fill empty dictionary
        author_stats[author]["total_pages"] += book["total_pages"]
        author_stats[author]["total_chapters"] += book["chapter_count"]
        author_stats[author]["titles"].append(book["title"])
        author_stats[author]["publication_dates"].append(book["publication_date"])

    # compute publication_period for each author and delete  publication_dates
    for author in author_stats:
        author_stats[author]["publication_period"] = [
            min(author_stats[author]["publication_dates"]),
            max(author_stats[author]["publication_dates"])
        ]
        del author_stats[author]["publication_dates"]

    # compute average_chapters_per_book for each author and delete total_chapters
    for author in author_stats:
        author_stats[author]["average_chapters_per_book"] = author_stats[author]["total_chapters"] / len(
            author_stats[author]["titles"])

        del author_stats[author]["total_chapters"]

    return author_stats

# get list of genres in books without duplicates
def get_genres(books: list) -> list:
    genres = set()
    for book in books:
        genres.add(book["genre"])
    return list(genres)

pprint(get_statistics(books))
pprint(get_genres(books))
