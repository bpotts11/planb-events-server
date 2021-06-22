from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from planbapi.models import *


class ProductViewSet(ViewSet):
    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        # Get the current authenticated user
        current_customer_user = self.request.query_params.get('customer', None)
        current_vendor_user = self.request.query_params.get('vendor', None)
        products = Product.objects.all()
        if current_customer_user is not None:
            customer = Customer.objects.get(user=request.auth.user)
        if current_vendor_user is not None:
            vendor = Vendor.objects.get(user=request.auth.user)
            products = Product.objects.filter(vendor=vendor).order_by('name')

        # Support filtering products by user

        # if current_vendor_user is not None:
        #     products = products.filter(user=vendor)

        # if current_customer_user is not None:

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product instance
        """

        # Uses the token passed in the `Authorization` header
        vendor = Vendor.objects.get(user=request.auth.user)

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        product = Product()
        product.vendor = vendor
        product.name = request.data["name"]
        product.price = request.data["price"]
        product.description = request.data["description"]

        try:
            product.save()
            serializer = ProductSerializer(
                product, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)

        product.name = request.data["name"]
        product.price = request.data["price"]
        product.description = request.data["description"]

        try:
            product.save()
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'vendor')
        depth = 1
