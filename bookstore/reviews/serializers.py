from rest_framework import serializers
from .models import Review
from books.models import Book

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # Ensure book exists

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        """ Ensure rating is between 1 and 5 """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
