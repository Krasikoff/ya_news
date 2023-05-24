import pytest
from datetime import datetime, timedelta
# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment

@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def author_client(author, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(author)  # Логиним автора в клиенте.
    return client

@pytest.fixture
def news(author):
    news = News.objects.create(title='Заголовок', text='Текст') 
    return news

@pytest.fixture
def pk_for_args(news):  
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return news.id,

#@pytest.fixture
#def news(author):
#    today = datetime.today()
#    news = News.objects.bulk_create(
#    News(title=f'Новость {index}', 
#         text='Просто текст.',
#         date=today - timedelta(days=index),
#         )
#            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
#        ) 
#    return news

#        comment = Comment.objects.create(
#            news=cls.news,
#            author=cls.author,
#            text='Текст комментария'
