from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.data_structures import ProductDataStructure, CategoryDataStructure
from store.models import Product, Category
from store.serializers import ProductSerializer, CategorySerializer
from store.viewset_base import ViewSetBase


class ProductAPI(ViewSetBase):

    def create_product(self, request):
        parameters = self.generate_parameters(request)
        structured_product = ProductDataStructure(**parameters)
        try:
            new_product = Product.objects.create(**structured_product.__dict__)
            new_product.save()
            return Response(ProductSerializer(new_product, many=False, read_only=True).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def get_all_products(request):
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True, read_only=True).data)

    @staticmethod
    def get_category_products(request, category_id):
        if Category.objects.filter(id=category_id).exists():
            products = Product.objects.filter(category_id=category_id)
            return Response(ProductSerializer(products, many=True, read_only=True).data)
        else:
            raise Http404

    @staticmethod
    def get_product_by_id(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return Response(ProductSerializer(product, many=False, read_only=True).data)

    def edit_product(self, request, product_id):
        parameters = self.generate_parameters(request)
        structured_product = ProductDataStructure(**parameters)
        try:
            product = get_object_or_404(Product, id=product_id)
            product.__dict__.update(**structured_product.__dict__)
            if structured_product.__dict__.get('category'):
                product.category = get_object_or_404(Category, id=structured_product.__dict__.get("category").id)
            product.save()
            return Response(ProductSerializer(product, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(ProductAPI, self).get_permissions()


class CategoryAPI(ViewSetBase):
    def create_category(self, request):
        parameters = self.generate_parameters(request)
        structured_category = CategoryDataStructure(**parameters)
        try:
            new_category = Category.objects.create(**structured_category.__dict__)
            new_category.save()
            return Response(CategorySerializer(new_category, many=False, read_only=True).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def edit_category(self, request, category_id):
        parameters = self.generate_parameters(request)
        structured_category = CategoryDataStructure(**parameters)
        category = get_object_or_404(Category, id=category_id)
        try:
            category.__dict__.update(**structured_category.__dict__)
            if structured_category.__dict__.get("parent"):
                category.parent = get_object_or_404(Category, id=structured_category.__dict__.get("parent").id)
            category.save()
            return Response(CategorySerializer(category, many=False, read_only=True).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"status": "failed", "message": str(ex), "parameters": self.generate_parameters(request)},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def get_categories(request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True, read_only=True).data)
