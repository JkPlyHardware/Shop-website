from django.urls import path
from .views import CategoryList, ProductList, ProductDetail, TestimonialList
urlpatterns = [
    path("categories/", CategoryList.as_view(), name="categories"),
    path("products/", ProductList.as_view(), name="products"),
    path("products/<slug:slug>/", ProductDetail.as_view(), name="product-detail"),
    path("testimonials/", TestimonialList.as_view(), name="testimonials"),
]
