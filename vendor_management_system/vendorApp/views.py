from django.utils import timezone
from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def perform_create(self, serializer):
        serializer.save()

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        if serializer.validated_data['status'] == 'completed':
            serializer.instance.vendor.quality_rating_avg = serializer.instance.calculate_quality_rating_avg()
            serializer.instance.vendor.save()

    def perform_update(self, serializer):
        serializer.save()
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'completed':
            serializer.instance.vendor.quality_rating_avg = serializer.instance.calculate_quality_rating_avg()
            serializer.instance.vendor.fulfillment_rate = serializer.instance.calculate_fulfillment_rate()
            serializer.instance.vendor.save()

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    http_method_names = ['patch']

    def perform_update(self, serializer):
        serializer.save(acknowledgment_date=timezone.now())
        serializer.instance.vendor.average_response_time = serializer.instance.calculate_average_response_time()
        serializer.instance.vendor.save()

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'
