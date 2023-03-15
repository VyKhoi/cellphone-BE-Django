from django.contrib import admin
from django.urls import path
from . import views
# các URL khác cho chức năng thêm, xóa, sửa và tìm kiếm sản phẩm
from django.urls import path,include

urlpatterns = [
    path('oke', views.hello , name = 'index'),
    path('getcolor',views.get_color_names, name='index'),
    # path('Smartphone/<int:branch_id>/', views.get_products, name='smartphone_list'),
    path('branch/<int:branch_id>/phones', views.get_products_phones, name='smartphone_list'),
    path('branch/<int:branch_id>/product/<int:product_id>/type/<int:type_of_product>', views.get_detail_product, name='smartphone_detail'),
    path('branch/<int:branch_id>/laptops', views.get_products_laptop, name='laptop_list'),
    path('comments/<int:id_product>', views.get_comments_product,name='smartphone_comments'),

    #tra cuu don hoang
    path('order_lookup/<str:deliveryPhone>/', views.get_order_lockup, name='order_lockup'),

    path('branch/<int:branch_id>/total-phones', views.get_products_phones_all, name='phones-list'),
    path('branch/<int:branch_id>/total-laptops', views.get_products_laptops_all, name='phones-list'),
]