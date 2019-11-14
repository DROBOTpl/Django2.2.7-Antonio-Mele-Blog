# Antonio Mele | Django 2 - blog
> Książka Antonio Mele pod tytułem "Django 2 - praktyczne tworzenie aplikacji sieciowych."
> Przepracowana dla wersji Django 2.2.7 w Pythonie 3.5.4

### Rozdział 1 - Utworzenie aplikacji bloga

##### 1.1 Instalowanie Django 
```pip install Django==2.2.7```

Wersję django w konsoli Pythona sprawdzam poleceniem:

```
>>> import django
>>> django.get_version()
```

##### 1.2 Tworzenie pierwszego projektu
`django-admin startproject mysite .`

###### Utworzenie aplikacji
```
py manage.py startapp blog
py manage.py migrate
```

##### 1.3 Projekt Schematu danych dla bloga
> Model to klasa Pythona która (podklasa klasy django.db.models.Model).  
> Django tworzy tabelę dla każdego modelu zdefiniowanego w pliku _models.py_  
> Każdy atrybut tej klasy reprezentuje pole bazy danych  
- Definiuję model Post w _models.py_ 
- aktywuję aplikację w _settings.py_
- `py manage.py makemigrations blog`
- aby przyjrzeć się kodowi SQL wykonam: `py manage.py sqlmigrate blog 0001`
- `py manage.py migrate`

> jeśli zmodyfikuję istniejące pole lub dodam nowe muszę ponownie zastosować makemigrations i migrate

##### 1.4 Tworzenie witryny administracyjnej dla Modeli
> Django ma wbudowany interfejs admina, jest on podpięty w INSTALLED_APPS jako django.contrib.admin, można go tam odkomentować jeśli nie używany

- `py manage.py createsuperuser`
- aby dodać model Post do panelu admina rejestruję go w _admin.py_, potem personalizuję jego wyświetlanie

##### 1.5 Praca z obiektami QuerySet i menedżerami

> QuerySet - wbudowany w Django interfejs API do abstrakcji baz danych. Mechanizm mapowania relacyjno-obiektowego  
> https://docs.djangoproject.com/en/3.0/ref/models/

uruchamianie shella  
`py manage.py shell`  
aby shell działał w PyCharm dodaję w Python Console najpierw wszystkie linijki z pliku wsgi.py:
```
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()
```

###### Tworzenie obiektów
```
from django.contrib.auth.models import User
from blog.models import Post
```

- Tworzenie obiektu za pomocą instrukcji SQL Insert
> Metoda get() pobiera pojedyńczy obiekt z db. Jeżeli obiekt nie istnieje, zwróci wyjątek **DoesNotExist**,
>a jeśli db zwróci więcej niż jeden wynik to da wyjątek **MultipleObjectsReturned**

```
# pobieram obiekt user którego pole 'username' to 'drobot', przypisuję go do zmiennej
user = User.objects.get(username='drobot')

# tworzę egzemplarz klasy Post z wypełnionymi polami, jako autora ustalam użytkownika którego wcześniej pobrałem  
post = Post(title = 'inny post', slug = 'inny-post', body = 'inna treść', author = user)

# utrwalam w db
post.save()
```

- Tworzenie i utrwalenie w db obiektu za pomocą funkcji **create()**  
`Post.objects.create(title='create post', slug='create-post', body='one more post', author=user)`

###### Aktualizowanie obiektów
```
post.title = 'inny się zmienia'
post.save()
```

###### Pobieranie obiektów
> za pomocą get() pobieram 1 obiekt, za pomocą all() wszystkie
- tworzę obiekt który będzie zwracał wszystkie obiekty Post
`all_posts = Post.objects.all()`

- do filtrowania obiektów używam metody **filter()** można filtrować wg wielu pól jednocześnie, można też łączyć kilka filtrów
```
Post.objects.filter(publish__year=2019)
Post.objects.filter(title='Mario Pizza')
Post.objects.filter(publish__year=2019, title='Mario Pizza')
Post.objects.filter(publish__year=2019).filter(author__username='drobot')
```

- metoda **exclude()** pozwala wykluczać wyniki z kwerendy
`Post.objects.filter(publish__year=2019).exclude(title__startswith='Mario')`

- metoda order_by() porządkuje wyniki wg różnych pól
```
Post.objects.order_by('title')
Post.objects.order_by('-title')
```
 
 ###### Usuwanie obiektów
 ```
post = Post.objects.get(id=1)
post.delete()
```

 ###### Tworzenie menedżerów obiektów
 
 > objects - to domyślny menedżer każdego modelu, który pobiera wszystkie obiekty z db.
 - w pliku _models.py_ utworzę własnego menedżera do pobierania wszystkich postów których stan jest określony jako published
