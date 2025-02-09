from django.db import transaction
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer



class ReviewListCreateView(generics.ListCreateAPIView):
    """ Allows users to list all reviews and add new ones """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """ Ensure a user can only review a book once """
        book = serializer.validated_data['book']
        existing_review = Review.objects.filter(user=self.request.user, book=book).exists()
        if existing_review:
            return Response({"error": "You have already reviewed this book."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            serializer.save(user=self.request.user)



class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve, Update, or Delete a specific review """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_update(self, serializer):
        """ Ensure only the review owner can update the review """
        if self.get_object().user != self.request.user:
            return Response({"error": "You can only edit your own reviews."}, status=status.HTTP_403_FORBIDDEN)
        with transaction.atomic():
            serializer.save()


    def perform_destroy(self, instance):
        """ Ensure only the review owner can delete the review """
        if instance.user != self.request.user:
            return Response({"error": "You can only delete your own reviews."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
