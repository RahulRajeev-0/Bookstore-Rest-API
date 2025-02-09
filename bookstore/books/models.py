from django.db import models
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    biography = models.TextField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# separate manager for avoiding soft delete books 
class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True) # length of isbn no is 13 
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    description = models.TextField()
    publisher = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author) # many to many = sometimes (multiple author write a book and book have multiple authors)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp of deletion

    objects = BookManager()  # Custom manager to exclude deleted books
    all_objects = models.Manager() 

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """ Soft delete the book instead of permanently deleting it. """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    
    def restore(self):
        """ Restore a soft-deleted book. """
        self.is_deleted = False
        self.deleted_at = None
        self.save()



    

