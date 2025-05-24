from django.contrib import admin
from django.urls import path
from .views import signup_page, login_page, logout_page
from . import views

app_name = 'accounts'
urlpatterns = [
    path("signup/", signup_page, name="signup"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout")

]
