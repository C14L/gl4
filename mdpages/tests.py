from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from mdpages.models import Article, Topic


class MdpagesTestCase(TestCase):
    topic_title = 'Some Topiic'
    topic_auto_slug = 'some-topiic'
    page_title = 'Some $!# title /#hk/dj$#fysu'
    page_auto_slug = 'some-title-hkdjfysu'
    page_manual_slug = 'manual-slug-8hsk'
    page_text = 'This is the do97fsihf page text.'

    username = 'mainuser'
    email = 'mainuser@example.com'
    password = 'hunter2'

    def setUp(self):
        args = [self.username, self.email, self.password]
        try:
            self.mainuser = User.objects.get(username=args[0])
        except User.DoesNotExist:
            self.mainuser = User.objects.create_user(*args)

        self.topic, created = Topic.objects.get_or_create(title=self.topic_title)

        self.article, created = Article.objects.get_or_create(
            title=self.page_title, text=self.page_text,
            user=self.mainuser, topic=self.topic, is_published=True)

        self.url = reverse('mdpages_article',
                           args=[self.topic.slug, self.article.slug])

    def tearDown(self):
        # self.mainuser.delete()
        pass

    def test_create_page(self):
        self.assertEqual(self.topic.slug, self.topic_auto_slug)
        self.assertEqual(self.article.slug, self.page_auto_slug)
        self.article.slug = self.page_manual_slug
        self.article.save()
        self.assertEqual(self.article.slug, self.page_manual_slug)

    def test_view_page(self):
        url = reverse('mdpages_article', args=[self.topic.slug,
                                               self.article.slug])
        response = self.client.get(url)
        self.assertContains(response, self.page_title)
        self.assertContains(response, self.page_text)

    def test_view_page_with_safe_html_and_markdown(self):
        """Assert that markdown and safe HTML is rendered."""
        res1 = '<a href="https://example.com">link</a>'
        res2 = '<a href="https://example.org/">markdown text</a>'
        self.article.text = ('Text <a href="https://example.com">link</a>.\n\n'
                             'And [markdown text](https://example.org/) too.')
        self.article.save()
        response = self.client.get(self.url)
        self.assertContains(response, res1)
        self.assertContains(response, res2)

    # def test_view_page_with_unsafe_html(self):
    #     """Assert that unsafe HTML is removed when pages render."""
    #     self.article.text = '<a href="javascript:alert(\'h4x0R\')">3v1l</a>'
    #     self.article.save()
    #     response = self.client.get(self.url)
    #     self.assertNotContains(response, self.article.text)

    def test_display_edit_btn_only_for_auth_user(self):
        args = [self.article.pk]
        admin_url = reverse('admin:mdpages_article_change', args=args)
        page_url = reverse('mdpages_article', args=[self.topic.slug,
                                                    self.article.slug])
        # Anon can NOT see the button
        response = self.client.get(page_url)
        self.assertNotContains(response, admin_url)

        # Regular user can NOT see the button
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(page_url)
        self.assertNotContains(response, admin_url)

        # Auth is_staff user can.
        self.mainuser.is_staff = True
        self.mainuser.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(page_url)
        self.assertContains(response, admin_url)
