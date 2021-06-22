from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from planbapi.models import *


class VendorViewSet(ViewSet):
    def list(self, request):
        """Handle GET requests to vendors resource
        Returns:
            Response -- JSON serialized list of vendors
        """
        vendors = Vendor.objects.all()

        # Support filtering vendors
        vendor = self.request.query_params.get('vendorId', None)
        if vendor is not None:
            vendors = vendors.filter(
                vendor__id=vendor).order_by('business_name')

        serializer = VendorSerializer(
            vendors, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single vendor
        Returns:
            Response -- JSON serialized vendor instance
        """
        try:
            vendor = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(vendor, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class VendorSerializer(serializers.ModelSerializer):
    """JSON serializer for vendors

    Arguments:serializer type """
    class Meta:
        model = Vendor
        fields = ('id', 'business_name', 'about', 'category',
                  'phone', 'address', 'city', 'state')
        depth = 1
