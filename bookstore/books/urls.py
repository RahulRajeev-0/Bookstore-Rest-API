from django.urls import path
from . import views

urlpatterns = [
     path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
     
     path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
     path('books/<int:pk>/delete/', views.BookSoftDeleteView.as_view(), name='book-soft-delete'),
     path('books/<int:pk>/restore/', views.BookRestoreView.as_view(), name='book-restore'),
     path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
     path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
