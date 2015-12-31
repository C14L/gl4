from django.test import TestCase
from django.contrib.auth.models import User
from companydb.models import UserProfile, Stock, Project, Group
from stonedb.models import Stone


class CompanydbTestCase(TestCase):
    def setUp(self):
        self.mainuser = User.objects.create_user('mainuser')
        self.stone = Stone.objects.create(name='Test Stone', slug='test-stone')
        self.group = Group.objects.create(name='Test Group', slug='test-group')

    def test_create_delete_user(self):
        user = User.objects.create_user('testuser')
        Stock.objects.create(user=user, stone=self.stone)
        Project.objects.create(user=user, stone=self.stone)
        self.group.members.add(user)

        qs1 = UserProfile.objects.filter(user=user)
        qs2 = Stock.objects.filter(user=user, stone=self.stone)
        qs3 = Project.objects.filter(user=user, stone=self.stone)
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
