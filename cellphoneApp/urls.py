from django.contrib import admin
from django.urls import path
from . import views
# các URL khác cho chức năng thêm, xóa, sửa và tìm kiếm sản phẩm
from django.urls import path,include

urlpatterns = [
    path('oke', views.hello , name = 'index'),
    path('getcolor',views.get_color_names, name='index'),
    # path('Smartphone/<int:branch_id>/', views.get_products, name='smartphone_list'),
    path('branch/<int:branch_id>/', views.get_products, name='smartphone_list'),
    path('branch/<int:branch_id>/product/<int:product_id>/', views.get_detail_product, name='smartphone_detail')

]