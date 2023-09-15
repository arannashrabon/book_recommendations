from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from books.helpers import book_recommendation, search_book, search_books
from books.models import Bookmark, History, Review


@login_required(login_url="login/")
def index(req) -> HttpResponse:
    recommended_books = book_recommendation()
    if req.method == "POST":
        filter = req.POST["filter"]
        query = req.POST["query"]
        books = search_books(query, filter)
        return render(
            req,
            "index.html",
            {
                "is_authenticated": req.user.is_authenticated,
                "name": req.user.username[:2],
                "books": books,
                "query": query,
                "filter": filter,
                "recommended_books": recommended_books,
            },
        )
    else:
        return render(
            req,
            "index.html",
            {
                "is_authenticated": req.user.is_authenticated,
                "name": req.user.username[:2],
                "recommended_books": recommended_books,
            },
        )


def register(req) -> HttpResponse:
    if req.method == "POST":
        name = req.POST["name"]
        email = req.POST["email"]
        password = req.POST["password"]
        user = User.objects.create_user(name, email, password)
        # user.has_perm('foo.add_bar')
        user.save()
        login_user(req, user)
        return redirect("index")

    return render(req, "signup.html", {"is_authenticated": req.user.is_authenticated})


def login(req) -> HttpResponse:
    if req.method == "POST":
        user = authenticate(
            req, username=req.POST["name"], password=req.POST["password"]
        )
        if user is not None:
            login_user(req, user)
            return redirect("index")
        else:
            # No backend authenticated the credentials
            ...

    return render(req, "login.html", {"is_authenticated": req.user.is_authenticated})


@login_required(login_url="login/")
def logout(request) -> HttpResponse:
    logout_user(request)
    return redirect("login")


@login_required(login_url="login/")
def bookmark(req: HttpRequest, book_id) -> HttpResponse:
    user = req.user
    book = Bookmark.objects.create(user=user, book_id=book_id)
    book.save()
    return JsonResponse({"success": True})


@login_required(login_url="login/")
def remove_bookmark(req: HttpRequest, book_id) -> HttpResponse:
    user = req.user
    book = Bookmark.objects.filter(user=user, book_id=book_id)
    book.delete()
    return redirect("bookmark_profile")


@login_required(login_url="login/")
def bookmarks_profile(req: HttpRequest) -> HttpResponse:
    user = req.user
    book = Bookmark.objects.filter(user=user)
    books = []
    for b in book:
        book = search_book(b.book_id)
        books.append(book)
    return render(
        req,
        "bookmarks.html",
        {
            "success": True,
            "title": "Bookmarks",
            "books": books,
            "is_authenticated": req.user.is_authenticated,
            "name": req.user.username[:2],
        },
    )


@login_required(login_url="login/")
def review_profile(req: HttpRequest) -> HttpResponse:
    user = req.user
    book = Review.objects.filter(user=user)
    books = []
    for b in book:
        book = search_book(b.book_id)
        books.append(book)
    return render(
        req,
        "bookmarks.html",
        {
            "success": True,
            "title": "Reviews",
            "books": books,
            "is_authenticated": req.user.is_authenticated,
            "name": req.user.username[:2],
        },
    )


@login_required(login_url="login/")
def reading_history_profile(req: HttpRequest) -> HttpResponse:
    user = req.user
    book = History.objects.filter(user=user)
    books = []
    for b in book:
        book = search_book(b.book_id)
        books.append(book)
    return render(
        req,
        "bookmarks.html",
        {
            "success": True,
            "title": "Reading History Profile",
            "books": books,
            "is_authenticated": req.user.is_authenticated,
            "name": req.user.username[:2],
        },
    )


@login_required(login_url="login/")
def details(req, book_id) -> HttpResponse:
    user = req.user
    review = None
    try:
        exit = History.objects.get(user=user, book_id=book_id)
        exit.read_count += 1
        exit.save()
    except:
        history = History.objects.create(user=user, book_id=book_id)
        history.save()

    try:
        review = Review.objects.get(user=user, book_id=book_id)
    except:
        print("error")
    print(review)

    book = search_book(book_id)
    return render(
        req,
        "bookDetails.html",
        {
            "book": book,
            "is_authenticated": req.user.is_authenticated,
            "name": req.user.username[:2],
            "review": review,
        },
    )


@login_required(login_url="login/")
def review(req, book_id) -> HttpResponse:
    user = req.user
    try:
        rating_count = 0

        for key in req.POST:
            if key.startswith("rating_") and req.POST[key] == "on":
                rating_count += 1

        exit = Review.objects.get(user=user, book_id=book_id)

        exit.review_count = rating_count
        exit.comment = req.POST["comment"]
        exit.save()

    except Review.DoesNotExist:
        history = Review.objects.create(
            user=user,
            book_id=book_id,
            review_count=rating_count,
            comment=req.POST["comment"],
        )
        history.save()
    book = search_book(book_id)
    return redirect(f"/details/{book_id}")
