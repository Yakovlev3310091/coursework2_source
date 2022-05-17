import pytest

from app.posts.dao.comments_dao import CommentsDAO

class TestCommentsDao:

    @pytest.fixture()
    def comments_dao(self):
        return CommentsDAO("tests/mock/comments.json")

    @pytest.fixture()
    def keys_expected(self):
        return {"post_pk", "commenter_name", "comment", "pk"}

    # получение комментариев к посту

    def test_get_by_post_pk_check_type(self, comments_dao):
        comments = comments_dao.get_by_post_pk(1)
        assert type(comments) == list, "Результат должен быть списком"
        assert type(comments[0]) == dict, "Результат должен быть словарем"

    def test_get_by_post_pk_check_keys(self, comments_dao, keys_expected):
        comment = comments_dao.get_by_post_pk(1)[0]
        comment_keys = set(comment.keys())
        assert comment_keys == keys_expected, "Список ключей не соответствует"


    parameters_for_post_and_comments = [
        (1, {1, 2}),
        (2, {7}),
        (0, set())
    ]

    @pytest.mark.parametrize("post_pk, correct_comments_pks", parameters_for_post_and_comments)
    def test_get_by_post_pk_check_match(self, comments_dao, post_pk, correct_comments_pks):
        """ проверка выбора коммента по pk поста"""
        comments = comments_dao.get_by_post_pk(post_pk)
        comment_pks = set([comment["pk"] for comment in comments])
        assert comment_pks == comment_pks, f"Не совпадает pk коммента для поста{post_pk}"
