from django.urls import path
from .views import home_view, signup_view, login_view, logout_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),

]
