import pytest
import pdb
from django.conf import settings
from django.urls import reverse
#Количество новостей на главной странице — не более 10.
@pytest.mark.parametrize(
    # В качестве параметров передаем name и args для reverse.
    'name, args',
    (
        ('news:home', None),
    )
)
@pytest.mark.usefixtures('news_page') 
def test_news_count(client, name, args):
        # Загружаем главную страницу.
    url = reverse(name, args = args)
    response = client.get(url)
        #pdb.set_trace()
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
    object_list = response.context['object_list']
       # Определяем длину списка.
    news_count = len(object_list)
        # Проверяем, что на странице именно 10 новостей.
    assert(news_count == settings.NEWS_COUNT_ON_HOME_PAGE) 

#Новости отсортированы от самой свежей к самой старой. Свежие новости в начале списка.
@pytest.mark.parametrize(
    # В качестве параметров передаем name и args для reverse.
    'name, args',
    (
        ('news:home', None),
    )
)
@pytest.mark.usefixtures('news_page')
def test_news_order(client, name, args):
    url = reverse(name, args = args)
    response = client.get(url)
    object_list = response.context['object_list']
        # Получаем дату первой новости.
    first_news_date = object_list[0].date
        # Получаем список всех дат новостей на странице.
    all_dates = [news.date for news in object_list]
        # Проверяем, что у первой новости - самое большое значение даты.
    assert(first_news_date == max(all_dates)) 

#Комментарии на странице отдельной новости отсортированы в хронологическом порядке: старые в начале списка, новые — в конце.
@pytest.mark.parametrize(
    # В качестве параметров передаем name и args для reverse.
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
@pytest.mark.usefixtures('couple_of_comments')
def test_comments_order(client, name, args):
    url = reverse(name, args = args)
    response = client.get(url)
        # Проверяем, что объект новости находится в словаре контекста
        # под ожидаемым именем - названием модели.
    assert(('news'in response.context) == True)
        # Получаем объект новости.
    news = response.context['news']
        # Получаем все комментарии к новости.
    all_comments = news.comment_set.all()
        # Проверяем, что время создания первого комментария в списке
        # меньше, чем время создания второго.
    assert(all_comments[0].created < all_comments[1].created) 

#Анонимному пользователю недоступна форма для отправки комментария на странице отдельной новости, а авторизованному доступна.
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('admin_client'), True)
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
def test_anonymous_client_has_no_form(parametrized_client, name, args, expected_status):
    url = reverse(name, args = args)
    response = response = parametrized_client.get(url)
    assert(('form' in response.context) == expected_status)
