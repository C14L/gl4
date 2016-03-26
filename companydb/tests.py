from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from companydb.models import UserProfile, Stock, Project, Group
from stonedb.models import Stone


class CompanydbTestCase(TestCase):
    def setUp(self):
        args = ['mainuser', 'mainuser@example.com', 'hunter2']
        self.mainuser = User.objects.create_user(*args)
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
        username = 'mainuser'
        pages = ['companydb_stock_detail_new', 'companydb_projects_detail_new',
                 'companydb_delete', 'companydb_details',
                 'companydb_about', 'companydb_areas']
        for p in pages:
            request_url = reverse(p, args=[username])
            redirect_url = reverse('account_login') + '?next=' + request_url
            response = self.client.get(request_url, follow=True)
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

        a = {'args': [username]}
        pages = [
            ('companydb/item.html', reverse('companydb_item', **a), 1),
            ('companydb/projects.html', reverse('companydb_projects', **a), 1),
            ('companydb/stock.html', reverse('companydb_stock', **a), 1),
            ('companydb/photos.html', reverse('companydb_photos', **a), 0),
            ('companydb/contact.html', reverse('companydb_contact', **a), 0), ]
        for p in pages:
            response = self.client.get(p[1])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, p[0])
            if p[2] == 1:
                self.assertContains(response, x, msg_prefix=p[0] + '; ' + p[1])

        user.delete()

    def test_only_auth_user_can_access_photo_upload(self):
        """
        For anon and auth user, look for upload form on photos page and POST
        to upload URL.
        """
        username = 'testuser3'
        user = User.objects.create_user(username, 'xyz@example.com', 'hunter2')
        target_url = reverse('companydb_photos', args=[username])
        redirect_url = reverse('account_login') + '?next=' + target_url

        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'multipart/form-data')
        response = self.client.post(target_url)
        self.assertRedirects(response, redirect_url)

        self.client.login(username="testuser3", password="hunter2")
        response = self.client.get(target_url)
        self.assertContains(response, 'multipart/form-data')
        response = self.client.post(target_url)
        self.assertEqual(response.status_code, 200)

        user.delete()

    def test_auth_user_can_add_delete_profile_photo(self):
        pass

    def test_only_auth_user_can_edit_profile(self):
        username, password = 'mainuser', 'hunter2'
        url = reverse('companydb_details', args=[username])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'name': 'yioljdjkghlksdhlgskgh',
                'contact': '894yirlgyfuygfidbyl',
                'contact_position': 'oie7rykifhdshg',
                'street': '988ferihugd',
                'city': 'fsfdglydflgdfkh',
                'zip': 'f98alaighflskhf',
                'country_sub_name': 'e0piqweyhgfbvk',
                'country_name': '29olhglk.,jufa',
                'tel': 'fowhfljsdfljs',
                'mobile': 'r8oiuqgehldjflakdh',
                'web': 'wfyeloufkdhlfjs', }
        response = self.client.post(url, data=data, follow=True)
        for k, v in data.items():
            self.assertContains(response, v)

    def test_only_auth_user_can_add_edit_delete_stock(self):
        pass

    def test_only_auth_user_can_add_delete_stock_photo(self):
        pass

    def test_only_auth_user_can_add_edit_delete_project(self):
        pass

    def test_only_auth_user_can_add_delete_project_photo(self):
        pass
