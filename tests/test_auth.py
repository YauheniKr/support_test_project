import pytest
from django.conf import settings


class TestAuthAPI:

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, client, admin):
        response = client.post('/auth/jwt/create/',
                               data={'username': admin.username, 'password': '1234567'})

        assert response.status_code != 404, \
            'Page `auth/jwt/create/` не найдена'

        assert response.status_code == 200, \
            'Страница `auth/jwt/create/` работает не правильно'

        auth_data = response.json()
        assert 'access' in auth_data and auth_data.get('access'), 'При POST запросе `/auth/jwt/create/` не возвращается токен'
