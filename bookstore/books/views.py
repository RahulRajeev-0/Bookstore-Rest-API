from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
   
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
       


class CustomPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = "page_size"  # Allow client to request more data
    max_page_size = 50  # Prevent excessive data load


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Enable Filtering by author, genre, and publication_date
    filterset_fields = ['authors', 'genre', 'publication_date']

    # Enable Search (title, description, publisher)
    search_fields = ['title', 'description', 'publisher']

    # Enable Ordering (default: by title)
    ordering_fields = ['title', 'publication_date', 'price']
    ordering = ['title']
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()

    