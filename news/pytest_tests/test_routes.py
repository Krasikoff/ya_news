from pytest_django.asserts import assertRedirects
from http import HTTPStatus
import pytest 
from pytest import lazy_fixture 
from django.urls import reverse

#Главная страница доступна анонимному пользователю.
#Страница отдельной новости доступна анонимному пользователю.
#Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.(анониму в том числе)
@pytest.mark.parametrize(
    'name, args', 
    (
        ('news:home', None) ,
        ('users:login',  None),
        ('users:logout', None), 
        ('users:signup', None),
        ('news:detail', lazy_fixture('pk_for_args')),
    )
)
@pytest.mark.django_db
def test_home_availability_for_anonymous_user(client, name, args):
    # Адрес страницы получаем через reverse():
    url = reverse(name, args = args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK 

#Страницы удаления и редактирования комментария доступны автору комментария.

@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('notes:edit', 'notes:delete'),
)
def test_pages_availability_for_author(parametrized_client, name, comment, expected_status):
    url = reverse(name, args=(pk_for_args_comment,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status



#При попытке перейти на страницу редактирования или удаления комментария анонимный пользователь перенаправляется на страницу авторизации.
#Авторизованный пользователь не может зайти на страницы редактирования или удаления чужих комментариев (возвращается ошибка 404).