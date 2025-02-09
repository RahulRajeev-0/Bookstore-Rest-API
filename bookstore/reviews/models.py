from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from books.models import Book

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Authenticated User
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'book')  # Prevents duplicate reviews from the same user

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"
