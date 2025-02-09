from django.urls import path
from . import views

urlpatterns = [
     path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
     path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
]
