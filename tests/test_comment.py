import pytest
from support_api.models import Comment


class TestCommentAPI:

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_found(self, user_client, post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code != 404, \
            'Страница `/api/v1/posts/{post.id}/comments/` не найдена, проверьте этот адрес в *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_comments_get(self, user_client, post, comment_1_post, comment_2_post, comment_1_another_post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code == 200, \
            'При GET запросе `/api/v1/posts/{post.id}/comments/` ' \
            'с токеном авторизации не возвращаетсся статус 200'

    @pytest.mark.django_db(transaction=True)
    def test_comments_create(self, user_client, post, admin, another_user):
        comments_count = Comment.objects.count()

        data = {}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, \
            'При POST запросе на `/api/v1/posts/{post.id}/comments/` ' \
            'с не правильными данными не возвращается статус 400'

        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 201, \
            'При POST запросе на `/api/v1/posts/{post.id}/comments/` ' \
            'с правильными данными не возвращается статус 201'

        test_data = response.json()
        msg_error = 'При POST запросе на `/api/v1/posts/{post.id}/comments/` не' \
                    'возвращается словарь с данными нового комментария'
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == admin.username, \
            'При POST запросе на `/api/v1/posts/{post.id}/comments/` не' \
            'создается комментарий от авторизованного пользователя'
        assert comments_count + 1 == Comment.objects.count(), \
            'При POST запросе на `/api/v1/posts/{post.id}/comments/` не создается комментарий'

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_client, post, comment_1_post, admin):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 200, \
            'Страница `/api/v1/posts/{post.id}/comments/{comment.id}/` не найдена'

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/',
                                     data={'text': 'Поменяли текст коммента'})

        assert response.status_code == 200, \
            'При PATCH запросе `/api/v1/posts/{post.id}/comments/{comment.id}/` не' \
            'возвращается статус 200'

        test_comment = Comment.objects.filter(id=comment_1_post.id).first()

        assert test_comment.text == 'Поменяли текст коммента', \
            'При PATCH запросе `/api/v1/posts/{id}/` вы изменяется статья'

        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 403, \
            'При PATCH запросе `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'для не своей статьи не возвращается статус 403'

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 204, \
            'При DELETE запросе `/api/v1/posts/{post.id}/comments/{comment.id}/` не возвращается статус 204'

        test_comment = Comment.objects.filter(id=post.id).first()

        assert not test_comment, \
            'При DELETE запросе `/api/v1/posts/{post.id}/comments/{comment.id}/` не удалили комментарий'

        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/')

        assert response.status_code == 403, \
            'При DELETE запросе `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'для не своего комментария возвращается статус 403'

    def test_status_comment(self, another_user, user_client, post, comment_1_post):
        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        response = user_client.get(f'/api/v1/posts/{post.id}/')
        assert response.json().get('status') == 'In progress', 'После добавления комментария статус поста не ' \
                                                               'изменяется на In progress '

    def test_status_comment_close(self, another_user, user_client, post, comment_1_post):
        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        data_status = {'status': 'Close'}
        user_client.patch(f'/api/v1/posts/{post.id}/', data=data_status)
        user_client.get(f'/api/v1/posts/{post.id}/')
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, 'Нельзя добавить комментарий к уже закрытому посту'
