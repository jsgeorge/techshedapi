from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('autos', autos_view, name="autos"),
    path('saveautoinquiry', save_auto_inquiry, name="saveautoinq"),
    path('autos/category/<int:id>/<str:name>',
         autos_ctgry_view,
         name="autosctgry"),
    path('search', srch_autos_view, name="searchautos"),
    path('searchhome', srch_autos_home_view, name="searchautoshome"),
    path('autos/<int:id>', auto_detail_view, name="autodetail"),
    path('about', about_view, name="about"),
    path('services', services_view, name="services"),
    path('contacts', contacts_view, name="contacts"),
]
