from pytest_django.asserts import assertRedirects
from http import HTTPStatus
from pytest_lazyfixture import lazy_fixture
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
#При попытке перейти на страницу редактирования или удаления комментария анонимный пользователь перенаправляется на страницу авторизации.
#Авторизованный пользователь не может зайти на страницы редактирования или удаления чужих комментариев (возвращается ошибка 404).
#Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны анонимным пользователям.