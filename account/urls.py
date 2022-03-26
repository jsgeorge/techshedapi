from django.urls import path
from .views import *

urlpatterns = [
    path('signin', signin_view, name="login"),
    path('signup', signup_view, name="reg"),
    path('signout', signout_view, name="signout"),
    path('profile', profile_view, name="profile"),
    path('emailmsg', send_contact_email, name="sendcontactemail")
]