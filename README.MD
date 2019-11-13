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