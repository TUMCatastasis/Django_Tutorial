from django.urls import path

from tum_meteo_tut import views

urlpatterns = [
    path("tum_meteo_tut/", views.temp_here, name="temp_here"),
    path("tum_meteo_tut/discover", views.temp_somewhere, name="temp_somewhere"),
    path("tum_meteo_tut/search", views.search, name="search"),
    path("tum_meteo_tut/search_internal", views.find_city, name="find_city")
]