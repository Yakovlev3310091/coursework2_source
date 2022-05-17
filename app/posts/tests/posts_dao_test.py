import os

import pytest

from app.posts.dao.posts_dao import PostsDAO


class TestPostsDao:

    @pytest.fixture
    def posts_dao(self):
        return PostsDAO("data/posts.json")

    @pytest.fixture
    def keys_expected(self):
        return {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    # Получение всех постов

    def test_get_all_check_type(self, posts_dao):
        posts = posts_dao.get_all()
        assert type(posts) == list, "Список постов должен быть списком"
        assert type(posts[0]) == dict, "Каждый пост должен быть словарем"


    def test_get_all_has_keys(self, posts_dao, keys_expected):
        posts = posts_dao.get_all()
        first_post = posts[0]
        first_post_keys = set(first_post.keys())
        assert first_post_keys == keys_expected, "Полученные ключи неверны"

    # Получение одного поста

    def test_get_one_check_type(self, posts_dao):
        post = posts_dao.get_by_pk(1)
        assert type(post) == dict, "Пост должен быть словарем"


    def test_get_one_has_keys(self, posts_dao, keys_expected):
        post = posts_dao.get_by_pk(1)
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи неверны"

    parameters_to_get_by_pk = [1, 2, 3, 4, 5, 6, 7, 8]

    @pytest.mark.parametrize("post_pk", parameters_to_get_by_pk)

    def test_get_one_check_type_has_correct_pk(self, posts_dao, post_pk):
        post = posts_dao.get_by_pk(post_pk)
        assert post["pk"] == post_pk, "Номер полученного поста не соответствует номеру запрошенного"

    # Получение по пользователю

    def test_get_by_user_check_type(self, posts_dao):
        posts = posts_dao.get_by_user("leo")
        assert type(posts) == list, "Результат поиска по пользователю должен быть списком"
        assert type(posts[0]) == dict, "Найденные элементы по пользователю должны быть словарями"

    def test_get_by_user_has_keys(self, posts_dao, keys_expected):
        post = posts_dao.get_by_user("leo")[0]
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи неверны"

    parameters_to_get_by_user = [
        ("leo", [1, 5]),
        ("hank", [3, 7]),
        ("johnny", [2, 6]),
        ("Глеб Хомутов",[])
    ]

    @pytest.mark.parametrize("poster_name, correct_pks", parameters_to_get_by_user)
    def test_get_by_user_correct_match(self, posts_dao, poster_name, correct_pks):
        """ Проверяет правильность работы по поиску пользователя"""
        posts = posts_dao.get_by_user(poster_name)
        pks = []
        for post in posts:
            pks.append(post["pk"])
        assert pks == correct_pks, f"Неверный список постов для пользователя {poster_name}"
    #
    # Получение по поиску постов

    def test_search_check_type(self, posts_dao):
        posts = posts_dao.search("а")
        assert type(posts) == list, "Результат поиска должен быть списком"
        assert type(posts[0]) == dict, "Найденные элементы должны быть словарями"

    def test_search_has_keys(self, posts_dao, keys_expected):
        post = posts_dao.search("а")[0]
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи неверны"

    queries_and_responses = [
        ("000000", []),
        ("еда", [1]),
        ("дом", [2, 7, 8]),
        ("Дом", [2, 7, 8]),
        ("а", list(range(1, 9)))
    ]

    @pytest.mark.parametrize("query, correct_pks", queries_and_responses)
    def test_search_correct_match(self, posts_dao, query, correct_pks):
        posts = posts_dao.search(query)
        pks = []
        for post in posts:
            pks.append(post["pk"])
        assert pks == correct_pks, f"Неверный поиск по запросу {query}"