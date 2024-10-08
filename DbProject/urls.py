from django.contrib import admin
from django.urls import path
from loginreg import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignUpPage,name='signer'),
    path('login/',views.loginpage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.logoutpage,name='logout'),
]
