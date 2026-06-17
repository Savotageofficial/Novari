from django.urls import path

from novari_base import views



urlpatterns = [
    path("admin/products/<int:id>/", views.AdminProductDeleteView.as_view()),  # 7 , 6
    path("products/", views.ProductListView.as_view()),  # 1
    path("products/<int:id>/", views.ProductDetailView.as_view()),  # 2
    path("admin/login/", views.AdminLoginView.as_view()),  # 3
    path("admin/products/", views.AdminProductsView.as_view()),  # 4, 5
    path("orders/", views.SubmitOrderView.as_view()),  # 10

]