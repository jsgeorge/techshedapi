"""pythonauto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from account.views import (signin_view, signup_view, signout_view,
#                            profile_view)
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from autos.serializers import *
from autos.views import(
    AutoViewSetREST,
    #AutoSearchViewSetREST,
    AutoCategoryViewSetREST,
    AutoMakeViewSetREST,
    FeaturdAutoViewSetREST,
    LatestAutoViewSetREST,
    CategoryViewSetREST,
    MakeViewSetREST,
    UserViewSetREST,
    OrderViewSetREST,
    FavoriteViewSetREST,
    
)
router = routers.DefaultRouter()
router.register('api/users', UserViewSetREST)
router.register('api/autos', AutoViewSetREST),
router.register('api/autos/<int id>', AutoViewSetREST)
router.register('api/featured', FeaturdAutoViewSetREST)
router.register("api/latest", LatestAutoViewSetREST)
router.register('api/categories', CategoryViewSetREST)
router.register('api/makes', MakeViewSetREST)
router.register('api/filter', AutoCategoryViewSetREST)
router.register('api/filterbymake', AutoMakeViewSetREST)
router.register('api/orders', OrderViewSetREST)
#router.register('api/lookup', AutoSearchViewSetREST)
router.register('api/favorites', FavoriteViewSetREST)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/auth/', obtain_auth_token),
]
