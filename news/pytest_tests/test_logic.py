import pytest
import pdb
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING


#Анонимный пользователь не может отправить комментарий.
#Авторизованный пользователь может отправить комментарий.
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), True),
        (pytest.lazy_fixture('admin_client'), False)
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
#@pytest.mark.usefixtures('form_data')
def test_anonymous_user_cant_authorised_user_can_create_comment(parametrized_client, name, args, form_data, expected_status):
    comments_count_before = Comment.objects.count()
    url = reverse(name, args = args)
    parametrized_client.post(url, data=form_data)
    #pdb.set_trace()
        # Считаем количество комментариев.
    comments_count_after = Comment.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
    assert((comments_count_before == comments_count_after) == expected_status )

#Если комментарий содержит запрещённые слова, он не будет опубликован, а форма вернёт ошибку.
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
def test_user_cant_use_bad_words(author_client, name, args):
        comments_count_before = Comment.objects.count()
        # Формируем данные для отправки формы; текст включает
        # первое слово из списка стоп-слов.
        bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
        # Отправляем запрос через авторизованный клиент.
        url = reverse(name, args = args)
        response = author_client.post(url, data=bad_words_data)
        # Проверяем, есть ли в ответе ошибка формы.
        #assertFormError(response, 'form', 'slug', errors=(note.slug + WARNING))
        assertFormError(
            response,
            form='form',
            field='text',
            errors=WARNING
        )
        # Дополнительно убедимся, что комментарий не был создан.
        comments_count_after = Comment.objects.count()
        assert(comments_count_before == comments_count_after)

#Авторизованный пользователь может редактировать или удалять свои комментарии.
#Авторизованный пользователь не может редактировать или удалять чужие комментарии.
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('pk_for_args_comment')),
    )
)
@pytest.mark.usefixtures('pk_for_args_comment')
def test_author_can_delete_comment(author_client, name, args, urls):
    pdb.set_trace()
        # От имени автора комментария отправляем DELETE-запрос на удаление.
    comments_count_before = Comment.objects.count()
    url = reverse(name, args = args)
    response = author_client.delete(url)
    url_to_comments = urls['url_to_comments'] + '#comments' 
        # Проверяем, что редирект привёл к разделу с комментариями.
        # Заодно проверим статус-коды ответов.
    assertRedirects(response, url_to_comments)
      # Считаем количество комментариев в системе.
    comments_count_after = Comment.objects.count()
        # Ожидаем ноль комментариев в системе.
    assert(comments_count_after == comments_count_before)

