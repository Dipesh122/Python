from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('number/<int:id>', views.number),
    path('index/', views.template_test),
    path('movies/<int:id>', views.get_movie_info),
    path('movies/', views.get_movies),
    path('post_movie/', views.post_movie),
    path('signin/',views.signin),

    path('add_to_favorite/<int:id>',
    views.add_to_favorite,
    name="Add to favorite"),
    path('remove_from_favorite/<int:id>',
    views.remove_from_favorites,name="Remove from favorite"),
    path('user_fav/',views.get_user_favorites),

]
