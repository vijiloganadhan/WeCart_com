from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name="home"),
    path('products/<int:ids>',views.display_cat,name="products"),
    path('search',views.search,name="search"),
    path('dproducts/<int:ids>',views.display_products,name="dproducts"),
    path('signup/',views.signup_views,name="signup"),
    path('login/',views.login_views,name="login"),
    path('logout',views.logout_views,name="logout"),
    path('addcart/<int:ids>',views.add_cart,name="addcart"),
    path('remove/<int:ids>',views.remove_cart,name="remove"),
    path('display',views.display_cart,name="display"),
    path('buynow/<int:ids>',views.buynow,name="buynow"),
    path('display_order',views.display_order, name="orders"),
    path('delete_order/<int:ids>',views.delete_order,name="delete"),
    path('mail/<int:ids>',views.order_success,name="mail"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)