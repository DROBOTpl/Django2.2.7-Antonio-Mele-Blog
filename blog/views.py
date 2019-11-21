from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from .models import Post, Comment


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posty na każdej stronie
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Jeżeli zmienna page nie jest liczbą całkowitą, wówczas pobierana jest pierwsza strona wyników.
        posts = paginator.page(1)
    except EmptyPage:
        # Jeżeli zmienna page ma wartość większą niż numer ostatniej strony wyników, wtedy pobierana
        # jest ostatnia strona wyników
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


# widok listy wszystkich postów
class PostListView(ListView):

    # zamiast definiować atrybut QuerySet, mogę podać model a Django przygotuje całą kolekcję
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


# widok pojedynczego posta
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # lista aktywnych komentarzy dla danego posta
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # komentarz został opublikowany
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # tworzę obiekt Comment ale jeszcze nie zapisuję go w db
            new_comment = comment_form.save(commit=False)
            # przypisuję komentarz do konkretnego obiektu bieżącego posta
            new_comment.post = post
            # zapisanie komentarza w bazie danych
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})


# widok formularza z wysyłaniem wiadomości email
def post_share(request, post_id):
    # pobranie posta na podstawie jego id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == 'POST':
        # formularz został wysłany
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # weryfikacja pól formularza zakończyła się powodzeniem...
            cd = form.cleaned_data

            # get_absolute_url() pobiera bezwzględną ścieżkę do posta
            # build_absolute_uri() buduje adres URL zawierający schemat HTTP oraz nazwę hosta
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # pobieram temat i treść z formularza
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'\
                .format(post.title, post_url, cd['name'], cd['comments'])
            # wysyłam email przy pomocy funkcji send_mail()
            send_mail(subject, message, 'drobot@myblog.com', [cd['to']])
            # zmienną sent wykorzystam w szablonie do komunikatu 'success'
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
