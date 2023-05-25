from pytest_django.asserts import assertRedirects
from http import HTTPStatus
import pytest
import pdb
#from pytest_lazyfixture import lazy_fixture
from django.urls import reverse

#Главная страница доступна анонимному пользователю.
#Страница отдельной новости доступна анонимному пользователю.
#Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.(анониму в том числе)
@pytest.mark.parametrize(
    'name, args', 
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),    
        ('news:home', None) ,
        ('users:login',  None),
        ('users:logout', None), 
        ('users:signup', None),
    )
)
@pytest.mark.django_db
def test_home_availability_for_anonymous_user(client, name, args):
    # Адрес страницы получаем через reverse():
    url = reverse(name, args = args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK 

#Страницы удаления и редактирования комментария доступны автору комментария.
#Авторизованный пользователь не может зайти на страницы редактирования или удаления чужих комментариев (возвращается ошибка 404).
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
@pytest.mark.django_db
def test_pages_availability_for_author(parametrized_client, name, comment, expected_status):
#    pdb.set_trace()
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status



#При попытке перейти на страницу редактирования или удаления комментария анонимный пользователь перенаправляется на страницу авторизации.
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('pk_for_args_comment')),
        ('news:delete', pytest.lazy_fixture('pk_for_args_comment')),
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
