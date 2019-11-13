from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # klucz główny wygeneruje się automatycznie jako pole id
    # aby go nadpisać muszę dodać do któregoś pola: primary_key = True
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # metadane dla django aby po wysłaniu obiektu do db wyniki sortował malejąco względem pola publish
    class Meta:
        ordering = ('-publish',)
        # w klasie meta mogę też podać własną nazwę tabeli używając db_table

    # metoda str zwraca czytelną reprezentację obiektu
    def __str__(self):
        return self.title
