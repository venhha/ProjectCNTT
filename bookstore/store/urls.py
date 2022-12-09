from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  #tránh nhầm vs view của store

app_name = 'store'
urlpatterns = [

    path('', views.store, name="store"), #url 'store:store'
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update"),

    # login handle
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="store/pages/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='store:store'), name='logout'),
    
    # checkout
    path('place/', views.placeOrder, name='place'),

]
