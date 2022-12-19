from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  #tránh nhầm vs view của store
from django.views.generic import FormView

app_name = 'store'
urlpatterns = [
    #home
    path('', views.index, name="home"), #url 'store:home'
    
    #account
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="home/accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='store:home'), name='logout'),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    
    #cart
    path('cart/', views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('<int:pID>', views.product_detail_view, name="product_detail"),#view_product_detail
    path('author/<int:auID>', views.author_detail_view, name="author_detail"),#view_author_detail

    
    # checkout
    path('checkout/', views.checkout, name="checkout"),
    path('checkout_submit/', views.checkout_submit, name='checkout_submit'),
    
    #other
    path('comment/<int:oID>', views.order_comment, name='order_comment'),
    path('checkout_info/', views.checkout_info_view, name='checkout_info'),
    path('checkout_detail/<int:iID>', views.view_checkout_detail, name='checkout_detail'),
]