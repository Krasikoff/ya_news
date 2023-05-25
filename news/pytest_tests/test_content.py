import pytest
import pdb
from django.conf import settings
from django.urls import reverse


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
    )
)
@pytest.mark.usefixtures('news_page') 
def test_news_count(client, name, args):
    '''Количество новостей на главной странице — не более 10.'''
    url = reverse(name, args = args)
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert(news_count == settings.NEWS_COUNT_ON_HOME_PAGE) 

@pytest.mark.parametrize(
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
    first_news_date = object_list[0].date
    all_dates = [news.date for news in object_list]
    assert(first_news_date == max(all_dates)) 

@pytest.mark.parametrize(
    # В качестве параметров передаем name и args для reverse.
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
@pytest.mark.usefixtures('couple_of_comments')
def test_comments_order(client, name, args):
    '''Комментарии на странице отдельной новости отсортированы в 
    хронологическом порядке: старые в начале списка, новые — в конце.'''
    url = reverse(name, args = args)
    response = client.get(url)
    assert(('news'in response.context) == True)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert(all_comments[0].created < all_comments[1].created) 

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
    '''Анонимному пользователю недоступна форма для отправки
    комментария на странице отдельной новости, а авторизованному доступна.'''
    url = reverse(name, args = args)
    response = response = parametrized_client.get(url)
    assert(('form' in response.context) == expected_status)
