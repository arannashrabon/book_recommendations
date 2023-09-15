from django.contrib.auth.models import User
from django.db import models


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Favorite(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.username} - favorite"


class Bookmark(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.username} - bookmark"


class History(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book_id = models.CharField(max_length=50)
    read_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} - history"


class Review(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book_id = models.CharField(max_length=50)
    review_count = models.IntegerField(default=0)
    comment = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.username} - review"
