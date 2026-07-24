from rest_framework import serializers
from .models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=True
    )
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'category',
            'image', 'stock', 'avg_rating', 'created_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email', read_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']