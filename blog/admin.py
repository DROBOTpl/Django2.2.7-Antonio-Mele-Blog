from django.contrib import admin
from .models import Post, Comment


# aby zarejestrować model wystarczy
# admin.site.register(Post)


# rejestrowanie modelu przy pomocy niestandardowej klasy dziedziczącej po ModelAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # wyświetlane pola w admin/blog/post
    list_display = ('title', 'slug', 'author', 'publish', 'status')

    # prawy pasek boczny do filtrowania wybranych
    list_filter = ('status', 'created', 'publish', 'author')

    # wyszukiwarka która wyszukuje tylko w zaznaczonych polach
    search_fields = ('title', 'body')

    # auto wypełnianie pola 'slug' względem pola 'title'
    prepopulated_fields = {'slug': ('title',)}

    # wyszukiwarka użytkownika (widget) przy dodawaniu rekordu w /admin/blog/post/add/
    raw_id_fields = ('author',)

    # fajne - górny pasek z filtrem wg. daty dodania
    date_hierarchy = 'publish'

    # sortowanie domyślne wg. kolumn
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'body', 'post', 'created', 'active',)
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
