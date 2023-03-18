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
    path('branch/<int:branch_id>/product/<int:product_id>/', views.get_detail_product, name='smartphone_detail'),
    path('branch/<int:branch_id>/laptops', views.get_products_laptop, name='laptop_list'),
    path('comments/<int:id_product>', views.get_comments_product,name='smartphone_comments'),

    #tra cuu don hoang
    path('order_lookup/<str:deliveryPhone>/', views.get_order_lockup, name='order_lockup'),

    path('branch/<int:branch_id>/total-phones', views.get_products_phones_all, name='phones-list'),
    path('branch/<int:branch_id>/total-laptops', views.get_products_laptops_all, name='phones-list'),
    #dang ky
    path('register/', views.save_user, name='register_user'),

    path('branch/<int:branch_id>/search/<path:name_product>', views.search, name='search'),
    path('checkout', views.StripeCheckoutView.as_view(), name='checkout'),
    path('checkout2', views.create_payment_intent,name = 'checkout2'),
    path('checkout-succeed', views.order,name = 'order_succeed'),

    path('branch/<int:branch_id>/search-price/<int:from_price>/<int:to_price>/<int:type_product>', views.search_price, name='search_price'),

]