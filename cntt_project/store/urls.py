from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  #tránh nhầm vs view của store
from django.views.generic import FormView

app_name = 'store'
urlpatterns = [
    #home
    path('', views.index, name="home"), #url 'store:home'
    # login handle
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="home/accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='store:home'), name='logout'),
    
    #cart
    path('cart/', views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update"),
    path('<int:pID>', views.product_detail_view, name="product_detail"),#view_product_detail
    
    # checkout
    path('checkout/', views.checkout, name="checkout"),
    path('checkout_submit/', views.checkout_submit, name='checkout_submit'),
    
    #other
    path('comment/', views.comment, name='comment'),
    path('checkout_info/', views.checkout_info_view, name='checkout_info'),
    path('checkout_info/<int:iID>', views.view_checkout_detail, name='checkout_detail'),
]