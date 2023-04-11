from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, TEXT_LENGTH

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names_for_group(self):
        """Проверяем, что у моделей корректно работает __str__ у group."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_models_have_correct_object_names_for_post(self):
        """Проверяем, что у моделей корректно работает __str__ у post."""
        post = PostModelTest.post
        expected_object_name = post.text[:TEXT_LENGTH]
        self.assertEqual(expected_object_name, str(post))
