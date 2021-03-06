from django.urls import path, include
from accounts import views

urlpatterns = [
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('register/', views.registration, name="registration"),
    path('reset/', include('accounts.url_reset')),
]
