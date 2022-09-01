from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin-page/', views.admin, name='admin'),
    path('cart/', views.view_cart, name='view-cart'),
    path('checkout', views.checkout, name ='checkout'),
    path('cart/<int:product_id>/increment/', views.quantity_increment, name='increment'),
    path('cart/<int:pk>/decrement/', views.quantity_decrement, name='decrement'),
    path('<int:product_id>/', views.remove_product, name='remove-product'),
    path('cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('category/<slug:slug>', views.category_detail, name='category-detail'),
    path('question-and-answer', views.question_answer, name='question-answer'),
    path('create-product', views.create_product, name='new-product'),
    path('delete-product/<str:product_id>', views.delete_product, name='delete-product'),
    path('product/<int:product_id>/edit', views.product_update, name='product-update'),
]


