from typing import Any
from django.db import IntegrityError, transaction
from django.db.models import Avg,QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response


from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer, ReviewSerializer
from .services import user_has_purchased

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'updated_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet[Product]:
        """GET: список відгуків про товар. POST: створити один (тільки для покупців, один раз)."""
        return (
            Product.objects.all()
            .select_related('category')
            .annotate(avg_rating=Avg('reviews__rating'))
            .order_by('-created_at')
        )
    @action(detail=True, methods=['get', 'post'], url_path='reviews', serializer_class=ReviewSerializer)
    def review(self, request: Request, pk:Any=None) -> Response:
        product = self.get_object()
        if request.method == 'GET':
            page = self.paginate_queryset(product.reviews.select_related('user'))
            serialize = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serialize.data)

        if not user_has_purchased(request.user, product):
            raise PermissionDenied('You cfn review only products you have purchased')
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save(user=request.user, product=product)
        except IntegrityError:
            raise ValidationError('You have already reviewed this product.')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

