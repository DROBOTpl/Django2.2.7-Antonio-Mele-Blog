from django.shortcuts import render, get_object_or_404
from .models import Post


# widok listy wszystkich postów
# widok pobiera parametr request który jest wymagany dla wszystkich widoków
def post_list(request):
    # pobieram opublikowane posty za pomocą mojego menedżera
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


# widok pojedynczego posta
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post} )

