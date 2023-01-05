from django.urls import path
from example import views


urlpatterns = [
    path('', views.hello_world, name='main_page'),
    path('menu/<path:item>', views.walk_menu),
    path('example/', views.walk_menu, name='example')
]
