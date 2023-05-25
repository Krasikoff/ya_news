import pytest
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta
from news.models import News, Comment
from django.utils import timezone

@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def reader(django_user_model):  
    return django_user_model.objects.create(username='НеАвтор')

@pytest.fixture
def author_client(author, client):
    client.force_login(author)  
    return client

@pytest.fixture
def reader_client(reader, client): 
    client.force_login(reader)  
    return client

@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок', 
        text='Текст',) 
    return news

@pytest.fixture
def pk_for_args(news):  
    return (news.id,)

@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment

@pytest.fixture
def pk_for_args_comment(comment):  
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
    for index in range(2):
        comment = Comment.objects.create(
        news=news, 
        author=author,
        text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return couple_of_comments

@pytest.fixture
def form_data(author, news):
    return {
        'text': 'Новый текст',
    }
