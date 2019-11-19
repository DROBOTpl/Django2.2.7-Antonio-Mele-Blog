from  django.urls import path
from . import  views

# definiuję przestrzeń nazw, będę mógł odwoływać się do modułu za pomocą nazwy
app_name = 'blog'

urlpatterns = [
    # widoki posta
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),

    # do przechwytywania wartości z adresu URL używamy < >
    # ten url pobiera 4 argumenty i jest mapowany na widok
    path(' /<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),

    # formularz z wysyłaniem wiadomości email
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
