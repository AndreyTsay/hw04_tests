from http import HTTPStatus

from django import forms
from django.contrib.auth import get_user_model
from django.core.paginator import Page
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group
from posts.views import NUMBER_OF_POSTS
from posts.tests.constants import (

    GROUP_LIST_TEMPLATE,
    GROUP_LIST_URL_NAME,
    INDEX_TEMPLATE,
    INDEX_URL_NAME,
    PROFILE_URL_NAME,
    PROFILE_URL_TEMPLATE,
    POST_DETAIL_URL_NAME,
    POST_DETAIL_URL_TEMPLATE,
    POST_EDIT_URL_NAME,
    POST_EDIT_URL_NAME_TEMPLATE,
    POST_CREATE_URL_NAME,
    POST_CREATE_URL_TEMPLATE
)

User = get_user_model()


class PaginatorViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='NAY')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug21',
            description='Тестовое описание',
        )
        self.post = Post.objects.create(
            author=self.user,
            text='Hoho',
            group=self.group,
        )

    def test_paginator_index(self):
        url_expected_post_number = {
            INDEX_URL_NAME: (
                {},
                Post.objects.all()[:NUMBER_OF_POSTS]
            ),
        }
        for url_name, params in url_expected_post_number.items():
            kwargs, queryset = params
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                page_obj = response.context.get('page_obj')
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertQuerysetEqual(
                    page_obj, queryset, lambda x: x
                )

    def test_paginator_group_list(self):
        url_expected_post_number = {
            GROUP_LIST_URL_NAME: (
                {'slug': self.group.slug},
                self.group.posts.all()[:NUMBER_OF_POSTS]
            ),
        }
        for url_name, params in url_expected_post_number.items():
            kwargs, queryset = params
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                page_obj = response.context.get('page_obj')
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertQuerysetEqual(
                    page_obj, queryset, lambda x: x
                )

    def test_paginator_profile(self):
        url_expected_post_number = {
            PROFILE_URL_NAME: (
                {'username': self.user.username},
                self.user.posts.all()[:NUMBER_OF_POSTS]
            ),
        }
        for url_name, params in url_expected_post_number.items():
            kwargs, queryset = params
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                page_obj = response.context.get('page_obj')
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertQuerysetEqual(
                    page_obj, queryset, lambda x: x
                )

    def test_pages_show_correct_context(self):
        """Шаблоны index, group_list, profile сформированы
        с правильным контекстом.
        """
        data = {
            INDEX_URL_NAME: (
                INDEX_TEMPLATE, {}
            ),
            GROUP_LIST_URL_NAME: (
                GROUP_LIST_TEMPLATE, {'slug': self.group.slug}
            ),
            PROFILE_URL_NAME: (
                PROFILE_URL_TEMPLATE, {'username': self.user.username}
            )}

        for url_name, params in data.items():
            with self.subTest(url_name=url_name):
                template, kwargs = params
                response = self.authorized_client.get(
                    reverse(url_name, kwargs=kwargs))
                page_obj = response.context.get('page_obj')
                text = self.post
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
                self.assertIn(text, page_obj)


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NAY')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug21',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая запись",
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_templates(self):
        data = {
            INDEX_URL_NAME: (
                INDEX_TEMPLATE, {}
            ),
            GROUP_LIST_URL_NAME: (
                GROUP_LIST_TEMPLATE, {'slug': self.group.slug}
            ),
            PROFILE_URL_NAME: (
                PROFILE_URL_TEMPLATE, {'username': self.user.username}
            ),
            POST_DETAIL_URL_NAME: (
                POST_DETAIL_URL_TEMPLATE, {'post_id': self.post.id}
            ),
            POST_EDIT_URL_NAME: (
                POST_EDIT_URL_NAME_TEMPLATE, {'post_id': self.post.id}
            ),
            POST_CREATE_URL_NAME: (
                POST_CREATE_URL_TEMPLATE, {}
            ),
        }
        for url_name, params in data.items():
            with self.subTest(url_name=url_name):
                template, kwargs = params
                response = self.authorized_client.get(
                    reverse(url_name, kwargs=kwargs))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_paginator_profile(self):
        url_expected_post_number = {
            PROFILE_URL_NAME: (
                {'username': self.user.username},
                self.user.posts.all()[:NUMBER_OF_POSTS]
            ),
        }
        for url_name, params in url_expected_post_number.items():
            kwargs, queryset = params
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name, kwargs=kwargs))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                page_obj = response.context.get('page_obj')
                self.assertIsNotNone(page_obj)
                self.assertIsInstance(page_obj, Page)
                self.assertQuerysetEqual(
                    page_obj, queryset, lambda x: x
                )

    def test_posts_index_page_show_correct_context(self):
        """Шаблон posts/index сформирован с правильным контекстом."""
        response = self.client.get(reverse(INDEX_URL_NAME))
        page_context = (
            'title',
            'page_obj',
        )
        for value in page_context:
            self.assertIn(value, response.context)
        expected = list(Post.objects.all()[:NUMBER_OF_POSTS])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_group_list_show_correct_context(self):
        """Список постов в шаблоне group_list равен ожидаемому контексту."""
        response = self.client.get(
            reverse(GROUP_LIST_URL_NAME, kwargs={"slug": self.group.slug})
        )
        page_context = (
            'page_obj',
            'group',
        )
        for value in page_context:
            self.assertIn(value, response.context)
        expected = list(
            Post.objects.filter(group_id=self.group.id)[:NUMBER_OF_POSTS])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_profile_show_correct_context(self):
        """Список постов в шаблоне profile равен ожидаемому контексту."""
        response = self.client.get(
            reverse(PROFILE_URL_NAME, args=(self.user.username,))
        )
        page_context = (
            'page_obj',
            'author',
        )
        for value in page_context:
            self.assertIn(value, response.context)
        expected = list(
            Post.objects.filter(author_id=self.user.id)[:NUMBER_OF_POSTS])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(POST_DETAIL_URL_NAME, kwargs={'post_id': self.post.id}))
        page_context = (
            'post',
            'post_count',
        )
        for value in page_context:
            self.assertIn(value, response.context)
        response_to_post = response.context['post']
        post_text = {response_to_post.text: 'Тестовый пост',
                     response_to_post.group: self.group,
                     response_to_post.author: self.user.username}
        for value, expected in post_text.items():
            self.assertEqual(post_text[value], expected)

    def test_post_create_page_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(POST_CREATE_URL_NAME))
        page_context = (
            'form',
        )
        for value in page_context:
            self.assertIn(value, response.context)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField}
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_check_group_not_in_mistake_group_list_page(self):
        """Проверяем чтобы созданный Пост с группой не попап в чужую группу."""
        form_fields = {
            reverse(
                GROUP_LIST_URL_NAME, kwargs={"slug": self.group.slug}
            ): Post.objects.exclude(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context.get("page_obj")
                self.assertNotIn(expected, form_field)
