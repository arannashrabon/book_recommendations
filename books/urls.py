from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<str:book_id>/", views.details, name="details"),
    path("review/", views.review_profile, name="review_profile"),
    path("review/<str:book_id>/", views.review, name="review"),
    path("bookmark/", views.bookmarks_profile, name="bookmark_profile"),
    path("bookmark/<str:book_id>/", views.bookmark, name="bookmark"),
    path(
        "remove_bookmark/<str:book_id>/", views.remove_bookmark, name="remove_bookmark"
    ),
    path(
        "reading_history_profile/",
        views.reading_history_profile,
        name="reading_history_profile",
    ),
    path("signup/", views.register, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
