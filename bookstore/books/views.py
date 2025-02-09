from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

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
    filter_backends = [DjangoFilterBackend, 
                       filters.SearchFilter, 
                       filters.OrderingFilter]
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



class BookSoftDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        with transaction.atomic():
            book.is_deleted = True
            book.deleted_at = timezone.now()
            book.save()
        return Response(
            {"message": "Book soft deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
            )
    

class BookRestoreView(generics.UpdateAPIView):
    queryset = Book.all_objects.all()  # Get all books, including deleted ones
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """ Restore a soft-deleted book. """
        book = self.get_object()
        if not book.is_deleted:
            return Response(
                {"message": "Book is not deleted"}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        
        with transaction.atomic():
            book.restore()
        return Response(
            {"message": "Book restored successfully"}, 
            status=status.HTTP_200_OK
            )


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        with transaction.atomic():  # Ensures atomicity
            serializer.save()

        return Response(
            {"message": "Book updated successfully", "book": serializer.data},
            status=status.HTTP_200_OK
        )
