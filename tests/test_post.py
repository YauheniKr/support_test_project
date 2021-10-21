import pytest
from support_api.models import Post


class TestPostAPI:

    @pytest.mark.django_db(transaction=True)
    def test_post_not_found(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code != 404, 'Page `/api/v1/posts/` not found'

    @pytest.mark.django_db(transaction=True)
    def test_post_not_auth(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code == 401, \
            'Check `/api/v1/posts/` without token returns status 401'

    @pytest.mark.django_db(transaction=True)
    def test_posts_get(self, user_client, post, another_post):
        response = user_client.get('/api/v1/posts/')
        assert response.status_code == 200, \
            'GET request `/api/v1/posts/` with token not returns status 200'

        test_data = response.json()
        assert len(test_data) == Post.objects.count(), \
            'GET request `/api/v1/posts/` post lists not returns'

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user_client1, admin, another_user):
        post_count = Post.objects.count()

        data = {}
        response = user_client1.post('/api/v1/posts/', data=data)
        assert response.status_code == 400, \
            'POST request  `/api/v1/posts/` with incorrect data not return 400'

        data = {'author': another_user.id, 'text': 'Статья номер 3'}
        response = user_client1.post('/api/v1/posts/', data=data)
        assert response.status_code == 201, \
            'POST request `/api/v1/posts/` with correct data not return status 201'

        test_data = response.json()
        msg_error = 'POST request `/api/v1/posts/` not return dict with new post data'
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == another_user.username, \
            'POST request `/api/v1/posts/` not create post from auth user'
        assert post_count + 1 == Post.objects.count(), \
            'POST request `/api/v1/posts/` not create post'

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_client, post, admin):
        response = user_client.get(f'/api/v1/posts/{post.id}/')
        assert response.status_code == 200, \
            'Page `/api/v1/posts/{id}/` not found'

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_client, user_client1, post, another_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/',
                                     data={'text': 'Post changed'})

        assert response.status_code == 200, \
            'PATCH request `/api/v1/posts/{id}/` not return status 200'

        test_post = Post.objects.filter(id=post.id).first()

        assert test_post.text == 'Post changed', \
            'PATCH request `/api/v1/posts/{id}/` not change post'

        response = user_client1.patch(f'/api/v1/posts/{post.id}/',
                                     data={'text': 'Post changed'})

        assert response.status_code == 403, \
            'PATCH request `/api/v1/posts/{id}/` for not own post returns 403'

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_client, user_client1, post, another_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 204, \
            'DELETE request `/api/v1/posts/{id}/` not return status 204'

        test_post = Post.objects.filter(id=post.id).first()

        assert not test_post, 'DELETE request `/api/v1/posts/{id}/` not delete post'

        response = user_client1.delete(f'/api/v1/posts/{another_post.id}/')

        assert response.status_code == 403, \
            'DELETE request `/api/v1/posts/{id}/` for not own post return status  403'
