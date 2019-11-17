from  django.urls import path
from . import  views

# definiuję przestrzeń nazw, będę mógł odwoływać się do modułu za pomocą nazwy
app_name = 'blog'

urlpatterns = [
    # widoki posta
    path('', views.post_list, name='post_list'),

    # do przechwytywania wartości z adresu URL używamy < >
    # ten url pobiera 4 argumenty i jest mapowany na widok
    path(' /<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]
