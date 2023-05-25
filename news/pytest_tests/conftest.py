import pytest
import pdb
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta
from news.models import News, Comment
from django.utils import timezone

@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def reader(django_user_model):  
    return django_user_model.objects.create(username='НеАвтор')

@pytest.fixture
def author_client(author, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(author)  # Логиним автора в клиенте.
    return client

@pytest.fixture
def reader_client(reader, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(reader)  # Логиним автора в клиенте.
    return client

@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок', 
        text='Текст',) 
    return news

@pytest.fixture
def pk_for_args(news):  
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.id,)

@pytest.fixture
def urls(news):
    url = reverse('news:detail', pytest.lazy_fixture(news.id))
    url_to_comments = url + '#comments'
    edit_url = reverse('news:edit', args=(news_id,))
    urls = {'url': url, 'url_to_comments':url_to_comments, 'edit_url':edit_url}
    return urls


@pytest.fixture
def comment(author, news):
#    pdb.set_trace()
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment

@pytest.fixture
def pk_for_args_comment(comment):  
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return comment.id,

@pytest.fixture
def news_page(author):
    today = datetime.today()
    news_page = News.objects.bulk_create(
    News(title=f'Новость {index}', 
         text='Просто текст.',
         date=today - timedelta(days=index),
         )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ) 
    return news_page

@pytest.fixture
def couple_of_comments(author, news):
    now = timezone.now()
        # Создаём комментарии в цикле.
    for index in range(2):
        # Создаём объект и записываем его в переменную.
        comment = Comment.objects.create(
        news=news, 
        author=author,
        text=f'Tекст {index}',
        )
            # Сразу после создания меняем время создания комментария.
        
        comment.created = now + timedelta(days=index)
            # И сохраняем эти изменения.
        comment.save()
    return couple_of_comments

@pytest.fixture
def form_data(author, news):
    return {
#        'news'=news,
        'text': 'Новый текст',
#        'author':author
    }
