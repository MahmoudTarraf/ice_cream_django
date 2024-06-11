from django.urls import path
from . import views
urlpatterns = [
    path('login',views.login),
    path('login_admin',views.login_admin),
    path('signup',views.signup),
    path('getuser/<str:identifier>',views.get_user),
    path('changeusername/',views.change_username),
    path('changeemail/',views.change_email),
    path('changephonenumber/',views.change_phoneNumber),
]
