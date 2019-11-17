from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Post


# widok listy wszystkich postów
# widok pobiera parametr request który jest wymagany dla wszystkich widoków
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # zmienna oddająca 3 posty na każdej stronie
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # jeżeli zmienna page nie jest liczbą całkowitą wówczas pobierana jest pierwsza strona wyników
        posts = paginator.page(1)
    except EmptyPage:
        # jeśli zmienna page ma wartość większą niż numer ostatniej strony
        # wyników, wtedy pobierana jest ostatnia strona wyników
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


# widok pojedynczego posta
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
