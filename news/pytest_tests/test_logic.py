import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING


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
def test_anonymous_user_cant_authorised_user_can_create_comment(parametrized_client, name, args, form_data, expected_status):
    '''Анонимный пользователь не может отправить комментарий.
    Авторизованный пользователь может отправить комментарий.'''
    comments_count_before = Comment.objects.count()
    url = reverse(name, args = args)
    parametrized_client.post(url, data=form_data)
    comments_count_after = Comment.objects.count()
    assert((comments_count_before == comments_count_after) == expected_status )


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
def test_user_cant_use_bad_words(author_client, name, args):
    '''Если комментарий содержит запрещённые слова, он 
    не будет опубликован, а форма вернёт ошибку.'''
    comments_count_before = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse(name, args = args)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count_after = Comment.objects.count()
    assert(comments_count_before == comments_count_after)

@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('pk_for_args_comment')),
    )
)
@pytest.mark.django_db
def test_author_can_delete_comment(author_client, name, args, news,):
    '''Авторизованный пользователь может удалять свои комментарии.'''
    comments_count_before = Comment.objects.count()
    url = reverse(name, args = args)
    response = author_client.delete(url)
    url_to_comments = reverse('news:detail',
                              args = (news.id,))  + '#comments' 
    assertRedirects(response, url_to_comments)
    comments_count_after = Comment.objects.count()
    assert(comments_count_after == comments_count_before-1)

@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('pk_for_args_comment')),
    )
)
@pytest.mark.django_db
def test_author_can_edit_comment(author_client, name, args, comment, news,form_data):
    '''Авторизованный пользователь может редактировать свои комментарии.'''
    url = reverse(name, args = args)
    response = author_client.post(url, data=form_data)
    url_to_comments = reverse('news:detail',
                              args = (news.id,))  + '#comments' 
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert(comment.text == form_data['text'])

@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('pk_for_args_comment')),
    )
)
@pytest.mark.django_db
def test_user_cant_delete_comment(reader_client, name, args):
    '''Авторизованный пользователь не может удалять чужие комментарии.'''
    comments_count_before = Comment.objects.count()
    url = reverse(name, args = args)
    response = reader_client.delete(url)
    assert(response.status_code == HTTPStatus.NOT_FOUND)
    comments_count_after = Comment.objects.count()
    assert(comments_count_after == comments_count_before)

@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('pk_for_args_comment')),
    )
)
@pytest.mark.django_db
def test_user_cant_edit_comment(reader_client, name, args, comment,form_data):
    '''Авторизованный пользователь не может редактировать чужие комментарии.'''
    comment_text_before = comment.text
    url = reverse(name, args = args)
    response = reader_client.post(url, form_data)
    assert(response.status_code == HTTPStatus.NOT_FOUND)
    comment.refresh_from_db()
    assert(comment.text == comment_text_before)
