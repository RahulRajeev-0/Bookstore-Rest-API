from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    biography = models.TextField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.title





    

