# Antonio Mele | Django 2 - blog
> Książka Antonio Mele pod tytułem "Django 2 - praktyczne tworzenie aplikacji sieciowych."
> Przepracowana dla wersji Django 2.2.7 w Pythonie 3.5.4


## Rozdział 1 - Utworzenie aplikacji bloga

#### 1.1 Instalowanie Django 
```pip install Django==2.2.7```

Wersję django w konsoli Pythona sprawdzam poleceniem:

```
>>> import django
>>> django.get_version()
```

<hr>

#### 1.2 Tworzenie pierwszego projektu
`django-admin startproject mysite .`

###### Utworzenie aplikacji
```
py manage.py startapp blog
py manage.py migrate
```

<hr>

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

<hr>

#### 1.4 Tworzenie witryny administracyjnej dla Modeli
> Django ma wbudowany interfejs admina, jest on podpięty w INSTALLED_APPS jako django.contrib.admin, można go tam odkomentować jeśli nie używany

- `py manage.py createsuperuser`
- aby dodać model Post do panelu admina rejestruję go w _admin.py_, potem personalizuję jego wyświetlanie

<hr>

#### 1.5 Praca z obiektami QuerySet i menedżerami

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

##### Tworzenie obiektów
```
from django.contrib.auth.models import User
from blog.models import Post
```

- Tworzenie obiektu za pomocą instrukcji SQL Insert
> Metoda get() pobiera pojedynczy obiekt z db. Jeżeli obiekt nie istnieje, zwróci wyjątek **DoesNotExist**,
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

##### Aktualizowanie obiektów
```
post.title = 'inny się zmienia'
post.save()
```

##### Pobieranie obiektów
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
 
 ##### Usuwanie obiektów
 ```
post = Post.objects.get(id=1)
post.delete()
```

 ##### Tworzenie menedżerów obiektów
 
 > objects - to domyślny menedżer każdego modelu, który pobiera wszystkie obiekty z db.
 - w pliku _models.py_ utworzę własnego menedżera do pobierania wszystkich postów których stan jest określony jako published

<hr>

#### 1.6 Przygotowanie widoków listy i szczegółów
> Widok to funkcja Pythona, która otrzymuje żądanie sieciowe i udziela na nie odpowiedzi.
>Wewnątrz tej funkcji znajduje się logika odpowiedzialna za zwrot żądanej odpowiedzi.
 
##### Tworzenie widoków listy i szczegółów
 - tworzę widoki post_list i post_detail w _blog/views.py_

##### Dodanie wzorców adresów URL do widoków
> wzorce adresów URL mapują URL na widoki
- tworzę plik _blog/urls.py_ i definiuję wzorce URL w funkcji **path()**
- dołączam wzorce adresów pliku _blog/urls.py_ w głównym _urls.py_ przy pomocy funkcji **include()**

##### Kanoniczne adresu URL dla modeli
> Konwencja Django polega na dodaniu metody **get_absolute_url()** do modelu zwracającego kanoniczny adres URL obiektu.
> W tej metodzie wykorzystujemy funkcję **reverse()** tworzącą URL na podstawie nazwy i parametrów opcjonalnych.

- edytuję _models.py_ dodając metodę **get_absolute_url()**

<hr>

#### 1.7 Utworzenie szablonów dla widoków
- tworzę szablony - bazowy, listy postów i szczegółów posta

<hr>

#### 1.8 Dodanie stronicowania
> Django ma wbudowane klasy stronicowania, sposób działania mechanizmu:
> 1. Tworzy egzemplarz klasy Paginator, wraz z liczbą obiektów do wyświetlenia na stronie  
> 2. Pobiera parametr GET.page wskazujący numer bieżącej strony  
> 3. metoda page() klasy Paginator pobiera obiekty dla danej strony  
> 4. dodanie except, czyli co robić jeśli parametr nie jest liczbą całkowitą lub ma wartość większą niż numer ostatniej strony wyników  
> 5. Przekazanie numerów stron i pobranych obiektów do szablonu

- edytuję _views.py_ dodając klasy stronicowania
- tworzę szablon _pagination.html_
- edytuję _blog/list.html_ i dodaję w nim _pagination.html_

<hr>

#### 1.8 Użycie widoków opartych na klasach
> Widoki oparte na klasach są innym sposobem implementacji widoków jako obiektów Pythona.  
> Widok to funkcja otrzymująca żądanie sieciowe i zwracająca odpowiedź, można więc zdefiniować widok jako metodę klasy.  
> Django oferuje klasy widoku bazowego dziedziczące po klasie **View**  
> https://docs.djangoproject.com/en/2.2/topics/class-based-views/

- zmieniam widok **post_list** na widok oparty na klasie, zmieniam też patch w _urls.py_ i link do paginacji w _list.html_

<hr>

## Rozdział 2 - Usprawnienie bloga za pomocą funkcji zaawansowanych

<hr>

#### 2.1 Współdzielenie postów przy użyciu wiadomości email

##### Tworzenie formularzy w Django
> Django ma wbudowany framework formularzy ułatwiający ich tworzenie.
> Django dostarcza dwie klasy bazowe do tworzenia formularzy:  
> - **Form** (do standardowych formularzy)  
> - **ModelForm** (do budowania form, za pomocą których będą tworzone lub uaktualniane egzemplarze modelu)

- tworzę plik _blog/forms.py_ w którym generuję formularz dziedziczący po klasie bazowej **Form**
- robię widok do obsługi formularza w  _views.py_

##### Wysyłanie wiadomości e-mail w Django

- w settings.py dodaję konfigurację konta mailowego SMTP z którego Django wysyła maile
- edytuję views.py  dodając widok formularza z wysyłaniem wiadomości email
- dodaję ścieżkę patch() w _urls.py_
- tworzę templatkę _blog/templates/blog/post/share.html_
- dodaję link w  _blog/templates/blog/post/detail.html_
- dodaję też css

<hr>


