import pytest
from support_api.models import Post


class TestPostAPI:

    @pytest.mark.django_db(transaction=True)
    def test_post_not_found(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code != 404, 'Страница `/api/v1/posts/` не найдена'

    @pytest.mark.django_db(transaction=True)
    def test_post_not_auth(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code == 401, \
            'Проверьте, что `/api/v1/posts/` при запросе без токена возвращаете статус 401'

    @pytest.mark.django_db(transaction=True)
    def test_posts_get(self, user_client, post, another_post):
        response = user_client.get('/api/v1/posts/')
        assert response.status_code == 200, \
            'При GET запросе `/api/v1/posts/` с токеном авторизации не возвращаетсся статус 200'

        test_data = response.json()
        assert len(test_data) == Post.objects.count(), \
            'При GET запросе на `/api/v1/posts/` не возвращается весь список постов'

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user_client1, admin, another_user):
        post_count = Post.objects.count()

        data = {}
        response = user_client1.post('/api/v1/posts/', data=data)
        assert response.status_code == 400, \
            'При POST запросе на `/api/v1/posts/` с не правильными данными не возвращается статус 400'

        data = {'author': another_user.id, 'text': 'Статья номер 3'}
        response = user_client1.post('/api/v1/posts/', data=data)
        assert response.status_code == 201, \
            'При POST запросе на `/api/v1/posts/` с правильными данными не возвращается статус 201'

        test_data = response.json()
        msg_error = 'Проверьте, что при POST запросе на `/api/v1/posts/` возвращается словарь с данными новой статьи'
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == another_user.username, \
            'При POST запросе на `/api/v1/posts/` не создается статья от авторизованного пользователя'
        assert post_count + 1 == Post.objects.count(), \
            'При POST запросе на `/api/v1/posts/` не создается статья'

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_client, post, admin):
        response = user_client.get(f'/api/v1/posts/{post.id}/')
        assert response.status_code == 200, \
            'Страница `/api/v1/posts/{id}/` не найдена'

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_client, user_client1, post, another_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 200, \
            'При PATCH запросе `/api/v1/posts/{id}/` не возвращается статус 200'

        test_post = Post.objects.filter(id=post.id).first()

        assert test_post.text == 'Поменяли текст статьи', \
            'При PATCH запросе `/api/v1/posts/{id}/` не изменяется статья'

        response = user_client1.patch(f'/api/v1/posts/{post.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 403, \
            'При PATCH запросе `/api/v1/posts/{id}/` для не своей статьи возвращается статус 403'

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_client, user_client1, post, another_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 204, \
            'При DELETE запросе `/api/v1/posts/{id}/` возвращается статус 204'

        test_post = Post.objects.filter(id=post.id).first()

        assert not test_post, 'При DELETE запросе `/api/v1/posts/{id}/` не удаляется статья'

        response = user_client1.delete(f'/api/v1/posts/{another_post.id}/')

        assert response.status_code == 403, \
            'При DELETE запросе `/api/v1/posts/{id}/` для не своей статьи не возвращается статус 403'
