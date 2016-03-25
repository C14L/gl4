from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from companydb.models import UserProfile, Stock, Project, Group
from stonedb.models import Stone


class CompanydbTestCase(TestCase):
    def setUp(self):
        self.mainuser = User.objects.create_user('mainuser')
        self.stone = Stone.objects.create(name='Test Stone', slug='test-stone')
        self.group = Group.objects.create(name='Test Group', slug='test-group')

    def test_create_delete_user(self):
        """
        User, Stock, Project, and Group membership can be created. And when the
        user is deleted, all related items are removed as well.
        """
        user = User.objects.create_user('testuser')
        Stock.objects.create(user=user, stone=self.stone)
        Project.objects.create(user=user).stones.add(self.stone)
        self.group.members.add(user)

        qs1 = UserProfile.objects.filter(user=user)
        qs2 = Stock.objects.filter(user=user, stone=self.stone)
        qs3 = Project.objects.filter(user=user, stones=self.stone)
        qs4 = self.group.members.filter(pk=user.id)

        # assert they all exist
        self.assertTrue(qs1.exists())
        self.assertTrue(qs2.exists())
        self.assertTrue(qs3.exists())
        self.assertTrue(qs4.exists())

        user.delete()

        # assert all related objects are gone too
        self.assertFalse(qs1.exists())
        self.assertFalse(qs2.exists())
        self.assertFalse(qs3.exists())
        self.assertFalse(qs4.exists())

    def test_login_required_redirects_anon(self):
        """
        Make sure that certain views are not accessible by anon and redirect to
        a login view.
        """
        c = Client()
        username = 'mainuser'
        pages = ['companydb_stock_detail_new', 'companydb_projects_detail_new',
                 'companydb_delete', 'companydb_db_details',
                 'companydb_db_about', 'companydb_db_areas']
        for p in pages:
            request_url = reverse(p, args=[username])
            redirect_url = reverse('account_login') + '?next=' + request_url
            response = c.get(request_url, follow=True)
            self.assertRedirects(response, redirect_url, msg_prefix=p)

    def test_existing_user_profile_pages_viewable_by_anon(self):
        """
        A user's profile page should be viewable.
        """
        x, username = 'jd432resb98ghl', 'testuser2'
        user = User.objects.create_user(username)
        user.profile.about = x
        user.profile.save()
        Stock.objects.create(user=user, stone=self.stone, description=x)
        Project.objects.create(user=user, description=x).stones.add(self.stone)
        self.group.members.add(user)
        c, a = Client(), {'args': [username]}
        pages = [
            ('companydb/item.html', reverse('companydb_item', **a), 1),
            ('companydb/projects.html', reverse('companydb_projects', **a), 1),
            ('companydb/stock.html', reverse('companydb_stock', **a), 1),
            ('companydb/photos.html', reverse('companydb_photos', **a), 0),
            ('companydb/contact.html', reverse('companydb_contact', **a), 0),
        ]
        for p in pages:
            response = c.get(p[1])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, p[0])
            if p[2] == 1:
                self.assertContains(response, x, msg_prefix=p[0] + '; ' + p[1])

    def test_only_auth_user_can_photo_upload(self):
        """
        For anon and auth user, look for upload form on photos page and POST
        to upload URL.
        """
        c, username = Client(), 'testuser3'
        target_url = reverse('companydb_photos', args=[username])
        redirect_url = reverse('account_login') + '?next=' + target_url
        response = c.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'photo-upload-form')
        response = c.post(target_url)
        self.assertRedirects(response, redirect_url)
