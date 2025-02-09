from rest_framework import serializers
import re

# models
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), 
        many=True, 
        write_only=True, 
        source='authors'
    )

    class Meta:
        model = Book
        fields = '__all__'

    
    def validate_isbn(self, value):
        """
        validating ISBN 
        """
        value = value.replace("-", "").replace(" ", "")
        if not re.match(r'^\d{10}(\d{3})?$', value):
            raise serializers.ValidationError("Invalid ISBN format. ISBN must be 10 or 13 digits.")
        
        # Validate ISBN-10 Checksum
        if len(value) == 10:
            if not self.is_valid_isbn10(value):
                raise serializers.ValidationError("Invalid ISBN-10 checksum.")
        
        # Validate ISBN-13 Checksum
        elif len(value) == 13:
            if not self.is_valid_isbn13(value):
                raise serializers.ValidationError("Invalid ISBN-13 checksum.")
            
        return value
    

    """
    Validate an ISBN-10 number.
    To check if an ISBN-10 is valid:
    1. Calculate the total sum by multiplying each digit (except the last one) by its position (1-9).
    2. Find the remainder of the total sum divided by 11.
    3. The remainder should be equal to the last (check) digit. If the check digit is 'X', it represents the value 10.
    """
    def is_valid_isbn10(self, isbn):
        isbn_body = isbn[:-1]
        total = 0 
        # for calculating the total sum ISBN 10 formula 
        for i, digit in enumerate(isbn_body):
            total += (i + 1) * int(digit)

        check_digit = total % 11 
        return str(check_digit) == isbn[:-1] or (check_digit == 10 and isbn[:-1] == "X")

        
    """
    Validate an ISBN-13 number.
    To check if an ISBN-13 is valid:
    1. Calculate the total sum by multiplying each digit (except the last one) alternatively by 1 and 3.
    2. Find the remainder of the total sum divided by 10.
    3. The remainder should be 0 to indicate a valid ISBN-13.
    4. The check digit is the value needed to make the total sum a multiple of 10.
    """
    def is_valid_isbn13(self, isbn):
        total = 0 
        for i, digit in enumerate(isbn[:-1]):
            if i % 2 == 0 :
                total += 1 * int(digit)
            else:
                total += 3 * int(digit)
        check_digit = (10 - (total % 10)) % 10 
        return str(check_digit) == isbn[-1]
    



    
