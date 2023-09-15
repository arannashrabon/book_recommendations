import random
from itertools import chain

import requests

from books.models import Bookmark, History, Review


def search_books(
    query,
    filter="q",
):
    q = query

    if filter == "title":
        q = f"intitle:{query}"
    if filter == "author":
        q = f"inauthor:{query}"
    if filter == "genre":
        q = f"subject:{query}"

    res = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={q}&key=AIzaSyAL1vDBQ5jwGdj5whgjwE1KWNPlMfflMS4"
    )
    data = res.json()

    return data["items"]


def search_book(query):
    res = requests.get(
        f"https://www.googleapis.com/books/v1/volumes/{query}?key=AIzaSyAL1vDBQ5jwGdj5whgjwE1KWNPlMfflMS4"
    )
    data = res.json()
    data["volumeInfo"]["id"] = data["id"]

    return data["volumeInfo"]


def book_recommendation():
    # Sample user behavior data (replace this with your actual data)
    bookmarks = Bookmark.objects.all()
    history = History.objects.all()
    reviews = Review.objects.all()

    # Combine all user behavior into a single list
    user_behavior = list(chain(bookmarks, history, reviews))

    # Filter out books the user has already interacted with
    user_books = set(item.book_id for item in user_behavior)

    temp_books = []

    # Display the recommended books
    for b in user_books:
        temp_books.append(search_book(b))

    random_sample_mystery = search_books("Mystery", filter="genre")
    random_sample_fantasy = search_books("Fantasy", filter="genre")
    random_sample_romance = search_books("Romance", filter="genre")
    random_sample_thriller = search_books("Thriller", filter="genre")
    random_sample_horror = search_books("Horror", filter="genre")
    random_sample_science = search_books("Science", filter="genre")
    random_sample_cookbook = search_books("Cookbook", filter="genre")
    random_sample_poetry = search_books("Poetry", filter="genre")

    # Combine all the lists into one
    all_books = (
        random_sample_mystery
        + random_sample_fantasy
        + random_sample_romance
        + random_sample_thriller
        + random_sample_horror
        + random_sample_science
        + random_sample_cookbook
        + random_sample_poetry
    )

    # Remove duplicates by converting the tuple to a set and then back to a list
    sample = all_books

    final = random.choices(sample, k=10)
    books = []
    for b in final:
        b["volumeInfo"]["id"] = b["id"]
        books.append(b["volumeInfo"])

    return books
