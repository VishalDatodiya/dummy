from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from project_module.models import Module
from project_module.apis.serializers import ModuleSerializer

from common.pagination import CustomPagination
from common import responses


class ModuleListView(APIView):
    """
    This APIView class handles GET and POST requests for Module objects, providing pagination and searching for GET requests.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    # Decorator for drf_spectacular(swagger) is used.
    @extend_schema(request=ModuleSerializer,responses=ModuleSerializer(many=True))
    def get(self, request, format=None):
        search_query = request.query_params.get("search", None)
        modules = Module.objects.all().order_by('id')
        if search_query:
            modules = modules.filter(module_name__icontains=search_query)
        
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(modules, request) 
        serializer = ModuleSerializer(result_page, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        return Response(response_data ,status=status.HTTP_200_OK)
    
    @extend_schema(request=ModuleSerializer)
    def post(self, request, format=None):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = responses.success_response(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = responses.failed_response()
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
