from django.contrib import admin
from django.urls import path
from verification import views
from knox.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account', views.login.as_view()),
    path('verify', views.verify_user.as_view()),
    path('login', views.user_login.as_view()),
    path('logout', LogoutView.as_view()),
]
