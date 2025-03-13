from django.urls import path
from .views import home_view, signup_view, login_view, logout_view, post_ad, profile_view, update_profile
from . import views

urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path("post_ad/", post_ad, name="post_ad"),
    path('profile/', profile_view, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),

]
